
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
# Thuật toán Nearest Neighbor
# ---------------------------------------------------------
 
def nearest_neighbor(dist, start=0):
    """
    Thuật toán Nearest Neighbor.
 
    dist  : ma trận khoảng cách (list[list[float]])
    start : chỉ số thành phố xuất phát
 
    Trả về: danh sách chỉ số thành phố theo thứ tự hành trình
    """
    n = len(dist)
    visited = [False] * n
    tour = [start]
    visited[start] = True
    current = start
 
    for _ in range(n - 1):
        nearest_city = None
        nearest_dist = float("inf")
        for j in range(n):
            if not visited[j] and dist[current][j] < nearest_dist:
                nearest_dist = dist[current][j]
                nearest_city = j
        tour.append(nearest_city)
        visited[nearest_city] = True
        current = nearest_city
 
    return tour
 
 
def nearest_neighbor_best_start(dist):
    """Chạy Nearest Neighbor với mọi điểm xuất phát, trả về hành trình tốt nhất."""
    n = len(dist)
    best_tour = None
    best_len = float("inf")
    for start in range(n):
        tour = nearest_neighbor(dist, start)
        length = tour_length(tour, dist)
        if length < best_len:
            best_len = length
            best_tour = tour
    return best_tour, best_len
