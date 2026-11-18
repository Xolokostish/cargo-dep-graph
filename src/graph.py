"""Построение графа зависимостей (итеративный DFS)."""

from typing import Callable, Dict, List, Set


def build_graph(
    root: str,
    fetcher: Callable[[str], List[str]],
    filter_sub: str = "",
) -> Dict[str, List[str]]:
    """Строит граф зависимостей через итеративный DFS."""
    graph: Dict[str, List[str]] = {}
    stack: List[str] = [root]
    visited: Set[str] = set()
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if filter_sub and filter_sub in node:
            graph[node] = []
            continue
        try:
            deps = fetcher(node)
        except Exception:
            deps = []
        filtered = [
            d for d in deps
            if not (filter_sub and filter_sub in d)
        ]
        graph[node] = filtered
        for dep in filtered:
            if dep not in visited:
                stack.append(dep)
    return graph


def load_test_graph(path: str) -> Dict[str, List[str]]:
    """Загружает тестовый граф из файла."""
    graph: Dict[str, List[str]] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" not in line:
                continue
            src, dsts = line.split("->", 1)
            src = src.strip()
            deps = [
                d.strip()
                for d in dsts.split(",")
                if d.strip()
            ]
            graph[src] = deps
    return graph
