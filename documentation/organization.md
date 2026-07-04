# Documentation - Organization

## Reporting

The [COO](../company/roles.md) owns documentation as part of operations.

```
COO
|-- Product & API Docs - user-facing documentation
|-- Internal Knowledge - runbooks, processes, onboarding
`-- Information Arch.   - structure, search, standards
```

## Interfaces

| Works with | On |
|---|---|
| [Engineering](../engineering/documentation-requirements.md) | API refs, architecture, READMEs |
| [Product](../product/README.md) | Feature docs, guides, release notes |
| [Operations](../operations/README.md) | Internal processes, runbooks, onboarding |
| [Post-launch](../post-launch/README.md) | Drift detection, maintenance |

## Where this plugs into the kernel

Work is decomposed and routed by the [coordinator](../orchestration/coordinator.md), reviewed at the
[quality gates](quality-gates.md), and its lasting knowledge persists to
[memory](../memory/README.md). Major decisions require cross-functional review before
[CEO Agent](../orchestration/ceo-agent.md) approval.
