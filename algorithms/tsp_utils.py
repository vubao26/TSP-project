import time
import tracemalloc
import math
import functools
import os

# =================================================================
# 1. DOC DU LIEU TU FILE TSPLIB (.tsp)
# =================================================================

def read_tsplib(filepath):
    """
    Doc file dinh dang TSPLIB (vi du: berlin52.tsp, burma14.tsp, kroA100.tsp, st70.tsp)
    """
    name = None
    dimension = None
    edge_weight_type = "EUC_2D"
    coords = []
    reading_coords = False

    with open(filepath, "r") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            if line.startswith("NAME"):
                name = line.split(":")[1].strip()
            elif line.startswith("DIMENSION"):
                dimension = int(line.split(":")[1].strip())
            elif line.startswith("EDGE_WEIGHT_TYPE"):
                edge_weight_type = line.split(":")[1].strip()
            elif line.startswith("NODE_COORD_SECTION"):
                reading_coords = True
                continue
            elif line.startswith("EOF"):
                break
            elif reading_coords:
                parts = line.split()
                if len(parts) >= 3:
                    city_id = int(parts[0]) - 1   # chuyen ve 0-indexed
                    x = float(parts[1])
                    y = float(parts[2])
                    coords.append((city_id, x, y))

    return {
        "name": name,
        "dimension": dimension,
        "edge_weight_type": edge_weight_type,
        "coords": coords,
    }


def read_opt_tour(filepath):
    """
    Doc file loi giai toi uu (.opt.tour) do TSPLIB cung cap
    """
    tour = []
    reading_tour = False
    with open(filepath, "r") as f:
        for raw_line in f:
            line = raw_line.strip()
            if line.startswith("TOUR_SECTION"):
                reading_tour = True
                continue
            if not reading_tour:
                continue
            if line in ("-1", "EOF"):
                break
            if line:
                tour.append(int(line) - 1)   # ve 0-indexed
    return tour


# =================================================================
# 2. TINH MA TRAN KHOANG CACH
# =================================================================

def _nint(x):
    """Ham lam tron ve so nguyen gan nhat - theo dung quy uoc cua TSPLIB."""
    return int(x + 0.5)


def _euclidean(p1, p2):
    """Khoang cach EUC_2D (chuan TSPLIB): lam tron ve so nguyen gan nhat."""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return _nint(math.sqrt(dx * dx + dy * dy))


def _geo(p1, p2):
    """
    Khoang cach GEO (dung cho burma14.tsp - toa do la kinh do/vi do).
    Cong thuc chuan TSPLIB cho EDGE_WEIGHT_TYPE = GEO.
    """
    RRR = 6378.388

    def to_radians(coord):
        deg = int(coord)
        minutes = coord - deg
        return math.pi * (deg + 5.0 * minutes / 3.0) / 180.0

    lat1, lon1 = to_radians(p1[0]), to_radians(p1[1])
    lat2, lon2 = to_radians(p2[0]), to_radians(p2[1])

    q1 = math.cos(lon1 - lon2)
    q2 = math.cos(lat1 - lat2)
    q3 = math.cos(lat1 + lat2)

    return int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)


def compute_distance_matrix(coords, edge_weight_type="EUC_2D"):
    n = len(coords)
    dist_matrix = [[0.0] * n for _ in range(n)]

    dist_fn = _geo if edge_weight_type == "GEO" else _euclidean

    points = [(x, y) for (_id, x, y) in coords]

    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = dist_fn(points[i], points[j])
    return dist_matrix


def generate_random_instance(n, seed=42, width=1000, height=1000):
    import random
    rng = random.Random(seed)
    coords = [(i, rng.uniform(0, width), rng.uniform(0, height)) for i in range(n)]
    dist_matrix = compute_distance_matrix(coords, "EUC_2D")
    return coords, dist_matrix


def take_subinstance(coords, n):
    sub = coords[:n]
    return [(i, x, y) for i, (_old_id, x, y) in enumerate(sub)]


# =================================================================
# 3. TINH DO DAI TOUR
# =================================================================

def tour_length(tour, dist_matrix):
    n = len(tour)
    total = 0.0
    for i in range(n):
        a = tour[i]
        b = tour[(i + 1) % n]   # % n de noi vong ve diem dau
        total += dist_matrix[a][b]
    return total


def relative_error(found_length, optimal_length):
    if optimal_length == 0:
        return 0.0
    return (found_length - optimal_length) / optimal_length * 100.0


# =================================================================
# 4. DO RUNTIME + MEMORY (BENCHMARK PROTOCOL CHUNG CUA NHOM)
# =================================================================

def measure_performance(algorithm_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(dist_matrix, *args, **kwargs):
            n = len(dist_matrix)

            tracemalloc.start()
            t0 = time.perf_counter()

            tour, extra = func(dist_matrix, *args, **kwargs)

            t1 = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            return {
                "algorithm": algorithm_name,
                "tour": tour,
                "tour_length": tour_length(tour, dist_matrix),
                "runtime": t1 - t0,                     # giay
                "memory_usage": peak / (1024 * 1024),   # MB
                "n_cities": n,
                "extra": extra or {},
            }
        return wrapper
    return decorator


def print_result(result, optimal_length=None):
    """In ket qua ra man hinh theo dung cac truong da thong nhat."""
    print(f"--- {result['algorithm']} (n={result['n_cities']}) ---")
    print(f"Tour         : {result['tour']}")
    print(f"Tour Length  : {result['tour_length']:.2f}")
    print(f"Runtime      : {result['runtime']*1000:.4f} ms")
    print(f"Memory Usage : {result['memory_usage']:.4f} MB")
    if optimal_length is not None:
        err = relative_error(result["tour_length"], optimal_length)
        print(f"Relative Error vs Optimal: {err:.4f}%")
    if result["extra"]:
        print(f"Extra Info   : {result['extra']}")
    print()
