# Playbook: Database Failure

**When to use:** the database is down, unreachable, or returning corrupt data.

1. **Declare** an incident; protect data — stop writes if corruption is suspected.
2. **Identify** failure type: node down · replication lag · disk full · corruption.
3. **Failover** to a healthy replica if available; promote and redirect.
4. **If corruption:** isolate, then restore from the latest verified [backup](../playbooks/failed-backup.md); quantify data loss window.
5. **Verify** integrity before resuming writes.
6. **Root cause** with the [Database Maintenance Agent](../../agents/post-launch/database-maintenance-agent.md).

**Success criteria:** data integrity preserved; service restored from a known-good state.
**Escalate if:** data loss is possible/confirmed → human approval before destructive recovery ([approval](../../orchestration/approval-engine.md)).
