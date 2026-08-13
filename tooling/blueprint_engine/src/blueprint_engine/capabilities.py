from __future__ import annotations
from pathlib import Path
from .io import load_data
from .models import MatchResult

LEVEL_SCORE = {"native": 1.0, "bound": 0.8, "partial": 0.35, "none": 0.0, "native-runtime": 1.0}


def match_formats(
    matrix_path: str | Path,
    required: list[str],
    *,
    allow_partial: bool = False,
) -> list[MatchResult]:
    matrix = load_data(matrix_path)
    formats = matrix.get("formats", {})
    matches: list[MatchResult] = []
    for format_id, caps in formats.items():
        levels: dict[str, str] = {}
        partial: list[str] = []
        rejected = False
        score = 0.0
        for cap in required:
            level = caps.get(cap, "none")
            levels[cap] = level
            if level == "none":
                rejected = True
                break
            if level == "partial":
                partial.append(cap)
                if not allow_partial:
                    rejected = True
                    break
            score += LEVEL_SCORE.get(level, 0.0)
        if rejected:
            continue
        denom = max(len(required), 1)
        matches.append(MatchResult(format_id, score / denom, levels, tuple(partial)))
    return sorted(matches, key=lambda m: (-m.score, m.format_id))
