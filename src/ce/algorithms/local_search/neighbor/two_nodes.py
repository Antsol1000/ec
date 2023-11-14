from typing import List, Tuple

from ce.tsp_optimized import TSP


def two_nodes_moves(solution: List[int]):
    # exchange position of any two nodes
    # return pair (position_1, position_2)
    for i, _ in enumerate(solution):
        for j, _ in enumerate(solution):
            # first node is fixed to not generate different (but same) neighbors
            if 0 < i < j:
                yield i, j


def two_nodes_cost_delta(solution: List[int], move: Tuple[int, int], tsp: TSP) -> int:
    i, j = move
    node1, node2 = solution[i], solution[j]
    before1, after1 = solution[(i - 1) % len(solution)], solution[(i + 1) % len(solution)]
    before2, after2 = solution[(j - 1) % len(solution)], solution[(j + 1) % len(solution)]

    if after1 == node2:
        return (
            + tsp.distances[before1, node2] + tsp.distances[node1, after2]
            - tsp.distances[before1, node1] - tsp.distances[node2, after2]
        )

    return (
            + tsp.distances[before1, node2] + tsp.distances[node2, after1]
            + tsp.distances[before2, node1] + tsp.distances[node1, after2]
            - tsp.distances[before1, node1] - tsp.distances[node1, after1]
            - tsp.distances[before2, node2] - tsp.distances[node2, after2]
    )


def two_nodes_new_solution(solution: List[int], move: Tuple[int, int]) -> List[int]:
    i, j = move
    return solution[:i] + [solution[j]] + solution[i + 1:j] + [solution[i]] + solution[j + 1:]


if __name__ == '__main__':
    s = [0, 1, 2, 3, 4]
    for m in two_nodes_moves(s):
        print(f"{m}: {two_nodes_new_solution(s, m)}")
