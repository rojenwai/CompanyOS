# Retrieval

How memory and knowledge are searched and returned. Backs both the [Memory Manager](../orchestration/memory-manager.md)
and [Knowledge Manager](../orchestration/knowledge-manager.md).

## Retrieval contract

Every retrieval returns, for each result:

- **source** — where it came from
- **confidence** — how sure the system is
- **timestamp** — when it was created/last verified
- **relevance score** — how well it matches the query

## Ranking

Results are ranked by relevance, then recency, then source reliability. Low-confidence or stale
results are flagged, not silently dropped.

## Tagging

Everything written to memory is tagged (project, domain, type, entities) so it is retrievable later.
Untagged memory is effectively lost — tagging is part of every [validated write](retention-and-versioning.md).

## When nothing authoritative is found

Retrieval returns "no reliable source" rather than a low-confidence guess, so the calling agent can
apply [failure handling](../../handbook/governance/failure-handling.md).
