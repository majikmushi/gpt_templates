from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .models import ValidationResult


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _validate(value: dict[str, Any], schema_path: Path, target: str) -> ValidationResult:
    result = ValidationResult(target)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(value), key=lambda e: list(e.absolute_path)):
        path = ".".join(str(part) for part in error.absolute_path) or None
        result.add("error", f"{target}.schema", error.message, path)
    return result


def validate_framework_artifact(root: str | Path, value: dict[str, Any], artifact_kind: str) -> ValidationResult:
    root = Path(root)
    schemas = {
        "abstract-model": "abstract-model.schema.json",
        "representation-binding": "representation-binding.schema.json",
        "style-profile": "style-profile.schema.json",
        "style-binding": "style-binding.schema.json",
        "generation-request": "generation-request.schema.json",
    }
    if artifact_kind not in schemas:
        raise KeyError(f"Unknown framework artifact kind {artifact_kind!r}")
    return _validate(value, root / "schemas" / schemas[artifact_kind], artifact_kind)


def load_abstract_model(root: str | Path, model_id: str) -> dict[str, Any]:
    root = Path(root)
    registry = _load_yaml(root / "abstract-models/registry.yaml")
    for entry in registry.get("models", []):
        if entry.get("id") == model_id or entry.get("legacy_alias") == model_id:
            if entry.get("detail"):
                return _load_yaml(root / entry["detail"])
            return {**entry, "kind": "abstract-representation-model-summary"}
    raise KeyError(f"Unknown abstract model {model_id!r}")


def load_representation_binding(root: str | Path, binding_id: str) -> dict[str, Any]:
    root = Path(root)
    registry = _load_yaml(root / "representation-bindings/registry.yaml")
    for entry in registry.get("bindings", []):
        if entry.get("id") == binding_id:
            return _load_yaml(root / entry["path"])
    raise KeyError(f"Unknown representation binding {binding_id!r}")


def resolve_representation_binding(root: str | Path, model_id: str, chosen_format: str) -> dict[str, Any]:
    root = Path(root)
    registry = _load_yaml(root / "representation-bindings/registry.yaml")
    candidates = [entry for entry in registry.get("bindings", []) if entry.get("model") == model_id and entry.get("format") == chosen_format]
    if not candidates:
        raise KeyError(f"No representation binding for model {model_id!r} and chosen format {chosen_format!r}")
    if len(candidates) > 1:
        raise ValueError(f"Multiple bindings exist for model {model_id!r} and chosen format {chosen_format!r}; choose one explicitly")
    return _load_yaml(root / candidates[0]["path"])


def load_style(root: str | Path, style_id: str) -> dict[str, Any]:
    root = Path(root)
    registry = _load_yaml(root / "styles/registry.yaml")
    for entry in registry.get("styles", []):
        if entry.get("id") == style_id:
            return _load_yaml(root / entry["path"])
    raise KeyError(f"Unknown style profile {style_id!r}")


def load_style_binding(root: str | Path, binding_id: str) -> dict[str, Any]:
    root = Path(root)
    registry = _load_yaml(root / "style-bindings/registry.yaml")
    for entry in registry.get("bindings", []):
        if entry.get("id") == binding_id:
            return _load_yaml(root / entry["path"])
    raise KeyError(f"Unknown style binding {binding_id!r}")


def resolve_style_binding(root: str | Path, chosen_format: str) -> dict[str, Any]:
    root = Path(root)
    registry = _load_yaml(root / "style-bindings/registry.yaml")
    candidates = [entry for entry in registry.get("bindings", []) if entry.get("format") == chosen_format]
    if not candidates:
        raise KeyError(f"No style binding for chosen format {chosen_format!r}")
    if len(candidates) > 1:
        raise ValueError(f"Multiple style bindings exist for chosen format {chosen_format!r}; choose one explicitly")
    return _load_yaml(root / candidates[0]["path"])


def plan_generation(root: str | Path, request: dict[str, Any]) -> dict[str, Any]:
    root = Path(root)
    validation = validate_framework_artifact(root, request, "generation-request")
    if not validation.ok:
        return {"ok": False, "validation": validation.as_dict()}

    model_id = request["abstract_model"]
    chosen_format = request["representation"]["format"]
    model = load_abstract_model(root, model_id)

    requested_binding = request["representation"].get("binding", "auto")
    binding = resolve_representation_binding(root, model_id, chosen_format) if requested_binding == "auto" else load_representation_binding(root, requested_binding)
    if binding.get("model") != model_id or binding.get("format") != chosen_format:
        raise ValueError("Explicit representation binding does not match requested model and chosen format")

    style = None
    style_binding = None
    if (request.get("style") or {}).get("profile"):
        style = load_style(root, request["style"]["profile"])
        requested_style_binding = request["style"].get("binding", "auto")
        style_binding = resolve_style_binding(root, chosen_format) if requested_style_binding == "auto" else load_style_binding(root, requested_style_binding)
        if style_binding.get("format") != chosen_format:
            raise ValueError("Explicit style binding does not match chosen format")

    return {
        "ok": True,
        "selection": {
            "abstract_model": model["id"],
            "chosen_format": chosen_format,
            "format_selection": "chosen-not-auto-selected",
            "representation_binding": binding["id"],
            "style_profile": style["id"] if style else None,
            "style_binding": style_binding["id"] if style_binding else None,
            "overlays": list(request.get("overlays") or []),
        },
        "contracts": {"model": model, "representation_binding": binding, "style": style, "style_binding": style_binding},
        "execution_order": ["canonical-semantics", "abstract-model", "chosen-format", "representation-binding", "semantic-overlays", "style-profile", "format-style-binding", "transform", "validate", "provenance-and-equivalence"],
    }
