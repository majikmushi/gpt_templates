# Validation Model

Validation is first-class and applies both to generated representations and to the framework contracts used to understand representation systems.

## Validation layers

1. **Artifact/schema** - required fields, data types and structural constraints.
2. **Language definition** - normalized syntax/metamodel/semantics/capability records.
3. **Source adapter** - specification-source adapter status and schema.
4. **Source provenance** - pinned source commits and evidence blob hashes.
5. **Semantic** - IDs, references, relationship endpoints and containment.
6. **Format release** - requested release exists and required capabilities are present.
7. **Syntax/serialization** - target parser or structural validation.
8. **Representation/style binding compatibility** - binding version ranges and capabilities.
9. **Renderer compatibility** - explicit renderer-release <-> format-release contract plus effective capabilities.
10. **Runtime/render** - parser or renderer behaviour.
11. **Fixture/regression** - known-valid, known-invalid and semantic round-trip cases.

## Authority model

Authority is declared per evidence source, for example:

```text
normative specification / schema
native authoritative runtime
formal grammar
semantic/metamodel implementation
conformance tests
supporting documentation
repository-derived checks
```

No universal ordering is assumed across all languages.

## Mermaid

The currently pinned classDiagram reference is Mermaid `11.4.1` from `majikmushi/mermaid` commit `446f6a7701065eb12e024475243434eb727dc172`.

Mermaid's runtime parser is syntax authority when installed. Static class checks are conservative source-derived preflight checks. Renderer compatibility is a separate claim governed by `renderer-compatibility/`.

## UML

Current UML validation covers the repository interchange representation, not normative UML conformance. Until a UML specification release is explicitly ingested and registered, UML format-version support remains `unpinned`.

## Generic source checking

```bash
blueprint-engine --repo . source-check <provenance.yaml> <source-root>
```

This is the sole source-provenance command. Format-specific compatibility aliases are intentionally not maintained.
