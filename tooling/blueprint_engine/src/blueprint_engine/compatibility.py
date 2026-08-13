from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def version_matches(version: str, specifier: str | None) -> bool:
    if not specifier:
        return True
    try:
        return Version(version) in SpecifierSet(specifier)
    except (InvalidVersion, InvalidSpecifier) as exc:
        raise ValueError(f"Cannot evaluate version {version!r} against {specifier!r}") from exc


def resolve_format_release(
    root: str | Path,
    format_id: str,
    *,
    version: str | None = None,
    version_constraint: str | None = None,
) -> dict[str, Any]:
    if version and version_constraint:
        raise ValueError("Specify either an exact format version or a version constraint, not both")
    root = Path(root)
    registry = _load_yaml(root / "format-versions/registry.yaml")
    entry = next((item for item in registry.get("formats", []) if item.get("format") == format_id), None)
    if entry is None:
        return {"status": "unregistered", "format": format_id, "version": None, "artifact": None}

    releases = list(entry.get("releases") or [])
    if not releases:
        return {"status": "unpinned", "format": format_id, "version": None, "artifact": None, "version_scheme": entry.get("version_scheme")}

    selected: dict[str, Any] | None = None
    if version:
        selected = next((release for release in releases if str(release.get("version")) == version), None)
        if selected is None:
            raise KeyError(f"Format {format_id!r} has no registered release {version!r}")
    elif version_constraint:
        if entry.get("version_scheme") != "pep440":
            raise ValueError(f"Format {format_id!r} does not support ordered version constraints")
        candidates = [release for release in releases if version_matches(str(release["version"]), version_constraint)]
        if not candidates:
            raise KeyError(f"No registered {format_id!r} release satisfies {version_constraint!r}")
        selected = max(candidates, key=lambda release: Version(str(release["version"])))
    else:
        default_id = entry.get("default_release")
        selected = next((release for release in releases if release.get("id") == default_id), None)
        if selected is None:
            raise ValueError(f"Format {format_id!r} has releases but no valid pinned default")

    artifact = _load_yaml(root / selected["path"])
    return {
        "status": "resolved",
        "format": format_id,
        "version": str(selected["version"]),
        "version_scheme": entry.get("version_scheme"),
        "release_id": selected["id"],
        "artifact": artifact,
    }


def load_renderer(root: str | Path, renderer_id: str) -> dict[str, Any]:
    root = Path(root)
    registry = _load_yaml(root / "renderers/registry.yaml")
    entry = next((item for item in registry.get("renderers", []) if item.get("id") == renderer_id), None)
    if entry is None:
        raise KeyError(f"Unknown renderer {renderer_id!r}")
    renderer = _load_yaml(root / entry["path"])
    renderer["_registry_default_release"] = entry.get("default_release")
    return renderer


def resolve_renderer_release(root: str | Path, renderer_id: str, *, version: str | None = None) -> dict[str, Any]:
    renderer = load_renderer(root, renderer_id)
    releases = list(renderer.get("releases") or [])
    selected_version = version or renderer.pop("_registry_default_release", None)
    if not selected_version:
        return {"status": "unpinned", "renderer": renderer_id, "version": None, "artifact": renderer}
    release = next((item for item in releases if str(item.get("version")) == str(selected_version)), None)
    if release is None:
        raise KeyError(f"Renderer {renderer_id!r} has no registered release {selected_version!r}")
    return {"status": "resolved", "renderer": renderer_id, "version": str(selected_version), "release": release, "artifact": renderer}


def resolve_renderer_compatibility(
    root: str | Path,
    *,
    renderer_id: str,
    renderer_version: str,
    format_id: str,
    format_version: str,
) -> dict[str, Any] | None:
    root = Path(root)
    registry = _load_yaml(root / "renderer-compatibility/registry.yaml")
    for entry in registry.get("contracts", []):
        if entry.get("renderer") != renderer_id or entry.get("format") != format_id:
            continue
        contract = _load_yaml(root / entry["path"])
        if version_matches(renderer_version, contract.get("renderer_versions")) and version_matches(format_version, contract.get("format_versions")):
            return contract
    return None


def missing_capabilities(required: list[str] | tuple[str, ...], available: list[str] | tuple[str, ...] | set[str]) -> list[str]:
    available_set = set(available)
    return sorted(set(required) - available_set)
