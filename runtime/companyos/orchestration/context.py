"""Scoped context assembly for a spawned agent.

Implements ``ai/memory/context-management.md``: "precision beats volume". An
agent instance receives its own task, the parent objective, the outputs of the
tasks it actually depends on, any reviewer findings against it, and a bounded
memory retrieval. It does **not** receive the conversation, the other branches
of the DAG, or the outputs of sibling tasks it does not depend on.

``ContextBundle.keys`` records exactly which slices were included, and lands on
the ``AgentResult``, so context isolation is auditable after the fact rather
than assumed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from ..config import RuntimeConfig
from ..memory.store import MemoryStore
from ..models import AgentResult, Task, TaskGraph
from .prompts import untrusted

#: Per-slice caps, so one enormous upstream output cannot crowd out the rest.
_MAX_DEP_CHARS = 4_000
_MAX_MEMORY_CHARS = 2_000


@dataclass
class ContextBundle:
    """The assembled, bounded context for one agent instance."""

    task_id: str
    sections: list[tuple[str, str]] = field(default_factory=list)
    keys: list[str] = field(default_factory=list)
    truncated: bool = False

    def add(self, key: str, body: str) -> None:
        if body and body.strip():
            self.sections.append((key, body.strip()))
            self.keys.append(key)

    def render(self, max_chars: int) -> str:
        """Flatten to a prompt body, dropping the least important tail if needed."""
        parts = [f"## {key}\n{body}" for key, body in self.sections]
        text = "\n\n".join(parts)
        if len(text) <= max_chars:
            return text
        self.truncated = True
        return text[:max_chars].rsplit("\n", 1)[0] + "\n\n[context truncated to fit the budget]"

    def to_dict(self) -> dict:
        return {"task_id": self.task_id, "keys": list(self.keys), "truncated": self.truncated}


class ContextBuilder:
    """Builds one :class:`ContextBundle` per task."""

    def __init__(self, config: RuntimeConfig, memory: MemoryStore | None = None) -> None:
        self.config = config
        self.memory = memory

    def build(
        self,
        task: Task,
        graph: TaskGraph,
        results: Mapping[str, AgentResult],
        *,
        plan: Mapping[str, Any] | None = None,
        request: str = "",
    ) -> ContextBundle:
        bundle = ContextBundle(task_id=task.id)

        # 1. The task itself.
        own = [f"Objective: {task.objective}"]
        if task.description:
            own.append(f"Scope: {task.description}")
        if task.acceptance_criteria:
            own.append(
                "Acceptance criteria:\n"
                + "\n".join(f"- {c}" for c in task.acceptance_criteria)
            )
        bundle.add("your task", "\n".join(own))

        # 2. Parent objective only -- never the whole conversation.
        if plan:
            parent = [f"Company objective: {plan.get('objective', request)}"]
            if plan.get("strategy"):
                parent.append(f"Approach: {plan['strategy']}")
            bundle.add("why this work exists", "\n".join(parent))

        # 3. Outputs of direct dependencies, and nothing else.
        for dependency_id in task.dependencies:
            dependency = graph.get(dependency_id)
            result = results.get(dependency_id)
            if dependency is None or result is None or not result.output:
                continue
            bundle.add(
                f"input from {result.agent_name or result.agent_id}",
                untrusted(
                    f"agent:{result.agent_id}",
                    f"Task: {dependency.objective}\n\n{result.output[:_MAX_DEP_CHARS]}",
                ),
            )

        # 4. Reviewer findings against this task, on a retry.
        if task.findings:
            bundle.add(
                "reviewer findings to address",
                "\n".join(
                    f"- [{f.get('severity', 'medium')}] {f.get('issue', '')} "
                    f"-> {f.get('required_change', '')}"
                    for f in task.findings
                ),
            )

        # 5. Bounded memory retrieval.
        if self.memory is not None:
            query = f"{task.objective} {' '.join(task.required_capabilities)}"
            records = self.memory.retrieve(query, k=3)
            if records:
                body = "\n\n".join(
                    f"[{r.store} · {r.source}]\n{r.text[:800]}" for r in records
                )[:_MAX_MEMORY_CHARS]
                bundle.add("organizational memory", untrusted("memory", body))

        return bundle

    def isolation_report(
        self, task: Task, graph: TaskGraph, results: Mapping[str, AgentResult]
    ) -> dict:
        """Which sibling outputs were deliberately withheld from this task."""
        allowed = set(task.dependencies)
        withheld = [
            other.id
            for other in graph
            if other.id != task.id and other.id not in allowed and other.id in results
        ]
        return {"task_id": task.id, "shared": sorted(allowed), "withheld": sorted(withheld)}
