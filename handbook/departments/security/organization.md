# Security - Organization

## Reporting

The [Chief Security Officer](../../company/roles.md) owns cybersecurity, privacy, encryption, compliance, penetration testing, and threat modeling.

```
Chief Security Officer
|-- Security Architecture   - secure design, threat modeling
|-- Offensive Security      - pen testing, red team
|-- Vulnerability & Response - scanning, patching, incidents
`-- Compliance & Privacy    - frameworks, audits, data protection
```

## Interfaces

| Works with | On |
|---|---|
| [Engineering](../engineering/README.md) | Secure coding, reviews, secret management |
| [AI](../ai-engineering/ai-security.md) | Prompt injection, data leakage, model misuse |
| [Post-launch](../post-launch/README.md) | Incident response, patching, monitoring |
| [Legal](../legal/README.md) | Compliance frameworks, breach obligations, privacy |
| [DevOps](../devops/README.md) | Infrastructure hardening, secrets, access |

## Where this plugs into the kernel

Work is decomposed and routed by the [coordinator](../../../ai/orchestration/coordinator.md), reviewed at the
[quality gates](quality-gates.md), and its lasting knowledge persists to
[memory](../../../ai/memory/README.md). Major decisions require cross-functional review before
[CEO Agent](../../../ai/orchestration/ceo-agent.md) approval.
