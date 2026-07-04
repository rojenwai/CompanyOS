# AI Startup — Added Agents

In addition to the core [engineering](../../agents/engineering/), [product](../../agents/product/), and
[post-launch](../../agents/post-launch/) agents, an AI startup activates the **AI Division** agents.
Write each from the [agent template](../../agents/agent-template.md); they follow the
[AI engineering standards](../../ai/README.md).

| Agent | Mission (one line) |
|---|---|
| AI Architect | Choose models, infrastructure, serving, and training approach |
| Machine Learning Engineer | Build training, inference, evaluation, and deployment |
| LLM Engineer | Prompt engineering, RAG, fine-tuning, agents, tool calling, memory |
| NLP Engineer | Embeddings, retrieval, summarization, translation |
| Computer Vision Engineer | Detection, tracking, segmentation, OCR (if applicable) |
| Reinforcement Learning Engineer | Planning, policies, simulation, optimization (if applicable) |
| AI Evaluation Agent | Measure accuracy, hallucination, latency, safety, cost |
| Data Engineer | Pipelines, datasets, labeling, quality (feeds ML + RAG) |

## Interaction with core

These agents plug into the same [orchestration kernel](../../orchestration/README.md); the
[AI Evaluation Agent](../../ai/evaluation-and-testing.md) gates model/prompt changes alongside the core
[Reviewer](../../orchestration/reviewer.md), and model degradation is handled by the core
[AI model degradation playbook](../../post-launch/playbooks/ai-model-degradation.md).
