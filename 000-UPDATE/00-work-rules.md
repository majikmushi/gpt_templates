# Phase 0 — Architecture Isolation Rules

## Objective

Develop the replacement architecture without allowing the current repository layout or implementation to become a de facto constraint.

## Scope

Phase 0 creates a controlled scratch workspace only. It does not redesign implementation artifacts.

## Rules

1. `000-UPDATE/` is the sole working area for architecture-rebuild material until the new architecture is baselined.
2. Existing schemas, registries, manifests, transforms, code, tests and documentation are implementation evidence, not architectural authority.
3. Existing names may be reused later only when the new architecture independently justifies the same concept.
4. No production schema is rewritten before the conceptual architecture that governs it is complete.
5. No existing implementation is deleted before it has been assessed against the completed foundational architecture.
6. Architecture work must distinguish semantic decisions from implementation convenience.
7. Every later implementation work package must cite the architectural rule it implements.
8. If existing implementation conflicts with the new architecture, implementation changes; architecture is not silently bent around old code.
9. If implementation review reveals a genuine missing architectural concern, it is returned to the architecture workspace as an explicit issue rather than solved ad hoc in code.
10. Conversation history is not an architectural state store. Decisions required by later passes must be persisted in this workspace.
11. Each phase SHALL declare its recommended model class and minimum acceptable model class.
12. A phase SHALL NOT silently continue into a phase that requires a different model class.

## Model transition gate

Model selection is an explicit execution concern for this architecture-rebuild process.

Before substantive work begins on any phase, the acting agent SHALL read `000-UPDATE/MODEL-ROUTING.md` and determine the model class required for that phase.

When the next phase has a different recommended model from the current phase, the acting agent SHALL stop at the phase boundary and:

1. complete the current phase's bounded objective;
2. persist all architectural decisions, unresolved issues, evidence references, and resume instructions into `000-UPDATE/`;
3. verify that a fresh context can continue without relying on conversational history;
4. identify the next phase by number and name;
5. notify the user of the recommended model to select;
6. state why that model class is appropriate for the next phase;
7. NOT begin substantive work on the next phase until the user continues after the model change.

The notification SHOULD use this form:

```text
Phase <N> complete.
Next phase: <N+1> — <name>.
Recommended model: <Sol|Terra|Luna>.
Please switch to <model> before continuing.
```

If consecutive phases use the same recommended model, no model-change interruption is required, but the phase boundary and persisted checkpoint still apply.

If a named model is unavailable, the agent SHALL stop and tell the user that the required model class is unavailable rather than silently substituting a materially weaker class. The user may explicitly authorize an equivalent or stronger substitute.

## Phase declaration requirement

Every phase document created under `000-UPDATE/` SHOULD begin with an execution declaration equivalent to:

```yaml
phase: 1
name: foundational-architecture
recommended_model: Sol
minimum_model: Sol
requires_model_transition_from_previous: true
status: candidate
```

This declaration is workflow metadata, not part of the eventual production architecture.

## Phase gate

Phase 1 may complete before any inventory/disposition analysis of the current repository is used to influence the architecture.

Only after Phase 1 is coherent may the repository be inspected for:

- concepts worth keeping;
- implementation worth adapting;
- artifacts that should be replaced;
- artifacts that should be deleted;
- unrelated material that can remain untouched.

That inspection is a separate phase and SHALL follow the model-routing gate before substantive classification work begins.
