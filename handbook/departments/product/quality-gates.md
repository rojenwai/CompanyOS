# Product Quality Gates

## Discovery gate
Advance to definition only when the problem is validated with evidence and a target [persona](user-personas.md) is identified.

## Definition gate
Advance to build only when the [PRD](requirements.md) is complete, prioritized, and stories meet the [Definition of Ready](../engineering/definition-of-ready.md).

## Launch checklist
Ship only when:

- [ ] Product ready
- [ ] Engineering approved
- [ ] QA passed
- [ ] Security approved
- [ ] Performance validated
- [ ] Documentation complete
- [ ] Support prepared
- [ ] Marketing prepared
- [ ] Analytics configured
- [ ] Rollback plan available

(Executed with the [release checklist](../../templates/documents/release-checklist.md).)

## Post-launch gate
A feature is only "successful" once its instrumented [success metric](metrics.md) shows the intended
outcome — otherwise it enters the [iteration loop](../post-launch/README.md).
