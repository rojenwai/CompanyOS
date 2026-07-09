# Documentation Agents

The AI agents for the [documentation department](../../../handbook/departments/documentation/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [API Documentation Agent](api-documentation-agent.md) | Keep API reference docs complete, accurate, and example-rich - generated from the source of truth. |
| [Knowledge Base Agent](knowledge-base-agent.md) | Keep internal knowledge - runbooks, processes, onboarding - findable, owned, and current. |
| [Technical Writer Agent](technical-writer-agent.md) | Produce clear, accurate, task-oriented documentation for every product capability. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent documentation <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
