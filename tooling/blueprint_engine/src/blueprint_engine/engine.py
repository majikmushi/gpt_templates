from __future__ import annotations

from pathlib import Path
from typing import Any

from .capabilities import match_formats
from .catalog import scan_artifacts
from .compare import compare_canonical
from .compatibility import (
    load_renderer,
    resolve_format_release,
    resolve_renderer_compatibility,
    resolve_renderer_release,
)
from .framework_layers import (
    load_abstract_model,
    load_representation_binding,
    load_style,
    load_style_binding,
    plan_generation,
    resolve_representation_binding,
    resolve_style_binding,
    validate_framework_artifact,
)
from .imports import uml_class_to_canonical, xml_to_canonical
from .language_definitions import (
    load_language_definition,
    validate_language_definition,
    validate_specification_source_adapter,
)
from .mermaid_runtime import MermaidRuntimeBridge, MermaidRuntimeError, MermaidRuntimeUnavailable
from .mermaid_source import mermaid_class_ast_to_canonical
from .models import CompareResult, MatchResult, TransformResult, ValidationResult
from .routing import find_route
from .source_provenance import check_git_source
from .transforms import transform_canonical
from .validators import validate_canonical, validate_target


class BlueprintEngine:
    def __init__(self, repository_root: str | Path):
        self.root = Path(repository_root)

    def catalog(self) -> list[dict[str, Any]]:
        return scan_artifacts(self.root)

    def match(self, required: list[str], *, allow_partial: bool = False) -> list[MatchResult]:
        return match_formats(self.root / "capability-matrix/formats.yaml", required, allow_partial=allow_partial)

    def route(self, source: str, target: str) -> list[dict[str, Any]]:
        return find_route(self.root / "conversion-graph/graph.yaml", source, target)

    def language_definition(self, definition_id: str) -> dict[str, Any]:
        return load_language_definition(self.root, definition_id)

    def validate_language_definition(self, value: dict[str, Any]) -> ValidationResult:
        return validate_language_definition(value, self.root / "schemas/language-definition.schema.json")

    def validate_specification_source_adapter(self, value: dict[str, Any]) -> ValidationResult:
        return validate_specification_source_adapter(value, self.root / "schemas/specification-source-adapter.schema.json")

    def abstract_model(self, model_id: str) -> dict[str, Any]:
        return load_abstract_model(self.root, model_id)

    def representation_binding(self, binding_id: str) -> dict[str, Any]:
        return load_representation_binding(self.root, binding_id)

    def resolve_representation_binding(self, model_id: str, chosen_format: str) -> dict[str, Any]:
        return resolve_representation_binding(self.root, model_id, chosen_format)

    def style(self, style_id: str) -> dict[str, Any]:
        return load_style(self.root, style_id)

    def style_binding(self, binding_id: str) -> dict[str, Any]:
        return load_style_binding(self.root, binding_id)

    def resolve_style_binding(self, chosen_format: str) -> dict[str, Any]:
        return resolve_style_binding(self.root, chosen_format)

    def format_release(self, format_id: str, *, version: str | None = None, version_constraint: str | None = None) -> dict[str, Any]:
        return resolve_format_release(self.root, format_id, version=version, version_constraint=version_constraint)

    def renderer(self, renderer_id: str) -> dict[str, Any]:
        return load_renderer(self.root, renderer_id)

    def renderer_release(self, renderer_id: str, *, version: str | None = None) -> dict[str, Any]:
        return resolve_renderer_release(self.root, renderer_id, version=version)

    def renderer_compatibility(self, renderer_id: str, renderer_version: str, format_id: str, format_version: str) -> dict[str, Any] | None:
        return resolve_renderer_compatibility(
            self.root,
            renderer_id=renderer_id,
            renderer_version=renderer_version,
            format_id=format_id,
            format_version=format_version,
        )

    def validate_framework_artifact(self, value: dict[str, Any], artifact_kind: str) -> ValidationResult:
        return validate_framework_artifact(self.root, value, artifact_kind)

    def plan_generation(self, request: dict[str, Any]) -> dict[str, Any]:
        return plan_generation(self.root, request)

    def check_source_provenance(self, source_root: str | Path, provenance: str | Path | dict[str, Any]) -> dict[str, Any]:
        if not isinstance(provenance, dict):
            path = Path(provenance)
            if not path.is_absolute():
                path = self.root / path
            provenance = path
        return check_git_source(source_root, provenance)

    def validate_canonical(self, model: dict[str, Any]) -> ValidationResult:
        return validate_canonical(model, self.root / "canonical/core/model.schema.json")

    def validate_target(self, target_format: str, content: Any, *, require_runtime: bool = False) -> ValidationResult:
        return validate_target(target_format, content, repository_root=self.root, require_runtime=require_runtime)

    def transform(
        self,
        model: dict[str, Any],
        target_format: str,
        *,
        binding_id: str | None = None,
        overlays: list[str] | None = None,
        format_version: str | None = None,
        validate: bool = True,
        require_runtime: bool = False,
    ) -> tuple[TransformResult, ValidationResult | None]:
        source_validation = self.validate_canonical(model)
        if not source_validation.ok:
            raise ValueError(f"Canonical source failed validation: {source_validation.as_dict()}")
        result = transform_canonical(
            model,
            target_format,
            binding_id=binding_id,
            overlays=overlays,
            format_version=format_version,
        )
        target_validation = self.validate_target(target_format, result.content, require_runtime=require_runtime) if validate else None
        return result, target_validation

    def compare(self, a: dict[str, Any], b: dict[str, Any]) -> CompareResult:
        return compare_canonical(a, b)

    def mermaid_ast(self, text: str) -> dict[str, Any]:
        bridge = MermaidRuntimeBridge(self.root)
        runtime = bridge.ast(text)
        if not runtime.ok:
            error = runtime.error or {}
            if error.get("code") == "runtime-unavailable":
                raise MermaidRuntimeUnavailable(error.get("message", "Mermaid runtime unavailable"))
            raise MermaidRuntimeError(error.get("message", "Mermaid runtime rejected the diagram"))
        if runtime.ast is None:
            raise MermaidRuntimeError("Mermaid runtime returned no AST")
        return runtime.ast

    def mermaid_class_to_canonical(
        self,
        text: str,
        *,
        model_id: str = "imported.mermaid.class",
        binding_id: str | None = None,
    ) -> dict[str, Any]:
        validation = self.validate_target("format.mermaid.class", text, require_runtime=True)
        if not validation.ok:
            raise ValueError(f"Mermaid source failed validation: {validation.as_dict()}")
        ast = self.mermaid_ast(text)
        model = mermaid_class_ast_to_canonical(ast, model_id=model_id, binding_id=binding_id)
        canonical_validation = self.validate_canonical(model)
        if not canonical_validation.ok:
            raise ValueError(f"Mermaid AST adapter produced invalid canonical model: {canonical_validation.as_dict()}")
        return model

    def roundtrip_xml(self, model: dict[str, Any]) -> CompareResult:
        transformed, validation = self.transform(model, "format.xml", validate=True)
        if validation is not None and not validation.ok:
            return CompareResult("non-equivalent", notes=["Generated XML failed validation"])
        return self.compare(model, xml_to_canonical(transformed.content))

    def roundtrip_uml_class(self, model: dict[str, Any]) -> CompareResult:
        transformed, validation = self.transform(model, "format.uml.class", validate=True)
        if validation is not None and not validation.ok:
            return CompareResult("non-equivalent", notes=["Generated UML class interchange model failed validation"])
        return self.compare(model, uml_class_to_canonical(transformed.content))
