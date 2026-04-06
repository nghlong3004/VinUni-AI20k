import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup path so we can import internal modules from `src/`
src_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(src_dir))

from agent.camping_agent import get_camping_agent

# Load environment variables
load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Xin chào {user.mention_html()}! Tôi là trợ lý AI chuyên về Lên kế hoạch Cắm trại (Camping Trip Planner). "
        "Hãy cho tôi biết bạn muốn đi đâu, đi với ai và yêu cầu đặc biệt nào không nhé!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages by passing them to the ReAct framework."""
    user_text = update.message.text
    
    # Gửi thông báo đang xử lý
    processing_message = await update.message.reply_text("Đang suy nghĩ và lên kế hoạch cho bạn...")
    
    try:
        # Tạo agent mới cho Request này
        agent = get_camping_agent()
        
        # agent.run() là synchronous, dùng executor để không block asyncio event loop
        loop = asyncio.get_running_loop()
        final_answer = await loop.run_in_executor(None, agent.run, user_text)
        
        await processing_message.edit_text(final_answer)
    except Exception as e:
        await processing_message.edit_text(f"Đã xảy ra lỗi trong quá trình xử lý: {str(e)}")

def main() -> None:
    """Start the bot."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        print("Lỗi: TELEGRAM_BOT_TOKEN chưa được cài đặt trong file .env!")
        return

    # Tạo Application mới sử dụng python-telegram-bot v20+
    application = Application.builder().token(token).build()

    # Thêm handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Chạy bot
    print("Bot Telegram đang chạy... Nhấn Ctrl+C để dừng.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
