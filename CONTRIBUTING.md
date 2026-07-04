# Quy trình làm việc nhóm (Git Workflow)

Nhóm 4 người, mỗi người phụ trách 1-2 thuật toán. Để tránh conflict và dễ review, làm theo quy trình sau.

## 1. Nhánh (branches)

- `main`: nhánh ổn định, chỉ merge code đã chạy được và review xong.
- `dev`: nhánh tổng hợp trước khi merge vào `main`.
- Mỗi thành viên tạo nhánh riêng theo cú pháp: `feature/<ten>-<thuat-toan>`
  - Ví dụ: `feature/anh-brute-force`, `feature/binh-genetic-algorithm`

## 2. Quy trình cho mỗi thành viên

```bash
# Cập nhật code mới nhất
git checkout dev
git pull origin dev

# Tạo nhánh riêng để code
git checkout -b feature/ten-thuat-toan

# ... code, commit ...
git add .
git commit -m "feat: cài đặt thuật toán Nearest Neighbor"

# Đẩy lên GitHub
git push origin feature/ten-thuat-toan
```

Sau đó tạo **Pull Request** vào nhánh `dev`, tag 1 bạn khác review trước khi merge.

## 3. Quy ước commit message

- `feat: ...` – thêm tính năng/thuật toán mới
- `fix: ...` – sửa lỗi
- `docs: ...` – cập nhật báo cáo/tài liệu
- `test: ...` – thêm/sửa test
- `chore: ...` – việc lặt vặt (cấu hình, dọn dẹp)

## 4. Chuẩn code cho từng thuật toán

Mỗi file trong `algorithms/` cần có:

1. Hàm chính nhận vào ma trận khoảng cách (hoặc danh sách tọa độ) và trả về `(route, total_distance, runtime)`.
2. Docstring mô tả độ phức tạp thời gian (Big-O) và nguyên lý hoạt động.
3. Có thể chạy độc lập bằng `python algorithms/ten_file.py` để test nhanh.

Ví dụ interface thống nhất (xem `algorithms/nearest_neighbor.py`):

```python
def solve(distance_matrix) -> tuple[list[int], float, float]:
    """
    Trả về:
        route: danh sách chỉ số thành phố theo thứ tự đi qua
        total_distance: tổng độ dài quãng đường
        runtime: thời gian chạy (giây)
    """
```

Giữ interface giống nhau giúp `benchmark.py` có thể gọi tất cả thuật toán tự động.

## 5. Deadline & checklist gợi ý

- [ ] Tuần 1: Mỗi người cài đặt xong thuật toán của mình + test trên bộ dữ liệu nhỏ (5-10 thành phố)
- [ ] Tuần 2: Chạy benchmark trên bộ dữ liệu lớn hơn (20-50-100 thành phố), thu thập số liệu
- [ ] Tuần 3: Vẽ biểu đồ so sánh (notebook), viết phần phân tích cho thuật toán mình phụ trách
- [ ] Tuần 4: Tổng hợp báo cáo hoàn chỉnh, review chéo, chỉnh sửa cuối cùng

## 6. Review Pull Request

Khi review code của bạn khác, kiểm tra:
- Interface đúng chuẩn `solve()` chưa
- Có test/ví dụ chạy thử chưa
- Code có comment giải thích thuật toán chưa
- Kết quả trả về có đúng logic (đi qua đủ n thành phố, không lặp) không
