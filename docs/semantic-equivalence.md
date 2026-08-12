# Semantic Equivalence

Text equality is not representation equality. Two artifacts may differ in syntax, ordering, layout, colour, tool metadata or diagram primitives while carrying the same domain meaning.

Equivalence is evaluated against canonical semantics and declared profile mappings.

Levels: `exact`, `equivalent`, `projection`, `approximate`, `non-equivalent`.

Round-trip safety is a tested property backed by fixtures, not a label inferred from successful parsing.
