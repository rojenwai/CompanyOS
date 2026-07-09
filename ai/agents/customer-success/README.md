# Customer Success Agents

The AI agents for the [customer-success department](../../../handbook/departments/customer-success/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Customer Health Agent](customer-health-agent.md) | Score account health and predict churn early enough to prevent it. |
| [Customer Onboarding Agent](customer-onboarding-agent.md) | Get every new customer to first value as fast as possible. |
| [Renewal & Expansion Agent](renewal-expansion-agent.md) | Secure renewals on delivered value and grow accounts where more value exists. |
| [Support Agent](support-agent.md) | Resolve customer issues quickly and accurately, and turn them into product signal. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent customer-success <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
