from tsp_utils_son import (
    load_file_content, 
    parse_tsp_file, 
    parse_opt_tour, 
    calculate_distance_matrix, 
    compute_tour_length
)
from simulated_annealing import simulated_annealing
from genetic_algorithm import genetic_algorithm

if __name__ == "__main__":
    # Danh sách dữ liệu cấu hình chạy thực nghiệm
    file_names = ["burma14", "berlin52", "st70", "kroA100"]
    
    print("=" * 88)
    print(f"{'Bộ Dữ Liệu':<12} | {'Tối ưu Gốc':<12} | {'Kết quả SA':<12} | {'Gap SA (%)':<12} | {'Kết quả GA':<12} | {'Gap GA (%)':<12}")
    print("=" * 88)
    
    for name in file_names:
        # Đọc dữ liệu đầu vào của đồ thị .tsp
        tsp_content = load_file_content(f"Datasets/{name}.tsp")
        if not tsp_content:
            print(f"Không tìm thấy file {name}.tsp, bỏ qua...")
            continue
            
        coords, weight_type = parse_tsp_file(tsp_content)
        dist_matrix = calculate_distance_matrix(coords, weight_type)
        
        # Kiểm tra và nạp file lời giải tối ưu .opt.tour (nếu có)
        opt_content = load_file_content(f"Datasets/{name}.opt.tour")
        if opt_content:
            opt_tour = parse_opt_tour(opt_content)
            opt_len = compute_tour_length(opt_tour, dist_matrix)
            opt_str = f"{opt_len:.0f}"
        else:
            opt_len = None
            opt_str = "Chưa có"
            
        # Thực thi thuật toán Simulated Annealing và tự tính độ dài chu trình
        sa_tour, _ = simulated_annealing(dist_matrix, t0=1500, alpha=0.97, max_iter=300)
        sa_best_len = compute_tour_length(sa_tour, dist_matrix)
        sa_gap_str = f"{((sa_best_len - opt_len) / opt_len * 100):.2f}%" if opt_len else "N/A"
        
        # Thực thi thuật toán Genetic Algorithm và tự tính độ dài chu trình
        ga_tour, _ = genetic_algorithm(dist_matrix, pop_size=100, generations=300)
        ga_best_len = compute_tour_length(ga_tour, dist_matrix)
        ga_gap_str = f"{((ga_best_len - opt_len) / opt_len * 100):.2f}%" if opt_len else "N/A"

        # In dòng kết quả của bộ dữ liệu hiện tại ra bảng công khai
        print(f"{name:<12} | {opt_str:<12} | {sa_best_len:<12.1f} | {sa_gap_str:<12} | {ga_best_len:<12.1f} | {ga_gap_str:<12}")

        # In dòng kết quả của bộ dữ liệu hiện tại ra bảng
        print(f"{name:<12} | {opt_str:<12} | {sa_best_len:<12.1f} | {sa_gap_str:<12} | {ga_best_len:<12.1f} | {ga_gap_str:<12}")

        # In dòng kết quả của bộ dữ liệu hiện tại
        print(f"{name:<12} | {opt_str:<12} | {sa_best_len:<12.1f} | {sa_gap_str:<12} | {ga_best_len:<12.1f} | {ga_gap_str:<12}")
    print("=" * 88)