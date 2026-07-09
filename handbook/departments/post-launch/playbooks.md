# Post-Launch Playbooks

Post-launch has enough situational guides to warrant their own folder. The full set lives in
[playbooks/](playbooks/).

| Playbook | Situation |
|---|---|
| [Critical outage](playbooks/critical-outage.md) | Full or partial service outage |
| [Database failure](playbooks/database-failure.md) | Database down or corrupt |
| [Memory leak](playbooks/memory-leak.md) | Growing memory / OOM |
| [Security breach](playbooks/security-breach.md) | Suspected or confirmed breach |
| [Broken deployment](playbooks/broken-deployment.md) | A deploy broke production |
| [Slow API](playbooks/slow-api.md) | Latency degradation |
| [High cloud cost](playbooks/high-cloud-cost.md) | Cost spike |
| [Dependency vulnerability](playbooks/dependency-vulnerability.md) | Vulnerable dependency |
| [Failed backup](playbooks/failed-backup.md) | Backup or restore failed |
| [AI model degradation](playbooks/ai-model-degradation.md) | Model quality/latency/cost regression |
| [Rollback](playbooks/rollback.md) | Executing a rollback |
| [Emergency hotfix](playbooks/emergency-hotfix.md) | Shipping an urgent fix |

Each pairs with [incident-response.md](incident-response.md) and the
[incident checklist](checklists/incident-checklist.md).
