from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import Any

import yaml


def git_blob_sha(data: bytes) -> str:
    """Return the Git object ID for blob bytes without requiring a repository."""
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def _load_manifest(value: str | Path | dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return yaml.safe_load(Path(value).read_text(encoding="utf-8"))


def check_git_source(
    source_root: str | Path,
    provenance: str | Path | dict[str, Any],
) -> dict[str, Any]:
    """Verify a local Git-backed specification source against pinned evidence.

    The manifest shape intentionally matches existing Mermaid provenance files:
    `source.commit` pins the repository revision and `files[*].sha` pins Git blob IDs.
    Other language integrations can use the same contract without Mermaid-specific code.
    """

    root = Path(source_root).resolve()
    manifest = _load_manifest(provenance)
    source = manifest.get("source") or {}
    expected_commit = source.get("commit")

    try:
        actual_commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        actual_commit = None

    files: list[dict[str, Any]] = []
    for entry in manifest.get("files", []):
        path = root / entry["path"]
        actual_sha = git_blob_sha(path.read_bytes()) if path.is_file() else None
        expected_sha = entry.get("sha")
        files.append(
            {
                "path": entry["path"],
                "role": entry.get("role"),
                "expected_sha": expected_sha,
                "actual_sha": actual_sha,
                "ok": actual_sha == expected_sha,
            }
        )

    commit_matches = expected_commit is None or actual_commit == expected_commit
    files_match = all(item["ok"] for item in files)
    return {
        "source": source,
        "expected_commit": expected_commit,
        "actual_commit": actual_commit,
        "commit_matches": commit_matches,
        "files": files,
        "files_match": files_match,
        "ok": commit_matches and files_match,
    }
