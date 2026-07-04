# Agents — The AI Organization

Every AI agent is an expert. No agent attempts to do every job. Complex work is decomposed into
specialized tasks and coordinated by the [orchestration kernel](../orchestration/README.md). Each
agent owns its domain, and every important decision requires review from multiple perspectives.

Every agent is defined by the [standard agent spec](agent-template.md) — 11 sections, no exceptions.

## Agent hierarchy

```
CEO Agent
├── Orchestration (the kernel)
├── Research Division
├── Product Division
├── Business Division
├── Design Division
├── Engineering Division
├── AI Division
├── Hardware Division
├── Security Division
├── DevOps Division
├── Data Division
├── Documentation Division
├── Marketing Division
├── Sales Division
├── Finance Division
├── Legal Division
├── Investor Relations
└── Post-Launch / Maintenance Division
```

## Registry

Legend: ✅ spec written · 🧭 planned (write from the [template](agent-template.md)).

### Orchestration (kernel)
[CEO Agent](../orchestration/ceo-agent.md) ✅ · [Planner](../orchestration/planner.md) ✅ ·
[Task Decomposer](../orchestration/task-decomposer.md) ✅ · [Coordinator](../orchestration/coordinator.md) ✅ ·
[Memory Manager](../orchestration/memory-manager.md) ✅ · [Knowledge Manager](../orchestration/knowledge-manager.md) ✅ ·
[Reviewer](../orchestration/reviewer.md) ✅ · [QA Reviewer](../orchestration/qa-reviewer.md) ✅ ·
[Security Reviewer](../orchestration/security-reviewer.md) ✅ · [Documentation Reviewer](../orchestration/documentation-reviewer.md) ✅

### Engineering Division → [engineering/](engineering/)
[Software Architect](engineering/software-architect.md) ✅ · [Backend Engineer](engineering/backend-engineer.md) ✅ ·
[Frontend Engineer](engineering/frontend-engineer.md) ✅ · [Mobile Engineer](engineering/mobile-engineer.md) ✅ ·
[Database Engineer](engineering/database-engineer.md) ✅ · [Cloud Engineer](engineering/cloud-engineer.md) ✅ ·
[API Architect](engineering/api-architect.md) ✅ · [QA Engineer](engineering/qa-engineer.md) ✅ ·
[Performance Engineer](engineering/performance-engineer.md) ✅ · [Refactoring Agent](engineering/refactoring-agent.md) ✅

### Product Division → [product/](product/)
[Product Manager](product/product-manager.md) ✅ · [Feature Prioritization Agent](product/feature-prioritization-agent.md) ✅ ·
[Customer Journey Agent](product/customer-journey-agent.md) ✅ · [User Story Agent](product/user-story-agent.md) ✅ ·
[MVP Planning Agent](product/mvp-planning-agent.md) ✅

### Post-Launch / Maintenance Division → [post-launch/](post-launch/)
[Maintenance Manager](post-launch/maintenance-manager.md) ✅ · [Bug Triage Agent](post-launch/bug-triage-agent.md) ✅ ·
[Regression Agent](post-launch/regression-agent.md) ✅ · [Dependency Update Agent](post-launch/dependency-update-agent.md) ✅ ·
[Security Patch Agent](post-launch/security-patch-agent.md) ✅ · [Performance Monitoring Agent](post-launch/performance-monitoring-agent.md) ✅ ·
[Infrastructure Health Agent](post-launch/infrastructure-health-agent.md) ✅ · [Database Maintenance Agent](post-launch/database-maintenance-agent.md) ✅ ·
[API Compatibility Agent](post-launch/api-compatibility-agent.md) ✅ · [Technical Debt Agent](post-launch/technical-debt-agent.md) ✅ ·
[Documentation Maintenance Agent](post-launch/documentation-maintenance-agent.md) ✅

### Research Division 🧭
Problem Discovery · Market Research · Competitor Analysis · Patent Research · Academic Research · Technology Scout · Trend Prediction · Opportunity Ranking — see [research/](../research/).

### AI Division 🧭
AI Architect · Machine Learning Engineer · Computer Vision Engineer · NLP Engineer · LLM Engineer · Reinforcement Learning Engineer · AI Evaluation Agent — see [ai/](../ai/).

### Design Division 🧭
UX Research · UI Designer · Interaction Designer · Design System Agent — see [design/](../design/).

### Business · Hardware · Security · DevOps · Data · Documentation · Marketing · Sales · Finance · Legal · Investor Relations 🧭
Planned. Each division's agents are written from the [template](agent-template.md) as its department is built.

---

## Collaboration rules

Every agent must:

1. Explain reasoning.
2. Challenge assumptions.
3. Review work from other agents.
4. Cite evidence where applicable.
5. Identify risks.
6. Estimate cost.
7. Estimate timeline.
8. Provide alternatives.
9. Document decisions.
10. Recommend next actions.

**No agent operates independently on major decisions.** Strategic work requires cross-functional
review before approval by the [CEO Agent](../orchestration/ceo-agent.md).
