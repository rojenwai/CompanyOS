# Product AI Agents

Full specs in [agents/product/](../agents/product/).

| Agent | Mission (one line) | Spec |
|---|---|---|
| Product Manager | Turn validated problems into prioritized, well-defined product work | [product-manager.md](../agents/product/product-manager.md) |
| Feature Prioritization Agent | Rank features by evidence, not opinion | [feature-prioritization-agent.md](../agents/product/feature-prioritization-agent.md) |
| Customer Journey Agent | Map the full customer journey to find friction | [customer-journey-agent.md](../agents/product/customer-journey-agent.md) |
| User Story Agent | Produce testable stories with acceptance criteria | [user-story-agent.md](../agents/product/user-story-agent.md) |
| MVP Planning Agent | Define the smallest product that solves the core problem | [mvp-planning-agent.md](../agents/product/mvp-planning-agent.md) |

## Collaboration map

Discovery ([Customer Journey](../agents/product/customer-journey-agent.md)) → definition
([Product Manager](../agents/product/product-manager.md) + [User Story](../agents/product/user-story-agent.md)) →
prioritization ([Feature Prioritization](../agents/product/feature-prioritization-agent.md)) →
scope ([MVP Planning](../agents/product/mvp-planning-agent.md)) → handoff to
[engineering](../engineering/README.md).
