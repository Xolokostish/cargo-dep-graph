"""Топологическая сортировка графа зависимостей."""

from typing import Dict, List


def topological_sort(
    graph: Dict[str, List[str]],
    root: str,
) -> List[str]:
    """Возвращает порядок загрузки зависимостей.

    graph[node] = список зависимостей node.
    Если A -> B, значит A зависит от B,
    и B должен быть загружен раньше A.
    """
    in_degree: Dict[str, int] = {
        n: len(deps) for n, deps in graph.items()
    }

    reverse_graph: Dict[str, List[str]] = {
        n: [] for n in graph
    }
    for node, deps in graph.items():
        for dep in deps:
            if dep in reverse_graph:
                reverse_graph[dep].append(node)

    queue = [
        n for n in in_degree if in_degree[n] == 0
    ]
    result: List[str] = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        for dependent in reverse_graph.get(node, []):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    return result
