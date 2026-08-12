from __future__ import annotations
from copy import deepcopy
from typing import Any

def _get_path(obj: Any, path: str) -> Any:
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur

def _matches(item: dict[str, Any], predicate: dict[str, Any]) -> bool:
    return all(_get_path(item, key) == expected for key, expected in predicate.items())

def _render(value: Any, item: dict[str, Any]) -> Any:
    if isinstance(value, str) and value.startswith("$."):
        return deepcopy(_get_path(item, value[2:]))
    if isinstance(value, list):
        return [_render(v, item) for v in value]
    if isinstance(value, dict):
        return {k: _render(v, item) for k, v in value.items()}
    return deepcopy(value)

class DeclarativeMappingEngine:
    """Small deterministic mapping engine for repository transform specs.

    Spec:
      target: {nodes: [], edges: []}
      rules:
        - select: elements
          match: {type: component}
          emit_to: nodes
          emit: {id: "$.id", kind: "$.type", label: "$.name"}
    """

    def apply(self, source: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
        target = deepcopy(spec.get("target", {}))
        for rule in spec.get("rules", []):
            collection_name = rule["select"]
            emit_to = rule["emit_to"]
            target.setdefault(emit_to, [])
            for item in source.get(collection_name, []):
                if _matches(item, rule.get("match", {})):
                    target[emit_to].append(_render(rule.get("emit", {}), item))
        return target
