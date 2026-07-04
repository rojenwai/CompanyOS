# Performance Standards

Optimize based on evidence. **Never optimize prematurely.**

## Measure

Startup time · memory · CPU · latency · battery · network usage · disk usage · power consumption.

## Rules

- Establish a baseline and a target before optimizing.
- Profile first; optimize the measured bottleneck, not the assumed one.
- Re-measure after each change; keep the benchmark in the repo.
- Guard against regressions with performance tests (see [testing-standards.md](testing-standards.md)).

Owned by the [Performance Engineer](../agents/engineering/performance-engineer.md); ongoing
production performance is watched by the [Performance Monitoring Agent](../agents/post-launch/performance-monitoring-agent.md).
