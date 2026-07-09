# Technical Debt — Prioritization

Not all debt is equal. Prioritize by **risk × cost-of-delay ÷ effort**.

## Scoring

| Factor | Question |
|---|---|
| Risk | Does it threaten correctness, security, or reliability? |
| Cost of delay | How much does it slow future work or raise bug risk each week? |
| Blast radius | How much of the system does it touch? |
| Effort | How expensive is repayment? |

## Priority tiers

- **P0 — repay now:** threatens correctness/security/reliability. Blocks feature work.
- **P1 — this cycle:** meaningfully slows delivery or raises risk.
- **P2 — scheduled:** cosmetic or low-impact; batch into maintenance.

Debt competes for the sprint's reserved debt capacity ([repayment-plan](repayment-plan.md)), scored
alongside features via the [engineering decision frameworks](../../engineering/decision-frameworks.md).
