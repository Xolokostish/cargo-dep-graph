"""Визуализация графа через Graphviz."""

import subprocess
from typing import Dict


def graph_to_dot(graph: Dict[str, list]) -> str:
    """Генерирует DOT-представление графа."""
    lines = ["digraph deps {", "  rankdir=LR;"]
    for node in graph:
        for dep in graph[node]:
            lines.append(f'  "{node}" -> "{dep}";')
    lines.append("}")
    return "\n".join(lines)


def render_png(dot: str, output: str) -> None:
    """Рендерит DOT в PNG через dot."""
    try:
        subprocess.run(
            ["dot", "-Tpng", "-o", output],
            input=dot,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as e:
        raise RuntimeError(
            "Graphviz не установлен. "
            "Выполни: brew install graphviz"
        ) from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Ошибка dot: {e.stderr}"
        ) from e
