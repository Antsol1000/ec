
from ce.utils.plot import quality_plots

def experiment(runs, run_fn, cost_fn):
    results, best_solution, best_solution_cost = [], None, 1e9

    for i in range(runs):
        solution = run_fn(i)
        cost = cost_fn(solution)
        results.append(cost)
        if cost < best_solution_cost:
            best_solution = solution
            best_solution_cost = cost

    print(f'MIN {min(results)}, AVG {sum(results) / len(results)}, MAX {max(results)}')
    return results, best_solution

def run_all_experiments(runs, list_of_fn, cost_fn, names):
    best_solutions = []
    results_list = []
    
    for fn, name in zip(list_of_fn, names):
        print(f'Running {name}')
        result, best_sol = experiment(runs, fn, cost_fn)
        results_list.append(result)
        best_solutions.append(best_sol)
    quality_plots(results_list, categories=names)
    return best_solutions, results_list