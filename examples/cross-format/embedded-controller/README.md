# Embedded Controller Cross-Format Example

One small system is represented through several targets.

- `model.yaml` is the canonical semantic form.
- `model.mmd` is a Mermaid class-diagram projection.
- `model.puml` is a PlantUML class-diagram projection.
- `schema.json` is a JSON Schema projection of configuration structure, not full communication semantics.
- `model.xml` is a hierarchical structured representation.

The representations are not automatically semantically identical. The round-trip fixture declares what each path is expected to preserve or lose.
