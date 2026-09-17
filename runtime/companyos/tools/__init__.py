"""Tools available to spawned agents, and the registry that hands them out.

Everything here is default-deny. A tool must be (a) implemented, (b) allowed by
runtime policy, and (c) implied by the agent's own spec before an instance can
call it. See :mod:`companyos.tools.policy`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

from ..errors import ToolError, ToolPermissionError
from ..providers import ToolSpec


@dataclass
class ToolContext:
    """Everything a tool is allowed to know about its caller.

    Deliberately narrow: no environment, no secrets, no provider handle. A tool
    cannot reach the model, and an agent cannot reach the process environment
    through a tool.
    """

    root: Path
    run_id: str = ""
    task_id: str = ""
    agent_id: str = ""
    readable_dirs: tuple[str, ...] = ()
    memory: Any = None
    scratch: Any = None


@dataclass
class ToolResult:
    """The outcome of one tool call."""

    name: str
    ok: bool
    content: str = ""
    error: str = ""
    arguments: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "tool": self.name,
            "ok": self.ok,
            "arguments": dict(self.arguments),
            "content": self.content[:2000],
            "error": self.error,
        }


@dataclass(frozen=True)
class Tool:
    """A callable capability offered to an agent instance."""

    name: str
    description: str
    parameters: Mapping[str, Any]
    handler: Callable[[Mapping[str, Any], ToolContext], str]
    mutating: bool = False
    """True if the tool changes state outside the run. Never granted by default."""

    def spec(self) -> ToolSpec:
        return ToolSpec(self.name, self.description, self.parameters)

    def invoke(self, arguments: Mapping[str, Any], context: ToolContext) -> ToolResult:
        try:
            return ToolResult(
                self.name, True, self.handler(arguments, context), arguments=arguments
            )
        except ToolError as exc:
            return ToolResult(self.name, False, error=str(exc), arguments=arguments)
        except Exception as exc:  # pragma: no cover - defensive
            return ToolResult(
                self.name, False, error=f"{type(exc).__name__}: {exc}", arguments=arguments
            )


class ToolRegistry:
    """Name -> :class:`Tool`, filtered by policy at call time."""

    def __init__(self, tools: Mapping[str, Tool] | None = None) -> None:
        self._tools: dict[str, Tool] = dict(tools or {})

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise ToolPermissionError(f"unknown tool {name!r}")
        return self._tools[name]

    def __contains__(self, name: object) -> bool:
        return name in self._tools

    def names(self) -> list[str]:
        return sorted(self._tools)

    def specs_for(self, allowed: "set[str] | tuple[str, ...]") -> list[ToolSpec]:
        return [self._tools[n].spec() for n in sorted(allowed) if n in self._tools]

    @classmethod
    def default(cls) -> "ToolRegistry":
        from .builtin import BUILTIN_TOOLS

        return cls({t.name: t for t in BUILTIN_TOOLS})


__all__ = [
    "Tool",
    "ToolContext",
    "ToolRegistry",
    "ToolResult",
]
