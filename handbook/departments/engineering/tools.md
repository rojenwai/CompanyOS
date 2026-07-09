# Engineering Tools

The tooling engineering relies on. Agents may only use tools listed in their
[spec](../../../ai/agents/agent-template.md).

| Category | Purpose | Notes |
|---|---|---|
| Version control | Source of truth, review | Protected `main`, PR-based ([workflows](workflows.md)) |
| CI/CD | Build, test, scan, deploy | Gates merges and releases ([automation](automation.md)) |
| Test runners + coverage | Enforce [testing standards](testing-standards.md) | Coverage gate in CI |
| Static analysis / linters | Enforce [coding standards](standards.md) | Blocking in CI |
| Dependency / security scanners | Enforce [security standards](security-standards.md) | Feeds [Security Patch Agent](../../../ai/agents/post-launch/security-patch-agent.md) |
| IaC | Reproducible infrastructure | Owned by Cloud Engineer |
| Observability | Metrics, logs, traces | See [observability](../post-launch/observability.md) |
| API / schema tooling | OpenAPI, contract tests | Owned by [API Architect](../../../ai/agents/engineering/api-architect.md) |

Tool choices are decided via [decision-frameworks.md](decision-frameworks.md) (build vs buy) and
recorded as [ADRs](../../templates/documents/adr.md).
