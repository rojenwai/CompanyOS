# Session Memory

**Scope:** the current conversation/task only. Ephemeral.

## What's stored
The working context of an in-flight task: the request, intermediate reasoning, transient decisions, and open questions.

## Lifetime
Discarded when the session ends, **except** durable facts that are *promoted* to a longer-lived store (project, decision, or lessons) by the [Memory Manager](../orchestration/memory-manager.md).

## Writers / readers
Written and read by the active agents during the task.

## Rules
Nothing in session memory is authoritative until validated and promoted. See [retention-and-versioning.md](retention-and-versioning.md).
