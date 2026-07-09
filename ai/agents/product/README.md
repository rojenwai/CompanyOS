# Product Agents

The AI agents for the [product department](../../../handbook/departments/product/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [# Customer Journey Agent](customer-journey-agent.md) |  |
| [# Feature Prioritization Agent](feature-prioritization-agent.md) |  |
| [# MVP Planning Agent](mvp-planning-agent.md) |  |
| [# Product Manager Agent](product-manager.md) |  |
| [# User Story Agent](user-story-agent.md) |  |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent product <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
