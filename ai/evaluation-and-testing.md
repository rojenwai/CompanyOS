# AI Evaluation & Testing

## Evaluation framework

Every AI system is measured on: accuracy · precision · recall · latency · cost · reliability · safety ·
robustness · user satisfaction · task completion rate.

## Required tests

- **Prompt regression** — outputs stay correct as prompts change.
- **Tool integration** — tools are called correctly with valid inputs.
- **Memory consistency** — context is assembled correctly ([memory](../memory/README.md)).
- **Retrieval quality** — [RAG](README.md#retrieval-augmented-generation-rag) returns relevant, sourced results.
- **Latency** — within targets.
- **Adversarial prompts & jailbreak resistance** — safety holds under attack ([ai-security.md](ai-security.md)).
- **Long-context handling** — no degradation with large context.

## Process

Maintain evaluation datasets; run the suite before promoting a prompt/model change; record results.
Production degradation is caught by the [AI model degradation playbook](../post-launch/playbooks/ai-model-degradation.md)
and feeds the [continuous improvement loop](../orchestration/continuous-improvement-engine.md).
