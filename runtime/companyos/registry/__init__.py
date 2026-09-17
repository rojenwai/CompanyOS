"""Agent discovery: Markdown specs in, typed definitions out."""

from .capabilities import TAXONOMY, extract, known_capabilities, namespace, normalize
from .definition import SECTION_NAMES, AgentDefinition, AgentKind
from .parser import parse_agent_spec
from .registry import AgentRegistry

__all__ = [
    "TAXONOMY",
    "SECTION_NAMES",
    "AgentDefinition",
    "AgentKind",
    "AgentRegistry",
    "extract",
    "known_capabilities",
    "namespace",
    "normalize",
    "parse_agent_spec",
]
