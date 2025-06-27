# Summary Template ✦ (with Built-In Guidelines)
> Copy everything inside this fenced block when you prepare a **full-design summary**.  
> **Delete everything above `## What This Design/Feature Does`** before sharing with reviewers.

---

## ✦ Author Guidelines  *(remove this section before publishing)*

| # | Guideline |
|---|-----------|
| **1** | The summary **must be valid Markdown** from top to bottom. |
| **2** | **Always wrap** configuration, schemas, command snippets, and **diagrams** inside triple-back-tick **code fences** → ` ```yaml `, ` ```json `, ` ```mermaid `, etc. |
| **3** | Keep the section headings in this template **exactly as written**. Add sub-headings only inside these sections. |
| **4** | Prefer tables only when they remain < 80 characters wide; otherwise use bullet lists. |
| **5** | Diagrams (preferably Mermaid) should clarify structure, data-flow, or lifecycle and **must** be in fenced blocks. |
| **6** | Do **not** embed large source code files—only minimal config or pseudocode. |
| **7** | Mask secrets with placeholders like `${SECRET}`—no real credentials anywhere. |
| **8** | If the design introduces RBAC/sudo/tokens, include a **Security / Access Controls** subsection. |
| **9** | End with **Implementation Notes** only if extra developer guidance is necessary. |
| **10** | The summary must be self-contained: reviewers need no prior chat context to understand scope, architecture, and samples. |

---

## What This Design/Feature Does (one-liner)

## Example Use-Case for Context

## Conversation Changelog
| # | When (relative) | Topic / Decision | Key Outcome |
|---|-----------------|------------------|-------------|
| … | … | … | … |

## Core Design Summary
1. **Purpose** – short paragraph.
2. **High-Level Architecture**
   - *Component A* – role  
   - *Component B* – role  
3. **Key Responsibilities & Data-flow**
   - Bullet list *or* small table mapping components → APIs / queues / locks.
4. **Threading / Concurrency Model**  *(or “Execution Model” if not threaded)*
5. **Security / Access Controls**  *(omit if not applicable)*

## Config Layout
*(Primary operator-edited configuration first; secondary or library file next if relevant.)*

**Primary configuration example**
```yaml
# YAML goes here
```

**Secondary configuration example (if applicable)**
```yaml
# YAML goes here
```

## Diagrams
```mermaid
%% Put a component or flow diagram here
```

## Implementation Notes  *(optional)*
- First note …  
- Second note …
