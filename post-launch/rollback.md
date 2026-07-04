# Rollback

Every release must be reversible. Rollback restores the last known-good state quickly and safely.

## When to roll back

- A [release checklist](../templates/documents/release-checklist.md) post-deploy check fails.
- Error rate, latency, or saturation breaches thresholds after a deploy.
- A [SEV1/SEV2 incident](incident-response.md) is traced to a recent change.

**Mitigate first, diagnose second** — rolling back to stop customer impact is preferred over debugging live.

## Procedure

1. Confirm the last known-good version/artifact.
2. Trigger rollback via the [Execution Engine](../orchestration/execution-engine.md) (automated where possible).
3. Verify health via [observability](observability.md).
4. Communicate status ([incident response](incident-response.md)).
5. Open a postmortem; the failed change returns to engineering with a reproducing test.

## Design requirements

Deploys are designed for rollback: backward-compatible migrations, feature flags, and idempotent
actions ([execution lifecycle](../orchestration/execution-lifecycle.md)).
