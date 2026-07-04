# Example - Design Critique Notes

> Worked example - illustrative, not a live record.

**Feature:** Saved Views panel.

| Area | Finding | Action |
|---|---|---|
| Hierarchy | Primary action competes with secondary | Demote 'Duplicate' to overflow |
| Feedback | No confirmation on save | Add inline saved toast + optimistic state |
| Accessibility | Icon-only buttons lack labels | Add aria-labels and tooltips |
| States | Empty state undefined | Design empty state with a create CTA |

**Outcome:** Criticals (accessibility, empty state) block handoff; hierarchy and feedback fixes scheduled before build.
