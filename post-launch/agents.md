# Maintenance AI Agents

These agents continuously inspect the product even when no developer is actively working on it. Full
specs in [agents/post-launch/](../agents/post-launch/).

| Agent | Mission (one line) | Spec |
|---|---|---|
| Maintenance Manager | Keep every product healthy; coordinate the division | [maintenance-manager.md](../agents/post-launch/maintenance-manager.md) |
| Bug Triage Agent | Classify and route bugs fast and correctly | [bug-triage-agent.md](../agents/post-launch/bug-triage-agent.md) |
| Regression Agent | Catch reintroduced defects before customers do | [regression-agent.md](../agents/post-launch/regression-agent.md) |
| Dependency Update Agent | Keep dependencies current, safe, and licensed | [dependency-update-agent.md](../agents/post-launch/dependency-update-agent.md) |
| Security Patch Agent | Apply security patches promptly and safely | [security-patch-agent.md](../agents/post-launch/security-patch-agent.md) |
| Performance Monitoring Agent | Detect performance regressions in production | [performance-monitoring-agent.md](../agents/post-launch/performance-monitoring-agent.md) |
| Infrastructure Health Agent | Keep infrastructure healthy and within cost | [infrastructure-health-agent.md](../agents/post-launch/infrastructure-health-agent.md) |
| Database Maintenance Agent | Keep data healthy, backed up, and intact | [database-maintenance-agent.md](../agents/post-launch/database-maintenance-agent.md) |
| API Compatibility Agent | Prevent breaking changes to published APIs | [api-compatibility-agent.md](../agents/post-launch/api-compatibility-agent.md) |
| Technical Debt Agent | Detect and track debt continuously | [technical-debt-agent.md](../agents/post-launch/technical-debt-agent.md) |
| Documentation Maintenance Agent | Keep documentation accurate and current | [documentation-maintenance-agent.md](../agents/post-launch/documentation-maintenance-agent.md) |

## Collaboration map

Detection agents (monitoring, health, debt, dependency, API) raise findings → [Maintenance Manager](../agents/post-launch/maintenance-manager.md)
triages → routes fixes to [engineering](../engineering/README.md) or applies safe automated changes →
[reviewers](../orchestration/reviewer.md) gate → [Execution Engine](../orchestration/execution-engine.md) ships.
