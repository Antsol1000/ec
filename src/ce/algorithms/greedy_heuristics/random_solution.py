import random
from typing import List

from ce import TSP


def get_next_random_node(current_solution: List[int], tsp: TSP) -> int:
    allowable_nodes = [i for i in tsp.indexes if i not in current_solution]

    return random.sample(allowable_nodes, 1)[0]


def random_solution(tsp: TSP, with_debug=None) -> List[int]:
    k = tsp.get_desired_solution_length()

    solution = []
    while len(solution) < k:
        if with_debug is not None:
            with_debug.append(solution.copy())

        current_node = get_next_random_node(solution, tsp)
        solution.append(current_node)

    return solution
