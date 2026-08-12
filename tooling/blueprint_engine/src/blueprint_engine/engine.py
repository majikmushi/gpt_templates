from __future__ import annotations
from pathlib import Path
from typing import Any
from .capabilities import match_formats
from .catalog import scan_artifacts
from .compare import compare_canonical
from .imports import xml_to_canonical, uml_class_to_canonical
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
        return match_formats(self.root / "capability-matrix/formats.yaml", required, allow_partial=allow_partial)

    def route(self, source: str, target: str) -> list[dict[str, Any]]:
        return find_route(self.root / "conversion-graph/graph.yaml", source, target)

    def validate_canonical(self, model: dict[str, Any]) -> ValidationResult:
        return validate_canonical(model, self.root / "canonical/core/model.schema.json")

    def transform(
        self,
        model: dict[str, Any],
        target_format: str,
        *,
        profile_id: str | None = None,
        overlays: list[str] | None = None,
        validate: bool = True,
    ) -> tuple[TransformResult, ValidationResult | None]:
        source_validation = self.validate_canonical(model)
        if not source_validation.ok:
            raise ValueError(f"Canonical source failed validation: {source_validation.as_dict()}")
        result = transform_canonical(model, target_format, profile_id=profile_id, overlays=overlays)
        target_validation = validate_target(target_format, result.content) if validate else None
        return result, target_validation

    def compare(self, a: dict[str, Any], b: dict[str, Any]) -> CompareResult:
        return compare_canonical(a, b)

    def roundtrip_xml(self, model: dict[str, Any]) -> CompareResult:
        transformed, validation = self.transform(model, "format.xml", validate=True)
        if validation is not None and not validation.ok:
            return CompareResult("non-equivalent", notes=["Generated XML failed validation"])
        recovered = xml_to_canonical(transformed.content)
        return self.compare(model, recovered)

    def roundtrip_uml_class(self, model: dict[str, Any]) -> CompareResult:
        transformed, validation = self.transform(model, "format.uml.class", validate=True)
        if validation is not None and not validation.ok:
            return CompareResult("non-equivalent", notes=["Generated UML class interchange model failed validation"])
        recovered = uml_class_to_canonical(transformed.content)
        return self.compare(model, recovered)
