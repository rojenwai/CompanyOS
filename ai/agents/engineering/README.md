# Engineering Agents

The AI agents for the [engineering department](../../../handbook/departments/engineering/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [# API Architect Agent](api-architect.md) |  |
| [# Backend Engineer Agent](backend-engineer.md) |  |
| [# Cloud Engineer Agent](cloud-engineer.md) |  |
| [# Database Engineer Agent](database-engineer.md) |  |
| [# Frontend Engineer Agent](frontend-engineer.md) |  |
| [# Mobile Engineer Agent](mobile-engineer.md) |  |
| [# Performance Engineer Agent](performance-engineer.md) |  |
| [# QA Engineer Agent](qa-engineer.md) |  |
| [# Refactoring Agent](refactoring-agent.md) |  |
| [# Software Architect Agent](software-architect.md) |  |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent engineering <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
