"""The immutable, parsed form of a Markdown agent specification.

``AgentDefinition`` is the *template*: "what this type of agent is". It is
read-only, shared, and long-lived. Its runtime counterpart is
``orchestration.spawner.AgentInstance`` -- "a temporary running agent handling
one specific task".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

#: The 11 sections every spec must have (scripts/check-structure.py enforces it).
SECTION_NAMES: Mapping[int, str] = {
    1: "mission",
    2: "responsibilities",
    3: "inputs",
    4: "outputs",
    5: "tools",
    6: "workflows",
    7: "collaboration",
    8: "escalation",
    9: "quality_standards",
    10: "kpis",
    11: "review_requirements",
}


class AgentKind:
    """Behavioural class of an agent, derived from where its spec lives."""

    EXECUTIVE = "executive"
    """C-suite. Delegates and decides; does not implement."""

    ORCHESTRATION = "orchestration"
    """Kernel components: CEO, planner, decomposer, coordinator, managers."""

    REVIEWER = "reviewer"
    """Critique functions. Execute, but only over other agents' output."""

    SPECIALIST = "specialist"
    """Does the actual work. The default for a department agent."""


@dataclass(frozen=True)
class AgentDefinition:
    """A parsed agent spec. Never mutated at runtime."""

    id: str
    """Stable slug, ``<division>/<file-stem>`` -- e.g. ``engineering/backend-engineer``."""

    name: str
    division: str
    kind: str
    source_path: Path
    reports_to: str | None = None
    sections: Mapping[int, str] = field(default_factory=dict)
    capabilities: tuple[str, ...] = ()
    capability_scores: Mapping[str, int] = field(default_factory=dict)
    tools: tuple[str, ...] = ()
    """Runtime tool names this spec's section 5 maps onto."""

    prohibited_tools: tuple[str, ...] = ()
    raw_tools_text: str = ""
    can_execute_independently: bool = True
    """False for delegators: they must decompose rather than produce the deliverable."""

    reviews_for: tuple[str, ...] = ()
    """Concerns this agent reviews, when it is a reviewer."""

    supervises: tuple[str, ...] = ()
    """Divisions this agent owns, parsed from an executive spec's responsibilities."""

    def section(self, number: int) -> str:
        return self.sections.get(number, "")

    @property
    def mission(self) -> str:
        return self.section(1)

    @property
    def responsibilities(self) -> str:
        return self.section(2)

    @property
    def quality_standards(self) -> str:
        return self.section(9)

    @property
    def escalation_rules(self) -> str:
        return self.section(8)

    @property
    def workflows(self) -> str:
        return self.section(6)

    @property
    def index_text(self) -> str:
        """The text selection scores against: identity plus what it does."""
        parts = [self.name, self.division, self.id.replace("/", " ").replace("-", " ")]
        parts += [self.section(n) for n in (1, 2, 4, 5, 6)]
        return "\n".join(p for p in parts if p)

    def to_dict(self, *, full: bool = False) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "division": self.division,
            "kind": self.kind,
            "reports_to": self.reports_to,
            "capabilities": list(self.capabilities),
            "tools": list(self.tools),
            "prohibited_tools": list(self.prohibited_tools),
            "can_execute_independently": self.can_execute_independently,
            "source_path": str(self.source_path),
        }
        if full:
            data["sections"] = {SECTION_NAMES.get(k, str(k)): v for k, v in self.sections.items()}
        return data
