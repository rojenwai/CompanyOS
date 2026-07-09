# Task Routing

How the [Coordinator](coordinator.md) maps a subtask to the agent best suited to execute it.

## Routing signals

1. **Domain** — which [division](../agents/README.md) owns this kind of work.
2. **Capability** — which agent's [spec](../agents/agent-template.md) lists the required responsibilities/tools.
3. **Dependencies** — inputs must be ready (from the [task decomposer](task-decomposer.md) graph).
4. **Load & priority** — balance utilization against the critical path.
5. **Risk** — high-risk work is routed with mandatory review/approval attached.

## Routing table (excerpt)

| Subtask type | Routed to |
|---|---|
| Architecture / service boundaries | [Software Architect](../agents/engineering/software-architect.md) |
| API design | [API Architect](../agents/engineering/api-architect.md) |
| Feature implementation (server) | [Backend Engineer](../agents/engineering/backend-engineer.md) |
| Feature implementation (UI) | [Frontend Engineer](../agents/engineering/frontend-engineer.md) |
| Test authoring | [QA Engineer](../agents/engineering/qa-engineer.md) |
| Requirement / story definition | [Product Manager](../agents/product/product-manager.md) |
| Prioritization | [Feature Prioritization Agent](../agents/product/feature-prioritization-agent.md) |
| Production issue | [post-launch agents](../agents/post-launch/) |

## Fallbacks

If no agent matches, the Coordinator escalates to the [CEO Agent](ceo-agent.md) to either define a new
agent (from the [template](../agents/agent-template.md)) or reshape the plan.
