# Representation Profiles and Bindings

Earlier repository versions used **representation profile** for two different ideas: an abstract model type and its mapping into a target format. Those responsibilities are now separated.

## Preferred terminology

- **Abstract representation model**: what kind of model is being constructed, independent of format.
- **Representation binding**: how one abstract model maps into one chosen format.
- **Semantic overlay**: additional semantic dimension layered onto the model.
- **Style profile**: presentation intent only.
- **Style binding**: format-specific realization of style intent.

Example:

```text
model.electronics-system
        +
format.mermaid.class
        =
binding.electronics-system.mermaid-class
```

The binding is the place where a Mermaid `class`, relation, namespace, annotation or other primitive may be deliberately repurposed to represent electronics semantics.

## Representation profile compatibility

The term `representation-profile` remains valid for complex mapping policies and legacy manifests, but it should not be used as the primary identity of a reusable abstract model.

Legacy:

```text
profile.domain.interface-driven-model
profile.mermaid.class.interface-driven-model
```

Preferred:

```text
model.interface-driven-class
binding.interface-driven-class.mermaid-class
```

`abstract-models/registry.yaml` records legacy domain-profile aliases.

## Binding responsibilities

A representation binding should declare:

- abstract model ID;
- chosen target format ID;
- relevant language definition;
- concept -> primitive mappings;
- relationship -> connector mappings;
- feature mappings;
- required target capabilities;
- fidelity;
- known losses;
- fallback representations where applicable.

A binding does **not** choose a representation format.

## Semantic overloading

A primitive's conventional meaning is a default, not an absolute semantic boundary. Explicit bindings make primitive overloading interpretable, transformable and testable rather than relying on undocumented convention.
