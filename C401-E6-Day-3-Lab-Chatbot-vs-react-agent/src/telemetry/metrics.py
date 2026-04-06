import time
from typing import Dict, Any, List
from src.telemetry.logger import logger

class PerformanceTracker:
    """
    Tracking industry-standard metrics for LLMs.
    """
    PRICING_RATES_1M = {
        # OpenAI Models
        "gpt-5.2": (1.75, 14.00),
        "gpt-5-mini": (0.25, 2.00),
        "gpt-5": (1.25, 10.00),
        "gpt-4o": (2.50, 10.00),
        "gpt-4o-mini": (0.15, 0.60),
        
        
        # Google Gemini Models (Standard pricing for prompts < 128k tokens)
        "gemini-3-flash-preview": (0.50, 3.00),
        "gemini-3.1-pro-preview": (2.00, 12.00),
        "gemini-2.5-pro": (1.25, 10.00),
        "gemini-2.5-flash": (0.30, 2.50),
    }

    def __init__(self):
        self.session_metrics = []

    def track_request(self, provider: str, model: str, usage: Dict[str, int], latency_ms: int):
        """
        Logs a single request metric to our telemetry.
        """
        metric = {
            "provider": provider,
            "model": model,
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "latency_ms": latency_ms,
            "cost_estimate": self._calculate_cost(model, usage) # Mock cost calculation
        }
        self.session_metrics.append(metric)
        logger.log_event("LLM_METRIC", metric)

    def _calculate_cost(self, model: str, usage: Dict[str, int]) -> float:
        """
        TODO: Implement real pricing logic.
        For now, returns a dummy constant.
        """
        # 1. Extract token counts (default to 0 if not provided)
        # Note: Some APIs use different keys, but prompt_tokens/completion_tokens is standard
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        
        # Fallback if only total_tokens is provided
        if prompt_tokens == 0 and completion_tokens == 0:
            total = usage.get("total_tokens", 0)
            # Rough estimation: assume 50/50 split if we only have total tokens
            prompt_tokens = total / 2
            completion_tokens = total / 2

        # 2. Find the matching model pricing
        model_lower = model.lower()
        prompt_rate = 0.0
        completion_rate = 0.0
        
        # We use prefix matching so "gpt-4o-2024-05-13" matches "gpt-4o"
        for known_model, (p_rate, c_rate) in self.PRICING_RATES_1M.items():
            if known_model in model_lower:
                prompt_rate = p_rate
                completion_rate = c_rate
                break
                
        if prompt_rate == 0.0 and completion_rate == 0.0:
            print(f"Warning: Pricing for model '{model}' not found. Cost will be 0.")

        # 3. Calculate final cost
        cost = (prompt_tokens / 1_000_000) * prompt_rate + (completion_tokens / 1_000_000) * completion_rate
        
        return float(cost)

# Global tracker instance
tracker = PerformanceTracker()
