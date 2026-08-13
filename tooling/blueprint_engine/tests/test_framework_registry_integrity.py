from pathlib import Path

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


def test_legacy_domain_profile_aliases_are_one_to_one():
    new_registry = _load("abstract-models/registry.yaml")
    legacy_registry = _load("profiles/domain/class-like-models.yaml")
    aliases = {entry["legacy_alias"]: entry["id"] for entry in new_registry["models"]}
    assert len(aliases) == 44
    for entry in legacy_registry["profiles"]:
        assert aliases[entry["id"]] == entry["abstract_model"]
