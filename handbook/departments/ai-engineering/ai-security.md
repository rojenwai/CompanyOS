# AI Security

Protect AI systems against their specific threats. Complements the general
[security standards](../engineering/security-standards.md).

## Threats

- **Prompt injection** — malicious input hijacking instructions.
- **Data poisoning** — corrupting training/RAG sources.
- **Tool abuse** — coercing an agent to misuse a tool.
- **Unauthorized access** — reaching data/tools beyond scope.
- **Sensitive-data leakage** — exposing secrets or personal data.
- **Model misuse** — using the system for prohibited purposes.

## Defenses

- **Validate all external inputs** before they reach a model or tool.
- Constrain each agent to the tools in its [spec](../../../ai/agents/agent-template.md); least privilege.
- Never place secrets or personal data in prompts, logs, or [memory](../../../ai/memory/retention-and-versioning.md) that isn't access-controlled.
- Test with adversarial prompts and jailbreak attempts ([evaluation-and-testing.md](evaluation-and-testing.md)).
- Human-in-the-loop for high-risk actions ([approval engine](../../../ai/orchestration/approval-engine.md)).

Findings feed the [Security Reviewer](../../../ai/orchestration/security-reviewer.md) and, in production, the
[security-breach playbook](../post-launch/playbooks/security-breach.md).
