# Blueprint Representation Engine

Executable core for the `gpt_templates` representation framework.

## Implemented

- artifact catalog scanning
- capability matching and conversion routing
- canonical semantic model validation
- canonical exports to Mermaid, PlantUML, UML class interchange, JSON Schema, XML and Markdown
- XML and UML class imports
- declarative XSLT-like mapping rules
- deterministic provenance hashes
- semantic comparison and round-trip checks
- Mermaid native runtime syntax validation
- Mermaid classDiagram AST extraction and canonical import
- Mermaid source-provenance verification

## Install

```bash
python -m pip install -e tooling/blueprint_engine
```

For authoritative Mermaid validation/AST extraction:

```bash
cd tooling/blueprint_engine/node
npm install
```

## CLI

```bash
blueprint-engine --repo . catalog
blueprint-engine --repo . match typed_entities cardinality
blueprint-engine --repo . route canonical.core format.mermaid.class
blueprint-engine --repo . transform examples/cross-format/embedded-controller/model.yaml format.mermaid.class
blueprint-engine --repo . validate format.mermaid.class examples/cross-format/embedded-controller/model.mmd --require-runtime
blueprint-engine --repo . mermaid-ast examples/cross-format/embedded-controller/model.mmd
blueprint-engine --repo . mermaid-import examples/cross-format/embedded-controller/model.mmd -o /tmp/model.yaml
```

Mermaid static checks are source-derived preflight only. `--require-runtime` requires the
native Mermaid parser and fails if it is unavailable.
