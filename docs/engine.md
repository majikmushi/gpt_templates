# Executable Representation Engine

## Purpose

The repository now contains an executable Python engine under `tooling/blueprint_engine/`. It turns the framework manifests into an operational pipeline instead of leaving them as design contracts only.

## Runtime pipeline

```text
Canonical source
  -> canonical schema + semantic checks
  -> capability/profile selection
  -> transform handler or declarative mapping
  -> target artifact
  -> target validator
  -> provenance record
  -> optional semantic/round-trip comparison
```

## Built-in target transforms

| Target | Output | Fidelity policy |
|---|---|---|
| Mermaid classDiagram | `.mmd` text | profile-dependent |
| PlantUML | `.puml` text | profile-dependent |
| UML class interchange | JSON object | lossless for supported structural subset |
| JSON Schema | JSON Schema 2020-12 | explicit projection |
| XML | repository XML model profile | profile-dependent, round-trip capable |
| Markdown | documentation view | presentation-only |

Transform results always carry a transform ID, target format, declared fidelity, explicit loss list, and deterministic source hash.

## Declarative mapping engine

`DeclarativeMappingEngine` provides the XSLT-like generic layer.

A mapping spec selects a canonical collection, matches objects, and emits target objects:

```yaml
target:
  nodes: []
  edges: []

rules:
  - select: elements
    match:
      type: component
    emit_to: nodes
    emit:
      id: $.id
      label: $.name
      kind: $.type
```

This engine is intentionally data-oriented. Syntax-specific encoders remain separate so format grammar concerns do not contaminate semantic mapping rules.

## Validation

Validation is layered:

1. canonical JSON Schema validation;
2. canonical semantic checks such as unique IDs and valid endpoints;
3. target-specific validation;
4. explicit scope warnings where validation is not normative.

Current target validation:

- JSON Schema: Draft 2020-12 meta-schema checking;
- XML: well-formedness plus repository-profile root checks;
- Mermaid: engine-generated classDiagram subset only;
- PlantUML: wrapper and structural balance checks;
- UML: repository interchange model consistency, not the normative UML metamodel;
- Markdown: basic document structure.

## Semantic comparison

Canonical models are compared independently of ordering and non-semantic metadata.

Classifications:

- `exact`
- `equivalent`
- `projection`
- `non-equivalent`

Round-trip claims only pass when the recovered canonical model compares as `exact` or `equivalent`.

## Extension points

Add a format by implementing:

1. a format manifest;
2. capability entries;
3. a transform/export handler;
4. an optional import handler;
5. a validator;
6. fixtures and tests;
7. conversion-graph edges.

Full Mermaid validation remains a separate task and should be derived from the Mermaid grammar/source/runtime rather than inferred from documentation.
