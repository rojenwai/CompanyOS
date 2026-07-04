# DevOps - Agents

The DevOps agents, each written from the [agent template](../agents/agent-template.md) and living
in [agents/devops/](../agents/devops/).

| Agent | Mission (one line) |
|---|---|
| [CI/CD Engineer Agent](../agents/devops/cicd-engineer-agent.md) | Build and maintain the automated pipeline from commit to production. |
| [Platform Engineer Agent](../agents/devops/platform-engineer-agent.md) | Provision and manage reproducible infrastructure as code. |
| [Site Reliability Agent](../agents/devops/site-reliability-agent.md) | Keep production reliable within its SLOs and error budgets. |
| [Release Engineer Agent](../agents/devops/release-engineer-agent.md) | Orchestrate safe, progressive releases and clean rollbacks. |

All agent output is reviewed per [review-process.md](review-process.md); major decisions escalate to the
[CEO Agent](../orchestration/ceo-agent.md).
