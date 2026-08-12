# Specification Ingestion and Normalized Language Definitions

The framework does not assume every representation language is defined by a text grammar. Instead, external language/specification evidence is ingested through **specification source adapters** into a **Normalized Language Definition (NLD)**.

```text
Specification / implementation evidence
        |
        +-- grammar source
        +-- metamodel source
        +-- schema source
        +-- runtime source
        +-- conformance tests
        +-- documentation
        +-- serialization source
        +-- constraint source
        |
        v
Normalized Language Definition
        |
        +-- syntax
        +-- metamodel
        +-- semantics
        +-- constraints
        +-- capabilities
        +-- serializations
        +-- runtime behavior
        +-- conformance evidence
        +-- provenance
        |
        v
Generated / hand-written validators, parsers, adapters and representation bindings
```

## Why this layer exists

Mermaid and UML are structurally different sources of truth. Mermaid class diagrams are primarily implemented through lexer/grammar, runtime parser, semantic DB and regression tests. UML is a modeling language whose future normative integration should be metamodel/constraint-first, with concrete serializations handled separately.

The NLD lets both feed the same downstream machinery without forcing UML into a parser-shaped abstraction or reducing Mermaid to documentation prose.

## Authority is per source

A language definition may combine sources with different authority. Examples:

- `authoritative-runtime` for an implementation's parser;
- `normative-specification` for a formal standard;
- `normative-schema` for a machine-readable schema;
- `conformance-evidence` for official/upstream tests;
- `supporting` for documentation;
- `derived` for repository-normalized semantic structures.

No aggregate language definition becomes more authoritative than its pinned evidence.

## Source kinds

The initial adapter taxonomy is:

- `grammar-source`
- `metamodel-source`
- `schema-source`
- `runtime-source`
- `test-source`
- `documentation-source`
- `serialization-source`
- `constraint-source`

Additional kinds can be introduced through schema versioning instead of embedding format-specific assumptions into the engine.

## Mermaid

`language-definitions/mermaid/class-diagram.yaml` is populated from the pinned Mermaid repository evidence. Runtime syntax validation remains authoritative; the NLD records the grammar-derived and ClassDB-derived structure used by preflight checks, semantic import and future generated validators.

## UML

`language-definitions/uml/manifest.yaml` is intentionally a scaffold. It establishes the target shape for metamodel, semantic constraints, views and serializations, but it does not claim normative UML conformance until a specific specification version and evidence set are selected and pinned.

A future UML ingestion can therefore look like:

```text
UML metamodel ---------+
UML constraints -------+--> language.uml
UML serialization -----+       |
UML conformance tests -+       +--> UML validator
                                +--> XMI adapter
                                +--> UML view definitions
                                +--> Mermaid / PlantUML bindings
```

## Versioning and staleness

Source adapters record versions, commits or evidence hashes where available. When a source changes, only dependent NLD sections and generated artifacts need to be invalidated and regenerated. This is preferable to treating the entire language integration as one opaque validator.
