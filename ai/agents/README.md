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

### Research Division → [research/](research/) ✅
[Problem Discovery](research/problem-discovery-agent.md) · [Market Research](research/market-research-agent.md) · [Competitor Analysis](research/competitor-analysis-agent.md) · [Opportunity Ranking](research/opportunity-ranking-agent.md)

### AI Division → [ai/](ai-engineering/) ✅
[AI Architect](ai-engineering/ai-architect-agent.md) · [LLM Engineer](ai-engineering/llm-engineer-agent.md) · [ML Engineer](ai-engineering/ml-engineer-agent.md) · [AI Evaluation](ai-engineering/ai-evaluation-agent.md)

### Design Division → [design/](design/) ✅
[UX Research](design/ux-research-agent.md) · [UI Designer](design/ui-designer-agent.md) · [Interaction Designer](design/interaction-designer-agent.md) · [Design System](design/design-system-agent.md) · [Accessibility](design/accessibility-agent.md)

### Strategy / Business Division → [strategy/](strategy/) ✅
[Business Strategy](strategy/business-strategy-agent.md) · [Business Model & Pricing](strategy/business-model-pricing-agent.md) · [Go-To-Market](strategy/go-to-market-agent.md) · [Fundraising](strategy/fundraising-agent.md)

### Security Division → [security/](security/) ✅
[Security Architect](security/security-architect-agent.md) · [Penetration Testing](security/penetration-testing-agent.md) · [Vulnerability Management](security/vulnerability-management-agent.md) · [Compliance & Privacy](security/compliance-privacy-agent.md)

### DevOps Division → [devops/](devops/) ✅
[CI/CD Engineer](devops/cicd-engineer-agent.md) · [Platform Engineer](devops/platform-engineer-agent.md) · [Site Reliability](devops/site-reliability-agent.md) · [Release Engineer](devops/release-engineer-agent.md)

### Finance Division → [finance/](finance/) ✅
[Financial Planning](finance/financial-planning-agent.md) · [Accounting](finance/accounting-agent.md) · [Revenue & Billing](finance/revenue-billing-agent.md) · [Cost Optimization](finance/cost-optimization-agent.md)

### Legal Division → [legal/](legal/) ✅
[Contract](legal/contract-agent.md) · [IP & Patent](legal/ip-patent-agent.md) · [Compliance](legal/compliance-agent.md) · [Privacy & Terms](legal/privacy-terms-agent.md)

### People & HR Division → [hr/](hr/) ✅
[Recruiting](hr/recruiting-agent.md) · [Onboarding](hr/onboarding-agent.md) · [Performance & Growth](hr/performance-growth-agent.md) · [Culture](hr/culture-agent.md)

### Operations Division → [operations/](operations/) ✅
[Project Management](operations/project-management-agent.md) · [Process Optimization](operations/process-optimization-agent.md) · [Vendor Management](operations/vendor-management-agent.md) · [Knowledge Management](operations/knowledge-management-agent.md)

### Marketing Division → [marketing/](marketing/) ✅
[Content Marketing](marketing/content-marketing-agent.md) · [SEO](marketing/seo-agent.md) · [Brand & Communications](marketing/brand-communications-agent.md) · [Growth Marketing](marketing/growth-marketing-agent.md)

### Sales Division → [sales/](sales/) ✅
[Prospecting](sales/prospecting-agent.md) · [Account Executive](sales/account-executive-agent.md) · [Sales Engineer](sales/sales-engineer-agent.md) · [Deal Desk](sales/deal-desk-agent.md)

### Customer Success Division → [customer-success/](customer-success/) ✅
[Customer Onboarding](customer-success/customer-onboarding-agent.md) · [Support](customer-success/support-agent.md) · [Customer Health](customer-success/customer-health-agent.md) · [Renewal & Expansion](customer-success/renewal-expansion-agent.md)

### Data Division → [data/](data/) ✅
[Data Engineer](data/data-engineer-agent.md) · [Analytics Engineer](data/analytics-engineer-agent.md) · [Data Scientist](data/data-scientist-agent.md) · [Data Governance](data/data-governance-agent.md)

### Documentation Division → [documentation/](documentation/) ✅
[Technical Writer](documentation/technical-writer-agent.md) · [API Documentation](documentation/api-documentation-agent.md) · [Knowledge Base](documentation/knowledge-base-agent.md)

### Hardware Division → [hardware/](hardware/) ✅
[Firmware Engineer](hardware/firmware-engineer-agent.md) · [Electrical Engineer](hardware/electrical-engineer-agent.md) · [Mechanical Engineer](hardware/mechanical-engineer-agent.md) · [Hardware Test](hardware/hardware-test-agent.md)

### Investor Relations Division → [investor-relations/](investor-relations/) ✅
[Investor Reporting](investor-relations/investor-reporting-agent.md) · [Board Governance](investor-relations/board-governance-agent.md) · [Cap Table](investor-relations/cap-table-agent.md)

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
