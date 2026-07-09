# Engineering AI Agents

The AI agents that execute engineering work. Full specs live in [agents/engineering/](../../../ai/agents/engineering/).
Agents never work independently on major decisions — the [Reviewer](../../../ai/orchestration/reviewer.md),
[QA Reviewer](../../../ai/orchestration/qa-reviewer.md), and [Security Reviewer](../../../ai/orchestration/security-reviewer.md)
gate their output.

| Agent | Mission (one line) | Spec |
|---|---|---|
| Software Architect | Define architecture that is scalable, secure, and maintainable | [software-architect.md](../../../ai/agents/engineering/software-architect.md) |
| Backend Engineer | Build reliable server-side services and data access | [backend-engineer.md](../../../ai/agents/engineering/backend-engineer.md) |
| Frontend Engineer | Build fast, accessible user interfaces | [frontend-engineer.md](../../../ai/agents/engineering/frontend-engineer.md) |
| Mobile Engineer | Build performant native/cross-platform apps | [mobile-engineer.md](../../../ai/agents/engineering/mobile-engineer.md) |
| Database Engineer | Design correct, performant, durable data stores | [database-engineer.md](../../../ai/agents/engineering/database-engineer.md) |
| Cloud Engineer | Provide scalable, secure infrastructure | [cloud-engineer.md](../../../ai/agents/engineering/cloud-engineer.md) |
| API Architect | Design clear, versioned, documented APIs | [api-architect.md](../../../ai/agents/engineering/api-architect.md) |
| QA Engineer | Ensure adequate, meaningful test coverage | [qa-engineer.md](../../../ai/agents/engineering/qa-engineer.md) |
| Performance Engineer | Optimize based on evidence | [performance-engineer.md](../../../ai/agents/engineering/performance-engineer.md) |
| Refactoring Agent | Improve maintainability without changing behavior | [refactoring-agent.md](../../../ai/agents/engineering/refactoring-agent.md) |

## Collaboration map

Architect sets boundaries → implementers build within them → QA/Security/Docs reviewers gate →
[Execution Engine](../../../ai/orchestration/execution-engine.md) ships → [post-launch](../post-launch/README.md) maintains.
