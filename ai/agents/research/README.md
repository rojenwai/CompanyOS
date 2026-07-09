# Research Agents

The AI agents for the [research department](../../../handbook/departments/research/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Competitor Analysis Agent](competitor-analysis-agent.md) | Map the competitive landscape and find defensible positioning gaps. |
| [Market Research Agent](market-research-agent.md) | Size the market and quantify demand for a validated problem. |
| [Opportunity Ranking Agent](opportunity-ranking-agent.md) | Score and rank opportunities so the company pursues the highest-value bets first. |
| [Problem Discovery Agent](problem-discovery-agent.md) | Surface and validate significant, underserved problems worth building a company around. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent research <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
