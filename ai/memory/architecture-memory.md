# Architecture Memory

**Scope:** system designs and their rationale, long-lived.

## What's stored
Architecture diagrams · technology choices · service boundaries · trade-offs — captured primarily as [ADRs](../../handbook/templates/documents/adr.md).

## Lifetime
Permanent and append-only: decisions are superseded, never silently rewritten.

## Writers / readers
Written by architect agents; read before any change that touches system structure to avoid re-litigating settled trade-offs.

## Link
Project-specific architecture lives in [project-memory.md](project-memory.md); the *why* lives here.
