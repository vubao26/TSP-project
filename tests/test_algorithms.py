"""
Test cơ bản: kiểm tra tất cả thuật toán đều trả về tuyến đường hợp lệ
(đi qua đúng n thành phố, không lặp) trên bộ dữ liệu mẫu nhỏ.

Chạy: python -m pytest tests/  (hoặc python tests/test_algorithms.py)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.utils import load_cities, build_distance_matrix
from algorithms import nearest_neighbor, dynamic_programming, branch_and_bound
from algorithms import genetic_algorithm, aco


def _is_valid_route(route, n):
    return sorted(route) == list(range(n))


def test_nearest_neighbor():
    coords = load_cities(os.path.join(os.path.dirname(__file__), "..", "data", "sample_10.txt"))
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = nearest_neighbor.solve(dist_matrix)
    assert _is_valid_route(route, len(coords))
    assert dist > 0


def test_dynamic_programming():
    coords = load_cities(os.path.join(os.path.dirname(__file__), "..", "data", "sample_10.txt"))
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = dynamic_programming.solve(dist_matrix)
    assert _is_valid_route(route, len(coords))


def test_branch_and_bound():
    coords = load_cities(os.path.join(os.path.dirname(__file__), "..", "data", "sample_10.txt"))
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = branch_and_bound.solve(dist_matrix)
    assert _is_valid_route(route, len(coords))
    # DP là tối ưu, branch and bound phải cho ra cùng kết quả tối ưu
    dp_route, dp_dist, _ = dynamic_programming.solve(dist_matrix)
    assert abs(dist - dp_dist) < 1e-6


def test_genetic_algorithm():
    coords = load_cities(os.path.join(os.path.dirname(__file__), "..", "data", "sample_10.txt"))
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = genetic_algorithm.solve(dist_matrix, generations=50, seed=1)
    assert _is_valid_route(route, len(coords))


def test_aco():
    coords = load_cities(os.path.join(os.path.dirname(__file__), "..", "data", "sample_10.txt"))
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = aco.solve(dist_matrix, iterations=20, seed=1)
    assert _is_valid_route(route, len(coords))


if __name__ == "__main__":
    test_nearest_neighbor()
    test_dynamic_programming()
    test_branch_and_bound()
    test_genetic_algorithm()
    test_aco()
    print("Tất cả test đều PASS!")
