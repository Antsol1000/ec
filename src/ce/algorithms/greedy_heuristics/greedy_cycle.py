from typing import List, Tuple

from ce import TSP, get_edges


def get_cheapest_node_for_edge(a: int, b: int, cycle: List[int], tsp: TSP) -> Tuple[int, int]:
    allowable_nodes_with_cost = {
        i: tsp.distances[a][i] + tsp.distances[b][i] + tsp.nodes[i].cost
        for i in tsp.indexes if i not in cycle
    }

    next_node = min(allowable_nodes_with_cost, key=allowable_nodes_with_cost.get)
    return next_node, allowable_nodes_with_cost[next_node]


def extend_cycle(cycle: List[int], tsp: TSP):
    if len(cycle) == 1:
        current_node = cycle[0]
        next_node = min(range(len(tsp.distances[current_node])),
                        key=lambda x: tsp.distances[current_node][x] + tsp.nodes[x].cost)
        return [current_node, next_node]

    min_cost, min_node, min_edge_idx = 1e9, None, None
    for i, (a, b) in enumerate(get_edges(cycle)):
        cheapest_node, cheapest_node_cost = get_cheapest_node_for_edge(a, b, cycle, tsp)
        if cheapest_node_cost < min_cost:
            min_node = cheapest_node
            min_cost = cheapest_node_cost
            min_edge_idx = i

    cycle.insert(min_edge_idx, min_node)
    return cycle


def greedy_cycle(tsp: TSP, start_node: int, with_debug=None) -> List[int]:
    all_nodes, k = tsp.indexes, tsp.get_desired_solution_length()

    solution = [start_node]
    while len(solution) < k:
        if with_debug is not None:
            with_debug.append(solution.copy())

        solution = extend_cycle(solution, tsp)

    return solution
