# Playbook: Slow API

**When to use:** API latency degrades (p95/p99 breaches [SLA](../sla.md)).

1. **Confirm** scope: which endpoints, since when, correlated with a deploy or traffic change?
2. **Check the usual causes:** slow DB queries (missing index), downstream dependency, cache miss storm, resource saturation.
3. **Mitigate:** scale out, enable/raise caching, or [rollback](rollback.md) a recent change.
4. **Diagnose** with traces ([observability](../observability.md)); find the slow span.
5. **Fix** the bottleneck; add a [performance regression test](../../engineering/performance-standards.md).

**Success criteria:** latency back within SLA; regression guard added.
**Escalate if:** latency breach is customer-critical → declare an [incident](../incident-response.md).
