# Data - Playbooks

Situational guides. Each names the trigger and the steps.

### A dashboard shows wrong numbers

1. Trace to the metric definition and pipeline
2. Check freshness and quality tests
3. Fix the root cause (source, pipeline, or model)
4. Backfill and verify
5. Add a test to prevent recurrence

### Conflicting metric definitions

1. Identify the divergent definitions
2. Agree one canonical definition with the owner
3. Model it once in the semantic layer
4. Deprecate the duplicates
5. Communicate the change
