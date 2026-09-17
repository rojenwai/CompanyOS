"""Core runtime data model: tasks, the task DAG, agent results, and the run record."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Iterator, Mapping

from .errors import CyclicDependencyError, MalformedTaskError
from .ids import iso, new_id, now
from .status import RunStatus, TaskStatus, spec_state


@dataclass
class Task:
    """One unit of work small enough for a single agent instance.

    Mirrors ``ai/orchestration/task-decomposer.md``: atomic, with explicit
    inputs, outputs, acceptance criteria, and a single accountable owner-type.
    """

    objective: str
    description: str = ""
    id: str = field(default_factory=lambda: new_id("task"))
    priority: int = 5
    """1 = highest. Used to order ready tasks competing for a slot."""

    dependencies: list[str] = field(default_factory=list)
    required_capabilities: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    assigned_agent: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    input_context: dict = field(default_factory=dict)
    output: str | None = None
    error: str | None = None

    parent_id: str | None = None
    depth: int = 0
    optional: bool = False
    """If true, dependents still run when this task fails."""

    attempts: int = 0
    findings: list[dict] = field(default_factory=list)
    """Reviewer findings carried into the next attempt."""

    created_at: float = field(default_factory=now)
    started_at: float | None = None
    completed_at: float | None = None

    def validate(self) -> None:
        if not self.objective.strip():
            raise MalformedTaskError(f"task {self.id}: empty objective")
        if self.id in self.dependencies:
            raise MalformedTaskError(f"task {self.id}: depends on itself")

    @property
    def duration_s(self) -> float | None:
        if self.started_at is None:
            return None
        return (self.completed_at or now()) - self.started_at

    def mark(self, status: TaskStatus, *, error: str | None = None) -> None:
        self.status = status
        # The clock starts when the task leaves the queue, so spawn time counts
        # toward the task's duration -- the scheduler marks SPAWNING, and only
        # the agent instance marks RUNNING.
        if status in (TaskStatus.SPAWNING, TaskStatus.RUNNING) and self.started_at is None:
            self.started_at = now()
        if status.terminal:
            self.completed_at = now()
        if error is not None:
            self.error = error

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "objective": self.objective,
            "description": self.description,
            "priority": self.priority,
            "dependencies": list(self.dependencies),
            "required_capabilities": list(self.required_capabilities),
            "acceptance_criteria": list(self.acceptance_criteria),
            "assigned_agent": self.assigned_agent,
            "status": self.status.value,
            "spec_state": spec_state(self.status),
            "parent_id": self.parent_id,
            "depth": self.depth,
            "optional": self.optional,
            "attempts": self.attempts,
            "output": self.output,
            "error": self.error,
            "findings": list(self.findings),
            "created_at": iso(self.created_at),
            "started_at": iso(self.started_at) if self.started_at else None,
            "completed_at": iso(self.completed_at) if self.completed_at else None,
            "duration_s": self.duration_s,
        }


class TaskGraph:
    """A DAG of tasks with dependency-aware readiness.

    The scheduler asks this object what may run now; it never guesses ordering
    itself. Independent nodes come back together, which is what makes parallel
    execution safe.
    """

    def __init__(self, tasks: Iterable[Task] = ()) -> None:
        self._tasks: dict[str, Task] = {}
        for task in tasks:
            self.add(task)

    # -- construction ----------------------------------------------------------

    def add(self, task: Task) -> Task:
        task.validate()
        if task.id in self._tasks:
            raise MalformedTaskError(f"duplicate task id: {task.id}")
        self._tasks[task.id] = task
        return task

    def validate(self) -> None:
        """Check every dependency resolves and the graph is acyclic."""
        for task in self._tasks.values():
            for dep in task.dependencies:
                if dep not in self._tasks:
                    raise MalformedTaskError(f"task {task.id}: unknown dependency {dep!r}")
        self.topological_order()  # raises on a cycle

    # -- access ----------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._tasks)

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks.values())

    def __contains__(self, task_id: object) -> bool:
        return task_id in self._tasks

    def __getitem__(self, task_id: str) -> Task:
        return self._tasks[task_id]

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    @property
    def tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def dependents_of(self, task_id: str) -> list[Task]:
        return [t for t in self._tasks.values() if task_id in t.dependencies]

    # -- scheduling ------------------------------------------------------------

    def topological_order(self) -> list[Task]:
        """Kahn's algorithm. Raises :class:`CyclicDependencyError` on a cycle."""
        indegree = {tid: 0 for tid in self._tasks}
        for task in self._tasks.values():
            for dep in task.dependencies:
                if dep in indegree:
                    indegree[task.id] += 1

        queue = sorted(
            (tid for tid, n in indegree.items() if n == 0),
            key=lambda tid: (self._tasks[tid].priority, tid),
        )
        order: list[Task] = []
        while queue:
            tid = queue.pop(0)
            order.append(self._tasks[tid])
            for dependent in self.dependents_of(tid):
                indegree[dependent.id] -= 1
                if indegree[dependent.id] == 0:
                    queue.append(dependent.id)
                    queue.sort(key=lambda i: (self._tasks[i].priority, i))

        if len(order) != len(self._tasks):
            stuck = sorted(set(self._tasks) - {t.id for t in order})
            raise CyclicDependencyError(f"dependency cycle among tasks: {', '.join(stuck)}")
        return order

    def layers(self) -> list[list[Task]]:
        """Group tasks into waves that could execute concurrently.

        Used for plan display and for asserting parallelism in tests; the live
        scheduler is finer-grained than this and starts a task the moment its
        own dependencies finish.
        """
        remaining = {t.id: set(t.dependencies) & set(self._tasks) for t in self._tasks.values()}
        done: set[str] = set()
        out: list[list[Task]] = []
        while remaining:
            wave = sorted(
                (tid for tid, deps in remaining.items() if deps <= done),
                key=lambda tid: (self._tasks[tid].priority, tid),
            )
            if not wave:
                raise CyclicDependencyError(
                    f"dependency cycle among tasks: {', '.join(sorted(remaining))}"
                )
            out.append([self._tasks[tid] for tid in wave])
            done |= set(wave)
            for tid in wave:
                remaining.pop(tid)
        return out

    def ready_tasks(self) -> list[Task]:
        """Pending tasks whose dependencies have all completed successfully."""
        ready = []
        for task in self._tasks.values():
            if task.status not in (TaskStatus.PENDING, TaskStatus.READY, TaskStatus.RETRYING):
                continue
            if self._deps_satisfied(task):
                ready.append(task)
        ready.sort(key=lambda t: (t.priority, t.created_at, t.id))
        return ready

    def blocked_tasks(self) -> list[Task]:
        """Pending tasks that can never run because a required dependency failed."""
        blocked = []
        for task in self._tasks.values():
            if task.status.terminal:
                continue
            for dep_id in task.dependencies:
                dep = self._tasks.get(dep_id)
                if dep is None:
                    continue
                failed = dep.status in (
                    TaskStatus.FAILED,
                    TaskStatus.SKIPPED,
                    TaskStatus.CANCELLED,
                )
                if failed and not dep.optional:
                    blocked.append(task)
                    break
        return blocked

    def _deps_satisfied(self, task: Task) -> bool:
        for dep_id in task.dependencies:
            dep = self._tasks.get(dep_id)
            if dep is None:
                return False
            if dep.status is TaskStatus.COMPLETED:
                continue
            # An optional dependency that finished badly still unblocks us.
            if dep.optional and dep.status.terminal:
                continue
            return False
        return True

    def to_dict(self) -> dict:
        return {"tasks": [t.to_dict() for t in self.topological_order()]}


@dataclass
class Usage:
    """Token accounting for one provider call or one agent instance."""

    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens

    def __add__(self, other: "Usage") -> "Usage":
        return Usage(
            self.input_tokens + other.input_tokens,
            self.output_tokens + other.output_tokens,
        )

    def to_dict(self) -> dict:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total,
        }


@dataclass
class AgentResult:
    """The structured return value of one agent instance."""

    agent_id: str
    task_id: str
    status: TaskStatus
    instance_id: str = field(default_factory=lambda: new_id("inst"))
    agent_name: str = ""
    output: str = ""
    artifacts: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    tool_calls: list[dict] = field(default_factory=list)
    memory_writes: list[dict] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    provider: str = ""
    model: str = ""
    started_at: float = field(default_factory=now)
    completed_at: float | None = None
    context_keys: list[str] = field(default_factory=list)
    """Which context slices this instance was given -- the audit trail for
    context isolation (``ai/memory/context-management.md``)."""

    @property
    def ok(self) -> bool:
        return self.status is TaskStatus.COMPLETED

    @property
    def execution_time_s(self) -> float:
        return (self.completed_at or now()) - self.started_at

    def to_dict(self) -> dict:
        return {
            "instance_id": self.instance_id,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "task_id": self.task_id,
            "status": self.status.value,
            "output": self.output,
            "artifacts": dict(self.artifacts),
            "errors": list(self.errors),
            "tool_calls": list(self.tool_calls),
            "memory_writes": list(self.memory_writes),
            "usage": self.usage.to_dict(),
            "provider": self.provider,
            "model": self.model,
            "execution_time_s": round(self.execution_time_s, 4),
            "context_keys": list(self.context_keys),
        }


@dataclass
class ReviewFinding:
    """One actionable defect, per ``ai/orchestration/reviewer.md``."""

    task_id: str
    severity: str = "medium"
    issue: str = ""
    required_change: str = ""
    reviewer: str = "orchestration/reviewer"

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "severity": self.severity,
            "issue": self.issue,
            "required_change": self.required_change,
            "reviewer": self.reviewer,
        }


@dataclass
class ReviewReport:
    """A reviewer's verdict over an aggregated set of results."""

    verdict: "object"  # Verdict; annotated loosely to avoid a circular import
    summary: str = ""
    findings: list[ReviewFinding] = field(default_factory=list)
    reviewer: str = "orchestration/reviewer"
    usage: Usage = field(default_factory=Usage)

    def findings_for(self, task_id: str) -> list[ReviewFinding]:
        return [f for f in self.findings if f.task_id == task_id]

    @property
    def tasks_needing_rework(self) -> list[str]:
        seen: list[str] = []
        for f in self.findings:
            if f.task_id not in seen and f.severity in ("critical", "high", "medium"):
                seen.append(f.task_id)
        return seen

    def to_dict(self) -> dict:
        return {
            "reviewer": self.reviewer,
            "verdict": getattr(self.verdict, "value", str(self.verdict)),
            "summary": self.summary,
            "findings": [f.to_dict() for f in self.findings],
            "usage": self.usage.to_dict(),
        }


@dataclass
class RunRecord:
    """The complete, serializable record of one orchestration run.

    This is the single source the Agent Map, the CLI, and any future API read
    from. Nothing about a run lives only in memory of the orchestrator.
    """

    request: str
    id: str = field(default_factory=lambda: new_id("run"))
    status: RunStatus = RunStatus.PENDING
    root_task_id: str | None = None
    entry_agent: str = "orchestration/ceo-agent"
    graph: TaskGraph = field(default_factory=TaskGraph)
    results: dict[str, AgentResult] = field(default_factory=dict)
    reviews: list[ReviewReport] = field(default_factory=list)
    plan: dict = field(default_factory=dict)
    final_output: str = ""
    errors: list[str] = field(default_factory=list)
    requires_human_approval: bool = False
    approval_reason: str = ""
    started_at: float = field(default_factory=now)
    completed_at: float | None = None
    budget: dict = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)

    @property
    def duration_s(self) -> float:
        return (self.completed_at or now()) - self.started_at

    @property
    def usage(self) -> Usage:
        total = Usage()
        for r in self.results.values():
            total = total + r.usage
        for review in self.reviews:
            total = total + review.usage
        return total

    def result_for(self, task_id: str) -> AgentResult | None:
        return self.results.get(task_id)

    def successful_results(self) -> list[AgentResult]:
        return [r for r in self.results.values() if r.ok]

    def failed_results(self) -> list[AgentResult]:
        return [r for r in self.results.values() if not r.ok]

    def to_dict(self) -> dict:
        return {
            "run_id": self.id,
            "request": self.request,
            "status": self.status.value,
            "entry_agent": self.entry_agent,
            "root_task": self.root_task_id,
            "plan": self.plan,
            "graph": self.graph.to_dict(),
            "results": {tid: r.to_dict() for tid, r in self.results.items()},
            "reviews": [r.to_dict() for r in self.reviews],
            "final_output": self.final_output,
            "errors": list(self.errors),
            "requires_human_approval": self.requires_human_approval,
            "approval_reason": self.approval_reason,
            "usage": self.usage.to_dict(),
            "budget": dict(self.budget),
            "started_at": iso(self.started_at),
            "completed_at": iso(self.completed_at) if self.completed_at else None,
            "duration_s": round(self.duration_s, 4),
        }


#: Convenience alias used by context builders.
ResultMap = Mapping[str, AgentResult]
