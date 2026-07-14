"""
two_opt.py

Cai dat thuat toan 2-opt (Local Search) cho bai toan TSP, dung nhu y tuong
va pseudocode da trinh bay trong tai lieu nghien cuu cua Member C:
    - Xuat phat tu mot tour kha thi ban dau.
    - Lap lai viec quet cac cap canh, hoan doi (swap) canh neu lam giam
      tong chieu dai (delta < 0), cho den khi khong con cai thien duoc nua.

Khong hard-code du lieu thanh pho: tat ca deu nhan vao qua tham so.
"""

from __future__ import annotations
from typing import List, Tuple, Sequence, Dict, Any, Optional

from utils.distance_utils import build_distance_matrix, tour_length, is_valid_tour

Coordinate = Tuple[float, float]


def nearest_neighbor_initial_tour(
    dist: Sequence[Sequence[float]],
    start: int = 0,
) -> List[int]:
    """
    Tao tour khoi tao bang Nearest Neighbor, dung lam dau vao cho 2-opt
    khi nguoi dung khong tu cung cap initial_tour.

    Args:
        dist: ma tran khoang cach.
        start: thanh pho xuat phat.

    Returns:
        Tour khoi tao (list[int]).
    """
    n = len(dist)
    visited = [False] * n
    visited[start] = True
    tour = [start]
    current = start

    for _ in range(n - 1):
        next_city = min(
            (j for j in range(n) if not visited[j]),
            key=lambda j: dist[current][j],
        )
        tour.append(next_city)
        visited[next_city] = True
        current = next_city

    return tour


def _two_opt_swap(tour: List[int], i: int, j: int) -> List[int]:
    """
    Thuc hien mot phep 2-opt move: dao nguoc doan tour[i+1 .. j].

    Args:
        tour: tour hien tai.
        i, j: chi so hai canh duoc chon de hoan doi (i < j).

    Returns:
        Tour moi sau khi dao doan.
    """
    return tour[:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]


def two_opt(
    cities: Sequence[Coordinate],
    initial_tour: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """
    Cai thien mot tour bang thuat toan 2-opt cho den khi dat toi uu cuc bo.

    Args:
        cities: danh sach toa do (x, y) cua cac thanh pho.
        initial_tour: tour khoi tao (neu None, tu dong sinh bang Nearest Neighbor).

    Returns:
        dict gom:
            "tour": tour toi uu cuc bo tim duoc (list[int]),
            "tour_length": tong chieu dai chu trinh (float),
            "initial_tour_length": chieu dai tour khoi tao, de doi chieu muc cai thien,
            "iterations": so lan swap da thuc hien.
    """
    n = len(cities)
    if n < 4:
        raise ValueError("2-opt can it nhat 4 thanh pho de co the hoan doi canh.")

    dist = build_distance_matrix(cities)

    tour = list(initial_tour) if initial_tour is not None else nearest_neighbor_initial_tour(dist)
    if not is_valid_tour(tour, n):
        raise ValueError("initial_tour khong hop le: phai chua dung n thanh pho, khong lap.")

    initial_length = tour_length(tour, dist)

    improved = True
    iterations = 0

    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                # Bo qua cap canh ke nhau tai vi tri dau/cuoi (khong tao ra thay doi thuc su)
                if i == 0 and j == n - 1:
                    continue

                a, b = tour[i], tour[i + 1]
                c, d = tour[j], tour[(j + 1) % n]

                delta = (dist[a][c] + dist[b][d]) - (dist[a][b] + dist[c][d])

                if delta < -1e-9:  # dung nguong nho de tranh sai so so thuc
                    tour = _two_opt_swap(tour, i, j)
                    improved = True
                    iterations += 1

    final_length = tour_length(tour, dist)

    return {
        "tour": tour,
        "tour_length": final_length,
        "initial_tour_length": initial_length,
        "iterations": iterations,
    }
