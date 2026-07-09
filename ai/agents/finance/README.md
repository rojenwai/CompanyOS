# Finance Agents

The AI agents for the [finance department](../../../handbook/departments/finance/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Accounting Agent](accounting-agent.md) | Keep the books accurate, current, and audit-ready. |
| [Cost Optimization Agent](cost-optimization-agent.md) | Ensure the company gets maximum value per dollar spent, especially on infrastructure and AI. |
| [Financial Planning Agent](financial-planning-agent.md) | Maintain the forecast, budget, and runway so leadership always knows the financial picture. |
| [Revenue & Billing Agent](revenue-billing-agent.md) | Bill correctly, collect reliably, and recognize revenue properly. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent finance <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
