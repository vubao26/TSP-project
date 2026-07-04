"""
Nearest Neighbor (Tham lam) cho TSP.

Nguyên lý: bắt đầu từ 1 thành phố, luôn chọn thành phố gần nhất chưa thăm để đi tới,
lặp lại đến khi thăm hết tất cả thành phố.

Độ phức tạp thời gian: O(n^2)
Độ phức tạp không gian: O(n)

Ưu điểm: rất nhanh. Nhược điểm: kết quả thường không tối ưu (có thể lệch 20-30%
so với lời giải tối ưu).
"""
import time

try:
    from .utils import load_cities, build_distance_matrix, route_length
except ImportError:
    from utils import load_cities, build_distance_matrix, route_length


def solve(distance_matrix, start_city=0):
    n = len(distance_matrix)
    start = time.perf_counter()

    visited = [False] * n
    route = [start_city]
    visited[start_city] = True
    current = start_city

    for _ in range(n - 1):
        nearest, nearest_dist = -1, float("inf")
        for j in range(n):
            if not visited[j] and distance_matrix[current, j] < nearest_dist:
                nearest, nearest_dist = j, distance_matrix[current, j]
        route.append(nearest)
        visited[nearest] = True
        current = nearest

    runtime = time.perf_counter() - start
    total_distance = route_length(route, distance_matrix)
    return route, total_distance, runtime


if __name__ == "__main__":
    coords = load_cities("data/sample_10.txt" if __package__ else "../data/sample_10.txt")
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = solve(dist_matrix)
    print(f"Route: {route}")
    print(f"Total distance: {dist:.2f}")
    print(f"Runtime: {runtime:.4f}s")
