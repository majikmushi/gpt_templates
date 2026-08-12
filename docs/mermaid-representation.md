# Mermaid as an Abstract Representation Target

Mermaid diagram families are treated as collections of representational primitives,
not as fixed semantic meanings.

## Source authority

The Mermaid integration is pinned to `majikmushi/mermaid` `develop` commit
`446f6a7701065eb12e024475243434eb727dc172` (Mermaid package `11.4.1`).

`validators/mermaid/source-provenance.yaml` records the exact source-file SHAs used
to derive the class-diagram rules. `validators/mermaid/registry.yaml` records the
diagram families registered by Mermaid's diagram orchestration source.

## Native parser and AST bridge

The engine delegates authoritative syntax acceptance to Mermaid itself:

```text
source text
 -> mermaid.parse()
 -> mermaidAPI.getDiagramFromText()
 -> diagram-specific DB
 -> normalized repository AST
 -> representation profile
 -> canonical semantic model
```

For `classDiagram`, the adapter reads Mermaid's `ClassDB`: classes, members,
methods, annotations, namespaces, relations, notes, direction, links, styles and
accessibility metadata.

This is deliberately different from maintaining a second Mermaid grammar in Python.

## Semantic repurposing

The native class primitives can represent software classes, components, electronics,
resources, roles, capabilities, schemas, taxonomies, physical assemblies and other
typed relational structures. Representation profiles make those meanings explicit.

Visual channels such as styling, annotations, namespaces and relation labels can carry
additional semantic dimensions. Overlay collision/accessibility policies remain
separate from Mermaid syntax validity.

## Class source-derived constraints

The reference validator currently records:

- two accepted class-diagram headers (`classDiagram`, `classDiagram-v2`);
- four direction values (`TB`, `BT`, `RL`, `LR`);
- relation endpoint markers and solid/dotted line types;
- cardinality/end labels;
- namespace membership;
- quoted notes;
- link targets;
- generic syntax;
- visibility/static/abstract member semantics;
- annotation/stereotype syntax;
- lollipop interface normalization.

See `validators/mermaid/class/rules.yaml`.

## Expansion

The same native runtime validation path works for all Mermaid diagram families.
Source-level semantic profiles are currently deepest for class diagrams; other families
are registered as `runtime-validation-available / source-profile-pending` until their
grammar/DB/test sources are analysed.
