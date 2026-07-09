# Legal Agents

The AI agents for the [legal department](../../../handbook/departments/legal/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Compliance Agent](compliance-agent.md) | Map regulatory obligations and keep the company on the right side of them. |
| [Contract Agent](contract-agent.md) | Draft, review, and flag risk in contracts so the business can sign with confidence. |
| [IP & Patent Agent](ip-patent-agent.md) | Protect the company's intellectual property and keep its use of others' IP clean. |
| [Privacy & Terms Agent](privacy-terms-agent.md) | Keep the company's terms honest and its data practices privacy-respecting. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent legal <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
