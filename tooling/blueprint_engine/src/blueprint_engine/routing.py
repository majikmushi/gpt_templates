from __future__ import annotations
import heapq
from pathlib import Path
from typing import Any
from .io import load_data

FIDELITY_COST = {
    "lossless": 0.0,
    "lossless-for-structural-subset": 0.2,
    "lossless-for-schema-subset": 0.2,
    "high": 0.4,
    "profile-dependent": 0.8,
    "partial": 1.5,
    "projection": 2.0,
    "presentation-only": 3.0,
    "stylesheet-defined": 1.0,
}

def _edge_cost(edge: dict[str, Any]) -> float:
    cost = FIDELITY_COST.get(str(edge.get("fidelity")), 1.2)
    reversible = edge.get("reversible")
    if reversible is False:
        cost += 1.0
    elif reversible == "conditional":
        cost += 0.15
    return cost

def find_route(graph_path: str | Path, source: str, target: str) -> list[dict[str, Any]]:
    graph = load_data(graph_path)
    edges = graph.get("edges", [])
    adjacency: dict[str, list[dict[str, Any]]] = {}
    for edge in edges:
        adjacency.setdefault(edge["from"], []).append(edge)

    queue: list[tuple[float, int, str, list[dict[str, Any]]]] = [(0.0, 0, source, [])]
    best: dict[str, float] = {source: 0.0}
    serial = 1
    while queue:
        cost, _, node, path = heapq.heappop(queue)
        if node == target:
            return path
        if cost > best.get(node, float("inf")):
            continue
        for edge in adjacency.get(node, []):
            new_cost = cost + _edge_cost(edge)
            nxt = edge["to"]
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(queue, (new_cost, serial, nxt, path + [edge]))
                serial += 1
    raise ValueError(f"No conversion route from {source!r} to {target!r}")
