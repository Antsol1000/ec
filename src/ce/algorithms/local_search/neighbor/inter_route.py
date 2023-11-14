from typing import List, Tuple

from numba import jit, njit

from ce import TSP


@jit(nopython=True, cache=True)
def inter_route_moves(solution: List[int], indexes):
    # replace any node of the solution with any node from the rest
    # return pair (position_to_replace, node_idx_to_insert)
    m = []
    for i, _ in enumerate(solution):
        for n in set(indexes) - set(solution):
            m.append((0, (i, n)))
    return m


def inter_route_cost_delta(solution: List[int], move: Tuple[int, int], tsp: TSP) -> int:
    i, outer_node = move
    node_to_replace = solution[i]
    before, after = solution[(i - 1) % len(solution)], solution[(i + 1) % len(solution)]

    return (
            + tsp.nodes[outer_node].cost - tsp.nodes[node_to_replace].cost
            + tsp.distances[before, outer_node] + tsp.distances[outer_node, after]
            - tsp.distances[before, node_to_replace] - tsp.distances[after, node_to_replace]
    )


def inter_route_new_solution(solution: List[int], move: Tuple[int, int]) -> List[int]:
    i, outer_node = move
    return solution[:i] + [outer_node] + solution[i + 1:]


if __name__ == '__main__':
    s = [0, 1, 2]
    t = TSP([0, 1, 2, 3, 4, 5], None, None)
    for m in inter_route_moves(s, t):
        print(f"{m}: {inter_route_new_solution(s, m)}")
