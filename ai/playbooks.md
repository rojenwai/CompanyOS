# AI Engineering - Playbooks

Situational guides. Each names the trigger and the steps.

### Model quality regresses in production

1. Confirm with the [AI Evaluation Agent](evaluation-and-testing.md)
2. Roll back to the last-good model/prompt version
3. Diagnose (data, prompt, model, drift)
4. Fix, re-evaluate, and re-ship
5. Follow the [ai-model-degradation playbook](../post-launch/playbooks/ai-model-degradation.md)

### Suspected prompt injection

1. Contain and log the incident
2. Reproduce with an adversarial test
3. Harden inputs and constrain tools
4. Add the case to the eval suite
5. Notify [security](../security/README.md)
