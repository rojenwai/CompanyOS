# Playbook: Critical Outage

**When to use:** a full or partial service outage with customer impact (SEV1/SEV2).

1. **Declare** a SEV1/SEV2 [incident](../incident-response.md); assign an Incident Commander.
2. **Assess** scope via [monitoring](../monitoring.md) and [observability](../observability.md).
3. **Communicate** immediately — status page + stakeholders.
4. **Mitigate first:** is a recent change the cause? → [rollback](../rollback.md). Infra? → failover.
5. **Stabilize**, then diagnose root cause.
6. **Verify** full recovery in observability.
7. **Postmortem** → [lessons-learned](../../memory/lessons-learned.md).

**Success criteria:** service restored within SEV target; customers informed throughout.
**Escalate if:** not mitigated within the SEV1 target → [CEO Agent](../../orchestration/ceo-agent.md) + human leadership.
