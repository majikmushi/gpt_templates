# Blueprint Representation Engine

Executable core for the `gpt_templates` representation framework.

## Version 0.3 framework layers

The engine now resolves abstract representation models, user-chosen formats, model-to-format representation bindings, semantic overlays, abstract style profiles, format-specific style bindings and machine-validated generation requests.

It deliberately does not auto-select a format during normal planning.

## Install

```bash
python -m pip install -e tooling/blueprint_engine
```

For authoritative Mermaid runtime validation/AST extraction:

```bash
cd tooling/blueprint_engine/node
npm install
```

## Framework CLI

```bash
blueprint-engine --repo . abstract-model model.interface-driven-class
blueprint-engine --repo . resolve-binding model.interface-driven-class format.mermaid.class
blueprint-engine --repo . style style.technical-dark
blueprint-engine --repo . resolve-style-binding format.mermaid.class
blueprint-engine --repo . generation-plan examples/generation/interface-driven-mermaid.yaml
```

## Existing CLI

```bash
blueprint-engine --repo . catalog
blueprint-engine --repo . match typed_entities cardinality
blueprint-engine --repo . route canonical.core format.mermaid.class
blueprint-engine --repo . transform examples/cross-format/embedded-controller/model.yaml format.mermaid.class
blueprint-engine --repo . validate format.mermaid.class examples/cross-format/embedded-controller/model.mmd --require-runtime
blueprint-engine --repo . mermaid-ast examples/cross-format/embedded-controller/model.mmd
blueprint-engine --repo . mermaid-import examples/cross-format/embedded-controller/model.mmd -o /tmp/model.yaml
```

Architecture rules for future implementation live in `docs/framework-architecture.md`.
