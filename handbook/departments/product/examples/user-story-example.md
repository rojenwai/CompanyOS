# Example - User Stories & Acceptance Criteria

> Worked example - illustrative, not a live record. Format per [requirements.md](../requirements.md);
> stories must meet the [Definition of Ready](../../engineering/definition-of-ready.md) before build.

**Feature:** Saved Views (see the [PRD example](prd-example.md)).

---

## Story 1 - Save the current view

**As a** support lead
**I want to** save my current filter and column layout as a named view
**So that** I don't rebuild the same filters every morning.

**Acceptance criteria** (specific, measurable, testable, unambiguous):

- [ ] Given filters and columns are set, when I click "Save view" and enter a name, then the view is saved to my account.
- [ ] A view name is required, must be 1-50 characters, and must be unique per user; a duplicate name shows an inline error.
- [ ] The saved view captures filters, sort order, and visible columns - not the current page number.
- [ ] Saving shows immediate confirmation ([feedback](../../design/interaction-design.md)) and the new view appears in the view list without a reload.
- [ ] The "Save view" control is keyboard reachable and screen-reader labelled ([accessibility](../../design/accessibility.md)).

**Not in scope:** sharing a view with teammates (Story 4).

---

## Story 2 - Apply a saved view

**As a** support lead
**I want to** apply a saved view in one click
**So that** I reach my working state instantly.

**Acceptance criteria:**

- [ ] Given a saved view exists, when I select it, then filters, sort, and columns are restored within 500ms (p95).
- [ ] The applied view's name is visible in the toolbar so I always know which view I'm in.
- [ ] If a saved view references a column that no longer exists, the view loads without it and shows a non-blocking notice (no error state, no crash).
- [ ] Empty state: if I have no saved views, the list explains what views are and how to create one.

---

## Why these are "Ready"

Each story names a real user, a real outcome, and criteria a QA engineer could test without asking a
question. Edge cases (duplicate name, deleted column, empty state) are decided *before* build, not
discovered during it - which is the entire point of the [Definition of Ready](../../engineering/definition-of-ready.md).
