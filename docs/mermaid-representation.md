# Mermaid as a Representation System

Mermaid diagram families are collections of syntax, structural primitives, visual channels and runtime behaviour. They are not abstract model types.

## Source authority and current version

The current classDiagram reference is pinned to `majikmushi/mermaid` commit `446f6a7701065eb12e024475243434eb727dc172`, package version `11.4.1`.

This source evidence contributes to:

- `language.mermaid.class-diagram`;
- `format-version.mermaid.class.11.4.1`;
- `validator.mermaid.class`;
- `renderer.mermaid-js` release `11.4.1`;
- `compatibility.renderer.mermaid-js.mermaid-class.11.4.1`.

The format release and renderer release remain separate framework concepts even though this reference implementation obtains both from the same Mermaid package.

## Native parser and AST path

```text
Mermaid source text
 -> mermaid.parse()
 -> mermaidAPI.getDiagramFromText()
 -> diagram-specific DB
 -> normalized repository AST
 -> representation binding
 -> canonical semantic model
```

For classDiagram, the adapter reads classes, members, methods, annotations, namespaces, relations, notes, direction, links, styles and accessibility metadata from Mermaid's parsed DB.

## Abstract-model bindings

A Mermaid class primitive can represent many abstract concepts, but that semantic reuse must be explicit in a `binding.*` artifact.

For example:

```text
model.interface-driven-class
  + format.mermaid.class
  -> binding.interface-driven-class.mermaid-class
```

The binding, not Mermaid itself, defines that a class plus `<<interface>>` realizes the abstract `interface` concept for that model.

## Version compatibility

Bindings and style bindings declare the format-release ranges they support and the capabilities they require. Current source-backed class bindings target exact Mermaid `11.4.1`; no forward/backward compatibility is inferred.

When a renderer is chosen, generation planning separately resolves renderer compatibility. Syntax acceptance by Mermaid does not automatically prove another renderer/integration will display the artifact equivalently.

## Expansion to other Mermaid diagram families

For each family:

1. pin grammar/runtime/DB/test evidence;
2. create a versioned format release with evidence-backed capabilities;
3. add representation bindings for selected abstract models;
4. add style bindings where presentation can be realized;
5. add validators and semantic AST adapters;
6. register renderer compatibility only after testing exact release combinations;
7. establish round-trip claims through semantic comparison.
