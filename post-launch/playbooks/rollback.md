# Playbook: Rollback

**When to use:** you need to revert production to the last known-good state. See the full
[rollback policy](../rollback.md).

1. **Confirm** the last known-good version/artifact.
2. **Announce** the rollback ([incident](../incident-response.md) comms).
3. **Execute** via the [Execution Engine](../../orchestration/execution-engine.md) (blue-green switch, previous artifact, or revert).
4. **Verify** health in [observability](../observability.md) (errors, latency, saturation).
5. **Return** the failed change to engineering with a reproducing test.

**Success criteria:** production on a known-good version; health green.
**Escalate if:** rollback fails or migrations are irreversible → SEV1 [outage](critical-outage.md) + [approval](../../orchestration/approval-engine.md) for recovery.
