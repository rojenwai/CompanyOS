# Software Development Lifecycle (SDLC)

> Every project follows the same disciplined process. **No phase may be skipped** without explicit
> approval from the [CEO Agent](../orchestration/ceo-agent.md).

## Overview

```
Idea → Problem Discovery → Research → Market Validation → Business Analysis
→ Product Definition → Requirements → Architecture → System Design → UI/UX Design
→ Development → Testing → Security Review → Performance Optimization → Documentation
→ Deployment → Monitoring → Customer Feedback → Iteration → Scaling
```

## The 20 phases

| # | Phase | Owner | Exit criteria |
|---|---|---|---|
| 1 | **Problem Discovery** | [Product](../product/discovery.md) | Problem validated with evidence |
| 2 | **Research** | [Research](../research/README.md) | Opportunity confirmed |
| 3 | **Market Validation** | [Product](../product/discovery.md) / [Strategy](../strategy/README.md) | Clear demand identified |
| 4 | **Business Analysis** | [Strategy](../strategy/README.md) | Viable business model |
| 5 | **Product Definition** | [Product](../product/README.md) | Vision, goals, metrics set |
| 6 | **Requirements** | [Product](../product/requirements.md) | Functional + non-functional + stories ready |
| 7 | **Architecture** | [Engineering](../engineering/organization.md) | Architecture approved ([ADR](../templates/documents/adr.md)) |
| 8 | **System Design** | Engineering | Services/modules designed |
| 9 | **Database Design** | [Engineering](../engineering/database-standards.md) | Schema, migrations, backup plan |
| 10 | **API Design** | [Engineering](../engineering/api-standards.md) | Contracts + OpenAPI docs |
| 11 | **UI/UX Design** | [Design](../design/README.md) | Flows, prototypes, accessibility reviewed |
| 12 | **Development** | [Engineering](../engineering/workflows.md) | [Definition of Done](../engineering/quality-gates.md) met |
| 13 | **Testing** | [Engineering/QA](../engineering/testing-standards.md) | Coverage targets met |
| 14 | **Security Review** | [Security](../engineering/security-standards.md) | Security approved |
| 15 | **Performance Optimization** | [Engineering](../engineering/performance-standards.md) | Performance verified |
| 16 | **Documentation** | [Docs](../engineering/documentation-requirements.md) | Required docs complete |
| 17 | **Deployment** | [Engineering/DevOps](../post-launch/release-management.md) | Deployed + rollback ready |
| 18 | **Monitoring** | [Post-Launch](../post-launch/monitoring.md) | Monitoring & alerts live |
| 19 | **Customer Feedback** | [Post-Launch](../post-launch/customer-feedback.md) | Feedback collected |
| 20 | **Iteration** | [Post-Launch](../post-launch/continuous-improvement.md) | Improvements prioritized → Scaling |

## Gates

Each phase is protected by a [quality gate](../governance/quality-gates.md); the
[execution engine](../orchestration/execution-engine.md) will not advance work that has not cleared it.
Phases 1–6 are product/strategy-led, 7–17 engineering-led, and 18–20 post-launch-led — but every phase
requires cross-functional review per the [collaboration rules](../agents/README.md).
