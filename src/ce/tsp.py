import csv

from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class Node:
    idx: int
    x: int
    y: int
    cost: int


def get_edges(cycle: List[int]) -> List[Tuple[int, int]]:
    if not cycle:
        return []

    return list(zip(cycle, cycle[1:] + [cycle[0]]))


@dataclass
class TSP:
    indexes: List[int]
    nodes: List[Node]
    distances: np.ndarray

    def get_desired_solution_length(self) -> int:
        return (len(self.nodes) + 1) // 2

    def get_solution_cost(self, solution: List[int]) -> int:
        dist_cost = sum(self.distances[i, j] for i, j in get_edges(solution))
        node_cost = sum(self.nodes[i].cost for i in solution)
        return dist_cost + node_cost

    def plot(self, solutions: List[List[int]] = ((), )):
        num_plots = len(solutions)
        fig, axs = plt.subplots(1, len(solutions), figsize=(8*num_plots,8))

        for i, s in enumerate(solutions):
            self._plot_single(s, axs[i] if len(solutions) > 1 else axs)

        plt.show()

    def _plot_single(self, solution: List[int], fig):
        x = [c.x for c in self.nodes]
        y = [c.y for c in self.nodes]
        costs = [c.cost for c in self.nodes]
        max_cost = max(costs)
        costs_normalised = [cost*5/max_cost for cost in costs]
        fig.scatter(x, y, s=costs_normalised, marker="o")

        for a, b in get_edges(solution):
            x = [self.nodes[a].x, self.nodes[b].x]
            y = [self.nodes[a].y, self.nodes[b].y]
            fig.plot(x, y, lw=1, ls="-", marker="", color='red')


def create_tsp(file_path: str) -> TSP:
    def load_nodes_from_csv(file_path: str) -> List[Node]:
        nodes = []
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            for i, row in enumerate(csv_reader):
                row = [int(value) for value in row]
                nodes.append(Node(i, *row))
        return nodes

    def get_distances(nodes: List[Node]) -> np.ndarray:
        def distance(n1: Node, n2: Node) -> int:
            return round(((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2) ** .5)

        distances = np.zeros((len(nodes), len(nodes)))
        for i, n1 in enumerate(nodes):
            for j, n2 in enumerate(nodes):
                distances[i, j] = distance(n1, n2) if n1 != n2 else 1e9
        return distances

    nodes = load_nodes_from_csv(file_path)
    indexes = [n.idx for n in nodes]
    distances = get_distances(nodes)
    return TSP(indexes, nodes, distances)

