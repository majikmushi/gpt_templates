from __future__ import annotations

from pathlib import Path
from typing import Any

from .capabilities import match_formats
from .catalog import scan_artifacts
from .compare import compare_canonical
from .imports import uml_class_to_canonical, xml_to_canonical
from .mermaid_runtime import MermaidRuntimeBridge, MermaidRuntimeError, MermaidRuntimeUnavailable
from .mermaid_source import mermaid_class_ast_to_canonical
from .models import CompareResult, MatchResult, TransformResult, ValidationResult
from .routing import find_route
from .transforms import transform_canonical
from .validators import validate_canonical, validate_target


class BlueprintEngine:
    def __init__(self, repository_root: str | Path):
        self.root = Path(repository_root)

    def catalog(self) -> list[dict[str, Any]]:
        return scan_artifacts(self.root)

    def match(self, required: list[str], *, allow_partial: bool = False) -> list[MatchResult]:
        return match_formats(
            self.root / "capability-matrix/formats.yaml",
            required,
            allow_partial=allow_partial,
        )

    def route(self, source: str, target: str) -> list[dict[str, Any]]:
        return find_route(self.root / "conversion-graph/graph.yaml", source, target)

    def validate_canonical(self, model: dict[str, Any]) -> ValidationResult:
        return validate_canonical(model, self.root / "canonical/core/model.schema.json")

    def validate_target(
        self,
        target_format: str,
        content: Any,
        *,
        require_runtime: bool = False,
    ) -> ValidationResult:
        return validate_target(
            target_format,
            content,
            repository_root=self.root,
            require_runtime=require_runtime,
        )

    def transform(
        self,
        model: dict[str, Any],
        target_format: str,
        *,
        profile_id: str | None = None,
        overlays: list[str] | None = None,
        validate: bool = True,
        require_runtime: bool = False,
    ) -> tuple[TransformResult, ValidationResult | None]:
        source_validation = self.validate_canonical(model)
        if not source_validation.ok:
            raise ValueError(
                f"Canonical source failed validation: {source_validation.as_dict()}"
            )
        result = transform_canonical(
            model,
            target_format,
            profile_id=profile_id,
            overlays=overlays,
        )
        target_validation = (
            self.validate_target(
                target_format,
                result.content,
                require_runtime=require_runtime,
            )
            if validate
            else None
        )
        return result, target_validation

    def compare(self, a: dict[str, Any], b: dict[str, Any]) -> CompareResult:
        return compare_canonical(a, b)

    def mermaid_ast(self, text: str) -> dict[str, Any]:
        bridge = MermaidRuntimeBridge(self.root)
        runtime = bridge.ast(text)
        if not runtime.ok:
            error = runtime.error or {}
            code = error.get("code")
            if code == "runtime-unavailable":
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
        profile_id: str | None = None,
    ) -> dict[str, Any]:
        validation = self.validate_target(
            "format.mermaid.class",
            text,
            require_runtime=True,
        )
        if not validation.ok:
            raise ValueError(f"Mermaid source failed validation: {validation.as_dict()}")
        ast = self.mermaid_ast(text)
        model = mermaid_class_ast_to_canonical(
            ast,
            model_id=model_id,
            profile_id=profile_id,
        )
        canonical_validation = self.validate_canonical(model)
        if not canonical_validation.ok:
            raise ValueError(
                "Mermaid AST adapter produced invalid canonical model: "
                f"{canonical_validation.as_dict()}"
            )
        return model

    def roundtrip_xml(self, model: dict[str, Any]) -> CompareResult:
        transformed, validation = self.transform(model, "format.xml", validate=True)
        if validation is not None and not validation.ok:
            return CompareResult(
                "non-equivalent",
                notes=["Generated XML failed validation"],
            )
        recovered = xml_to_canonical(transformed.content)
        return self.compare(model, recovered)

    def roundtrip_uml_class(self, model: dict[str, Any]) -> CompareResult:
        transformed, validation = self.transform(model, "format.uml.class", validate=True)
        if validation is not None and not validation.ok:
            return CompareResult(
                "non-equivalent",
                notes=["Generated UML class interchange model failed validation"],
            )
        recovered = uml_class_to_canonical(transformed.content)
        return self.compare(model, recovered)
