# Repository Architecture

The authoritative architectural overview is [`framework-architecture.md`](framework-architecture.md).

## Core pipeline

```text
Canonical / source semantics
        -> Abstract representation model
        -> Chosen representation format
        -> Representation binding
        -> Semantic overlays
        -> Style profile
        -> Format-specific style binding
        -> Transform / adapter
        -> Concrete artifact
        -> Validation / provenance / semantic comparison
```

The word **chosen** is intentional. Normal generation does not auto-select a format. `binding: auto` only resolves a mapping for a format already selected by the caller.

## Architectural boundaries

- **Canonical semantics** define meaning and source facts.
- **Abstract models** define reusable model types independently of syntax.
- **Formats/language definitions** define what representation systems can express.
- **Representation bindings** map one abstract model into one chosen format.
- **Semantic overlays** add additional meaning.
- **Style profiles** control presentation without changing meaning.
- **Style bindings** translate abstract style intent into target-specific styling mechanisms.
- **Transforms/adapters** execute mappings.
- **Validators/provenance/equivalence** determine validity, authority, loss and semantic preservation.

## Stable artifact namespaces

```text
model.interface-driven-class
format.mermaid.class
binding.interface-driven-class.mermaid-class
overlay.security.trust-zone
style.technical-dark
style-binding.mermaid.class
language.mermaid.class-diagram
transform.canonical-to-mermaid-class
validator.mermaid.class
```

Stable IDs are independent of repository paths.
