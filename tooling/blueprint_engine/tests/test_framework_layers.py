from pathlib import Path

import yaml

from blueprint_engine.engine import BlueprintEngine

REPO = Path(__file__).resolve().parents[3]


def test_abstract_model_registry_contains_44_models():
    registry = yaml.safe_load((REPO / "abstract-models/registry.yaml").read_text(encoding="utf-8"))
    assert len(registry["models"]) == 44
    assert registry["selection_policy"]["format_is_user_chosen"] is True


def test_detailed_abstract_model_validates():
    engine = BlueprintEngine(REPO)
    model = engine.abstract_model("model.interface-driven-class")
    result = engine.validate_framework_artifact(model, "abstract-model")
    assert result.ok, result.as_dict()


def test_chosen_format_resolves_binding_and_pinned_default_version():
    engine = BlueprintEngine(REPO)
    request = {
        "abstract_model": "model.interface-driven-class",
        "representation": {"format": "format.mermaid.class", "binding": "auto"},
        "style": {"profile": "style.technical-dark", "binding": "auto"},
        "overlays": ["overlay.visual-channels.base"],
    }
    plan = engine.plan_generation(request)
    assert plan["ok"] is True
    assert plan["selection"]["chosen_format"] == "format.mermaid.class"
    assert plan["selection"]["format_selection"] == "chosen-not-auto-selected"
    assert plan["selection"]["format_version"] == "11.4.1"
    assert plan["selection"]["representation_binding"] == "binding.interface-driven-class.mermaid-class"
    assert plan["selection"]["style_binding"] == "style-binding.mermaid.class"


def test_renderer_compatibility_is_explicit_and_versioned():
    engine = BlueprintEngine(REPO)
    plan = engine.plan_generation({
        "abstract_model": "model.interface-driven-class",
        "representation": {
            "format": "format.mermaid.class",
            "version": "11.4.1",
            "renderer": {"id": "renderer.mermaid-js", "version": "11.4.1"},
        },
        "style": {"profile": "style.neutral-technical"},
    })
    assert plan["ok"] is True, plan
    assert plan["selection"]["renderer"] == "renderer.mermaid-js"
    assert plan["selection"]["renderer_version"] == "11.4.1"
    assert plan["selection"]["renderer_compatibility"] == "compatibility.renderer.mermaid-js.mermaid-class.11.4.1"


def test_format_constraint_resolves_to_exact_registered_release():
    engine = BlueprintEngine(REPO)
    release = engine.format_release("format.mermaid.class", version_constraint=">=11,<12")
    assert release["status"] == "resolved"
    assert release["version"] == "11.4.1"


def test_unpinned_format_is_reported_without_false_version_claim():
    engine = BlueprintEngine(REPO)
    release = engine.format_release("format.uml.class")
    assert release["status"] == "unpinned"
    assert release["version"] is None


def test_same_abstract_model_can_bind_to_multiple_formats():
    engine = BlueprintEngine(REPO)
    ids = {engine.resolve_representation_binding("model.interface-driven-class", fmt)["id"] for fmt in ("format.mermaid.class", "format.uml.class", "format.plantuml")}
    assert ids == {"binding.interface-driven-class.mermaid-class", "binding.interface-driven-class.uml-class", "binding.interface-driven-class.plantuml"}


def test_generation_request_requires_chosen_format():
    engine = BlueprintEngine(REPO)
    result = engine.validate_framework_artifact({"abstract_model": "model.interface-driven-class", "representation": {}}, "generation-request")
    assert not result.ok


def test_style_is_independent_of_model_binding():
    engine = BlueprintEngine(REPO)
    style = engine.style("style.technical-dark")
    style_binding = engine.resolve_style_binding("format.mermaid.class")
    assert style["kind"] == "style-profile"
    assert style_binding["kind"] == "style-binding"
    assert "model" not in style
