import random
import time

from sortedcontainers import SortedDict

from ce import create_tsp
from ce.algorithms.greedy_heuristics import random_solution
from ce.algorithms.local_search import two_edges_neighborhood
from ce.algorithms.local_search.local_search_cache import steepest_local_search_cache


def select_parents(population):
    return random.sample(population, 2)


def crossover(parent1, parent2):
    return parent1[:80] + [p for p in parent2 if p not in set(parent1[:80])][:20]


def evolution(tsp, initial_population, local_search_fn, time_limit):
    population = [local_search_fn(tsp, x)[0] for x in initial_population]
    population = SortedDict({tsp.get_solution_cost(x): x for x in population})

    iterations, iterations_with_improvements, start_time = 0, 0, time.time()
    while time.time() - start_time < time_limit:
        parents = select_parents(population.values())
        offspring = crossover(*parents)
        offspring = local_search_fn(tsp, offspring)[0]
        offspring_cost = tsp.get_solution_cost(offspring)
        if offspring_cost < population.keys()[-1] and offspring_cost not in population:
            del population.keys()[-1]
            population[offspring_cost] = offspring
            iterations_with_improvements += 1
        iterations += 1

    return population, iterations, iterations_with_improvements


if __name__ == '__main__':
    ls_fn = lambda tsp, x: steepest_local_search_cache(tsp, x, two_edges_neighborhood)

    t = create_tsp("../../../../data/TSPC.csv")
    c = [random_solution(t) for _ in range(20)]
