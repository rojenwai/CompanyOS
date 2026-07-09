# Sales Agents

The AI agents for the [sales department](../../../handbook/departments/sales/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Account Executive Agent](account-executive-agent.md) | Run honest discovery-led deals from opportunity to close. |
| [Deal Desk Agent](deal-desk-agent.md) | Keep pricing, terms, and forecasting consistent and clean across deals. |
| [Prospecting Agent](prospecting-agent.md) | Identify and qualify the accounts most likely to be a great fit. |
| [Sales Engineer Agent](sales-engineer-agent.md) | Prove technical fit honestly so the right deals advance and the wrong ones don't stall later. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent sales <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
