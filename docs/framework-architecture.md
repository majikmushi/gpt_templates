# Representation Framework Architecture

## Purpose

The repository is a format-neutral representation framework. Its core job is to describe meaning once, select an abstract model for that meaning, and express that model through a **chosen** representation format using explicit bindings, overlays and styles.

Mermaid, UML and PlantUML are representation systems. They are not abstract model types. An Interface-Driven Class Model, Electronics System Model, Service Model or Security Model is an abstract model and may have bindings to several representation systems.

## Core invariant

The framework does **not** automatically choose a representation format unless a future caller explicitly asks for format recommendation/selection. A normal generation request contains a chosen format.

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
Representation binding
        |
        +---- Semantic overlays
        |
        +---- Style profile
                  |
                  v
           Format style binding
        |
        v
Transform / adapter
        |
        v
Concrete artifact
        |
        v
Validation + provenance + equivalence
```

`binding: auto` means "resolve a compatible binding for the already chosen format". It must never mean "choose a format".

## The five architectural layers

### 1. Semantic and canonical layer

Answers: **what exists and what does it mean?**

Primary artifacts:

- canonical semantic model;
- domain/source data;
- semantic vocabulary;
- blueprints and templates where they describe domain intent;
- equivalence rules.

This layer is independent of concrete diagram syntax, styling and renderer behaviour.

### 2. Abstract representation model layer

Answers: **what kind of model are we making?**

Examples:

- `model.interface-driven-class`;
- `model.component`;
- `model.service`;
- `model.electronics-system`;
- `model.security`;
- `model.permission-rbac`;
- `model.metamodel`.

An abstract model defines concepts, relationships, features and constraints without deciding whether they will become Mermaid classes, UML elements, PlantUML constructs, Graphviz nodes or another representation.

The registry is `abstract-models/registry.yaml`.

### 3. Representation layer

Answers: **which chosen format will carry the model, and how?**

A representation binding joins exactly one abstract model to exactly one target format:

```text
model.interface-driven-class
        +
format.mermaid.class
        =
binding.interface-driven-class.mermaid-class
```

The same model can have another binding:

```text
model.interface-driven-class
        +
format.uml.class
        =
binding.interface-driven-class.uml-class
```

Bindings declare primitive mappings, feature mappings, fidelity and known losses. They do not own the abstract model and do not choose the target format.

The registry is `representation-bindings/registry.yaml`.

### 4. Semantic overlay and presentation style layer

This layer intentionally has two independent mechanisms.

#### Semantic overlays

Overlays add meaning that is orthogonal to the base model, for example:

- trust zone;
- lifecycle;
- voltage domain;
- ownership;
- criticality;
- deployment zone.

An overlay may request visual channels but the information remains semantic. If colour is used for a critical semantic distinction, a non-colour fallback is required.

#### Style profiles

Styles change presentation, not meaning. Examples include:

- colour palette;
- light/dark theme;
- typography;
- connector weight/pattern preferences;
- node border/corner treatment;
- grouping presentation;
- spacing/density;
- layout intent.

`styles/` stores abstract style intent. `style-bindings/` translates that intent into capabilities of the chosen format. A style profile therefore stays portable while its concrete realization is format-specific.

A style rule must not silently redefine a semantic relationship. For example, a style may prefer dotted dependency connectors only when doing so does not conflict with the chosen representation binding's semantic use of connector patterns.

### 5. Execution and assurance layer

Answers: **how is the selected plan executed and verified?**

Includes:

- capability matrix;
- conversion graph;
- transform/adapters;
- validators;
- runtime parsers;
- semantic comparison;
- round-trip tests;
- source provenance;
- language-definition provenance;
- CLI/tool contracts.

Validation is layered. Syntax validity does not imply semantic equivalence, and successful rendering does not imply that an abstract model survived a lossy mapping.

## Language definitions are separate from abstract models

`language-definitions/` describes representation systems themselves: syntax, metamodel, constraints, serializations, runtime behaviour and conformance evidence.

Examples:

- Mermaid is grammar/runtime/DB/test driven;
- UML is metamodel/constraint/serialization driven;
- a schema language may be metaschema driven.

These definitions inform format capabilities, validators and representation bindings. They do not define the domain model being represented.

```text
External specification evidence
        |
Specification source adapters
        |
Normalized Language Definition
        |
   +----+------------------+
   |                       |
Format capabilities      Validators
   |                       |
   +--------> Representation binding
```

## Generation request contract

A request should look conceptually like:

```yaml
abstract_model: model.interface-driven-class
representation:
  format: format.mermaid.class
  binding: auto
style:
  profile: style.technical-dark
  binding: auto
overlays:
  - overlay.visual-channels.base
options:
  layout: left-to-right
```

The important part is that `representation.format` is supplied. The resolver may select a binding only inside that chosen format.

The machine-readable contract is `schemas/generation-request.schema.json`.

## Binding resolution

Given `(abstract_model, chosen_format)`:

1. resolve the abstract model;
2. search `representation-bindings/registry.yaml` for that exact model/format pair;
3. if one binding exists, use it when `binding: auto`;
4. if none exist, fail with an unsupported-pair error;
5. if several exist, require an explicit binding;
6. never change the chosen format to make a binding available.

Style binding resolution follows the same principle but is keyed by the already chosen format.

## Fidelity and loss

Bindings and transforms must declare fidelity independently.

Suggested levels:

- `exact` - semantics and structure preserved;
- `high` - intended model semantics preserved with representation differences;
- `profile-dependent` - equivalence depends on an explicit profile/binding;
- `projection` - a deliberate subset/view;
- `approximate` - some concepts represented by convention;
- `lossy` - known semantic information is omitted.

A visually similar artifact is not automatically equivalent.

## Style versus semantic collision policy

The resolver/renderer should use this priority:

1. preserve abstract-model semantics;
2. preserve semantic-overlay semantics;
3. preserve target-format validity;
4. apply style intent where compatible;
5. remap style channels if possible;
6. fall back to textual/structural encoding for semantic information;
7. report style losses rather than corrupt semantics.

Style is always lower priority than semantic meaning.

## Current first-class registries

- `registry.abstract-models`
- `registry.representation-bindings`
- `registry.semantic-overlays`
- `registry.styles`
- `registry.style-bindings`
- `registry.language-definitions`
- `registry.specification-source-adapters`
- `matrix.format-capabilities`
- `graph.conversions`

## Legacy profile migration

Earlier repository versions stored the 44 abstract model types under `profile.domain.*` and separately seeded `profile.mermaid.class.*`. That mixed two different concepts.

New code should use:

```text
OLD
profile.domain.interface-driven-model
profile.mermaid.class.interface-driven-model

NEW
model.interface-driven-class
binding.interface-driven-class.mermaid-class
```

`abstract-models/registry.yaml` retains legacy aliases for discovery/backward compatibility. New functionality must not create additional domain model types under format-specific profile namespaces.

The term **representation profile** may still be used for complex mapping policies, but a reusable model type belongs in `abstract-models/` and a model-to-format mapping belongs in `representation-bindings/`.

## Extension workflow for a new abstract model

1. add the model to `abstract-models/registry.yaml`;
2. create a detailed `abstract-representation-model` manifest when semantics are known;
3. validate against `schemas/abstract-model.schema.json`;
4. add bindings only for formats intentionally supported;
5. declare binding fidelity and losses;
6. add fixtures for each binding;
7. add semantic round-trip/equivalence tests where import exists;
8. document non-obvious conventions.

## Extension workflow for a new format

1. ingest/pin its specification evidence into a Normalized Language Definition;
2. register capabilities;
3. implement syntax/runtime validation with explicit authority;
4. add representation bindings for selected abstract models;
5. add a format-specific style binding;
6. add transforms/import adapters;
7. add fixtures and conformance tests;
8. add conversion-graph edges;
9. declare fidelity and degradation behaviour.

## Extension workflow for a style

1. add a format-neutral style profile under `styles/`;
2. use semantic names/intent rather than raw target syntax where possible;
3. reuse an existing style binding for each chosen format;
4. add a new style binding only when the format needs a different translation mechanism;
5. test accessibility and semantic-channel collisions;
6. record unsupported style features as presentation loss, not semantic loss.

## Development rules

Future implementations should preserve these boundaries:

- models do not choose formats;
- formats do not own model semantics;
- bindings map models to chosen formats;
- overlays add semantic dimensions;
- styles modify presentation only;
- style bindings translate style intent only;
- language definitions describe representation systems, not domain models;
- transforms report loss;
- validators declare authority;
- provenance records source/version evidence;
- round-trip claims are tested, never inferred from syntax validity.
