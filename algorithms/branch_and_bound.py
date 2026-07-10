import heapq
from typing import List, Tuple, FrozenSet
from tsp_utils import measure_performance

def _prim_mst_cost(nodes, dist_matrix):
    if len(nodes) <= 1:
        return 0.0

    nodes = list(nodes)
    in_mst = {nodes[0]}
    remaining = set(nodes[1:])
    total_cost = 0.0

    while remaining:
        best_edge_cost = float("inf")
        best_v = None
        for u in in_mst:
            for v in remaining:
                if dist_matrix[u][v] < best_edge_cost:
                    best_edge_cost = dist_matrix[u][v]
                    best_v = v
        total_cost += best_edge_cost
        in_mst.add(best_v)
        remaining.remove(best_v)

    return total_cost


def _lower_bound(path, visited_set, dist_matrix, n, start):
    cost_so_far = 0.0
    for i in range(len(path) - 1):
        cost_so_far += dist_matrix[path[i]][path[i + 1]]

    unvisited = [c for c in range(n) if c not in visited_set]

    if not unvisited:
        # Da di het tat ca thanh pho -> chi con canh quay ve diem xuat phat
        return cost_so_far + dist_matrix[path[-1]][start]

    # MST tren (cac thanh pho chua tham quan + thanh pho hien tai)
    mst_nodes = unvisited + [path[-1]]
    mst_cost = _prim_mst_cost(mst_nodes, dist_matrix)

    # Uoc luong them 1 canh re nhat de "dong" chu trinh ve diem xuat phat
    min_return_edge = min(dist_matrix[c][start] for c in unvisited)

    return cost_so_far + mst_cost + min_return_edge


def _branch_and_bound_core(dist_matrix, start=0):
    n = len(dist_matrix)

    best_tour = None
    best_length = float("inf")
    nodes_explored = 0
    nodes_pruned = 0

    # Moi phan tu trong heap: (lower_bound, path_tuple, visited_frozenset)
    # heapq luon lay ra phan tu co lower_bound NHO NHAT truoc (best-first)
    init_path = (start,)
    init_visited = frozenset([start])
    init_bound = _lower_bound(init_path, init_visited, dist_matrix, n, start)

    heap: List[Tuple[float, Tuple[int, ...], FrozenSet[int]]] = [
        (init_bound, init_path, init_visited)
    ]

    while heap:
        bound, path, visited = heapq.heappop(heap)
        nodes_explored += 1

        # CAT NHANH: neu can duoi cua nhanh nay da >= loi giai tot nhat
        # hien co, thi KHONG CAN xet nhanh nay nua (chac chan khong tot hon)
        if bound >= best_length:
            nodes_pruned += 1
            continue

        if len(path) == n:
            # Da di qua du n thanh pho -> tinh do dai chu trinh day du
            total_length = 0.0
            for i in range(n):
                a = path[i]
                b = path[(i + 1) % n]
                total_length += dist_matrix[a][b]

            if total_length < best_length:
                best_length = total_length
                best_tour = list(path)
            continue

        # MO RONG nhanh: thu di den tung thanh pho CHUA tham quan
        last_city = path[-1]
        for next_city in range(n):
            if next_city not in visited:
                new_path = path + (next_city,)
                new_visited = visited | {next_city}
                new_bound = _lower_bound(new_path, new_visited, dist_matrix, n, start)

                # Chi day vao heap neu con "co co hoi" tot hon best_length hien tai
                if new_bound < best_length:
                    heapq.heappush(heap, (new_bound, new_path, new_visited))

    extra_info = {
        "nodes_explored": nodes_explored,
        "nodes_pruned": nodes_pruned,
    }
    return best_tour, extra_info


@measure_performance("Branch and Bound")
def solve(dist_matrix, start=0):
    return _branch_and_bound_core(dist_matrix, start)
