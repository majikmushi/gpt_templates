# GPT Templates / Blueprint Registry

A reusable repository for blueprints, templates, schemas, representation profiles, transforms, validators, fixtures, and documentation.

The repository separates **meaning** from **representation**:

```text
Domain Data
  -> Canonical Model
  -> Blueprint
  -> Representation Profile
  -> Transformer
  -> Target Format
  -> Validator
```

## Core directories

- `blueprints/` - reusable domain or system blueprints.
- `templates/` - target-oriented reusable templates.
- `canonical/` - canonical/intermediate model definitions.
- `formats/` - capabilities, syntax metadata, and constraints for representation languages.
- `profiles/` - semantic mappings from abstract concepts to format primitives.
- `overlays/` - composable visual/semantic encodings such as colour, border, grouping, or icon meaning.
- `transforms/` - declarative/executable transformations between representations.
- `validators/` - syntax, semantic, compatibility, lint, and render validation definitions.
- `schemas/` - schemas governing repository artifact manifests.
- `registry/` - machine-readable capability and artifact catalogues.
- `fixtures/` - valid, invalid, edge-case, and regression examples.
- `examples/` - worked examples.
- `docs/` - repository and format documentation.

## Design principles

1. A format primitive is not limited to its conventional meaning.
2. Representation profiles define how abstract concepts map to available primitives.
3. Visual channels are independent semantic carriers.
4. Critical meaning must not depend on colour alone.
5. Transforms declare fidelity, reversibility, and lossiness.
6. Validators are first-class artifacts.
7. Every reusable artifact has a stable ID and version independent of its path.
8. Generated artifacts should preserve provenance.

See [`docs/architecture.md`](docs/architecture.md) for the model and [`docs/mermaid-representation.md`](docs/mermaid-representation.md) for the initial Mermaid abstraction strategy.
