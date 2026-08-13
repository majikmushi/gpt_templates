# GPT Templates / Representation Framework

A reusable, format-neutral framework for semantic models, abstract representation models, representation formats, bindings, styles, transforms, validators, fixtures and provenance.

## Core idea

Describe meaning once, choose the abstract model you want, choose the representation format you want, then let explicit bindings map the model into that format.

```text
Canonical / source semantics
        -> Abstract representation model
        -> Chosen format
        -> Representation binding
        -> Semantic overlays
        -> Style profile
        -> Format style binding
        -> Transform / adapter
        -> Concrete artifact
        -> Validation / provenance / equivalence
```

A format is **chosen**, not silently selected. `binding: auto` only resolves a compatible binding within that chosen format.

For example, `model.interface-driven-class` can currently resolve to bindings for Mermaid classDiagram, UML class view, or PlantUML while remaining the same abstract model.

## First-class framework layers

- `canonical/` and `semantics/` - format-independent meaning.
- `abstract-models/` - reusable model types such as interface-driven class, service, electronics, security and RBAC models.
- `language-definitions/` and `formats/` - representation-system capabilities, syntax/metamodel and constraints.
- `representation-bindings/` - model -> chosen-format mappings.
- `overlays/` - additional semantic dimensions.
- `styles/` - format-neutral presentation intent.
- `style-bindings/` - translation of style intent into target-specific styling mechanisms.
- `transforms/` and `adapters/` - execution.
- `validators/`, `provenance/`, `fixtures/` - assurance and evidence.
- `capability-matrix/` and `conversion-graph/` - support/fidelity and conversion routing.

The original 44 class-like domain profiles have been promoted into `registry.abstract-models`. Legacy `profile.domain.*` IDs are retained as aliases rather than being the preferred model identity.

## Representation-system ingestion

External specification evidence is normalized separately from domain modelling:

```text
External language/specification evidence
        -> Specification Source Adapters
        -> Normalized Language Definition
        -> Capabilities / validators / bindings
```

Mermaid currently has source-derived/runtime-backed evidence pinned to `majikmushi/mermaid`. UML is intentionally scaffolded as a metamodel/constraint/serialization-driven language family until a normative version is pinned.

## Executable engine

`tooling/blueprint_engine/` implements catalog discovery, capability matching, conversion routing, canonical validation, language-definition/source-provenance support, abstract-model/binding/style resolution, transforms, semantic comparison and round-trip checks.

New framework commands include:

```bash
blueprint-engine --repo . abstract-model model.interface-driven-class
blueprint-engine --repo . resolve-binding model.interface-driven-class format.mermaid.class
blueprint-engine --repo . style style.technical-dark
blueprint-engine --repo . resolve-style-binding format.mermaid.class
blueprint-engine --repo . generation-plan examples/generation/interface-driven-mermaid.yaml
```

See [`docs/framework-architecture.md`](docs/framework-architecture.md) first for future development. Supporting documentation includes [`docs/specification-ingestion.md`](docs/specification-ingestion.md), [`docs/validation.md`](docs/validation.md), [`docs/visual-encoding.md`](docs/visual-encoding.md), and [`docs/mermaid-source-validation.md`](docs/mermaid-source-validation.md).

## Design invariants

1. Abstract models do not choose representation formats.
2. Representation formats do not own domain-model semantics.
3. Bindings map one abstract model to one chosen format and declare fidelity/loss.
4. Semantic overlays add meaning; style profiles do not.
5. Critical meaning must not depend on colour alone.
6. Styles are portable intent; style bindings perform target-specific realization.
7. Format primitives may be semantically overloaded only through explicit bindings/profiles.
8. Validators declare authority, evidence and degradation mode.
9. Syntax validity does not imply semantic equivalence.
10. Round-trip claims require semantic comparison tests.
11. Language/specification evidence is normalized before being treated as validator/binding authority.
12. Stable artifact IDs are independent of file paths.
