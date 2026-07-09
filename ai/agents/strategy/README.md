# Strategy Agents

The AI agents for the [strategy department](../../../handbook/departments/strategy/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Business Model & Pricing Agent](business-model-pricing-agent.md) | Design how the company creates and captures value, and price it defensibly. |
| [Business Strategy Agent](business-strategy-agent.md) | Recommend the company's strategic moves - what to pursue, when, and why it is defensible. |
| [Fundraising Agent](fundraising-agent.md) | Prepare the company to raise capital on the best terms - or chart a path without it. |
| [Go-To-Market Agent](go-to-market-agent.md) | Define how the product reaches and wins its market. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent strategy <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
