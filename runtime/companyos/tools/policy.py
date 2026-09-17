"""Tool permission boundaries for dynamically spawned agents.

The rule, in order of precedence:

1. The runtime's ``denied_tools`` wins over everything. A spec cannot grant
   itself a tool the operator has forbidden.
2. A spec's own prohibitions ("never fabricates", "prohibited from…") are
   honoured next.
3. What remains is the union of the runtime's ``default_tools`` (a read-only
   floor) and the tools the agent's section 5 maps onto.
4. Mutating tools are never granted implicitly -- they must be named in
   ``default_tools`` *and* survive steps 1-2.

A spawned agent therefore has strictly less authority than the process running
it, and never more than its own specification claims.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..config import RuntimeConfig
from ..errors import ToolPermissionError
from ..registry.definition import AgentDefinition
from . import ToolRegistry


@dataclass(frozen=True)
class ToolPolicy:
    """The resolved tool grant for one agent instance."""

    agent_id: str
    allowed: frozenset[str]
    denied: frozenset[str]
    max_calls: int

    def check(self, name: str) -> None:
        """Raise unless this instance may call ``name``."""
        if name in self.denied:
            raise ToolPermissionError(
                f"agent {self.agent_id!r} is denied tool {name!r} by runtime policy"
            )
        if name not in self.allowed:
            raise ToolPermissionError(
                f"agent {self.agent_id!r} may not use tool {name!r}; "
                f"allowed: {', '.join(sorted(self.allowed)) or 'none'}"
            )

    def permits(self, name: str) -> bool:
        return name in self.allowed and name not in self.denied

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "allowed": sorted(self.allowed),
            "denied": sorted(self.denied),
            "max_calls": self.max_calls,
        }


def resolve_policy(
    definition: AgentDefinition,
    config: RuntimeConfig,
    registry: ToolRegistry,
) -> ToolPolicy:
    """Compute the tool grant for one agent definition under a runtime config."""
    denied = set(config.denied_tools) | set(definition.prohibited_tools)

    granted = (set(config.default_tools) | set(definition.tools)) - denied
    # Only tools that actually exist, and never a mutating tool the operator
    # did not explicitly put in default_tools.
    resolved: set[str] = set()
    for name in granted:
        if name not in registry:
            continue
        if registry.get(name).mutating and name not in config.default_tools:
            denied.add(name)
            continue
        resolved.add(name)

    return ToolPolicy(
        agent_id=definition.id,
        allowed=frozenset(resolved),
        denied=frozenset(denied),
        max_calls=config.limits.max_tool_calls_per_agent,
    )
