# Release Checklist — <version>

**Release type:** Major / Minor / Patch / Hotfix · **Owner:** <name/agent> · **Target date:** <date>

## Pre-release gates

- [ ] Requirements complete
- [ ] Tests passing (unit, integration, e2e)
- [ ] Documentation updated
- [ ] [Security review](security-review.md) approved
- [ ] Performance verified
- [ ] Product approved
- [ ] Rollback plan prepared and tested
- [ ] Monitoring & alerts configured
- [ ] Support/on-call briefed

## Deploy

- [ ] Build & package
- [ ] Deploy to staging → verify
- [ ] Deploy to production (flagged / phased)
- [ ] Smoke tests pass in production

## Post-release

- [ ] Telemetry looks healthy (errors, latency, saturation)
- [ ] Announce (changelog / customers)
- [ ] Feed learnings to [post-launch](../../post-launch/README.md) and [continuous improvement](../../post-launch/README.md)

## Rollback

**Trigger:** <condition> · **Procedure:** link to [rollback](../../post-launch/rollback.md).
