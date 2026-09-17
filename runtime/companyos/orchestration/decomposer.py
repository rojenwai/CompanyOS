"""The Task Decomposer: a plan becomes a dependency-ordered DAG of subtasks.

Runs the agent described by ``ai/orchestration/task-decomposer.md``. Its output
is sanitized hard, because a model can and will emit duplicate ids, forward
references, and cycles. The rule is simple and preserves intent: a task may only
depend on a task declared before it, which makes the result acyclic by
construction while keeping the ordering the model asked for.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .. import purposes
from ..config import RuntimeConfig
from ..errors import ProviderError
from ..models import Task, TaskGraph, Usage
from ..observability import EventBus, EventType
from ..providers import Message, Provider, extract_json
from ..registry import AgentRegistry
from ..registry import capabilities as caps
from .prompts import json_instruction, kernel_system_prompt, untrusted

_TASK_SCHEMA = """{
  "tasks": [
    {
      "id": "t1",
      "objective": "what this one agent must deliver",
      "description": "scope, and what is explicitly out of scope",
      "required_capabilities": ["one or two capability tags"],
      "dependencies": ["ids of tasks whose output this one needs"],
      "priority": 1,
      "acceptance_criteria": ["testable done-conditions"],
      "optional": false
    }
  ]
}"""


class TaskDecomposer:
    """Splits a plan into atomic, independently assignable subtasks."""

    AGENT_ID = "orchestration/task-decomposer"

    def __init__(
        self,
        registry: AgentRegistry,
        provider: Provider,
        config: RuntimeConfig,
        bus: EventBus,
    ) -> None:
        self.registry = registry
        self.provider = provider
        self.config = config
        self.bus = bus
        self.definition = registry.get(self.AGENT_ID)

    async def decompose(
        self, request: str, plan: Mapping[str, Any], *, run_id: str, max_tasks: int
    ) -> tuple[TaskGraph, Usage]:
        """Return ``(graph, usage)``. Always yields at least one task."""
        max_tasks = max(1, max_tasks)
        system = kernel_system_prompt(
            self.definition,
            "Split this plan into the smallest set of subtasks that covers it. "
            "Only add a dependency when one task genuinely needs another's output: "
            "tasks with no dependency between them will be executed in parallel.",
        )
        user = "\n\n".join(
            [
                f"Produce at most {max_tasks} subtasks.",
                "Original request:",
                untrusted("user-request", request),
                "Plan:",
                untrusted("planner-output", _render_plan(plan)),
                json_instruction(_TASK_SCHEMA),
            ]
        )

        usage = Usage()
        raw: list[Mapping[str, Any]] = []
        try:
            completion = await self.provider.complete(
                system=system,
                messages=[Message("user", user)],
                purpose=purposes.DECOMPOSE,
                context={
                    "request": request,
                    "plan": dict(plan),
                    "run_id": run_id,
                    "max_tasks": max_tasks,
                },
            )
            usage = completion.usage
            data = extract_json(completion.text)
            raw = list(data.get("tasks") or []) if isinstance(data, Mapping) else list(data)
        except (ProviderError, ValueError, TypeError, AttributeError) as exc:
            self.bus.emit(
                EventType.TASKS_DECOMPOSED,
                run_id=run_id,
                agent_id=self.AGENT_ID,
                message=f"decomposer fell back to one task per capability: {exc}",
                data={"degraded": True},
            )

        tasks = self._sanitize(raw, plan, request, max_tasks)
        graph = TaskGraph(tasks)
        graph.validate()

        self.bus.emit(
            EventType.TASKS_DECOMPOSED,
            run_id=run_id,
            agent_id=self.AGENT_ID,
            message=f"{len(graph)} subtask(s) in {len(graph.layers())} wave(s)",
            data={
                "tasks": [
                    {"id": t.id, "objective": t.objective, "dependencies": t.dependencies}
                    for t in graph
                ],
                "waves": [[t.id for t in wave] for wave in graph.layers()],
            },
        )
        return graph, usage

    # -- sanitizing ------------------------------------------------------------

    def _sanitize(
        self,
        raw: Sequence[Mapping[str, Any]],
        plan: Mapping[str, Any],
        request: str,
        max_tasks: int,
    ) -> list[Task]:
        tasks: list[Task] = []
        id_map: dict[str, str] = {}
        seen_declared: set[str] = set()

        for index, item in enumerate(raw):
            if len(tasks) >= max_tasks:
                break
            if not isinstance(item, Mapping):
                continue
            objective = str(item.get("objective") or "").strip()
            if not objective:
                continue

            declared = str(item.get("id") or f"t{index + 1}").strip()
            if declared in seen_declared:
                continue  # duplicate id: drop rather than silently merge
            seen_declared.add(declared)

            task = Task(
                objective=objective,
                description=str(item.get("description") or ""),
                priority=_int(item.get("priority"), default=5, low=1, high=9),
                required_capabilities=[
                    caps.normalize(c)
                    for c in (item.get("required_capabilities") or [])
                    if isinstance(c, str) and c.strip()
                ],
                acceptance_criteria=[
                    str(c) for c in (item.get("acceptance_criteria") or []) if str(c).strip()
                ],
                optional=bool(item.get("optional", False)),
            )
            if not task.required_capabilities:
                task.required_capabilities = self._infer_capabilities(task, plan)

            # Backward references only: guarantees a DAG.
            for dependency in item.get("dependencies") or []:
                mapped = id_map.get(str(dependency))
                if mapped:
                    task.dependencies.append(mapped)

            id_map[declared] = task.id
            tasks.append(task)

        if not tasks:
            tasks = self._fallback_tasks(plan, request, max_tasks)
        return tasks

    def _infer_capabilities(self, task: Task, plan: Mapping[str, Any]) -> list[str]:
        detected = caps.extract(f"{task.objective}\n{task.description}")
        if detected:
            ranked = sorted(detected.items(), key=lambda kv: (-kv[1], kv[0]))
            return [c for c, _ in ranked[:2]]
        planned = list(plan.get("required_capabilities") or [])
        return planned[:1] or ["operations.process"]

    def _fallback_tasks(
        self, plan: Mapping[str, Any], request: str, max_tasks: int
    ) -> list[Task]:
        """One task per planned capability when decomposition produced nothing."""
        wanted = list(plan.get("required_capabilities") or [])[:max_tasks] or [
            "operations.process"
        ]
        objective = str(plan.get("objective") or request).strip()
        return [
            Task(
                objective=f"{capability.split('.')[-1].replace('-', ' ').capitalize()}"
                f" workstream for: {objective}",
                description=f"Cover the {capability} dimension of the objective.",
                required_capabilities=[capability],
                priority=index + 1,
                acceptance_criteria=["Concrete, evidence-backed conclusions"],
            )
            for index, capability in enumerate(wanted)
        ]


def _render_plan(plan: Mapping[str, Any]) -> str:
    lines = [f"Objective: {plan.get('objective', '')}", f"Strategy: {plan.get('strategy', '')}"]
    for key in ("required_capabilities", "divisions", "success_criteria", "risks"):
        values = plan.get(key) or []
        if values:
            lines.append(f"{key.replace('_', ' ').capitalize()}: {', '.join(map(str, values))}")
    return "\n".join(lines)


def _int(value: Any, *, default: int, low: int, high: int) -> int:
    try:
        return max(low, min(high, int(value)))
    except (TypeError, ValueError):
        return default
