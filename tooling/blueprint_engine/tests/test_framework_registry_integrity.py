from pathlib import Path

import pytest
import yaml

from blueprint_engine.engine import BlueprintEngine

REPO = Path(__file__).resolve().parents[3]


def _load(path: str):
    return yaml.safe_load((REPO / path).read_text(encoding="utf-8"))


def test_all_representation_bindings_validate_and_reference_registered_models():
    engine = BlueprintEngine(REPO)
    model_ids = {entry["id"] for entry in _load("abstract-models/registry.yaml")["models"]}
    for entry in _load("representation-bindings/registry.yaml")["bindings"]:
        assert entry["model"] in model_ids
        value = _load(entry["path"])
        result = engine.validate_framework_artifact(value, "representation-binding")
        assert result.ok, (entry["path"], result.as_dict())
        assert value["model"] == entry["model"]
        assert value["format"] == entry["format"]


def test_all_styles_validate():
    engine = BlueprintEngine(REPO)
    for entry in _load("styles/registry.yaml")["styles"]:
        value = _load(entry["path"])
        result = engine.validate_framework_artifact(value, "style-profile")
        assert result.ok, (entry["path"], result.as_dict())


def test_all_style_bindings_validate_and_match_registry_format():
    engine = BlueprintEngine(REPO)
    for entry in _load("style-bindings/registry.yaml")["bindings"]:
        value = _load(entry["path"])
        result = engine.validate_framework_artifact(value, "style-binding")
        assert result.ok, (entry["path"], result.as_dict())
        assert value["format"] == entry["format"]


def test_format_renderer_and_compatibility_artifacts_validate():
    engine = BlueprintEngine(REPO)
    release = _load("format-versions/mermaid-class-11.4.1.yaml")
    renderer = _load("renderers/mermaid-js.yaml")
    compatibility = _load("renderer-compatibility/mermaid-js-mermaid-class-11.4.1.yaml")
    assert engine.validate_framework_artifact(release, "format-version").ok
    assert engine.validate_framework_artifact(renderer, "renderer").ok
    assert engine.validate_framework_artifact(compatibility, "renderer-compatibility").ok


def test_removed_profile_layer_is_not_resolvable_or_present():
    engine = BlueprintEngine(REPO)
    with pytest.raises(KeyError):
        engine.abstract_model("profile.domain.interface-driven-model")
    assert not (REPO / "profiles/domain/class-like-models.yaml").exists()
    assert not (REPO / "profiles/mermaid/class/registry.yaml").exists()
    assert not (REPO / "schemas/representation-profile.schema.json").exists()
