from typing import List

from ce import TSP


def get_nearest_neighbor(node: int, current_solution: List[int], tsp: TSP) -> int:
    allowable_nodes = [i for i in tsp.indexes if i not in current_solution]

    # TODO: should we include node cost or not ???
    # return min(allowable_nodes, key=lambda x: tsp.distances[node][x] + tsp.nodes[x].cost)
    return min(allowable_nodes, key=lambda x: tsp.distances[node][x])


def nearest_neighbor(tsp: TSP, start_node: int, with_debug=None) -> List[int]:
    k = tsp.get_desired_solution_length()

    current_node, solution = start_node, [start_node]
    while len(solution) < k:
        if with_debug is not None:
            with_debug.append(solution.copy())

        current_node = get_nearest_neighbor(current_node, solution, tsp)
        solution.append(current_node)

    return solution
