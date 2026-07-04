# Technical Debt — Policy

Technical debt is allowed **only if** it is documented, estimated, prioritized, and scheduled for
repayment. This is the operational home of the engineering
[technical-debt policy](../../engineering/technical-debt-policy.md).

## What counts as debt

Duplicate code · dead code · outdated libraries · architecture drift · code smells · performance
regressions · documentation drift. The [Technical Debt Agent](../../agents/post-launch/technical-debt-agent.md)
detects these continuously.

## Rules

- No undocumented debt — record it when you take it ([tracking](tracking.md)).
- Every sprint allocates capacity to repayment ([repayment-plan](repayment-plan.md)).
- Debt threatening correctness, security, or reliability is repaid before new features.

See also: [tracking](tracking.md) · [prioritization](prioritization.md) · [review-process](review-process.md) ·
[repayment-plan](repayment-plan.md) · [metrics](metrics.md).
