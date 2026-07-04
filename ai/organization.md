# AI Engineering - Organization

## Reporting

The [CTO](../company/roles.md) owns AI standards and infrastructure; the [Chief Scientist](../company/roles.md) owns scientific validation and research.

```
CTO / Chief Scientist
|-- AI Architecture      - models, serving, training approach
|-- Applied AI (LLM/NLP) - prompts, RAG, agents, tool use
|-- ML / Vision / RL     - task-specific models
`-- AI Evaluation        - accuracy, safety, cost, drift
```

## Interfaces

| Works with | On |
|---|---|
| [Engineering](../engineering/README.md) | Integration, serving, APIs |
| [Data](../data/README.md) | Datasets, pipelines, labeling, grounding |
| [Security](../security/README.md) | Adversarial testing, leakage, model misuse |
| [Post-launch](../post-launch/README.md) | Drift, cost, and quality monitoring |
| [Product](../product/README.md) | Which problems AI should and should not solve |

## Where this plugs into the kernel

Work is decomposed and routed by the [coordinator](../orchestration/coordinator.md), reviewed at the
[quality gates](quality-gates.md), and its lasting knowledge persists to
[memory](../memory/README.md). Major decisions require cross-functional review before
[CEO Agent](../orchestration/ceo-agent.md) approval.
