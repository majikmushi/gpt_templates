from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class MermaidRuntimeUnavailable(RuntimeError):
    """Raised when the optional Mermaid Node runtime cannot be executed."""


class MermaidRuntimeError(RuntimeError):
    """Raised when the Mermaid runtime reports a parser/adapter failure."""


@dataclass(frozen=True)
class MermaidRuntimeResult:
    ok: bool
    mode: str
    diagram_type: str | None = None
    ast: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    runtime: dict[str, Any] | None = None


class MermaidRuntimeBridge:
    """Invoke Mermaid's own parser through the repository Node bridge.

    The bridge deliberately delegates syntax acceptance to Mermaid itself.
    Python-side rules are only preflight/lint checks and must not be treated
    as a replacement for the Mermaid parser.
    """

    def __init__(
        self,
        repository_root: str | Path,
        *,
        node_binary: str = "node",
        timeout_seconds: float = 15.0,
    ) -> None:
        self.repository_root = Path(repository_root)
        self.node_binary = node_binary
        self.timeout_seconds = timeout_seconds
        self.bridge_path = (
            self.repository_root
            / "tooling"
            / "blueprint_engine"
            / "node"
            / "mermaid_bridge.mjs"
        )

    def available(self) -> bool:
        return self.bridge_path.is_file() and shutil.which(self.node_binary) is not None

    def invoke(self, mode: str, text: str) -> MermaidRuntimeResult:
        if mode not in {"validate", "ast"}:
            raise ValueError(f"Unsupported Mermaid bridge mode: {mode!r}")
        if not self.bridge_path.is_file():
            raise MermaidRuntimeUnavailable(f"Mermaid bridge not found: {self.bridge_path}")
        if shutil.which(self.node_binary) is None:
            raise MermaidRuntimeUnavailable(f"Node executable not found: {self.node_binary}")

        payload = json.dumps({"mode": mode, "text": text})
        try:
            proc = subprocess.run(
                [self.node_binary, str(self.bridge_path)],
                input=payload,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise MermaidRuntimeError(
                f"Mermaid runtime timed out after {self.timeout_seconds:g}s"
            ) from exc

        stdout = proc.stdout.strip()
        if not stdout:
            detail = proc.stderr.strip() or f"exit code {proc.returncode}"
            raise MermaidRuntimeError(f"Mermaid runtime returned no JSON: {detail}")

        try:
            value = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise MermaidRuntimeError(
                f"Mermaid runtime returned invalid JSON: {stdout[:500]}"
            ) from exc

        result = MermaidRuntimeResult(
            ok=bool(value.get("ok")),
            mode=str(value.get("mode", mode)),
            diagram_type=value.get("diagramType"),
            ast=value.get("ast"),
            error=value.get("error"),
            runtime=value.get("runtime"),
        )
        return result

    def validate(self, text: str) -> MermaidRuntimeResult:
        return self.invoke("validate", text)

    def ast(self, text: str) -> MermaidRuntimeResult:
        return self.invoke("ast", text)
