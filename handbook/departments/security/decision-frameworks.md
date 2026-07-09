# Security - Decision Frameworks

How decisions are made here. All decisions follow the company
[decision framework](../../governance/decision-framework.md); these are the department-specific ones.

- **Block vs. allow a release** - Block on any unresolved critical or high finding; the block is not silently overridable.
- **Patch now vs. schedule** - Patch immediately for exploited or critical CVEs; schedule lower-severity within SLA.
- **Risk acceptance** - Residual risk may be accepted only by the CSO, documented and time-boxed.

Reversible decisions are made fast and revisited; irreversible ones require review and are recorded in
[decision memory](../../../ai/memory/decision-memory.md).
