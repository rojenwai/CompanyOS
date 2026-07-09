# Hotfix Policy

A hotfix is an urgent, narrowly-scoped fix to production outside the normal release train.

## When a hotfix is justified

- An active [SEV1/SEV2 incident](incident-response.md) that [rollback](rollback.md) cannot resolve.
- A critical security vulnerability under active exploitation.

## Rules

- **Minimal scope** — fix only the failing behavior; no unrelated changes.
- **Still reviewed** — an expedited [review](review-process.md) and [security check](../../../ai/orchestration/security-reviewer.md) still apply; quality gates are compressed, not skipped.
- **Tested** — includes a test reproducing the issue.
- **Approved** — production change requires [approval](../../../ai/orchestration/approval-engine.md).
- **Back-merged** — the fix is merged back into `develop`/`main` so it is not lost in the next release.

## Branch

Hotfixes use `hotfix/<name>` off the release branch ([engineering workflow](../engineering/workflows.md)),
and follow the [emergency-hotfix playbook](playbooks/emergency-hotfix.md).
