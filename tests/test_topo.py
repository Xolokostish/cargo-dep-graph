"""Тесты топологической сортировки."""

import unittest

from src.topo import topological_sort


class TestTopoSort(unittest.TestCase):
    """Тесты topological_sort."""

    def test_linear_chain(self) -> None:
        """Цепочка A -> B -> C."""
        graph = {"A": ["B"], "B": ["C"], "C": []}
        order = topological_sort(graph, "A")
        self.assertLess(
            order.index("C"), order.index("B")
        )
        self.assertLess(
            order.index("B"), order.index("A")
        )

    def test_diamond(self) -> None:
        """Ромб: A -> B,C -> D."""
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        order = topological_sort(graph, "A")
        self.assertLess(
            order.index("D"), order.index("B")
        )
        self.assertLess(
            order.index("D"), order.index("C")
        )
        self.assertLess(
            order.index("B"), order.index("A")
        )


if __name__ == "__main__":
    unittest.main()
