# Incident Report — Checkout latency spike

**Incident ID:** INC-2026-042 · **Severity:** SEV2 · **Status:** Resolved · **Commander:** Maintenance Manager Agent
**Detected:** 14:02 · **Resolved:** 14:38 · **Duration:** 00:36

## Summary

A deploy introduced an unindexed query on the orders table, raising checkout p95 latency from 240ms to
2.9s for ~34 minutes. Rolled back; no data loss; no orders failed, but ~1,100 customers saw slow checkouts.

## Impact

- **Customers affected:** ~1,100 (slow, not failed, checkouts)
- **Services:** checkout API
- **Business:** no revenue lost; SLA latency objective breached for 36 min

## Timeline

| Time | Event |
|---|---|
| 14:00 | Deploy v3.4.1 |
| 14:02 | Latency alert (p95 > 1s) pages on-call |
| 14:10 | SEV2 declared; traced to recent deploy |
| 14:22 | Rollback to v3.4.0 initiated |
| 14:38 | p95 back to 250ms; incident resolved |

## Root cause

A new "orders by status" filter query had no supporting index; under production volume it degraded
sharply. The query was not exercised at production scale in testing.

## Resolution & recovery

Rolled back the deploy. Fix-forward added the missing index and a load test at production scale before redeploy.

## Action items

| Action | Owner | Priority | Due |
|---|---|---|---|
| Add composite index (status, created_at) | Database Engineer | P0 | 2026-04-02 |
| Add production-scale load test for checkout queries | QA Engineer | P1 | 2026-04-05 |
| Add query-plan check to CI for new queries | Cloud Engineer | P2 | 2026-04-12 |

## Lessons learned

Performance tests must run at production-representative scale ([performance standards](../../engineering/performance-standards.md)).
Filed to [lessons-learned](../../../../ai/memory/lessons-learned.md); action item created as tracked
[technical debt](../technical-debt/tracking.md) until the CI check lands.
