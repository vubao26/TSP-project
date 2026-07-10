import itertools
from tsp_utils import measure_performance


def _brute_force_core(dist_matrix, start=0):
    n = len(dist_matrix)
    cities = [c for c in range(n) if c != start]

    best_tour = None
    best_length = float("inf")
    permutations_checked = 0

    # Thu TAT CA (n-1)! hoan vi cua cac thanh pho con lai
    for perm in itertools.permutations(cities):
        candidate_tour = [start] + list(perm)
        permutations_checked += 1

        # Tinh do dai chu trinh ung voi hoan vi nay
        length = 0.0
        for i in range(n):
            a = candidate_tour[i]
            b = candidate_tour[(i + 1) % n]
            length += dist_matrix[a][b]

        if length < best_length:
            best_length = length
            best_tour = candidate_tour

    extra_info = {
        "permutations_checked": permutations_checked,
        "theoretical_permutations": math_factorial(n - 1),
    }
    return best_tour, extra_info


def math_factorial(k):
    result = 1
    for i in range(2, k + 1):
        result *= i
    return result


@measure_performance("Brute Force")
def solve(dist_matrix, start=0):
    return _brute_force_core(dist_matrix, start)
