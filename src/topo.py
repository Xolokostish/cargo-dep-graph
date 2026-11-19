"""Топологическая сортировка графа зависимостей."""

from typing import Dict, List


def _build_reverse_graph(
    graph: Dict[str, List[str]]
) -> Dict[str, List[str]]:
    """Строит обратный граф для алгоритма Кана.

    Args:
        graph: Исходный граф зависимостей.

    Returns:
        Обратный граф {узел: [зависящие_узлы]}.
    """
    reverse: Dict[str, List[str]] = {n: [] for n in graph}
    for node, deps in graph.items():
        for dep in deps:
            if dep in reverse:
                reverse[dep].append(node)
    return reverse


def topological_sort(
    graph: Dict[str, List[str]],
    root: str,
) -> List[str]:
    """Возвращает порядок загрузки зависимостей (топосорт).

    Использует алгоритм Кана. Сначала загружаются пакеты
    без зависимостей (листья графа).

    Args:
        graph: Словарь {пакет: [зависимости]}.
        root: Корневой пакет (для контекста).

    Returns:
        Список пакетов в порядке загрузки.
    """
    # Считаем входящие степени (количество зависимостей)
    in_degree: Dict[str, int] = {
        n: len(deps) for n, deps in graph.items()
    }

    # Строим обратный граф для обновления степеней
    reverse_graph = _build_reverse_graph(graph)

    # Инициализация очереди (узлы без зависимостей)
    queue = [
        n for n in in_degree if in_degree[n] == 0
    ]
    result: List[str] = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        
        # Обновляем степени соседей в обратном графе
        for dependent in reverse_graph.get(node, []):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    return result
