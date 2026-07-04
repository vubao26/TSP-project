# Báo Cáo: Phân Tích & So Sánh Các Thuật Toán Giải Bài Toán TSP

> Đây là dàn ý gợi ý. Copy nội dung này sang Google Docs / Word để cả nhóm cùng viết,
> hoặc viết trực tiếp bằng Markdown rồi export sang PDF/Word sau.

## 1. Giới thiệu
- Bài toán TSP là gì? Ứng dụng thực tế (logistics, thiết kế mạch, giao hàng...)
- Vì sao TSP là bài toán NP-hard, độ khó tăng theo n
- Mục tiêu của báo cáo

## 2. Cơ sở lý thuyết
Với mỗi thuật toán, trình bày:
- Ý tưởng thuật toán
- Độ phức tạp thời gian/không gian (Big-O)
- Ưu điểm / nhược điểm

### 2.1 Nhóm thuật toán chính xác (Exact Algorithms)
- Brute Force
- Dynamic Programming (Held-Karp)
- Branch and Bound

### 2.2 Nhóm thuật toán xấp xỉ / heuristic
- Nearest Neighbor (Greedy)
- Genetic Algorithm
- Ant Colony Optimization

## 3. Phương pháp thực nghiệm
- Môi trường chạy thử nghiệm (CPU, ngôn ngữ, thư viện)
- Bộ dữ liệu test: số lượng thành phố (ví dụ 5, 8, 10, 15, 20, 50, 100...)
- Tiêu chí đo: thời gian chạy, tổng độ dài tuyến đường, % lệch so với tối ưu

## 4. Kết quả và phân tích
- Bảng số liệu (từ `results/benchmark_results.csv`)
- Biểu đồ so sánh thời gian chạy theo n (từ notebook)
- Biểu đồ so sánh độ chính xác
- Nhận xét: thuật toán nào tốt cho n nhỏ, n lớn, khi nào nên dùng heuristic

## 5. Kết luận
- Tóm tắt phát hiện chính
- Khuyến nghị chọn thuật toán theo từng tình huống thực tế
- Hướng phát triển thêm (kết hợp heuristic, dùng GPU, thuật toán khác như Simulated Annealing, Christofides...)

## 6. Phân công & đóng góp thành viên
- Bảng ghi rõ ai làm phần nào (dùng để giảng viên chấm điểm minh bạch)

## 7. Tài liệu tham khảo
- Xem `docs/references.md`
