# Executable Representation Engine

The Python engine under `tooling/blueprint_engine/` executes repository contracts. Version 0.3 adds first-class abstract-model, representation-binding and style resolution while preserving the earlier direct transform API.

## Planning pipeline

```text
Generation request
  -> validate request
  -> resolve abstract model
  -> accept chosen format
  -> resolve representation binding inside chosen format
  -> resolve semantic overlays
  -> resolve style profile
  -> resolve format-specific style binding
  -> execution plan
```

The planner never substitutes a different format because another binding would be easier. `representation.format` is required by `schemas/generation-request.schema.json`.

Example:

```bash
blueprint-engine --repo . generation-plan examples/generation/interface-driven-mermaid.yaml
```

The returned plan includes `format_selection: chosen-not-auto-selected`, the resolved representation binding, optional style/style binding, overlays and execution order.

## Framework resolution commands

```bash
blueprint-engine --repo . abstract-model model.interface-driven-class
blueprint-engine --repo . representation-binding binding.interface-driven-class.mermaid-class
blueprint-engine --repo . resolve-binding model.interface-driven-class format.mermaid.class
blueprint-engine --repo . style style.technical-dark
blueprint-engine --repo . style-binding style-binding.mermaid.class
blueprint-engine --repo . resolve-style-binding format.mermaid.class
blueprint-engine --repo . framework-validate abstract-model abstract-models/interface-driven-class.yaml
```

## Current execution boundary

The new planning/resolution layer is executable. Existing `transform` handlers still use the legacy `profile_id`/overlay transform interface internally. Future transform work should consume the resolved generation plan directly rather than adding more format-specific meaning to `profile_id`.

That migration should preserve the compatibility transform API until callers have moved to generation requests.

## Language/specification layer

Language definitions and specification source adapters remain separate from model selection. They describe target representation systems and feed capability/validation authority.

Commands include:

```bash
blueprint-engine --repo . language-definition language.mermaid.class-diagram
blueprint-engine --repo . language-definition-validate language-definitions/mermaid/class-diagram.yaml
blueprint-engine --repo . source-adapter-validate adapters/specification/mermaid.yaml
blueprint-engine --repo . source-check validators/mermaid/source-provenance.yaml /path/to/mermaid
```

## Existing transforms and assurance

The engine also provides canonical validation, capability matching, conversion routing, target transforms, Mermaid runtime validation/AST import, semantic comparison and supported round-trip checks.

See `docs/framework-architecture.md` for the architectural rules that new engine features must follow.
