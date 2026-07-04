# Investor Relations - Organization

## Reporting

The [CEO](../company/roles.md) (relationships, narrative) and [CFO](../company/roles.md) (numbers, cap table).

```
CEO / CFO
|-- Investor Reporting - updates, metrics, data room
|-- Board & Governance - meetings, minutes, resolutions
`-- Cap Table & Compliance - ownership, filings
```

## Interfaces

| Works with | On |
|---|---|
| [Finance](../finance/README.md) | Metrics, financials, cap table |
| [Strategy](../strategy/README.md) | Narrative, milestones, fundraising |
| [Legal](../legal/README.md) | Governance, filings, compliance |
| Board & investors | Reporting, engagement, decisions |

## Where this plugs into the kernel

Work is decomposed and routed by the [coordinator](../orchestration/coordinator.md), reviewed at the
[quality gates](quality-gates.md), and its lasting knowledge persists to
[memory](../memory/README.md). Major decisions require cross-functional review before
[CEO Agent](../orchestration/ceo-agent.md) approval.
