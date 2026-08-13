# Profiles

`profiles/` is retained for compatibility and for advanced reusable mapping policies. It is no longer the preferred home for abstract model identities.

Use:

- `abstract-models/` for reusable model types;
- `representation-bindings/` for abstract-model -> chosen-format mappings;
- `overlays/` for additional semantic dimensions;
- `styles/` for presentation intent;
- `style-bindings/` for target-specific style translation.

Legacy `profile.domain.*` and `profile.mermaid.class.*` artifacts remain readable while migration proceeds. New model types must not be introduced as format-specific profiles.

See `docs/framework-architecture.md` and `migrations/abstract-model-layer-v1.yaml`.
