# Validators

Validator manifests describe authoritative scope, provenance and implementation.

Executable core validation lives in `tooling/blueprint_engine/src/blueprint_engine/validators.py`.

Current checks range from native meta-schema/parsing checks (JSON Schema, XML) to deliberately limited repository-subset checks (Mermaid, UML, PlantUML). Full Mermaid validation remains pending source-derived implementation.
