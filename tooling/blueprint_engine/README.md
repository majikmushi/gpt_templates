# Blueprint Representation Engine

Executable core for the `gpt_templates` representation framework.

## Implemented

- artifact catalog scanning
- capability matching
- conversion-route selection
- canonical semantic model validation
- canonical -> Mermaid classDiagram
- canonical -> PlantUML
- canonical -> UML class interchange JSON
- canonical -> JSON Schema projection
- canonical -> XML profile
- canonical -> Markdown
- XML -> canonical import
- UML class interchange -> canonical import
- declarative XSLT-like mapping rules
- output validation
- deterministic provenance hashes
- semantic comparison
- XML and UML-class round-trip testing

## Install

```bash
python -m pip install -e tooling/blueprint_engine
```

## CLI

```bash
blueprint-engine --repo . catalog
blueprint-engine --repo . match typed_entities cardinality
blueprint-engine --repo . route canonical.core format.json-schema
blueprint-engine --repo . transform examples/cross-format/embedded-controller/model.yaml format.mermaid.class
blueprint-engine --repo . validate canonical.core examples/cross-format/embedded-controller/model.yaml
blueprint-engine --repo . roundtrip examples/cross-format/embedded-controller/model.yaml format.xml
```

Validation for Mermaid and UML is deliberately scoped. The current implementation validates the repository's generated/interchange subset. It is not a replacement for a source/spec-derived normative validator.
