# Testing Standards

Every feature requires: unit tests · integration tests · edge-case tests · failure tests · regression tests.

Critical systems additionally require: load tests · stress tests · security tests.

## Testing pyramid

```
        e2e / UI
      integration
   unit (the broad base)
```

Plus, across the pyramid: performance, load, stress, security, accessibility, and regression tests
(see the [SDLC testing phase](../../workflows/sdlc.md)).

## Coverage targets

| Scope | Target |
|---|---|
| Overall | 80% |
| Core business logic | 95% |
| Mission-critical | 100% |

## Rules

- Refactoring without tests is prohibited (see [refactoring-policy.md](refactoring-policy.md)).
- Every acceptance criterion maps to at least one test.
- Tests are reviewed by the [QA Reviewer](../../../ai/orchestration/qa-reviewer.md) as a [quality gate](quality-gates.md).
- Coverage is a floor, not a goal — meaningful assertions matter more than the percentage.
