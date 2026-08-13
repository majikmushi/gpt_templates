# Mermaid as a Representation Target

Mermaid is a representation system whose diagram families expose reusable primitives. Mermaid is not an abstract model type.

An abstract model such as `model.interface-driven-class`, `model.electronics-system` or `model.security` may be represented through Mermaid only when an explicit representation binding exists for the chosen Mermaid format.

## Source authority

The Mermaid integration is pinned to `majikmushi/mermaid` `develop` commit `446f6a7701065eb12e024475243434eb727dc172` (Mermaid package `11.4.1`).

`validators/mermaid/source-provenance.yaml` records source-file SHAs used to derive class-diagram rules. `validators/mermaid/registry.yaml` records diagram families registered by Mermaid's orchestration source.

## Native parser and AST bridge

```text
Mermaid source
 -> mermaid.parse()
 -> mermaidAPI.getDiagramFromText()
 -> diagram-specific DB
 -> normalized repository AST
 -> representation binding / profile context
 -> canonical semantic model
```

For `classDiagram`, the adapter reads Mermaid `ClassDB` information including classes, members, methods, annotations, namespaces, relations, notes, direction, links, styles and accessibility metadata.

Native runtime acceptance remains syntax authority when available.

## Model-to-Mermaid bindings

The preferred architecture is:

```text
abstract model
   +
chosen Mermaid diagram format
   -> representation binding
   -> Mermaid artifact
```

For example:

```text
model.interface-driven-class
   + format.mermaid.class
   -> binding.interface-driven-class.mermaid-class
```

A Mermaid primitive's conventional meaning is not an absolute semantic boundary. A binding may deliberately repurpose classes, relations, namespaces, annotations or labels, but that semantic overloading must be explicit and fidelity/loss must be declared.

## Semantic overlays versus styling

Semantic overlays can use Mermaid visual channels to encode additional meaning. Style profiles independently control presentation such as palette, typography, connector appearance and density.

`style-binding.mermaid.class` translates abstract style intent into Mermaid-supported mechanisms. Style must not override the semantic meaning assigned by the representation binding or overlays.

## Class source-derived constraints

The current source-derived validator records accepted class headers, direction values, relation endpoint markers, line types, cardinality labels, namespaces, quoted notes, link targets, generic syntax, member visibility/static/abstract semantics, annotations/stereotypes and lollipop normalization.

See `validators/mermaid/class/rules.yaml`.

## Expansion

The native runtime validation path works across Mermaid diagram families. Future deep support should add source-derived language-definition evidence, model-specific representation bindings, style-channel capabilities, fixtures and semantic import/round-trip tests for each selected family.
