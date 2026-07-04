# Engineering Quality Gates

Specializes the company [quality gates](../governance/quality-gates.md) for code. Work does not
advance until every criterion for its phase is met.

## Definition of Ready (before work starts)

A task is ready when it contains: Requirements · Acceptance Criteria · Dependencies · Design ·
Priority · Estimate. Full detail in [definition-of-ready.md](definition-of-ready.md).

## Definition of Done (before it ships)

- Code complete
- Tests pass
- Documentation updated
- Reviewed
- Security approved
- Performance verified
- Merged
- Deployed

This mirrors the company [Definition of Done](../governance/definition-of-done.md): **ready for
production, not merely implemented.**

## Release gate

Before release: requirements complete · tests passing · docs updated · [security review](security-standards.md)
approved · performance verified · product approved · rollback prepared. See the
[release checklist](../templates/documents/release-checklist.md).
