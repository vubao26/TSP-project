"""
Ant Colony Optimization (ACO - Tối ưu đàn kiến) cho TSP.

Nguyên lý: mô phỏng cách đàn kiến tìm đường đi ngắn nhất bằng vệt pheromone
- Mỗi "kiến" xây dựng 1 tuyến đường, xác suất chọn cạnh tiếp theo phụ thuộc vào
  lượng pheromone trên cạnh đó và độ ngắn của cạnh (heuristic 1/distance).
- Sau mỗi vòng lặp (iteration), pheromone bay hơi (evaporation) và được cập nhật
  thêm dựa trên chất lượng các tuyến đường vừa tìm được.

Độ phức tạp thời gian: O(iterations * num_ants * n^2)
Đây cũng là thuật toán heuristic, phù hợp cho bài toán kích thước lớn.
"""
import time
import random

try:
    from .utils import load_cities, build_distance_matrix, route_length
except ImportError:
    from utils import load_cities, build_distance_matrix, route_length


def solve(distance_matrix, num_ants=20, iterations=100, alpha=1.0, beta=3.0,
          evaporation_rate=0.5, q=100.0, seed=None):
    """
    alpha: mức độ ảnh hưởng của pheromone
    beta: mức độ ảnh hưởng của thông tin heuristic (1/khoảng cách)
    evaporation_rate: tốc độ bay hơi pheromone (0-1)
    q: hằng số dùng để cập nhật lượng pheromone mới
    """
    if seed is not None:
        random.seed(seed)

    n = len(distance_matrix)
    start = time.perf_counter()

    pheromone = [[1.0 for _ in range(n)] for _ in range(n)]
    best_route, best_distance = None, float("inf")

    # Tránh chia cho 0 trên đường chéo
    eta = [[1.0 / distance_matrix[i, j] if i != j else 0 for j in range(n)] for i in range(n)]

    for _iteration in range(iterations):
        all_routes = []
        for _ant in range(num_ants):
            visited = [False] * n
            current = random.randrange(n)
            visited[current] = True
            route = [current]

            for _ in range(n - 1):
                probs = []
                for j in range(n):
                    if visited[j]:
                        probs.append(0)
                    else:
                        probs.append((pheromone[current][j] ** alpha) * (eta[current][j] ** beta))

                total = sum(probs)
                if total == 0:
                    # fallback: chọn ngẫu nhiên thành phố chưa thăm
                    candidates = [j for j in range(n) if not visited[j]]
                    next_city = random.choice(candidates)
                else:
                    r = random.uniform(0, total)
                    cumulative = 0
                    next_city = None
                    for j in range(n):
                        cumulative += probs[j]
                        if cumulative >= r:
                            next_city = j
                            break
                    if next_city is None:
                        next_city = next(j for j in range(n) if not visited[j])

                route.append(next_city)
                visited[next_city] = True
                current = next_city

            dist = route_length(route, distance_matrix)
            all_routes.append((route, dist))
            if dist < best_distance:
                best_distance, best_route = dist, route

        # Bay hơi pheromone
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1 - evaporation_rate)

        # Cập nhật pheromone dựa trên các tuyến đường vừa đi
        for route, dist in all_routes:
            deposit = q / dist
            for i in range(len(route)):
                a, b = route[i], route[(i + 1) % len(route)]
                pheromone[a][b] += deposit
                pheromone[b][a] += deposit

    runtime = time.perf_counter() - start
    return best_route, best_distance, runtime


if __name__ == "__main__":
    coords = load_cities("data/sample_10.txt" if __package__ else "../data/sample_10.txt")
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = solve(dist_matrix, seed=42)
    print(f"Route: {route}")
    print(f"Total distance: {dist:.2f}")
    print(f"Runtime: {runtime:.4f}s")
