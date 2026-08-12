from __future__ import annotations
from typing import Any
from .models import CompareResult

def _element_map(model: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
    out = {}
    for e in model.get("elements", []):
        out[e["id"]] = (
            e.get("type"),
            e.get("name"),
            tuple(sorted((e.get("properties") or {}).items())),
        )
    return out

def _relationship_map(model: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
    out = {}
    for r in model.get("relationships", []):
        out[r["id"]] = (
            r.get("type"), r.get("source"), r.get("target"), r.get("direction"),
            r.get("source_cardinality"), r.get("target_cardinality"),
            tuple(sorted(r.get("semantics") or [])),
            tuple(sorted((r.get("annotations") or {}).items())),
        )
    return out

def compare_canonical(a: dict[str, Any], b: dict[str, Any]) -> CompareResult:
    if a == b:
        return CompareResult("exact")

    ea, eb = _element_map(a), _element_map(b)
    ra, rb = _relationship_map(a), _relationship_map(b)
    if ea == eb and ra == rb:
        return CompareResult("equivalent", notes=["Non-semantic metadata/order differences ignored"])

    missing: list[str] = []
    extra: list[str] = []
    for key in sorted(set(ea) | set(eb)):
        if key not in eb:
            missing.append(f"element:{key}")
        elif key not in ea:
            extra.append(f"element:{key}")
        elif ea[key] != eb[key]:
            missing.append(f"element-changed:{key}")
    for key in sorted(set(ra) | set(rb)):
        if key not in rb:
            missing.append(f"relationship:{key}")
        elif key not in ra:
            extra.append(f"relationship:{key}")
        elif ra[key] != rb[key]:
            missing.append(f"relationship-changed:{key}")

    projection = not any(x.startswith(("element-changed:", "relationship-changed:")) for x in missing)
    classification = "projection" if projection and not extra else "non-equivalent"
    return CompareResult(classification, missing=missing, extra=extra)
