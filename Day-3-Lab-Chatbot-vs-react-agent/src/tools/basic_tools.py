"""
Basic tools for the ReAct Agent.
Each tool is a Python function. Register them via get_all_tools().
"""
import math
import re
import requests
from datetime import datetime


# ─── Tool Functions ───────────────────────────────────────────────────────────

def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.
    Examples: '2 + 2', 'sqrt(16)', '100 * 3.14 / 2'
    """
    try:
        # Allow only safe math operations
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        allowed.update({"abs": abs, "round": round, "int": int, "float": float})
        # Strip anything that isn't a math token
        safe_expr = re.sub(r"[^0-9+\-*/().,\s\w]", "", expression)
        result = eval(safe_expr, {"__builtins__": {}}, allowed)
        return f"{result}"
    except Exception as e:
        return f"Calculator error: {e}. Check your expression syntax."


def get_current_time(timezone: str = "UTC") -> str:
    """
    Return the current date and time.
    timezone argument is informational only (returns system local time).
    """
    now = datetime.now()
    return f"Current date/time: {now.strftime('%Y-%m-%d %H:%M:%S')} (local system time)"


def search_wikipedia(query: str) -> str:
    """
    Fetch a short summary from Wikipedia for the given query.
    Uses the Wikipedia REST API (no API key required).
    """
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query)}"
        response = requests.get(url, timeout=8, headers={"User-Agent": "ReActAgent/1.0"})
        if response.status_code == 200:
            data = response.json()
            extract = data.get("extract", "")
            title = data.get("title", query)
            # Truncate to keep context manageable
            if len(extract) > 500:
                extract = extract[:497] + "..."
            return f"[Wikipedia: {title}]\n{extract}"
        elif response.status_code == 404:
            return f"Wikipedia: No article found for '{query}'. Try a different search term."
        else:
            return f"Wikipedia API error: HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return "Wikipedia search timed out. Try again or rephrase your query."
    except Exception as e:
        return f"Wikipedia search failed: {e}"


def word_count(text: str) -> str:
    """Count words and characters in the given text."""
    words = len(text.split())
    chars = len(text)
    return f"Word count: {words} words, {chars} characters."


# ─── Tool Registry ────────────────────────────────────────────────────────────

TOOL_REGISTRY = {
    "calculator": {
        "name": "calculator",
        "description": (
            "Evaluate mathematical expressions. "
            "Input: a math expression string like '2 * (3 + 4)' or 'sqrt(144)'. "
            "Use for any arithmetic or math computation."
        ),
        "function": calculator,
    },
    "get_current_time": {
        "name": "get_current_time",
        "description": (
            "Get the current date and time. "
            "Input: optional timezone string (e.g. 'UTC', 'Asia/Ho_Chi_Minh'). "
            "Use whenever the user asks about the current time or date."
        ),
        "function": get_current_time,
    },
    "search_wikipedia": {
        "name": "search_wikipedia",
        "description": (
            "Search Wikipedia for factual information about a topic. "
            "Input: a search query string (e.g. 'Python programming language'). "
            "Use for general knowledge questions, definitions, or historical facts."
        ),
        "function": search_wikipedia,
    },
    "word_count": {
        "name": "word_count",
        "description": (
            "Count the number of words and characters in a text. "
            "Input: the text string to count. "
            "Use when the user asks about the length of a piece of text."
        ),
        "function": word_count,
    },
}


def get_all_tools() -> list:
    """Return all tools as a list of dicts (name, description, function)."""
    return list(TOOL_REGISTRY.values())


def get_tool_by_name(name: str):
    """Return a single tool dict by name, or None if not found."""
    return TOOL_REGISTRY.get(name)
