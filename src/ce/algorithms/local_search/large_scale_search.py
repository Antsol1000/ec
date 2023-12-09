import time
from typing import List

import numpy as np

from ce import TSP
from ce.algorithms.greedy_regret_heuristics.greedy_cycle_with_weighted_regret import extend_cycle
from ce.algorithms.local_search.local_search_cache import steepest_local_search_cache


def break_solution(solution: List[int], break_factor=0.3):
    break_length = int(break_factor * len(solution))
    start_index = np.random.randint(1, len(solution) - break_length)
    end_index = start_index + break_length

    return solution[:start_index] + solution[end_index:]


def repair_solution(solution: List[int], tsp: TSP):
    while len(solution) < tsp.get_desired_solution_length():
        solution = extend_cycle(solution, tsp, 0.5)

    return solution


def large_scale_search(tsp: TSP, init_solution: List[int], time_limit: float, neighborhood_fn, with_ls: bool):
    best_solution, _ = steepest_local_search_cache(tsp, init_solution, neighborhood_fn)
    best_solution_cost, iterations = tsp.get_solution_cost(best_solution), 0

    start_time = time.time()
    while time.time() - start_time < time_limit:
        iterations += 1
        new_solution = break_solution(best_solution)
        new_solution = repair_solution(new_solution, tsp)
        if with_ls:
            new_solution, _ = steepest_local_search_cache(tsp, new_solution, neighborhood_fn)

        new_solution_cost = tsp.get_solution_cost(new_solution)
        if new_solution_cost < best_solution_cost:
            best_solution = new_solution
            best_solution_cost = new_solution_cost

    return best_solution, iterations
