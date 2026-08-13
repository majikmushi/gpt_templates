# Mermaid Source-Derived Validation and AST Integration

## Reference source

The current integration is derived from `majikmushi/mermaid`:

- branch: `develop`
- commit: `446f6a7701065eb12e024475243434eb727dc172`
- package version: `11.4.1`

Exact evidence paths and Git blob SHAs are recorded in `validators/mermaid/source-provenance.yaml`.

## Authority

Mermaid runtime parsing is the authoritative syntax path for the pinned runtime release. Static Python checks are source-derived preflight only.

```text
Mermaid source
    -> mermaid.parse()
    -> parser result
    -> mermaidAPI.getDiagramFromText()
    -> diagram DB
    -> normalized AST
    -> optional representation binding
    -> canonical semantic model
```

For classDiagram the AST adapter handles classes, members, methods, annotations, namespaces, relations, notes, direction, links, styles and accessibility metadata.

## Version scope

The source evidence creates an exact registered format release: `format-version.mermaid.class.11.4.1`.

Validation of this release does not imply that an arbitrary older/newer Mermaid version behaves identically. New versions require new evidence/release records and regression checks.

## Renderer scope

Parser/runtime validation and rendering compatibility are independent framework claims. `renderer.mermaid-js` release `11.4.1` currently has an exact compatibility contract with Mermaid classDiagram `11.4.1`. Other renderers or versions require separate contracts.

## Source verification

Use the generic provenance checker:

```bash
blueprint-engine --repo . source-check validators/mermaid/source-provenance.yaml /path/to/mermaid
```

It verifies the pinned source commit and each evidence file's Git blob hash.

## Extending another Mermaid family/release

1. pin parser/grammar/DB/detector/test evidence;
2. update or create its normalized language definition;
3. create an exact `format-version` artifact;
4. enumerate release capabilities from evidence;
5. add/update representation and style bindings with explicit version ranges;
6. use the shared native runtime for syntax validation;
7. add a diagram-specific semantic AST adapter where needed;
8. add renderer compatibility contracts only for tested renderer/release combinations;
9. establish semantic round-trip claims through comparison tests.
