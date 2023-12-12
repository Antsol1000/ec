from typing import List, Set, Tuple


def node_similarity(solution1: List[int], solution2: List[int]) -> float:
    common_nodes = set(solution1).intersection(set(solution2))
    return len(common_nodes) / len(solution1)


def _get_edges(solution: List[int]) -> Set[Tuple[int, int]]:
    edges = set(zip(solution, solution[1:] + [solution[0]]))
    return edges.union(e[::-1] for e in edges)


def edge_similarity(solution1: List[int], solution2: List[int]) -> float:
    common_edges = _get_edges(solution1).intersection(_get_edges(solution2))
    return len(common_edges) / 2 / len(solution1)


def calculate_similarities(solution: List[int], other_solutions: List[List[int]], similarity_fn) -> List[float]:
    return [similarity_fn(solution, x) for x in other_solutions]


def calculate_avg_similarity(solution: List[int], other_solutions: List[List[int]], similarity_fn) -> float:
    similarities = calculate_similarities(solution, other_solutions, similarity_fn)
    return sum(similarities) / len(similarities)


if __name__ == '__main__':
    print(calculate_similarities([1, 2, 3], [[3, 2, 1], [3, 5, 4], [4, 5, 6]], node_similarity))
    print(calculate_similarities([1, 2, 3, 4], [[1, 2, 3, 5], [1, 3, 2, 4], [4, 3, 2, 1]], edge_similarity))
