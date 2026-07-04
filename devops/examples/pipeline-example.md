# Example - CI/CD Pipeline Stages

> Worked example - illustrative, not a live record.

```
commit
  -> lint + unit tests
  -> build immutable artifact
  -> integration tests
  -> security scans (SCA/SAST/secret) [gate]
  -> coverage gate (>=80%)
  -> deploy to staging + e2e
  -> canary (5%) + health check [auto-rollback on breach]
  -> progressive rollout to 100%
  -> post-deploy verification + changelog
```

Any red gate stops the pipeline; a failed canary triggers automatic rollback to the last-good version.
