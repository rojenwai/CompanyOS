# Finance - Organization

## Reporting

The [CFO](../../company/roles.md) owns pricing, forecasts, runway, budgeting, fundraising, and financial models.

```
CFO
|-- FP&A            - forecasting, budgeting, unit economics
|-- Accounting      - bookkeeping, close, audit
`-- Revenue & Billing - pricing ops, invoicing, collections
```

## Interfaces

| Works with | On |
|---|---|
| [Strategy](../strategy/README.md) | Business model, pricing, unit economics, fundraising |
| [Investor Relations](../investor-relations/README.md) | Reporting, board and investor updates |
| [DevOps](../devops/README.md) / [AI](../ai-engineering/README.md) | Infrastructure and model cost |
| [HR](../hr/README.md) | Headcount planning and payroll |

## Where this plugs into the kernel

Work is decomposed and routed by the [coordinator](../../../ai/orchestration/coordinator.md), reviewed at the
[quality gates](quality-gates.md), and its lasting knowledge persists to
[memory](../../../ai/memory/README.md). Major decisions require cross-functional review before
[CEO Agent](../../../ai/orchestration/ceo-agent.md) approval.
