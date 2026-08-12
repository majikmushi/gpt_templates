from __future__ import annotations
from pathlib import Path
from typing import Any
from .io import load_data

MANIFEST_SUFFIXES = {".yaml", ".yml", ".json"}

def scan_artifacts(root: str | Path) -> list[dict[str, Any]]:
    root = Path(root)
    out: list[dict[str, Any]] = []
    skip_parts = {".git", ".venv", "node_modules", "__pycache__"}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in MANIFEST_SUFFIXES:
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        try:
            data = load_data(path)
        except Exception:
            continue
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            out.append({
                "id": data["id"],
                "kind": data.get("kind", "unspecified"),
                "version": data.get("version"),
                "status": data.get("status"),
                "path": path.relative_to(root).as_posix(),
                "title": data.get("title"),
            })
    return out

def index_by_id(artifacts: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {a["id"]: a for a in artifacts}
