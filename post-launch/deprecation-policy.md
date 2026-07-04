# Deprecation Policy

How a feature or API is retired without breaking customers. Deprecation is a managed process, not a
silent removal.

## Process

1. **Decide** — via [product evolution](product-evolution.md); record in [decision memory](../memory/decision-memory.md).
2. **Announce** — communicate the timeline well in advance, with reasons.
3. **Provide a path** — migration guide and, where possible, an automated migration.
4. **Support window** — keep the deprecated capability working through a defined window ([versioning](versioning.md)).
5. **Remove** — only after the window and after usage has dropped to the agreed threshold.

## Rules

- Never remove a published [API](../engineering/api-standards.md) capability without a version bump and migration path.
- The [API Compatibility Agent](../agents/post-launch/api-compatibility-agent.md) monitors for accidental breaking changes.
- Retiring an entire product follows [end-of-life](end-of-life.md).
