# GPT Templates / Blueprint Registry

A reusable repository for blueprints, templates, schemas, semantic models, representation profiles, transforms, validators, fixtures and documentation.

```text
External language/specification evidence
  -> Specification Source Adapters
  -> Normalized Language Definition
  -> Canonical / Representation Semantics
  -> Capability Matching
  -> Representation Profile
  -> Transformer / Adapter
  -> Target Format
  -> Validator
  -> Provenance / Semantic Comparison
```

## Executable engine

`tooling/blueprint_engine/` implements catalog discovery, capability matching, conversion routing, canonical validation, multi-format transforms, declarative XSLT-like mappings, source provenance checks, normalized language-definition validation, semantic comparison and round-trip checks.

Mermaid integration includes source-derived metadata pinned to `majikmushi/mermaid`, Mermaid's own runtime parser as syntax authority, generic AST extraction through `getDiagramFromText()`, a classDiagram `ClassDB` -> canonical adapter, and source verification down to Git blob SHAs.

The framework is no longer Mermaid-shaped at the ingestion boundary. `language-definitions/` and `adapters/specification/` provide a common path for grammar-driven languages, metamodel-driven languages such as future UML ingestion, schema-driven formats, runtime-defined languages and conformance-test evidence.

See [`docs/specification-ingestion.md`](docs/specification-ingestion.md), [`docs/engine.md`](docs/engine.md), [`docs/validation.md`](docs/validation.md), and [`docs/mermaid-source-validation.md`](docs/mermaid-source-validation.md).

## Core directories

- `blueprints/`, `templates/`, `canonical/`, `semantics/`
- `language-definitions/`, `formats/`, `profiles/`, `overlays/`
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
7. Language/specification evidence is normalized before validator generation.
8. Authority is tracked per source, not assumed for an entire language definition.
9. Stable artifact IDs are independent of file paths.
10. Generated artifacts preserve provenance.
11. Round-trip claims require semantic comparison tests.
12. Syntax validity does not imply semantic equivalence.

## Mermaid validation authority

The reference Mermaid source is pinned in `validators/mermaid/source-provenance.yaml`. Static checks are conservative source-derived preflight rules; when the optional Node bridge is installed, Mermaid's own `parse()` is the syntax authority. `--require-runtime` prevents degraded validation from being mistaken for native parser acceptance.

## UML readiness

UML is represented as a metamodel/semantic language family rather than a single text grammar. `language-definitions/uml/manifest.yaml` is intentionally unpinned until a concrete UML specification version and evidence set are selected. Future metamodel, constraint and XMI/serialization adapters can feed the same normalized language-definition layer without changing the core architecture.
