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

## Phase gate

Phase 1 may complete before any inventory/disposition analysis of the current repository is used to influence the architecture.

Only after Phase 1 is coherent may the repository be inspected for:

- concepts worth keeping;
- implementation worth adapting;
- artifacts that should be replaced;
- artifacts that should be deleted;
- unrelated material that can remain untouched.
