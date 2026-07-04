"""
Các hàm tiện ích dùng chung cho tất cả thuật toán:
- Đọc dữ liệu từ file
- Tính ma trận khoảng cách
- Tính tổng độ dài 1 tuyến đường
"""
import numpy as np


def load_cities(filepath):
    """Đọc file dữ liệu dạng 'id x y' -> trả về mảng tọa độ shape (n, 2)."""
    coords = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            x, y = float(parts[1]), float(parts[2])
            coords.append((x, y))
    return np.array(coords)


def build_distance_matrix(coords):
    """Tính ma trận khoảng cách Euclid giữa các thành phố."""
    n = len(coords)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist[i, j] = np.linalg.norm(coords[i] - coords[j])
    return dist


def route_length(route, distance_matrix):
    """Tính tổng độ dài của 1 tuyến đường (đã bao gồm quay về điểm xuất phát)."""
    total = 0.0
    for i in range(len(route)):
        a, b = route[i], route[(i + 1) % len(route)]
        total += distance_matrix[a, b]
    return total
