# Execution Lifecycle

The states every unit of work moves through, and the rules for delegation, conflict resolution, and
retries.

## States

```
QUEUED → ASSIGNED → IN_PROGRESS → IN_REVIEW → AWAITING_APPROVAL → EXECUTING → DONE
                          │             │              │              │
                          └─ BLOCKED ◄──┴──────────────┴──────────────┘
                          └─ FAILED → (retry) → ASSIGNED
```

## Delegation

Work is delegated top-down: [CEO Agent](ceo-agent.md) → [Planner](planner.md) →
[Task Decomposer](task-decomposer.md) → [Coordinator](coordinator.md) → specialist agents. Each level
delegates the *what*, and the level below owns the *how*.

## Conflict resolution

When two agents disagree or produce incompatible outputs:

1. Compare against acceptance criteria and [standards](../../handbook/standards/) — the objective rule wins.
2. If still tied, the owning executive agent decides.
3. If cross-domain, the [CEO Agent](ceo-agent.md) decides, recording rationale to [decision memory](../memory/decision-memory.md).

## Retry logic

- **Transient failure** (tool/timeout): retry with backoff, up to a bounded limit.
- **Deterministic failure** (wrong output): return to the author with the [Reviewer](reviewer.md) findings; do not blind-retry.
- **Repeated failure**: escalate to the CEO Agent; consider re-planning.
- **Post-execution failure**: trigger [rollback](../../handbook/departments/post-launch/rollback.md) and an [incident report](../../handbook/templates/documents/incident-report.md).

## Idempotency & safety

Irreversible actions run only after recorded [approval](approval-engine.md) and are designed to be
safely re-runnable or explicitly guarded against double-execution.
