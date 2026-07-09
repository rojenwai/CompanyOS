# Ai Engineering Agents

The AI agents for the [ai-engineering department](../../../handbook/departments/ai-engineering/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [AI Architect Agent](ai-architect-agent.md) | Choose the models, serving, and grounding architecture for each AI feature. |
| [AI Evaluation Agent](ai-evaluation-agent.md) | Prove AI quality, safety, and cost before anything ships, and gate releases. |
| [LLM Engineer Agent](llm-engineer-agent.md) | Build grounded, versioned LLM features - prompts, RAG, agents, and tool use. |
| [ML Engineer Agent](ml-engineer-agent.md) | Train, evaluate, and deploy task-specific models. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent ai-engineering <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
