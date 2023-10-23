from typing import List, Tuple

from ce import TSP, get_edges
import logging
import numpy as np


def get_2_regret_weighted(edges: List[Tuple[int, int]], tsp: TSP, node_index: int) -> Tuple[int, Tuple[int, int]]:
    u, v = np.array(edges).T
    dist_uv = tsp.distances[u, v]
    dist_un = tsp.distances[u, node_index]
    dist_nv = tsp.distances[node_index, v]
    temp_dist = dist_un + dist_nv - dist_uv
    
    change_of_distance = np.column_stack((temp_dist, np.arange(len(edges))))
    best_edge, second_best_edge = change_of_distance[change_of_distance[:, 0].argsort()][:2]
    return second_best_edge[0] - tsp.nodes[node_index].cost  , int(best_edge[1]) 

def extend_cycle(cycle: List[int], tsp: TSP):
    if len(cycle) == 1:
        current_node = cycle[0]
        next_node = np.argmin(tsp.distances[current_node, :] + np.array([node.cost for node in tsp.nodes]))
        return [current_node, next_node]

    # iterate over nodes and get cost of adding each node to cycle
    edges = get_edges(cycle)
    nodes_indices = set(tsp.indexes) - set(cycle)
    regrets = [(node, get_2_regret_weighted(edges, tsp, node)) for node in nodes_indices]
    
    # get bigest regret 
    node, (regret, edge_to_extend) = max(regrets, key=lambda x: x[1][0])
    cycle.insert(edge_to_extend + 1, node)
    return cycle
    
    
def greedy_cycle_with_weighted_regret(tsp: TSP, start_node: int, with_debug=None) -> List[int]:
    all_nodes, k = tsp.indexes, tsp.get_desired_solution_length()

    solution = [start_node]
    while len(solution) < k:
        if with_debug is not None:
            with_debug.append(solution.copy())

        solution = extend_cycle(solution, tsp)

    return solution
