# DevOps - Decision Frameworks

How decisions are made here. All decisions follow the company
[decision framework](../governance/decision-framework.md); these are the department-specific ones.

- **Rollback vs. fix-forward** - Roll back first to restore service; fix forward only when rollback is riskier.
- **Deployment strategy** - Canary/blue-green for risky changes; rolling for routine ones.
- **Buy vs. self-host infrastructure** - Prefer managed services unless cost or control clearly justifies self-hosting.

Reversible decisions are made fast and revisited; irreversible ones require review and are recorded in
[decision memory](../memory/decision-memory.md).
