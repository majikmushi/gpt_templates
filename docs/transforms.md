# Transformation Model

Transforms are the repository equivalent of an XSLT-like mapping layer: they convert one structured representation into another while keeping semantic mapping explicit.

## Implemented engine

The executable implementation is `tooling/blueprint_engine/src/blueprint_engine/`.

Two transformation mechanisms are available:

1. **Built-in format encoders** for targets with syntax or serialization rules.
2. **Declarative mapping rules** for XSLT-like object-to-object projection.

The declarative engine uses:

```text
select -> match -> emit
```

and can map canonical `elements` and `relationships` into arbitrary target collections.

## Transform categories

- source -> canonical
- canonical -> target
- target -> canonical
- target -> target
- normalization
- enrichment
- projection/simplification

## Runtime guarantees

Every built-in transform returns:

- transform ID
- target format
- media type
- fidelity declaration
- explicit semantic losses
- deterministic source hash
- profile/overlay provenance when supplied

Transforms must not silently discard semantics. JSON Schema export, for example, declares relationship loss and lists dropped relationship IDs in the generated schema.

## Routing

The conversion graph is executable through the engine. Route selection prefers lower-loss paths and adds cost for non-reversible edges.

## Round trips

XML and the repository UML-class interchange model currently support tested canonical round trips. Mermaid and PlantUML imports are intentionally deferred until their parser/grammar boundaries are defined.
