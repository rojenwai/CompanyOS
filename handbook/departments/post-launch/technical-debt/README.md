# Technical Debt

Debt is not a moral failing - it is a deliberate trade made under time pressure. What is unacceptable is
**undocumented, untracked, unrepaid** debt. This folder is the system that keeps debt visible and shrinking.

The governing rule, from [post-launch standards](../standards.md): debt is allowed only if it is
**documented, estimated, prioritized, and scheduled for repayment** - and every sprint allocates capacity
to pay some down.

## Index

| File | Purpose |
|---|---|
| [policy.md](policy.md) | When taking on debt is allowed, and the conditions attached |
| [tracking.md](tracking.md) | How debt is recorded and kept visible |
| [prioritization.md](prioritization.md) | How debt items are ranked against each other and against features |
| [repayment-plan.md](repayment-plan.md) | How debt is scheduled and paid down |
| [review-process.md](review-process.md) | How debt is reviewed, and by whom |
| [metrics.md](metrics.md) | How the debt trend is measured |

## Who runs it

The [Technical Debt Agent](../../../../ai/agents/post-launch/technical-debt-agent.md) scans for, records,
and ranks debt; [engineering](../../engineering/technical-debt-policy.md) owns repayment capacity;
the trend is reported on the [maintenance dashboard](../dashboards.md).
