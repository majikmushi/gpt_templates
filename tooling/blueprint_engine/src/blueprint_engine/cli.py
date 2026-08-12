from __future__ import annotations
import argparse
import json
from pathlib import Path
from .engine import BlueprintEngine
from .io import dump_data, load_data
from .validators import validate_target

FORMAT_EXT = {
    "format.mermaid.class": "mmd",
    "format.plantuml": "puml",
    "format.uml.class": "json",
    "format.json-schema": "json",
    "format.xml": "xml",
    "format.markdown": "md",
}

def _repo(args: argparse.Namespace) -> Path:
    return Path(args.repo).resolve()

def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="blueprint-engine")
    p.add_argument("--repo", default=".", help="Repository root")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("catalog")

    m = sub.add_parser("match")
    m.add_argument("capabilities", nargs="+")
    m.add_argument("--allow-partial", action="store_true")

    r = sub.add_parser("route")
    r.add_argument("source")
    r.add_argument("target")

    t = sub.add_parser("transform")
    t.add_argument("source")
    t.add_argument("target_format", choices=sorted(FORMAT_EXT))
    t.add_argument("-o", "--output")
    t.add_argument("--profile")
    t.add_argument("--overlay", action="append", default=[])
    t.add_argument("--no-validate", action="store_true")

    v = sub.add_parser("validate")
    v.add_argument("target_format", choices=["canonical.core", *sorted(FORMAT_EXT)])
    v.add_argument("path")

    c = sub.add_parser("compare")
    c.add_argument("left")
    c.add_argument("right")

    rt = sub.add_parser("roundtrip")
    rt.add_argument("source")
    rt.add_argument("target_format", choices=["format.xml", "format.uml.class"])

    args = p.parse_args(argv)
    engine = BlueprintEngine(_repo(args))

    if args.command == "catalog":
        _print(engine.catalog())
        return 0
    if args.command == "match":
        _print([m.__dict__ for m in engine.match(args.capabilities, allow_partial=args.allow_partial)])
        return 0
    if args.command == "route":
        _print(engine.route(args.source, args.target))
        return 0
    if args.command == "transform":
        model = load_data(args.source)
        result, validation = engine.transform(
            model, args.target_format, profile_id=args.profile, overlays=args.overlay,
            validate=not args.no_validate,
        )
        content = result.content
        fmt = "json" if isinstance(content, (dict, list)) else "text"
        text = dump_data(content, fmt)
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        meta = {
            "transform_id": result.transform_id,
            "target_format": result.target_format,
            "fidelity": result.fidelity,
            "losses": result.losses,
            "provenance": result.provenance,
            "validation": validation.as_dict() if validation else None,
        }
        print(json.dumps(meta, indent=2), file=__import__("sys").stderr)
        return 0 if validation is None or validation.ok else 2
    if args.command == "validate":
        value = load_data(args.path)
        if args.target_format == "canonical.core":
            result = engine.validate_canonical(value)
        else:
            result = validate_target(args.target_format, value)
        _print(result.as_dict())
        return 0 if result.ok else 2
    if args.command == "compare":
        result = engine.compare(load_data(args.left), load_data(args.right))
        _print(result.__dict__)
        return 0 if result.equivalent else 3
    if args.command == "roundtrip":
        model = load_data(args.source)
        result = engine.roundtrip_xml(model) if args.target_format == "format.xml" else engine.roundtrip_uml_class(model)
        _print(result.__dict__)
        return 0 if result.equivalent else 3
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
