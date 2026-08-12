from __future__ import annotations
import json
from typing import Any, Callable
from xml.etree.ElementTree import Element, SubElement, tostring
from .models import TransformResult
from .provenance import make_provenance

Handler = Callable[[dict[str, Any]], tuple[Any, str, list[str]]]

def _safe_id(value: str) -> str:
    out = []
    for ch in value:
        out.append(ch if ch.isalnum() or ch in "_-" else "_")
    result = "".join(out)
    if result and result[0].isdigit():
        result = "_" + result
    return result or "_"

def _label(element: dict[str, Any]) -> str:
    return str(element.get("name") or element["id"])

def _relationship_label(rel: dict[str, Any]) -> str:
    annotations = rel.get("annotations") or {}
    return str(annotations.get("protocol") or annotations.get("label") or rel.get("type") or "")

def canonical_to_mermaid_class(model: dict[str, Any]) -> tuple[str, str, list[str]]:
    lines = ["classDiagram"]
    for el in model.get("elements", []):
        eid = _safe_id(el["id"])
        label = _label(el).replace('"', "'")
        lines.append(f'    class {eid}["{label}"] {{')
        lines.append(f"        <<{el.get('type', 'entity')}>>")
        for key, value in sorted((el.get("properties") or {}).items()):
            val = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
            lines.append(f"        +{key}: {val}")
        lines.append("    }")
    rel_map = {
        "inheritance": "<|--",
        "composition": "*--",
        "aggregation": "o--",
        "dependency": "..>",
        "realization": "..|>",
        "association": "-->",
        "communication": "--",
        "ownership": "*--",
        "containment": "*--",
    }
    for rel in model.get("relationships", []):
        source, target = _safe_id(rel["source"]), _safe_id(rel["target"])
        arrow = rel_map.get(rel.get("type"), "-->")
        if rel.get("direction") == "bidirectional" and arrow == "-->":
            arrow = "<-->"
        label = _relationship_label(rel).replace('"', "'")
        sc = rel.get("source_cardinality")
        tc = rel.get("target_cardinality")
        left = f'{source} "{sc}"' if sc else source
        right = f'"{tc}" {target}' if tc else target
        suffix = f" : {label}" if label else ""
        lines.append(f"    {left} {arrow} {right}{suffix}")
    return "\n".join(lines) + "\n", "text/vnd.mermaid", []

def canonical_to_plantuml(model: dict[str, Any]) -> tuple[str, str, list[str]]:
    lines = ["@startuml"]
    for el in model.get("elements", []):
        eid = _safe_id(el["id"])
        label = _label(el).replace('"', "'")
        lines.append(f'class "{label}" as {eid} <<{el.get("type", "entity")}>> {{')
        for key, value in sorted((el.get("properties") or {}).items()):
            val = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
            lines.append(f"  +{key}: {val}")
        lines.append("}")
    rel_map = {
        "inheritance": "<|--",
        "composition": "*--",
        "aggregation": "o--",
        "dependency": "..>",
        "realization": "..|>",
        "association": "-->",
        "communication": "--",
        "ownership": "*--",
        "containment": "*--",
    }
    for rel in model.get("relationships", []):
        source, target = _safe_id(rel["source"]), _safe_id(rel["target"])
        arrow = rel_map.get(rel.get("type"), "-->")
        label = _relationship_label(rel).replace('"', "'")
        sc = rel.get("source_cardinality")
        tc = rel.get("target_cardinality")
        left = f'{source} "{sc}"' if sc else source
        right = f'"{tc}" {target}' if tc else target
        suffix = f" : {label}" if label else ""
        lines.append(f"{left} {arrow} {right}{suffix}")
    lines.append("@enduml")
    return "\n".join(lines) + "\n", "text/x-plantuml", []

def canonical_to_uml_class(model: dict[str, Any]) -> tuple[dict[str, Any], str, list[str]]:
    out = {
        "id": model["id"] + ".uml-class",
        "kind": "uml-class-model",
        "classes": [
            {
                "id": el["id"],
                "name": _label(el),
                "stereotypes": [el.get("type", "entity")],
                "attributes": dict(el.get("properties") or {}),
            }
            for el in model.get("elements", [])
        ],
        "relationships": [
            {
                "id": rel["id"],
                "type": rel["type"],
                "source": rel["source"],
                "target": rel["target"],
                "direction": rel.get("direction", "directed"),
                "source_cardinality": rel.get("source_cardinality"),
                "target_cardinality": rel.get("target_cardinality"),
                "semantics": list(rel.get("semantics") or []),
                "annotations": dict(rel.get("annotations") or {}),
            }
            for rel in model.get("relationships", [])
        ],
    }
    return out, "application/vnd.blueprint.uml+json", []

def canonical_to_json_schema(model: dict[str, Any]) -> tuple[dict[str, Any], str, list[str]]:
    defs: dict[str, Any] = {}
    properties: dict[str, Any] = {}
    for el in model.get("elements", []):
        prop_schema: dict[str, Any] = {}
        for key, value in sorted((el.get("properties") or {}).items()):
            if isinstance(value, bool):
                t = "boolean"
            elif isinstance(value, int):
                t = "integer"
            elif isinstance(value, float):
                t = "number"
            elif isinstance(value, list):
                t = "array"
            elif isinstance(value, dict):
                t = "object"
            else:
                t = "string"
            prop_schema[key] = {"type": t}
        defs[el["id"]] = {
            "type": "object",
            "title": _label(el),
            "properties": prop_schema,
            "additionalProperties": True,
            "x-blueprint-element-type": el.get("type"),
        }
        properties[el["id"]] = {"$ref": f"#/$defs/{el['id']}"}
    losses = []
    if model.get("relationships"):
        losses.append("relationships are not represented by the JSON Schema projection")
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": model["id"],
        "title": (model.get("metadata") or {}).get("title", model["id"]),
        "type": "object",
        "properties": properties,
        "$defs": defs,
        "x-blueprint-projection": {
            "source_type": model.get("type"),
            "dropped_relationship_ids": [r["id"] for r in model.get("relationships", [])],
        },
    }
    return schema, "application/schema+json", losses

def canonical_to_xml(model: dict[str, Any]) -> tuple[str, str, list[str]]:
    root = Element("model", {"id": model["id"], "type": str(model.get("type", "model"))})
    metadata = SubElement(root, "metadata")
    for key, value in sorted((model.get("metadata") or {}).items()):
        m = SubElement(metadata, "entry", {"name": str(key)})
        m.text = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)

    elements = SubElement(root, "elements")
    for el in model.get("elements", []):
        node = SubElement(elements, "element", {"id": el["id"], "type": str(el.get("type", "entity")), "name": _label(el)})
        props = SubElement(node, "properties")
        for key, value in sorted((el.get("properties") or {}).items()):
            SubElement(props, "property", {"name": str(key), "json": json.dumps(value, ensure_ascii=False)})
        anns = SubElement(node, "annotations")
        for key, value in sorted((el.get("annotations") or {}).items()):
            SubElement(anns, "annotation", {"name": str(key), "json": json.dumps(value, ensure_ascii=False)})

    relationships = SubElement(root, "relationships")
    for rel in model.get("relationships", []):
        attrs = {
            "id": rel["id"], "type": str(rel.get("type", "association")),
            "source": rel["source"], "target": rel["target"],
            "direction": str(rel.get("direction", "directed")),
        }
        if rel.get("source_cardinality") is not None:
            attrs["source_cardinality"] = str(rel["source_cardinality"])
        if rel.get("target_cardinality") is not None:
            attrs["target_cardinality"] = str(rel["target_cardinality"])
        rnode = SubElement(relationships, "relationship", attrs)
        for semantic in rel.get("semantics", []):
            s = SubElement(rnode, "semantic")
            s.text = str(semantic)
        anns = SubElement(rnode, "annotations")
        for key, value in sorted((rel.get("annotations") or {}).items()):
            SubElement(anns, "annotation", {"name": str(key), "json": json.dumps(value, ensure_ascii=False)})

    containers = SubElement(root, "containers")
    for container in model.get("containers", []):
        cattrs = {"id": container["id"], "type": container["type"]}
        if container.get("parent"):
            cattrs["parent"] = container["parent"]
        cnode = SubElement(containers, "container", cattrs)
        for member in container.get("members", []):
            SubElement(cnode, "member", {"ref": member})

    return tostring(root, encoding="unicode") + "\n", "application/xml", []

def canonical_to_markdown(model: dict[str, Any]) -> tuple[str, str, list[str]]:
    title = (model.get("metadata") or {}).get("title", model["id"])
    lines = [f"# {title}", "", f"- Model ID: `{model['id']}`", f"- Type: `{model.get('type', 'model')}`", "", "## Elements", ""]
    for el in model.get("elements", []):
        lines.append(f"### {_label(el)}")
        lines.append("")
        lines.append(f"- ID: `{el['id']}`")
        lines.append(f"- Type: `{el.get('type', 'entity')}`")
        props = el.get("properties") or {}
        if props:
            lines.extend(["", "| Property | Value |", "|---|---|"])
            for key, value in sorted(props.items()):
                lines.append(f"| {key} | {value} |")
        lines.append("")
    lines.extend(["## Relationships", "", "| ID | Type | Source | Target | Direction | Label |", "|---|---|---|---|---|---|"])
    for rel in model.get("relationships", []):
        lines.append(f"| {rel['id']} | {rel['type']} | {rel['source']} | {rel['target']} | {rel.get('direction', 'directed')} | {_relationship_label(rel)} |")
    return "\n".join(lines) + "\n", "text/markdown", ["format is presentation-oriented; round-trip recovery is not guaranteed"]

HANDLERS: dict[str, tuple[str, str, Handler]] = {
    "format.mermaid.class": ("transform.canonical-to-mermaid-class", "profile-dependent", canonical_to_mermaid_class),
    "format.plantuml": ("transform.canonical-to-plantuml", "profile-dependent", canonical_to_plantuml),
    "format.uml.class": ("transform.canonical-to-uml-class", "lossless-for-structural-subset", canonical_to_uml_class),
    "format.json-schema": ("adapter.json-schema.export", "projection", canonical_to_json_schema),
    "format.xml": ("adapter.xml.export", "profile-dependent", canonical_to_xml),
    "format.markdown": ("adapter.markdown.export", "presentation-only", canonical_to_markdown),
}

def transform_canonical(
    model: dict[str, Any],
    target_format: str,
    *,
    profile_id: str | None = None,
    overlays: list[str] | None = None,
) -> TransformResult:
    try:
        transform_id, fidelity, handler = HANDLERS[target_format]
    except KeyError as exc:
        raise ValueError(f"No built-in canonical transform for {target_format!r}") from exc
    content, media_type, losses = handler(model)
    provenance = make_provenance(model, transform_id, target_format, profile_id=profile_id, overlays=overlays)
    return TransformResult(target_format, content, media_type, transform_id, fidelity, losses, provenance)
