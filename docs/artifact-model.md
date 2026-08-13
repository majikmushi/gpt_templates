# Artifact Model

All reusable framework objects expose stable identity, version/status and explicit compatibility/provenance where relevant.

## Common metadata

- `id` - stable namespaced identifier.
- `kind` - artifact kind.
- `version` - version of the framework artifact itself.
- `status` - implementation/evidence status.
- `title` / `description` - human-readable purpose.
- `compatibility` - format/version/capability constraints when applicable.
- `provenance` - origin and derivation evidence.

Do not confuse an artifact's own `version` with a version of an external format or renderer. External releases have dedicated first-class artifacts.

## Important artifact kinds

- `abstract-representation-model` (`model.*`)
- `representation-binding` (`binding.*`)
- `style-profile` (`style.*`)
- `style-binding` (`style-binding.*`)
- `format-version` (`format-version.*`)
- `renderer` (`renderer.*`)
- `renderer-compatibility` (`compatibility.renderer.*`)
- normalized language definitions
- transforms/adapters
- validators
- fixtures/provenance records

## Composition

Composition may use inheritance, inclusion, overlays, parameterization and transform chains. Semantic overlays and presentation styles remain distinct composition mechanisms.

## Loss and fidelity

Transforms/bindings must report semantic loss explicitly. Supported vocabulary includes exact/high/binding-dependent/projection/approximate/lossy at binding level and more specific transform claims where appropriate.

Syntactic validity, successful rendering and semantic equivalence are independent claims.
