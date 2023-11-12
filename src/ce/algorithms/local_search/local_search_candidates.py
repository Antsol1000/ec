import random

from ce.algorithms.local_search.neighbor.inter_route import *
from ce.algorithms.local_search.neighbor.two_edges import *
from ce.algorithms.local_search.neighbor.two_nodes import *
from ce.algorithms.local_search.neighbor.candidate_moves import *
from ce.tsp_optimized import TSP


def two_nodes_candidates_neighborhood(solution: List[int], tsp: TSP, candidate_edges: set):
    neighborhood = (
            [('i', move) for move in inter_route_candidate_moves(solution, tsp, candidate_edges)]
            + [('2n', move) for move in two_nodes_candidate_moves(solution, candidate_edges)]
    )
    random.shuffle(neighborhood)
    return neighborhood


def two_edges_candidates_neighborhood(solution: List[int], tsp: TSP, candidate_edges: set):
    neighborhood = (
            [('i', move) for move in inter_route_candidate_moves(solution, tsp, candidate_edges)]
            + [('2e', move) for move in two_edges_candidate_moves(solution, candidate_edges)]
    )
    random.shuffle(neighborhood)
    return neighborhood


def get_cost_delta(neighbor, solution, tsp: TSP):
    move_type, move = neighbor
    return {
        'i': inter_route_cost_delta,
        '2n': two_nodes_cost_delta,
        '2e': two_edges_cost_delta,
    }[move_type](solution, move, tsp)


def get_new_solution(neighbor, solution):
    move_type, move = neighbor
    return {
        'i': inter_route_new_solution,
        '2n': two_nodes_new_solution,
        '2e': two_edges_new_solution,
    }[move_type](solution, move)



def steepest_local_candidates_search(tsp: TSP, init_solution, neighborhood, n = 10) -> List[int]:
    solution = init_solution
    local_optimum = False
    
    candidate_edges = calculate_candidate_endges(tsp, n)
    while not local_optimum:
        best_neighbor = min(neighborhood(solution, tsp, candidate_edges), key=lambda x: get_cost_delta(x, solution, tsp))
        if get_cost_delta(best_neighbor, solution, tsp) < 0:
            solution = get_new_solution(best_neighbor, solution)
        else:
            local_optimum = True

    return solution
