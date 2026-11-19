"""Построение графа зависимостей (итеративный DFS)."""

from typing import Callable, Dict, List, Set


def _is_filtered(name: str, sub: str) -> bool:
    """Проверяет необходимость фильтрации пакета."""
    return bool(sub and sub in name)


def _get_deps(
    node: str,
    fetcher: Callable[[str], List[str]],
    sub: str,
) -> List[str]:
    """Безопасно получает и фильтрует зависимости узла."""
    try:
        raw = fetcher(node)
    except Exception:
        raw = []
    return [d for d in raw if not _is_filtered(d, sub)]


def build_graph(
    root: str,
    fetcher: Callable[[str], List[str]],
    filter_sub: str = "",
) -> Dict[str, List[str]]:
    """Строит граф зависимостей итеративным DFS."""
    graph: Dict[str, List[str]] = {}
    stack: List[str] = [root]
    visited: Set[str] = set()

    while stack:
        node = stack.pop()
        if node in visited:
            continue

        visited.add(node)

        if _is_filtered(node, filter_sub):
            graph[node] = []
            continue

        deps = _get_deps(node, fetcher, filter_sub)
        graph[node] = deps

        for dep in deps:
            if dep not in visited:
                stack.append(dep)

    return graph


def load_test_graph(path: str) -> Dict[str, List[str]]:
    """Загружает тестовый граф из текстового файла."""
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
