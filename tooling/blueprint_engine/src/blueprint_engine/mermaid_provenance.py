from __future__ import annotations

from pathlib import Path
from typing import Any

from .source_provenance import check_git_source, git_blob_sha


def check_mermaid_source(
    mermaid_root: str | Path,
    provenance_file: str | Path,
) -> dict[str, Any]:
    """Backward-compatible wrapper around the generic Git source checker."""
    return check_git_source(mermaid_root, provenance_file)


__all__ = ["check_mermaid_source", "check_git_source", "git_blob_sha"]
