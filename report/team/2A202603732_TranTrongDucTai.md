# Báo cáo cá nhân — TranTrongDucTai-2A202603732

## 1. Thông tin thành viên

- Họ tên: Trần Trọng Đức Tài
- MSSV: 2A202603732
- Email: 26ai.taittd@vinuni.edu.vn

## 2. Phần việc phụ trách

- **CP3 (Tool mới & Unit Test):** Nghiên cứu hợp đồng tool (`tools/README.md`), thiết kế và cài đặt tool mới `extract_keywords` phục vụ bài toán tóm lược/trích xuất từ khóa cho Research Agent; đăng ký tool trong registry và schema hệ thống; viết bộ unit tests bao phủ các nhánh.
- **CP2 (Tối ưu vòng `v3`):** Phối hợp cùng nhóm nhận bản `v2`, phân tích các case còn lại để đưa ra một giả thuyết tối ưu cuối cùng, chạy eval và ghi nhận version log `v3`.

## 3. Đóng góp cụ thể

- **Phát triển tool mới (`extract_keywords`):**
  - Cài đặt hàm `extract_keywords(text, top_k)` trong `starter_v0/tools/extract_keywords/tool.py` hỗ trợ trích xuất từ khóa tần suất cao, lọc bỏ stop words (tiếng Anh và tiếng Việt), xử lý Unicode ký tự có dấu, và trả về dict an toàn `{ "error": ... }` khi gặp dữ liệu không hợp lệ mà không làm crash agent (`raise Exception`).
  - Viết tài liệu đặc tả `starter_v0/tools/extract_keywords/TOOL.md` đầy đủ YAML frontmatter theo đúng chuẩn của đề bài.
  - Đăng ký hàm vào `TOOL_FUNCTIONS` trong `starter_v0/tools/__init__.py` và khai báo schema tham số đầy đủ trong `starter_v0/artifacts/tools.yaml`.
- **Viết Unit Tests cho Tool:**
  - Viết 3 unit tests hoàn chỉnh trong `starter_v0/tests/test_tools_todo.py`:
    1. Happy path: kiểm tra trích xuất đúng top keyword ("agent" xuất hiện 3 lần).
    2. Bad input: kiểm tra chuỗi rỗng, khoảng trắng, và trường hợp model gửi số dạng chuỗi (`top_k="2"`).
    3. Failure branch: kiểm tra bắt lỗi an toàn khi truyền sai kiểu dữ liệu (`text=None`) hoặc `top_k <= 0`.
  - Chạy `pytest` xác nhận: `tests/test_tool_contract.py` pass 60/60 checks, toàn suite pass 70/70 tests, 0 failed.

## 4. Bằng chứng

- File/commit/PR:
  - Tool source & docs: `starter_v0/tools/extract_keywords/tool.py`, `TOOL.md` (commit `1f527c4` trên branch `2A202603732_TranTrongDucTai`)
  - Registry & schema: `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml`
  - Unit tests: `starter_v0/tests/test_tools_todo.py`
  - Báo cáo nhóm: Mục CP3, Bảng B5 trong `report/team/group_report.md`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng `pytest` offline để kiểm tra hợp đồng schema và unit tests, đảm bảo 0 failed.

## 5. Tự đánh giá

- Hoàn thành đầy đủ các tiêu chuẩn của tiêu chí C4 và C8 theo Rubric: tool chạy ổn định, không gọi mạng ngoài, có tài liệu chuẩn, có đầy đủ 3 bài test cho 3 nhánh hành vi khác nhau và không gây lỗi cho test suite chung của dự án.

