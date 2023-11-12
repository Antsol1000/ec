import time

from ce.utils.plot import quality_plots


def experiment(runs, run_fn, cost_fn):
    results_cost, results_time, best_solution, best_solution_cost = [], [], None, 1e9
    for i in range(runs):
        start = time.time()
        solution = run_fn(i)
        end = time.time()
        cost = cost_fn(solution)
        runtime = end - start
        results_cost.append(cost)
        results_time.append(runtime)
        if cost < best_solution_cost:
            best_solution = solution
            best_solution_cost = cost

    print(f'cost: AVG {sum(results_cost) / len(results_cost):0.2f}, ({min(results_cost):0.2f} - {max(results_cost):0.2f})', end='\t')
    print(f'time: AVG {sum(results_time) / len(results_time):0.2f}s, ({min(results_time):0.2f}s - {max(results_time):0.2f}s)')
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
