# Bug Management

The lifecycle of a bug, from report to verified fix. Owned by the
[Bug Triage Agent](../agents/post-launch/bug-triage-agent.md).

## Lifecycle

```
Reported → Triaged → Prioritized → Assigned → Fixed → Verified → Closed
                └── (if not reproducible) → Needs Info / Closed
```

## Triage

Every bug is classified by:

- **Severity** — impact if it occurs (critical → trivial).
- **Priority** — how soon to fix, given severity × frequency × reach.
- **Type** — regression, functional, performance, security, data.

Security bugs route to the [Security Patch Agent](../agents/post-launch/security-patch-agent.md);
regressions to the [Regression Agent](../agents/post-launch/regression-agent.md).

## Rules

- Every fix ships with a test that reproduces the bug (prevents [regression](../agents/post-launch/regression-agent.md)).
- Critical/customer-impacting bugs may become [incidents](incident-response.md).
- Recurring bug clusters are flagged as [technical debt](technical-debt/policy.md) or product signals
  ([feedback](customer-feedback.md)).
