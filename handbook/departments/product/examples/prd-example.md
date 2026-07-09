# PRD — Saved Views (excerpt)

**Author:** Product Manager Agent · **Status:** Approved · **Reviewers:** Eng, Design, Security

## Executive summary

Let users save and reuse filtered views of their dashboard so repeat analysis takes seconds, not
minutes. Targets the "power analyst" persona, who reconstructs the same filters daily.

## Problem statement

Interviews (n=14) and analytics show power analysts re-apply the same 4–6 filters every session;
average time-to-first-insight is 90s. This friction correlates with lower daily retention among the
segment.

## Goals

- Cut median time-to-first-insight for the power-analyst persona from 90s to < 15s.
- Increase daily retention of the segment by 5pts within 8 weeks.

## Non-goals

- Sharing views across accounts (future).
- Scheduled export of views (future).

## Functional requirements

- Save the current filter set as a named view; list, rename, delete views.
- Set a default view applied on load.

## Non-functional requirements

- View applies in < 200ms p95 ([performance standards](../../engineering/performance-standards.md)).
- Views are per-user and access-controlled ([security standards](../../engineering/security-standards.md)).

## User stories

- **As a** power analyst **I want** to save my current filters as a named view **so that** I can
  return to my analysis instantly.
  - **Acceptance:** a saved view restores all filters exactly; appears in my list; survives reload.

## Success metrics

North-star support: time-to-first-insight (↓), segment daily retention (↑), view adoption rate.
