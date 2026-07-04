# Maintenance

Ongoing upkeep that keeps a product healthy between (and independent of) feature work. The
[maintenance agents](agents.md) perform this continuously, even when no developer is active.

## Continuous maintenance activities

| Activity | Owner agent |
|---|---|
| Dependency updates | [Dependency Update Agent](../agents/post-launch/dependency-update-agent.md) |
| Security patches | [Security Patch Agent](../agents/post-launch/security-patch-agent.md) |
| Performance watch | [Performance Monitoring Agent](../agents/post-launch/performance-monitoring-agent.md) |
| Infrastructure health | [Infrastructure Health Agent](../agents/post-launch/infrastructure-health-agent.md) |
| Database health & backups | [Database Maintenance Agent](../agents/post-launch/database-maintenance-agent.md) |
| API compatibility | [API Compatibility Agent](../agents/post-launch/api-compatibility-agent.md) |
| Technical-debt detection | [Technical Debt Agent](../agents/post-launch/technical-debt-agent.md) |
| Documentation accuracy | [Documentation Maintenance Agent](../agents/post-launch/documentation-maintenance-agent.md) |

## Every release includes maintenance

Bug fixes · performance improvements · UX improvements · security updates · documentation updates ·
[technical-debt reduction](technical-debt/repayment-plan.md).

## Principle

Maintain steadily so upkeep never becomes a crisis. Findings are triaged by the
[Maintenance Manager](../agents/post-launch/maintenance-manager.md) and routed to
[engineering](../engineering/README.md) or fixed via safe automation.
