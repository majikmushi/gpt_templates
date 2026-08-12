# Multi-Format Representation Framework

The repository treats a representation language as a capability provider rather than a fixed semantic destination.

## Layers

1. **Ontology / canonical model** — format-independent meaning.
2. **Blueprint** — reusable abstract structure or intent.
3. **Representation profile** — maps domain concepts to target primitives.
4. **Overlay** — assigns extra semantic dimensions to visual or structural channels.
5. **Adapter** — reads/writes a concrete format.
6. **Transform** — converts between semantic/representation layers.
7. **Validator** — checks schema, syntax, semantics, compatibility and policy.
8. **Renderer** — turns a representation into a presentation artifact.
9. **Equivalence checker** — determines whether declared meaning was preserved.

## Seed format families

- Mermaid — textual diagrams and generic visual encoding.
- UML — tool-neutral modeling semantics.
- PlantUML — textual UML-oriented representation.
- JSON Schema — formal data shape/validation.
- XML — hierarchical structured data with schema ecosystems and XSLT.
- Markdown — human-readable documentation/presentation.

The set is deliberately heterogeneous so assumptions are tested across diagrams, schemas, structured trees and documents.
