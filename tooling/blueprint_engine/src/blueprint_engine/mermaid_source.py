from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .mermaid_runtime import MermaidRuntimeBridge, MermaidRuntimeError, MermaidRuntimeUnavailable
from .models import ValidationResult

_ALLOWED_DIRECTIONS = {"TB", "BT", "RL", "LR"}
_ALLOWED_LINK_TARGETS = {"_self", "_blank", "_parent", "_top"}
_RELATION_MARKERS = {
    0: "aggregation", 1: "inheritance", 2: "composition", 3: "dependency", 4: "interface",
    "0": "aggregation", "1": "inheritance", "2": "composition", "3": "dependency", "4": "interface",
    "none": "none", None: "none",
}


def preflight_mermaid_class(text: str) -> ValidationResult:
    result = ValidationResult("format.mermaid.class")
    lines = text.splitlines()
    meaningful: list[tuple[int, str]] = []
    in_frontmatter = False
    for index, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if index == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---": in_frontmatter = False
            continue
        if not stripped or stripped.startswith("%%"): continue
        meaningful.append((index, stripped))
    if not meaningful or not re.match(r"^classDiagram(?:-v2)?(?:\s|$)", meaningful[0][1]):
        result.add("error", "mermaid.class.header", "Class diagrams must start with classDiagram or classDiagram-v2 after optional frontmatter/comments", f"line:{meaningful[0][0] if meaningful else 1}")
        return result
    brace_balance = 0
    for line_no, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("%%"): continue
        direction = re.match(r"^direction\s+(\S+)", line)
        if direction and direction.group(1) not in _ALLOWED_DIRECTIONS:
            result.add("error", "mermaid.class.direction", f"Unsupported classDiagram direction {direction.group(1)!r}; expected one of {sorted(_ALLOWED_DIRECTIONS)}", f"line:{line_no}")
        if line.startswith("note ") and not line.startswith("note for "):
            payload = line[len("note "):].strip()
            if not (payload.startswith('"') and payload.endswith('"')):
                result.add("error", "mermaid.class.note-text", "Standalone note text must be double quoted", f"line:{line_no}")
        elif line.startswith("note for ") and re.match(r'^note\s+for\s+\S+\s+(".*")\s*$', line) is None:
            result.add("error", "mermaid.class.note-text", 'note for syntax requires a class name followed by double-quoted text', f"line:{line_no}")
        click_target = re.search(r"\s(_[A-Za-z]+)\s*$", line) if line.startswith(("click ", "link ")) else None
        if click_target and click_target.group(1) not in _ALLOWED_LINK_TARGETS:
            result.add("error", "mermaid.class.link-target", f"Unsupported link target {click_target.group(1)!r}", f"line:{line_no}")
        scrubbed = re.sub(r'"[^"]*"', "", line)
        brace_balance += scrubbed.count("{") - scrubbed.count("}")
        if brace_balance < 0:
            result.add("error", "mermaid.class.braces", "Closing brace without a matching opening class/namespace body", f"line:{line_no}")
            brace_balance = 0
    if brace_balance:
        result.add("error", "mermaid.class.braces", "Unbalanced class/namespace body braces")
    return result


def validate_mermaid_runtime(text: str, *, repository_root: str | Path | None = None, require_runtime: bool = False) -> ValidationResult:
    result = ValidationResult("format.mermaid")
    if repository_root is None:
        result.add("error" if require_runtime else "warning", "mermaid.runtime-not-requested", "Mermaid runtime parser was not invoked")
        return result
    bridge = MermaidRuntimeBridge(repository_root)
    try:
        runtime = bridge.validate(text)
    except MermaidRuntimeUnavailable as exc:
        result.add("error" if require_runtime else "warning", "mermaid.runtime-unavailable", str(exc)); return result
    except MermaidRuntimeError as exc:
        result.add("error", "mermaid.runtime-bridge", str(exc)); return result
    if not runtime.ok:
        error = runtime.error or {}
        code = error.get("code", "mermaid-parse")
        severity = "warning" if code == "runtime-unavailable" and not require_runtime else "error"
        message = error.get("message") or "Mermaid parser rejected the diagram"
        detail = error.get("detail")
        if isinstance(detail, dict) and detail.get("message"): message = f"{message}: {detail['message']}"
        result.add(severity, f"mermaid.runtime.{code}", message)
    return result


def validate_mermaid_class(text: str, *, repository_root: str | Path | None = None, require_runtime: bool = False) -> ValidationResult:
    result = preflight_mermaid_class(text)
    if not result.ok: return result
    if repository_root is None:
        result.add("warning", "mermaid.runtime-not-requested", "Source-derived preflight passed; Mermaid runtime parser was not invoked")
        return result
    bridge = MermaidRuntimeBridge(repository_root)
    try:
        runtime = bridge.validate(text)
    except MermaidRuntimeUnavailable as exc:
        result.add("error" if require_runtime else "warning", "mermaid.runtime-unavailable", str(exc)); return result
    except MermaidRuntimeError as exc:
        result.add("error", "mermaid.runtime-bridge", str(exc)); return result
    if not runtime.ok:
        code = (runtime.error or {}).get("code", "mermaid-parse")
        severity = "warning" if code == "runtime-unavailable" and not require_runtime else "error"
        message = (runtime.error or {}).get("message") or "Mermaid parser rejected the diagram"
        detail = (runtime.error or {}).get("detail")
        if isinstance(detail, dict) and detail.get("message"): message = f"{message}: {detail['message']}"
        result.add(severity, f"mermaid.runtime.{code}", message)
        return result
    if runtime.diagram_type and not str(runtime.diagram_type).startswith("classDiagram"):
        result.add("error", "mermaid.class.detected-type", f"Mermaid detected {runtime.diagram_type!r}, expected classDiagram")
    return result


def _member_to_plain(member: dict[str, Any]) -> dict[str, Any]:
    return {key: member.get(key) for key in ("id", "memberType", "visibility", "classifier", "parameters", "returnType", "text") if member.get(key) not in (None, "")}


def _relationship_semantics(relation: dict[str, Any]) -> tuple[str, list[str], str]:
    descriptor = relation.get("relation") or {}
    left = _RELATION_MARKERS.get(descriptor.get("type1"), "unknown")
    right = _RELATION_MARKERS.get(descriptor.get("type2"), "unknown")
    semantics = [value for value in (left, right) if value not in {"none", "unknown"}]
    if "inheritance" in semantics: rel_type = "inheritance"
    elif "composition" in semantics: rel_type = "composition"
    elif "aggregation" in semantics: rel_type = "aggregation"
    elif "dependency" in semantics: rel_type = "dependency"
    elif "interface" in semantics: rel_type = "interface"
    else: rel_type = "association"
    if left != "none" and right != "none": direction = "bidirectional"
    elif left != "none" or right != "none": direction = "directed"
    else: direction = "undirected"
    return rel_type, semantics or ["association"], direction


def mermaid_class_ast_to_canonical(ast: dict[str, Any], *, model_id: str = "imported.mermaid.class", binding_id: str | None = None) -> dict[str, Any]:
    if ast.get("kind") != "mermaid-class-ast": raise ValueError("Expected Mermaid class AST")
    elements: list[dict[str, Any]] = []
    for cls in ast.get("classes", []):
        properties: dict[str, Any] = {}
        members = [_member_to_plain(m) for m in cls.get("members", [])]
        methods = [_member_to_plain(m) for m in cls.get("methods", [])]
        if members: properties["members"] = members
        if methods: properties["methods"] = methods
        if cls.get("type"): properties["generic_type"] = cls["type"]
        mermaid_annotations = {key: value for key, value in {
            "stereotypes": cls.get("annotations") or [], "css_classes": cls.get("cssClasses"),
            "styles": cls.get("styles") or [], "link": cls.get("link"), "link_target": cls.get("linkTarget"),
            "tooltip": cls.get("tooltip"),
        }.items() if value not in (None, "", [])}
        elements.append({"id": cls["id"], "type": "class", "name": cls.get("label") or cls["id"], "properties": properties, "annotations": {"mermaid": mermaid_annotations}})
    existing_ids = {element["id"] for element in elements}
    for interface in ast.get("interfaces", []):
        if interface.get("id") and interface["id"] not in existing_ids:
            elements.append({"id": interface["id"], "type": "interface", "name": interface.get("label") or interface["id"], "properties": {}, "annotations": {"mermaid": {"synthetic_lollipop": True}}})
            existing_ids.add(interface["id"])
    relationships: list[dict[str, Any]] = []
    for index, rel in enumerate(ast.get("relations", []), start=1):
        rel_type, semantics, direction = _relationship_semantics(rel)
        descriptor = rel.get("relation") or {}
        relationships.append({
            "id": rel.get("id") or f"mermaid-rel-{index}", "type": rel_type, "source": rel["id1"], "target": rel["id2"], "direction": direction,
            "source_cardinality": None if rel.get("relationTitle1") in (None, "none", "") else rel.get("relationTitle1"),
            "target_cardinality": None if rel.get("relationTitle2") in (None, "none", "") else rel.get("relationTitle2"),
            "semantics": semantics,
            "annotations": {"mermaid": {"title": rel.get("title") or "", "left_marker": _RELATION_MARKERS.get(descriptor.get("type1"), "unknown"), "right_marker": _RELATION_MARKERS.get(descriptor.get("type2"), "unknown"), "line_type": "dotted" if descriptor.get("lineType") == 1 else "solid"}},
        })
    for rel in relationships:
        if rel.get("source_cardinality") is None: rel.pop("source_cardinality", None)
        if rel.get("target_cardinality") is None: rel.pop("target_cardinality", None)
    endpoint_ids = {endpoint for rel in relationships for endpoint in (rel["source"], rel["target"])}
    for endpoint in sorted(endpoint_ids - existing_ids):
        elements.append({"id": endpoint, "type": "implicit-reference", "name": endpoint, "properties": {}, "annotations": {"mermaid": {"implicit_relation_endpoint": True}}})
        existing_ids.add(endpoint)
    containers = [{"id": namespace["id"], "type": "namespace", "members": list(namespace.get("classIds") or []), "annotations": {"mermaid": {"child_ids": namespace.get("childIds") or []}}} for namespace in ast.get("namespaces", [])]
    metadata: dict[str, Any] = {"source_format": "format.mermaid.class", "direction": ast.get("direction") or "TB"}
    if binding_id: metadata["representation_binding"] = binding_id
    accessibility = ast.get("accessibility") or {}
    if any(accessibility.values()): metadata["accessibility"] = accessibility
    if ast.get("notes"): metadata["notes"] = ast["notes"]
    return {
        "id": model_id, "type": "model", "metadata": metadata, "elements": elements,
        "relationships": relationships, "containers": containers, "visual_encodings": [],
        "provenance": {"source_format": "format.mermaid.class", "adapter": "adapter.mermaid.class.runtime-ast", **({"representation_binding": binding_id} if binding_id else {})},
    }
