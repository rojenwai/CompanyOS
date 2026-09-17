"""Orchestration step names, passed to providers as routing metadata.

Kept in their own module so the provider layer and the orchestration layer can
both name a step without importing each other.
"""

from __future__ import annotations

PLAN = "plan"
"""CEO -> Planner: frame the objective and the approach."""

DECOMPOSE = "decompose"
"""Planner -> Task Decomposer: produce the subtask DAG."""

EXECUTE = "execute"
"""A spawned specialist instance doing its task."""

REVIEW = "review"
"""A reviewer critiquing aggregated results."""

SYNTHESIZE = "synthesize"
"""Entry agent composing the final response."""

ALL = (PLAN, DECOMPOSE, EXECUTE, REVIEW, SYNTHESIZE)
