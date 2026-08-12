# Embedded Controller Cross-Format Example

`model.yaml` is the canonical source.

The executable engine generates:

- `model.mmd` - Mermaid classDiagram
- `model.puml` - PlantUML
- `model.uml.json` - repository UML class interchange object
- `schema.json` - JSON Schema projection
- `model.xml` - repository XML profile
- `model.md` - Markdown presentation

The JSON Schema export intentionally drops relationship topology and records that loss in `x-blueprint-projection`.

The XML and UML-class interchange representations are used by round-trip tests because their current engine mappings preserve the supported structural semantics.
