import math
import random
 
 
# ---------------------------------------------------------
# Hàm tiện ích: tính khoảng cách và tổng chi phí hành trình
# ---------------------------------------------------------
 
def euclidean_distance(p1, p2):
    """Tính khoảng cách Euclid giữa 2 điểm (x, y)."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
 
 
def build_distance_matrix(points):
    """Xây dựng ma trận khoảng cách từ danh sách tọa độ điểm."""
    n = len(points)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = euclidean_distance(points[i], points[j])
    return dist
 
 
def tour_length(tour, dist):
    """Tính tổng chi phí của một hành trình khép kín."""
    total = 0.0
    n = len(tour)
    for i in range(n):
        total += dist[tour[i]][tour[(i + 1) % n]]
    return total
 
 
# ---------------------------------------------------------
# Thuật toán Cheapest Insertion
# ---------------------------------------------------------
 
def cheapest_insertion(dist):
    """
    Thuật toán Cheapest Insertion.
 
    dist : ma trận khoảng cách (list[list[float]])
 
    Ý tưởng:
        - Khởi tạo chu trình con bằng cạnh có chi phí nhỏ nhất.
        - Lặp lại: với mỗi thành phố k chưa nằm trong chu trình và mỗi
          cạnh (i, j) hiện có trong chu trình, tính chi phí chèn:
                increase = d(i, k) + d(k, j) - d(i, j)
          Chọn cặp (k, cạnh) có "increase" nhỏ nhất, chèn k vào giữa
          cạnh đó (tức là vào "vị trí lắp đặt rẻ nhất").
 
    Trả về: danh sách chỉ số thành phố theo thứ tự hành trình
    """
    n = len(dist)
 
    # Bước 1: khởi tạo chu trình con bằng cạnh có chi phí nhỏ nhất
    min_dist = float("inf")
    a, b = 0, 1
    for i in range(n):
        for j in range(i + 1, n):
            if dist[i][j] < min_dist:
                min_dist = dist[i][j]
                a, b = i, j
 
    tour = [a, b]
    remaining = set(range(n)) - {a, b}
 
    # Bước 2: lặp lại chèn thành phố vào vị trí có chi phí tăng thêm nhỏ nhất
    while remaining:
        best_increase = float("inf")
        best_city = None
        best_position = None
 
        for k in remaining:
            m = len(tour)
            for pos in range(m):
                i = tour[pos]
                j = tour[(pos + 1) % m]
                increase = dist[i][k] + dist[k][j] - dist[i][j]
                if increase < best_increase:
                    best_increase = increase
                    best_city = k
                    best_position = pos + 1
 
        tour.insert(best_position, best_city)
        remaining.remove(best_city)
 
    return tour
 
 
# ---------------------------------------------------------
# Chạy thử nghiệm
# ---------------------------------------------------------
 
def print_tour(name, tour, dist):
    length = tour_length(tour, dist)
    path_str = " -> ".join(str(c) for c in tour) + f" -> {tour[0]}"
    print(f"[{name}]")
    print(f"  Hành trình: {path_str}")
    print(f"  Tổng chi phí: {length:.2f}")
    print()
 
 
def main():
    random.seed(42)
 
    # Sinh ngẫu nhiên n thành phố với tọa độ (x, y) trong khoảng [0, 100]
    n = 10
    points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
 
    print("Danh sách tọa độ thành phố:")
    for idx, p in enumerate(points):
        print(f"  Thành phố {idx}: ({p[0]:.2f}, {p[1]:.2f})")
    print()
 
    dist = build_distance_matrix(points)
 
    # Cheapest Insertion
    ci_tour = cheapest_insertion(dist)
    print_tour("Cheapest Insertion", ci_tour, dist)
 
 
if __name__ == "__main__":
    main()
