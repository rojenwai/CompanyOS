# Security Agents

The AI agents for the [security department](../../../handbook/departments/security/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Compliance & Privacy Agent](compliance-privacy-agent.md) | Keep the company compliant and customer data protected by design. |
| [Penetration Testing Agent](penetration-testing-agent.md) | Find exploitable weaknesses before attackers do. |
| [Security Architect Agent](security-architect-agent.md) | Threat-model systems and design controls so weaknesses are prevented by design. |
| [Vulnerability Management Agent](vulnerability-management-agent.md) | Continuously find, triage, and drive remediation of vulnerabilities across the stack. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent security <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
