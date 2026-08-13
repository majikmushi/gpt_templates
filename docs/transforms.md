# Transformation Model

Transforms execute mappings after model, format, version and binding choices have been resolved.

## Responsibilities

Transforms may perform:

- source -> canonical import;
- canonical -> target export;
- target -> canonical import;
- target -> target conversion;
- normalization;
- enrichment;
- projection/simplification.

A transform must not choose a different representation format merely because it is easier to encode.

## Transformation mechanisms

1. Built-in format encoders for syntax/serialization targets.
2. Declarative `select -> match -> emit` mappings for structured projections.

Representation bindings define model-to-format semantics. Transforms implement those resolved mappings; they are not a substitute for the binding layer.

## Runtime result

A built-in transform returns:

- transform ID;
- target format;
- media type;
- fidelity;
- explicit losses;
- deterministic source hash;
- representation-binding provenance when supplied;
- exact target-format version when supplied;
- semantic overlay provenance.

Higher-level generation execution should additionally record style/style-binding and renderer compatibility data from the resolved plan.

## Version discipline

A transform implementation may support several registered format releases, but generation planning resolves an exact release before execution. Transform code must not silently emit syntax from a newer format version than the plan targets.

## Routing and round trips

The conversion graph uses `binding-dependent` for paths whose semantics depend on a representation binding. Projection and loss must remain explicit. Round-trip equivalence is established only by semantic comparison of the recovered canonical model.
