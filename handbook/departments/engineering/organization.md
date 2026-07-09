# Organization

Engineering reports to the [CTO](../../company/roles.md) and is executed by the
[engineering agents](agents.md), coordinated by the [orchestration kernel](../../../ai/orchestration/README.md).

## Structure

```
CTO
└── Software Architect (sets architecture, boundaries, standards)
    ├── Backend · Frontend · Mobile · Database · Cloud · API Architect
    ├── QA Engineer · Performance Engineer
    └── Refactoring Agent
```

## Interfaces

| Interfaces with | For | Via |
|---|---|---|
| [product/](../product/) | requirements, priorities | PRDs, user stories |
| [design/](../design/) | UI/UX specs | design system, prototypes |
| [ai/](../ai-engineering/) | model integration | AI engineering standards |
| [post-launch/](../post-launch/) | operability, maintenance | monitoring, on-call handoff |
| [orchestration/](../../../ai/orchestration/) | task routing, review, approval | Coordinator + reviewers |
