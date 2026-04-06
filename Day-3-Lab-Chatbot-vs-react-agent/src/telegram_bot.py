"""
Telegram Bot interface for the ReAct Agent / Chatbot.

Each Telegram user gets their own isolated agent instance.
The heavy LLM work runs in a thread-pool so it doesn't block
Telegram's async event loop.

Commands:
    /start      — greeting + instructions
    /help       — list available tools
    /agent      — switch to ReAct Agent mode (default)
    /chatbot    — switch to plain Chatbot mode
    /clear      — reset conversation (agent's history)
"""

import os
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from telegram import Update, constants
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from src.core.deepseek_provider import DeepSeekProvider
from src.agent.agent import ReActAgent
from src.agent.chatbot import Chatbot
from src.agent.camping_agent import CampingAgent
from src.tools.basic_tools import get_all_tools
from src.telemetry.logger import logger

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# Thread pool for running synchronous LLM calls
_executor = ThreadPoolExecutor(max_workers=4)

# ─── Per-user state ───────────────────────────────────────────────────────────
# user_id -> {"mode": "agent"|"chatbot", "agent": ReActAgent, "chatbot": Chatbot}

_user_sessions: Dict[int, dict] = {}


def _build_provider() -> DeepSeekProvider:
    return DeepSeekProvider(
        model_name=os.getenv("DEFAULT_MODEL", "deepseek-chat"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )


def _get_session(user_id: int) -> dict:
    """Return (or create) a session dict for a user."""
    if user_id not in _user_sessions:
        llm = _build_provider()
        tools = get_all_tools()
        _user_sessions[user_id] = {
            "mode": "agent",
            "agent": ReActAgent(llm=llm, tools=tools, max_steps=6),
            "chatbot": Chatbot(llm=_build_provider()),
            "camping": CampingAgent(llm=_build_provider()),
        }
    return _user_sessions[user_id]


# ─── Command Handlers ─────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tools = get_all_tools()
    tool_list = "\n".join(f"  • {t['name']}" for t in tools)
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}! I am a ReAct Agent.\n\n"
        f"I can use these tools:\n{tool_list}\n\n"
        f"Commands:\n"
        f"  /agent   - ReAct Agent mode (default)\n"
        f"  /chatbot - Plain Chatbot mode (no tools)\n"
        f"  /camping - Camping Trip Planner mode\n"
        f"  /clear   - Reset memory\n"
        f"  /help    - Show this message\n\n"
        f"Just send me a message to get started!",
        parse_mode=constants.ParseMode.HTML,
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await cmd_start(update, context)


async def cmd_agent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    session = _get_session(update.effective_user.id)
    session["mode"] = "agent"
    await update.message.reply_text(
        "Switched to ReAct Agent mode.\n"
        "I will use tools step-by-step to answer your questions."
    )


async def cmd_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    session = _get_session(update.effective_user.id)
    session["mode"] = "chatbot"
    await update.message.reply_text(
        "Switched to Chatbot mode.\n"
        "I will answer directly without using any tools."
    )


async def cmd_camping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    session = _get_session(update.effective_user.id)
    session["mode"] = "camping"
    await update.message.reply_text(
        "Da chuyen sang che do Lap Ke Hoach Cam Trai!\n\n"
        "Hay mo ta chuyen di ban muon, vi du:\n"
        "'Toi muon 30/4 nay di cam trai o dau do quanh Ha Noi, "
        "gan Gia Lam, gia dinh 4 nguoi, cho toi biet dia diem, "
        "thoi tiet, phuong tien va dung cu can chuan bi.'\n\n"
        "Toi se tu dong tim kiem thong tin va lap ke hoach day du cho ban!"
    )


async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in _user_sessions:
        del _user_sessions[user_id]
    await update.message.reply_text("Memory cleared! Starting fresh.")


# ─── Message Handler ──────────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text.strip()
    session = _get_session(user_id)
    mode = session["mode"]

    logger.log_event("TELEGRAM_MESSAGE", {
        "user_id": user_id,
        "username": update.effective_user.username,
        "mode": mode,
        "text_preview": user_text[:100],
    })

    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=constants.ChatAction.TYPING,
    )

    # Run the blocking LLM call in a thread so we don't freeze the bot
    loop = asyncio.get_event_loop()
    try:
        if mode == "agent":
            answer = await loop.run_in_executor(
                _executor, session["agent"].run, user_text,
            )
        elif mode == "camping":
            answer = await loop.run_in_executor(
                _executor, session["camping"].run, user_text,
            )
        else:
            answer = await loop.run_in_executor(
                _executor, session["chatbot"].chat, user_text,
            )
    except Exception as e:
        log.error(f"Error handling message from {user_id}: {e}", exc_info=True)
        answer = f"Sorry, something went wrong:\n{e}"

    # Telegram message limit is 4096 chars — split if needed
    for chunk in _split_message(answer):
        await update.message.reply_text(chunk)


def _split_message(text: str, max_len: int = 4096) -> list[str]:
    """Split long text into chunks that fit Telegram's limit."""
    if len(text) <= max_len:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:max_len])
        text = text[max_len:]
    return chunks


# ─── Bot Entry Point ──────────────────────────────────────────────────────────

def run_telegram_bot(token: str) -> None:
    """Build and start the Telegram bot (blocking call)."""
    log.info("Starting Telegram bot...")

    app = (
        Application.builder()
        .token(token)
        .build()
    )

    # Register handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("agent", cmd_agent))
    app.add_handler(CommandHandler("chatbot", cmd_chatbot))
    app.add_handler(CommandHandler("camping", cmd_camping))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    log.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
