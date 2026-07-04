# Phân Tích & So Sánh Các Thuật Toán Giải Bài Toán TSP

Đồ án nhóm: nghiên cứu, cài đặt và so sánh hiệu năng của các thuật toán giải quyết
bài toán Người bán hàng du lịch (Traveling Salesman Problem - TSP).

## 🎯 Mục tiêu

- Cài đặt các thuật toán giải TSP theo 2 nhóm: **chính xác (exact)** và **xấp xỉ/heuristic (approximate)**.
- Đo và so sánh: thời gian chạy, độ chính xác (so với lời giải tối ưu hoặc gần tối ưu), khả năng mở rộng theo số thành phố.
- Viết báo cáo phân tích, kết luận thuật toán nào phù hợp với quy mô bài toán nào.

## 👥 Thành viên & phân công

| Thành viên | Thuật toán phụ trách | Vai trò khác |
|---|---|---|
| A | Brute Force + Dynamic Programming (Held-Karp) | Tổng hợp phần "Exact Algorithms" trong báo cáo |
| B | Nearest Neighbor + Branch and Bound | Viết script benchmark & vẽ biểu đồ |
| C | Genetic Algorithm | Tổng hợp phần "Heuristic Algorithms" |
| D | Ant Colony Optimization (ACO) | Viết báo cáo tổng hợp, chỉnh sửa & trình bày |

> Cập nhật bảng này với tên thật của các thành viên.

## 📁 Cấu trúc thư mục

```
tsp-project/
├── algorithms/          # Code cài đặt từng thuật toán (mỗi người 1 file)
│   ├── brute_force.py
│   ├── dynamic_programming.py
│   ├── nearest_neighbor.py
│   ├── branch_and_bound.py
│   ├── genetic_algorithm.py
│   └── aco.py
├── data/                # Bộ dữ liệu test (danh sách tọa độ thành phố)
│   └── sample_10.txt
├── results/             # Kết quả benchmark (csv, biểu đồ)
├── docs/                # Báo cáo (bản thảo .md, hình ảnh, tài liệu tham khảo)
├── notebooks/           # Jupyter notebook phân tích, vẽ biểu đồ so sánh
├── tests/               # Unit test cho từng thuật toán
├── benchmark.py         # Script chạy toàn bộ thuật toán & xuất kết quả so sánh
├── requirements.txt
└── README.md
```

## 🚀 Cách chạy

```bash
# 1. Clone repo
git clone https://github.com/<username>/tsp-project.git
cd tsp-project

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Chạy benchmark toàn bộ thuật toán trên 1 bộ dữ liệu
python benchmark.py --data data/sample_10.txt
```

## 📊 Tiêu chí so sánh

- **Thời gian chạy (runtime)** theo số lượng thành phố n
- **Độ chính xác** (chênh lệch % so với lời giải tối ưu, nếu có)
- **Độ phức tạp** (Big-O lý thuyết vs thực nghiệm)
- **Khả năng mở rộng** (n tối đa có thể chạy trong thời gian hợp lý)

## 📝 Quy trình làm việc nhóm

Xem chi tiết tại [CONTRIBUTING.md](./CONTRIBUTING.md).

## 📚 Tài liệu tham khảo

Thêm các nguồn tham khảo (paper, sách, blog) vào `docs/references.md`.
