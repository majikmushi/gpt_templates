# Visual Encoding and Semantic Overlays

A diagram can carry information through multiple independent visual channels.

## Typical channels

- shape
- fill colour
- stroke colour
- border pattern
- line/edge style
- arrow type
- icon
- label
- annotation/stereotype
- spatial grouping
- subgraph/namespace/container
- ordering/direction

## Example dimensions

The same format may encode:

- shape -> component type
- colour -> trust zone
- subgraph -> deployment zone
- border -> lifecycle state
- edge style -> communication/dependency type
- arrow direction -> data flow
- edge label -> protocol
- icon -> implementation/vendor

## Overlay composition

Overlays add semantic dimensions without redefining the base profile.

Example:

```text
Electronics System Profile
  + Voltage Domain Overlay
  + Safety Criticality Overlay
  + Ownership Overlay
  + Lifecycle Overlay
```

## Collision handling

Two overlays that request the same single-use channel may conflict. A transformer should:

1. re-map one semantic dimension to another compatible channel;
2. combine channels only where unambiguous;
3. fall back to labels/annotations;
4. fail validation if semantics would become ambiguous.

## Accessibility

Critical meaning must not rely on colour alone. Profiles should provide textual or structural fallbacks and require a legend when the encoding is not self-evident.
