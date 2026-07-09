# AI Engineering - Quality Gates

Work does not progress until the relevant gate passes. These implement the company
[quality gates](../../governance/quality-gates.md).

| Gate | Must pass |
|---|---|
| Evaluation gate | Passing accuracy, hallucination, safety, latency, and cost report |
| Grounding gate | Factual features retrieve with source, confidence, and timestamp |
| Versioning gate | Prompt/model versioned with a model card and rollback |
| Security gate | Adversarial and injection tests pass ([ai-security.md](ai-security.md)) |
