from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import yaml

def load_data(path: str | Path) -> Any:
    path = Path(path)
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    if suffix == ".json":
        return json.loads(text)
    return text

def dump_data(value: Any, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(value, indent=2, sort_keys=True) + "\n"
    if fmt == "yaml":
        return yaml.safe_dump(value, sort_keys=False, allow_unicode=True)
    if not isinstance(value, str):
        raise TypeError(f"Cannot dump non-string value as {fmt}")
    return value
