import time
from typing import List

import numpy as np

from ce import TSP
from ce.algorithms.local_search.local_search_cache import steepest_local_search_cache


def break_solution(solution: List[int], indexes: List[int], break_length=20) -> List[int]:
    start_index = np.random.randint(0, len(solution) - break_length)
    end_index = start_index + break_length

    outer_nodes = np.array(list(set(indexes) - set(solution[:start_index]) - set(solution[end_index:])))
    replacements = np.random.choice(outer_nodes, size=break_length, replace=False).tolist()

    return solution[:start_index] + replacements + solution[end_index:]


def multiple_start_local_search(tsp: TSP, init_solutions: List[List[int]], neighborhood_fn):
    best_solution, best_solution_cost, total_iterations = None, 1e9, 0

    for init_solution in init_solutions:
        solution, iterations = steepest_local_search_cache(tsp, init_solution, neighborhood_fn)
        solution_cost = tsp.get_solution_cost(solution)
        if solution_cost < best_solution_cost:
            best_solution = solution
            best_solution_cost = solution_cost
        total_iterations += iterations

    return best_solution, total_iterations


def iterated_local_search(tsp: TSP, init_solution: List[int], time_limit: float, neighborhood_fn, ls_counter_log=None):
    best_solution, best_solution_cost, total_iterations, ls_counter = None, 1e9, 0, 0
    solution = init_solution

    start_time = time.time()
    while time.time() - start_time < time_limit:
        solution, iterations = steepest_local_search_cache(tsp, solution, neighborhood_fn)
        solution_cost = tsp.get_solution_cost(solution)
        if solution_cost < best_solution_cost:
            best_solution = solution
            best_solution_cost = solution_cost
        total_iterations += iterations
        ls_counter += 1
        solution = break_solution(solution, tsp.indexes)

    if ls_counter_log is not None:
        ls_counter_log.append(ls_counter)

    return best_solution, total_iterations
