# 000-UPDATE — Architecture Rebuild Workspace

## Purpose

`000-UPDATE/` is an isolated architecture-development workspace for rebuilding the framework from first principles.

The existing repository structure, schemas, registries, engine implementation and documentation are **not architectural inputs** to Phase 1. They may contain useful implementation work, but they are treated as provisional until the new foundational architecture has been defined.

## Working rule

Architecture is defined here first. Existing repository artifacts are evaluated only after the relevant architecture phase is complete.

Until an architecture baseline is approved:

- do not rewrite existing schemas;
- do not reorganize production directories;
- do not retrofit the existing engine to emerging concepts;
- do not preserve an existing abstraction merely because code already depends on it;
- do not delete existing implementation solely because it conflicts with unfinished architecture;
- record architecture decisions and unresolved questions inside this workspace;
- follow `MODEL-ROUTING.md` before starting each new phase;
- stop and notify the user before entering a phase that requires a different recommended model.

## Current sequence

1. `00-work-rules.md` — isolation, sequencing and model-transition rules.
2. `MODEL-ROUTING.md` — model allocation and mandatory phase-boundary switching instructions.
3. `01-foundational-architecture.md` — Phase 1 foundational information model.
4. Only after Phase 1 is complete and the model-transition gate is satisfied: inspect the current repository and classify existing work against the new foundation.

## Current model route

- Phase 1 — Foundational architecture: **Sol**.
- Phase 1A — Existing-repository disposition: **Terra**.
- Phase 2 — Authority and ownership architecture: **Sol**.

The complete phase/model table is in `MODEL-ROUTING.md`.

## Status

Phase 0: active workspace established.

Phase 1: foundational architecture candidate exists in `01-foundational-architecture.md`.

No production architecture is changed merely by material being added to this folder. This workspace becomes authoritative only when a later architecture-baseline phase explicitly promotes its decisions.
