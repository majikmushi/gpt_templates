from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import fromstring, ParseError
from jsonschema import Draft202012Validator
from .models import ValidationResult

def validate_canonical(model: dict[str, Any], schema_path: str | Path) -> ValidationResult:
    result = ValidationResult("canonical.core")
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(model), key=lambda e: list(e.absolute_path)):
        path = ".".join(str(p) for p in err.absolute_path) or None
        result.add("error", "canonical.schema", err.message, path)
    ids = {e.get("id") for e in model.get("elements", [])}
    if len(ids) != len(model.get("elements", [])):
        result.add("error", "canonical.element-id-duplicate", "Element IDs must be unique")
    rel_ids = {r.get("id") for r in model.get("relationships", [])}
    if len(rel_ids) != len(model.get("relationships", [])):
        result.add("error", "canonical.relationship-id-duplicate", "Relationship IDs must be unique")
    for rel in model.get("relationships", []):
        for end in ("source", "target"):
            if rel.get(end) not in ids:
                result.add("error", "canonical.relationship-endpoint", f"{rel.get('id')}: unknown {end} {rel.get(end)!r}", f"relationships.{rel.get('id')}.{end}")
    for container in model.get("containers", []):
        for member in container.get("members", []):
            if member not in ids:
                result.add("error", "canonical.container-member", f"{container.get('id')}: unknown member {member!r}")
    return result

def validate_mermaid_class(text: str) -> ValidationResult:
    """Validate only the engine-owned Mermaid classDiagram subset.

    This is intentionally not a normative Mermaid parser. The future Mermaid
    source-derived validator remains the authority for full language validation.
    """
    result = ValidationResult("format.mermaid.class")
    stripped = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("%%")]
    if not stripped or stripped[0] != "classDiagram":
        result.add("error", "mermaid.subset.header", "Expected classDiagram header")
        return result
    balance = 0
    declared: set[str] = set()
    for i, line in enumerate(stripped[1:], start=2):
        if line.startswith("class "):
            ident = line.split()[1].split("[", 1)[0].split("{", 1)[0]
            declared.add(ident)
        balance += line.count("{") - line.count("}")
        if balance < 0:
            result.add("error", "mermaid.subset.braces", "Closing brace without opening brace", f"line:{i}")
            balance = 0
    if balance:
        result.add("error", "mermaid.subset.braces", "Unbalanced class body braces")
    if not declared:
        result.add("warning", "mermaid.subset.no-classes", "No class declarations found")
    result.add("warning", "mermaid.validation-scope", "Validated engine-generated subset only; full Mermaid validation is pending source-derived rules")
    return result

def validate_plantuml(text: str) -> ValidationResult:
    result = ValidationResult("format.plantuml")
    stripped = text.strip()
    if not stripped.startswith("@startuml"):
        result.add("error", "plantuml.header", "Missing @startuml")
    if not stripped.endswith("@enduml"):
        result.add("error", "plantuml.footer", "Missing @enduml")
    if text.count("{") != text.count("}"):
        result.add("error", "plantuml.braces", "Unbalanced braces")
    return result

def validate_json_schema(schema: dict[str, Any]) -> ValidationResult:
    result = ValidationResult("format.json-schema")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        result.add("error", "json-schema.meta-schema", str(exc))
    return result

def validate_xml(text: str) -> ValidationResult:
    result = ValidationResult("format.xml")
    try:
        root = fromstring(text)
    except ParseError as exc:
        result.add("error", "xml.well-formed", str(exc))
        return result
    if root.tag != "model":
        result.add("warning", "xml.profile-root", f"Expected repository model profile root <model>, got <{root.tag}>")
    return result

def validate_markdown(text: str) -> ValidationResult:
    result = ValidationResult("format.markdown")
    if not text.strip():
        result.add("error", "markdown.empty", "Markdown output is empty")
    elif not any(line.startswith("# ") for line in text.splitlines()):
        result.add("warning", "markdown.heading", "No level-1 heading found")
    return result

def validate_uml_class(value: dict[str, Any]) -> ValidationResult:
    result = ValidationResult("format.uml.class")
    if value.get("kind") != "uml-class-model":
        result.add("error", "uml.class.kind", "Expected kind=uml-class-model")
        return result
    ids = [c.get("id") for c in value.get("classes", [])]
    if len(ids) != len(set(ids)):
        result.add("error", "uml.class.duplicate", "Class IDs must be unique")
    idset = set(ids)
    for rel in value.get("relationships", []):
        if rel.get("source") not in idset or rel.get("target") not in idset:
            result.add("error", "uml.class.endpoint", f"Unknown relationship endpoint in {rel.get('id')}")
    result.add("warning", "uml.validation-scope", "Validated repository UML class interchange model, not the normative UML metamodel")
    return result

def validate_target(target_format: str, content: Any) -> ValidationResult:
    if target_format == "format.mermaid.class":
        return validate_mermaid_class(content)
    if target_format == "format.plantuml":
        return validate_plantuml(content)
    if target_format == "format.json-schema":
        return validate_json_schema(content)
    if target_format == "format.xml":
        return validate_xml(content)
    if target_format == "format.markdown":
        return validate_markdown(content)
    if target_format == "format.uml.class":
        return validate_uml_class(content)
    raise ValueError(f"No built-in validator for {target_format!r}")
