# Hr Agents

The AI agents for the [hr department](../../../handbook/departments/hr/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Culture Agent](culture-agent.md) | Keep the company's culture deliberate, healthy, and aligned to its principles. |
| [Onboarding Agent](onboarding-agent.md) | Get every new hire (and agent) productive and connected fast. |
| [Performance & Growth Agent](performance-growth-agent.md) | Help people grow through clear expectations, frequent feedback, and fair evaluation. |
| [Recruiting Agent](recruiting-agent.md) | Run a rigorous, fast, fair hiring process that raises the bar with every hire. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent hr <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
