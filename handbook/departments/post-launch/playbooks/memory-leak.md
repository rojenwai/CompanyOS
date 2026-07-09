# Playbook: Memory Leak

**When to use:** memory usage grows unbounded; OOM kills or restarts.

1. **Stabilize:** restart/recycle affected instances; scale out temporarily to hold SLA.
2. **Confirm** the trend in [observability](../observability.md) (memory over time, correlate with a deploy).
3. **Bisect:** did it start with a release? → consider [rollback](../rollback.md).
4. **Diagnose:** capture a heap profile; find the retained allocations ([Performance Monitoring Agent](../../../../ai/agents/post-launch/performance-monitoring-agent.md)).
5. **Fix** the leak; add a regression guard ([performance standards](../../engineering/performance-standards.md)).

**Success criteria:** memory stable over time; no OOM restarts.
**Escalate if:** repeated OOM despite mitigation → declare an [incident](../incident-response.md).
