# GPT Templates / Blueprint Registry

A reusable repository for blueprints, templates, schemas, semantic models, representation profiles, transforms, validators, adapters, renderers, fixtures, benchmarks, packages, and documentation.

```text
Domain Data
  -> Canonical Semantic Model
  -> Blueprint
  -> Capability Matching
  -> Representation Profile + Overlays
  -> Transformer / Adapter
  -> Target Format
  -> Validator
  -> Renderer
  -> Semantic Equivalence / Round-Trip Check
```

## Seed representation families

- Mermaid
- UML
- PlantUML
- JSON Schema
- XML + XSLT
- Markdown

These intentionally cover different representation classes: diagrams, formal models, structured trees, validation schemas, transformation languages and documents.

## Core directories

- `blueprints/`, `templates/`, `canonical/`, `semantics/`
- `formats/`, `profiles/`, `overlays/`
- `capability-matrix/`, `conversion-graph/`
- `transforms/`, `adapters/`, `validators/`, `renderers/`
- `schemas/`, `rules/`, `policies/`, `catalog/`
- `fixtures/`, `examples/`, `benchmarks/`
- `provenance/`, `migrations/`, `packages/`, `tooling/`, `docs/`

## Design principles

1. A primitive is not limited to its conventional meaning.
2. Semantic overloading is explicit through representation profiles.
3. Visual channels can carry independent semantic dimensions.
4. Critical meaning must not rely on colour alone.
5. Transforms declare fidelity, reversibility, determinism and lossiness.
6. Validators are first-class artifacts and record rule provenance.
7. Reusable artifacts have stable IDs independent of path.
8. Generated artifacts preserve provenance and transform history.
9. Capability matching selects representations by what they can express.
10. Round-trip safety is established through semantic-equivalence fixtures, not syntax success.

Start with [`docs/multi-format-framework.md`](docs/multi-format-framework.md), [`docs/architecture.md`](docs/architecture.md), and [`docs/transformation-routing.md`](docs/transformation-routing.md).
