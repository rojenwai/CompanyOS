# Updates, Retention & Versioning

The rules for how memory changes over time. Memory is **never modified without validation**.

## Updates

- Writes go through the [Memory Manager](../orchestration/memory-manager.md), which validates before committing.
- Append-only stores ([decision](decision-memory.md), [architecture](architecture-memory.md)) are superseded, never overwritten.
- Conflicting writes are escalated, not silently merged.

## Promotion

Facts move up in scope only when validated: **session → project → company**. A transient session note
does not become company memory without explicit promotion and review.

## Retention

| Store | Retention |
|---|---|
| Session | Discarded at session end (unless promoted) |
| Project | Life of project, then archived at [EOL](../post-launch/end-of-life.md) |
| Company / Department / Knowledge | Permanent, versioned |
| User / Customer | Per privacy policy; user/customer-controlled; deletable on request |

## Versioning

Long-lived memory is versioned so any change is traceable and reversible. Version history supports
audits and lets the [Continuous Improvement Engine](../orchestration/continuous-improvement-engine.md)
measure whether a change actually helped.

## Privacy

User and customer memory follow data-protection law (GDPR etc.): access-controlled, never logged to
observability, and deletable on request.
