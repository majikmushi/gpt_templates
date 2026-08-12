# Representation Profiles

A representation profile defines **what target primitives mean in a specific modelling context**.

A Mermaid `classDiagram`, for example, has a native UML interpretation, but its classes, members, namespaces, relations, cardinalities, styles, and annotations can represent many other systems abstractly.

## Profile responsibilities

A profile should declare:

- native/parent profile
- concepts represented
- structural mappings
- relationship mappings
- visual encodings
- required target capabilities
- fidelity
- suitability
- limitations
- fallback representations
- compatible overlays

## Example

```yaml
id: profile.mermaid.class.electronics-system
kind: representation-profile
extends:
  - profile.mermaid.class.physical-system

concept_mapping:
  board:
    maps_to: class
  component:
    maps_to: class
  parameter:
    maps_to: attribute
  function:
    maps_to: operation
  subsystem:
    maps_to: namespace

relationship_mapping:
  contains:
    maps_to: composition
  connects_to:
    maps_to: association
  depends_on:
    maps_to: dependency
  implements_interface:
    maps_to: realization
```

## Semantic overloading

A primitive's conventional meaning is a default, not a hard semantic boundary.

Profiles make overloading explicit so the diagram remains interpretable and transformable rather than relying on undocumented visual convention.
