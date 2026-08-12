# Executable Representation Engine

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

The Python package lives under `tooling/blueprint_engine/`.

## Mermaid native integration

Version 0.2 adds an optional Node bridge that uses Mermaid itself for syntax validation
and AST extraction. This avoids duplicating Mermaid's parser.

```text
Mermaid source
 -> native mermaid.parse()
 -> native getDiagramFromText()
 -> diagram DB
 -> normalized AST
 -> canonical adapter
```

For class diagrams the native `ClassDB` is adapted into canonical elements,
relationships, containers and annotations.

Install the bridge:

```bash
cd tooling/blueprint_engine/node
npm install
```

Require authoritative native validation with:

```bash
blueprint-engine --repo . validate format.mermaid.class model.mmd --require-runtime
```

Extract/import:

```bash
blueprint-engine --repo . mermaid-ast model.mmd
blueprint-engine --repo . mermaid-import model.mmd -o model.yaml
```

Without the Node runtime/package the engine retains source-derived preflight checks and
emits a warning; it never silently claims native parser validation occurred.

## Built-in target transforms

| Target | Output | Fidelity |
|---|---|---|
| Mermaid classDiagram | `.mmd` | profile-dependent |
| PlantUML | `.puml` | profile-dependent |
| UML class interchange | JSON | structural-subset lossless |
| JSON Schema | JSON Schema 2020-12 | explicit projection |
| XML | repository XML profile | round-trip capable subset |
| Markdown | documentation | presentation-only |

## Declarative mapping

`DeclarativeMappingEngine` provides the XSLT-like data transformation layer using
`select -> match -> emit`. Syntax-specific encoders stay separate from semantic mapping.

## Validation

- canonical JSON Schema + reference checks;
- Mermaid native parser plus source-derived preflight when runtime is installed;
- JSON Schema meta-schema validation;
- XML well-formedness;
- UML repository-interchange consistency;
- PlantUML/Markdown structural checks.

## Provenance

Mermaid source rules have their own provenance manifest containing source repository,
branch, commit, package version and individual Git blob SHAs. A local Mermaid checkout
can be checked against that manifest with `check_mermaid_source()`.

## Round trips

XML and UML-class interchange have tested canonical round trips. Mermaid class import is
implemented through the native runtime; semantic equivalence remains profile-dependent
because a representation profile may intentionally overload or project Mermaid
primitives.
