# Example - Metric Definition

> Worked example - illustrative, not a live record.

**Metric:** Weekly Active Team (WAT).

| Field | Definition |
|---|---|
| Meaning | A customer team with >=3 distinct users performing a core action in a rolling 7-day window |
| Grain | Per customer team, per day (rolling 7d) |
| Source | events.core_action, joined to teams |
| Owner | Data + Product |
| Excludes | Internal/test accounts, deleted users |

**Rule:** WAT is defined once in the semantic layer; every dashboard reads this definition - no local recomputation.
