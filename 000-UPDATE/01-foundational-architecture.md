# Phase 1 — Foundational Architecture

## Status

Foundational architecture candidate.

This document deliberately defines the information/ownership model without reference to the current repository structure or schemas.

## 1. Foundational premise

A design is an evolving body of engineering meaning. For an agent-driven system, that meaning must exist independently of any individual model context or conversation.

The framework therefore treats the **Authoritative Design Representation** as the persisted, machine-readable encoding of the current design state.

The central rule is:

> If a fresh Designer / Engineer Agent cannot reconstruct the current design, its engineering significance, and its unresolved state from persisted project information without relying on prior conversation context, the design representation is incomplete.

The representation is not merely documentation produced after design. It is the durable encoded form through which the design is stored, retrieved, transformed, reviewed and continued.

## 2. Design and representation are related but not identical concepts

### Design

The design is the engineering meaning: the things that exist, their properties and relationships, intended behaviour, constraints, requirements, decisions, assumptions, unresolved questions and other engineering-significant information.

### Authoritative Design Representation

The Authoritative Design Representation (ADR) is the durable encoding of that design meaning.

The ADR is the authoritative machine-readable design state for agent execution. It must preserve identity and semantic meaning independently of a particular diagram language, renderer or conversational context.

The ADR is not required to look like a diagram. It is an information representation from which engineering views and other encodings can be derived.

### Representation View

A Representation View is an intentional perspective over the ADR. A view selects and organizes design semantics for a purpose such as physical architecture, logical communication, interface definition, dependency analysis, power distribution, requirements traceability, security or another engineering concern.

A view may contain the whole design or only a deliberate subset.

### Concrete Representation Artifact

A Concrete Representation Artifact is a serialized or rendered encoding of a view in a chosen representation system and release, for example a Mermaid artifact, UML artifact, PlantUML text, Graphviz representation, machine-readable interchange object, report, or future format.

A concrete artifact is not automatically the authoritative design state.

### View-local State

View-local state affects presentation of a particular representation without changing engineering meaning. Examples include layout, position, label placement, collapsed groups, visual routing and other display-specific choices.

### Execution State

Execution state records where an agent is in a multi-pass process: stages, checkpoints, completed work, unresolved items and resume instructions. It is operational state, not design meaning.

These states must not be conflated.

## 3. The authoritative information layers

The architecture requires at least four logically separate information layers:

1. **Engineering semantic state** — the actual design meaning.
2. **Representation state** — how portions of that meaning are organized into views and bound to representation systems.
3. **View-local presentation state** — layout/style information specific to an artifact or view.
4. **Agent execution state** — staged-work state used to survive context limits and resume work.

A change in one layer must not silently mutate another layer.

For example:

- moving a node is normally view-local state, not an engineering change;
- changing an interface endpoint is an engineering semantic change;
- selecting a different colour palette is style/presentation state;
- assigning colour to encode a trust zone is representation of semantic state and must remain recoverable independently of colour alone;
- advancing from analysis pass 2 to pass 3 is execution state only.

## 4. Persistence is the memory boundary

The conversational context of any agent is transient and non-authoritative.

All information needed to resume engineering work must be persisted outside the context window.

This includes, as applicable:

- current design state;
- accepted decisions;
- assumptions and uncertainties;
- design revision/baseline identity;
- representation/view definitions;
- provenance and evidence references;
- unresolved issues;
- execution checkpoints and resume contracts.

A later agent instance must be able to load persisted state and continue without reconstructing prior reasoning from chat history.

## 5. Stable engineering identity is fundamental

Engineering objects require stable identities that survive changes in representation.

The same engineering object may appear as different primitives in different representation systems while retaining one engineering identity.

Therefore:

> Engineering identity is independent of representation primitive identity.

A component represented as a UML Component, Mermaid node, PlantUML class-like primitive, JSON object or other format remains the same engineering object if all representations reference the same stable semantic identity.

This identity principle is necessary for:

- multi-view consistency;
- change detection;
- round-trip import/export;
- coverage accounting;
- provenance;
- revision comparison;
- retrieval by future agents.

## 6. One design may have many views

No single diagram or view is assumed to contain every aspect of a non-trivial engineering design.

The ADR may be represented through multiple complementary views, each optimized for a specific concern.

Examples include:

- system context;
- physical architecture;
- logical architecture;
- communications interfaces;
- power distribution;
- dependencies;
- state/behaviour;
- requirements traceability;
- ownership;
- security/trust boundaries;
- deployment;
- failure/redundancy structure.

The views collectively represent the same underlying design identities.

The architecture must be able to account for which design semantics are represented in which views.

## 7. Representation is an encoding operation, not a redesign operation

Transforming the ADR into another representation may reorganize, project, annotate or visually encode the design, but it must not silently change engineering meaning.

A representation process may:

- choose a suitable abstract representation model for a requested view;
- bind semantic concepts to primitives of a chosen format;
- allocate visual channels;
- apply semantic overlays;
- apply presentation style;
- split a complex representation into multiple views;
- declare deliberate projection or approximation.

It may not:

- invent domain facts to make a diagram cleaner;
- remove engineering information without declaring the loss;
- change an engineering relationship because a target format is inconvenient;
- treat renderer behaviour as engineering truth;
- silently substitute another representation format when a format was explicitly chosen.

## 8. External representations have explicit recoverability

A Concrete Representation Artifact may be:

- losslessly recoverable;
- semantically equivalent for a defined subset;
- bidirectional with known limitations;
- a deliberate projection;
- approximate;
- export-only;
- presentation-only.

No representation is assumed to be a complete design source merely because it can be parsed.

A representation may be used to reconstruct the full design only when its binding/import contract establishes sufficient semantic recoverability for the required scope.

Otherwise the ADR remains the complete authoritative design representation and the external artifact is a view of it.

## 9. Round-trip edits require change classification

When an editable external representation is imported, differences must be classified before the ADR is changed.

At minimum the architecture must distinguish:

- engineering semantic change;
- semantic-overlay change;
- annotation/documentation change;
- style change;
- view-local/layout change;
- ambiguous/unresolvable change.

Automatic write-back to engineering state is permitted only where the import/binding contract can classify the change deterministically and policy permits it.

Ambiguous changes become explicit proposals/issues rather than silent design mutations.

## 10. Fidelity and coverage are first-class properties

A successful render is not proof that the design has been represented faithfully.

Every representation path must be capable of declaring:

- what was represented exactly;
- what was represented equivalently through another primitive;
- what was projected;
- what was approximated;
- what appears in another view;
- what was intentionally omitted;
- what is unsupported;
- what remains unresolved.

Coverage is measured against engineering semantic identities, not visual element count.

Known semantic loss must be explicit and auditable.

## 11. Format, format release, renderer and renderer release are separate

The representation system selected for a view is conceptually independent from the particular version of that system and from the renderer used to realize it.

The architecture therefore distinguishes:

- representation format identity;
- exact format/specification release;
- renderer/tool identity;
- renderer/tool release;
- compatibility evidence between them.

A renderer limitation must not be misclassified as a limitation of the representation format itself.

Unknown compatibility remains unknown until evidence exists.

## 12. Semantic overlays and style are separate

Additional semantic dimensions may be encoded through visual or structural channels. Examples include trust zone, lifecycle, ownership, voltage domain or criticality.

These are semantic overlays because they carry meaning.

Style controls presentation such as palette, typography, spacing, connector appearance and grouping treatment.

Style must never redefine engineering semantics. When presentation conflicts with semantic encoding, semantic meaning has priority and the style must degrade or be remapped.

## 13. The Designer / Engineer Agent operates on the ADR

The Designer / Engineer Agent is the semantic design authority within its assigned engineering role.

Its normal engineering process reads and evolves the ADR. Representation capture is therefore not a separate form completed after design; the persisted design representation evolves inline with engineering work.

At any later point, a fresh Designer / Engineer Agent can retrieve the ADR, the required revision/baseline, and unresolved engineering state, then continue work.

The agent should not need to parse presentation artifacts merely to remember what it previously designed when the authoritative representation is available.

## 14. The Specification / Representation Agent operates across the representation boundary

The Specification / Representation Agent consumes the ADR and representation intent, then creates and validates one or more views/artifacts.

Its role is to faithfully encode design meaning, not to become the design authority.

It may also import supported external representations and identify proposed changes back toward the ADR, subject to recoverability and change-classification rules.

## 15. Multi-pass execution is a fundamental operating mode

Complex engineering and representation work may exceed a single model context.

The architecture therefore assumes staged, bounded passes with persisted checkpoints.

A completed pass must leave enough machine-readable state for another context to resume without the earlier conversation.

The authoritative design state and the agent execution state are persisted separately so that a workflow checkpoint cannot accidentally become engineering truth.

## 16. Revision and baseline principle

The ADR is evolutionary rather than a single mutable blob with no history.

The architecture must support identifying which design revision or baseline a representation was derived from.

A representation artifact must therefore be traceable to the design state that produced it.

The precise revision/event storage mechanism is intentionally deferred to later architecture phases; Phase 1 only establishes the requirement.

## 17. Source-of-truth rules

The foundational source-of-truth policy is:

1. Engineering meaning is authoritative in the ADR.
2. Representation/view definitions are authoritative for how that meaning is selected and encoded for a view.
3. View-local state is authoritative only for that view's presentation.
4. Execution state is authoritative only for workflow continuation.
5. External artifacts are authoritative for engineering semantics only to the extent explicitly established by a reversible/import contract and accepted change policy.
6. Conversation history is never an authoritative source of persisted design state.

## 18. Retrieval requirement

A valid implementation of this architecture must eventually support the conceptual operation:

`retrieve design <design-id> [revision/baseline]`

The result must provide sufficient persisted semantic and process state for an appropriately authorized Designer / Engineer Agent to understand the design and continue work without access to the conversation that created it.

The exact API and storage format are implementation concerns and are deliberately not specified in Phase 1.

## 19. Architectural invariants established by Phase 1

The following are foundational and should be treated as constraints on later phases:

1. The design must survive the loss of conversation context.
2. The ADR is the persisted machine-readable encoding of engineering design state.
3. Engineering identity is stable across representation systems and views.
4. A concrete diagram/artifact is a representation of design state, not automatically the complete design state.
5. One design may have multiple complementary views.
6. Engineering semantic state, representation state, view-local state and execution state are distinct.
7. Representation may project or approximate only when loss/fidelity is explicit.
8. External edits require semantic change classification before affecting engineering state.
9. Format/version and renderer/version compatibility are independent concerns.
10. Semantic overlays carry meaning; style does not.
11. A future agent must be able to reconstruct the design from persisted state.
12. Representation coverage is measured against design semantics, not visual completeness.
13. Multi-pass execution must persist resumable state outside the model context.
14. Existing implementation does not constrain these invariants.

## 20. Deliberately unresolved for later phases

Phase 1 does not decide:

- concrete schemas;
- directory structure outside `000-UPDATE/`;
- storage engine;
- exact identifier syntax;
- exact revision/event model;
- exact engineering domain metamodel;
- agent command syntax;
- synchronization/merge policy for concurrent edits;
- implementation language;
- exact abstract-model catalogue;
- exact file formats for persisted state.

Those decisions must be derived from later architectural analysis rather than prematurely embedded into implementation.

## 21. Phase 1 completion test

Phase 1 is considered coherent if the following question has an unambiguous answer:

**Where does the design live, independently of any agent context or diagram format?**

Answer:

> The design lives as engineering meaning encoded in the persisted Authoritative Design Representation. Views and concrete artifacts encode selected aspects of that design; agent execution state records how work proceeds; neither conversation history nor presentation artifacts are implicitly the design authority.
