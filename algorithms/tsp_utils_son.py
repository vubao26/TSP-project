import numpy as np
import math
import os

def load_file_content(file_path):
    """Đọc nội dung từ một file vật lý."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_tsp_file(file_content):
    """Đọc dữ liệu tọa độ từ file .tsp (Hỗ trợ EUC_2D và GEO)."""
    lines = file_content.strip().split('\n')
    coords = {}
    edge_weight_type = "EUC_2D"
    node_section = False
    
    for line in lines:
        line = line.strip()
        if not line: continue
        if "EDGE_WEIGHT_TYPE" in line:
            parts = line.split(":")
            edge_weight_type = parts[1].strip() if len(parts) > 1 else line.split()[-1]
        elif "NODE_COORD_SECTION" in line:
            node_section = True
            continue
        elif "EOF" in line: break
        
        if node_section:
            parts = line.split()
            if len(parts) >= 3:
                idx = int(parts[0]) - 1
                coords[idx] = (float(parts[1]), float(parts[2]))
    return coords, edge_weight_type

def parse_opt_tour(tour_content):
    """Đọc chu trình tối ưu từ file .opt.tour."""
    lines = tour_content.strip().split('\n')
    tour = []
    tour_section = False
    for line in lines:
        line = line.strip()
        if not line: continue
        if "TOUR_SECTION" in line:
            tour_section = True
            continue
        if "EOF" in line: break
        if tour_section:
            for node in line.split():
                if node == "-1": break
                tour.append(int(node) - 1)
    return tour

def calculate_distance_matrix(coords, edge_weight_type):
    """Tính toán ma trận khoảng cách dựa trên cấu hình hệ tọa độ."""
    n = len(coords)
    dist_matrix = np.zeros((n, n))
    
    if edge_weight_type == "GEO":
        def get_lat_lon(coord):
            deg = int(coord)
            min_val = coord - deg
            return math.pi * (deg + 5.0 * min_val / 3.0) / 180.0
            
        lat = {i: get_lat_lon(coords[i][0]) for i in range(n)}
        lon = {i: get_lat_lon(coords[i][1]) for i in range(n)}
        RRR = 6378.388
        for i in range(n):
            for j in range(n):
                if i == j: continue
                q1 = math.cos(lon[i] - lon[j])
                q2 = math.cos(lat[i] - lat[j])
                q3 = math.cos(lat[i] + lat[j])
                dist = int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
                dist_matrix[i][j] = dist
    else:
        for i in range(n):
            for j in range(n):
                if i == j: continue
                xd = coords[i][0] - coords[j][0]
                yd = coords[i][1] - coords[j][1]
                dist = int(math.sqrt(xd*xd + yd*yd) + 0.5)
                dist_matrix[i][j] = dist
    return dist_matrix

def compute_tour_length(tour, dist_matrix):
    """Tính tổng độ dài của chu trình."""
    length = 0
    n = len(tour)
    for i in range(n):
        length += dist_matrix[tour[i]][tour[(i + 1) % n]]
    return length