# Refactoring Policy

Refactor when: duplicate logic appears · complexity grows · performance degrades · testing becomes
difficult · architecture becomes unclear.

## The one hard rule

**Refactoring without tests is prohibited.** Establish a passing test suite that pins current
behavior *before* changing structure, so a refactor is provably behavior-preserving.

## Process

1. Confirm tests cover the area (add characterization tests if not).
2. Refactor in small, reviewable steps.
3. Keep the suite green at each step.
4. Review via the standard [review process](review-process.md).

Owned by the [Refactoring Agent](../agents/engineering/refactoring-agent.md); triggered by debt
detected via the [technical debt policy](technical-debt-policy.md).
