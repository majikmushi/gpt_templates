# Mermaid Source-Derived Validation and AST Integration

## Reference source

This integration was derived from `majikmushi/mermaid`:

- branch: `develop`
- commit: `446f6a7701065eb12e024475243434eb727dc172`
- Mermaid package version: `11.4.1`

The exact evidence files and Git blob SHAs are recorded in
`validators/mermaid/source-provenance.yaml`. This lets the framework detect when a
later Mermaid revision invalidates assumptions used by a validator or adapter.

## Why the runtime is authoritative

Mermaid's `mermaidAPI.parse()` is implemented specifically to parse diagram text and
validate syntax. `Diagram.fromText()` performs type detection, lazy-loads the selected
diagram implementation, attaches a diagram-specific DB to Jison parsers, clears the DB
and executes the parser.

The framework therefore does not maintain a second complete Mermaid grammar.

```text
Mermaid source
    |
    v
native mermaid.parse()
    |
    +--> parser rejection -> validation error
    |
    v
mermaidAPI.getDiagramFromText()
    |
    v
Diagram { type, db, parser, renderer }
    |
    v
diagram-specific AST/DB adapter
```

## Validation modes

### Native runtime

`validator.mermaid.runtime` invokes Mermaid through
`tooling/blueprint_engine/node/mermaid_bridge.mjs`.

This path supports every diagram family registered by Mermaid's diagram orchestration.

### Source-derived preflight

`format.mermaid.class` also runs conservative static checks taken directly from the
class Jison grammar, ClassDB, ClassMember types and source tests. They catch a useful
subset of errors before invoking Node but are not advertised as grammar-complete.

### Explicit degradation

If Node/Mermaid is unavailable, normal validation returns a warning. With
`--require-runtime`, it returns an error.

## Class diagram semantic adapter

The class reference adapter obtains Mermaid's parsed ClassDB and normalizes:

- classes and labels;
- attributes and methods;
- visibility, generic type, static/abstract classifier;
- annotations/stereotypes;
- CSS classes and inline styles;
- namespaces;
- relation endpoint markers, line type, labels and cardinalities;
- notes;
- direction;
- links, link targets and tooltips;
- accessibility title/description.

Lollipop relations are represented using the synthetic interface nodes exposed by
ClassDB's normalized render data. If a future Mermaid runtime yields an unresolved
relation endpoint, the adapter preserves it as an explicit implicit-reference element
rather than emitting an invalid canonical model.

## Class source rules

The pinned class grammar accepts both `classDiagram` and `classDiagram-v2`. Direction
values are `TB`, `BT`, `RL`, and `LR`. Relation endpoint marker semantics are encoded by
ClassDB as aggregation, extension, composition, dependency and lollipop; relation
lines are solid or dotted.

The source also establishes quoted note text, supported link targets, member visibility
symbols, static/abstract classifiers, generic `~...~` syntax, annotations and namespace
membership rules.

Machine-readable evidence for each rule is in
`validators/mermaid/class/rules.yaml`.

## Source checkout verification

Given a local checkout of `majikmushi/mermaid`:

```bash
blueprint-engine --repo . mermaid-source-check /path/to/mermaid
```

The command compares the checkout HEAD and each evidence file's Git blob hash with the
pinned provenance manifest.

## Extending to another Mermaid diagram family

For each family:

1. pin grammar/parser/DB/detector/test evidence;
2. add source-derived rule metadata;
3. use the generic native runtime parser for syntax;
4. add a diagram-specific DB/AST adapter when semantic round trips matter;
5. add valid/invalid fixtures sourced from or aligned with Mermaid's own tests;
6. update capability and conversion metadata;
7. establish round-trip claims only after semantic comparison passes.

The parser/runtime layer is shared; only the deep semantic adapter varies by diagram
family.
