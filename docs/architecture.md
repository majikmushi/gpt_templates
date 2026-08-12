# Repository Architecture

## Purpose

This repository is a registry and execution substrate for reusable representational knowledge: blueprints, templates, schemas, transforms, validators, and the metadata needed to combine them safely.

## Pipeline

```text
Source / Domain Data
        |
        v
Canonical Model
        |
        v
Blueprint Requirements
        |
        v
Capability Matching
        |
        v
Representation Profile
        |
        v
Transformer
        |
        v
Target Artifact
        |
        v
Validator Stack
```

## Separation of concerns

### Format
Defines what a target language can express: primitives, syntax features, styling channels, constraints, and version compatibility.

### Blueprint
Defines the abstract thing to represent, independent of output language.

### Representation profile
Maps domain concepts to format primitives and visual channels.

### Overlay
Adds a semantic dimension to an existing representation profile without redefining the base mapping.

### Transform
Converts source/canonical data into another representation and declares fidelity/loss characteristics.

### Validator
Checks schema, syntax, semantics, format restrictions, compatibility, lint, and optional runtime/render behaviour.

## Artifact identity

Artifact IDs are stable and independent of file paths. A path may change; an artifact ID should not.

Suggested ID namespaces:

```text
format.mermaid.class
profile.mermaid.class.electronics-system
overlay.security.trust-zone
transform.canonical-to-mermaid-class
validator.mermaid.class.syntax
blueprint.system.embedded-controller
```

## Provenance

Generated files should be able to record:

- source artifact ID/version
- blueprint ID/version
- profile ID/version
- transform ID/version
- validator set/version
- source hash
- generation timestamp
