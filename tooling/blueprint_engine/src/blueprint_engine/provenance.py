from __future__ import annotations
import hashlib
import json
from typing import Any


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def make_provenance(
    source: Any,
    transform_id: str,
    target_format: str,
    *,
    binding_id: str | None = None,
    overlays: list[str] | None = None,
    style_id: str | None = None,
    style_binding_id: str | None = None,
    format_version: str | None = None,
    renderer_id: str | None = None,
    renderer_version: str | None = None,
    compatibility_contract: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_hash": canonical_hash(source),
        "transform": transform_id,
        "target_format": target_format,
    }
    if binding_id:
        result["representation_binding"] = binding_id
    if overlays:
        result["overlays"] = list(overlays)
    if style_id:
        result["style"] = style_id
    if style_binding_id:
        result["style_binding"] = style_binding_id
    if format_version:
        result["target_format_version"] = format_version
    if renderer_id:
        result["renderer"] = renderer_id
    if renderer_version:
        result["renderer_version"] = renderer_version
    if compatibility_contract:
        result["renderer_compatibility"] = compatibility_contract
    return result
