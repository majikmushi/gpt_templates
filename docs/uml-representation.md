# UML Representation Strategy

UML is modeled as a **semantic/metamodel language family**, not as one text grammar or one renderer syntax.

```text
UML specification evidence
    |
    +-- metamodel source
    +-- semantic/constraint source
    +-- serialization source
    +-- conformance evidence
    +-- documentation source
    |
    v
language.uml
    |
    +-- metamodel
    +-- semantics
    +-- constraints
    +-- views
    +-- serializations
    +-- capabilities
    |
    +--> UML validators
    +--> XMI/serialization adapters
    +--> UML diagram/view definitions
    +--> Mermaid / PlantUML representation bindings
```

## Normalized language definition

`language-definitions/uml/manifest.yaml` is the common ingestion target. It is currently `scaffold-unpinned` and deliberately makes no normative UML version claim.

A future implementation should pin an explicit UML specification version and then populate the definition through specification source adapters. This prevents the framework from confusing a tool-specific textual notation with UML itself.

## Model, view, serialization and rendering are separate

The framework keeps these concepts distinct:

```text
UML semantic model
    != UML diagram/view
    != UML interchange serialization
    != UML rendering syntax
```

A class diagram is therefore a view/binding over part of a UML model. PlantUML or Mermaid may visualize compatible subsets, while XMI or another interchange format can carry model serialization. Fidelity is declared per transform/binding.

## Current status

The repository already seeds UML structural and behavioural diagram categories and a repository class-interchange representation. Those are useful framework artifacts, but they are not advertised as normative UML conformance.

The new specification-ingestion layer makes future UML support fit without changing the Mermaid implementation or forcing a parser-centric abstraction onto UML.
