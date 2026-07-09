# AI Engineering - Agents

The AI Engineering agents, each written from the [agent template](../../../ai/agents/agent-template.md) and living
in [agents/ai/](../../../ai/agents/ai-engineering/).

| Agent | Mission (one line) |
|---|---|
| [AI Architect Agent](../../../ai/agents/ai-engineering/ai-architect-agent.md) | Choose the models, serving, and grounding architecture for each AI feature. |
| [LLM Engineer Agent](../../../ai/agents/ai-engineering/llm-engineer-agent.md) | Build grounded, versioned LLM features - prompts, RAG, agents, and tool use. |
| [ML Engineer Agent](../../../ai/agents/ai-engineering/ml-engineer-agent.md) | Train, evaluate, and deploy task-specific models. |
| [AI Evaluation Agent](../../../ai/agents/ai-engineering/ai-evaluation-agent.md) | Prove AI quality, safety, and cost before anything ships, and gate releases. |

All agent output is reviewed per [review-process.md](review-process.md); major decisions escalate to the
[CEO Agent](../../../ai/orchestration/ceo-agent.md).
