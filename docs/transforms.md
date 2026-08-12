# Transformation Model

Transforms are the repository equivalent of an XSLT-like mapping layer: they convert one structured representation into another while keeping the semantic mapping explicit.

## Transform categories

- source -> canonical
- canonical -> target
- target -> canonical
- target -> target
- normalization
- enrichment
- projection/simplification

## Manifest requirements

Each transform should state:

- source model/schema
- destination model/schema
- required profile
- parameters
- preconditions
- output guarantees
- fidelity/lossiness
- reversibility
- deterministic behaviour
- dependency/runtime requirements

## Transform graph

Transforms form a graph rather than a single pipeline. Tooling can calculate a path such as:

```text
JSON Schema
  -> canonical.data-model
  -> profile.mermaid.class.logical-data
  -> Mermaid classDiagram
```

Round-trip claims should only be made when tested with fixtures.
