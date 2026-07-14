"""
test_ilp.py

Unit test cho module ILP (algorithms/ilp.py), theo dung Buoc 5 - 6 cua Giai doan 2:
    - Thuat toan chay dung, khong loi.
    - Tour hop le (di qua du thanh pho, khong lap, quay ve diem xuat phat).
    - Tour Length tinh dung.
    - ILP phai cho nghiem toi uu (doi chieu voi Brute Force lam Ground Truth).

Dataset dung de test: cac bo du lieu nho tong hop (n <= 10), phu hop pham vi
khuyen dung cua ILP trong tai lieu nghien cuu (n <= 10).
"""

import itertools
import math
import unittest

from algorithms.ilp import solve_ilp
from utils.distance_utils import build_distance_matrix, tour_length, is_valid_tour


def brute_force_optimal_length(cities):
    """Ham doi chieu doc lap (Ground Truth), khong dung chung code voi ILP,
    de dam bao viec kiem thu la khach quan."""
    n = len(cities)
    dist = build_distance_matrix(cities)
    best = math.inf
    for perm in itertools.permutations(range(1, n)):
        candidate = [0] + list(perm)
        length = tour_length(candidate, dist)
        best = min(best, length)
    return best


class TestILP(unittest.TestCase):

    def setUp(self):
        # Bo 4 diem la 1 hinh vuong, biet truoc nghiem toi uu la chu vi hinh vuong
        self.square = [(0, 0), (0, 10), (10, 10), (10, 0)]

        # Bo 6 diem tong hop, khong theo hinh dang dac biet
        self.six_points = [(0, 0), (2, 4), (5, 2), (7, 6), (3, 8), (8, 1)]

    def test_ilp_runs_without_error(self):
        result = solve_ilp(self.square)
        self.assertIn("tour", result)
        self.assertIn("tour_length", result)
        self.assertIn("status", result)

    def test_ilp_returns_valid_tour(self):
        result = solve_ilp(self.square)
        self.assertTrue(is_valid_tour(result["tour"], len(self.square)))

    def test_ilp_tour_length_matches_recomputation(self):
        result = solve_ilp(self.square)
        dist = build_distance_matrix(self.square)
        recomputed = tour_length(result["tour"], dist)
        self.assertAlmostEqual(result["tour_length"], recomputed, places=6)

    def test_ilp_optimal_on_square(self):
        # Nghiem toi uu cua hinh vuong canh 10 la di theo chu vi: 4 x 10 = 40
        result = solve_ilp(self.square)
        self.assertEqual(result["status"], "Optimal")
        self.assertAlmostEqual(result["tour_length"], 40.0, places=3)

    def test_ilp_matches_brute_force_ground_truth(self):
        expected = brute_force_optimal_length(self.six_points)
        result = solve_ilp(self.six_points)
        self.assertEqual(result["status"], "Optimal")
        self.assertAlmostEqual(result["tour_length"], expected, places=3)


if __name__ == "__main__":
    unittest.main()
