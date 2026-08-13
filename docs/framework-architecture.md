# Representation Framework Architecture

## Purpose

This repository is a format-neutral representation framework. It describes meaning independently from a representation system, then converts that meaning into a **chosen** format through explicit, version-aware bindings and optional renderer contracts.

Mermaid, UML and PlantUML are representation systems. Interface-Driven Class, Electronics System, Service and Security are abstract representation models.

## Authoritative execution stack

```text
Canonical / source semantics
        |
        v
Abstract representation model
        |
        v
Chosen representation format
        |
        v
Resolve exact format release
        |
        v
Representation binding
        |
        +---- Semantic overlays
        |
        +---- Style profile
        |        |
        |        v
        |   Format style binding
        |
        +---- Optional chosen renderer
                 |
                 v
          Renderer release
                 |
                 v
      Renderer-format compatibility
        |
        v
Transform / adapter
        |
        v
Concrete artifact
        |
        v
Validation + provenance + semantic equivalence
```

The framework does not auto-select a format in normal generation. `binding: auto` means resolve a binding **inside the chosen format**. Renderer selection follows the same rule: renderer compatibility may be checked, but a renderer is not silently substituted.

## Layer 1: semantic/canonical model

Answers **what exists and what does it mean?**

This layer contains canonical entities, relationships, properties, containers, domain/source facts and equivalence semantics. It contains no target syntax or renderer styling assumptions.

## Layer 2: abstract representation models

Answers **what kind of model are we building?**

`abstract-models/registry.yaml` contains reusable model types such as:

- `model.interface-driven-class`
- `model.component`
- `model.service`
- `model.electronics-system`
- `model.security`
- `model.permission-rbac`
- `model.metamodel`

An abstract model defines concepts, relationships, features and constraints. It does not choose Mermaid, UML, PlantUML, or another representation.

## Layer 3: representation systems and versions

Answers **what format was chosen, and which exact release defines its capabilities?**

### Language definitions

`language-definitions/` normalizes grammar, metamodel, constraints, serialization, runtime and conformance evidence from external sources.

### Format identity

A format ID such as `format.mermaid.class` is stable across releases.

### Format release

`format-versions/` records exact releases. Each release may carry source commit/specification version, capabilities and validation evidence.

No backward/forward compatibility is assumed merely from version ordering.

## Layer 4: representation bindings

Answers **how does this abstract model map into this chosen format?**

A binding joins exactly one abstract model to one target format:

```text
model.interface-driven-class
  + format.mermaid.class
  = binding.interface-driven-class.mermaid-class
```

Bindings define primitive mappings, feature mappings, required target capabilities, supported format-version constraints, fidelity and loss.

They never own the model and never choose the format.

## Layer 5: overlays and style

### Semantic overlays

Overlays add semantic dimensions such as lifecycle, trust zone, voltage domain, ownership or criticality. They may request visual channels but remain semantic information.

### Style profiles

Styles alter presentation only: palette, typography, connector appearance, node formatting, density, spacing and layout intent.

### Style bindings

`style-bindings/` maps abstract style intent into the mechanisms exposed by the chosen format release. A style binding declares required capabilities and version compatibility separately from the representation binding.

Semantic meaning always has priority over style preference.

## Layer 6: renderer compatibility

Answers **can this renderer release realize this format release with the capabilities required by the selected bindings?**

The framework deliberately separates:

- renderer identity (`renderer.*`)
- renderer release
- format identity (`format.*`)
- format release (`format-version.*`)
- renderer-format compatibility (`compatibility.renderer.*`)

A renderer compatibility contract is not inferred from syntax validity. It is evidence-backed and may report `native`, `partial`, `unsupported`, or `unverified` support.

Renderer limitations remain renderer limitations; they are not copied into the format definition.

See `docs/version-and-renderer-compatibility.md`.

## Layer 7: execution and assurance

Transforms/adapters execute resolved plans. Validators check canonical structure, target syntax, semantic constraints and runtime behaviour. Provenance records exactly which contracts were used. Semantic comparison determines whether a conversion is exact, equivalent, a projection, or non-equivalent.

Syntax validity, successful rendering and semantic equivalence are three separate claims.

## Generation request

```yaml
abstract_model: model.interface-driven-class
representation:
  format: format.mermaid.class
  version: "11.4.1"
  binding: auto
  renderer:
    id: renderer.mermaid-js
    version: "11.4.1"
  compatibility_mode: strict
style:
  profile: style.technical-dark
  binding: auto
overlays:
  - overlay.visual-channels.base
```

A request may use `version_constraint` instead of exact `version`. Constraints resolve only against releases registered in `format-versions/registry.yaml`; the resolved execution plan always pins one exact release.

## Resolution order

1. validate canonical/source semantics;
2. resolve abstract model;
3. accept the caller-chosen format;
4. resolve an exact registered format release;
5. resolve/validate the representation binding against that release;
6. compose semantic overlays;
7. resolve style profile/style binding and check format capabilities;
8. if a renderer was chosen, resolve its exact release;
9. require a matching renderer-format compatibility contract in strict mode;
10. evaluate effective renderer capabilities;
11. execute transform/adapter;
12. validate artifact;
13. record provenance;
14. run semantic equivalence/round-trip checks where supported.

## Fidelity and loss

Representation bindings use:

- `exact`
- `high`
- `binding-dependent`
- `projection`
- `approximate`
- `lossy`

Transform-level fidelity may be more specific, such as `lossless-for-structural-subset`.

A binding or transform must report omitted/approximated meaning. Visual similarity is not semantic equivalence.

## Version and compatibility states

`source-pinned` / `verified` means evidence exists for the declared scope.

`unpinned` / `unverified` is an intentional state for formats or renderers whose source/specification evidence has not yet been incorporated. The framework must not fabricate a version range to make planning succeed.

## Current registries

- `registry.abstract-models`
- `registry.representation-bindings`
- `registry.semantic-overlays`
- `registry.styles`
- `registry.style-bindings`
- `registry.format-versions`
- `registry.renderers`
- `registry.renderer-compatibility`
- `registry.language-definitions`
- `registry.specification-source-adapters`
- `matrix.format-capabilities`
- `graph.conversions`

## Adding an abstract model

1. add a stable `model.*` ID;
2. define concepts/relationships/features/constraints;
3. validate the model schema;
4. add bindings only for intentionally supported formats;
5. declare fidelity/loss and required format capabilities;
6. add fixtures and semantic tests.

## Adding or updating a format

1. pin specification/source evidence;
2. update/create its normalized language definition;
3. create a `format-version` artifact for each evidence-backed release;
4. enumerate capabilities per release;
5. add/update representation and style bindings with explicit version constraints;
6. implement validation/import/export adapters;
7. add fixtures and round-trip tests;
8. only then change the registry default release.

## Adding or updating a renderer

1. register renderer identity;
2. register exact renderer releases;
3. test against exact format releases;
4. create compatibility contracts containing supported/degraded/unsupported capabilities and known issues;
5. test semantic structures and style realization;
6. only then make a renderer release a default.

## Adding a style

1. add format-neutral presentation intent under `styles/`;
2. avoid embedding target syntax in the style profile;
3. map it through style bindings;
4. declare required capabilities/version ranges;
5. provide graceful presentation fallbacks;
6. never use style to redefine semantics.

## Development invariants

Future changes must preserve these boundaries:

- models do not choose formats;
- format identity is not format release identity;
- bindings map models to chosen formats;
- bindings declare release compatibility and required capabilities;
- overlays add semantics;
- style alters presentation only;
- renderer identity/version is independent from format identity/version;
- renderer support is claimed only through explicit compatibility evidence;
- unknown compatibility remains explicit;
- transforms report loss;
- validators declare authority;
- resolved plans/provenance pin exact versions;
- round-trip/equivalence claims are tested.
