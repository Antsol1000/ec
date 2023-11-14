from typing import List, Set

from ce import TSP


def get_candidate_edges_for_solution_vertex(tsp: TSP, vertex: int, n: int = 10):
    # outer nodes are nodes not in solution
    outer_nodes = [i for i in tsp.indexes if i != vertex]

    costs = []
    for outer_node in outer_nodes:
        # calculate cost of inserting outer node between previous and next vertex
        cost = tsp.distances[vertex, outer_node] + tsp.nodes[outer_node].cost
        costs.append((outer_node, cost))

        # get n best candidates
    costs.sort(key=lambda x: x[1])
    candidate_edges = set([(vertex, costs[i][0]) for i in range(n)])
    return candidate_edges

def calculate_candidate_endges(tsp: TSP, n: int):
    set_of_candidate_edges = set()
    for i, _ in enumerate(tsp.indexes):
        candidate_edges = get_candidate_edges_for_solution_vertex(tsp, i, n = n)
        # add candidate edges to set
        set_of_candidate_edges.update(candidate_edges)
    return set_of_candidate_edges


def inter_route_candidate_moves(solution: List[int], tsp: TSP, candidate_edges: Set):
    # replace any node of the solution with any node from the rest
    # return pair (position_to_replace, node_idx_to_insert)
    # calculate candidate nodes take in vertex cost and distance

    for i, _ in enumerate(solution):
        outer_nodes = [i for i in tsp.indexes if i not in solution]
        previous_vertex = solution[(i - 1) % len(solution)]
        next_vertex = solution[(i + 1) % len(solution)]
        for n in outer_nodes:
            if (previous_vertex, n) in candidate_edges or (next_vertex, n) in candidate_edges:
                yield i, n


def two_edges_candidate_moves(solution: List[int], candidate_edges: Set):
    # exchange position of any two edges
    # return pair (position_of_edge_1, position_of_edge_2)
    # edge nr i connects nodes i and i+1
    for i, i_node in enumerate(solution):
        for j, j_node in enumerate(solution):
            # no point in exchanging adjacent edges
            if i < j and (j - i) > 1 and not (i == 0 and j == len(solution) - 1):
                if (i_node, j_node) in candidate_edges or (j_node, i_node) in candidate_edges or  (solution[(j + 1) % len(solution)], solution[(i + 1) % len(solution)]) in candidate_edges or (solution[(i + 1) % len(solution)], solution[(j + 1) % len(solution)]) in candidate_edges:
                    yield i, j

def two_nodes_candidate_moves(solution: List[int], candidate_edges: Set):
    # exchange position of any two nodes
    # return pair (position_1, position_2)
    for i, _ in enumerate(solution):
        for j, _ in enumerate(solution):
            # first node is fixed to not generate different (but same) neighbors
            if 0 < i < j:
                previous_vertex_i = solution[(i - 1) % len(solution)]
                next_vertex_i = solution[(i + 1) % len(solution)]
                previous_vertex_j = solution[(j - 1) % len(solution)]
                next_vertex_j = solution[(j + 1) % len(solution)]
                if (previous_vertex_i, solution[j]) in candidate_edges or (solution[j], next_vertex_i) in candidate_edges or (previous_vertex_j, solution[i]) in candidate_edges or (solution[i], next_vertex_j) in candidate_edges:
                    yield i, j
                    
                    
