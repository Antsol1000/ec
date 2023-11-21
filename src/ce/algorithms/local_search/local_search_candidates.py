from ce.algorithms.local_search.local_search import get_cost_delta, get_cost_delta_matrix, get_new_solution
from ce.algorithms.local_search.neighbor.candidate_moves import *


def two_nodes_candidates_neighborhood(solution: List[int], tsp: TSP, candidate_edges: set):
    return (
            inter_route_candidate_moves(solution, tsp.indexes, candidate_edges)
            + two_nodes_candidate_moves(solution, candidate_edges)
    )


def two_edges_candidates_neighborhood(solution: List[int], tsp: TSP, candidate_edges: set):
    return (
            inter_route_candidate_moves(solution, tsp.indexes, candidate_edges)
            + two_edges_candidate_moves(solution, candidate_edges)
    )


def get_cost_delta_matrix(neighborhood_fn, solution, tsp: TSP, candidate_edges):
    return {
        n: get_cost_delta(n, solution, tsp)
        for n in neighborhood_fn(solution, tsp, candidate_edges)
    }


def steepest_local_candidates_search(tsp: TSP, init_solution, neighborhood_fn, candidate_edges):
    solution = init_solution
    local_optimum, counter = False, 0

    while not local_optimum:
        cost_delta_matrix = get_cost_delta_matrix(neighborhood_fn, solution, tsp, candidate_edges)
        best_neighbor = min(cost_delta_matrix, key=cost_delta_matrix.get)
        if cost_delta_matrix[best_neighbor] < 0:
            solution = get_new_solution(best_neighbor, solution)
            counter += 1
        else:
            local_optimum = True

    return solution, counter
