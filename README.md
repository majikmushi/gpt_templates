# GPT Templates / Blueprint Registry

A reusable repository for blueprints, templates, schemas, semantic models, representation
profiles, transforms, validators, fixtures, and documentation.

```text
Domain Data
  -> Canonical Model
  -> Capability Matching
  -> Representation Profile
  -> Transformer / Adapter
  -> Target Format
  -> Validator
  -> Provenance / Semantic Comparison
```

## Executable engine

`tooling/blueprint_engine/` implements catalog discovery, capability matching, conversion
routing, canonical validation, multi-format transforms, declarative XSLT-like mappings,
provenance, semantic comparison and round-trip checks.

Mermaid integration now also includes:

- source-derived validation metadata pinned to `majikmushi/mermaid`;
- Mermaid's own runtime parser as the authoritative syntax checker;
- generic Mermaid AST extraction through `getDiagramFromText()`;
- a classDiagram `ClassDB` -> canonical semantic adapter;
- source-provenance verification down to individual Git blob SHAs.

See [`docs/engine.md`](docs/engine.md),
[`docs/validation.md`](docs/validation.md), and
[`docs/mermaid-source-validation.md`](docs/mermaid-source-validation.md).

## Core directories

- `blueprints/`, `templates/`, `canonical/`, `semantics/`
- `formats/`, `profiles/`, `overlays/`
- `transforms/`, `adapters/`, `validators/`, `renderers/`
- `schemas/`, `capability-matrix/`, `conversion-graph/`
- `catalog/`, `registry/`, `fixtures/`, `examples/`
- `policies/`, `rules/`, `provenance/`, `migrations/`, `packages/`, `benchmarks/`
- `tooling/`, `docs/`

## Design principles

1. A format primitive is not limited to its conventional meaning.
2. Representation profiles make semantic overloading explicit.
3. Visual channels can carry additional semantic dimensions.
4. Critical meaning must not depend on colour alone.
5. Transforms declare fidelity, reversibility and information loss.
6. Validators declare their authority, evidence and degradation mode.
7. Stable artifact IDs are independent of file paths.
8. Generated artifacts preserve provenance.
9. Round-trip claims require semantic comparison tests.
10. Syntax validity does not imply semantic equivalence.

## Mermaid validation authority

The reference Mermaid source is pinned in
`validators/mermaid/source-provenance.yaml`. Static checks are conservative,
source-derived preflight rules; when the optional Node bridge is installed, Mermaid's
own `parse()` is the syntax authority. `--require-runtime` prevents degraded validation
from being mistaken for native parser acceptance.
