# Security - Quality Gates

Work does not progress until the relevant gate passes. These implement the company
[quality gates](../../governance/quality-gates.md).

| Gate | Must pass |
|---|---|
| Design gate | Threat model exists; critical controls specified |
| Code gate | No secrets; input/output handled; SAST clean of highs |
| Dependency gate | No known-critical vulnerabilities |
| Release gate | Security Reviewer sign-off; no open criticals |
