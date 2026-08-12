from pathlib import Path

import yaml

from blueprint_engine import BlueprintEngine
from blueprint_engine.source_provenance import git_blob_sha

REPO = Path(__file__).resolve().parents[3]


def test_language_definition_registry_and_schema():
    engine = BlueprintEngine(REPO)
    mermaid = engine.language_definition("language.mermaid.class-diagram")
    uml = engine.language_definition("language.uml")
    assert engine.validate_language_definition(mermaid).ok
    assert engine.validate_language_definition(uml).ok
    assert mermaid["runtime"]["parser_api"] == "mermaid.parse"
    assert uml["status"] == "scaffold-unpinned"


def test_specification_source_adapter_schemas():
    engine = BlueprintEngine(REPO)
    for relative in (
        "adapters/specification/mermaid.yaml",
        "adapters/specification/uml.yaml",
    ):
        value = yaml.safe_load((REPO / relative).read_text(encoding="utf-8"))
        result = engine.validate_specification_source_adapter(value)
        assert result.ok, (relative, result.as_dict())


def test_git_blob_sha_is_deterministic():
    payload = b"normalized language definition\n"
    assert git_blob_sha(payload) == git_blob_sha(payload)
    assert len(git_blob_sha(payload)) == 40
