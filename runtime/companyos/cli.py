"""Command line interface.

The runtime is fully usable from here and from :class:`companyos.Orchestrator`;
no UI is required, and none of the orchestration logic lives in this module.

    companyos run "Design and implement authentication for a web application."
    companyos agents list --division security
    companyos select "threat model the login flow" -c security.threat-modeling
    companyos map .companyos/runs/run_ab12cd34.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .config import ProviderConfig, RuntimeConfig, RuntimeLimits, find_repo_root
from .errors import CompanyOSError
from .observability import ConsoleSink, EventBus
from .orchestration import Orchestrator, render_tree
from .orchestration.selector import AgentSelector
from .registry import AgentRegistry, known_capabilities


# --- argument parsing ---------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="companyos",
        description="Dynamic multi-agent orchestration over the CompanyOS agent specs.",
    )
    parser.add_argument("--version", action="version", version=f"companyos {__version__}")
    parser.add_argument("--root", help="CompanyOS repository root (default: auto-detect)")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="orchestrate a request end to end")
    run.add_argument("request", help="what you want the company to do")
    run.add_argument("--provider", default="mock",
                     help="mock (offline, default) | anthropic | openai | local")
    run.add_argument("--model", default="", help="model id for the chosen provider")
    run.add_argument("--base-url", default="", help="override the provider endpoint")
    run.add_argument("--max-agents", type=int, help="cap on spawned agent instances")
    run.add_argument("--max-parallel", type=int, help="cap on concurrent instances")
    run.add_argument("--max-iterations", type=int, help="plan/execute/review cycles")
    run.add_argument("--task-timeout", type=float, help="seconds per agent instance")
    run.add_argument("--run-timeout", type=float, help="seconds for the whole run")
    run.add_argument("--save", metavar="FILE", help="write the full run record as JSON")
    run.add_argument("--map", metavar="FILE", dest="map_file",
                     help="write the Agent Map as JSON")
    run.add_argument("--json", action="store_true", help="print the run record instead of prose")
    run.add_argument("--no-trace", action="store_true", help="do not write a JSONL trace")
    run.add_argument("-v", "--verbose", action="store_true", help="stream every event")

    agents = sub.add_parser("agents", help="inspect the agent registry")
    agents_sub = agents.add_subparsers(dest="agents_command", required=True)
    listing = agents_sub.add_parser("list", help="list discovered agent definitions")
    listing.add_argument("--division")
    listing.add_argument("--capability")
    listing.add_argument("--kind", choices=["specialist", "executive", "orchestration", "reviewer"])
    listing.add_argument("--json", action="store_true")
    show = agents_sub.add_parser("show", help="show one agent definition")
    show.add_argument("agent_id")
    show.add_argument("--json", action="store_true")

    select = sub.add_parser("select", help="explain which agents a task would select")
    select.add_argument("task", help="task text")
    select.add_argument("-c", "--capability", action="append", default=[],
                        help="required capability (repeatable)")
    select.add_argument("-n", "--top", type=int, default=8)
    select.add_argument("--json", action="store_true")

    capabilities = sub.add_parser("capabilities", help="list the capability vocabulary")
    capabilities.add_argument("--json", action="store_true")

    map_cmd = sub.add_parser("map", help="render a saved run record or Agent Map")
    map_cmd.add_argument("file")

    sub.add_parser("doctor", help="check the runtime can find specs and a provider")
    return parser


# --- commands -----------------------------------------------------------------


def cmd_run(args: argparse.Namespace) -> int:
    limits = RuntimeLimits(
        **{
            key: value
            for key, value in {
                "max_agents": args.max_agents,
                "max_parallel": args.max_parallel,
                "max_iterations": args.max_iterations,
                "task_timeout_s": args.task_timeout,
                "run_timeout_s": args.run_timeout,
            }.items()
            if value is not None
        }
    )
    config = RuntimeConfig(
        root=_root(args),
        provider=ProviderConfig(
            name=args.provider, model=args.model, base_url=args.base_url
        ),
        limits=limits,
    )

    bus = EventBus([ConsoleSink(verbose=args.verbose)])
    orchestrator = Orchestrator(config, bus=bus, trace_to_disk=not args.no_trace)

    print(f"CompanyOS runtime | {len(orchestrator.registry)} agent definitions | "
          f"provider {orchestrator.provider.name}/{orchestrator.provider.model}",
          file=sys.stderr)
    print(file=sys.stderr)

    run = asyncio.run(orchestrator.run(args.request))
    agent_map = orchestrator.agent_map(run)

    for path, payload in ((args.save, run.to_dict()), (args.map_file, agent_map)):
        if not path:
            continue
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(run.to_dict(), indent=2))
        return 0 if run.status.value == "completed" else 1

    print()
    print("AGENT MAP")
    print("-" * 100)
    print(render_tree(agent_map))
    print()
    print("RESULT")
    print("-" * 100)
    print(run.final_output or "(no output)")
    print()
    _print_summary(run, agent_map)
    return 0 if run.status.value == "completed" else 1


def _print_summary(run, agent_map: dict) -> None:
    usage = run.usage
    print(
        f"status={run.status.value} | agents spawned={run.budget.get('agents_spawned', 0)} "
        f"| tasks={len(run.graph)} | reviews={len(run.reviews)} "
        f"| tokens={usage.total} | {run.duration_s:.2f}s"
    )
    if run.requires_human_approval:
        print(f"HUMAN APPROVAL REQUIRED: {run.approval_reason}")
    for error in run.errors:
        print(f"error: {error}")


def cmd_agents(args: argparse.Namespace) -> int:
    registry = AgentRegistry.discover(_root(args))
    if args.agents_command == "show":
        definition = registry.resolve(args.agent_id)
        if args.json:
            print(json.dumps(definition.to_dict(full=True), indent=2))
            return 0
        print(f"{definition.name}  [{definition.id}]")
        print(f"  division   : {definition.division}")
        print(f"  kind       : {definition.kind}")
        print(f"  reports to : {definition.reports_to or registry.supervisor_for(definition)}")
        print(f"  executes   : {definition.can_execute_independently}")
        print(f"  tools      : {', '.join(definition.tools) or 'none mapped'}")
        print(f"  spec       : {definition.source_path}")
        print(f"  capabilities: {', '.join(definition.capabilities[:12])}")
        print()
        print(f"  mission    : {definition.mission[:400]}")
        return 0

    found = registry.agents
    if args.division:
        found = [d for d in found if d.division == args.division]
    if args.kind:
        found = [d for d in found if d.kind == args.kind]
    if args.capability:
        wanted = {d.id for d in registry.with_capability(args.capability)}
        found = [d for d in found if d.id in wanted]

    if args.json:
        print(json.dumps([d.to_dict() for d in found], indent=2))
        return 0
    for definition in found:
        flag = " " if definition.can_execute_independently else "*"
        print(f"{flag} {definition.id:52s} {definition.kind:14s} {definition.name}")
    print(f"\n{len(found)} agent definition(s). '*' delegates rather than executes.")
    return 0


def cmd_select(args: argparse.Namespace) -> int:
    registry = AgentRegistry.discover(_root(args))
    selector = AgentSelector(registry)
    ranked = selector.rank(args.capability, args.task)[: args.top]
    if args.json:
        print(json.dumps([c.to_dict() for c in ranked], indent=2))
        return 0
    if not ranked:
        print("no agent scored above zero for that task")
        return 1
    print(f"{'score':>7}  {'agent':52s} matched capabilities")
    for candidate in ranked:
        print(
            f"{candidate.score:7.2f}  {candidate.agent_id:52s} "
            f"{', '.join(candidate.matched) or '-'}"
        )
    return 0


def cmd_capabilities(args: argparse.Namespace) -> int:
    names = known_capabilities()
    if args.json:
        print(json.dumps(names, indent=2))
        return 0
    for name in names:
        print(name)
    print(f"\n{len(names)} capabilities in the taxonomy.")
    return 0


def cmd_map(args: argparse.Namespace) -> int:
    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    if "nodes" not in data:  # a full run record: rebuild the map from it
        print("file is a run record, not an Agent Map; re-run with --map to export one")
        return 1
    print(render_tree(data))
    counts = data.get("counts", {})
    print(
        f"\n{counts.get('nodes', 0)} nodes | {counts.get('spawned', 0)} spawned "
        f"| {counts.get('completed', 0)} completed | {counts.get('failed', 0)} failed"
    )
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    root = _root(args)
    print(f"root      : {root}")
    registry = AgentRegistry.discover(root)
    stats = registry.stats()
    print(f"registry  : {stats['agents']} agents across {stats['divisions']} divisions")
    print(f"            {stats['by_kind']}")
    print(f"executable: {len(registry.executable())}")
    print(f"reviewers : {', '.join(r.id for r in registry.reviewers())}")
    print(f"memory    : {root / 'ai' / 'memory'}")

    from .memory.filestore import FileMemoryStore

    store = FileMemoryStore(root)
    print(f"            {len(store.stores)} memory stores indexed")
    print(f"traces    : {RuntimeConfig(root=root).traces_dir}")
    return 0


# --- entry point --------------------------------------------------------------


def _root(args: argparse.Namespace) -> Path:
    return Path(args.root).resolve() if args.root else find_repo_root()


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    handlers = {
        "run": cmd_run,
        "agents": cmd_agents,
        "select": cmd_select,
        "capabilities": cmd_capabilities,
        "map": cmd_map,
        "doctor": cmd_doctor,
    }
    try:
        return handlers[args.command](args)
    except CompanyOSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:  # pragma: no cover
        print("\ninterrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
