# GPT Templates / Blueprint Registry

A reusable repository for blueprints, templates, schemas, semantic models, representation profiles, transforms, validators, fixtures, and documentation.

The repository separates **meaning** from **representation** and now includes an executable core:

```text
Domain Data
  -> Canonical Model
  -> Capability Matching
  -> Representation Profile
  -> Transformer
  -> Target Format
  -> Validator
  -> Provenance / Semantic Comparison
```

## Executable engine

`tooling/blueprint_engine/` implements:

- artifact catalog discovery
- format capability matching
- conversion-route selection
- canonical model validation
- transforms to Mermaid, PlantUML, UML class interchange, JSON Schema, XML and Markdown
- declarative XSLT-like object mapping
- target validation
- deterministic provenance hashes
- semantic comparison
- XML and UML-class round-trip checks

See [`docs/engine.md`](docs/engine.md).

## Core directories

- `blueprints/` - reusable domain/system blueprints.
- `templates/` - target-oriented reusable templates.
- `canonical/` - canonical/intermediate semantic models.
- `semantics/` - shared semantic vocabulary and equivalence rules.
- `formats/` - representation-language capabilities and constraints.
- `profiles/` - mappings from abstract concepts to format primitives.
- `overlays/` - composable visual/semantic encodings.
- `transforms/` - declarative and built-in transformation contracts.
- `validators/` - validation manifests and scope declarations.
- `schemas/` - schemas governing repository artifacts.
- `capability-matrix/` - cross-format expressiveness matrix.
- `conversion-graph/` - executable conversion routing metadata.
- `catalog/` and `registry/` - discovery metadata.
- `adapters/` and `renderers/` - serialization/import and presentation boundaries.
- `fixtures/` and `examples/` - test and worked examples.
- `policies/`, `rules/`, `provenance/`, `migrations/`, `packages/`, `benchmarks/` - governance and lifecycle support.
- `tooling/` - executable framework tooling.
- `docs/` - architecture and usage documentation.

## Design principles

1. A format primitive is not limited to its conventional meaning.
2. Representation profiles make semantic overloading explicit.
3. Visual channels can carry additional semantic dimensions.
4. Critical meaning must not depend on colour alone.
5. Transforms declare fidelity, reversibility and information loss.
6. Validators are first-class artifacts and must declare their authority/scope.
7. Stable artifact IDs are independent of file paths.
8. Generated artifacts preserve provenance.
9. Round-trip claims require semantic comparison tests.
10. A syntactically valid output is not automatically semantically equivalent.

## Validation boundary

The implemented Mermaid checker validates the engine-generated `classDiagram` subset only. A full Mermaid validator will be derived later from Mermaid grammar/source/runtime behaviour rather than guessed from documentation.
