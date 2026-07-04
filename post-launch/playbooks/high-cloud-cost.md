# Playbook: High Cloud Cost

**When to use:** infrastructure cost spikes or drifts above budget.

1. **Confirm** the spike on the [cost dashboard](../dashboards.md); identify the service/resource driving it.
2. **Classify:** legitimate growth · misconfiguration · runaway process · leak · attack (e.g. traffic/abuse).
3. **Contain:** cap/scale-down the offending resource; kill runaway jobs; enable rate limits if abuse.
4. **Right-size:** review provisioning against actual [utilization](../monitoring.md).
5. **Prevent:** add a cost alert/budget guardrail ([Infrastructure Health Agent](../../agents/post-launch/infrastructure-health-agent.md)).

**Success criteria:** cost back within budget; guardrail added.
**Escalate if:** cost is driven by an attack → also run [security-breach](security-breach.md).
