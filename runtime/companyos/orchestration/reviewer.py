"""The review stage.

Uses the reviewer agents already specified in ``ai/orchestration/`` -- the
general Reviewer, the QA Reviewer, the Security Reviewer, the Documentation
Reviewer -- selected by the concerns the work actually raises. They run in
parallel over the aggregated results and their verdicts are merged by severity.

Two rules come straight from the specs and are enforced here, not left to the
model:

* A Security Reviewer **Block** can never be auto-approved
  (``approval-engine.md``). It sets the run to AWAITING_APPROVAL.
* A rejected deliverable goes back to its author with the findings attached,
  rather than being blind-retried (``execution-lifecycle.md``).
"""

from __future__ import annotations

import asyncio
from typing import Sequence

from .. import purposes
from ..config import RuntimeConfig
from ..errors import ProviderError
from ..models import ReviewFinding, ReviewReport, Usage
from ..observability import EventBus, EventType
from ..providers import Message, Provider, extract_json
from ..registry import AgentRegistry
from ..registry.definition import AgentDefinition
from ..status import Verdict
from .aggregator import Aggregation
from .prompts import json_instruction, kernel_system_prompt, untrusted
from .selector import AgentSelector

_REVIEW_SCHEMA = """{
  "verdict": "approve | approve_with_changes | revise | reject | escalate | block",
  "summary": "one or two sentences",
  "findings": [
    {
      "task_id": "the task the defect is in",
      "severity": "critical | high | medium | low",
      "issue": "what is wrong, specifically",
      "required_change": "what the author must do"
    }
  ]
}"""

#: Worst verdict wins when several reviewers disagree.
_SEVERITY_ORDER = [
    Verdict.APPROVE,
    Verdict.APPROVE_WITH_CHANGES,
    Verdict.REVISE,
    Verdict.REJECT,
    Verdict.ESCALATE,
    Verdict.BLOCK,
]


class ReviewCoordinator:
    """Runs the reviewer agents and merges their verdicts."""

    def __init__(
        self,
        registry: AgentRegistry,
        selector: AgentSelector,
        provider: Provider,
        config: RuntimeConfig,
        bus: EventBus,
    ) -> None:
        self.registry = registry
        self.selector = selector
        self.provider = provider
        self.config = config
        self.bus = bus

    async def review(
        self, request: str, aggregation: Aggregation, *, run_id: str, concerns: Sequence[str] = ()
    ) -> ReviewReport:
        """Review the aggregated results and return one merged report."""
        reviewers = self.selector.select_reviewers(list(concerns))
        if not reviewers:
            return ReviewReport(verdict=Verdict.APPROVE, summary="no reviewer is configured")

        self.bus.emit(
            EventType.REVIEW_STARTED,
            run_id=run_id,
            message=f"{len(reviewers)} reviewer(s)",
            data={"reviewers": [r.id for r in reviewers], "concerns": list(concerns)},
        )

        reports = await asyncio.gather(
            *(self._run_one(r, request, aggregation, run_id) for r in reviewers)
        )
        merged = self._merge(reports)

        self.bus.emit(
            EventType.REVIEW_COMPLETED,
            run_id=run_id,
            message=f"{merged.verdict.value}: {merged.summary[:100]}",
            data={
                "verdict": merged.verdict.value,
                "findings": len(merged.findings),
                "reviewers": [r.reviewer for r in reports],
            },
        )
        if merged.verdict is Verdict.BLOCK:
            self.bus.emit(
                EventType.APPROVAL_REQUIRED,
                run_id=run_id,
                message="security block cannot be auto-approved; human sign-off required",
                data={"verdict": merged.verdict.value},
            )
        return merged

    # -- one reviewer ----------------------------------------------------------

    async def _run_one(
        self,
        definition: AgentDefinition,
        request: str,
        aggregation: Aggregation,
        run_id: str,
    ) -> ReviewReport:
        system = kernel_system_prompt(
            definition,
            "Review the deliverables below. Never assume the author is correct. "
            "Report only specific, reproducible findings; do not rewrite the work.",
        )
        user = "\n\n".join(
            [
                "Original request:",
                untrusted("user-request", request),
                "Deliverables to review:",
                aggregation.render(),
                (
                    "Note: some tasks failed or were skipped. Judge whether the "
                    "remaining work is still sufficient.\n- "
                    + "\n- ".join(aggregation.gaps())
                    if aggregation.gaps()
                    else ""
                ),
                json_instruction(_REVIEW_SCHEMA),
            ]
        )

        try:
            completion = await self.provider.complete(
                system=system,
                messages=[Message("user", user)],
                purpose=purposes.REVIEW,
                context={
                    "run_id": run_id,
                    "agent_id": definition.id,
                    "reviewer": definition.id,
                    "task_ids": aggregation.task_ids,
                },
            )
            return self._parse(completion.text, definition, completion.usage, aggregation)
        except (ProviderError, ValueError, TypeError) as exc:
            # A reviewer that cannot run must not silently approve.
            return ReviewReport(
                verdict=Verdict.ESCALATE,
                summary=f"reviewer {definition.id} could not complete: {exc}",
                reviewer=definition.id,
            )

    def _parse(
        self,
        text: str,
        definition: AgentDefinition,
        usage: Usage,
        aggregation: Aggregation,
    ) -> ReviewReport:
        data = extract_json(text)
        verdict = _verdict(str(data.get("verdict", "approve")))

        # approval-engine.md gives blocking authority to the Security Reviewer
        # specifically. Identity decides it, not a claimed concern: any other
        # reviewer's block is recorded as a rejection, which still stops the
        # work but can be cleared by rework instead of human sign-off.
        if verdict is Verdict.BLOCK and not _may_block(definition):
            verdict = Verdict.REJECT

        valid_ids = set(aggregation.task_ids)
        findings = []
        for item in data.get("findings") or []:
            if not isinstance(item, dict):
                continue
            task_id = str(item.get("task_id", ""))
            findings.append(
                ReviewFinding(
                    task_id=task_id if task_id in valid_ids else "",
                    severity=str(item.get("severity", "medium")).lower(),
                    issue=str(item.get("issue", "")),
                    required_change=str(item.get("required_change", "")),
                    reviewer=definition.id,
                )
            )
        return ReviewReport(
            verdict=verdict,
            summary=str(data.get("summary", "")),
            findings=findings,
            reviewer=definition.id,
            usage=usage,
        )

    def _merge(self, reports: Sequence[ReviewReport]) -> ReviewReport:
        """Worst verdict wins; findings are concatenated, worst severity first."""
        if not reports:
            return ReviewReport(verdict=Verdict.APPROVE, summary="no reviews were produced")

        worst = max(reports, key=lambda r: _SEVERITY_ORDER.index(r.verdict))
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        findings = sorted(
            (f for report in reports for f in report.findings),
            key=lambda f: order.get(f.severity, 2),
        )
        usage = Usage()
        for report in reports:
            usage = usage + report.usage

        return ReviewReport(
            verdict=worst.verdict,
            summary=" | ".join(f"{r.reviewer}: {r.summary}" for r in reports if r.summary),
            findings=findings,
            reviewer=", ".join(r.reviewer for r in reports),
            usage=usage,
        )


def _may_block(definition: AgentDefinition) -> bool:
    """True only for the Security Reviewer itself."""
    slug = definition.id.rsplit("/", 1)[-1]
    return "security" in slug and "review" in slug


def _verdict(value: str) -> Verdict:
    normalized = value.strip().lower().replace(" ", "_").replace("-", "_")
    aliases = {
        "approved": Verdict.APPROVE,
        "approve_with_conditions": Verdict.APPROVE_WITH_CHANGES,
        "changes_requested": Verdict.REVISE,
        "blocked": Verdict.BLOCK,
        "rejected": Verdict.REJECT,
    }
    if normalized in aliases:
        return aliases[normalized]
    try:
        return Verdict(normalized)
    except ValueError:
        return Verdict.ESCALATE
