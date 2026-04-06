import os
from typing import Optional
from src.core.openai_provider import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter provider using OpenAI-compatible Chat Completions API."""

    def __init__(self, model_name: str = "openai/gpt-4o-mini", api_key: Optional[str] = None):
        resolved_key = api_key or os.getenv("OPENROUTER_API_KEY")
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        super().__init__(
            model_name=model_name,
            api_key=resolved_key,
            base_url=base_url,
            provider_name="openrouter",
        )
