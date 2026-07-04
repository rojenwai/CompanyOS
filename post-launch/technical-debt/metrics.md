# Technical Debt — Metrics

What we measure to keep debt under control.

| Metric | Definition | Direction |
|---|---|---|
| Total open debt | Count / estimated effort of open items | ↓ or stable |
| Debt trend | New vs. repaid per cycle | net ↓ |
| Repayment rate | Items/effort repaid per cycle | ≥ intake |
| P0 age | How long critical debt stays open | ↓ (target: near zero) |
| Debt-linked incidents | Incidents traceable to known debt | ↓ |
| Coverage of hotspots | Test coverage in high-churn/high-debt areas | ↑ |

## Rule

If intake outpaces repayment for consecutive cycles, that is a signal to raise the reserved
[repayment capacity](repayment-plan.md). Trends surface on the [maintenance dashboard](../dashboards.md).
