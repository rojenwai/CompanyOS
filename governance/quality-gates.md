# Quality Gates

Nothing progresses unless it satisfies every gate. Gates are binary.

- ✓ Requirements Complete
- ✓ Architecture Approved
- ✓ Security Reviewed
- ✓ Tests Passing
- ✓ Documentation Written
- ✓ Performance Verified
- ✓ UX Approved
- ✓ Product Approved
- ✓ CEO Approved

---

## How gates are applied

Each [department](../STRUCTURE.md#standard-department-structure) defines its own `quality-gates.md`
specializing these company-wide gates for its work. The [SDLC](../workflows/sdlc.md) maps gates to
lifecycle phases, and the [orchestration execution engine](../orchestration/execution-engine.md)
refuses to advance work that has not cleared the relevant gate.

Related: [definition-of-done.md](definition-of-done.md).
