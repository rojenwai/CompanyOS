# Example - RFC: Move background jobs to a durable queue

> Worked example - illustrative, not a live record. Uses the [RFC template](../../../templates/documents/rfc.md).

**Status:** Accepted · **Author:** Backend Engineer · **Reviewers:** Software Architect, SRE

## Problem

Background jobs run in-process on the API servers. When a server restarts during a deploy, in-flight jobs
are lost silently. In the last quarter this caused 3 incidents and ~40 lost customer exports, discovered
only when customers complained - a violation of our "detect before customers" principle
([post-launch](../../post-launch/principles.md)).

## Goals

- No job is lost on deploy or crash.
- Failed jobs are retried with backoff and land in a dead-letter queue after N attempts.
- Job execution is observable (queue depth, age, failure rate).

## Non-goals

- Sub-second job latency. Current p95 of ~30s is acceptable.
- Replacing the scheduler for cron-style jobs (separate RFC).

## Proposal

Introduce a durable queue. Producers enqueue a job with an idempotency key; a separate worker pool
consumes. Workers are stateless and horizontally scalable. Jobs are at-least-once delivered, so **every
handler must be idempotent** - enforced by requiring an idempotency key at enqueue time.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Keep in-process, drain on shutdown | Doesn't survive crashes, only graceful deploys |
| Database-backed job table | Works, but we'd rebuild retries, backoff, and DLQ ourselves |
| Managed queue service | **Chosen** - durable, battle-tested, less to operate |

## Risks

- **At-least-once delivery** means duplicate execution. Mitigation: idempotency keys are mandatory; a
  migration checklist audits every existing handler.
- **New infrastructure** to operate. Mitigation: managed service; runbook + alerts on queue depth and DLQ.

## Rollout

Behind a flag, one job type at a time, dual-running against the old path and comparing results for a week.
Reversible at every step ([rollback](../../post-launch/rollback.md)).

## Decision

Accepted. Recorded as an [ADR](adr-example.md); tracked to completion with a test proving no job loss
across a forced worker kill.
