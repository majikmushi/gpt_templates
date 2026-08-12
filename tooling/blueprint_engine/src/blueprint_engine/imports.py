from __future__ import annotations
import json
from typing import Any
from xml.etree.ElementTree import fromstring

def xml_to_canonical(text: str) -> dict[str, Any]:
    root = fromstring(text)
    if root.tag != "model":
        raise ValueError("Expected <model> root")
    model: dict[str, Any] = {
        "id": root.attrib["id"],
        "type": root.attrib.get("type", "model"),
        "metadata": {},
        "elements": [],
        "relationships": [],
        "containers": [],
        "visual_encodings": [],
    }
    metadata = root.find("metadata")
    if metadata is not None:
        for entry in metadata.findall("entry"):
            text_value = entry.text or ""
            try:
                value = json.loads(text_value)
            except json.JSONDecodeError:
                value = text_value
            model["metadata"][entry.attrib["name"]] = value
    elements = root.find("elements")
    if elements is not None:
        for node in elements.findall("element"):
            el: dict[str, Any] = {"id": node.attrib["id"], "type": node.attrib.get("type", "entity")}
            if node.attrib.get("name"):
                el["name"] = node.attrib["name"]
            props = {}
            pnode = node.find("properties")
            if pnode is not None:
                for p in pnode.findall("property"):
                    props[p.attrib["name"]] = json.loads(p.attrib.get("json", "null"))
            if props:
                el["properties"] = props
            anns = {}
            anode = node.find("annotations")
            if anode is not None:
                for a in anode.findall("annotation"):
                    anns[a.attrib["name"]] = json.loads(a.attrib.get("json", "null"))
            if anns:
                el["annotations"] = anns
            model["elements"].append(el)
    relationships = root.find("relationships")
    if relationships is not None:
        for node in relationships.findall("relationship"):
            rel: dict[str, Any] = {
                "id": node.attrib["id"], "type": node.attrib.get("type", "association"),
                "source": node.attrib["source"], "target": node.attrib["target"],
                "direction": node.attrib.get("direction", "directed"),
            }
            if "source_cardinality" in node.attrib:
                rel["source_cardinality"] = node.attrib["source_cardinality"]
            if "target_cardinality" in node.attrib:
                rel["target_cardinality"] = node.attrib["target_cardinality"]
            semantics = [s.text or "" for s in node.findall("semantic")]
            if semantics:
                rel["semantics"] = semantics
            anns = {}
            anode = node.find("annotations")
            if anode is not None:
                for a in anode.findall("annotation"):
                    anns[a.attrib["name"]] = json.loads(a.attrib.get("json", "null"))
            if anns:
                rel["annotations"] = anns
            model["relationships"].append(rel)
    containers = root.find("containers")
    if containers is not None:
        for node in containers.findall("container"):
            c = {"id": node.attrib["id"], "type": node.attrib["type"], "members": [m.attrib["ref"] for m in node.findall("member")]}
            if node.attrib.get("parent"):
                c["parent"] = node.attrib["parent"]
            model["containers"].append(c)
    return model

def uml_class_to_canonical(value: dict[str, Any]) -> dict[str, Any]:
    if value.get("kind") != "uml-class-model":
        raise ValueError("Expected kind=uml-class-model")
    model = {
        "id": value.get("id", "uml-import").removesuffix(".uml-class"),
        "type": "model",
        "elements": [],
        "relationships": [],
        "containers": [],
        "visual_encodings": [],
    }
    for cls in value.get("classes", []):
        stereotypes = cls.get("stereotypes") or []
        el = {
            "id": cls["id"],
            "type": stereotypes[0] if stereotypes else "entity",
            "name": cls.get("name", cls["id"]),
        }
        if cls.get("attributes"):
            el["properties"] = dict(cls["attributes"])
        model["elements"].append(el)
    for r in value.get("relationships", []):
        rel = {k: v for k, v in r.items() if v is not None and k in {
            "id", "type", "source", "target", "direction", "source_cardinality", "target_cardinality", "semantics", "annotations"
        }}
        model["relationships"].append(rel)
    return model
