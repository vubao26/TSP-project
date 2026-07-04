"""
Brute Force cho TSP.

Nguyên lý: thử tất cả các hoán vị (n-1)! của các thành phố (cố định thành phố 0
làm điểm xuất phát để giảm số hoán vị), chọn tuyến đường có tổng khoảng cách nhỏ nhất.

Độ phức tạp thời gian: O(n!) -> chỉ khả thi với n <= 10-11.
Độ phức tạp không gian: O(n)
"""
import time
from itertools import permutations

try:
    from .utils import load_cities, build_distance_matrix, route_length
except ImportError:
    from utils import load_cities, build_distance_matrix, route_length


def solve(distance_matrix):
    n = len(distance_matrix)
    start = time.perf_counter()

    cities = list(range(1, n))
    best_route = None
    best_distance = float("inf")

    for perm in permutations(cities):
        route = [0] + list(perm)
        dist = route_length(route, distance_matrix)
        if dist < best_distance:
            best_distance = dist
            best_route = route

    runtime = time.perf_counter() - start
    return best_route, best_distance, runtime


if __name__ == "__main__":
    coords = load_cities("data/sample_10.txt" if __package__ else "../data/sample_10.txt")
    # Dùng ít thành phố hơn vì brute force rất chậm, ví dụ 8 thành phố đầu
    coords = coords[:8]
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = solve(dist_matrix)
    print(f"Route: {route}")
    print(f"Total distance: {dist:.2f}")
    print(f"Runtime: {runtime:.4f}s")
