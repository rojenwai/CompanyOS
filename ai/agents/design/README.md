# Design Agents

The AI agents for the [design department](../../../handbook/departments/design/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Accessibility Agent](accessibility-agent.md) | Audit every surface against WCAG and drive remediation until it passes. |
| [Design System Agent](design-system-agent.md) | Maintain the components, tokens, and accessibility of the design system as one source of truth. |
| [Interaction Designer Agent](interaction-designer-agent.md) | Design flows, states, feedback, and motion so every interaction is clear and forgiving. |
| [UI Designer Agent](ui-designer-agent.md) | Produce accessible, on-system visual designs from requirements. |
| [UX Research Agent](ux-research-agent.md) | Study users and surface behavior, needs, and pain points as evidence for design decisions. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent design <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
