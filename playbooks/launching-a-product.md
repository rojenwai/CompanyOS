# Playbook: Launching a Product

**When to use:** a product/feature is built and you are taking it live.

1. **Confirm readiness** — pass the [product launch checklist](../product/quality-gates.md) and the
   engineering [release checklist](../templates/documents/release-checklist.md).
2. **Prepare operations** — [monitoring & alerts](../post-launch/monitoring.md) configured; on-call
   briefed ([on-call](../post-launch/on-call.md)); [rollback](../post-launch/rollback.md) tested.
3. **Prepare go-to-market** — positioning, messaging, and launch plan ready ([GTM](../strategy/go-to-market.md)).
4. **Ship** — deploy phased/canary via [release management](../post-launch/release-management.md); verify
   health in [observability](../post-launch/observability.md).
5. **Announce** — changelog and customer comms.
6. **Watch** — track the [success metric](../product/metrics.md) and telemetry; be ready to
   [roll back](../post-launch/rollback.md).
7. **Review** — schedule the post-launch review; feed learnings into
   [continuous improvement](../post-launch/continuous-improvement.md).

**Success criteria:** launched with monitoring live, rollback ready, and the success metric instrumented.
**Escalate if:** post-launch checks fail → [broken-deployment playbook](../post-launch/playbooks/broken-deployment.md).
