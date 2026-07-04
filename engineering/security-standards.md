# Security Standards

Baseline security requirements for all engineering work. Enforced by the
[Security Reviewer](../orchestration/security-reviewer.md) using the
[security review template](../templates/documents/security-review.md).

## Non-negotiables

- No plaintext passwords.
- No secrets in Git.
- Input validation everywhere.
- Parameterized queries (no string-built SQL).
- Output encoding (prevent XSS).
- Secure headers.
- Dependency scanning.
- Encryption at rest and in transit.
- Regular security audits.

## Security review checklist

Authentication · Authorization · Encryption · Secrets management · SQL injection · XSS · CSRF ·
Rate limiting · Dependency audit · OWASP Top 10 · Logging (without sensitive data) · Compliance.

## Ownership

The [Chief Security Officer](../company/roles.md) owns these standards; a Security Reviewer **Block**
requires explicit human override (see the [approval engine](../orchestration/approval-engine.md)).
Production security events trigger the [security-breach playbook](../post-launch/playbooks/).
