import statistics
from tsp_utils import (
    generate_random_instance,
    read_tsplib,
    compute_distance_matrix,
    take_subinstance,
    print_result,
)
import brute_force
import branch_and_bound


REPEAT = 10   # Theo Experimental Protocol da thong nhat trong nhom


def run_repeated(solve_fn, dist_matrix, repeat=REPEAT):
    runtimes = []
    result = None
    for _ in range(repeat):
        result = solve_fn(dist_matrix)
        runtimes.append(result["runtime"])

    result["runtime"] = statistics.mean(runtimes)   # ghi de bang runtime trung binh
    result["extra"]["runtime_std"] = statistics.stdev(runtimes) if repeat > 1 else 0.0
    result["extra"]["repeat"] = repeat
    return result


def sanity_check_small_instances():
    print("=" * 70)
    print("BUOC 1: SANITY CHECK - Brute Force vs Branch and Bound")
    print("(Ca 2 phai cho ra CUNG 1 tour_length toi uu)")
    print("=" * 70)

    for n in [6, 7, 8, 9]:
        _, dist_matrix = generate_random_instance(n, seed=n)

        bf_result = brute_force.solve(dist_matrix)
        bb_result = branch_and_bound.solve(dist_matrix)

        match = abs(bf_result["tour_length"] - bb_result["tour_length"]) < 1e-6
        status = "KHOP (dung)" if match else "!!! KHONG KHOP - CO LOI !!!"

        print(f"n={n:2d} | Brute Force = {bf_result['tour_length']:10.2f} "
              f"| Branch and Bound = {bb_result['tour_length']:10.2f} | {status}")
    print()


def benchmark_real_dataset(tsp_filepath, sizes=(8, 10, 12)):
    print("=" * 70)
    print(f"BUOC 2: BENCHMARK TREN DU LIEU THUC - {tsp_filepath}")
    print("=" * 70)

    data = read_tsplib(tsp_filepath)
    print(f"Dataset: {data['name']} | Dimension goc: {data['dimension']} "
          f"| Edge type: {data['edge_weight_type']}")
    print()

    for n in sizes:
        sub_coords = take_subinstance(data["coords"], n)
        dist_matrix = compute_distance_matrix(sub_coords, data["edge_weight_type"])

        bf_result = run_repeated(brute_force.solve, dist_matrix)
        bb_result = run_repeated(branch_and_bound.solve, dist_matrix)

        print(f"--- n = {n} (subset dau tien cua {data['name']}) ---")
        print_result(bf_result)
        print_result(bb_result)


def benchmark_bnb_larger(tsp_filepath, sizes=(10, 12, 14)):
    print("=" * 70)
    print(f"BUOC 3: BRANCH AND BOUND VOI n LON HON - {tsp_filepath}")
    print("=" * 70)

    data = read_tsplib(tsp_filepath)

    for n in sizes:
        sub_coords = take_subinstance(data["coords"], n)
        dist_matrix = compute_distance_matrix(sub_coords, data["edge_weight_type"])

        bb_result = run_repeated(branch_and_bound.solve, dist_matrix)
        print_result(bb_result)


if __name__ == "__main__":
    # BUOC 1: bat buoc phai chay va phai "KHOP" truoc khi dung ket qua
    sanity_check_small_instances()

    # BUOC 2 & 3: doi ten file cho dung duong dan dataset cua nhom
    # (vi du: "03_Datasets/burma14.tsp")
    import os
    dataset_path = "dataset TSP/burma14.tsp"

    if os.path.exists(dataset_path):
        benchmark_real_dataset(dataset_path, sizes=(8, 10))
        benchmark_bnb_larger(dataset_path, sizes=(10, 12, 14))
    else:
        print(f"[Bo qua Buoc 2, 3] Khong tim thay file '{dataset_path}'.")
        print("Hay doi 'dataset_path' thanh duong dan thuc te toi burma14.tsp "
              "trong thu muc 03_Datasets/ cua nhom.")