"""Runtime status vocabulary.

These extend -- rather than replace -- the states written in
``ai/orchestration/execution-lifecycle.md``:

    QUEUED -> ASSIGNED -> IN_PROGRESS -> IN_REVIEW -> AWAITING_APPROVAL -> EXECUTING -> DONE

The spec states are the *work item* lifecycle. ``TaskStatus`` below is that
lifecycle plus the runtime states a real scheduler needs (CANCELLED, SKIPPED,
RETRYING). ``spec_state()`` maps a runtime status back onto the documented
vocabulary so dashboards and the handbook stay consistent.
"""

from __future__ import annotations

from enum import Enum


class TaskStatus(str, Enum):
    """Lifecycle of a single task node in the run graph."""

    PENDING = "pending"
    """Created, dependencies not yet satisfied."""

    READY = "ready"
    """Dependencies satisfied, waiting for a scheduler slot."""

    SPAWNING = "spawning"
    """An agent instance is being created for this task."""

    RUNNING = "running"
    """The agent instance is executing."""

    WAITING = "waiting"
    """Blocked on an external signal (tool, approval, human)."""

    REVIEWING = "reviewing"
    """Output produced, under reviewer critique."""

    RETRYING = "retrying"
    """Rejected or failed; queued for another attempt."""

    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    """Not run because a required dependency failed."""

    CANCELLED = "cancelled"

    @property
    def terminal(self) -> bool:
        return self in _TERMINAL

    @property
    def successful(self) -> bool:
        return self is TaskStatus.COMPLETED


_TERMINAL = frozenset(
    {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.SKIPPED, TaskStatus.CANCELLED}
)


class RunStatus(str, Enum):
    """Lifecycle of a whole orchestration run."""

    PENDING = "pending"
    PLANNING = "planning"
    SPAWNING = "spawning"
    RUNNING = "running"
    REVIEWING = "reviewing"
    RETRYING = "retrying"
    SYNTHESIZING = "synthesizing"
    AWAITING_APPROVAL = "awaiting_approval"
    """A Security Reviewer block or an irreversible action needs a human.

    See ``ai/orchestration/approval-engine.md`` -- this state is never
    auto-cleared by the runtime.
    """

    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @property
    def terminal(self) -> bool:
        return self in {
            RunStatus.COMPLETED,
            RunStatus.FAILED,
            RunStatus.CANCELLED,
            RunStatus.AWAITING_APPROVAL,
        }


#: Runtime status -> the state name used in execution-lifecycle.md.
_SPEC_STATE = {
    TaskStatus.PENDING: "QUEUED",
    TaskStatus.READY: "QUEUED",
    TaskStatus.SPAWNING: "ASSIGNED",
    TaskStatus.RUNNING: "IN_PROGRESS",
    TaskStatus.WAITING: "BLOCKED",
    TaskStatus.REVIEWING: "IN_REVIEW",
    TaskStatus.RETRYING: "ASSIGNED",
    TaskStatus.COMPLETED: "DONE",
    TaskStatus.FAILED: "FAILED",
    TaskStatus.SKIPPED: "BLOCKED",
    TaskStatus.CANCELLED: "FAILED",
}


def spec_state(status: TaskStatus) -> str:
    """Translate a runtime status into the documented lifecycle state."""
    return _SPEC_STATE[status]


class Verdict(str, Enum):
    """Reviewer verdicts, as written in ``ai/orchestration/reviewer.md``."""

    APPROVE = "approve"
    APPROVE_WITH_CHANGES = "approve_with_changes"
    REVISE = "revise"
    REJECT = "reject"
    ESCALATE = "escalate"
    BLOCK = "block"
    """Security Reviewer only. Cannot be auto-approved."""

    @property
    def needs_rework(self) -> bool:
        return self in {Verdict.REVISE, Verdict.REJECT}

    @property
    def needs_human(self) -> bool:
        return self in {Verdict.ESCALATE, Verdict.BLOCK}
