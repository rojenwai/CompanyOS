# Documentation Memory

**Scope:** the canonical index of all documentation, long-lived.

## What's stored
Pointers to the authoritative version of every document (READMEs, guides, API docs, architecture), with ownership and freshness.

## Lifetime
Permanent; drift is actively detected.

## Writers / readers
Maintained by the [Documentation Reviewer](../orchestration/documentation-reviewer.md) and the Documentation Maintenance agent ([post-launch](../post-launch/README.md)); read to find the current source of truth.

## Rule
One canonical version per document; duplicates are reconciled, not multiplied.
