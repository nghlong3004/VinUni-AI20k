"""
run.py — Interactive runner to test Chatbot vs ReAct Agent vs Camping Planner.

Usage:
    python run.py --mode agent          # ReAct Agent (default)
    python run.py --mode chatbot        # Simple chatbot baseline
    python run.py --mode compare        # Side-by-side comparison
    python run.py --mode camping        # Camping Trip Planner Agent
    python run.py --mode telegram       # Telegram Bot

Demo camping question:
    "Toi muon 30/4 nay di cam trai o dau do quanh HN, gan Gia Lam, gia dinh 4 nguoi"
"""
import os
import sys
import argparse
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from src.core.deepseek_provider import DeepSeekProvider
from src.agent.agent import ReActAgent
from src.agent.chatbot import Chatbot
from src.tools.basic_tools import get_all_tools


# ─── Provider Factory ─────────────────────────────────────────────────────────

def build_provider():
    provider_name = os.getenv("DEFAULT_PROVIDER", "deepseek").lower()
    model = os.getenv("DEFAULT_MODEL", "deepseek-chat")

    if provider_name == "deepseek":
        return DeepSeekProvider(
            model_name=model,
            api_key=os.getenv("DEEPSEEK_API_KEY"),
        )
    elif provider_name == "google":
        from src.core.gemini_provider import GeminiProvider
        return GeminiProvider(
            model_name=model,
            api_key=os.getenv("GEMINI_API_KEY"),
        )
    elif provider_name == "openai":
        from src.core.openai_provider import OpenAIProvider
        return OpenAIProvider(
            model_name=model,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    else:
        raise ValueError(f"Unknown provider: {provider_name}. Options: deepseek | google | openai")


# ─── Modes ────────────────────────────────────────────────────────────────────

def run_agent_interactive():
    llm = build_provider()
    tools = get_all_tools()
    agent = ReActAgent(llm=llm, tools=tools, max_steps=6)

    print(f"\n{'='*60}")
    print(f"  [ReAct Agent]  Model: {llm.model_name}")
    print(f"  Tools: {', '.join(t['name'] for t in tools)}")
    print(f"{'='*60}")
    print("  Type your question. Press Ctrl+C or type 'exit' to quit.")
    print(f"{'='*60}\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input or user_input.lower() in ("exit", "quit", "q"):
                print("Goodbye!")
                break
            answer = agent.run(user_input)
            print(f"\n[Agent]: {answer}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


def run_chatbot_interactive():
    llm = build_provider()
    chatbot = Chatbot(llm=llm)

    print(f"\n{'='*60}")
    print(f"  [Chatbot Baseline]  Model: {llm.model_name}")
    print(f"  (No tools -- plain LLM responses)")
    print(f"{'='*60}")
    print("  Type your question. Press Ctrl+C or type 'exit' to quit.")
    print(f"{'='*60}\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input or user_input.lower() in ("exit", "quit", "q"):
                print("Goodbye!")
                break
            answer = chatbot.chat(user_input)
            print(f"\n[Chatbot]: {answer}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


def run_compare():
    """Run both chatbot and agent on the same set of demo questions."""
    llm_agent = build_provider()
    llm_chat = build_provider()
    tools = get_all_tools()
    agent = ReActAgent(llm=llm_agent, tools=tools, max_steps=6)
    chatbot = Chatbot(llm=llm_chat)

    demo_questions = [
        "What is 1234 multiplied by 5678?",
        "What is the current time?",
        "Search Wikipedia for 'Artificial intelligence' and give me a summary.",
    ]

    print(f"\n{'='*60}")
    print("  Chatbot vs ReAct Agent -- Side-by-Side Comparison")
    print(f"{'='*60}\n")

    for i, q in enumerate(demo_questions, 1):
        print(f"Q{i}: {q}")
        print("-" * 50)

        chat_ans = chatbot.chat(q)
        print(f"[Chatbot]: {chat_ans[:300]}")
        print()

        agent_ans = agent.run(q)
        print(f"[Agent]:   {agent_ans[:300]}")
        print("=" * 60 + "\n")


def run_telegram():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        print("ERROR: Set TELEGRAM_BOT_TOKEN in your .env file.")
        print("Get a token from @BotFather on Telegram.")
        return
    from src.telegram_bot import run_telegram_bot
    run_telegram_bot(token)


def run_camping_interactive():
    llm = build_provider()
    from src.agent.camping_agent import CampingAgent
    agent = CampingAgent(llm=llm)

    print(f"\n{'='*60}")
    print(f"  [Camping Trip Planner]  Model: {llm.model_name}")
    print(f"  Tools: search_camping_sites, get_weather_forecast,")
    print(f"         get_travel_and_gear_recommendations")
    print(f"{'='*60}")
    print("  Vi du: 'Toi muon 30/4 di cam trai gan Gia Lam, HN, 4 nguoi'")
    print("  Nhan Ctrl+C hoac go 'exit' de thoat.")
    print(f"{'='*60}\n")

    while True:
        try:
            user_input = input("Ban: ").strip()
            if not user_input or user_input.lower() in ("exit", "quit", "q"):
                print("Tam biet!")
                break
            answer = agent.run(user_input)
            print(f"\n[CampBot]: {answer}\n")
        except KeyboardInterrupt:
            print("\nTam biet!")
            break


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot vs ReAct Agent Runner")
    parser.add_argument(
        "--mode",
        choices=["agent", "chatbot", "compare", "telegram", "camping"],
        default="agent",
        help="Run mode: agent | chatbot | compare | telegram | camping",
    )
    args = parser.parse_args()

    if args.mode == "agent":
        run_agent_interactive()
    elif args.mode == "chatbot":
        run_chatbot_interactive()
    elif args.mode == "compare":
        run_compare()
    elif args.mode == "telegram":
        run_telegram()
    elif args.mode == "camping":
        run_camping_interactive()
