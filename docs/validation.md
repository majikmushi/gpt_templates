# Validation Model

Validation is a first-class artifact type. The executable engine separates **authority**
from **fallback checking** so a weak local checker cannot be mistaken for the target
language's parser.

## Layers

1. Schema validation.
2. Semantic/reference validation.
3. Native syntax/parser validation.
4. Source-derived format constraints.
5. Compatibility/version checks.
6. Lint/policy rules.
7. Runtime/render validation.
8. Fixture/regression validation.

## Mermaid authority model

Mermaid validation is now source-derived and runtime-backed.

The analysed source is `majikmushi/mermaid`, branch `develop`, commit
`446f6a7701065eb12e024475243434eb727dc172`, package version `11.4.1`.
Exact evidence-file SHAs are stored in `validators/mermaid/source-provenance.yaml`.

For syntax, Mermaid's own `parse()` is authoritative. Static Python rules are a
conservative preflight derived from the class-diagram Jison grammar, ClassDB,
ClassMember types and source tests; they are not a replacement parser.

When the optional Node bridge is installed:

```text
.mmd
 -> Mermaid parse()
 -> detected diagram type
 -> Mermaid Diagram/ClassDB
 -> normalized AST
 -> canonical adapter
```

When it is unavailable, validation reports the degradation explicitly. Use
`--require-runtime` to make missing native validation an error.

## Mermaid classDiagram reference implementation

The source-derived class validator records rules for:

- `classDiagram` and `classDiagram-v2` headers;
- `TB`, `BT`, `RL`, `LR` direction values;
- aggregation, extension, composition, dependency and lollipop relation markers;
- solid and dotted relation lines;
- quoted cardinality/end labels;
- quoted note text;
- link target values;
- member visibility and static/abstract classifiers;
- generic types;
- namespaces and annotations;
- lollipop-to-interface semantic normalization.

The AST adapter imports the parsed ClassDB rather than reparsing text in Python.

## Other formats

JSON Schema uses Draft 2020-12 meta-schema checking; XML uses well-formedness plus
repository-profile checks; UML currently validates the repository interchange model;
PlantUML and Markdown retain structural validators.

UML validation is still not a full OMG metamodel validator.
