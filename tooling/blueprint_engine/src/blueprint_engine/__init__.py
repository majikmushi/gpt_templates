"""Blueprint/template representation engine."""

__version__ = "0.3.0"

from .engine import BlueprintEngine
from .mermaid_runtime import MermaidRuntimeBridge, MermaidRuntimeError, MermaidRuntimeUnavailable
from .models import CompareResult, MatchResult, TransformResult, ValidationIssue, ValidationResult
from .source_provenance import check_git_source

__all__ = [
    "BlueprintEngine",
    "ValidationIssue",
    "ValidationResult",
    "TransformResult",
    "MatchResult",
    "CompareResult",
    "MermaidRuntimeBridge",
    "MermaidRuntimeError",
    "MermaidRuntimeUnavailable",
    "check_git_source",
]
