"""The Agent Registry: discovery and lookup over the Markdown agent specs.

The registry is the bridge between the spec repository and the runtime. It
walks ``ai/agents/`` and ``ai/orchestration/``, parses every spec once, and
exposes them for capability-based selection. It **does not duplicate** the
specs -- an ``AgentDefinition`` holds the parsed view plus the path it came
from, and a spec added to the repository appears here on the next load with no
code change.
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Iterator

from ..errors import AgentNotFoundError, RegistryError
from . import capabilities as caps
from .definition import AgentDefinition, AgentKind
from .parser import parse_agent_spec

#: Files inside the agent tree that are not agent specs.
_SKIP_NAMES = {"README.md", "agent-template.md"}

#: Spec-bearing kernel documents. Other files in ai/orchestration/ (the engines,
#: task-routing, execution-lifecycle) are prose, not agents, and are skipped
#: automatically because they carry no numbered sections.
_ORCHESTRATION_DIR = "orchestration"


class AgentRegistry:
    """An immutable, in-memory index of every discoverable agent definition."""

    def __init__(self, definitions: Iterable[AgentDefinition]) -> None:
        self._by_id: dict[str, AgentDefinition] = {}
        for definition in definitions:
            self._by_id[definition.id] = definition

        self._by_division: dict[str, list[AgentDefinition]] = defaultdict(list)
        self._by_capability: dict[str, list[AgentDefinition]] = defaultdict(list)
        for definition in self._by_id.values():
            self._by_division[definition.division].append(definition)
            for capability in definition.capabilities:
                self._by_capability[capability].append(definition)

        self._doc_tokens: dict[str, set[str]] = {
            aid: set(caps.tokenize(d.index_text)) for aid, d in self._by_id.items()
        }
        self._idf = self._build_idf()
        self._supervisors = self._build_supervisor_map()

    # -- discovery -------------------------------------------------------------

    @classmethod
    def discover(
        cls,
        root: Path | str,
        *,
        include_orchestration: bool = True,
        strict: bool = False,
    ) -> "AgentRegistry":
        """Load every agent spec under ``root``.

        ``strict`` turns an unparsable spec into an error instead of a skip, so
        CI can assert the whole tree loads while an interactive run degrades.
        """
        root = Path(root).resolve()
        agents_root = root / "ai" / "agents"
        if not agents_root.is_dir():
            raise RegistryError(f"no agent specs at {agents_root}")

        paths = [p for p in sorted(agents_root.rglob("*.md")) if p.name not in _SKIP_NAMES]
        if include_orchestration:
            kernel = root / "ai" / _ORCHESTRATION_DIR
            if kernel.is_dir():
                paths += [p for p in sorted(kernel.glob("*.md")) if p.name not in _SKIP_NAMES]

        definitions: list[AgentDefinition] = []
        for path in paths:
            try:
                definitions.append(parse_agent_spec(path, root=root))
            except RegistryError:
                if strict:
                    raise
                continue  # prose document in a spec folder; not an agent
        if not definitions:
            raise RegistryError(f"no parsable agent specs found under {agents_root}")
        return cls(definitions)

    # -- access ----------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._by_id)

    def __iter__(self) -> Iterator[AgentDefinition]:
        return iter(self._by_id.values())

    def __contains__(self, agent_id: object) -> bool:
        return agent_id in self._by_id

    @property
    def agents(self) -> list[AgentDefinition]:
        return sorted(self._by_id.values(), key=lambda d: d.id)

    @property
    def divisions(self) -> list[str]:
        return sorted(self._by_division)

    def get(self, agent_id: str) -> AgentDefinition:
        try:
            return self._by_id[agent_id]
        except KeyError:
            raise AgentNotFoundError(f"no agent definition with id {agent_id!r}") from None

    def by_division(self, division: str) -> list[AgentDefinition]:
        return sorted(self._by_division.get(division, ()), key=lambda d: d.id)

    def by_kind(self, kind: str) -> list[AgentDefinition]:
        return sorted((d for d in self if d.kind == kind), key=lambda d: d.id)

    def reviewers(self) -> list[AgentDefinition]:
        return self.by_kind(AgentKind.REVIEWER)

    def executives(self) -> list[AgentDefinition]:
        return self.by_kind(AgentKind.EXECUTIVE)

    def executable(self) -> list[AgentDefinition]:
        """Agents allowed to produce a deliverable themselves."""
        return sorted((d for d in self if d.can_execute_independently), key=lambda d: d.id)

    def with_capability(self, capability: str) -> list[AgentDefinition]:
        """Agents tagged with this capability, or with one inside its namespace."""
        capability = caps.normalize(capability)
        exact = list(self._by_capability.get(capability, ()))
        if exact:
            return sorted(exact, key=lambda d: d.id)
        prefix = capability + "."
        return sorted(
            {
                d.id: d
                for cap, defs in self._by_capability.items()
                if cap.startswith(prefix)
                for d in defs
            }.values(),
            key=lambda d: d.id,
        )

    def resolve(self, ref: str) -> AgentDefinition:
        """Resolve an id, a spec filename, or a human name to a definition.

        Lets a planner say "Security Architect Agent" or ``security/...`` and
        still land on the same definition.
        """
        ref = ref.strip()
        if ref in self._by_id:
            return self._by_id[ref]

        slug = re.sub(r"[^a-z0-9]+", "-", ref.lower()).strip("-")
        for definition in self.agents:
            candidates = {
                definition.id,
                definition.id.split("/", 1)[1],
                re.sub(r"[^a-z0-9]+", "-", definition.name.lower()).strip("-"),
            }
            if slug in candidates or f"{slug}-agent" in candidates:
                return definition

        matches = [d for d in self.agents if slug and slug in d.id]
        if len(matches) == 1:
            return matches[0]
        raise AgentNotFoundError(f"no agent definition matches {ref!r}")

    # -- hierarchy --------------------------------------------------------------

    def _build_supervisor_map(self) -> dict[str, str]:
        """division -> executive agent id, read from the executives' own specs.

        Primary source is each executive's ``Supervises the X, Y … divisions``
        sentence. A division nobody claims falls back to the executive whose own
        division matches, then to the CEO agent.
        """
        mapping: dict[str, str] = {}
        for executive in self.by_kind(AgentKind.EXECUTIVE):
            for division in executive.supervises:
                mapping.setdefault(division, executive.id)
        for division in self._by_division:
            if division in mapping:
                continue
            owner = next(
                (
                    d
                    for d in self.by_kind(AgentKind.EXECUTIVE)
                    if division.replace("-", " ") in d.name.lower()
                ),
                None,
            )
            if owner is not None:
                mapping[division] = owner.id
        return mapping

    def supervisor_for(self, definition: AgentDefinition) -> str | None:
        """The agent this one reports to at runtime, or ``None`` for the root.

        Tries the spec's own ``Reports to:`` line first, then the division ->
        executive map, so the delegation chain in the Agent Map reflects the
        handbook rather than a hardcoded tree.
        """
        if definition.kind == AgentKind.ORCHESTRATION or definition.id == self.ceo_id:
            return None
        if definition.reports_to:
            try:
                resolved = self.resolve(definition.reports_to)
                if resolved.id != definition.id:
                    return resolved.id
            except AgentNotFoundError:
                pass
        if definition.kind == AgentKind.EXECUTIVE:
            return self.ceo_id
        return self._supervisors.get(definition.division) or self.ceo_id

    @property
    def ceo_id(self) -> str:
        for candidate in ("orchestration/ceo-agent", "orchestration/ceo"):
            if candidate in self._by_id:
                return candidate
        executives = self.by_kind(AgentKind.EXECUTIVE)
        return executives[0].id if executives else self.agents[0].id

    # -- lexical scoring --------------------------------------------------------

    def _build_idf(self) -> dict[str, float]:
        n = max(1, len(self._doc_tokens))
        df: dict[str, int] = defaultdict(int)
        for tokens in self._doc_tokens.values():
            for token in tokens:
                df[token] += 1
        return {token: math.log(1 + n / (1 + count)) for token, count in df.items()}

    def lexical_score(self, agent_id: str, query: str) -> float:
        """IDF-weighted overlap between a query and an agent's spec text.

        This is the fallback that keeps selection working for wording the
        capability taxonomy has no phrase for. Normalized to roughly 0..1.
        """
        doc = self._doc_tokens.get(agent_id)
        if not doc:
            return 0.0
        query_tokens = set(caps.tokenize(query))
        if not query_tokens:
            return 0.0
        matched = sum(self._idf.get(token, 0.0) for token in query_tokens & doc)
        possible = sum(self._idf.get(token, 0.0) for token in query_tokens) or 1.0
        return matched / possible

    def stats(self) -> dict:
        by_kind: dict[str, int] = defaultdict(int)
        for definition in self:
            by_kind[definition.kind] += 1
        return {
            "agents": len(self),
            "divisions": len(self._by_division),
            "capabilities": len(self._by_capability),
            "by_kind": dict(sorted(by_kind.items())),
        }
