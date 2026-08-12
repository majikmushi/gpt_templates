# Mermaid runtime bridge

This optional Node bridge delegates syntax validation and AST extraction to Mermaid itself.

The dependency is pinned to Mermaid `11.4.1`, matching the analysed `majikmushi/mermaid`
`develop` commit `446f6a7701065eb12e024475243434eb727dc172`.

## Install

```bash
cd tooling/blueprint_engine/node
npm install
```

## Use

```bash
blueprint-engine --repo . validate format.mermaid.class diagram.mmd --require-runtime
blueprint-engine --repo . mermaid-ast diagram.mmd
blueprint-engine --repo . mermaid-import diagram.mmd -o canonical.yaml
```

Without the Node runtime/package, validation degrades explicitly to source-derived static
preflight and emits a warning. `--require-runtime` makes that condition an error.

The bridge intentionally calls Mermaid's own `parse()` and `mermaidAPI.getDiagramFromText()`;
it does not carry a second parser implementation.
