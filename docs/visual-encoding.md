# Visual Encoding, Semantic Overlays and Style

Visual channels are shared resources that may carry either semantic information or presentation choices. The framework keeps those uses separate.

## Semantic overlays

Overlays add meaning orthogonal to the abstract model, for example trust zone, lifecycle, voltage domain, ownership, criticality or deployment zone.

Typical semantic channels include:

- shape;
- fill/stroke colour;
- border pattern;
- connector pattern;
- arrow type/direction;
- icon;
- label/annotation;
- grouping/container;
- ordering.

Critical semantics must not depend on colour alone.

## Style profiles

Style profiles are format-neutral presentation intent, such as:

- palette/theme;
- typography;
- node borders/fills/corners;
- connector weight/pattern preferences;
- spacing/density;
- grouping appearance;
- layout intent.

Style must not redefine semantic meaning.

## Style bindings

A `style-binding.*` artifact translates presentation intent into mechanisms available in a chosen format. It also declares:

- supported format-version range;
- required format capabilities;
- fallbacks;
- accessibility behaviour.

Renderer compatibility is evaluated after format/style binding compatibility. A renderer may support fewer effective visual channels than the format release.

## Collision priority

1. preserve abstract-model semantics;
2. preserve semantic-overlay semantics;
3. preserve target-format validity;
4. apply style intent;
5. remap style channels where possible;
6. fall back to textual/structural semantic encoding;
7. report presentation loss rather than corrupt meaning.

## Example

```text
model.electronics-system
  + representation binding
  + voltage-domain overlay
  + safety-criticality overlay
  + style.technical-dark
  + format style binding
  -> concrete target styling
```

The first two overlays carry meaning. `style.technical-dark` changes presentation only.
