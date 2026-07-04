# Strategy - Organization

## Reporting

Shared across the [CEO](../company/roles.md) (direction), [CFO](../company/roles.md) (economics, fundraising), and [CMO](../company/roles.md) (go-to-market).

```
CEO
|-- Business Strategy   - lifecycle, positioning, competitive strategy
|-- Finance / Economics - model, pricing, unit economics, fundraising (-> finance/)
`-- Go-To-Market        - channels, funnel, launch (-> marketing/, sales/)
```

## Interfaces

| Works with | On |
|---|---|
| [Research](../research/README.md) | Ranked opportunities, market sizing |
| [Product](../product/README.md) | Product definition, roadmap direction, PMF |
| [Finance](../finance/README.md) | Forecasts, runway, fundraising |
| [Marketing](../marketing/README.md) / [Sales](../sales/README.md) | GTM execution |

## Where this plugs into the kernel

Work is decomposed and routed by the [coordinator](../orchestration/coordinator.md), reviewed at the
[quality gates](quality-gates.md), and its lasting knowledge persists to
[memory](../memory/README.md). Major decisions require cross-functional review before
[CEO Agent](../orchestration/ceo-agent.md) approval.
