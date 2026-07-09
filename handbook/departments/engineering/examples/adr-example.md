# ADR-0007 — Use PostgreSQL as the primary datastore

**Status:** Accepted · **Date:** 2026-03-14 · **Deciders:** Software Architect, Database Engineer, CTO

## Context

The service needs a transactional store for orders and payments with strong consistency, relational
integrity, and mature operational tooling. Expected scale is moderate (low millions of rows,
< 2k writes/sec) for the next 18 months. The team has strong SQL experience.

## Decision

We will use **PostgreSQL** as the primary datastore, accessed through a thin repository layer per the
[module rules](../standards.md).

## Consequences

- **Positive:** ACID transactions; rich indexing; JSONB for semi-structured data; excellent tooling
  and backup/restore; large hiring pool.
- **Negative:** We accept vertical-scaling limits for now; horizontal sharding is deferred and will
  require a future ADR if write volume 10×'s.
- **Follow-ups:** Define migration tooling; set up read replicas ([database standards](../database-standards.md));
  add the datastore to the [reliability dashboard](../dashboards.md).

## Alternatives considered

- **MongoDB** — rejected: relational integrity for orders/payments is a core requirement.
- **DynamoDB** — rejected: access patterns not yet stable enough for a single-table design; team
  SQL expertise favors Postgres.
