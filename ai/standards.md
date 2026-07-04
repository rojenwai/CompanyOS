# AI Engineering - Standards

Testable standards, not aspirations. These extend the company-wide
[standards](../standards/README.md).

1. No model or prompt ships without a passing evaluation report.
2. Every prompt and model is versioned; rollback is always available.
3. Every deployed model has a model card (capabilities, limits, eval results).
4. Retrieve before generating whenever factual accuracy matters.
5. Cost per request and per resolved task are tracked and budgeted.
6. Never log secrets, PII, or raw user data from AI systems.
