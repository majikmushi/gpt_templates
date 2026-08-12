# Artifact Model

All reusable repository objects should expose a common manifest vocabulary.

## Common metadata

- `id` - stable namespaced identifier.
- `kind` - artifact kind.
- `version` - artifact version.
- `status` - experimental, stable, deprecated, superseded, or retired.
- `title` - human-readable name.
- `description` - concise purpose.
- `tags` - discovery tags.
- `extends` - inherited artifacts.
- `depends_on` - required artifacts/tools.
- `compatibility` - format/tool/version constraints.
- `provenance` - origin and derivation metadata.

## Composition

Artifacts may be composed through:

- inheritance (`extends`)
- inclusion
- mixins/fragments
- overlays
- parameterization
- transform chains

Avoid copying definitions solely to make a variation.

## Lossiness

Transforms and mappings should declare one of:

- `lossless`
- `lossy`
- `presentation_only`
- `reversible`
- `round_trip_safe`

A transform can be syntactically valid while still losing semantics; that is a separate concern and must be recorded.
