"""
Chatbot Baseline — Simple LLM wrapper WITHOUT tool access.

Purpose: Compare against the ReAct Agent to demonstrate that a plain
chatbot cannot reliably handle multi-step, tool-requiring queries.
"""
from typing import List, Dict, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger
from src.telemetry.metrics import tracker


CHATBOT_SYSTEM_PROMPT = """You are a helpful AI assistant.
Answer the user's questions as accurately and concisely as possible.
If you don't know something, say so — do not make up facts."""


class Chatbot:
    """
    A minimal stateless chatbot with no tool access.
    Each call is independent (no conversation memory).
    """

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def chat(self, user_input: str) -> str:
        """Send a single message and return the LLM's response."""
        logger.log_event("CHATBOT_REQUEST", {
            "input": user_input,
            "model": self.llm.model_name,
        })

        try:
            result = self.llm.generate(
                prompt=user_input,
                system_prompt=CHATBOT_SYSTEM_PROMPT,
            )
        except Exception as e:
            logger.error(f"Chatbot LLM call failed: {e}")
            return f"Error: {e}"

        tracker.track_request(
            provider=result["provider"],
            model=self.llm.model_name,
            usage=result["usage"],
            latency_ms=result["latency_ms"],
        )

        logger.log_event("CHATBOT_RESPONSE", {
            "output_preview": result["content"][:200],
            "tokens": result["usage"],
            "latency_ms": result["latency_ms"],
        })

        return result["content"].strip()
