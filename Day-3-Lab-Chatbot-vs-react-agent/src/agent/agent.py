import re
from typing import List, Dict, Any, Optional, Tuple
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger
from src.telemetry.metrics import tracker


class ReActAgent:
    """
    A ReAct-style Agent following the Thought → Action → Observation loop.

    Flow:
        1. User sends a query.
        2. Agent builds a prompt with tool descriptions + conversation history.
        3. LLM responds with:
               Thought: <reasoning>
               Action: tool_name(argument)
        4. Agent parses the Action, executes the tool, appends:
               Observation: <tool result>
        5. Repeat until LLM outputs:
               Final Answer: <answer>
        6. Return the Final Answer to the user.
    """

    # Regex patterns for parsing LLM output
    _ACTION_RE = re.compile(
        r"Action\s*:\s*(\w+)\s*\(([^)]*)\)",
        re.IGNORECASE,
    )
    _FINAL_RE = re.compile(
        r"Final Answer\s*:\s*(.+)",
        re.IGNORECASE | re.DOTALL,
    )

    def __init__(
        self,
        llm: LLMProvider,
        tools: List[Dict[str, Any]],
        max_steps: int = 6,
    ):
        self.llm = llm
        self.tools = tools                        # list of {name, description, function}
        self.max_steps = max_steps
        self.history: List[Dict[str, str]] = []   # for multi-turn memory (optional)

    # ─── System Prompt ────────────────────────────────────────────────────────

    def get_system_prompt(self) -> str:
        """
        Build the system prompt that teaches the LLM the ReAct format
        and lists all available tools.
        """
        tool_lines = "\n".join(
            f"  - {t['name']}: {t['description']}" for t in self.tools
        )
        return f"""You are a helpful AI assistant that solves tasks step-by-step using tools.

AVAILABLE TOOLS:
{tool_lines}

YOU MUST FOLLOW THIS FORMAT EXACTLY for every response until you reach the final answer:

Thought: <your reasoning about what to do next>
Action: tool_name(argument)

After you receive an Observation from the tool, continue with:
Thought: <reasoning about observation>
Action: another_tool(argument)  (only if more info needed)
...

When you have enough information, output:
Thought: <final reasoning>
Final Answer: <your complete answer to the user>

STRICT RULES — VIOLATION IS NOT ALLOWED:
- You MUST call a tool for ANY math calculation — do NOT compute math in your head.
- You MUST call get_current_time for ANY question about the current time/date — do NOT guess or make up the time.
- You MUST call search_wikipedia for ANY factual/knowledge question — do NOT rely on memory.
- Only call ONE tool per step. Never call multiple tools in one response.
- The argument inside Action(...) must be a plain string — no quotes needed.
- NEVER fabricate Observations. Wait for the actual tool result before continuing.
- If a tool returns an error, try rephrasing the argument or use a different tool.
- Use "Final Answer:" ONLY after you have all necessary Observations from tools.
"""

    # ─── Main ReAct Loop ─────────────────────────────────────────────────────

    def run(self, user_input: str) -> str:
        """
        Execute the ReAct loop for a user query.

        Returns:
            The Final Answer string, or a fallback message if max_steps exceeded.
        """
        logger.log_event("AGENT_START", {
            "input": user_input,
            "model": self.llm.model_name,
            "max_steps": self.max_steps,
        })

        # Scratchpad accumulates the full Thought/Action/Observation transcript
        scratchpad = f"User Question: {user_input}\n\n"
        total_tokens = 0
        steps = 0

        while steps < self.max_steps:
            steps += 1
            logger.log_event("AGENT_STEP_START", {"step": steps, "scratchpad_length": len(scratchpad)})

            # ── 1. Call LLM ─────────────────────────────────────────────────
            try:
                result = self.llm.generate(
                    prompt=scratchpad,
                    system_prompt=self.get_system_prompt(),
                )
            except Exception as e:
                logger.error(f"LLM call failed at step {steps}: {e}")
                logger.log_event("AGENT_LLM_ERROR", {"step": steps, "error": str(e)})
                return f"Agent error: LLM call failed — {e}"

            llm_output = result["content"].strip()
            total_tokens += result["usage"].get("total_tokens", 0)

            # Track metrics via telemetry
            tracker.track_request(
                provider=result["provider"],
                model=self.llm.model_name,
                usage=result["usage"],
                latency_ms=result["latency_ms"],
            )

            logger.log_event("AGENT_LLM_RESPONSE", {
                "step": steps,
                "output_preview": llm_output[:200],
                "tokens": result["usage"],
                "latency_ms": result["latency_ms"],
            })

            # ── 2. Check for Final Answer ────────────────────────────────────
            final_match = self._FINAL_RE.search(llm_output)
            if final_match:
                final_answer = final_match.group(1).strip()
                logger.log_event("AGENT_END", {
                    "status": "success",
                    "steps": steps,
                    "total_tokens": total_tokens,
                    "answer_preview": final_answer[:200],
                })
                return final_answer

            # ── 3. Check for Action ──────────────────────────────────────────
            action_match = self._ACTION_RE.search(llm_output)
            if action_match:
                tool_name = action_match.group(1).strip()
                tool_arg = action_match.group(2).strip()

                logger.log_event("AGENT_ACTION", {
                    "step": steps,
                    "tool": tool_name,
                    "argument": tool_arg,
                })

                # Execute the tool
                observation = self._execute_tool(tool_name, tool_arg)

                logger.log_event("AGENT_OBSERVATION", {
                    "step": steps,
                    "tool": tool_name,
                    "observation_preview": observation[:200],
                })

                # Append LLM output + observation to scratchpad
                scratchpad += llm_output + f"\nObservation: {observation}\n\n"
            else:
                # LLM didn't follow format — nudge it with a hint
                logger.log_event("AGENT_PARSE_FAILURE", {
                    "step": steps,
                    "raw_output": llm_output[:300],
                })
                scratchpad += (
                    llm_output
                    + "\nObservation: [No valid Action detected. "
                    "Please output either 'Action: tool_name(argument)' "
                    "or 'Final Answer: <answer>'.]\n\n"
                )

        # Max steps reached without a Final Answer
        logger.log_event("AGENT_END", {
            "status": "max_steps_exceeded",
            "steps": steps,
            "total_tokens": total_tokens,
        })
        return (
            f"Agent reached the maximum of {self.max_steps} steps without a final answer. "
            "Try rephrasing your question or increasing max_steps."
        )

    # ─── Tool Execution ───────────────────────────────────────────────────────

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Find a tool by name and call it with the parsed argument string.
        Returns the tool's output or an error message.
        """
        for tool in self.tools:
            if tool["name"].lower() == tool_name.lower():
                try:
                    fn = tool["function"]
                    # Call with single string argument (all tools accept one arg)
                    result = fn(args) if args else fn()
                    return str(result)
                except Exception as e:
                    logger.error(f"Tool '{tool_name}' raised an error: {e}", exc_info=False)
                    return f"Tool error in '{tool_name}': {e}"

        available = [t["name"] for t in self.tools]
        return (
            f"Tool '{tool_name}' not found. "
            f"Available tools: {', '.join(available)}."
        )
