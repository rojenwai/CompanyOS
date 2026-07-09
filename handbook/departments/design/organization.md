# Design - Organization

## Reporting

The [Chief Designer](../../company/roles.md) owns design systems, accessibility, interaction, usability,
and visual language. Three functions report in:

```
Chief Designer
├── UX Research      - behavior, needs, mental models, accessibility findings
├── UX / Product Design - flows, information architecture, wireframes, prototypes
└── UI / Visual Design  - layout, type, color, iconography, components, themes
```

## Interfaces

| Works with | On |
|---|---|
| [Product](../product/README.md) | Problems, requirements, prioritization, launch |
| [Engineering](../engineering/README.md) | Implementation feasibility, component handoff, design tokens |
| [Research](../research/README.md) | Shared user research, market signals |
| [AI](../ai-engineering/README.md) | Designing AI interactions (streaming, uncertainty, corrections) |
| [Post-launch](../post-launch/README.md) | Usability issues surfaced in support and analytics |

## Where design plugs into the kernel

Design work is decomposed and routed by the [coordinator](../../../ai/orchestration/coordinator.md); design
reviews are a [quality gate](quality-gates.md) before build; findings persist in
[research memory](../../../ai/memory/research-memory.md).
