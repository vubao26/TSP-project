"""
distance_utils.py

Cac ham dung chung de:
    - Xay dung ma tran khoang cach tu danh sach toa do (Euclidean 2D).
    - Tinh tong chieu dai cua mot tour.
    - Kiem tra tinh hop le cua mot tour (di qua du thanh pho, khong lap, quay ve diem xuat phat).

Module nay khong hard-code bat ky du lieu thanh pho nao; tat ca deu nhan vao qua tham so.
"""

from __future__ import annotations
import math
from typing import List, Tuple, Sequence

Coordinate = Tuple[float, float]


def build_distance_matrix(cities: Sequence[Coordinate]) -> List[List[float]]:
    """
    Xay dung ma tran khoang cach Euclid tu danh sach toa do (x, y).

    Args:
        cities: danh sach toa do [(x0, y0), (x1, y1), ...]

    Returns:
        Ma tran khoang cach n x n (list of list), dist[i][j] = khoang cach tu i den j.
    """
    n = len(cities)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = cities[i]
        for j in range(n):
            if i == j:
                continue
            xj, yj = cities[j]
            dist[i][j] = math.hypot(xi - xj, yi - yj)
    return dist


def tour_length(tour: Sequence[int], dist_matrix: Sequence[Sequence[float]]) -> float:
    """
    Tinh tong chieu dai cua mot tour (bao gom canh quay ve diem xuat phat).

    Args:
        tour: danh sach thu tu cac thanh pho, vi du [0, 2, 1, 3] (khong lap lai diem dau).
        dist_matrix: ma tran khoang cach.

    Returns:
        Tong chieu dai chu trinh (float).
    """
    total = 0.0
    n = len(tour)
    for k in range(n):
        i = tour[k]
        j = tour[(k + 1) % n]  # canh cuoi noi ve diem xuat phat
        total += dist_matrix[i][j]
    return total


def is_valid_tour(tour: Sequence[int], n_cities: int) -> bool:
    """
    Kiem tra mot tour co hop le hay khong:
        - Di qua dung n_cities thanh pho.
        - Moi thanh pho xuat hien dung mot lan (khong lap, khong thieu).

    Args:
        tour: danh sach thu tu cac thanh pho.
        n_cities: tong so thanh pho can di qua.

    Returns:
        True neu hop le, False neu nguoc lai.
    """
    if len(tour) != n_cities:
        return False
    return set(tour) == set(range(n_cities))
