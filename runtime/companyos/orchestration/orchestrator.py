"""The Orchestrator: the executable form of ``ai/orchestration/README.md``.

    request -> CEO/entry -> Planner -> Task Decomposer -> selection -> spawning
            -> parallel execution -> aggregation -> review -> (rework) -> synthesis

Everything it coordinates is replaceable: the registry reads Markdown specs, the
provider is an interface, the scheduler only knows about a DAG, and the
reviewers are whichever reviewer specs the repository contains.
"""

from __future__ import annotations

import asyncio
from typing import Any, Mapping, Sequence

from ..config import Budget, RuntimeConfig
from ..errors import LimitExceeded, NoSuitableAgentError
from ..ids import now
from ..memory.scratch import RunScratchpad
from ..memory.store import MemoryStore
from ..models import AgentResult, RunRecord, Task, TaskGraph
from ..observability import EventBus, EventType, JsonlSink
from ..providers import Provider, resolve_provider
from ..registry import AgentRegistry
from ..registry import capabilities as caps
from ..status import RunStatus, TaskStatus, Verdict
from ..tools import ToolRegistry
from .aggregator import Aggregation, ResultAggregator
from .agent_map import build_agent_map
from .context import ContextBuilder
from .decomposer import TaskDecomposer
from .planner import Planner
from .reviewer import ReviewCoordinator
from .scheduler import DAGScheduler
from .selector import AgentSelector
from .spawner import AgentSpawner
from .synthesizer import Synthesizer

#: Agent budget held back for the reviewers, so execution cannot consume it all.
_REVIEWER_RESERVE = 2


class Orchestrator:
    """Runs one request end to end."""

    def __init__(
        self,
        config: RuntimeConfig,
        *,
        registry: AgentRegistry | None = None,
        provider: Provider | None = None,
        tools: ToolRegistry | None = None,
        memory: MemoryStore | None = None,
        bus: EventBus | None = None,
        entry_agent: str | None = None,
        trace_to_disk: bool = True,
    ) -> None:
        self.config = config
        self.registry = registry or AgentRegistry.discover(config.root)
        self.provider = provider or resolve_provider(config.provider)
        self.tools = tools or ToolRegistry.default()
        self.bus = bus or EventBus()
        self.selector = AgentSelector(self.registry)
        self.entry_agent = entry_agent or self.registry.ceo_id
        self.trace_to_disk = trace_to_disk

        if memory is None:
            from ..memory.filestore import FileMemoryStore

            memory = FileMemoryStore(
                config.root, allow_promotion=config.allow_memory_promotion
            )
        self.memory = memory

    # -- public API ------------------------------------------------------------

    def run_sync(self, request: str, **kwargs: Any) -> RunRecord:
        """Blocking wrapper around :meth:`run`, for CLI and scripts."""
        return asyncio.run(self.run(request, **kwargs))

    async def run(
        self, request: str, *, cancel: asyncio.Event | None = None
    ) -> RunRecord:
        """Execute a request and return the complete run record."""
        # Fail fast on a misconfigured provider, before any state is created.
        # Degrading gracefully is right for a step that fails mid-run; it is
        # wrong for a run that could never have worked.
        self.provider.preflight()

        run = RunRecord(request=request.strip(), entry_agent=self.entry_agent)
        budget = Budget(self.config.limits)
        scratch = RunScratchpad(run.id)
        sink: JsonlSink | None = None

        if self.trace_to_disk:
            try:
                sink = JsonlSink(self.config.traces_dir, run.id)
                self.bus.subscribe(sink)
            except OSError:  # pragma: no cover - unwritable trace dir is not fatal
                sink = None

        self.bus.emit(
            EventType.RUN_STARTED,
            run_id=run.id,
            agent_id=self.entry_agent,
            message=run.request[:120],
            data={"provider": self.provider.describe(), "limits": budget.snapshot()["limits"]},
        )

        try:
            await self._execute_run(run, budget, scratch, cancel)
        except asyncio.CancelledError:
            run.status = RunStatus.CANCELLED
            run.errors.append("run cancelled")
            raise
        except LimitExceeded as exc:
            run.errors.append(str(exc))
            self.bus.emit(
                EventType.LIMIT_HIT, run_id=run.id, message=str(exc), data={"limit": exc.limit}
            )
            if run.status not in (RunStatus.AWAITING_APPROVAL,):
                run.status = RunStatus.COMPLETED if run.final_output else RunStatus.FAILED
        except Exception as exc:  # noqa: BLE001 - a run must always return a record
            run.status = RunStatus.FAILED
            run.errors.append(f"{type(exc).__name__}: {exc}")
            self.bus.emit(EventType.RUN_FAILED, run_id=run.id, message=str(exc))
        finally:
            run.completed_at = now()
            run.budget = budget.snapshot()
            run.events = self.bus.to_list()
            self.bus.emit(
                EventType.RUN_COMPLETED,
                run_id=run.id,
                message=run.status.value,
                data={
                    "duration_s": round(run.duration_s, 3),
                    "usage": run.usage.to_dict(),
                    "agents_spawned": budget.agents_spawned,
                },
            )
            run.events = self.bus.to_list()
            if sink is not None:
                sink.close()

        return run

    def agent_map(self, run: RunRecord) -> dict:
        """The Agent Map document for a finished or in-flight run."""
        return build_agent_map(run, self.registry)

    # -- the pipeline ----------------------------------------------------------

    async def _execute_run(
        self,
        run: RunRecord,
        budget: Budget,
        scratch: RunScratchpad,
        cancel: asyncio.Event | None,
    ) -> None:
        planner = Planner(self.registry, self.provider, self.config, self.bus, self.memory)
        decomposer = TaskDecomposer(self.registry, self.provider, self.config, self.bus)
        aggregator = ResultAggregator()
        review_coordinator = ReviewCoordinator(
            self.registry, self.selector, self.provider, self.config, self.bus
        )
        synthesizer = Synthesizer(
            self.registry, self.provider, self.config, self.bus, self.entry_agent
        )
        context_builder = ContextBuilder(self.config, self.memory)
        spawner = AgentSpawner(
            self.config, self.provider, self.tools, self.bus, budget, self.memory, scratch
        )
        scheduler = DAGScheduler(self.config, self.bus, run.id)

        # 1. PLAN ---------------------------------------------------------------
        self._set_status(run, RunStatus.PLANNING)
        plan, plan_usage = await planner.plan(run.request, run_id=run.id)
        run.plan = plan
        budget.charge_tokens(plan_usage.total)

        # 2. DECOMPOSE ----------------------------------------------------------
        max_tasks = max(1, self.config.limits.max_agents - _REVIEWER_RESERVE)
        graph, decompose_usage = await decomposer.decompose(
            run.request, plan, run_id=run.id, max_tasks=max_tasks
        )
        run.graph = graph
        run.root_task_id = graph.tasks[0].id if len(graph) else None
        budget.charge_tokens(decompose_usage.total)

        # 3. SELECT -------------------------------------------------------------
        self._set_status(run, RunStatus.SPAWNING)
        self._assign_agents(graph, plan, run)

        async def execute(task: Task) -> AgentResult:
            return await self._run_task(
                task, graph, run, spawner, context_builder, plan
            )

        # 4-6. EXECUTE -> REVIEW -> REWORK --------------------------------------
        aggregation = Aggregation()
        review = None
        pending: set[str] | None = None

        while True:
            try:
                budget.charge_iteration()
            except LimitExceeded as exc:
                self.bus.emit(
                    EventType.LIMIT_HIT, run_id=run.id, message=str(exc),
                    data={"limit": exc.limit},
                )
                break

            self._set_status(run, RunStatus.RUNNING)
            await scheduler.run(
                graph, execute, cancel=cancel, results=run.results, only=pending
            )
            if cancel is not None and cancel.is_set():
                run.status = RunStatus.CANCELLED
                run.errors.append("run cancelled")
                return

            aggregation = aggregator.collect(graph, run.results)

            self._set_status(run, RunStatus.REVIEWING)
            review = await review_coordinator.review(
                run.request, aggregation, run_id=run.id, concerns=self._concerns(graph)
            )
            run.reviews.append(review)
            budget.charge_tokens(review.usage.total)

            if review.verdict.needs_human:
                run.requires_human_approval = True
                run.approval_reason = (
                    f"{review.verdict.value} from {review.reviewer}: {review.summary}"
                )
                break
            if not review.verdict.needs_rework:
                break

            pending = self._open_rework(graph, review, budget, run)
            if not pending:
                break
            self._set_status(run, RunStatus.RETRYING)

        # 7. SYNTHESIZE ---------------------------------------------------------
        self._set_status(run, RunStatus.SYNTHESIZING)
        run.final_output, synth_usage = await synthesizer.synthesize(
            run.request, aggregation, review, run_id=run.id, plan=plan
        )
        try:
            budget.charge_tokens(synth_usage.total)
        except LimitExceeded:
            pass  # the answer is already composed; do not discard it

        spawner.terminate_all("run finished")
        self._record_memory_proposals(run)

        if run.requires_human_approval:
            run.status = RunStatus.AWAITING_APPROVAL
        elif aggregation.empty:
            run.status = RunStatus.FAILED
        else:
            run.status = RunStatus.COMPLETED

    # -- stages ----------------------------------------------------------------

    def _assign_agents(
        self, graph: TaskGraph, plan: Mapping[str, Any], run: RunRecord
    ) -> None:
        """Capability-match every task to an agent definition, before execution."""
        assigned: set[str] = set()
        for task in graph:
            required = task.required_capabilities or list(
                plan.get("required_capabilities") or []
            )[:1]
            text = f"{task.objective}\n{task.description}"
            try:
                # Prefer staffing a specialist not already working this run --
                # two tasks that both half-match one agent are better served by
                # two agents. Reuse is still allowed when nothing else fits.
                try:
                    candidate = self.selector.select(required, text, exclude=assigned)
                except NoSuitableAgentError:
                    candidate = self.selector.select(required, text)
            except NoSuitableAgentError as exc:
                # task-routing.md: no match escalates rather than guessing.
                task.mark(TaskStatus.FAILED, error=str(exc))
                self.bus.emit(
                    EventType.SELECTION_FAILED,
                    run_id=run.id,
                    task_id=task.id,
                    message=str(exc),
                    data={"required_capabilities": required},
                )
                continue

            task.assigned_agent = candidate.agent_id
            assigned.add(candidate.agent_id)
            self.bus.emit(
                EventType.AGENT_SELECTED,
                run_id=run.id,
                task_id=task.id,
                agent_id=candidate.agent_id,
                message=f"{candidate.definition.name} (score {candidate.score:.2f})",
                data=candidate.to_dict(),
            )

    async def _run_task(
        self,
        task: Task,
        graph: TaskGraph,
        run: RunRecord,
        spawner: AgentSpawner,
        context_builder: ContextBuilder,
        plan: Mapping[str, Any],
    ) -> AgentResult:
        """Spawn one temporary instance, run it, retire it."""
        definition = self.registry.get(task.assigned_agent or "")
        task.attempts += 1
        bundle = context_builder.build(
            task, graph, run.results, plan=plan, request=run.request
        )
        instance = spawner.spawn(
            definition,
            task,
            bundle,
            run_id=run.id,
            parent_agent_id=self.registry.supervisor_for(definition) or self.entry_agent,
        )
        try:
            return await instance.run()
        finally:
            spawner.retire(instance)

    def _open_rework(
        self, graph: TaskGraph, review, budget: Budget, run: RunRecord
    ) -> set[str]:
        """Return tasks to a specialist with the findings attached.

        Per ``execution-lifecycle.md`` this is a *deterministic* failure path:
        the work goes back to its author with the review findings, not a blind
        retry, and only while attempts and agent budget remain.
        """
        rework: set[str] = set()
        for task_id in review.tasks_needing_rework:
            task = graph.get(task_id)
            if task is None or task.attempts >= self.config.limits.max_attempts_per_task:
                continue
            if budget.agents_remaining() <= 0:
                break
            task.findings = [f.to_dict() for f in review.findings_for(task_id)]
            task.output = None
            task.error = None
            task.completed_at = None
            task.mark(TaskStatus.RETRYING)
            run.results.pop(task_id, None)
            rework.add(task_id)
            self.bus.emit(
                EventType.TASK_RETRY,
                run_id=run.id,
                task_id=task_id,
                agent_id=task.assigned_agent or "",
                message=f"attempt {task.attempts + 1} with {len(task.findings)} finding(s)",
                data={"findings": task.findings},
            )
        return rework

    # -- helpers ---------------------------------------------------------------

    def _set_status(self, run: RunRecord, status: RunStatus) -> None:
        run.status = status
        self.bus.emit(EventType.RUN_STATUS, run_id=run.id, message=status.value)

    @staticmethod
    def _concerns(graph: TaskGraph) -> list[str]:
        """Which reviewer specialities this work calls for."""
        concerns = {"correctness"}
        for task in graph:
            for capability in task.required_capabilities:
                namespace = caps.namespace(capability)
                if namespace == "security":
                    concerns.add("security")
                elif capability.startswith("engineering.testing") or namespace == "devops":
                    concerns.add("quality")
                elif namespace == "docs":
                    concerns.add("documentation")
        return sorted(concerns)

    def _record_memory_proposals(self, run: RunRecord) -> None:
        """Surface proposed memory writes without persisting them."""
        proposals = getattr(self.memory, "proposals", lambda: [])()
        for proposal in proposals:
            if proposal.run_id and proposal.run_id != run.id:
                continue
            self.bus.emit(
                EventType.MEMORY_PROPOSED,
                run_id=run.id,
                task_id=proposal.task_id,
                agent_id=proposal.agent_id,
                message=f"{proposal.store}: {proposal.text[:80]}",
                data=proposal.to_dict(),
            )


def run_request(request: str, config: RuntimeConfig, **kwargs: Any) -> RunRecord:
    """One-call convenience entry point."""
    return Orchestrator(config, **kwargs).run_sync(request)
