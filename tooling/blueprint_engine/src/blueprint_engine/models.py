from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    code: str
    message: str
    path: str | None = None

@dataclass
class ValidationResult:
    target: str
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(i.severity == "error" for i in self.issues)

    def add(self, severity: str, code: str, message: str, path: str | None = None) -> None:
        self.issues.append(ValidationIssue(severity, code, message, path))

    def as_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "ok": self.ok,
            "issues": [i.__dict__ for i in self.issues],
        }

@dataclass
class TransformResult:
    target_format: str
    content: Any
    media_type: str
    transform_id: str
    fidelity: str
    losses: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class MatchResult:
    format_id: str
    score: float
    capability_levels: dict[str, str]
    partial: tuple[str, ...] = ()

@dataclass
class CompareResult:
    classification: str
    missing: list[str] = field(default_factory=list)
    extra: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def equivalent(self) -> bool:
        return self.classification in {"exact", "equivalent"}
