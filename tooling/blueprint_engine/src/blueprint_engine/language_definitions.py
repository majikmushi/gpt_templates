from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .models import ValidationResult


def _schema_validate(
    value: dict[str, Any],
    schema_path: str | Path,
    target: str,
) -> ValidationResult:
    result = ValidationResult(target)
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(value), key=lambda e: list(e.absolute_path)):
        path = ".".join(str(part) for part in err.absolute_path) or None
        result.add("error", f"{target}.schema", err.message, path)
    return result


def validate_language_definition(
    value: dict[str, Any],
    schema_path: str | Path,
) -> ValidationResult:
    result = _schema_validate(value, schema_path, "language-definition")
    if not result.ok:
        return result

    source_ids = [source.get("adapter_id") for source in value.get("sources", [])]
    if len(source_ids) != len(set(source_ids)):
        result.add(
            "error",
            "language-definition.source-duplicate",
            "Source adapter IDs must be unique within a language definition",
        )

    if value.get("status") not in {"scaffold-unpinned", "planned"}:
        if not value.get("provenance"):
            result.add(
                "warning",
                "language-definition.provenance-missing",
                "Implemented language definitions should record provenance",
            )
    return result


def validate_specification_source_adapter(
    value: dict[str, Any],
    schema_path: str | Path,
) -> ValidationResult:
    result = _schema_validate(value, schema_path, "specification-source-adapter")
    if not result.ok:
        return result

    if value.get("status") == "implemented" and (value.get("extractor") or {}).get("mode") == "planned":
        result.add(
            "error",
            "specification-source-adapter.status",
            "An implemented source adapter cannot have extractor.mode=planned",
        )
    return result


def load_language_registry(repository_root: str | Path) -> dict[str, Any]:
    path = Path(repository_root) / "language-definitions/registry.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_language_definition(
    repository_root: str | Path,
    definition_id: str,
) -> dict[str, Any]:
    root = Path(repository_root)
    registry = load_language_registry(root)
    for entry in registry.get("definitions", []):
        if entry.get("id") == definition_id:
            path = root / entry["path"]
            return yaml.safe_load(path.read_text(encoding="utf-8"))
    raise KeyError(f"Unknown language definition {definition_id!r}")
