# Format Versions and Renderer Compatibility

## Purpose

Version support is modelled explicitly so the framework can answer three different questions without conflating them:

1. **What representation format was chosen?**
2. **Which exact release of that format will the artifact target?**
3. **Can a particular renderer release correctly realize that format release and the capabilities required by the selected bindings?**

## Four separate identities

```text
format.mermaid.class
        |
        +--> format-version.mermaid.class.11.4.1

renderer.mermaid-js
        |
        +--> renderer release 11.4.1

(format release, renderer release)
        |
        +--> explicit renderer compatibility contract
```

### Format

A stable representation-system target such as `format.mermaid.class` or `format.uml.class`.

### Format release

A versioned description of that target's syntax/metamodel/capabilities. Stored under `format-versions/`.

A format release records exact evidence and does not imply compatibility with earlier or later versions unless such support is separately established.

### Renderer

A concrete rendering implementation/tool. Stored under `renderers/`. Renderer versions evolve independently from abstract model bindings and, conceptually, independently from format versions even when both are shipped in one package.

### Renderer compatibility contract

An evidence-backed relation between a renderer-version range and a format-version range. Stored under `renderer-compatibility/`.

It declares `native`, `partial`, `unsupported`, or `unverified` support plus capability-level evidence and known issues.

## Why this separation matters

A file can be valid Mermaid syntax yet render differently or incompletely in different Mermaid integrations. Conversely, a renderer limitation does not mean the Mermaid language itself lacks a feature. The framework therefore performs:

```text
binding requirements
       |
       v
format release capabilities
       |
       v
format-compatible?
       |
       +---- no --> fail/warn
       |
       v
optional renderer selected?
       |
       +---- no --> stop; make no renderer claim
       |
       v
renderer compatibility contract
       |
       v
renderer effective capabilities
       |
       v
renderer-compatible?
```

## Resolution policy

A generation request always chooses the format. It may then specify either:

```yaml
representation:
  format: format.mermaid.class
  version: "11.4.1"
```

or a registered version constraint:

```yaml
representation:
  format: format.mermaid.class
  version_constraint: ">=11,<12"
```

If neither is supplied, the format registry may supply a **pinned default release**. A default is allowed only when an exact registered release exists.

A constraint is resolved only against registered releases. The resolver does not infer the existence or compatibility of versions that are absent from the registry. The resulting generation plan always records one exact format version.

## Renderer selection

Rendering is optional at the planning layer. When requested, renderer identity is chosen explicitly:

```yaml
representation:
  format: format.mermaid.class
  version: "11.4.1"
  renderer:
    id: renderer.mermaid-js
    version: "11.4.1"
```

If renderer version is omitted, only an exact registered default renderer release may be used. The framework does not auto-select a different renderer to make an incompatible request work.

## Strict versus warning mode

`compatibility_mode: strict` treats missing/incompatible format or renderer contracts as generation-plan errors.

`compatibility_mode: warn` keeps the selected format/renderer but records uncertainty or incompatibility as warnings. This is useful for exploratory work but must not be represented as verified compatibility.

## Capability compatibility

Version ranges alone are insufficient. Every binding declares the capabilities it requires. A format release declares the capabilities it actually exposes. Renderer compatibility contracts describe effective renderer capabilities.

Compatibility is therefore the intersection:

```text
Abstract model requirements
        +
Representation binding requirements
        +
Style binding requirements
        v
Required capabilities
        ∩
Chosen format release capabilities
        ∩
Chosen renderer effective capabilities (if renderer selected)
```

Any missing requirement must fail or degrade according to the requested compatibility mode and the binding's declared fallback/loss behaviour.

## Unknown and unpinned support

`unpinned` and `unverified` are valid states. They are preferable to fabricated compatibility.

For example, the current UML scaffold has no pinned normative UML specification release in the framework. Therefore `format.uml.class` has no fabricated version number or compatibility range. A future UML ingestion phase must pin a specification version, generate a format-release artifact, then validate bindings against it.

The same policy applies to renderer/tool versions.

## Provenance requirements

A generated artifact should record, when applicable:

- abstract model ID/version;
- chosen format ID;
- exact format release;
- representation binding ID/version;
- semantic overlays;
- style profile and style binding;
- renderer ID and exact renderer release;
- renderer-compatibility contract ID/version;
- transform ID/version;
- validator set and source evidence;
- deterministic source hash.

This turns a generated artifact into a reproducible execution record rather than merely a syntax file.

## Updating a format

When adding a new format release:

1. pin the source/specification evidence;
2. create a `format-version` artifact;
3. enumerate capabilities from evidence, not assumptions;
4. evaluate every representation binding whose format matches;
5. evaluate every style binding whose format matches;
6. add/update validator fixtures;
7. test relevant import/round-trip paths;
8. add renderer compatibility contracts only for tested renderer releases;
9. update the pinned default only after tests pass.

Do not broaden `==11.4.1` to `>=11` merely because a newer release appears likely compatible.

## Updating a renderer

When adding a renderer release:

1. register the exact renderer version;
2. identify the exact format release(s) it is expected to support;
3. test syntax acceptance and rendering independently where possible;
4. record supported/degraded/unsupported capabilities;
5. record known rendering issues;
6. create a renderer-compatibility contract for the tested pair/range;
7. add fixtures that exercise style as well as semantic structures;
8. only then make the renderer release a default.

## Current Mermaid reference

The current source-backed reference uses Mermaid package `11.4.1`, pinned to `majikmushi/mermaid` commit `446f6a7701065eb12e024475243434eb727dc172`.

This produces two distinct framework facts:

- Mermaid classDiagram format behaviour is pinned at `11.4.1`.
- Mermaid JS renderer behaviour is pinned at `11.4.1`.

Their current compatibility contract is exact-to-exact because that is the evidence scope. Future Mermaid versions should be added as additional releases/contracts, not by silently rewriting history.
