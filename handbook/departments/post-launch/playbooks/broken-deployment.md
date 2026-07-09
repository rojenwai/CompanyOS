# Playbook: Broken Deployment

**When to use:** a deploy caused errors, latency, or broken functionality in production.

1. **Detect:** post-deploy health check or alert fails ([quality gates](../quality-gates.md)).
2. **Roll back first** to the last known-good version ([rollback](rollback.md)) — mitigate before diagnosing.
3. **Verify** recovery in [observability](../observability.md).
4. **Diagnose** the failed change offline; add a reproducing test.
5. **Fix forward** and redeploy through the full [release](../release-management.md) gates.

**Success criteria:** production restored within minutes; failed change quarantined with a test.
**Escalate if:** rollback itself fails → declare a SEV1 [outage](critical-outage.md).
