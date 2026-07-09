# Investor Relations Agents

The AI agents for the [investor-relations department](../../../handbook/departments/investor-relations/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Board Governance Agent](board-governance-agent.md) | Run clean board process - well-prepared meetings, accurate minutes, proper resolutions. |
| [Cap Table Agent](cap-table-agent.md) | Keep ownership records accurate and model the impact of financing and equity events. |
| [Investor Reporting Agent](investor-reporting-agent.md) | Produce accurate, consistent investor updates that reconcile to finance. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent investor-relations <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
