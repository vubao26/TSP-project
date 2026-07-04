"""
Script chạy và so sánh tất cả các thuật toán trên cùng 1 bộ dữ liệu.

Cách dùng:
    python benchmark.py --data data/sample_10.txt
    python benchmark.py --data data/sample_10.txt --skip brute_force,branch_and_bound

Lưu ý: Brute Force và Branch and Bound rất chậm với n lớn (>12-15), nên có thể
dùng --skip để bỏ qua khi test với bộ dữ liệu lớn.
"""
import argparse
import csv
import os

from algorithms.utils import load_cities, build_distance_matrix
from algorithms import brute_force, dynamic_programming, nearest_neighbor
from algorithms import branch_and_bound, genetic_algorithm, aco

ALGORITHMS = {
    "brute_force": brute_force.solve,
    "dynamic_programming": dynamic_programming.solve,
    "nearest_neighbor": nearest_neighbor.solve,
    "branch_and_bound": branch_and_bound.solve,
    "genetic_algorithm": genetic_algorithm.solve,
    "aco": aco.solve,
}


def main():
    parser = argparse.ArgumentParser(description="So sánh các thuật toán giải TSP")
    parser.add_argument("--data", required=True, help="Đường dẫn file dữ liệu thành phố")
    parser.add_argument("--skip", default="", help="Danh sách thuật toán bỏ qua, cách nhau bởi dấu phẩy")
    parser.add_argument("--output", default="results/benchmark_results.csv", help="File CSV kết quả")
    args = parser.parse_args()

    skip_set = {s.strip() for s in args.skip.split(",") if s.strip()}

    coords = load_cities(args.data)
    dist_matrix = build_distance_matrix(coords)
    n = len(coords)
    print(f"Số thành phố: {n}\n")

    results = []
    for name, func in ALGORITHMS.items():
        if name in skip_set:
            print(f"[BỎ QUA] {name}")
            continue
        print(f"[ĐANG CHẠY] {name} ...")
        try:
            route, distance, runtime = func(dist_matrix)
            print(f"  -> Khoảng cách: {distance:.2f} | Thời gian: {runtime:.4f}s")
            results.append({
                "algorithm": name,
                "num_cities": n,
                "total_distance": round(distance, 4),
                "runtime_seconds": round(runtime, 6),
                "route": " ".join(map(str, route)),
            })
        except Exception as e:
            print(f"  -> LỖI: {e}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["algorithm", "num_cities", "total_distance", "runtime_seconds", "route"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nĐã lưu kết quả vào: {args.output}")


if __name__ == "__main__":
    main()
