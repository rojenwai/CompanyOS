"""Dynamic agent spawning.

    AgentDefinition  (static, from Markdown, shared, long-lived)
           |
      AgentSpawner   (checks budget and depth, resolves tools, builds context)
           |
      AgentInstance  (temporary: one task, one scoped context, one tool grant)
           |
       execution     (provider call + bounded tool loop)
           |
      AgentResult    (structured: output, artifacts, errors, usage, timings)

An instance exists for the duration of one task. It holds no global state, it
cannot spawn anything itself, and it is terminated -- explicitly, and recorded
in the event stream -- as soon as its result is captured.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from .. import purposes
from ..config import Budget, RuntimeConfig
from ..errors import (
    AgentTimeoutError,
    LimitExceeded,
    ProviderError,
    ToolPermissionError,
)
from ..ids import new_id, now
from ..memory.store import MemoryStore
from ..models import AgentResult, Task, Usage
from ..observability import EventBus, EventType
from ..providers import Message, Provider
from ..registry.definition import AgentDefinition
from ..status import TaskStatus
from ..tools import ToolContext, ToolRegistry
from ..tools.policy import ToolPolicy, resolve_policy
from .context import ContextBundle
from .prompts import agent_system_prompt


@dataclass
class AgentInstance:
    """A temporary, running agent. One per task attempt."""

    definition: AgentDefinition
    task: Task
    policy: ToolPolicy
    context: ContextBundle
    provider: Provider
    tools: ToolRegistry
    config: RuntimeConfig
    bus: EventBus
    run_id: str
    parent_agent_id: str = ""
    parent_instance_id: str = ""
    depth: int = 0
    memory: MemoryStore | None = None
    scratch: Any = None
    id: str = field(default_factory=lambda: new_id("inst"))
    status: TaskStatus = TaskStatus.SPAWNING
    _cancelled: bool = field(default=False, repr=False)

    @property
    def agent_id(self) -> str:
        return self.definition.id

    # -- execution -------------------------------------------------------------

    async def run(self) -> AgentResult:
        """Execute the task and return a structured result.

        Never raises for an agent-level failure: a failure becomes an
        ``AgentResult`` with ``status=FAILED``, so one bad branch cannot take
        the run down. Budget violations do propagate -- those are run-level.
        """
        result = AgentResult(
            agent_id=self.agent_id,
            agent_name=self.definition.name,
            task_id=self.task.id,
            instance_id=self.id,
            status=TaskStatus.RUNNING,
            provider=self.provider.name,
            model=self.provider.model,
            context_keys=list(self.context.keys),
        )
        self.status = TaskStatus.RUNNING
        self.bus.emit(
            EventType.AGENT_STARTED,
            run_id=self.run_id,
            task_id=self.task.id,
            agent_id=self.agent_id,
            parent_agent_id=self.parent_agent_id,
            message=self.task.objective[:100],
            data={"instance_id": self.id, "context_keys": list(self.context.keys),
                  "tools": sorted(self.policy.allowed), "depth": self.depth},
        )

        try:
            await self._converse(result)
            result.status = TaskStatus.COMPLETED
        except asyncio.CancelledError:
            result.status = TaskStatus.CANCELLED
            result.errors.append("cancelled")
            self.status = TaskStatus.CANCELLED
            raise
        except AgentTimeoutError as exc:
            result.status = TaskStatus.FAILED
            result.errors.append(str(exc))
            self.bus.emit(
                EventType.AGENT_TIMEOUT,
                run_id=self.run_id,
                task_id=self.task.id,
                agent_id=self.agent_id,
                message=str(exc),
            )
        except LimitExceeded:
            raise
        except (ProviderError, Exception) as exc:  # noqa: B014 - deliberate catch-all
            result.status = TaskStatus.FAILED
            result.errors.append(f"{type(exc).__name__}: {exc}")

        result.completed_at = now()
        self.status = result.status

        event = EventType.AGENT_COMPLETED if result.ok else EventType.AGENT_FAILED
        self.bus.emit(
            event,
            run_id=self.run_id,
            task_id=self.task.id,
            agent_id=self.agent_id,
            parent_agent_id=self.parent_agent_id,
            message=(result.errors[0] if result.errors else f"{len(result.output)} chars"),
            data={
                "instance_id": self.id,
                "execution_time_s": round(result.execution_time_s, 3),
                "usage": result.usage.to_dict(),
                "tool_calls": len(result.tool_calls),
            },
        )
        return result

    async def _converse(self, result: AgentResult) -> None:
        """One provider call, plus a bounded tool loop."""
        system = agent_system_prompt(self.definition, allowed_tools=sorted(self.policy.allowed))
        body = self.context.render(self.config.limits.max_context_chars)
        messages = [
            Message(
                "user",
                f"{body}\n\nProduce your deliverable now. Be specific and concise. "
                f"State assumptions explicitly; never invent facts, numbers, or citations.",
            )
        ]
        tool_specs = self.tools.specs_for(self.policy.allowed)

        for _ in range(self.policy.max_calls + 1):
            if self._cancelled:
                raise asyncio.CancelledError
            completion = await self.provider.complete(
                system=system,
                messages=messages,
                tools=tool_specs or None,
                purpose=purposes.EXECUTE,
                context={
                    "agent_id": self.agent_id,
                    "agent_name": self.definition.name,
                    "task_id": self.task.id,
                    "run_id": self.run_id,
                    "objective": self.task.objective,
                    "acceptance_criteria": list(self.task.acceptance_criteria),
                    "findings": list(self.task.findings),
                },
            )
            result.usage = result.usage + completion.usage

            if not completion.wants_tools:
                result.output = completion.text
                return

            messages.append(Message("assistant", completion.text or "[tool use]"))
            for call in completion.tool_calls:
                messages.append(
                    Message(
                        "tool",
                        self._invoke_tool(call.name, call.arguments, result),
                        tool_call_id=call.id,
                    )
                )

        result.errors.append(
            f"tool-call budget exhausted after {self.policy.max_calls} calls"
        )
        result.output = result.output or "[no deliverable produced before the tool budget ran out]"

    def _invoke_tool(self, name: str, arguments: Any, result: AgentResult) -> str:
        """Permission-check, then run, one tool call."""
        try:
            self.policy.check(name)
        except ToolPermissionError as exc:
            self.bus.emit(
                EventType.TOOL_DENIED,
                run_id=self.run_id,
                task_id=self.task.id,
                agent_id=self.agent_id,
                message=str(exc),
                data={"tool": name},
            )
            result.tool_calls.append({"tool": name, "ok": False, "error": str(exc)})
            return f"DENIED: {exc}"

        outcome = self.tools.get(name).invoke(arguments or {}, self._tool_context())
        result.tool_calls.append(outcome.to_dict())
        self.bus.emit(
            EventType.TOOL_CALLED,
            run_id=self.run_id,
            task_id=self.task.id,
            agent_id=self.agent_id,
            message=f"{name} -> {'ok' if outcome.ok else outcome.error}",
            data={"tool": name},
        )
        if name == "remember" and outcome.ok:
            result.memory_writes.append({"tool": name, "detail": outcome.content})
        return outcome.content if outcome.ok else f"ERROR: {outcome.error}"

    def _tool_context(self) -> ToolContext:
        return ToolContext(
            root=self.config.root,
            run_id=self.run_id,
            task_id=self.task.id,
            agent_id=self.agent_id,
            readable_dirs=self.config.readable_dirs,
            memory=self.memory,
            scratch=self.scratch,
        )

    # -- lifecycle -------------------------------------------------------------

    def terminate(self, reason: str = "task complete") -> None:
        """Retire the instance. Instances are never reused across tasks."""
        self._cancelled = True
        self.bus.emit(
            EventType.AGENT_TERMINATED,
            run_id=self.run_id,
            task_id=self.task.id,
            agent_id=self.agent_id,
            message=reason,
            data={"instance_id": self.id},
        )


class AgentSpawner:
    """Creates agent instances, and refuses to create too many.

    Every guard that stops runaway spawning lives here: the agent budget, the
    task-depth cap, and the tool policy each instance is born with.
    """

    def __init__(
        self,
        config: RuntimeConfig,
        provider: Provider,
        tools: ToolRegistry,
        bus: EventBus,
        budget: Budget,
        memory: MemoryStore | None = None,
        scratch: Any = None,
    ) -> None:
        self.config = config
        self.provider = provider
        self.tools = tools
        self.bus = bus
        self.budget = budget
        self.memory = memory
        self.scratch = scratch
        self.live: dict[str, AgentInstance] = {}
        self.spawned: list[AgentInstance] = []

    def spawn(
        self,
        definition: AgentDefinition,
        task: Task,
        context: ContextBundle,
        *,
        run_id: str,
        parent_agent_id: str = "",
        parent_instance_id: str = "",
    ) -> AgentInstance:
        """Create one temporary instance of ``definition`` bound to ``task``."""
        if task.depth > self.config.limits.max_depth:
            raise LimitExceeded("max_depth", task.depth, self.config.limits.max_depth)
        self.budget.charge_agent()

        instance = AgentInstance(
            definition=definition,
            task=task,
            policy=resolve_policy(definition, self.config, self.tools),
            context=context,
            provider=self.provider,
            tools=self.tools,
            config=self.config,
            bus=self.bus,
            run_id=run_id,
            parent_agent_id=parent_agent_id,
            parent_instance_id=parent_instance_id,
            depth=task.depth,
            memory=self.memory,
            scratch=self.scratch,
        )
        self.live[instance.id] = instance
        self.spawned.append(instance)

        self.bus.emit(
            EventType.AGENT_SPAWNED,
            run_id=run_id,
            task_id=task.id,
            agent_id=definition.id,
            parent_agent_id=parent_agent_id,
            message=f"{definition.name} for: {task.objective[:80]}",
            data={
                "instance_id": instance.id,
                "division": definition.division,
                "depth": task.depth,
                "tools": sorted(instance.policy.allowed),
                "agents_spawned": self.budget.agents_spawned,
                "agents_remaining": self.budget.agents_remaining(),
            },
        )
        return instance

    def retire(self, instance: AgentInstance, reason: str = "task complete") -> None:
        """Terminate an instance and drop it from the live set."""
        instance.terminate(reason)
        self.live.pop(instance.id, None)

    def terminate_all(self, reason: str = "run finished") -> None:
        for instance in list(self.live.values()):
            self.retire(instance, reason)

    def snapshot(self) -> dict:
        return {
            "live": [
                {"instance_id": i.id, "agent_id": i.agent_id, "task_id": i.task.id}
                for i in self.live.values()
            ],
            "total_spawned": len(self.spawned),
        }
