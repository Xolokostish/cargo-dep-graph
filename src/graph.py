"""Построение графа зависимостей (итеративный DFS)."""

from typing import Callable, Dict, List, Set


def _is_filtered(name: str, filter_sub: str) -> bool:
    """Проверяет, нужно ли фильтровать пакет по подстроке.

    Args:
        name: Имя пакета.
        filter_sub: Подстрока для фильтрации.

    Returns:
        True, если пакет должен быть исключен.
    """
    return bool(filter_sub and filter_sub in name)


def build_graph(
    root: str,
    fetcher: Callable[[str], List[str]],
    filter_sub: str = "",
) -> Dict[str, List[str]]:
    """Строит граф зависимостей через итеративный DFS.

    Args:
        root: Корневой пакет.
        fetcher: Функция получения зависимостей.
        filter_sub: Подстрока для фильтрации.

    Returns:
        Словарь {пакет: [зависимости]}.
    """
    graph: Dict[str, List[str]] = {}
    stack: List[str] = [root]
    visited: Set[str] = set()

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        
        visited.add(node)

        # Обработка фильтрации корневого узла
        if _is_filtered(node, filter_sub):
            graph[node] = []
            continue

        # Получение и фильтрация зависимостей
        try:
            deps = fetcher(node)
        except Exception:
            deps = []

        filtered_deps = [
            d for d in deps 
            if not _is_filtered(d, filter_sub)
        ]
        
        graph[node] = filtered_deps

        for dep in filtered_deps:
            if dep not in visited:
                stack.append(dep)

    return graph


def load_test_graph(path: str) -> Dict[str, List[str]]:
    """Загружает тестовый граф из текстового файла.

    Args:
        path: Путь к файлу с описанием графа.

    Returns:
        Словарь графа зависимостей.
    """
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
