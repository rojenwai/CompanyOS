# Release Management

How changes reach customers safely and predictably.

## Release types

Alpha · Internal Alpha · Closed Beta · Public Beta · Release Candidate · General Availability ·
Patch · Hotfix · LTS · Experimental · Canary · Blue-Green · Rolling Deployment.

## Deployment strategies

- **Canary** — release to a small % first; widen if healthy.
- **Blue-Green** — stand up the new version alongside the old; switch traffic; keep the old for instant [rollback](rollback.md).
- **Rolling** — replace instances gradually.

## Process

Every release follows the [release checklist](../templates/documents/release-checklist.md): pass
[quality gates](quality-gates.md) → deploy (phased) → verify via [observability](observability.md) →
announce → monitor. A prepared [rollback](rollback.md) is mandatory.

## Ownership

Coordinated with [product release planning](../product/roadmap.md) and executed by the
[Execution Engine](../orchestration/execution-engine.md); production deploys require
[approval](../orchestration/approval-engine.md).
