# DevOps - Workflows

The core repeatable processes this department runs.

### Commit to production

1. Open a PR; CI runs tests, coverage, and security gates
2. Merge on green with reviews
3. Build an immutable artifact
4. Deploy progressively (canary)
5. Verify health
6. Promote or roll back

### Provision infrastructure

1. Define the change as code
2. Review and plan
3. Apply to a staging environment
4. Validate
5. Apply to production
6. Record and monitor cost
