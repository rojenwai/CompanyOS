"""Capability-based agent selection.

Given the capabilities a task requires, find the agent definitions that claim
them. There is no ``if task == X: use agent Y`` table anywhere in this module:
scoring combines

* **capability overlap** -- exact tag matches, then same-namespace matches;
* **lexical fit** -- IDF-weighted overlap between the task text and the agent's
  own spec, which catches wording the taxonomy has no phrase for;
* **structural priors** -- the division that owns the capability, and whether
  the agent's spec says it can produce a deliverable at all.

So a newly written Markdown spec becomes selectable with no code change, and an
agent is never chosen for work its spec does not describe.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..errors import NoSuitableAgentError
from ..registry import AgentRegistry
from ..registry import capabilities as caps
from ..registry.definition import AgentDefinition, AgentKind

# Score weights. Tuned so a single exact capability match outranks any amount of
# incidental lexical similarity, and a delegator never wins executable work.
W_EXACT = 3.0
W_NAMESPACE = 1.25
W_LEXICAL = 2.0
W_DIVISION_HINT = 0.75
W_NAME = 1.0
#: How much an agent's depth in a capability (number of matching signal phrases
#: in its own spec) amplifies an exact match. Without this, every agent that
#: mentions databases once ties with the Database Engineer.
W_DEPTH = 0.25
MAX_DEPTH_BONUS = 6
W_SPECIALIST = 0.5
P_REVIEWER = -1.5

DEFAULT_THRESHOLD = 1.0

#: Identity namespaces every agent carries (`role.<slug>`, `division.<name>`).
#: They match exactly or not at all -- a namespace-level match on them would
#: make every agent in the registry a candidate for any role request.
IDENTITY_NAMESPACES = frozenset({"role", "division"})


@dataclass
class Candidate:
    """One scored agent definition."""

    definition: AgentDefinition
    score: float
    matched: tuple[str, ...] = ()
    reasons: dict = field(default_factory=dict)

    @property
    def agent_id(self) -> str:
        return self.definition.id

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "agent_name": self.definition.name,
            "division": self.definition.division,
            "score": round(self.score, 3),
            "matched_capabilities": list(self.matched),
            "reasons": {k: round(v, 3) if isinstance(v, float) else v
                        for k, v in self.reasons.items()},
        }


class AgentSelector:
    """Ranks and picks agent definitions for a task."""

    def __init__(self, registry: AgentRegistry, *, threshold: float = DEFAULT_THRESHOLD) -> None:
        self.registry = registry
        self.threshold = threshold

    # -- ranking ---------------------------------------------------------------

    def rank(
        self,
        required_capabilities: "list[str] | tuple[str, ...]",
        task_text: str = "",
        *,
        executable_only: bool = True,
        exclude: "set[str] | tuple[str, ...]" = (),
        division_hint: str | None = None,
        include_kinds: "tuple[str, ...] | None" = None,
    ) -> list[Candidate]:
        """Score every eligible agent, best first."""
        wanted = [caps.normalize(c) for c in required_capabilities if c]
        wanted_namespaces = {caps.namespace(c) for c in wanted}
        hinted_divisions = caps.divisions_for(wanted)
        if division_hint:
            hinted_divisions = hinted_divisions | {division_hint}
        excluded = set(exclude)

        candidates: list[Candidate] = []
        for definition in self.registry:
            if definition.id in excluded:
                continue
            if include_kinds and definition.kind not in include_kinds:
                continue
            if executable_only and not definition.can_execute_independently:
                # A hard exclusion, not a penalty: a delegator must never be
                # assigned a deliverable however well it scores. The
                # orchestrator does the delegating, not the agent.
                continue
            candidate = self._score(
                definition, wanted, wanted_namespaces, task_text, hinted_divisions
            )
            if candidate.score > 0:
                candidates.append(candidate)

        candidates.sort(key=lambda c: (-c.score, c.agent_id))
        return candidates

    def _score(
        self,
        definition: AgentDefinition,
        wanted: list[str],
        wanted_namespaces: set[str],
        task_text: str,
        hinted_divisions: set[str],
    ) -> Candidate:
        available = set(definition.capabilities)
        exact = [c for c in wanted if c in available]

        namespace_hits: list[str] = []
        for capability in wanted:
            if capability in exact:
                continue
            prefix = caps.namespace(capability)
            if prefix in IDENTITY_NAMESPACES:
                continue
            if any(caps.namespace(a) == prefix for a in available):
                namespace_hits.append(capability)

        reasons: dict = {}
        score = 0.0
        if exact:
            reasons["exact"] = sum(W_EXACT * self._depth(definition, c) for c in exact)
            score += reasons["exact"]
            named = [c for c in exact if self._named_for(definition, c)]
            if named:
                reasons["name"] = W_NAME * len(named)
                score += reasons["name"]
        if namespace_hits:
            reasons["namespace"] = W_NAMESPACE * len(namespace_hits)
            score += reasons["namespace"]

        if task_text:
            lexical = self.registry.lexical_score(definition.id, task_text)
            if lexical:
                reasons["lexical"] = W_LEXICAL * lexical
                score += reasons["lexical"]

        if definition.division in hinted_divisions:
            reasons["division"] = W_DIVISION_HINT
            score += W_DIVISION_HINT

        if definition.kind == AgentKind.SPECIALIST:
            reasons["specialist"] = W_SPECIALIST
            score += W_SPECIALIST
        elif definition.kind == AgentKind.REVIEWER:
            reasons["reviewer_penalty"] = P_REVIEWER
            score += P_REVIEWER

        return Candidate(definition, score, tuple(exact + namespace_hits), reasons)

    @staticmethod
    def _depth(definition: AgentDefinition, capability: str) -> float:
        """How strongly this agent's own spec claims the capability."""
        hits = definition.capability_scores.get(capability, 1)
        return 1.0 + W_DEPTH * min(max(hits - 1, 0), MAX_DEPTH_BONUS)

    @staticmethod
    def _named_for(definition: AgentDefinition, capability: str) -> bool:
        """True when the agent is literally named for the capability."""
        leaf = capability.rsplit(".", 1)[-1]
        return bool(leaf) and leaf in definition.id

    # -- selection -------------------------------------------------------------

    def select(
        self,
        required_capabilities: "list[str] | tuple[str, ...]",
        task_text: str = "",
        *,
        exclude: "set[str] | tuple[str, ...]" = (),
        executable_only: bool = True,
    ) -> Candidate:
        """Pick the single best agent for a task.

        Raises :class:`NoSuitableAgentError` when nothing clears the threshold,
        which the orchestrator turns into an escalation rather than a guess --
        the fallback written in ``ai/orchestration/task-routing.md``.
        """
        ranked = self.rank(
            required_capabilities, task_text, exclude=exclude, executable_only=executable_only
        )
        if required_capabilities:
            # Lexical similarity ranks among genuine matches; it must never be
            # the sole reason an agent is chosen. Without this an agent that
            # merely shares vocabulary with the task can win work its spec says
            # nothing about.
            ranked = [c for c in ranked if c.matched]

        if not ranked or ranked[0].score < self.threshold:
            best = f" (best was {ranked[0].agent_id} at {ranked[0].score:.2f})" if ranked else ""
            raise NoSuitableAgentError(
                f"no agent matches capabilities {list(required_capabilities)}{best}"
            )
        return ranked[0]

    def select_team(
        self,
        capability_groups: "list[list[str]]",
        task_text: str = "",
        *,
        limit: int = 8,
        unique_agents: bool = True,
    ) -> list[Candidate]:
        """Pick one agent per capability group, optionally without repeats."""
        chosen: list[Candidate] = []
        used: set[str] = set()
        for group in capability_groups:
            if len(chosen) >= limit:
                break
            try:
                candidate = self.select(group, task_text, exclude=used if unique_agents else ())
            except NoSuitableAgentError:
                continue
            chosen.append(candidate)
            used.add(candidate.agent_id)
        return chosen

    def select_reviewers(
        self, concerns: "list[str] | tuple[str, ...]" = (), *, limit: int = 3
    ) -> list[AgentDefinition]:
        """Reviewers whose specs cover the given concerns.

        Always includes the general Reviewer, because
        ``ai/orchestration/reviewer.md`` is the unconditional correctness gate.
        """
        reviewers = self.registry.reviewers()
        general = [r for r in reviewers if r.id.endswith("/reviewer")]
        wanted = {c.lower() for c in concerns}

        specialised = [
            r
            for r in reviewers
            if r not in general and (not wanted or wanted & set(r.reviews_for))
        ]
        ordered = general + sorted(specialised, key=lambda r: r.id)
        return ordered[:limit] if ordered else reviewers[:limit]
