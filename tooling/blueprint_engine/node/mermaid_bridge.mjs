#!/usr/bin/env node
import fs from 'node:fs';

const readStdin = () => fs.readFileSync(0, 'utf8');

function toPlain(value) {
  if (value instanceof Map) {
    return Object.fromEntries([...value.entries()].map(([k, v]) => [k, toPlain(v)]));
  }
  if (value instanceof Set) {
    return [...value.values()].map(toPlain);
  }
  if (Array.isArray(value)) {
    return value.map(toPlain);
  }
  if (value && typeof value === 'object') {
    const out = {};
    for (const [key, child] of Object.entries(value)) {
      if (typeof child !== 'function' && key !== 'functions') {
        out[key] = toPlain(child);
      }
    }
    return out;
  }
  return value;
}

function classAst(diagram) {
  const db = diagram.db;
  const classes = typeof db.getClasses === 'function'
    ? [...db.getClasses().values()].map((c) => ({
        id: c.id,
        type: c.type ?? '',
        label: c.label ?? c.id,
        text: c.text ?? '',
        members: (c.members ?? []).map(toPlain),
        methods: (c.methods ?? []).map(toPlain),
        annotations: [...(c.annotations ?? [])],
        cssClasses: c.cssClasses ?? '',
        styles: [...(c.styles ?? [])],
        parent: c.parent ?? null,
        link: c.link ?? null,
        linkTarget: c.linkTarget ?? null,
        tooltip: c.tooltip ?? null,
      }))
    : [];

  const namespaces = typeof db.getNamespaces === 'function'
    ? [...db.getNamespaces().values()].map((ns) => ({
        id: ns.id,
        classIds: ns.classes instanceof Map ? [...ns.classes.keys()] : [],
        childIds: ns.children instanceof Map ? [...ns.children.keys()] : Object.keys(ns.children ?? {}),
      }))
    : [];

  const renderData = typeof db.getData === 'function' ? db.getData() : null;
  const classIds = new Set(classes.map((c) => c.id));
  const interfaces = (renderData?.nodes ?? [])
    .filter((node) => String(node.id).startsWith('interface') && !classIds.has(node.id))
    .map((node) => ({ id: node.id, label: node.label ?? node.id }));

  return {
    kind: 'mermaid-class-ast',
    diagramType: diagram.type,
    direction: typeof db.getDirection === 'function' ? db.getDirection() : null,
    classes,
    interfaces,
    relations: typeof db.getRelations === 'function' ? toPlain(db.getRelations()) : [],
    namespaces,
    notes: typeof db.getNotes === 'function' ? toPlain(db.getNotes()) : [],
    accessibility: {
      title: typeof db.getAccTitle === 'function' ? db.getAccTitle() : null,
      description: typeof db.getAccDescription === 'function' ? db.getAccDescription() : null,
      diagramTitle: typeof db.getDiagramTitle === 'function' ? db.getDiagramTitle() : null,
    },
  };
}

function serializeError(error) {
  if (!error) return { message: 'Unknown Mermaid error' };
  return {
    name: error.name ?? null,
    message: error.message ?? String(error),
    str: error.str ?? null,
    hash: toPlain(error.hash ?? null),
    stack: error.stack ?? null,
  };
}

let input;
try {
  input = JSON.parse(readStdin());
} catch (error) {
  process.stdout.write(JSON.stringify({
    ok: false,
    mode: 'bootstrap',
    error: { code: 'invalid-input', ...serializeError(error) },
  }));
  process.exit(2);
}

let mermaid;
try {
  ({ default: mermaid } = await import('mermaid'));
} catch (error) {
  process.stdout.write(JSON.stringify({
    ok: false,
    mode: input.mode ?? 'unknown',
    error: {
      code: 'runtime-unavailable',
      message: 'The Mermaid Node package could not be imported. Run npm install in tooling/blueprint_engine/node.',
      detail: serializeError(error),
    },
  }));
  process.exit(3);
}

try {
  mermaid.initialize({ startOnLoad: false, securityLevel: 'strict' });
  const parsed = await mermaid.parse(input.text);
  if (input.mode === 'validate') {
    process.stdout.write(JSON.stringify({
      ok: true,
      mode: 'validate',
      diagramType: parsed.diagramType,
      runtime: { package: 'mermaid' },
    }));
  } else if (input.mode === 'ast') {
    const diagram = await mermaid.mermaidAPI.getDiagramFromText(input.text);
    const ast = String(diagram.type).startsWith('classDiagram')
      ? classAst(diagram)
      : {
          kind: 'mermaid-generic-ast',
          diagramType: diagram.type,
          data: typeof diagram.db?.getData === 'function' ? toPlain(diagram.db.getData()) : null,
        };
    process.stdout.write(JSON.stringify({
      ok: true,
      mode: 'ast',
      diagramType: diagram.type,
      ast,
      runtime: { package: 'mermaid' },
    }));
  } else {
    throw new Error(`Unsupported mode: ${input.mode}`);
  }
} catch (error) {
  process.stdout.write(JSON.stringify({
    ok: false,
    mode: input.mode ?? 'unknown',
    error: { code: 'mermaid-parse', ...serializeError(error) },
    runtime: { package: 'mermaid' },
  }));
  process.exit(2);
}
