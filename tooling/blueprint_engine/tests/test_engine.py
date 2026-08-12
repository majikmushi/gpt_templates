from pathlib import Path
import json
import yaml
from blueprint_engine import BlueprintEngine
from blueprint_engine.declarative import DeclarativeMappingEngine

REPO = Path(__file__).resolve().parents[3]

def load_model():
    return yaml.safe_load((REPO / "examples/cross-format/embedded-controller/model.yaml").read_text())

def test_canonical_and_all_exports_validate():
    engine = BlueprintEngine(REPO)
    model = load_model()
    assert engine.validate_canonical(model).ok

    targets = [
        "format.mermaid.class",
        "format.plantuml",
        "format.uml.class",
        "format.json-schema",
        "format.xml",
        "format.markdown",
    ]
    for target in targets:
        result, validation = engine.transform(model, target)
        assert validation is not None
        assert validation.ok, (target, validation.as_dict())
        assert result.provenance["source_hash"].startswith("sha256:")

def test_projection_declares_relationship_loss():
    engine = BlueprintEngine(REPO)
    result, _ = engine.transform(load_model(), "format.json-schema")
    assert result.fidelity == "projection"
    assert result.losses
    assert result.content["x-blueprint-projection"]["dropped_relationship_ids"] == ["r1", "r2"]

def test_xml_roundtrip_equivalent():
    engine = BlueprintEngine(REPO)
    result = engine.roundtrip_xml(load_model())
    assert result.equivalent, result

def test_uml_roundtrip_equivalent_structural_subset():
    engine = BlueprintEngine(REPO)
    result = engine.roundtrip_uml_class(load_model())
    assert result.equivalent, result

def test_capability_matching():
    engine = BlueprintEngine(REPO)
    matches = engine.match(["typed_entities", "cardinality"])
    ids = [m.format_id for m in matches]
    assert "format.uml.class" in ids
    assert "format.mermaid.class" in ids
    assert "format.plantuml" in ids
    assert "format.xml" not in ids

def test_route_to_json_schema():
    engine = BlueprintEngine(REPO)
    route = engine.route("canonical.core", "format.json-schema")
    assert len(route) == 1
    assert route[0]["transform"] == "adapter.json-schema.export"

def test_declarative_mapping_engine():
    source = load_model()
    spec = {
        "target": {"nodes": [], "edges": []},
        "rules": [
            {
                "select": "elements",
                "match": {"type": "component"},
                "emit_to": "nodes",
                "emit": {"id": "$.id", "label": "$.name", "kind": "$.type"},
            },
            {
                "select": "relationships",
                "match": {"type": "communication"},
                "emit_to": "edges",
                "emit": {"id": "$.id", "source": "$.source", "target": "$.target"},
            },
        ],
    }
    out = DeclarativeMappingEngine().apply(source, spec)
    assert len(out["nodes"]) == 3
    assert len(out["edges"]) == 2

def test_tracked_examples_are_deterministic():
    engine = BlueprintEngine(REPO)
    model = load_model()
    targets = {
        "format.mermaid.class": "model.mmd",
        "format.plantuml": "model.puml",
        "format.uml.class": "model.uml.json",
        "format.json-schema": "schema.json",
        "format.xml": "model.xml",
        "format.markdown": "model.md",
    }
    example_dir = REPO / "examples/cross-format/embedded-controller"
    for target, filename in targets.items():
        result, validation = engine.transform(model, target)
        assert validation and validation.ok
        expected = (example_dir / filename).read_text()
        if isinstance(result.content, str):
            actual = result.content
        else:
            actual = json.dumps(result.content, indent=2, sort_keys=True) + "\n"
        assert actual == expected, filename
