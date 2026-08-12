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
    profile_id: str | None = None,
    overlays: list[str] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_hash": canonical_hash(source),
        "transform": transform_id,
        "target_format": target_format,
    }
    if profile_id:
        result["profile"] = profile_id
    if overlays:
        result["overlays"] = list(overlays)
    return result
