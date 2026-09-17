"""Final synthesis.

The entry agent (the CEO agent, by default) composes one answer from the
reviewed branch outputs. It is the only stage that sees everything -- and even
here every branch output is presented as untrusted data.

If the provider is unavailable, synthesis degrades to a deterministic assembly
of the branch outputs rather than losing the work.
"""

from __future__ import annotations

from typing import Any, Mapping

from .. import purposes
from ..config import RuntimeConfig
from ..errors import ProviderError
from ..models import ReviewReport, Usage
from ..observability import EventBus, EventType
from ..providers import Message, Provider
from ..registry import AgentRegistry
from ..status import Verdict
from .aggregator import Aggregation
from .prompts import kernel_system_prompt, untrusted


class Synthesizer:
    """Composes the final response."""

    def __init__(
        self,
        registry: AgentRegistry,
        provider: Provider,
        config: RuntimeConfig,
        bus: EventBus,
        entry_agent_id: str | None = None,
    ) -> None:
        self.registry = registry
        self.provider = provider
        self.config = config
        self.bus = bus
        self.definition = registry.get(entry_agent_id or registry.ceo_id)

    async def synthesize(
        self,
        request: str,
        aggregation: Aggregation,
        review: ReviewReport | None,
        *,
        run_id: str,
        plan: Mapping[str, Any] | None = None,
    ) -> tuple[str, Usage]:
        self.bus.emit(
            EventType.SYNTHESIS_STARTED,
            run_id=run_id,
            agent_id=self.definition.id,
            message=f"synthesizing {len(aggregation.successes)} branch result(s)",
        )

        if aggregation.empty:
            return self._nothing_produced(aggregation), Usage()

        system = kernel_system_prompt(
            self.definition,
            "Compose the final answer to the user from the reviewed work below. "
            "Do not invent anything the specialists did not produce. State plainly "
            "what is missing or unresolved.",
        )
        user = "\n\n".join(
            part
            for part in [
                "Original request:",
                untrusted("user-request", request),
                f"Objective: {plan.get('objective')}" if plan else "",
                "Reviewed deliverables:",
                aggregation.render(include_failures=False),
                self._review_note(review),
                self._gap_note(aggregation),
                "Write the answer for the user. Attribute each part to the agent that "
                "produced it. Be direct; no preamble.",
            ]
            if part
        )

        try:
            completion = await self.provider.complete(
                system=system,
                messages=[Message("user", user)],
                purpose=purposes.SYNTHESIZE,
                context={
                    "run_id": run_id,
                    "agent_id": self.definition.id,
                    "request": request,
                    "task_summaries": aggregation.summaries(),
                },
            )
            return completion.text, completion.usage
        except ProviderError as exc:
            return self._assemble(request, aggregation, review, str(exc)), Usage()

    # -- prompt pieces ---------------------------------------------------------

    @staticmethod
    def _review_note(review: ReviewReport | None) -> str:
        if review is None:
            return ""
        verdict = getattr(review.verdict, "value", str(review.verdict))
        note = f"Review verdict: {verdict}. {review.summary}"
        if review.findings:
            note += "\nUnresolved findings:\n" + "\n".join(
                f"- [{f.severity}] {f.issue}" for f in review.findings
            )
        return note

    @staticmethod
    def _gap_note(aggregation: Aggregation) -> str:
        gaps = aggregation.gaps()
        if not gaps:
            return ""
        return "Work that did not complete (say so in the answer):\n- " + "\n- ".join(gaps)

    # -- degraded paths --------------------------------------------------------

    @staticmethod
    def _nothing_produced(aggregation: Aggregation) -> str:
        lines = ["No deliverable was produced: every workstream failed or was skipped.", ""]
        lines += [f"- {gap}" for gap in aggregation.gaps()]
        return "\n".join(lines)

    def _assemble(
        self,
        request: str,
        aggregation: Aggregation,
        review: ReviewReport | None,
        reason: str,
    ) -> str:
        """Deterministic fallback: concatenate the branches, attributed."""
        lines = [
            f"# {request.strip()}",
            "",
            f"_Synthesis model unavailable ({reason}); "
            f"branch outputs are reproduced verbatim below._",
            "",
        ]
        for task, result in aggregation.successes:
            lines += [
                f"## {task.objective}",
                f"*{result.agent_name or result.agent_id}*",
                "",
                result.output,
                "",
            ]
        if review is not None and getattr(review.verdict, "value", "") != Verdict.APPROVE.value:
            lines += [f"> Review verdict: {review.verdict}. {review.summary}", ""]
        for gap in aggregation.gaps():
            lines.append(f"> Incomplete: {gap}")
        return "\n".join(lines)
