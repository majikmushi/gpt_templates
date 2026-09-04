# Architecture Rebuild Model Routing

This file defines which model class should execute each architecture-rebuild phase and when the agent must stop to ask the user to change models.

## Mandatory transition behaviour

- Every phase starts by checking this file.
- If the next phase has a different recommended model, stop at the boundary and notify the user before doing substantive work.
- Persist a resume-safe checkpoint in `000-UPDATE/` before asking for the model change.
- Do not rely on chat history as the only carrier of phase state.
- A stronger model may perform a weaker-model phase if the user explicitly chooses to do so, but a weaker model must not silently perform a stronger-model phase.

## Routing table

| Phase | Name | Recommended | Minimum | Purpose |
|---|---|---:|---:|---|
| 0 | Workspace isolation and work rules | Terra | Terra | Procedural setup and isolation |
| 1 | Foundational architecture | Sol | Sol | Define what the design/representation system fundamentally is |
| 1A | Existing-repository disposition against Phase 1 | Terra | Terra | Classify existing work as keep/adapt/replace/delete/defer without changing the foundation |
| 2 | Authority and ownership boundaries | Sol | Sol | Define who owns design meaning, representation, framework rules and changes |
| 3 | Authoritative design-state architecture | Sol | Sol | Define recoverable persisted design state independent of conversation context |
| 4 | Representation architecture | Sol | Sol | Define views, abstract models, formats, bindings, overlays, style and renderer separation |
| 5 | Round-trip and change semantics | Sol | Sol | Define semantic recovery, edit classification and design-update rules |
| 6 | Coverage and fidelity architecture | Sol | Terra | Define exact/equivalent/projected/approximate/unsupported coverage accounting |
| 7 | Staged agent execution architecture | Sol | Terra | Define stages, passes, checkpoints, resume contracts and state ownership |
| 8 | Designer / Engineer Agent contract | Sol | Terra | Define engineering role, inline capture and retrieval responsibilities |
| 9 | Specification Agent contract | Sol | Terra | Define representation executor role and prohibitions |
| 10 | Inter-agent protocol | Sol | Terra | Define shared-state interaction, requests, feedback and change proposals |
| 11 | Architecture consolidation and contradiction review | Sol | Sol | Produce one coherent architectural baseline candidate |
| 12 | Architecture baseline / freeze | Terra | Terra | Formalize approved architecture and freeze implementation authority boundaries |
| 13 | Repository implementation impact analysis | Terra | Terra | Compare frozen architecture with existing code/artifacts |
| 14 | Implementation work-package decomposition | Terra | Terra | Break implementation into bounded, testable packages |
| 15 | Schema rewrite/creation | Luna | Luna | Mechanical encoding of frozen conceptual models |
| 16 | Registry and manifest rewrite | Luna | Luna | Mechanical catalog/manifest implementation |
| 17 | Engine implementation | Terra | Terra | Integrate architecture into executable framework code |
| 18 | Tests and fixtures | Luna | Luna | Derive routine tests/fixtures; escalate difficult semantic cases to Terra |
| 19 | Documentation normalization | Luna | Luna | Bring subordinate docs into conformance with frozen architecture |
| 20 | Final architecture conformance review | Sol | Sol | Verify architecture, schemas, code, tests and docs agree |

## Immediate route

Current architectural work is Phase 1 and requires **Sol**.

After Phase 1 is explicitly accepted as coherent, the next bounded task is **Phase 1A — existing-repository disposition**, which should be executed with **Terra**.

After Phase 1A is persisted, the process returns to **Sol** for Phase 2.

## Escalation rule

If a Terra or Luna phase uncovers a question that changes architectural meaning rather than merely implementing it, that question is not resolved locally. The phase records the issue and routes it back to the appropriate Sol architecture phase.
