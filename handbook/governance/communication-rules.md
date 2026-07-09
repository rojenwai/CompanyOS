# Communication Rules

Every agent communicates using structured reports. Never send vague responses.

Every report contains:

- **Summary**
- **Findings**
- **Reasoning**
- **Risks**
- **Recommendations**
- **Action Items**
- **Confidence Level**

---

## Why structure

Structured reports are reviewable, comparable, and storable in [memory](../../ai/memory/). They force the
author to separate evidence from opinion and to state confidence explicitly, which is essential for
[hallucination prevention](../departments/ai-engineering/README.md) and for downstream agents that consume the output.

For long-form deliverables, follow the [universal output format](universal-output-format.md).
