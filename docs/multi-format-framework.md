# Multi-Format Representation Framework

The framework separates meaning from representation and now includes an executable engine.

```text
Domain data
  -> Canonical semantic model
  -> Capability matching
  -> Representation profile
  -> Transform
  -> Target format
  -> Validator
  -> Provenance
  -> Optional semantic equivalence / round trip
```

## Seeded formats

- Mermaid
- UML
- PlantUML
- JSON Schema
- XML / XSLT
- Markdown

The engine currently exports the canonical model to all six representative families. UML is represented by a machine-readable class interchange object; Mermaid and PlantUML are text encodings; JSON Schema is an explicitly lossy schema projection; XML is a loss-preserving repository profile for the supported structural model; Markdown is presentation-only.

## Why the canonical layer matters

A primitive's conventional meaning is not a hard semantic boundary. Profiles may map the same abstract concept to different target primitives, or use visual channels such as colour, grouping, borders and annotations as additional semantic dimensions.

The canonical model therefore stores semantic relationships before representation choices are applied.

## Operational status

The framework is no longer contract-only. `tooling/blueprint_engine/` implements catalog discovery, capability matching, route selection, transformation, validation, provenance and semantic comparison.

Normative language-specific validators remain separate work streams.
