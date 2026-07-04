# Data - Organization

## Reporting

The [CTO](../company/roles.md) owns data infrastructure; privacy is shared with the [CSO](../company/roles.md) and [CLO](../company/roles.md).

```
CTO
|-- Data Engineering  - pipelines, warehouse, quality
|-- Analytics Engineering - modeling, metrics layer
`-- Analytics / DS    - insight, experimentation, models
```

## Interfaces

| Works with | On |
|---|---|
| [AI](../ai/README.md) | Datasets, features, grounding sources |
| [Product](../product/analytics.md) | Product analytics and experiments |
| [All departments](../company/structure.md) | Metrics and dashboards |
| [Security](../security/README.md) / [Legal](../legal/README.md) | Privacy, governance, retention |

## Where this plugs into the kernel

Work is decomposed and routed by the [coordinator](../orchestration/coordinator.md), reviewed at the
[quality gates](quality-gates.md), and its lasting knowledge persists to
[memory](../memory/README.md). Major decisions require cross-functional review before
[CEO Agent](../orchestration/ceo-agent.md) approval.
