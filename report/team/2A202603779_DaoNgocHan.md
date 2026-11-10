# Báo cáo cá nhân — DaoNgocHan-2A202603779

## 1. Thông tin thành viên

- Họ tên: Đào Ngọc Hân
- MSSV: 2A202603779
- Email: daongochan1505@gmail.com

## 2. Phần việc phụ trách

- **CP1 (Setup & Baseline `v0`):** Thiết lập môi trường, cấu hình API keys, kiểm tra preflight & unit tests hợp đồng (`pytest`), chạy baseline `v0` và lập bảng phân tích lỗi (Failure Analysis).
- **CP2–CP5:** Phối hợp cùng nhóm tối ưu `system_prompt.md` / `tools.yaml`, xây dựng eval cases và hoàn thiện báo cáo nhóm.

## 3. Đóng góp cụ thể

- Cài đặt môi trường ảo Python, cấu hình các API keys (`OPENROUTER_API_KEY`, `TAVILY_API_KEY`, `FIRECRAWL_API_KEY`, `RAPIDAPI_KEY`) và xác nhận `preflight_provider.py --provider openrouter` hoạt động ổn định với model `openai/gpt-4o-mini`.
- Chạy đánh giá baseline `v0` trên bộ 20 case chuẩn `starter_v0/data/eval_base.json` trước khi can thiệp vào prompt và tool declarations. Kết quả `v0` hợp lệ (`measured_cases = 20/20`, `provider_error_cases = 0`) đạt `case_accuracy = 0.65`, `tool_routing_accuracy = 0.75`, `argument_accuracy = 0.65`, `multiturn_accuracy = 1.00`.
- Cập nhật dòng `v0` vào `starter_v0/artifacts/version_log.csv`, trích xuất bảng phẳng `starter_v0/analysis/base_runs.csv` và phân tích chi tiết cả 7 case FAIL (`R03`, `R08`, `R10`, `R11`, `R12`, `R13`, `R14`) vào Bảng B1 & B2 trong `report/team/group_report.md`.

## 4. Bằng chứng

- File/commit/PR:
  - Run log `v0`: `starter_v0/runs/v0_B_base_openrouter_20261110T173950199134.json` (commit `b4ab63d`)
  - Version log: `starter_v0/artifacts/version_log.csv` (commit `b4ab63d`)
  - Bảng phân tích phẳng: `starter_v0/analysis/base_runs.csv`
  - Báo cáo nhóm: Mục 1, Bảng B1, Bảng B2 trong `report/team/group_report.md`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Sử dụng `scripts/preflight_provider.py`, `pytest`, `run_eval.py` và `scripts/parse_runs.py` để kiểm증 tự động kết quả chạy và đối chiếu từng `actual_tool_calls` trong file run JSON với `expect` trong `data/eval_base.json`.

## 5. Tự đánh giá

- Hoàn thành đầy đủ yêu cầu của CP1 với số liệu thực tế từ API (`provider_error_cases = 0`), phân biệt rõ lỗi chọn sai tham số (`wrong_arg_value` ở `R03`, `R13`), lỗi thiếu hỏi lại (`missing_info` ở `R10`, `R11`), lỗi vượt ranh giới xác nhận (`wrong_boundary` ở `R12`) và lỗi gọi tool thừa cho câu hỏi ngoài phạm vi (`out_of_scope` ở `R08`, `R14`).

