# Devops Agents

The AI agents for the [devops department](../../../handbook/departments/devops/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [CI/CD Engineer Agent](cicd-engineer-agent.md) | Build and maintain the automated pipeline from commit to production. |
| [Platform Engineer Agent](platform-engineer-agent.md) | Provision and manage reproducible infrastructure as code. |
| [Release Engineer Agent](release-engineer-agent.md) | Orchestrate safe, progressive releases and clean rollbacks. |
| [Site Reliability Agent](site-reliability-agent.md) | Keep production reliable within its SLOs and error budgets. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent devops <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
