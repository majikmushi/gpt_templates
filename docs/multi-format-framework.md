# Multi-Format Representation Framework

The framework separates semantic meaning, abstract model type and concrete representation.

```text
Domain/source data
  -> Canonical semantic model
  -> Abstract representation model
  -> Chosen format
  -> Exact format release
  -> Representation binding
  -> Semantic overlays + style
  -> Optional renderer compatibility
  -> Transform
  -> Target artifact
  -> Validation / provenance / equivalence
```

## Seeded representation systems

- Mermaid
- UML
- PlantUML
- JSON Schema
- XML / XSLT
- Markdown

The same abstract model may have several format bindings. `model.interface-driven-class`, for example, may be represented through Mermaid classDiagram, UML class structures or PlantUML without changing the model's identity.

Capability matching describes fitness/support; it does not silently choose the format.

## Versions

A format ID is stable while format releases are registered separately under `format-versions/`. Generation planning resolves an exact release before compatibility-sensitive binding/style checks. Unknown versions remain unpinned rather than guessed.

## Renderers

A renderer is a separate implementation. Renderer releases are checked against format releases through explicit compatibility contracts. Successful syntax validation does not itself establish renderer compatibility.

## Operational status

`tooling/blueprint_engine/` implements catalog discovery, capability matching, route selection, version-aware generation planning, representation/style binding resolution, validation, provenance and semantic comparison.
