from typing import List, Tuple

from numba import jit

from ce import TSP


@jit(nopython=True, cache=True)
def two_edges_moves(solution: List[int]):
    # exchange position of any two edges
    # return pair (position_of_edge_1, position_of_edge_2)
    # edge nr i connects nodes i and i+1
    m = []
    for i, _ in enumerate(solution):
        for j, _ in enumerate(solution):
            # no point in exchanging adjacent edges
            if i < j and (j - i) > 1 and not (i == 0 and j == len(solution) - 1):
                m.append((2, (i, j)))
    return m


def two_edges_cost_delta(solution: List[int], move: Tuple[int, int], tsp: TSP) -> int:
    i, j = move
    from1, to1 = solution[i], solution[(i + 1) % len(solution)]
    from2, to2 = solution[j], solution[(j + 1) % len(solution)]
    return (
            - tsp.distances[from1, to1] - tsp.distances[from2, to2]
            + tsp.distances[from1, from2] + tsp.distances[to1, to2]
    )


def two_edges_new_solution(solution: List[int], move: Tuple[int, int]) -> List[int]:
    i, j = move
    return solution[:i + 1] + solution[j:i:-1] + solution[j + 1:]


if __name__ == '__main__':
    s = [0, 1, 2, 3, 4]
    for m in two_edges_moves(s):
        print(f"{m}: {two_edges_new_solution(s, m)}")
