# Validation Model

Validation is a first-class artifact type.

## Validation layers

1. **Schema** - required fields, data types, enums, structural constraints.
2. **Syntax** - target grammar/parser acceptance.
3. **Semantic** - references, relationships, cardinality, dependency and domain consistency.
4. **Format constraints** - target-specific restrictions and forbidden combinations.
5. **Compatibility** - feature/version/renderer support.
6. **Lint** - valid but undesirable patterns.
7. **Runtime/render** - parser or renderer behaviour where static validation is insufficient.
8. **Fixture/regression** - known-valid and known-invalid cases.

## Severity

- `error`
- `warning`
- `compatibility`
- `lint`
- `suggestion`

## Validator sources

Validators should record whether rules came from:

- formal grammar
- source code
- official documentation
- renderer/runtime behaviour
- repository policy
- profile-specific semantics

For Mermaid, the eventual validator should be derived from the Mermaid source tree and parser behaviour, not documentation alone.
