"""AI Hiking specialization of the OpenManus-style ToolCallAgent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from agent.tool_call_agent import ToolCallAgent
from agent.tool_collection import ToolCollection


@dataclass
class HikingManus(ToolCallAgent):
    name: str = "HikingManus"
    description: str = "A hiking-focused Manus agent using AI Hiking tools."
    llm: Any | None = None
    available_tools: ToolCollection = field(default_factory=ToolCollection)
    max_steps: int = 20
    max_observe: int | None = 10000

    @classmethod
    def create(cls, *, llm: Any, tools: list[Any], system_prompt: str | None = None, max_steps: int = 20) -> "HikingManus":
        return cls(
            llm=llm,
            available_tools=ToolCollection(*tools),
            system_prompt=system_prompt,
            max_steps=max_steps,
        )
