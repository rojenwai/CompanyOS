# Playbook: Failed Backup

**When to use:** a scheduled backup failed, or a restore test failed.

1. **Alert** immediately — a missing backup is a latent SEV1 waiting to happen.
2. **Diagnose:** storage full · permissions · job error · corrupt snapshot.
3. **Re-run** the backup once fixed; confirm completion.
4. **Test restore:** a backup is only valid if a restore succeeds — verify on a scratch environment.
5. **Root cause & prevent:** add/repair monitoring so silent failures cannot recur ([Database Maintenance Agent](../../../../ai/agents/post-launch/database-maintenance-agent.md)).

**Success criteria:** a verified, restorable backup exists; restore tested.
**Escalate if:** no valid backup exists for a critical dataset → SEV1, human leadership.
