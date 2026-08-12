# Validation Model

Validation is a first-class artifact type and now covers both representation artifacts and the definitions used to understand representation languages.

## Validation layers

1. **Artifact/schema** - required fields, data types, enums and structural constraints.
2. **Language-definition** - normalized syntax/metamodel/semantics/capability records conform to the NLD schema.
3. **Source-adapter** - specification-source adapter manifests conform to their schema and status rules.
4. **Source provenance** - pinned Git commits and evidence blob hashes still match the source checkout.
5. **Semantic** - unique IDs, valid references, relationship endpoints and container membership.
6. **Syntax/serialization** - target parser or structural checks.
7. **Format constraints** - target-specific restrictions.
8. **Compatibility** - feature/version/renderer support.
9. **Lint** - valid but undesirable patterns.
10. **Runtime/render** - parser or renderer behaviour.
11. **Fixture/regression** - known-valid and known-invalid cases.

## Authority model

Validator authority comes from the source evidence recorded in a normalized language definition. Different sources may carry different authority:

```text
normative specification / schema
native authoritative runtime
formal grammar
semantic/metamodel implementation
conformance tests
supporting documentation
repository-derived preflight rules
```

The exact order is language-specific and should be declared rather than assumed globally.

## Implemented validation

The Python engine implements canonical JSON Schema Draft 2020-12 validation, canonical semantic-reference validation, NLD schema validation, specification-source adapter validation, generic Git-backed source provenance verification, JSON Schema meta-schema validation, XML well-formedness validation, Mermaid runtime/source-derived validation, PlantUML structural validation, UML repository-interchange validation and Markdown structural validation.

## Mermaid

Mermaid's own runtime parser is syntax authority when installed. The class validator also uses conservative source-derived preflight rules. The source evidence is pinned in `validators/mermaid/source-provenance.yaml`, and `language-definitions/mermaid/class-diagram.yaml` records the normalized language definition consumed by the validator architecture.

If Mermaid runtime support is unavailable, default validation degrades with a warning. `--require-runtime` converts that condition to an error.

## UML

Current UML validation checks the repository's UML class-interchange representation, not the normative UML metamodel. `language-definitions/uml/manifest.yaml` is deliberately unpinned; normative UML claims remain blocked until an explicit specification version and evidence set are ingested.

## Generic source checking

```bash
blueprint-engine --repo . source-check <provenance.yaml> <source-root>
```

The command checks both the pinned source commit and every evidence file's Git blob ID. This mechanism is format-independent; `mermaid-source-check` is retained as a compatibility alias.
