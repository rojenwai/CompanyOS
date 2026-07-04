# Execution Engine

The execution engine carries out approved work and refuses to advance anything that has not cleared
its [quality gate](../governance/quality-gates.md).

## Responsibilities

- Execute or ship approved deliverables (deploys, publishes, commits, actions).
- Enforce the [Definition of Done](../governance/definition-of-done.md) at each step.
- Emit telemetry and status to [dashboards](../governance/README.md).
- On failure, invoke [retry logic and rollback](execution-lifecycle.md).

## Guardrails

- Never executes work that skipped a required review or approval.
- Never performs an irreversible action without recorded [approval](approval-engine.md).
- Every action is logged (see [observability](../post-launch/observability.md)); secrets are never logged.

## Post-execution

On completion it notifies the [Continuous Improvement Engine](continuous-improvement-engine.md) so
outcomes and lessons are captured to [memory](../memory/).
