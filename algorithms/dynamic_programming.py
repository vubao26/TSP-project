"""
Dynamic Programming - thuật toán Held-Karp cho TSP.

Nguyên lý: dùng bitmask để biểu diễn tập thành phố đã thăm, dp[mask][i] = độ dài
đường đi ngắn nhất bắt đầu từ thành phố 0, thăm đúng các thành phố trong `mask`,
kết thúc tại thành phố i.

Độ phức tạp thời gian: O(n^2 * 2^n) -> khả thi với n <= 18-20.
Độ phức tạp không gian: O(n * 2^n)
"""
import time

try:
    from .utils import load_cities, build_distance_matrix
except ImportError:
    from utils import load_cities, build_distance_matrix


def solve(distance_matrix):
    n = len(distance_matrix)
    start = time.perf_counter()

    # dp[mask][i]: chi phí nhỏ nhất đi từ thành phố 0, thăm tập `mask`, kết thúc tại i
    dp = [[float("inf")] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0  # chỉ thăm thành phố 0

    for mask in range(1 << n):
        for i in range(n):
            if dp[mask][i] == float("inf") or not (mask & (1 << i)):
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue  # đã thăm rồi
                next_mask = mask | (1 << j)
                new_cost = dp[mask][i] + distance_matrix[i, j]
                if new_cost < dp[next_mask][j]:
                    dp[next_mask][j] = new_cost
                    parent[next_mask][j] = i

    full_mask = (1 << n) - 1
    best_cost = float("inf")
    last_city = -1
    for i in range(1, n):
        cost = dp[full_mask][i] + distance_matrix[i, 0]
        if cost < best_cost:
            best_cost = cost
            last_city = i

    # Truy vết đường đi
    route = []
    mask = full_mask
    city = last_city
    while city != -1:
        route.append(city)
        prev_city = parent[mask][city]
        mask ^= (1 << city)
        city = prev_city
    route.reverse()

    runtime = time.perf_counter() - start
    return route, best_cost, runtime


if __name__ == "__main__":
    coords = load_cities("data/sample_10.txt" if __package__ else "../data/sample_10.txt")
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = solve(dist_matrix)
    print(f"Route: {route}")
    print(f"Total distance: {dist:.2f}")
    print(f"Runtime: {runtime:.4f}s")
