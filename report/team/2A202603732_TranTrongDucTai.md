# Báo cáo cá nhân — TranTrongDucTai-2A202603732

## 1. Thông tin thành viên

- Họ tên: Trần Trọng Đức Tài
- MSSV: 2A202603732
- Email: 26ai.taittd@vinuni.edu.vn
- GitHub: DucTai2804

## 2. Phần việc phụ trách

- **CP3 (Tool mới & Unit Test):** Nghiên cứu hợp đồng tool (`tools/README.md`), thiết kế và cài đặt 2 tool mới cho Research Agent gồm `extract_keywords` (trích xuất từ khóa/tần suất) và `text_stats` (thống kê số từ/số câu/đoạn và ước tính thời gian đọc WPM); đăng ký tool trong registry và schema hệ thống; viết bộ unit tests hoàn chỉnh cho từng tool bao phủ các nhánh.
- **CP4 (Bộ Eval của nhóm — 5 Multi-turn cases & eval case cho tool mới):** Thiết kế và cài đặt 5 test cases dạng multi-turn (`turns`) trong `starter_v0/data/eval_group.json` (từ `G06` đến `G10`), cùng test case `G12_text_stats_estimate` kiểm tra định tuyến đến tool `text_stats`.
- **CP2 (Tối ưu prompt/tools & phối hợp):** Phối hợp cùng nhóm kiểm thử và đồng bộ các phiên bản v1, v2, v3.

## 3. Đóng góp cụ thể

- **Phát triển 2 tool mới (`extract_keywords` & `text_stats`):**
  - **Tool `extract_keywords`:** Cài đặt hàm trong `starter_v0/tools/extract_keywords/tool.py` hỗ trợ trích xuất từ khóa tần suất cao, lọc bỏ stop words (Anh - Việt), xử lý Unicode ký tự có dấu, và trả về dict an toàn `{ "error": ... }` khi gặp dữ liệu không hợp lệ. Viết tài liệu đặc tả `TOOL.md`.
  - **Tool `text_stats`:** Cài đặt hàm trong `starter_v0/tools/text_stats/tool.py` tính toán số từ, số ký tự, số câu, số đoạn văn và ước tính thời gian đọc dựa trên tốc độ WPM. Viết tài liệu đặc tả `TOOL.md`.
  - Đăng ký cả 2 hàm vào `TOOL_FUNCTIONS` trong `starter_v0/tools/__init__.py` và khai báo schema tham số đầy đủ trong `starter_v0/artifacts/tools.yaml`.
- **Viết Unit Tests cho các Tool mới:**
  - Viết 3 unit tests cho `extract_keywords` trong `starter_v0/tests/test_tools_todo.py`.
  - Viết 3 unit tests cho `text_stats` trong `starter_v0/tests/test_text_stats.py` bao phủ happy path, bad input (chuỗi rỗng, wpm ép kiểu từ chuỗi) và failure branch (`text=None`, `wpm <= 0`).
  - Chạy `pytest` xác nhận: `tests/test_tool_contract.py` pass toàn bộ hợp đồng, toàn suite pass 86/86 tests, 0 failed.

- **Viết 5 Multi-turn Eval Cases cho nhóm (CP4):**
  - Viết 5 case multi-turn hoàn chỉnh trong `starter_v0/data/eval_group.json` (`G06` đến `G10`), kết hợp cùng 5 case single-turn của bạn Ngọc để hoàn thành đủ 10 case:
    1. `G06_multiturn_extract_keywords`: Kiểm thử trích xuất từ khóa với ngữ cảnh đoạn văn và cập nhật `top_k=3` qua nhiều lượt.
    2. `G07_multiturn_switch_to_arxiv`: Kiểm thử đổi từ tìm web sang tìm bài báo trên arXiv (`papers`).
    3. `G08_multiturn_timeline_correction`: Kiểm thử đổi handle Twitter sang `ylecun` và cập nhật giới hạn bài đăng từ 5 thành 3.
    4. `G09_multiturn_lookup_timeframe`: Kiểm thử cập nhật chủ đề bán dẫn, chuyển `topic='news'` và `timeframe='month'`.
    5. `G10_multiturn_confirmed_send`: Kiểm thử quy trình xác nhận Telegram đầy đủ qua các lượt hỏi - đáp và gọi `send(confirmed=true)`.
  - Kiểm tra tính tương thích với hàm chấm `run_eval.py` và bảo đảm không vi phạm hợp đồng schema.

## 4. Bằng chứng

- File/commit/PR:
  - Tool source & docs:
    - `starter_v0/tools/extract_keywords/tool.py`, `TOOL.md`
    - `starter_v0/tools/text_stats/tool.py`, `TOOL.md`
  - Registry & schema: `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml`
  - Unit tests:
    - `starter_v0/tests/test_tools_todo.py` (cho `extract_keywords`)
    - `starter_v0/tests/test_text_stats.py` (cho `text_stats`)
  - Eval group cases: `starter_v0/data/eval_group.json` (G06 - G10 multi-turn và G12 cho `text_stats`)
  - Báo cáo nhóm: Mục A2, B5a trong `report/team/group_report.md`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng `pytest` offline để kiểm tra hợp đồng schema và unit tests, đảm bảo 0 failed.

## 5. Tự đánh giá

- Hoàn thành đầy đủ các tiêu chuẩn của tiêu chí C4 và C8 theo Rubric: tool chạy ổn định, không gọi mạng ngoài, có tài liệu chuẩn, có đầy đủ 3 bài test cho 3 nhánh hành vi khác nhau và không gây lỗi cho test suite chung của dự án.

