# Marketing Agents

The AI agents for the [marketing department](../../../handbook/departments/marketing/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Brand & Communications Agent](brand-communications-agent.md) | Keep positioning sharp and the company's voice consistent and trusted across channels. |
| [Content Marketing Agent](content-marketing-agent.md) | Build an organic content engine that attracts and educates the right customers. |
| [Growth Marketing Agent](growth-marketing-agent.md) | Find and scale efficient acquisition channels through disciplined experimentation. |
| [SEO Agent](seo-agent.md) | Grow qualified organic traffic through technical and content SEO. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent marketing <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
