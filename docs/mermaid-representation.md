# Mermaid as an Abstract Representation Target

Mermaid diagram families should be treated as collections of representational primitives and constraints, not only as their conventional diagram names.

## Class diagram

Useful primitives include:

- class/entity nodes
- attributes
- operations
- namespaces
- inheritance
- composition
- aggregation
- association
- dependency
- realization
- interface/lollipop notation
- multiplicity
- annotations
- notes
- style classes

These can model software classes, but also system components, electronics, resources, ownership, roles, capabilities, schemas, taxonomies, physical assemblies, and other typed relational structures.

## Flowchart

Flowcharts provide a broad primitive set including many shapes, subgraphs, edge styles, direction, classes/styles, icons, and labels. They are particularly useful as a generic visual encoding substrate.

## Representation profiles

The repository stores explicit profiles describing how a target diagram is repurposed. This avoids hidden conventions and supports validation and transformation.

## Initial class-diagram profile registry

The seeded registry contains 44 profiles spanning:

- software and interface models
- data and schema models
- architecture models
- hardware and physical systems
- security and ownership models
- organisational models
- taxonomy/ontology models
- product and feature models
- metamodel and blueprint models

See `profiles/mermaid/class/registry.yaml`.
