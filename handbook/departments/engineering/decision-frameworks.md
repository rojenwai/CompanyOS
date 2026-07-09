# Engineering Decision Frameworks

How engineering decisions are made consistently. Extends the company
[decision framework](../../governance/decision-framework.md).

## Build vs. buy vs. adopt

Score each option on: fit · maintenance burden · security · licensing · total cost · lock-in.
Prefer the simplest option that meets requirements ([KISS](principles.md)). Record the outcome as an
[ADR](../../templates/documents/adr.md).

## Architecture decisions

Significant architecture choices are captured as [ADRs](../../templates/documents/adr.md) and stored in
[architecture memory](../../../ai/memory/architecture-memory.md). They are immutable once accepted — superseded
by a new ADR, never silently rewritten.

## Reversible vs. irreversible

- **Reversible** (feature flag, internal refactor): decide fast at the implementer level.
- **Irreversible** (public API shape, data migration, framework choice): require architect review and
  [approval](../../../ai/orchestration/approval-engine.md).
