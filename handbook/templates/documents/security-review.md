# Security Review — <system / change>

**Reviewer:** <name/agent> · **Date:** <date> · **Verdict:** Approved / Approved with conditions / Blocked

## Scope

What is being reviewed and what is explicitly out of scope.

## Threat model

- **Assets:** <what we protect>
- **Threat actors:** <who>
- **Entry points / attack surface:** <where>

## Checklist (OWASP-aligned)

- [ ] Authentication
- [ ] Authorization
- [ ] Input validation / injection (SQL, command, etc.)
- [ ] Output encoding (XSS)
- [ ] CSRF protection
- [ ] Secrets management (no secrets in code/logs)
- [ ] Encryption in transit and at rest
- [ ] Rate limiting / abuse protection
- [ ] Dependency vulnerabilities audited
- [ ] Logging without sensitive data
- [ ] Compliance requirements met

## Findings

| Severity | Finding | Recommendation | Status |
|---|---|---|---|
| Critical/High/Med/Low | <finding> | <fix> | <open/fixed> |

## Conditions for approval

- <what must be fixed before ship>
