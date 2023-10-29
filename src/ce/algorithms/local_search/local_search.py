import random

from ce.algorithms.local_search.neighbor.inter_route import *
from ce.algorithms.local_search.neighbor.two_edges import *
from ce.algorithms.local_search.neighbor.two_nodes import *
from ce.tsp_optimized import TSP


def two_nodes_neighborhood(solution: List[int], tsp: TSP):
    neighborhood = (
            [('i', move) for move in inter_route_moves(solution, tsp)]
            + [('2n', move) for move in two_nodes_moves(solution)]
    )
    random.shuffle(neighborhood)
    return neighborhood


def two_edges_neighborhood(solution: List[int], tsp: TSP):
    neighborhood = (
            [('i', move) for move in inter_route_moves(solution, tsp)]
            + [('2e', move) for move in two_edges_moves(solution)]
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


def greedy_local_search(tsp: TSP, init_solution, neighborhood) -> List[int]:
    solution = init_solution
    local_optimum = False

    while not local_optimum:
        step_done = False

        neighborhood1 = neighborhood(solution, tsp)
        for neighbor in neighborhood1:
            cost_delta = get_cost_delta(neighbor, solution, tsp)
            if cost_delta < 0:
                solution = get_new_solution(neighbor, solution)
                step_done = True
                break

        if not step_done:
            local_optimum = True

    return solution


def steepest_local_search(tsp: TSP, init_solution, neighborhood) -> List[int]:
    solution = init_solution
    local_optimum = False

    while not local_optimum:
        best_neighbor = min(neighborhood(solution, tsp), key=lambda x: get_cost_delta(x, solution, tsp))
        if get_cost_delta(best_neighbor, solution, tsp) < 0:
            solution = get_new_solution(best_neighbor, solution)
        else:
            local_optimum = True

    return solution
