import random
import time

import numpy as np

from ce import create_tsp
from ce.algorithms.greedy_heuristics import random_solution
from ce.algorithms.local_search import iterated_local_search, multiple_start_local_search, two_edges_neighborhood
from ce.utils.plot import quality_plots


def experiment(runs, run_fn, cost_fn):
    results_cost, results_iter, results_time, best_solution, best_solution_cost = [], [], [], None, 1e9
    for i in range(runs):
        start = time.time()
        solution, iterations = run_fn(i)
        end = time.time()
        cost = cost_fn(solution)
        runtime = end - start
        results_cost.append(cost)
        results_iter.append(iterations)
        results_time.append(runtime)
        if cost < best_solution_cost:
            best_solution = solution
            best_solution_cost = cost

    print(f'cost: {sum(results_cost) / len(results_cost):0.1f}, ({min(results_cost):0.0f} - {max(results_cost):0.0f})',
          end='\t|\t')
    print(
        f'iter: {sum(results_iter) / len(results_iter):05.1f}, ({min(results_iter):03.0f} - {max(results_iter):03.0f})',
        end='\t|\t')
    print(
        f'time: {sum(results_time) / len(results_time):0.1f}s, ({min(results_time):0.1f}s - {max(results_time):0.1f}s)')
    return results_cost, best_solution


def run_all_experiments(runs, list_of_fn, cost_fn, names):
    print("**************************************************************************************************")
    best_solutions = []
    results_list = []

    for fn, name in zip(list_of_fn, names):
        print(f'{name}:', end="\t")
        result, best_sol = experiment(runs, fn, cost_fn)
        results_list.append(result)
        best_solutions.append(best_sol)
    print("**************************************************************************************************\n\n")
    quality_plots(results_list, categories=names)
    return best_solutions, results_list


if __name__ == '__main__':
    t = create_tsp("../../../data/TSPC.csv")
    # c = [random_solution(t) for _ in range(5)]
    c = random_solution(t)

    random.seed(13)
    np.random.seed(13)

    # print(multiple_start_local_search(t, c, two_edges_neighborhood))
    cache = []
    print(iterated_local_search(t, c, 10, two_edges_neighborhood, cache))
    print(cache)
