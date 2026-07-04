# Requirements — PRD, Stories & Acceptance Criteria

How product defines what to build. The fill-in template is [templates/documents/prd.md](../templates/documents/prd.md).

## PRD contents

Executive summary · background · problem statement · goals · non-goals · [user personas](user-personas.md) ·
functional requirements · non-functional requirements · user stories · acceptance criteria · success
metrics · dependencies · risks · timeline · release plan.

## Functional requirements

Describe system behavior, business rules, user interactions, edge cases, error handling, permissions.

## Non-functional requirements

Performance · scalability · reliability · availability · security · accessibility · localization ·
compliance · maintainability · observability. (These map directly to
[engineering standards](../engineering/standards.md).)

## User stories

Format: **As a** \<persona> **I want** \<capability> **so that** \<outcome>.
Each includes: priority · acceptance criteria · dependencies · business value.

## Acceptance criteria

Must be **specific · measurable · testable · complete · unambiguous** — each criterion maps to at
least one [test](../engineering/testing-standards.md). Stories are only handed to engineering when
they meet the [Definition of Ready](../engineering/definition-of-ready.md).
