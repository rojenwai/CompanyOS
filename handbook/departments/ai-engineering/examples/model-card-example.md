# Example - Model Card

> Worked example - illustrative, not a live record.

**Feature:** Support-ticket summarizer
**Model:** claude-haiku (grounded via RAG over the docs KB)
**Version:** sum-2026.07-03

| Dimension | Result |
|---|---|
| Accuracy (human-rated, n=200) | 94% acceptable |
| Hallucination rate | 1.5% |
| p95 latency | 1.9s |
| Cost per summary | $0.004 |
| Jailbreak resistance | 100% of suite blocked |

**Limits:** English only; degrades on tickets >4k tokens (truncation).
**Rollback:** previous version sum-2026.06-02 pinned and one-command restorable.
