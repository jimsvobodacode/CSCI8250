import datetime
from typing import Any
from agents import RunHooks, RunContextWrapper, Agent, Tool, Usage


class LoggingHooks(RunHooks):
    def __init__(self) -> None:
        self._counter = 0

    # ────────────────────────────────────────────────────────────────────────────
    # Helpers
    # ────────────────────────────────────────────────────────────────────────────
    def _ts(self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    def _usage_to_str(self, usage: Usage) -> str:
        return (
            f"{usage.requests} req, {usage.input_tokens} in, "
            f"{usage.output_tokens} out, {usage.total_tokens} total tokens"
        )

    def _log(self, msg: str) -> None:
        self._counter += 1
        print(f"[{self._ts()}] #{self._counter}: {msg}")

    # ────────────────────────────────────────────────────────────────────────────
    # Callbacks
    # ────────────────────────────────────────────────────────────────────────────
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:  # type: ignore[override]
        self._log(
            f"Agent '{agent.name}' START. Usage: {self._usage_to_str(context.usage)}"
        )

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:  # type: ignore[override]
        self._log(
            #f"Agent '{agent.name}' END with output {output}. Usage: {self._usage_to_str(context.usage)}"
            f"Agent '{agent.name}' END"
        )

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:  # type: ignore[override]
        self._log(
            f"Tool '{tool.name}' START. Usage: {self._usage_to_str(context.usage)}"
        )

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str) -> None:  # type: ignore[override]
        self._log(
            f"Tool '{tool.name}' END with result {result}. Usage: {self._usage_to_str(context.usage)}"
        )

    async def on_handoff(
        self,
        context: RunContextWrapper,
        from_agent: Agent,
        to_agent: Agent,
    ) -> None:  # type: ignore[override]
        self._log(
            (
                f"Handoff from '{from_agent.name}' to '{to_agent.name}'. "
                f"Usage: {self._usage_to_str(context.usage)}"
            )
        )