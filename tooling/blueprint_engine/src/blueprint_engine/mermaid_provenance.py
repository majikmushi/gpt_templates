from __future__ import annotations
import hashlib
import subprocess
from pathlib import Path
from typing import Any
import yaml

def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()

def check_mermaid_source(mermaid_root: str | Path, provenance_file: str | Path) -> dict[str, Any]:
    root = Path(mermaid_root).resolve()
    provenance = yaml.safe_load(Path(provenance_file).read_text(encoding="utf-8"))
    expected_commit = provenance["source"]["commit"]
    try:
        actual_commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        actual_commit = None

    files = []
    for entry in provenance.get("files", []):
        path = root / entry["path"]
        actual_sha = git_blob_sha(path.read_bytes()) if path.is_file() else None
        files.append({
            "path": entry["path"],
            "expected_sha": entry["sha"],
            "actual_sha": actual_sha,
            "ok": actual_sha == entry["sha"],
        })
    return {
        "expected_commit": expected_commit,
        "actual_commit": actual_commit,
        "commit_matches": actual_commit == expected_commit,
        "files": files,
        "ok": all(item["ok"] for item in files),
    }
