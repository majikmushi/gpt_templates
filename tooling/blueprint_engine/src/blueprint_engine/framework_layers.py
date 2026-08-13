from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .compatibility import (
    load_renderer,
    missing_capabilities,
    resolve_format_release,
    resolve_renderer_compatibility,
    resolve_renderer_release,
    version_matches,
)
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
        "format-version": "format-version.schema.json",
        "renderer": "renderer.schema.json",
        "renderer-compatibility": "renderer-compatibility.schema.json",
    }
    if artifact_kind not in schemas:
        raise KeyError(f"Unknown framework artifact kind {artifact_kind!r}")
    return _validate(value, root / "schemas" / schemas[artifact_kind], artifact_kind)


def load_abstract_model(root: str | Path, model_id: str) -> dict[str, Any]:
    root = Path(root)
    registry = _load_yaml(root / "abstract-models/registry.yaml")
    for entry in registry.get("models", []):
        if entry.get("id") == model_id:
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

    representation = request["representation"]
    model_id = request["abstract_model"]
    chosen_format = representation["format"]
    mode = representation.get("compatibility_mode", "strict")
    warnings: list[str] = []
    errors: list[str] = []

    def compatibility_issue(message: str) -> None:
        (errors if mode == "strict" else warnings).append(message)

    model = load_abstract_model(root, model_id)
    requested_binding = representation.get("binding", "auto")
    binding = resolve_representation_binding(root, model_id, chosen_format) if requested_binding == "auto" else load_representation_binding(root, requested_binding)
    if binding.get("model") != model_id or binding.get("format") != chosen_format:
        return {"ok": False, "errors": ["Explicit representation binding does not match requested model and chosen format"]}

    format_release = resolve_format_release(
        root,
        chosen_format,
        version=representation.get("version"),
        version_constraint=representation.get("version_constraint"),
    )
    format_version = format_release.get("version")
    format_capabilities: list[str] = []
    if format_release["status"] == "resolved":
        format_capabilities = list((format_release.get("artifact") or {}).get("capabilities") or [])
        binding_compat = binding.get("compatibility") or {}
        if binding_compat.get("format_versions") and not version_matches(format_version, binding_compat["format_versions"]):
            compatibility_issue(f"Binding {binding['id']} does not declare compatibility with {chosen_format} {format_version}")
        missing = missing_capabilities(binding_compat.get("required_capabilities") or [], format_capabilities)
        if missing:
            compatibility_issue(f"Format release {chosen_format} {format_version} lacks binding capabilities: {', '.join(missing)}")
    else:
        warnings.append(f"No pinned format release is registered for {chosen_format}; version compatibility is unverified")

    style = None
    style_binding = None
    if (request.get("style") or {}).get("profile"):
        style = load_style(root, request["style"]["profile"])
        requested_style_binding = request["style"].get("binding", "auto")
        style_binding = resolve_style_binding(root, chosen_format) if requested_style_binding == "auto" else load_style_binding(root, requested_style_binding)
        if style_binding.get("format") != chosen_format:
            return {"ok": False, "errors": ["Explicit style binding does not match chosen format"]}
        if format_version:
            style_compat = style_binding.get("compatibility") or {}
            if style_compat.get("format_versions") and not version_matches(format_version, style_compat["format_versions"]):
                compatibility_issue(f"Style binding {style_binding['id']} does not declare compatibility with {chosen_format} {format_version}")
            missing = missing_capabilities(style_compat.get("required_capabilities") or [], format_capabilities)
            if missing:
                compatibility_issue(f"Format release {chosen_format} {format_version} lacks style capabilities: {', '.join(missing)}")

    renderer_resolution = None
    renderer_contract = None
    renderer_request = representation.get("renderer")
    if renderer_request:
        renderer_resolution = resolve_renderer_release(root, renderer_request["id"], version=renderer_request.get("version"))
        if not format_version:
            compatibility_issue("A renderer was selected but the chosen format has no pinned version to compare against")
        elif renderer_resolution["status"] != "resolved":
            compatibility_issue(f"Renderer {renderer_request['id']} has no pinned release")
        else:
            renderer_contract = resolve_renderer_compatibility(
                root,
                renderer_id=renderer_request["id"],
                renderer_version=renderer_resolution["version"],
                format_id=chosen_format,
                format_version=format_version,
            )
            if renderer_contract is None:
                compatibility_issue(
                    f"No renderer compatibility contract covers {renderer_request['id']} {renderer_resolution['version']} with {chosen_format} {format_version}"
                )
            elif renderer_contract.get("support") == "unsupported":
                compatibility_issue(f"Renderer compatibility contract {renderer_contract['id']} marks this combination unsupported")
            elif renderer_contract.get("support") in {"partial", "unverified"}:
                warnings.append(f"Renderer compatibility is {renderer_contract.get('support')} under {renderer_contract['id']}")
            if renderer_contract:
                supported = (renderer_contract.get("capabilities") or {}).get("supported") or []
                required = list((binding.get("compatibility") or {}).get("required_capabilities") or [])
                if style_binding:
                    required.extend((style_binding.get("compatibility") or {}).get("required_capabilities") or [])
                missing = missing_capabilities(required, supported)
                if missing:
                    compatibility_issue(f"Selected renderer release lacks required effective capabilities: {', '.join(missing)}")

    selection = {
        "abstract_model": model["id"],
        "chosen_format": chosen_format,
        "format_selection": "chosen-not-auto-selected",
        "format_version": format_version,
        "format_version_status": format_release["status"],
        "representation_binding": binding["id"],
        "style_profile": style["id"] if style else None,
        "style_binding": style_binding["id"] if style_binding else None,
        "overlays": list(request.get("overlays") or []),
        "renderer": renderer_resolution.get("renderer") if renderer_resolution else None,
        "renderer_version": renderer_resolution.get("version") if renderer_resolution else None,
        "renderer_compatibility": renderer_contract.get("id") if renderer_contract else None,
    }
    if errors:
        return {"ok": False, "selection": selection, "errors": errors, "warnings": warnings}

    return {
        "ok": True,
        "selection": selection,
        "warnings": warnings,
        "contracts": {
            "model": model,
            "format_release": format_release.get("artifact"),
            "representation_binding": binding,
            "style": style,
            "style_binding": style_binding,
            "renderer": renderer_resolution.get("artifact") if renderer_resolution else None,
            "renderer_compatibility": renderer_contract,
        },
        "execution_order": [
            "canonical-semantics",
            "abstract-model",
            "chosen-format",
            "resolve-format-version",
            "representation-binding",
            "semantic-overlays",
            "style-profile",
            "format-style-binding",
            "optional-renderer-compatibility",
            "transform",
            "validate",
            "provenance-and-equivalence",
        ],
    }
