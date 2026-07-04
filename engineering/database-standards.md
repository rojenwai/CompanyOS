# Database Standards

Normalize until performance requires denormalization. Owned by the
[Database Engineer](../agents/engineering/database-engineer.md).

## Every table has

Primary key · indexes · constraints · foreign keys · migration · rollback · audit strategy.

## Rules

- Schema changes ship as reversible migrations.
- Index for the queries you actually run; measure before denormalizing.
- Enforce integrity with constraints, not application code alone.
- Define a data-retention policy per table (aligns with [privacy](../memory/retention-and-versioning.md)).
- Back up and test restores; ongoing health is owned by the [Database Maintenance Agent](../agents/post-launch/database-maintenance-agent.md).
