# Semantic Overlays, Visual Encoding and Style

The framework separates **semantic visual encoding** from **presentation style**.

## Semantic overlays

Overlays add meaning to the underlying model. Typical dimensions include:

- security/trust zone;
- lifecycle state;
- ownership;
- voltage domain;
- safety criticality;
- deployment zone;
- protocol or communication class.

They may request visual channels such as shape, fill colour, stroke colour, border pattern, edge style, arrow type, icon, label, annotation or grouping.

If an overlay encodes critical meaning with colour, it must also provide a textual, structural or other non-colour fallback.

## Style profiles

Styles alter presentation without altering the semantic model. Typical style intent includes:

- theme and palette;
- typography;
- node borders/corners;
- connector weight/pattern preferences;
- grouping presentation;
- spacing/density;
- layout intent.

Abstract style profiles live under `styles/`. Format-specific translations live under `style-bindings/`.

## Why the separation matters

The same abstract model and representation binding can be rendered with different styles without becoming a different model:

```text
model.interface-driven-class
+ binding.interface-driven-class.mermaid-class
+ style.neutral-technical
```

or:

```text
model.interface-driven-class
+ binding.interface-driven-class.mermaid-class
+ style.technical-dark
```

The semantics stay the same.

## Collision priority

When style intent and semantic encoding compete for the same target feature, preserve information in this order:

1. abstract-model semantics;
2. semantic-overlay semantics;
3. target-format validity;
4. style intent.

A renderer may remap a style feature or report presentation loss, but must not silently change semantic meaning to satisfy styling.

## Existing channel policy

`overlays/visual-channels/base.yaml` defines reusable channel allocation and fallback rules. `overlays/registry.yaml` marks it as semantic/channel policy rather than a presentation theme.
