"""Главный модуль CLI-приложения."""

import sys
from typing import Dict

from src.config import load_config
from src.errors import ConfigError
from src.fetcher import get_direct_deps
from src.graph import build_graph, load_test_graph
from src.topo import topological_sort
from src.visualizer import graph_to_dot, render_png

DEFAULT_CONFIG = "config.csv"


def print_config(cfg: Dict[str, str]) -> None:
    """Выводит параметры в формате ключ-значение."""
    print("=== Конфигурация ===")
    for key, value in cfg.items():
        print(f"{key} = {value}")
    print("====================")


def run_stage2(cfg: Dict[str, str]) -> None:
    """Этап 2: вывод прямых зависимостей."""
    pkg = cfg["package_name"]
    mode = cfg["test_mode"]
    print(f"\n[Этап 2] Прямые зависимости {pkg}:")
    if mode == "on":
        graph = load_test_graph(cfg["source"])
        deps = graph.get(pkg, [])
        if not deps:
            first_node = next(iter(graph), None)
            if first_node:
                deps = graph.get(first_node, [])
                print(f"  (тестовый режим, пакет '{pkg}' "
                      f"не найден, показан '{first_node}')")
        for d in deps:
            print(f"  - {d}")
    else:
        try:
            deps = get_direct_deps(pkg)
            for d in deps:
                print(f"  - {d}")
        except Exception as e:
            print(f"  Ошибка: {e}")

def run_stage3(cfg: Dict[str, str]) -> Dict:
    """Этап 3: построение графа DFS."""
    pkg = cfg["package_name"]
    mode = cfg["test_mode"]
    filt = cfg["filter_substring"]
    print(f"\n[Этап 3] Граф зависимостей {pkg}:")
    if mode == "on":
        graph = load_test_graph(cfg["source"])
    else:
        graph = build_graph(pkg, get_direct_deps, filt)
    for node in graph:
        deps = graph[node]
        print(f"  {node} -> {', '.join(deps) or '(нет)'}")
    return graph


def run_stage4(cfg: Dict[str, str], graph: Dict) -> None:
    """Этап 4: топологическая сортировка."""
    pkg = cfg["package_name"]
    print(f"\n[Этап 4] Порядок загрузки для {pkg}:")
    order = topological_sort(graph, pkg)
    for i, p in enumerate(order, 1):
        print(f"  {i}. {p}")


def run_stage5(cfg: Dict[str, str], graph: Dict) -> None:
    """Этап 5: визуализация Graphviz -> PNG."""
    out = cfg["output_file"]
    print(f"\n[Этап 5] Визуализация -> {out}")
    dot = graph_to_dot(graph)
    render_png(dot, out)
    print(f"  Граф сохранён в {out}")


def main() -> int:
    """Точка входа приложения."""
    path = DEFAULT_CONFIG
    if len(sys.argv) > 1:
        path = sys.argv[1]
    try:
        cfg = load_config(path)
    except ConfigError as e:
        print(f"[ОШИБКА] {e}", file=sys.stderr)
        return 1
    print_config(cfg)
    run_stage2(cfg)
    graph = run_stage3(cfg)
    run_stage4(cfg, graph)
    run_stage5(cfg, graph)
    return 0


if __name__ == "__main__":
    sys.exit(main())
