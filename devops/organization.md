# DevOps - Organization

## Reporting

The [CTO](../company/roles.md) owns infrastructure and delivery tooling; reliability is shared with [post-launch](../post-launch/README.md).

```
CTO
|-- CI/CD & Release  - pipelines, release engineering
|-- Platform / Infra - IaC, environments, networking
`-- Reliability (SRE) - SLOs, capacity, incident tooling
```

## Interfaces

| Works with | On |
|---|---|
| [Engineering](../engineering/README.md) | Pipelines, environments, deploys |
| [Post-launch](../post-launch/README.md) | Reliability, monitoring, rollback, incidents |
| [Security](../security/README.md) | Hardening, secrets, access, scanning in CI |
| [AI](../ai/README.md) / [Data](../data/README.md) | Model and data pipeline infrastructure |

## Where this plugs into the kernel

Work is decomposed and routed by the [coordinator](../orchestration/coordinator.md), reviewed at the
[quality gates](quality-gates.md), and its lasting knowledge persists to
[memory](../memory/README.md). Major decisions require cross-functional review before
[CEO Agent](../orchestration/ceo-agent.md) approval.
