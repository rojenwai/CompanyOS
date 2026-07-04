# Engineering Metrics

What engineering measures. Every metric must drive a decision.

## North-star

**Reliable systems delivered** — proxied by change-failure rate × uptime, not by output volume.

## DORA metrics

| Metric | Definition | Direction |
|---|---|---|
| Deployment frequency | How often we ship | ↑ |
| Lead time for change | Commit → production | ↓ |
| Change failure rate | % of deploys causing incidents | ↓ |
| Mean time to recovery | Incident → resolved | ↓ |

## Quality metrics

Test coverage (vs [targets](testing-standards.md)) · escaped-defect rate · review turnaround ·
technical-debt trend · security findings pre- vs post-release.

## Anti-metrics (watch, don't optimize)

Lines of code · number of commits · raw velocity — easily gamed, poorly correlated with value.
