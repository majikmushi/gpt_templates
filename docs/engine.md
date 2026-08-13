# Representation Framework Engine

The Python package under `tooling/blueprint_engine/` resolves framework contracts and executes transformations.

## Planning pipeline

```text
Generation request
 -> validate request
 -> resolve abstract model
 -> accept chosen format
 -> resolve exact format release
 -> resolve representation binding
 -> check binding/version capabilities
 -> resolve semantic overlays
 -> resolve style + style binding
 -> check style/version capabilities
 -> optional chosen renderer release
 -> renderer-format compatibility contract
 -> effective renderer capability check
 -> execution plan
```

Generation planning is separate from rendering. It can therefore report unsupported/unverified combinations before a concrete renderer is invoked.

## Version APIs

- `format_release(format_id, version=..., version_constraint=...)`
- `renderer_release(renderer_id, version=...)`
- `renderer_compatibility(renderer_id, renderer_version, format_id, format_version)`

Ordered constraints use PEP 440 only for registries that explicitly declare that version scheme. Formats with opaque/non-ordered version schemes must use exact registered releases.

## Compatibility modes

`strict` fails unresolved/incompatible combinations.

`warn` preserves the caller's choices and records compatibility uncertainty as warnings. It does not upgrade an unverified combination into a verified one.

## Low-level transforms

The `transform` interface remains a low-level canonical encoder. It accepts binding identity and exact target-format version for provenance. Higher-level generation should use `generation-plan` first so version, style and renderer contracts are resolved consistently.

## Validation

Validation remains layered:

- canonical schema/semantic validation;
- framework artifact schema validation;
- target syntax validation;
- source/runtime validation where authoritative;
- renderer compatibility validation when rendering is requested;
- semantic equivalence/round-trip testing.

## CLI examples

```bash
blueprint-engine --repo . generation-plan request.yaml
blueprint-engine --repo . format-release format.mermaid.class --constraint '>=11,<12'
blueprint-engine --repo . renderer-release renderer.mermaid-js --version 11.4.1
blueprint-engine --repo . renderer-compatibility renderer.mermaid-js 11.4.1 format.mermaid.class 11.4.1
blueprint-engine --repo . framework-validate renderer-compatibility renderer-compatibility/mermaid-js-mermaid-class-11.4.1.yaml
```

## Extension rule

New code should operate on abstract models, bindings, exact format releases, styles and renderer compatibility contracts. Removed profile-layer identities are not accepted as aliases or migration inputs.
