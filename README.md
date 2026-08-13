# GPT Templates / Representation Framework

A reusable, format-neutral framework for semantic models, abstract representation models, representation formats, bindings, styles, transforms, validators, renderer compatibility, fixtures and provenance.

## Core idea

Describe meaning once, choose the abstract model, choose the representation format, then use explicit bindings to express that model through the chosen format.

```text
Canonical / source semantics
        -> Abstract representation model
        -> Chosen format
        -> Exact format release resolution
        -> Representation binding
        -> Semantic overlays
        -> Style profile
        -> Format style binding
        -> Optional chosen renderer + compatibility contract
        -> Transform / adapter
        -> Concrete artifact
        -> Validation / provenance / equivalence
```

A format is **chosen**, not silently selected. A renderer is also chosen when rendering is requested. `binding: auto` only resolves a compatible binding inside the already chosen format.

## First-class layers

- `canonical/`, `semantics/` - format-independent meaning.
- `abstract-models/` - reusable model types.
- `language-definitions/`, `formats/` - representation-system syntax/metamodel/capabilities.
- `format-versions/` - exact registered releases of formats.
- `representation-bindings/` - abstract-model -> chosen-format mappings.
- `overlays/` - additional semantic dimensions.
- `styles/` - format-neutral presentation intent.
- `style-bindings/` - format-specific realization of style intent.
- `renderers/` - versioned renderer implementations.
- `renderer-compatibility/` - explicit renderer-release <-> format-release support contracts.
- `transforms/`, `adapters/` - execution.
- `validators/`, `provenance/`, `fixtures/` - assurance and evidence.
- `capability-matrix/`, `conversion-graph/` - support/fidelity and conversion routing.

The framework contains 44 first-class abstract model types. Model identity is `model.*`; format-specific mappings are `binding.*`. The former profile-based model layer has been removed.

## Versions and renderers

A format family, a format release, a renderer and a renderer release are separate concepts. A renderer limitation must not be recorded as a limitation of the format itself.

For the source-backed Mermaid class implementation, the current pinned pair is:

- format release: `format-version.mermaid.class.11.4.1`
- renderer: `renderer.mermaid-js`
- renderer release: `11.4.1`
- compatibility contract: `compatibility.renderer.mermaid-js.mermaid-class.11.4.1`

UML and PlantUML are deliberately left version-`unpinned` until source/specification evidence is added. The framework does not invent compatibility ranges.

See [`docs/version-and-renderer-compatibility.md`](docs/version-and-renderer-compatibility.md).

## Executable engine

```bash
blueprint-engine --repo . abstract-model model.interface-driven-class
blueprint-engine --repo . resolve-binding model.interface-driven-class format.mermaid.class
blueprint-engine --repo . format-release format.mermaid.class --version 11.4.1
blueprint-engine --repo . renderer-release renderer.mermaid-js --version 11.4.1
blueprint-engine --repo . renderer-compatibility renderer.mermaid-js 11.4.1 format.mermaid.class 11.4.1
blueprint-engine --repo . generation-plan examples/generation/interface-driven-mermaid.yaml
```

For future development, read [`docs/framework-architecture.md`](docs/framework-architecture.md) first, then [`docs/version-and-renderer-compatibility.md`](docs/version-and-renderer-compatibility.md), [`docs/specification-ingestion.md`](docs/specification-ingestion.md), and [`docs/validation.md`](docs/validation.md).

## Design invariants

1. Abstract models do not choose representation formats.
2. Formats do not own domain-model semantics.
3. Bindings map one abstract model to one chosen format and declare fidelity/loss.
4. Format family and exact format release are distinct.
5. Renderer identity/version and format identity/version are distinct.
6. Renderer compatibility requires an explicit evidence-backed contract when claimed.
7. Semantic overlays add meaning; styles do not.
8. Critical meaning must not depend on colour alone.
9. Syntax validity does not imply semantic equivalence or renderer compatibility.
10. Unknown compatibility remains `unpinned`/`unverified`; it is never guessed.
11. Resolved generation plans and provenance pin exact versions.
12. Round-trip claims are tested, not inferred.
