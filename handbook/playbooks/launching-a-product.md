# Playbook: Launching a Product

**When to use:** a product/feature is built and you are taking it live.

1. **Confirm readiness** — pass the [product launch checklist](../departments/product/quality-gates.md) and the
   engineering [release checklist](../templates/documents/release-checklist.md).
2. **Prepare operations** — [monitoring & alerts](../departments/post-launch/monitoring.md) configured; on-call
   briefed ([on-call](../departments/post-launch/on-call.md)); [rollback](../departments/post-launch/rollback.md) tested.
3. **Prepare go-to-market** — positioning, messaging, and launch plan ready ([GTM](../departments/strategy/go-to-market.md)).
4. **Ship** — deploy phased/canary via [release management](../departments/post-launch/release-management.md); verify
   health in [observability](../departments/post-launch/observability.md).
5. **Announce** — changelog and customer comms.
6. **Watch** — track the [success metric](../departments/product/metrics.md) and telemetry; be ready to
   [roll back](../departments/post-launch/rollback.md).
7. **Review** — schedule the post-launch review; feed learnings into
   [continuous improvement](../departments/post-launch/continuous-improvement.md).

**Success criteria:** launched with monitoring live, rollback ready, and the success metric instrumented.
**Escalate if:** post-launch checks fail → [broken-deployment playbook](../departments/post-launch/playbooks/broken-deployment.md).
