# Post Launch Agents

The AI agents for the [post-launch department](../../../handbook/departments/post-launch/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [# API Compatibility Agent](api-compatibility-agent.md) |  |
| [# Bug Triage Agent](bug-triage-agent.md) |  |
| [# Database Maintenance Agent](database-maintenance-agent.md) |  |
| [# Dependency Update Agent](dependency-update-agent.md) |  |
| [# Documentation Maintenance Agent](documentation-maintenance-agent.md) |  |
| [# Infrastructure Health Agent](infrastructure-health-agent.md) |  |
| [# Maintenance Manager Agent](maintenance-manager.md) |  |
| [# Performance Monitoring Agent](performance-monitoring-agent.md) |  |
| [# Regression Agent](regression-agent.md) |  |
| [# Security Patch Agent](security-patch-agent.md) |  |
| [# Technical Debt Agent](technical-debt-agent.md) |  |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent post-launch <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
