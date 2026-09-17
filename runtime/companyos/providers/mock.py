"""A deterministic, offline provider.

Two jobs:

1. **Tests.** Script exact responses per orchestration step and assert on the
   prompts the runtime actually sent (``provider.calls``). No network, no keys.
2. **Offline demo.** With no script, a small rule-based brain answers each step
   plausibly, so ``companyos run --provider mock`` exercises the *real*
   orchestration path -- real registry, real selection, real DAG scheduling,
   real reviewer loop -- with a fake model behind it.

Its prose output is explicitly labelled as simulated. The point is to exercise
the machinery, never to pass for a model's answer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence

from .. import purposes
from ..config import ProviderConfig
from ..models import Usage
from ..registry import capabilities as caps
from . import Completion, Message, Provider, ToolSpec, estimate_tokens

#: Capability namespaces that produce inputs others consume. Tasks are layered
#: by tier, which is what gives the offline demo a real DAG (parallel within a
#: tier, sequential across tiers) instead of a flat fan-out.
_TIERS: Mapping[str, int] = {
    "research": 0,
    "data": 0,
    "people": 0,
    "security": 1,
    "engineering": 1,
    "ai": 1,
    "design": 1,
    "product": 1,
    "hardware": 1,
    "legal": 1,
    "finance": 1,
    "marketing": 1,
    "sales": 1,
    "customer": 1,
    "devops": 2,
    "operations": 2,
    "docs": 2,
    "strategy": 2,
    "investor": 2,
}
_DEFAULT_TIER = 1


@dataclass
class RecordedCall:
    """One provider invocation, kept so tests can assert on what was sent."""

    purpose: str
    system: str
    messages: tuple[Message, ...]
    context: Mapping[str, Any] = field(default_factory=dict)
    tools: tuple[str, ...] = ()

    @property
    def prompt(self) -> str:
        """Everything the model saw, for context-isolation assertions."""
        return self.system + "\n" + "\n".join(m.content for m in self.messages)


#: A scripted response: literal text, or a callable given the RecordedCall.
Scripted = str | Mapping[str, Any] | Callable[[RecordedCall], "str | Mapping[str, Any]"]


class MockProvider(Provider):
    """Deterministic provider with an optional per-purpose script."""

    name = "mock"
    default_model = "mock-1"

    def __init__(
        self,
        config: ProviderConfig | None = None,
        *,
        script: Mapping[str, Scripted | Sequence[Scripted]] | None = None,
        fail_agents: Sequence[str] = (),
        revise_once: bool = False,
        latency_s: float = 0.0,
    ) -> None:
        super().__init__(config or ProviderConfig(name="mock"))
        self.script: dict[str, list[Scripted]] = {}
        for purpose, value in (script or {}).items():
            self.script[purpose] = list(value) if isinstance(value, (list, tuple)) else [value]
        self.fail_agents = set(fail_agents)
        """Agent ids whose EXECUTE call raises, to exercise failure handling."""

        self.revise_once = revise_once
        """First review asks for revisions; later ones approve."""

        self.latency_s = latency_s
        """Simulated think time, used to prove tasks really overlap."""

        self.calls: list[RecordedCall] = []
        self._reviews = 0

    # -- Provider --------------------------------------------------------------

    async def complete(
        self,
        *,
        system: str,
        messages: list[Message],
        tools: list[ToolSpec] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        purpose: str = "",
        context: Mapping[str, Any] | None = None,
    ) -> Completion:
        call = RecordedCall(
            purpose=purpose,
            system=system,
            messages=tuple(messages),
            context=dict(context or {}),
            tools=tuple(t.name for t in (tools or ())),
        )
        self.calls.append(call)

        if self.latency_s:
            import asyncio

            await asyncio.sleep(self.latency_s)

        agent_id = str(call.context.get("agent_id", ""))
        if purpose == purposes.EXECUTE and agent_id in self.fail_agents:
            from ..errors import ProviderError

            raise ProviderError(f"simulated provider failure for {agent_id}")

        text = self._respond(call)
        prompt_chars = len(call.prompt)
        return Completion(
            text=text,
            usage=Usage(estimate_tokens(" " * prompt_chars), estimate_tokens(text)),
            provider=self.name,
            model=self.model,
            stop_reason="end_turn",
        )

    # -- response selection ----------------------------------------------------

    def _respond(self, call: RecordedCall) -> str:
        queue = self.script.get(call.purpose)
        if queue:
            scripted = queue.pop(0) if len(queue) > 1 else queue[0]
            value = scripted(call) if callable(scripted) else scripted
            return value if isinstance(value, str) else json.dumps(value)

        handler = {
            purposes.PLAN: self._plan,
            purposes.DECOMPOSE: self._decompose,
            purposes.EXECUTE: self._execute,
            purposes.REVIEW: self._review,
            purposes.SYNTHESIZE: self._synthesize,
        }.get(call.purpose, self._execute)
        return handler(call)

    # -- the rule-based brain --------------------------------------------------

    @staticmethod
    def _request_of(call: RecordedCall) -> str:
        return str(call.context.get("request") or call.messages[-1].content if call.messages else "")

    def _ranked_capabilities(self, text: str, limit: int) -> list[str]:
        scores = caps.extract(text)
        ranked = [cap for cap, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))]
        if not ranked:
            return ["operations.process"]
        # A real planner reasons about coverage; this stand-in widens within the
        # disciplines that matched so a terse request still staffs a team.
        return caps.expand(ranked[:limit], target=min(limit, 4))

    def _plan(self, call: RecordedCall) -> str:
        request = self._request_of(call)
        selected = self._ranked_capabilities(request, 8)
        divisions = sorted(caps.divisions_for(selected))
        return json.dumps(
            {
                "objective": request.strip().rstrip(".") or "Fulfil the request",
                "success_criteria": [
                    "Every workstream produces a concrete, reviewable deliverable",
                    "Findings are supported by evidence, not assertion",
                ],
                "strategy": (
                    "Split the objective across the divisions that own the required "
                    "capabilities, run independent workstreams in parallel, and review "
                    "the combined result before synthesis."
                ),
                "required_capabilities": selected,
                "divisions": divisions,
                "risks": ["Capability coverage is inferred from the request wording"],
                "parallelizable": True,
            }
        )

    def _decompose(self, call: RecordedCall) -> str:
        request = str(call.context.get("request", ""))
        plan = call.context.get("plan") or {}
        selected = list(plan.get("required_capabilities") or []) or self._ranked_capabilities(
            request, 6
        )
        max_tasks = int(call.context.get("max_tasks", 6))

        # One task per capability, deepest-signal first, capped by the budget.
        chosen = selected[:max_tasks]
        by_tier: dict[int, list[dict]] = {}
        for index, capability in enumerate(chosen, start=1):
            tier = _TIERS.get(caps.namespace(capability), _DEFAULT_TIER)
            by_tier.setdefault(tier, []).append(
                {
                    "id": f"t{index}",
                    "objective": self._objective_for(capability, request),
                    "description": (
                        f"Own the {capability.replace('.', ' ')} dimension of: {request.strip()}"
                    ),
                    "required_capabilities": [capability],
                    "priority": tier + 1,
                    "dependencies": [],
                    "acceptance_criteria": [
                        f"States concrete {caps.namespace(capability)} conclusions",
                        "Names assumptions and open questions explicitly",
                    ],
                }
            )

        # Each tier depends on every task in the tier before it: parallel within
        # a wave, strictly sequential across waves.
        tiers = sorted(by_tier)
        tasks: list[dict] = []
        previous: list[str] = []
        for tier in tiers:
            current = by_tier[tier]
            for task in current:
                task["dependencies"] = list(previous)
            tasks.extend(current)
            previous = [t["id"] for t in current]

        return json.dumps({"tasks": tasks})

    @staticmethod
    def _objective_for(capability: str, request: str) -> str:
        head, _, tail = capability.partition(".")
        subject = (tail or head).replace("-", " ")
        return f"{subject.capitalize()} workstream for: {request.strip().rstrip('.')}"

    def _execute(self, call: RecordedCall) -> str:
        agent = call.context.get("agent_name") or call.context.get("agent_id") or "Agent"
        objective = call.context.get("objective", "the assigned task")
        criteria = call.context.get("acceptance_criteria") or []
        findings = call.context.get("findings") or []

        lines = [
            f"[simulated output - mock provider, no model was called]",
            "",
            f"## {agent}: {objective}",
            "",
            "### Position",
            f"This workstream is owned end to end by {agent}, which is accountable for the "
            f"deliverable named in the task objective.",
            "",
            "### Findings",
        ]
        for criterion in criteria or ["Deliverable produced"]:
            lines.append(f"- {criterion}: addressed.")
        if findings:
            lines += ["", "### Revisions applied"]
            lines += [f"- {f.get('required_change') or f.get('issue')}" for f in findings]
        lines += [
            "",
            "### Assumptions",
            "- Generated without a live model; treat every specific as a placeholder.",
        ]
        return "\n".join(lines)

    def _review(self, call: RecordedCall) -> str:
        self._reviews += 1
        task_ids = list(call.context.get("task_ids") or [])
        if self.revise_once and self._reviews == 1 and task_ids:
            return json.dumps(
                {
                    "verdict": "revise",
                    "summary": "First pass is thin on evidence; one workstream needs another turn.",
                    "findings": [
                        {
                            "task_id": task_ids[0],
                            "severity": "medium",
                            "issue": "Conclusions are asserted without supporting evidence.",
                            "required_change": "Cite the evidence behind each conclusion.",
                        }
                    ],
                }
            )
        return json.dumps(
            {
                "verdict": "approve",
                "summary": "Workstreams are consistent and each acceptance criterion is addressed.",
                "findings": [],
            }
        )

    def _synthesize(self, call: RecordedCall) -> str:
        outputs = call.context.get("task_summaries") or []
        lines = [
            "[simulated synthesis - mock provider, no model was called]",
            "",
            f"## Result: {call.context.get('request', 'the request')}",
            "",
        ]
        for item in outputs:
            lines.append(f"- **{item.get('agent', 'agent')}** - {item.get('objective', '')}")
        lines += ["", "All workstreams completed and passed review."]
        return "\n".join(lines)
