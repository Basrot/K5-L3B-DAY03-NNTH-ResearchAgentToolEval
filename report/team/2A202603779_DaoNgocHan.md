# Báo cáo cá nhân — DaoNgocHan-2A202603779

## 1. Thông tin thành viên

- Họ tên: Đào Ngọc Hân
- MSSV: 2A202603779
- Email: daongochan1505@gmail.com
- GitHub: `daongochan`

## 2. Phần việc phụ trách

- **CP1 (Setup & Baseline `v0`):** Thiết lập môi trường, cấu hình API keys, kiểm tra preflight & unit tests hợp đồng (`pytest`), chạy baseline `v0` và lập bảng phân tích lỗi (Failure Analysis).
- **CP2 (Prompt & Tool Optimization `v1`–`v3`):** Cải tiến `system_prompt.md` và `tools.yaml` ở phiên bản `v1`, chạy đánh giá thực nghiệm `v1`, `v2`, `v3` trên `eval_base.json`, cập nhật `version_log.csv` và xuất bảng phân tích `analysis/base_runs.csv`.
- **CP3 & Bonus Test Challenge:** Nâng cấp và sửa lỗi biên (edge-case bugs) cho 6 tool có sẵn (`format`, `timeline`, `social_search`, `send`, `policy`, `lookup`); hoàn thiện toàn bộ 14/14 unit test `TODO` và viết 4 regression tests trong `starter_v0/tests/test_tools_todo.py` để đạt `104 passed, 0 failed, 0 skipped`.
- **CP4 & CP5 (Group Eval, UI & Báo cáo):** Thực thi chạy đánh giá `eval_group.json` (10/10 và 12/12 PASS), thiết kế lại giao diện Streamlit `starter_v0/app.py` & `.streamlit/config.toml` theo chuẩn tối giản của ChatGPT, tạo transcript kiểm thử thực tế 4 lượt (`v3_openrouter_20261110T224752771866.transcript.json`) và hoàn thiện các bảng B1, B2, B3, B4, B5a, B5 trong `report/team/group_report.md`.

## 3. Đóng góp cụ thể

1. **Thiết lập & Đánh giá Baseline `v0` (CP1):**
   - Cài đặt môi trường ảo Python, cấu hình các API keys (`OPENROUTER_API_KEY`, `TAVILY_API_KEY`, `FIRECRAWL_API_KEY`, `RAPIDAPI_KEY`) và xác nhận `preflight_provider.py --provider openrouter` hoạt động ổn định với model `openai/gpt-4o-mini`.
   - Chạy đánh giá baseline `v0` trên bộ 20 case chuẩn `starter_v0/data/eval_base.json` (`v0_B_base_openrouter_20261110T173950199134.json`), đạt `case_accuracy = 0.65`, `tool_routing_accuracy = 0.75`, `argument_accuracy = 0.65`, `multiturn_accuracy = 1.00`.
   - Phân tích chi tiết cả 7 case FAIL (`R03`, `R08`, `R10`, `R11`, `R12`, `R13`, `R14`) vào Bảng B2 trong `report/team/group_report.md`.
2. **Vòng lặp tối ưu dựa trên bằng chứng `v1` $\rightarrow$ `v3` (CP2):**
   - Viết lại `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml` cho phiên bản `v1` (loại bỏ các chỉ dẫn xấu cố ý của starter, thêm quy tắc routing và quy ước tham số), nâng `case_accuracy` từ `0.65` lên `0.90` (`18/20` PASS).
   - Phối hợp chạy đánh giá `v2` (`0.95` — `19/20` PASS) và `v3` (`1.00` — `20/20` PASS tuyệt đối trên mọi chỉ số), ghi đầy đủ mã hash, giả thuyết và metric trước/sau vào `starter_v0/artifacts/version_log.csv`, đồng thời tổng hợp `starter_v0/analysis/base_runs.csv` (80 dòng).
3. **Nâng cấp Tool có sẵn & Hoàn thiện Unit Test / Regression Test (CP3 & Bonus):**
   - Sửa các lỗi tiềm ẩn trong 6 tool có sẵn:
     - `format`: Sửa lỗi thừa dấu gạch ngang `" - "` ở cuối dòng khi item thiếu `url` và `source`.
     - `timeline` & `social_search`: Sửa lỗi `int(limit or 5)` biến `limit=0` thành `5` và tự động cắt ký tự `@` đầu `screenname`.
     - `policy`: Sửa lỗi `int(top_k or 3)` trả về 3 kết quả khi `top_k=0`.
     - `send`: Sửa lỗi bảo mật `if not confirmed:` cho phép chuỗi `"false"` lách qua hàng rào xác nhận.
     - `lookup`: Chuẩn hóa an toàn tham số `max_results`.
   - Hoàn thiện toàn bộ 14/14 test `TODO` và bổ sung 4 regression tests trong `starter_v0/tests/test_tools_todo.py`, đưa toàn bộ suite `pytest` đạt **104 passed, 0 failed, 0 skipped**.
4. **Đánh giá Group Eval, Tối ưu Giao diện Streamlit & Hoàn thiện Báo cáo (CP4, CP5):**
   - Chạy đánh giá `run_eval.py --suite group` đạt **10/10 PASS** (`v3_B_group_openrouter_20261110T193715824551.json`) và **12/12 PASS** sau khi tích hợp đủ 3 tool mới (`v3_B_group_openrouter_20261110T224703124394.json`).
   - Thiết kế lại giao diện `starter_v0/app.py` và `.streamlit/config.toml` theo phong cách tối giản của ChatGPT (hiệu ứng trượt đóng/mở Sidebar `cubic-bezier(0.4, 0, 0.2, 1)` với icon Panel Toggle SVG, font chữ `Inter`, loại bỏ 100% emoji màu, tích hợp bộ chọn model ngay bên phải bên trong hộp soạn tin nhắn, quản lý danh sách hội thoại trong phiên).
   - Thực hiện kiểm thử live chat 4 lượt (`v3_openrouter_20261110T224752771866.transcript.json`) bao phủ đủ: gọi tool mới `extract_keywords`, hỏi lại khi thiếu thông tin (`clarify`), bổ sung thông tin ở lượt sau (`timeline`), và xin xác nhận `yes_no` trước khi gửi Telegram.

## 4. Bằng chứng

- **Run logs (`starter_v0/runs/`):**
  - `v0`: `starter_v0/runs/v0_B_base_openrouter_20261110T173950199134.json` (commit `b4ab63d`)
  - `v1`: `starter_v0/runs/v1_B_base_openrouter_20261110T180455272193.json` (commit `89b35e9`)
  - `v2`: `starter_v0/runs/v2_B_base_openrouter_20261110T185059346257.json` (commit `1807a68`)
  - `v3` (Base 20/20): `starter_v0/runs/v3_B_base_openrouter_20261110T191036287347.json` (commit `ef3776f`)
  - `v3` (Group 10/10 & 12/12): `starter_v0/runs/v3_B_group_openrouter_20261110T193715824551.json` (commit `10ceed8`), `starter_v0/runs/v3_B_group_openrouter_20261110T224703124394.json`
- **Code, Tests & Transcripts:**
  - Prompt & Versioning: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/version_log.csv`, `starter_v0/analysis/base_runs.csv`
  - Upgraded Tools & Unit Tests: `starter_v0/tests/test_tools_todo.py`, `starter_v0/tools/format/tool.py`, `starter_v0/tools/timeline/tool.py`, `starter_v0/tools/social_search/tool.py`, `starter_v0/tools/send/tool.py`, `starter_v0/tools/policy/tool.py`, `starter_v0/tools/lookup/tool.py`
  - Streamlit UI & Transcripts: `starter_v0/app.py`, `starter_v0/.streamlit/config.toml`, `starter_v0/transcripts/v3_openrouter_20261110T224752771866.transcript.json`, `starter_v0/transcripts/v3_gemini_20261110T221335666627.transcript.json`
  - Báo cáo nhóm: `report/team/group_report.md` (Mục 1, B1, B2, B3, B4, B5a, B5)

## 5. Tự đánh giá

- Hoàn thành đầy đủ tất cả các hạng mục từ CP1 đến CP5 và phần Bonus Test Challenge với bằng chứng định lượng rõ ràng: Base Eval đạt **20/20 PASS (`1.00`)** ở `v3`, Group Eval đạt **12/12 PASS (`1.00`)**, bộ Unit Test đạt **104 passed, 0 failed, 0 skipped**, và giao diện Streamlit hoạt động mượt mà kèm transcript đầy đủ.
