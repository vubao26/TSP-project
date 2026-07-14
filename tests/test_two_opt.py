"""
test_two_opt.py

Unit test cho module 2-opt (algorithms/two_opt.py), theo dung Buoc 5 - 6 cua Giai doan 2:
    - Thuat toan chay dung, khong loi.
    - Tour hop le (di qua du thanh pho, khong lap, quay ve diem xuat phat).
    - Tour Length tinh dung.
    - 2-opt phai cai thien (hoac it nhat khong lam xau hon) so voi tour khoi tao tu Nearest Neighbor.

Dataset dung de test: burma14-style (tong hop nho) va mot bo du lieu lon hon (14 diem ngau nhien)
de mo phong quy mo cua burma14 (14 thanh pho) theo dung dataset chuan cua du an.
"""

import random
import unittest

from algorithms.two_opt import two_opt, nearest_neighbor_initial_tour
from utils.distance_utils import build_distance_matrix, tour_length, is_valid_tour


class TestTwoOpt(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        # Bo diem nho, hinh dang biet truoc: hinh chu nhat bi "roi loan" thu tu index
        # de kiem tra 2-opt co the sap xep lai dung thu tu hinh hoc.
        self.messy_rectangle = [(0, 0), (10, 10), (0, 10), (10, 0)]

        # Bo 14 diem ngau nhien, mo phong quy mo dataset burma14 (14 thanh pho)
        self.random_14 = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(14)]

    def test_two_opt_runs_without_error(self):
        result = two_opt(self.messy_rectangle)
        self.assertIn("tour", result)
        self.assertIn("tour_length", result)

    def test_two_opt_returns_valid_tour(self):
        result = two_opt(self.messy_rectangle)
        self.assertTrue(is_valid_tour(result["tour"], len(self.messy_rectangle)))

    def test_two_opt_tour_length_matches_recomputation(self):
        result = two_opt(self.messy_rectangle)
        dist = build_distance_matrix(self.messy_rectangle)
        recomputed = tour_length(result["tour"], dist)
        self.assertAlmostEqual(result["tour_length"], recomputed, places=6)

    def test_two_opt_fixes_crossing_edges(self):
        # Voi thu tu bi roi loan (0,0)->(10,10)->(0,10)->(10,0), 2 canh bi cat cheo nhau.
        # 2-opt phai sua ve chu vi hinh chu nhat: 4 canh x 10 = 40 (di theo canh, khong theo duong cheo).
        result = two_opt(self.messy_rectangle, initial_tour=[0, 1, 2, 3])
        self.assertAlmostEqual(result["tour_length"], 40.0, places=3)

    def test_two_opt_improves_or_equals_nearest_neighbor(self):
        dist = build_distance_matrix(self.random_14)
        nn_tour = nearest_neighbor_initial_tour(dist)
        nn_length = tour_length(nn_tour, dist)

        result = two_opt(self.random_14, initial_tour=nn_tour)

        self.assertLessEqual(result["tour_length"], nn_length + 1e-9)
        self.assertEqual(result["initial_tour_length"], nn_length)

    def test_two_opt_raises_on_invalid_initial_tour(self):
        with self.assertRaises(ValueError):
            two_opt(self.messy_rectangle, initial_tour=[0, 1, 1, 2])  # lap thanh pho 1


if __name__ == "__main__":
    unittest.main()
