"""
Branch and Bound cho TSP.

Nguyên lý: xây dựng cây tìm kiếm các tuyến đường có thể, dùng "cận dưới" (lower bound)
để cắt bỏ (prune) sớm các nhánh không thể tốt hơn lời giải tốt nhất đã tìm được,
tránh phải duyệt hết O(n!) khả năng như Brute Force.

Độ phức tạp thời gian: O(n!) trong trường hợp xấu nhất, nhưng thực tế nhanh hơn
Brute Force rất nhiều nhờ cắt tỉa. Khả thi với n <= 15-20 tùy dữ liệu.
"""
import time

try:
    from .utils import load_cities, build_distance_matrix
except ImportError:
    from utils import load_cities, build_distance_matrix


def _bound(distance_matrix, path, visited, n):
    """Cận dưới đơn giản: chi phí hiện tại + cạnh nhỏ nhất còn lại cho mỗi thành phố chưa thăm."""
    bound = 0
    for i in range(len(path) - 1):
        bound += distance_matrix[path[i], path[i + 1]]

    last = path[-1]
    # cộng thêm cạnh rẻ nhất nối từ mỗi thành phố chưa thăm (ước lượng lạc quan)
    for i in range(n):
        if not visited[i]:
            min_edge = min(
                distance_matrix[i, j] for j in range(n) if j != i
            )
            bound += min_edge
    return bound


def solve(distance_matrix):
    n = len(distance_matrix)
    start = time.perf_counter()

    best_route = [None]
    best_cost = [float("inf")]

    def branch(path, visited, cost):
        if len(path) == n:
            total = cost + distance_matrix[path[-1], path[0]]
            if total < best_cost[0]:
                best_cost[0] = total
                best_route[0] = path.copy()
            return

        for city in range(n):
            if visited[city]:
                continue
            new_cost = cost + distance_matrix[path[-1], city]
            if new_cost >= best_cost[0]:
                continue  # cắt tỉa: không thể tốt hơn lời giải hiện tại
            visited[city] = True
            path.append(city)
            branch(path, visited, new_cost)
            path.pop()
            visited[city] = False

    visited = [False] * n
    visited[0] = True
    branch([0], visited, 0)

    runtime = time.perf_counter() - start
    return best_route[0], best_cost[0], runtime


if __name__ == "__main__":
    coords = load_cities("data/sample_10.txt" if __package__ else "../data/sample_10.txt")
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = solve(dist_matrix)
    print(f"Route: {route}")
    print(f"Total distance: {dist:.2f}")
    print(f"Runtime: {runtime:.4f}s")
