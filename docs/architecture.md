# Repository Architecture

## Purpose

This repository is a registry and execution substrate for reusable representational knowledge: blueprints, templates, schemas, language definitions, transforms, validators and the metadata needed to combine them safely.

## Two input planes

The framework separates **definition evidence** from **domain/model data**.

```text
LANGUAGE / SPECIFICATION PLANE

Grammar   Metamodel   Schema   Runtime   Tests   Docs   Serialization   Constraints
   \         |          |         |        |      |          |              /
    +--------+----------+---------+--------+------+----------+-------------+
                                      |
                                      v
                         Specification Source Adapters
                                      |
                                      v
                         Normalized Language Definition
                                      |
                         +------------+------------+
                         |                         |
                         v                         v
                    Validators               Format capabilities

DOMAIN / MODEL PLANE

Source / Domain Data
        |
        v
Canonical Model
        |
        v
Blueprint Requirements
        |
        v
Capability Matching <---------------- Format capabilities
        |
        v
Representation Profile
        |
        v
Transformer / Adapter
        |
        v
Target Artifact
        |
        v
Validator Stack
```

The planes converge at capability selection, adapters and validators. A language definition describes what a representation language means and how its evidence is justified; a canonical model describes the user's subject matter.

## Separation of concerns

### Normalized language definition
Stores syntax, metamodel, semantics, constraints, capabilities, serializations, runtime behavior, conformance evidence and provenance without assuming every language is grammar-driven.

### Specification source adapter
Maps an external source of authority or evidence into one or more normalized language-definition sections. Supported source kinds include grammar, metamodel, schema, runtime, tests, documentation, serialization and constraints.

### Format
Defines a target representation family and its available primitives/capabilities. It may reference a normalized language definition but is not the same artifact.

### Blueprint
Defines the abstract thing to represent, independent of output language.

### Representation profile
Maps domain concepts to format primitives and visual channels.

### Overlay
Adds a semantic dimension to an existing representation profile without redefining the base mapping.

### Transform
Converts source/canonical data into another representation and declares fidelity/loss characteristics.

### Validator
Checks schema, syntax, semantics, format restrictions, compatibility, lint and optional runtime/render behaviour. Validator authority is tied back to language-definition evidence.

## Mermaid and UML

Mermaid demonstrates a grammar/runtime-first integration: Jison grammar, runtime parser, ClassDB and upstream tests feed `language.mermaid.class-diagram`.

UML demonstrates a metamodel-first future integration: metamodel, constraints and serialization sources will feed `language.uml`. This avoids treating UML as if it were one textual parser syntax.

## Artifact identity

Artifact IDs are stable and independent of file paths. Example namespaces:

```text
language.mermaid.class-diagram
language.uml
specification.mermaid.class
format.mermaid.class
profile.mermaid.class.electronics-system
overlay.security.trust-zone
transform.canonical-to-mermaid-class
validator.mermaid.class
blueprint.system.embedded-controller
```

## Provenance

Generated or derived artifacts should record source artifact/version, source evidence/version or commit, blueprint/profile/transform/validator IDs, source hashes and generation metadata. Source-derived language definitions additionally record evidence-file hashes so staleness can be detected selectively.
