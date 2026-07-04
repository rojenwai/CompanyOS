# Playbook: AI Model Degradation

**When to use:** an AI model's quality, latency, or cost regresses in production.

1. **Detect:** [AI performance](../monitoring.md) metrics drop (accuracy, hallucination rate, latency, cost per call).
2. **Classify:** input/data drift · provider change · prompt regression · upstream model update · cost spike.
3. **Mitigate:** roll back to the last known-good [prompt/model version](../../memory/prompt-memory.md); route to a fallback model if needed.
4. **Diagnose** against the [evaluation framework](../../ai/README.md); reproduce on the eval set.
5. **Fix:** update prompt/model; re-run [AI tests](../../ai/README.md) (prompt regression, adversarial) before redeploy.

**Success criteria:** model quality/latency/cost back within targets; eval suite green.
**Escalate if:** degradation causes customer-facing errors → declare an [incident](../incident-response.md).
