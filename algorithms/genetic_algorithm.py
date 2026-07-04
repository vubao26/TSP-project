"""
Genetic Algorithm (Thuật toán di truyền) cho TSP.

Nguyên lý: mô phỏng quá trình tiến hóa tự nhiên
- Khởi tạo quần thể (population) gồm nhiều tuyến đường ngẫu nhiên
- Chọn lọc (selection) các cá thể tốt (tuyến đường ngắn)
- Lai ghép (crossover - Order Crossover) tạo cá thể con
- Đột biến (mutation - hoán đổi 2 thành phố) để tránh hội tụ sớm
- Lặp qua nhiều thế hệ (generations)

Độ phức tạp thời gian: O(generations * population_size * n)
Đây là thuật toán heuristic: không đảm bảo tối ưu nhưng cho kết quả tốt trong
thời gian hợp lý ngay cả với n lớn (hàng trăm, hàng nghìn thành phố).
"""
import time
import random

try:
    from .utils import load_cities, build_distance_matrix, route_length
except ImportError:
    from utils import load_cities, build_distance_matrix, route_length


def _create_route(n):
    route = list(range(n))
    random.shuffle(route)
    return route


def _order_crossover(parent1, parent2):
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[start:end] = parent1[start:end]
    fill_values = [c for c in parent2 if c not in child]
    idx = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill_values[idx]
            idx += 1
    return child


def _mutate(route, mutation_rate=0.02):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randrange(len(route))
            route[i], route[j] = route[j], route[i]
    return route


def solve(distance_matrix, population_size=100, generations=300, mutation_rate=0.02, elite_size=10, seed=None):
    if seed is not None:
        random.seed(seed)

    n = len(distance_matrix)
    start = time.perf_counter()

    population = [_create_route(n) for _ in range(population_size)]

    best_route = None
    best_distance = float("inf")

    for _gen in range(generations):
        scored = [(route_length(r, distance_matrix), r) for r in population]
        scored.sort(key=lambda x: x[0])

        if scored[0][0] < best_distance:
            best_distance, best_route = scored[0]

        # Elitism: giữ lại các cá thể tốt nhất
        new_population = [r for _, r in scored[:elite_size]]

        # Sinh cá thể con bằng crossover + mutation cho đến khi đủ quần thể
        while len(new_population) < population_size:
            parent1 = random.choice(scored[:population_size // 2])[1]
            parent2 = random.choice(scored[:population_size // 2])[1]
            child = _order_crossover(parent1, parent2)
            child = _mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

    runtime = time.perf_counter() - start
    return best_route, best_distance, runtime


if __name__ == "__main__":
    coords = load_cities("data/sample_10.txt" if __package__ else "../data/sample_10.txt")
    dist_matrix = build_distance_matrix(coords)
    route, dist, runtime = solve(dist_matrix, seed=42)
    print(f"Route: {route}")
    print(f"Total distance: {dist:.2f}")
    print(f"Runtime: {runtime:.4f}s")
