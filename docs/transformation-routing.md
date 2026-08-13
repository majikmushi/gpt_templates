# Transformation Routing

Transforms form a directed graph. Route selection considers semantic capabilities, representation-binding compatibility, exact target-format release compatibility, fidelity/loss declarations, reversibility, validator availability and deterministic/tooling requirements.

Preferred routes minimize semantic loss, not hop count.

A route identifies possible conversions. Version-aware generation planning is still required before execution: each selected format node must resolve to an exact registered release where compatibility is claimed, and any chosen renderer must have a compatible renderer-format contract.

## Declarative transform analogy

XSLT remains both an actual XML transform engine and an architectural reference: declarative matching, selection, construction, parameters and composition. Repository transforms generalize that idea by operating against canonical semantics and resolved representation bindings.
