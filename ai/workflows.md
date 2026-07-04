# AI Engineering - Workflows

The core repeatable processes this department runs.

### AI delivery lifecycle

1. Define the metric that means good
2. Assemble/extend the evaluation set
3. Build the prompt/RAG/model
4. Run the evaluation suite (accuracy, safety, latency, cost)
5. Gate: pass or fix
6. Ship versioned with a model card
7. Monitor drift and cost in production

### Prompt change

1. Draft the new prompt version
2. Run prompt regression evals
3. Compare cost and quality vs. current
4. Promote in [prompt memory](../memory/prompt-memory.md) or roll back
