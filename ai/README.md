# AI Engineering

> 🌱 **Seeded department.** Real content migrated from the AI engineering handbook. The multi-agent
> orchestration and memory portions live in [orchestration/](../orchestration/) and [memory/](../memory/);
> this department covers AI-specific engineering standards. Upgrade to the full
> [structure](../STRUCTURE.md#standard-department-structure) later.

AI is treated as an engineering discipline, not prompt writing. The objective is **not** chatbots but
reliable intelligent systems that solve real problems, reason correctly, use tools effectively,
minimize hallucinations, and improve continuously.

## AI design principles

Every AI system must be: reliable · explainable · observable · modular · tool-driven · memory-aware ·
secure · cost-efficient · continuously evaluated. **Never rely solely on an LLM's internal knowledge
when external data is available.** See [design-principles.md](design-principles.md).

## AI system architecture & pipeline

```
User → API Gateway → Conversation Manager → Planner
  → Memory + Knowledge Base → Retriever (RAG) → Tool Router
  → Specialist Agents → Reviewer → Final Response
```

Every request: understand intent → gather context → search [memory](../memory/) → retrieve knowledge →
plan → select tools → delegate to specialists → validate → review → deliver. **Never answer immediately
if planning or retrieval is required.**

## Retrieval-Augmented Generation (RAG)

LLMs retrieve before generating whenever factual accuracy matters. Sources: internal docs, PRDs, design
docs, standards, APIs, databases, PDFs, source code, research papers. Every retrieval returns
**source, confidence, timestamp, and relevance score** (see [memory/retrieval.md](../memory/retrieval.md)).

## Prompt engineering standards

Prompts define: role · objective · context · constraints · expected output · evaluation criteria. Avoid
ambiguity. Prompts are versioned in [prompt memory](../memory/prompt-memory.md). See
[prompt-engineering.md](prompt-engineering.md).

## Reasoning & hallucination prevention

Before answering: identify objective → identify assumptions → verify available information → plan →
execute → validate → explain if appropriate.

**Never invent** APIs · functions · research · statistics · company information · legal advice · medical
facts. If uncertain: state uncertainty, recommend verification, retrieve more. This enforces the
company rule in [governance/failure-handling.md](../governance/failure-handling.md).

## Model selection

Select the model to the task (reasoning · coding · vision · speech · embedding · translation ·
classification). **Do not use the largest model if a smaller one suffices** ([cost](#cost-optimization)).
When building on Claude, default to the latest, most capable models for the task.

## Evaluation & testing

Measured on: accuracy · precision · recall · latency · cost · reliability · safety · robustness · user
satisfaction · task completion rate. Required tests: prompt regression · tool integration · memory
consistency · retrieval quality · latency · adversarial prompts · jailbreak resistance · long-context
handling. See [evaluation-and-testing.md](evaluation-and-testing.md).

## Autonomous execution & Human-in-the-Loop

Agents may act autonomously only when the objective is clear, information is available, safety
requirements are met, and confidence exceeds threshold — otherwise request clarification. Human
approval is **required** for financial commitments, legal documents, production deployments,
security-sensitive actions, irreversible operations, and customer-impacting changes
([approval engine](../orchestration/approval-engine.md)).

## Cost optimization

Prefer caching · batch processing · smaller models · efficient retrieval · streaming. Avoid unnecessary
model invocations. Manage context precisely ([memory/context-management.md](../memory/context-management.md)).

## Observability & AI security

Log tool usage · latency · errors · token usage · retrieval results · decision paths · model version —
never secrets or personal data. Protect against prompt injection · data poisoning · tool abuse ·
unauthorized access · sensitive-data leakage · model misuse. Validate all external inputs. See
[ai-security.md](ai-security.md).

## Continuous learning

After every task: record lessons → identify failure modes → update docs, prompts, workflows, and
evaluation datasets. The AI organization gets more capable through disciplined iteration, driven by the
[Continuous Improvement Engine](../orchestration/continuous-improvement-engine.md).
