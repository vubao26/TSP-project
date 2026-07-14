"""
ilp.py

Cai dat thuat toan ILP (Integer Linear Programming) cho bai toan TSP,
su dung thu vien PuLP va cong thuc MTZ (Miller-Tucker-Zemlin) de loai bo
chu trinh con (Subtour Elimination), dung nhu mo hinh toan hoc da trinh bay
trong tai lieu nghien cuu cua Member C.

Luu y:
    - Day la ban ILP "don gian", chi khuyen dung cho n <= 12 thanh pho
      (dung de doi chieu nghiem toi uu, KHONG dung de benchmark tren du lieu lon).
    - Khong hard-code du lieu thanh pho: tat ca deu nhan vao qua tham so "cities".
"""

from __future__ import annotations
from typing import List, Tuple, Sequence, Dict, Any, Optional

import pulp

from utils.distance_utils import build_distance_matrix, tour_length, is_valid_tour

Coordinate = Tuple[float, float]

# Nguong khuyen cao, chi mang tinh canh bao (khong chan cung) vi ILP se rat cham voi n lon.
RECOMMENDED_MAX_CITIES = 12


def _build_mtz_model(dist: Sequence[Sequence[float]], n: int) -> Tuple[pulp.LpProblem, Dict, Dict]:
    """
    Xay dung mo hinh ILP (MTZ) tu ma tran khoang cach.

    Args:
        dist: ma tran khoang cach n x n.
        n: so thanh pho.

    Returns:
        (model, x, u): bai toan PuLP, bien quyet dinh x[i,j], bien phu u[i].
    """
    model = pulp.LpProblem("TSP_ILP_MTZ", pulp.LpMinimize)

    # Bien quyet dinh: x[i, j] = 1 neu di truc tiep tu i den j
    x = {
        (i, j): pulp.LpVariable(f"x_{i}_{j}", cat="Binary")
        for i in range(n) for j in range(n) if i != j
    }

    # Bien phu MTZ: u[i] bieu dien thu tu tham thanh pho i (i = 1..n-1, thanh pho 0 co dinh la goc)
    u = {i: pulp.LpVariable(f"u_{i}", lowBound=1, upBound=n - 1, cat="Integer")
         for i in range(1, n)}

    # Ham muc tieu: minimize tong chi phi cac canh duoc chon
    model += pulp.lpSum(dist[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j)

    # Rang buoc bac ra: moi thanh pho roi di dung mot lan
    for i in range(n):
        model += pulp.lpSum(x[i, j] for j in range(n) if j != i) == 1, f"out_degree_{i}"

    # Rang buoc bac vao: moi thanh pho duoc den dung mot lan
    for j in range(n):
        model += pulp.lpSum(x[i, j] for i in range(n) if i != j) == 1, f"in_degree_{j}"

    # Rang buoc MTZ loai bo subtour: u_i - u_j + n * x_ij <= n - 1, voi i, j = 1..n-1, i != j
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model += u[i] - u[j] + n * x[i, j] <= n - 1, f"mtz_{i}_{j}"

    return model, x, u


def solve_ilp(
    cities: Sequence[Coordinate],
    time_limit_seconds: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Giai bai toan TSP bang ILP (MTZ formulation), tra ve ket qua theo chuan Output chung.

    Args:
        cities: danh sach toa do (x, y) cua cac thanh pho. KHONG hard-code, phai truyen vao.
        time_limit_seconds: gioi han thoi gian cho solver (None = khong gioi han).

    Returns:
        dict gom:
            "tour": danh sach thu tu thanh pho (list[int]),
            "tour_length": tong chieu dai chu trinh (float),
            "status": trang thai solver ("Optimal", "Infeasible", ...),
    """
    n = len(cities)
    if n < 2:
        raise ValueError("Can it nhat 2 thanh pho de giai TSP.")

    if n > RECOMMENDED_MAX_CITIES:
        # Chi canh bao, khong chan chay, de nguoi dung tu quyet dinh.
        print(
            f"[Canh bao] n = {n} > {RECOMMENDED_MAX_CITIES}. "
            f"ILP (ban don gian) co the rat cham hoac khong hoi tu. "
            f"Chi nen dung ILP de doi chieu nghiem toi uu tren du lieu nho."
        )

    dist = build_distance_matrix(cities)
    model, x, u = _build_mtz_model(dist, n)

    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=time_limit_seconds)
    model.solve(solver)

    status = pulp.LpStatus[model.status]

    tour: List[int] = []
    if status == "Optimal":
        tour = _reconstruct_tour(x, n)

    length = tour_length(tour, dist) if tour else float("inf")

    return {
        "tour": tour,
        "tour_length": length,
        "status": status,
    }


def _reconstruct_tour(x: Dict[Tuple[int, int], pulp.LpVariable], n: int) -> List[int]:
    """
    Xay dung lai tour (danh sach thu tu thanh pho) tu gia tri bien x[i, j] sau khi giai.

    Args:
        x: bien quyet dinh da duoc solver gan gia tri.
        n: so thanh pho.

    Returns:
        Danh sach thu tu thanh pho, bat dau tu thanh pho 0.
    """
    # Xay dung ban do "thanh pho tiep theo" tu cac canh duoc chon (x_ij = 1)
    next_city = {}
    for (i, j), var in x.items():
        if var.value() is not None and var.value() > 0.5:
            next_city[i] = j

    tour = [0]
    current = 0
    for _ in range(n - 1):
        current = next_city[current]
        tour.append(current)

    return tour
