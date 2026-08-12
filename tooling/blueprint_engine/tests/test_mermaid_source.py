from pathlib import Path
import pytest

from blueprint_engine.mermaid_runtime import MermaidRuntimeBridge, MermaidRuntimeUnavailable
from blueprint_engine.mermaid_source import (
    mermaid_class_ast_to_canonical,
    preflight_mermaid_class,
)

REPO = Path(__file__).resolve().parents[3]

def test_source_preflight_accepts_v2_and_directions():
    result = preflight_mermaid_class("classDiagram-v2\n direction LR\n class A")
    assert result.ok, result.as_dict()

def test_source_preflight_rejects_invalid_direction():
    result = preflight_mermaid_class("classDiagram\n direction DOWN\n class A")
    assert not result.ok
    assert any(i.code == "mermaid.class.direction" for i in result.issues)

def test_source_preflight_requires_quoted_note_text():
    result = preflight_mermaid_class("classDiagram\n note not-quoted")
    assert not result.ok
    assert any(i.code == "mermaid.class.note-text" for i in result.issues)

def test_class_ast_adapter_uses_native_relation_codes():
    ast = {
        "kind": "mermaid-class-ast",
        "diagramType": "classDiagram",
        "direction": "LR",
        "classes": [
            {"id": "A", "type": "", "label": "A", "members": [], "methods": [], "annotations": [], "cssClasses": "default", "styles": [], "parent": None, "link": None, "linkTarget": None, "tooltip": None},
            {"id": "B", "type": "", "label": "B", "members": [], "methods": [], "annotations": [], "cssClasses": "default", "styles": [], "parent": "N", "link": None, "linkTarget": None, "tooltip": None},
        ],
        "relations": [{
            "id1": "A", "id2": "B", "title": "contains",
            "relationTitle1": "1", "relationTitle2": "many",
            "relation": {"type1": 2, "type2": "none", "lineType": 0}
        }],
        "namespaces": [{"id": "N", "classIds": ["B"], "childIds": []}],
        "notes": [],
        "accessibility": {"title": None, "description": None, "diagramTitle": None},
    }
    model = mermaid_class_ast_to_canonical(ast, model_id="test.model")
    assert model["elements"][0]["id"] == "A"
    assert model["relationships"][0]["semantics"] == ["composition"]
    assert model["relationships"][0]["source_cardinality"] == "1"
    assert model["relationships"][0]["target_cardinality"] == "many"
    assert model["containers"][0]["members"] == ["B"]
    assert model["metadata"]["direction"] == "LR"

def test_runtime_unavailable_is_explicit():
    bridge = MermaidRuntimeBridge(REPO, node_binary="definitely-not-a-real-node-binary")
    with pytest.raises(MermaidRuntimeUnavailable):
        bridge.validate("classDiagram\nclass A")

def test_source_preflight_accepts_leading_comment():
    result = preflight_mermaid_class("%% comment\nclassDiagram\nclass A")
    assert result.ok, result.as_dict()
