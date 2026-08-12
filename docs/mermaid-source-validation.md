# Mermaid Source-Derived Validation and AST Integration

## Reference source

This integration was derived from `majikmushi/mermaid` branch `develop`, commit `446f6a7701065eb12e024475243434eb727dc172`, Mermaid package version `11.4.1`.

The exact evidence files and Git blob SHAs are recorded in `validators/mermaid/source-provenance.yaml`.

## Generic specification-ingestion layer

Mermaid now participates in the same source-ingestion architecture intended for UML and other languages:

```text
Mermaid grammar/runtime/DB/tests
    |
    v
Specification Source Adapters
    |
    v
language.mermaid.class-diagram
    |
    +--> static source-derived rules
    +--> native runtime validator
    +--> ClassDB AST adapter
    +--> canonical semantic model
```

`language-definitions/mermaid/class-diagram.yaml` is the normalized language definition. `adapters/specification/mermaid.yaml` describes how pinned Mermaid evidence contributes to it.

## Why the runtime is authoritative

Mermaid's `mermaidAPI.parse()` parses diagram text and validates syntax. `Diagram.fromText()` performs type detection, lazy-loads the selected diagram implementation, attaches a diagram-specific DB to Jison parsers, clears the DB and executes the parser.

The framework therefore does not maintain a second complete Mermaid grammar.

## Validation modes

`validator.mermaid.runtime` invokes Mermaid through `tooling/blueprint_engine/node/mermaid_bridge.mjs`. This path supports every diagram family registered by Mermaid's diagram orchestration.

`format.mermaid.class` also runs conservative static checks taken from the class Jison grammar, ClassDB, ClassMember types and source tests. They are preflight checks, not grammar-complete replacements.

If Node/Mermaid is unavailable, normal validation returns a warning. With `--require-runtime`, it returns an error.

## Class diagram semantic adapter

The class reference adapter obtains Mermaid's parsed ClassDB and normalizes classes and labels, attributes and methods, visibility, generic type, static/abstract classifiers, annotations, CSS classes and styles, namespaces, relationships, cardinalities, notes, direction, links and accessibility metadata.

Lollipop relations are represented using the synthetic interface nodes exposed by ClassDB's normalized render data.

## Source checkout verification

Generic command:

```bash
blueprint-engine --repo . source-check validators/mermaid/source-provenance.yaml /path/to/mermaid
```

Compatibility alias:

```bash
blueprint-engine --repo . mermaid-source-check /path/to/mermaid
```

Both compare the checkout HEAD and each evidence file's Git blob hash with the pinned provenance manifest.

## Extending to another Mermaid diagram family

For each family, pin grammar/parser/DB/detector/test evidence, add or generate an NLD, use the shared native runtime parser for syntax, add a diagram-specific DB/AST adapter where semantic round trips matter, add conformance fixtures, and only establish round-trip claims after semantic comparison passes.

The generic specification-ingestion architecture is described in `docs/specification-ingestion.md`.
