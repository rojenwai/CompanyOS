# Data Agents

The AI agents for the [data department](../../../handbook/departments/data/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Analytics Engineer Agent](analytics-engineer-agent.md) | Model raw data into a governed metrics layer that everyone can trust and reuse. |
| [Data Engineer Agent](data-engineer-agent.md) | Build reliable, reproducible pipelines that land trustworthy data in the warehouse. |
| [Data Governance Agent](data-governance-agent.md) | Keep data private, secure, well-cataloged, and correctly retained. |
| [Data Scientist Agent](data-scientist-agent.md) | Turn data into insight and predictive models that drive decisions. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent data <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
