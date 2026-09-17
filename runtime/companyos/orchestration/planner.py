"""The Planner: objective in, execution plan out.

Runs the agent described by ``ai/orchestration/planner.md`` -- its mission,
workflow, and quality standards become the system prompt, so the plan the
runtime produces is the plan that spec describes.
"""

from __future__ import annotations

from typing import Any, Mapping

from .. import purposes
from ..config import RuntimeConfig
from ..errors import ProviderError
from ..memory.store import MemoryStore
from ..observability import EventBus, EventType
from ..providers import Message, Provider, extract_json
from ..registry import AgentRegistry
from ..registry import capabilities as caps
from .prompts import json_instruction, kernel_system_prompt, untrusted

_PLAN_SCHEMA = """{
  "objective": "one sentence restating what must be achieved",
  "success_criteria": ["how we will know it is done"],
  "strategy": "how the work is split and why",
  "required_capabilities": ["dotted capability tags, most important first"],
  "divisions": ["divisions that should be involved"],
  "risks": ["what could make this plan wrong"],
  "parallelizable": true
}"""


class Planner:
    """Turns a user request into a structured plan."""

    AGENT_ID = "orchestration/planner"

    def __init__(
        self,
        registry: AgentRegistry,
        provider: Provider,
        config: RuntimeConfig,
        bus: EventBus,
        memory: MemoryStore | None = None,
    ) -> None:
        self.registry = registry
        self.provider = provider
        self.config = config
        self.bus = bus
        self.memory = memory
        self.definition = registry.get(self.AGENT_ID)

    async def plan(self, request: str, *, run_id: str) -> tuple[dict, Any]:
        """Return ``(plan, usage)``.

        A provider failure or unparsable answer degrades to a minimal
        single-capability plan rather than failing the run; the event stream
        records that it happened.
        """
        system = kernel_system_prompt(
            self.definition,
            "Produce an execution plan. Name the capabilities the work needs, not "
            "the agents -- agent selection happens downstream from your capabilities.",
        )
        user = "\n\n".join(
            [
                "Plan the following request.",
                untrusted("user-request", request),
                self._vocabulary(),
                self._memory_hint(request),
                json_instruction(_PLAN_SCHEMA),
            ]
        )

        try:
            completion = await self.provider.complete(
                system=system,
                messages=[Message("user", user)],
                purpose=purposes.PLAN,
                context={"request": request, "run_id": run_id},
            )
            plan = self._normalize(extract_json(completion.text), request)
            usage = completion.usage
        except (ProviderError, ValueError, TypeError) as exc:
            self.bus.emit(
                EventType.PLAN_CREATED,
                run_id=run_id,
                agent_id=self.AGENT_ID,
                message=f"planner fell back to capability extraction: {exc}",
                data={"degraded": True},
            )
            plan = self._fallback(request)
            from ..models import Usage

            usage = Usage()

        self.bus.emit(
            EventType.PLAN_CREATED,
            run_id=run_id,
            agent_id=self.AGENT_ID,
            message=plan["objective"][:120],
            data={
                "required_capabilities": plan["required_capabilities"],
                "divisions": plan["divisions"],
                "parallelizable": plan["parallelizable"],
            },
        )
        return plan, usage

    # -- prompt pieces ---------------------------------------------------------

    def _vocabulary(self) -> str:
        return (
            "Capability vocabulary (prefer these tags; a free-form tag is accepted "
            "and matched by text similarity):\n"
            + ", ".join(caps.known_capabilities())
            + "\n\nDivisions available: "
            + ", ".join(self.registry.divisions)
        )

    def _memory_hint(self, request: str) -> str:
        if self.memory is None:
            return ""
        records = self.memory.retrieve(request, k=3)
        if not records:
            return "Organizational memory: no reliable source for this request."
        body = "\n\n".join(f"[{r.source}]\n{r.text[:500]}" for r in records)
        return "Relevant organizational memory:\n" + untrusted("memory", body)

    # -- normalization ---------------------------------------------------------

    def _normalize(self, data: Any, request: str) -> dict:
        if not isinstance(data, Mapping):
            raise ValueError("plan is not an object")
        required = [
            caps.normalize(c)
            for c in (data.get("required_capabilities") or [])
            if isinstance(c, str) and c.strip()
        ]
        if not required:
            required = self._detect(request)
        return {
            "objective": str(data.get("objective") or request).strip(),
            "success_criteria": [str(s) for s in (data.get("success_criteria") or [])],
            "strategy": str(data.get("strategy") or ""),
            "required_capabilities": required,
            "divisions": [str(d) for d in (data.get("divisions") or [])]
            or sorted(caps.divisions_for(required)),
            "risks": [str(r) for r in (data.get("risks") or [])],
            "parallelizable": bool(data.get("parallelizable", True)),
        }

    def _fallback(self, request: str) -> dict:
        required = self._detect(request)
        return {
            "objective": request.strip(),
            "success_criteria": ["The request is answered with a reviewed deliverable"],
            "strategy": "Capability extraction fallback: the planner model was unavailable.",
            "required_capabilities": required,
            "divisions": sorted(caps.divisions_for(required)),
            "risks": ["Plan was derived without a model; coverage may be incomplete"],
            "parallelizable": True,
            "degraded": True,
        }

    @staticmethod
    def _detect(request: str) -> list[str]:
        scores = caps.extract(request)
        ranked = [c for c, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))]
        if not ranked:
            return ["operations.process"]
        return caps.expand(ranked[:6], target=4)
