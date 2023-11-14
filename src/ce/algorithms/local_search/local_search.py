import numpy as np

from ce.algorithms.local_search.neighbor.inter_route import *
from ce.algorithms.local_search.neighbor.two_edges import *
from ce.algorithms.local_search.neighbor.two_nodes import *
from ce import TSP


def two_nodes_neighborhood(solution: List[int], tsp: TSP):
    return (
            [('i', move) for move in inter_route_moves(solution, tsp)]
            + [('2n', move) for move in two_nodes_moves(solution)]
    )


def two_edges_neighborhood(solution: List[int], tsp: TSP):
    return (
            [('i', move) for move in inter_route_moves(solution, tsp)]
            + [('2e', move) for move in two_edges_moves(solution)]
    )


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


def greedy_local_search(tsp: TSP, init_solution, neighborhood_fn):
    solution = init_solution
    local_optimum, counter = False, 0

    while not local_optimum:
        step_done = False

        neighborhood = neighborhood_fn(solution, tsp)
        random_order = np.arange(len(neighborhood))
        np.random.shuffle(random_order)
        for i in random_order:
            cost_delta = get_cost_delta(neighborhood[i], solution, tsp)
            if cost_delta < 0:
                solution = get_new_solution(neighborhood[i], solution)
                step_done = True
                counter += 1
                break

        if not step_done:
            local_optimum = True

    return solution, counter


def steepest_local_search(tsp: TSP, init_solution, neighborhood_fn):
    solution = init_solution
    local_optimum, counter = False, 0

    while not local_optimum:
        neighborhood = neighborhood_fn(solution, tsp)
        cost_delta_matrix = {n: get_cost_delta(n, solution, tsp) for n in neighborhood}
        best_neighbor = min(neighborhood, key=lambda x: cost_delta_matrix[x])
        if cost_delta_matrix[best_neighbor] < 0:
            solution = get_new_solution(best_neighbor, solution)
            counter += 1
        else:
            local_optimum = True

    return solution, counter
