import math
import random
from tsp_utils_son import compute_tour_length

def simulated_annealing(dist_matrix, t0=1500, alpha=0.97, t_min=0.001, max_iter=400):
    """Thuật toán Mô phỏng luyện kim giải bài toán TSP."""
    n = len(dist_matrix)
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_len = compute_tour_length(current_tour, dist_matrix)
    
    best_tour = list(current_tour)
    best_len = current_len
    t = t0
    
    while t > t_min:
        for _ in range(max_iter):
            # Toán tử biến đổi cấu trúc lân cận 2-opt
            i, j = sorted(random.sample(range(n), 2))
            new_tour = current_tour.copy()
            new_tour[i:j+1] = reversed(new_tour[i:j+1])
            
            new_len = compute_tour_length(new_tour, dist_matrix)
            delta = new_len - current_len
            
            # Tiêu chuẩn Metropolis điều kiện nhận nghiệm tệ hơn
            if delta < 0 or random.random() < math.exp(-delta / t):
                current_tour = new_tour
                current_len = new_len
                if current_len < best_len:
                    best_tour = list(current_tour)
                    best_len = current_len
        t *= alpha  # Hạ nhiệt độ
    return best_tour, {"t0": t0, "alpha": alpha}