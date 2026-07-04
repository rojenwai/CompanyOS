# Security - Standards

Testable standards, not aspirations. These extend the company-wide
[standards](../standards/README.md).

1. No secrets in code or logs - ever; secrets live in a vault.
2. All input validated; all output encoded; parameterized queries only.
3. Encryption in transit and at rest for sensitive data.
4. Least-privilege access for every human and agent.
5. Every dependency scanned; no known-critical vulnerabilities in production.
6. Every production system emits security-relevant logs (no secrets/PII).
