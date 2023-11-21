from typing import List, Tuple

from ce import TSP, create_tsp
from ce.algorithms.local_search.local_search import get_cost_delta, get_cost_delta_matrix, get_new_solution, \
    two_edges_neighborhood, \
    two_nodes_neighborhood


def update_matrix_inter(matrix: dict, solution: List[int], new_solution: List[int], move: Tuple[int, int],
                        move_types: List[int], tsp: TSP):
    position, outer_node = move
    node_to_replace = solution[position]
    position_before, position_after = (position - 1) % len(solution), (position + 1) % len(solution)

    # inter moves
    if 0 in move_types:
        for i, _ in enumerate(solution):
            # remove inserted outer_node from cache
            del matrix[(0, (i, outer_node))]
            # calculate costs for removed node
            matrix[(0, (i, node_to_replace))] = get_cost_delta((0, (i, node_to_replace)), new_solution, tsp)
        for n in set(tsp.indexes) - set(new_solution):
            # recalculate for nodes adjacent to the exchanged one
            for r in (position_before, position, position_after):
                matrix[(0, (r, n))] = get_cost_delta((0, (r, n)), new_solution, tsp)

    # 2-nodes moves
    if 1 in move_types:
        for i, _ in enumerate(solution):
            # recalculate for nodes adjacent to the exchanged one
            for j in (position_before, position, position_after):
                if 0 < i < j:
                    matrix[(1, (i, j))] = get_cost_delta((1, (i, j)), new_solution, tsp)
                if 0 < j < i:
                    matrix[(1, (j, i))] = get_cost_delta((1, (j, i)), new_solution, tsp)

    # 2-edges moves
    if 2 in move_types:
        for i, _ in enumerate(solution):
            # recalculate for edges that touch exchanged node
            for j in (position_before, position):
                if i < j and (j - i) > 1 and not (i == 0 and j == len(solution) - 1):
                    matrix[(2, (i, j))] = get_cost_delta((2, (i, j)), new_solution, tsp)
                if j < i and (i - j) > 1 and not (j == 0 and i == len(solution) - 1):
                    matrix[(2, (j, i))] = get_cost_delta((2, (j, i)), new_solution, tsp)


def update_matrix_2nodes(matrix: dict, solution: List[int], new_solution: List[int], move: Tuple[int, int],
                         move_types: List[int], tsp: TSP):
    pos1, pos2 = move
    before1, after1 = (pos1 - 1) % len(solution), (pos1 + 1) % len(solution)
    before2, after2 = (pos2 - 1) % len(solution), (pos2 + 1) % len(solution)

    # inter moves
    if 0 in move_types:
        for n in set(tsp.indexes) - set(new_solution):
            # update rows (-/+ 1) (corresponding to replacement position in solution)
            for r in {pos1, pos2, before1, before2, after1, after2}:
                matrix[(0, (r, n))] = get_cost_delta((0, (r, n)), new_solution, tsp)

    # 2-nodes moves
    if 1 in move_types:
        for i, _ in enumerate(solution):
            # update rows (-/+ 1) (corresponding to replacement position in solution)
            for j in {pos1, pos2, before1, before2, after1, after2}:
                if 0 < i < j:
                    matrix[(1, (i, j))] = get_cost_delta((1, (i, j)), new_solution, tsp)
                if 0 < j < i:
                    matrix[(1, (j, i))] = get_cost_delta((1, (j, i)), new_solution, tsp)

    # 2-edges moves
    if 2 in move_types:
        pass


def update_matrix_2edges(matrix: dict, solution: List[int], new_solution: List[int], move: Tuple[int, int],
                         move_types: List[int], tsp: TSP):
    e1, e2 = move
    from1, to1 = e1, (e1 + 1) % len(solution)
    from2, to2 = e2, (e2 + 1) % len(solution)

    # inter moves
    if 0 in move_types:
        for n in set(tsp.indexes) - set(new_solution):
            # recalculate for nodes in exchange
            for r in {from1, to1, from2, to2}:
                matrix[(0, (r, n))] = get_cost_delta((0, (r, n)), new_solution, tsp)
            # swap for nodes where direction was changed
            for r in range((from2 - to1) // 2):
                a, b = to1 + 1 + r, from2 - r - 1
                matrix[(0, (a, n))], matrix[(0, (b, n))] = matrix[(0, (b, n))], matrix[(0, (a, n))]

    # 2-nodes moves
    if 1 in move_types:
        pass

    # 2-edges moves
    if 2 in move_types:
        for i, _ in enumerate(solution):
            # recalculate for edges between the whole exchange
            for j in range(from1, from2 + 1):
                if i < j and (j - i) > 1 and not (i == 0 and j == len(solution) - 1):
                    matrix[(2, (i, j))] = get_cost_delta((2, (i, j)), new_solution, tsp)
                if j < i and (i - j) > 1 and not (j == 0 and i == len(solution) - 1):
                    matrix[(2, (j, i))] = get_cost_delta((2, (j, i)), new_solution, tsp)


def update_matrix(matrix, neighbor, solution, new_solution, move_types, tsp):
    move_type, move = neighbor
    return {
        0: update_matrix_inter,
        1: update_matrix_2nodes,
        2: update_matrix_2edges,
    }[move_type](matrix, solution, new_solution, move, move_types, tsp)


def get_move_types(neighborhood_fn) -> List[int]:
    return {
        two_nodes_neighborhood: [0, 1],
        two_edges_neighborhood: [0, 2],
    }[neighborhood_fn]


def print_cost_matrix(move_type, matrix):
    sol, out = set(), set()
    for i in matrix:
        m, (a, b) = i
        if m == move_type:
            sol.add(a)
            out.add(b)
    sol, out = list(sol), list(out)
    sol.sort()
    out.sort()
    print("  |", end="\t")
    for i in out:
        print(i, end="\t")
    print()
    print("------------------")
    for i in sol:
        print(str(i) + " |", end='\t')
        for j in out:
            if move_type == 0:
                print(f"{matrix[(move_type, (i, j))]:03.0f}", end="\t")
            if move_type == 1:
                if i == j:
                    print("NA", end="\t")
                else:
                    print(f"{matrix[(move_type, tuple(sorted((i, j))))]:03.0f}", end="\t")
        print()
    print()


def steepest_local_search_cache(tsp: TSP, init_solution, neighborhood_fn):
    solution = init_solution
    local_optimum, counter = False, 0
    cost_delta_matrix = get_cost_delta_matrix(neighborhood_fn, solution, tsp)

    while not local_optimum:
        best_neighbor = min(cost_delta_matrix, key=cost_delta_matrix.get)
        if cost_delta_matrix[best_neighbor] < 0:
            new_sol = get_new_solution(best_neighbor, solution)
            update_matrix(cost_delta_matrix, best_neighbor, solution, new_sol, get_move_types(neighborhood_fn), tsp)
            solution = new_sol
            counter += 1
        else:
            local_optimum = True

    return solution, counter


if __name__ == '__main__':
    steepest_local_search_cache(create_tsp("../../../../data/tsp_test.csv"), [3, 5, 4, 6], two_nodes_neighborhood)
