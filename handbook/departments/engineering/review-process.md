# Review Process

Every change is reviewed before merge. Reviewers never assume the author is correct
([Reviewer](../../../ai/orchestration/reviewer.md)).

## Code review checklist

Correctness · Readability · Naming · Architecture · Performance · Security · Testing · Documentation ·
Error handling · Edge cases · Accessibility · Maintainability.

## Architecture review checklist

Scalable · Secure · Maintainable · Observable · Fault tolerant · Documented · Testable · Extensible.

## Reviewers

- Minimum **2** reviewers; **3** for critical infrastructure (see [workflows.md](workflows.md)).
- Security-sensitive changes require the [Security Reviewer](../../../ai/orchestration/security-reviewer.md).
- Test adequacy is checked by the [QA Reviewer](../../../ai/orchestration/qa-reviewer.md); docs by the [Documentation Reviewer](../../../ai/orchestration/documentation-reviewer.md).

## Outcomes

Approve · Approve with changes · Reject with reasons · Escalate. A rejected change returns to the
author via the [Coordinator](../../../ai/orchestration/coordinator.md).
