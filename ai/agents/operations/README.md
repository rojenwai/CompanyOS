# Operations Agents

The AI agents for the [operations department](../../../handbook/departments/operations/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Knowledge Management Agent](knowledge-management-agent.md) | Keep the company's knowledge and assets findable, current, and owned. |
| [Process Optimization Agent](process-optimization-agent.md) | Design the lightest processes that reliably produce the outcome, and automate the routine. |
| [Project Management Agent](project-management-agent.md) | Keep initiatives planned, coordinated, and unblocked to on-time delivery. |
| [Vendor Management Agent](vendor-management-agent.md) | Get the right tools and services at the right price and terms, and keep them managed. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent operations <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
