# Báo cáo cá nhân — Thiều Thế Ngọc

## 1. Thông tin thành viên

- Họ tên: Thiều Thế Ngọc
- MSSV: 2A202603788
- Email: 26ai.ngoctt@vinuni.edu.vn

## 2. Phần việc phụ trách

- CP2 — phân tích lỗi và cải tiến `artifacts/tools.yaml` theo từng giả thuyết cho v2 và v3.
- CP4 — viết 5 case eval single-turn cho `data/eval_group.json`, trong đó có case kiểm tra routing tới tool mới `extract_keywords`.

## 3. Đóng góp cụ thể

- Phân tích lỗi `R12_confirm_before_send` trong run v1: agent gọi `send` với `confirmed=false` thay vì xin xác nhận trước.
- **V2 — commit `55fb0c7`:** thử giả thuyết rằng mô tả rõ boundary xác nhận trong khai báo `send` và `clarify` sẽ khiến agent hỏi xác nhận thay vì gọi gửi ngay. Run v2 đạt 19/20 case; R12 đã gọi `clarify` nhưng vẫn dùng `response_type="text"` thay vì `"yes_no"`.
- **V3 — commit `de2d24d`:** dựa trên lỗi R12 còn lại, làm rõ rằng yêu cầu gửi Telegram phải bắt đầu bằng xác nhận `yes_no`, kể cả khi nội dung chưa rõ; chỉ hỏi nội dung bổ sung sau khi xác nhận. Run v3 đạt 20/20 case; R12 gọi `clarify` với `response_type="yes_no"`.
- Viết 5 case single-turn trong `starter_v0/data/eval_group.json`:
  - Route yêu cầu trích từ khóa tới tool mới `extract_keywords`.
  - Tìm bài arXiv bằng `papers`.
  - Tra cứu chính sách quyền riêng tư nội bộ bằng `policy`.
  - Hỏi bổ sung khi thiếu arXiv ID/URL.
  - Xin xác nhận trước khi gửi Telegram.
- Bộ `eval_group.json` hiện có 5 case single-turn này; 5 case multi-turn còn cần được bổ sung để đủ yêu cầu CP4. Chưa ghi nhận group eval run trong phần đóng góp này.

## 4. Bằng chứng

- File/commit:
  - `starter_v0/artifacts/tools.yaml`
  - `starter_v0/data/eval_group.json`
  - Commit `55fb0c7` — thay đổi khai báo tool cho giả thuyết v2.
  - Commit `de2d24d` — thay đổi khai báo tool cho giả thuyết v3.
  - Commit `44059ba` — thêm 5 case single-turn.
- Eval:
  - Run v1: `starter_v0/runs/v1_B_base_openrouter_20261110T180455272193.json`.
  - Run v2: `starter_v0/runs/v2_B_base_openrouter_20261110T185059346257.json` — 19/20 pass; R12 sai `response_type`.
  - Run v3: `starter_v0/runs/v3_B_base_openrouter_20261110T191036287347.json` — 20/20 pass; R12 dùng `response_type="yes_no"`.
  - Version history: `starter_v0/artifacts/version_log.csv`.
- AI/công cụ đã dùng và cách tự kiểm tra:
  - Dùng Copilot/ChatGPT để hỗ trợ phân tích run và rà soát wording của tool declarations, sau đó tự đối chiếu kết quả với expected behavior trong `starter_v0/data/eval_base.json`.
  - Kiểm tra cấu trúc 5 case group bằng cách parse JSON, xác nhận đủ các trường bắt buộc và có case route tới `extract_keywords`.
  - Chạy `pytest tests/test_tool_contract.py -q`: 60 passed.

## 5. Tự đánh giá

- Các thay đổi v2 và v3 được tách thành hai giả thuyết liên tiếp về cùng lỗi R12; run v2 cho thấy lỗi chưa hết, còn run v3 xác nhận case R12 và toàn bộ base eval đạt.
- Đã hoàn thành 5 case single-turn theo phân công; cần phối hợp hoàn thành 5 case multi-turn và chạy group eval trước khi xem CP4 hoàn tất.
