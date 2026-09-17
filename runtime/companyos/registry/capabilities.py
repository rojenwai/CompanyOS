"""Capability taxonomy and extraction.

Agent specs are prose. The runtime needs comparable tags so selection can be
capability-driven rather than a hardcoded ``if task == X: use agent Y`` table.

The taxonomy below maps a dotted capability onto the phrases that signal it.
Extraction runs over an agent's own spec text, so **adding a new Markdown agent
spec is enough to make it selectable** -- no code change, no registration step.
The same extractor runs over the user's request, which is what lets the two be
matched.
"""

from __future__ import annotations

import re
from typing import Iterable, Mapping

#: capability -> signal phrases. Order does not matter; matches are additive.
TAXONOMY: Mapping[str, tuple[str, ...]] = {
    # --- engineering ---------------------------------------------------------
    "engineering.architecture": (
        "architecture", "service boundar", "system design", "adr", "design doc",
        "technical strategy", "scalab", "build-vs-buy", "build vs buy",
    ),
    "engineering.backend": (
        "server-side", "backend", "back-end", "endpoint", "service", "api implementation",
        "messaging", "caching", "authorization", "authentication",
    ),
    "engineering.frontend": (
        "frontend", "front-end", "ui implementation", "component", "browser",
        "client-side", "web app",
    ),
    "engineering.mobile": ("mobile", "ios", "android", "app store"),
    "engineering.api": ("api design", "api contract", "rest", "graphql", "openapi", "versioning"),
    "engineering.database": (
        "database", "schema", "migration", "query", "index", "sql", "data model",
        "persistence", "storage",
    ),
    "engineering.performance": (
        "performance", "latency", "throughput", "profil", "benchmark", "load test", "optimi",
    ),
    "engineering.testing": (
        "test", "coverage", "regression", "qa", "unit test", "integration test",
    ),
    "engineering.refactoring": ("refactor", "technical debt", "code smell", "cleanup"),
    "engineering.cloud": ("cloud", "aws", "gcp", "azure", "infrastructure", "terraform"),
    # --- security ------------------------------------------------------------
    "security.threat-modeling": (
        "threat model", "stride", "attack tree", "trust boundar", "attack surface",
    ),
    "security.controls": (
        "security control", "secure default", "hardening", "encryption", "secrets",
        "access control", "least privilege", "authentication", "authorization",
        "login", "session", "password", "oauth", "mfa", "credential",
    ),
    "security.vulnerability": (
        "vulnerabilit", "cve", "patch", "dependency scan", "static analysis", "owasp",
    ),
    "security.pentest": ("penetration test", "exploit", "red team", "pentest"),
    "security.compliance": (
        "compliance", "soc 2", "iso 27001", "gdpr", "hipaa", "audit", "privacy",
    ),
    # --- data ----------------------------------------------------------------
    "data.engineering": ("pipeline", "etl", "elt", "ingestion", "warehouse", "data engineer"),
    "data.analytics": ("analytics", "metric definition", "dashboard", "reporting", "dbt"),
    "data.science": ("statistic", "model training", "experiment", "hypothesis", "forecast"),
    "data.governance": ("data governance", "lineage", "data quality", "retention policy", "pii"),
    # --- ai ------------------------------------------------------------------
    "ai.architecture": ("ai architect", "rag", "retrieval-augmented", "inference", "llm system"),
    "ai.llm": ("prompt", "llm", "fine-tun", "context window", "token"),
    "ai.ml": ("machine learning", "training pipeline", "feature store", "model serving"),
    "ai.evaluation": ("eval", "benchmark suite", "hallucinat", "model card"),
    # --- product -------------------------------------------------------------
    "product.requirements": (
        "requirement", "user story", "acceptance criteria", "prd", "spec the feature",
    ),
    "product.prioritization": ("prioriti", "roadmap", "backlog", "rice", "trade-off"),
    "product.discovery": ("customer journey", "jobs to be done", "problem discovery", "mvp"),
    # --- design --------------------------------------------------------------
    "design.ux-research": ("ux research", "usability", "user interview", "user research"),
    "design.ui": ("visual design", "ui design", "layout", "typography", "mockup"),
    "design.interaction": ("interaction design", "flow", "prototype", "microcopy"),
    "design.system": ("design system", "design token", "component library"),
    "design.accessibility": ("accessibilit", "wcag", "screen reader", "a11y"),
    # --- research ------------------------------------------------------------
    "research.market": ("market", "tam", "sam", "som", "market siz", "industry trend"),
    "research.competitive": ("competitor", "competitive", "landscape", "positioning against"),
    "research.problem": (
        "problem discovery", "pain point", "recurring pain", "user need",
        "validate the problem", "jobs-to-be-done", "jtbd", "underserved",
    ),
    "research.opportunity": (
        "opportunity", "opportunity ranking", "prioritize opportunities",
        "significance score",
    ),
    # --- strategy ------------------------------------------------------------
    "strategy.business": ("business strategy", "moat", "differentiat", "strategic"),
    "strategy.pricing": ("pricing", "business model", "monetiz", "packaging", "unit economics"),
    "strategy.gtm": ("go-to-market", "gtm", "launch plan", "channel"),
    "strategy.fundraising": ("fundrais", "investor", "pitch", "valuation", "term sheet"),
    # --- devops --------------------------------------------------------------
    "devops.cicd": ("ci/cd", "pipeline", "build system", "continuous integration"),
    "devops.platform": ("platform", "kubernetes", "container", "developer experience"),
    "devops.reliability": ("reliability", "sre", "slo", "incident", "on-call", "uptime"),
    "devops.release": ("release", "deploy", "rollout", "rollback", "versioning"),
    # --- finance -------------------------------------------------------------
    "finance.planning": ("financial plan", "budget", "forecast", "runway", "burn"),
    "finance.accounting": ("accounting", "ledger", "close", "reconcil"),
    "finance.revenue": ("revenue", "billing", "invoice", "arr", "mrr", "subscription"),
    "finance.cost": ("cost optimi", "spend", "cogs", "cloud cost", "margin"),
    # --- legal ---------------------------------------------------------------
    "legal.contracts": ("contract", "msa", "sow", "negotiat", "terms of service"),
    "legal.ip": ("patent", "trademark", "intellectual property", "copyright"),
    "legal.compliance": ("regulat", "legal compliance", "licence", "license obligation"),
    "legal.privacy": ("privacy policy", "data protection", "dpa", "consent"),
    # --- people --------------------------------------------------------------
    "people.recruiting": ("recruit", "hiring", "candidate", "interview loop"),
    "people.onboarding": ("onboard", "ramp", "first week"),
    "people.performance": ("performance review", "career", "growth plan", "feedback cycle"),
    "people.culture": ("culture", "values", "engagement", "retention of staff"),
    # --- operations ----------------------------------------------------------
    "operations.project": ("project management", "schedule", "milestone", "critical path"),
    "operations.process": ("process", "workflow optimi", "sop", "efficiency"),
    "operations.vendor": ("vendor", "procurement", "supplier"),
    "operations.knowledge": ("knowledge management", "documentation index", "wiki"),
    # --- marketing / sales / cs ----------------------------------------------
    "marketing.content": ("content marketing", "blog", "editorial", "copywriting"),
    "marketing.seo": ("seo", "search ranking", "keyword"),
    "marketing.brand": ("brand", "communications", "messaging", "press"),
    "marketing.growth": ("growth", "funnel", "acquisition", "conversion rate", "campaign"),
    "sales.prospecting": ("prospect", "lead", "outbound", "pipeline generation"),
    "sales.account": ("account executive", "close the deal", "quota", "negotiation"),
    "sales.engineering": ("sales engineer", "demo", "proof of concept", "technical win"),
    "sales.dealdesk": ("deal desk", "discount", "quote", "approval of terms"),
    "customer.onboarding": ("customer onboarding", "time to value", "implementation"),
    "customer.support": ("support", "ticket", "troubleshoot", "sla response"),
    "customer.health": ("health score", "churn", "adoption", "usage signal"),
    "customer.expansion": ("renewal", "expansion", "upsell"),
    # --- documentation -------------------------------------------------------
    "docs.technical-writing": ("technical writ", "documentation", "guide", "tutorial"),
    "docs.api": ("api documentation", "reference doc", "changelog"),
    "docs.knowledge-base": ("knowledge base", "faq", "help center"),
    # --- hardware ------------------------------------------------------------
    "hardware.firmware": ("firmware", "embedded", "rtos", "driver"),
    "hardware.electrical": ("electrical", "pcb", "circuit", "schematic"),
    "hardware.mechanical": ("mechanical", "enclosure", "cad", "tolerance"),
    "hardware.test": ("hardware test", "bring-up", "validation rig"),
    # --- investor relations --------------------------------------------------
    "investor.reporting": ("investor report", "shareholder update", "board deck"),
    "investor.governance": ("board governance", "board meeting", "minutes"),
    "investor.captable": ("cap table", "equity", "option pool", "dilution"),
    # --- executive / orchestration -------------------------------------------
    "executive.direction": (
        "delegate", "set objective", "prioriti", "allocate resources", "strategic decision",
    ),
    "executive.review": ("review", "verdict", "approve", "quality bar", "sign-off"),
    "orchestration.planning": ("plan", "decompos", "subtask", "dependenc", "critical path"),
    "orchestration.memory": ("memory", "retrieval", "context assembl"),
}

#: Divisions that own each capability namespace, used as a soft selection prior.
NAMESPACE_DIVISIONS: Mapping[str, tuple[str, ...]] = {
    "engineering": ("engineering",),
    "security": ("security",),
    "data": ("data",),
    "ai": ("ai-engineering",),
    "product": ("product",),
    "design": ("design",),
    "research": ("research",),
    "strategy": ("strategy",),
    "devops": ("devops",),
    "finance": ("finance",),
    "legal": ("legal",),
    "people": ("hr",),
    "operations": ("operations",),
    "marketing": ("marketing",),
    "sales": ("sales",),
    "customer": ("customer-success",),
    "docs": ("documentation",),
    "hardware": ("hardware",),
    "investor": ("investor-relations",),
    "executive": ("executive", "orchestration"),
    "orchestration": ("orchestration",),
}

_WORD = re.compile(r"[a-z0-9][a-z0-9+.#-]*")


def normalize(capability: str) -> str:
    """Canonical form: lowercase, dots kept, spaces and underscores hyphenated."""
    cap = capability.strip().lower().replace("_", "-").replace(" ", "-")
    cap = re.sub(r"-{2,}", "-", cap)
    return cap.strip("-.")


def namespace(capability: str) -> str:
    """The leading segment of a dotted capability (``security.pentest`` -> ``security``)."""
    return normalize(capability).split(".", 1)[0]


def extract(text: str, *, threshold: int = 1) -> dict[str, int]:
    """Score every taxonomy capability against ``text``.

    Returns ``{capability: score}`` for capabilities scoring at least
    ``threshold``. Case-insensitive substring matching is deliberate: the specs
    are prose, and stemmed prefixes like ``vulnerabilit`` catch both singular
    and plural without a stemmer dependency.

    A match is weighted by how specific the phrase is -- its word count -- so
    "threat model" outweighs a bare "flow". Without that, every capability
    whose single-word signal happens to appear ties, and the tie falls to
    alphabetical order, which is meaningless.
    """
    lowered = text.lower()
    scores: dict[str, int] = {}
    for capability, phrases in TAXONOMY.items():
        score = sum(len(phrase.split()) for phrase in phrases if phrase in lowered)
        if score >= threshold:
            scores[capability] = score
    return scores


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens, used for the lexical half of selection scoring."""
    return _WORD.findall(text.lower())


def expand(selected: Iterable[str], *, target: int = 4) -> list[str]:
    """Broaden a thin capability set along the namespaces that already matched.

    A terse request ("is there a market for this?") produces one signal, which
    would staff one agent. Expansion covers the rest of the discipline that
    signal belongs to -- research.market pulls in competitive, problem, and
    opportunity analysis -- without inventing a namespace nothing matched.

    Only ever widens within matched namespaces, so it cannot drag an unrelated
    division into the plan.
    """
    out = list(dict.fromkeys(normalize(c) for c in selected if c))
    if len(out) >= target:
        return out[:target] if target > 0 else out

    for space in dict.fromkeys(namespace(c) for c in out):
        for capability in sorted(TAXONOMY):
            if len(out) >= target:
                return out
            if namespace(capability) == space and capability not in out:
                out.append(capability)
    return out


def divisions_for(capabilities: Iterable[str]) -> set[str]:
    """Divisions that plausibly own the given capabilities."""
    out: set[str] = set()
    for cap in capabilities:
        out.update(NAMESPACE_DIVISIONS.get(namespace(cap), ()))
    return out


def known_capabilities() -> list[str]:
    return sorted(TAXONOMY)
