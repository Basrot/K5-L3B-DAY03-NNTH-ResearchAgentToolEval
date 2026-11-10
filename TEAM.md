# Team

## Thông tin nhóm

- Tên nhóm: NNTH
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-NNTH-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: `https://github.com/Basrot/K5-L3B-DAY03-NNTH-ResearchAgentToolEval` (nhánh: `main`)

## Thành viên

| STT | Họ tên             | MSSV        | Email                     | GitHub     | Vai trò                                                                      |
| --: | ------------------ | ----------- | ------------------------- | ---------- | ---------------------------------------------------------------------------- |
|   1 | Nguyễn Gia Nam     | 2A202603761 | 26ai.namng@vinuni.edu.vn  | Basrot     | Trưởng nhóm / Phát triển Streamlit UI, tích hợp Agent, Live Chat, Deploy và báo cáo |
|   2 | Thiều Thế Ngọc     | 2A202603788 | 26ai.ngoctt@vinuni.edu.vn | BFNGOC     | CP2: phân tích lỗi v1, tối ưu tool declaration cho R12                       |
|   3 | Đào Ngọc Hân       | 2A202603779 | daongochan1505@gmail.com  | daongochan | Phụ trách Baseline v0, Failure Analysis (CP1), Tối ưu Prompt/Tools & Báo cáo |
|   4 | Trần Trọng Đức Tài | 2A202603732 | 26ai.taittd@vinuni.edu.vn |            | Phụ trách Tool Developer & Testing (CP3), tối ưu v3                          |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.
## NguyenGiaNam-2A202603761

### Phần việc phụ trách

- Trưởng nhóm, hỗ trợ quản lý repository GitHub và tích hợp sản phẩm chung.
- Phát triển giao diện Research Agent bằng Streamlit (CP4 — UI và Live Chat).
- Tích hợp giao diện với backend Tool Calling của nhóm thông qua `chat.py`.
- Kiểm thử hội thoại nhiều lượt, lưu transcript JSON làm bằng chứng.
- Triển khai website trên Streamlit Community Cloud để phục vụ demo công khai.
- Phối hợp hoàn thiện `TEAM.md`, `group_report.md` và báo cáo cá nhân.

### Đóng góp cụ thể

- Xây dựng giao diện `starter_v0/app.py` bằng Streamlit, hỗ trợ người dùng gửi câu hỏi và nhận phản hồi trực tiếp từ AI Research Agent.
- Tích hợp hàm `run_model_tool_loop()` để Agent có thể thực hiện Tool Calling nhiều vòng, nhận kết quả công cụ và tạo câu trả lời cuối cùng.
- Xây dựng chức năng hiển thị lịch sử hội thoại, tên công cụ được gọi, arguments và kết quả thực thi công cụ.
- Bổ sung cấu hình Provider, Model, số lượt hội thoại giữ ngữ cảnh và số vòng gọi công cụ tối đa.
- Triển khai chức năng lưu và tải transcript JSON, phục vụ kiểm tra các lượt chat và đánh giá hành vi Agent.
- Kiểm thử kết nối với OpenRouter và Gemini; sử dụng `gemini-3.5-flash-lite` trong các phiên kiểm thử giao diện.
- Thực hiện kiểm thử các tình huống cơ bản, yêu cầu thiếu thông tin và hội thoại nhiều lượt. Ghi nhận các lỗi như HTTP 402, HTTP 503 và thiếu API key.
- Triển khai ứng dụng trên Streamlit Community Cloud, cấu hình API key thông qua Secrets và kiểm thử hội thoại trên website công khai.
- Không cung cấp tool `send` trong giao diện web nhằm tránh gửi Telegram ngoài ý muốn.
- Phối hợp cập nhật tài liệu nhóm và tích hợp mã nguồn UI vào nhánh `main`.

### Bằng chứng

- Source code UI: `starter_v0/app.py`.
- Dependencies: `starter_v0/requirements.txt`.
- Backend tích hợp: `starter_v0/chat.py`.
- Transcript kiểm thử: `starter_v0/transcripts/v0_gemini_20261110T181508022586.transcript.json`.
- Live Chat trên Streamlit Cloud: [BỔ SUNG ĐƯỜNG DẪN FILE TRANSCRIPT ĐÃ TẢI VÀ COMMIT].
- Website demo công khai: [BỔ SUNG URL `.streamlit.app`].
- Merge commit tích hợp UI: `1566ce9`.
- Báo cáo cá nhân: `report/team/2A202603761_NguyenGiaNam.md`.
- Báo cáo nhóm: `report/team/group_report.md` (các mục A1, A3, B4, B5a và khó khăn triển khai).
- Công cụ hỗ trợ: ChatGPT, Python 3.11, Streamlit, Gemini API, Git, GitHub và Visual Studio Code.

## DaoNgocHan-2A202603779

### Phần việc phụ trách

- Thiết lập môi trường, kiểm tra preflight & pytest, chạy Baseline `v0` và phân tích lỗi (CP1).
- Phối hợp tối ưu prompt/tool declarations, xây dựng eval cases và hoàn thiện báo cáo nhóm.

### Đóng góp cụ thể

- Cấu hình môi trường `.venv` và API keys, xác thực kết nối OpenRouter (`openai/gpt-4o-mini`) và chạy bộ test hợp đồng (`pytest`).
- Thực thi chạy đánh giá baseline `v0` trên `data/eval_base.json` (đạt `case_accuracy = 0.65`, `routing = 0.75`, `args = 0.65`, `multiturn = 1.00`), ghi nhận vào `starter_v0/artifacts/version_log.csv`.
- Phân tích chi tiết 7/20 case FAIL của `v0` theo từng nhóm lỗi (`wrong_tool`, `wrong_arg_value`, `missing_info`, `wrong_boundary`, `out_of_scope`) trong Bảng B1 & B2 của `report/team/group_report.md`.

### Bằng chứng

- Run log: `starter_v0/runs/v0_B_base_openrouter_20261110T173950199134.json`
- Version log: `starter_v0/artifacts/version_log.csv` (commit `b4ab63d`)
- Phân tích CSV: `starter_v0/analysis/base_runs.csv`
- Báo cáo nhóm: Mục 1, Bảng B1, Bảng B2 trong `report/team/group_report.md`
- Báo cáo cá nhân: `report/team/2A202603779_DaoNgocHan.md`

## ThieuTheNgoc-2A202603788

### Phần việc phụ trách

- CP2 — phân tích lỗi R12 và cải tiến `artifacts/tools.yaml` theo từng giả thuyết cho v2 và v3.
- CP4 — viết case eval single-turn và multi-turn trong `data/eval_group.json`, bao gồm case route tới `extract_keywords` và `deduplicate_sources`.
- Phát triển tool `deduplicate_sources`.

### Đóng góp cụ thể

- Phân tích `R12_confirm_before_send` ở run v1: agent gọi `send` với `confirmed=false` thay vì xin xác nhận trước.
- V2: cập nhật boundary trong mô tả `clarify` và `send`; run đạt 19/20, nhưng R12 vẫn dùng `response_type="text"` thay vì `"yes_no"`.
- V3: làm rõ xác nhận yes/no phải là bước đầu tiên cho yêu cầu gửi Telegram, kể cả khi nội dung chưa rõ. Run đạt 20/20; R12 gọi `clarify` với `response_type="yes_no"`.
- Thêm 5 case single-turn: route tới `extract_keywords`, tìm bài arXiv bằng `papers`, tra cứu chính sách nội bộ bằng `policy`, hỏi khi thiếu arXiv ID/URL, và xác nhận trước khi gửi Telegram.
- Phát triển tool `deduplicate_sources` trong `starter_v0/tools/deduplicate_sources/`, loại bỏ URL trùng sau chuẩn hóa fragment và dấu gạch chéo cuối, đồng thời giữ query string và thứ tự nguồn đầu tiên.
- Thêm case `G11_deduplicate_sources_urls` để kiểm tra route đúng tool và truyền danh sách URL gồm URL trùng, hợp lệ và không hợp lệ.
- `eval_group.json` hiện có 11 case: 6 single-turn và 5 multi-turn. Chưa ghi nhận group eval run.

### Bằng chứng

- Khai báo tool: `starter_v0/artifacts/tools.yaml`.
- Eval cases: `starter_v0/data/eval_group.json`.
- Tool: `starter_v0/tools/deduplicate_sources/tool.py`, `starter_v0/tools/deduplicate_sources/TOOL.md`.
- Run v1: `starter_v0/runs/v1_B_base_openrouter_20261110T180455272193.json`.
- Run v2: `starter_v0/runs/v2_B_base_openrouter_20261110T185059346257.json` (19/20; R12 sai `response_type`).
- Run v3: `starter_v0/runs/v3_B_base_openrouter_20261110T191036287347.json` (20/20; R12 đúng `response_type="yes_no"`).
- Version log: `starter_v0/artifacts/version_log.csv`.
- Commit: `55fb0c7` (thay đổi cho v2), `de2d24d` (thay đổi cho v3), `44059ba` (5 case single-turn), `870ead4` (tool `deduplicate_sources`).
- Kiểm tra contract: `pytest tests/test_tool_contract.py -q` — 60 passed.
- Báo cáo cá nhân: `report/team/2A202603788_ThieuTheNgoc.md`.

## TranTrongDucTai-2A202603732

### Phần việc phụ trách

- Phát triển 2 Tool mới (`extract_keywords`, `text_stats`) và viết Unit Tests (CP3).
- Phối hợp đăng ký tool trong registry và schema tools.yaml.
- Thiết kế 5 case kiểm thử multi-turn trong bộ `data/eval_group.json` (CP4) và case cho tool mới.

### Đóng góp cụ thể

- Tạo tool `starter_v0/tools/extract_keywords/` và `starter_v0/tools/text_stats/` gồm `tool.py` và `TOOL.md` chuẩn contract.
- Đăng ký các tool trong `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml`.
- Viết các bộ unit tests hoàn chỉnh trong `starter_v0/tests/test_tools_todo.py` và `starter_v0/tests/test_text_stats.py` bao phủ happy path, bad input và error branch; giữ test suite 86 test passed, 0 failed.
- Xây dựng 5 case multi-turn (`G06` đến `G10`) cùng case `G12` trong `starter_v0/data/eval_group.json`.

### Bằng chứng

- Tool: `starter_v0/tools/extract_keywords/`, `starter_v0/tools/text_stats/`
- Tests: `starter_v0/tests/test_tools_todo.py`, `starter_v0/tests/test_text_stats.py`
- Eval group cases: `starter_v0/data/eval_group.json` (G06 - G10, G12)
- Báo cáo cá nhân: `report/team/2A202603732_TranTrongDucTai.md`
