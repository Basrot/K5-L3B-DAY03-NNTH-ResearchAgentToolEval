# Team

## Thông tin nhóm

- Tên nhóm: NNTH
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-NNTH-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: `https://github.com/Basrot/K5-L3B-DAY03-NNTH-ResearchAgentToolEval` (nhánh: `main`)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Gia Nam | 2A202603761 | | Basrot | Trưởng nhóm / Kỹ thuật |
|   2 | Thiều Thế Ngọc | 2A202603788 | | | Thành viên |
|   3 | Đào Ngọc Hân | 2A202603779 | daongochan1505@gmail.com | daongochan | Phụ trách Baseline v0, Failure Analysis (CP1), Tối ưu Prompt/Tools & Báo cáo |
|   4 | Trần Trọng Đức Tài | 2A202603732 | 26ai.taittd@vinuni.edu.vn | | Phụ trách Tool Developer & Testing (CP3), tối ưu v3 |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

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

## TranTrongDucTai-2A202603732

### Phần việc phụ trách

- Phát triển Tool mới `extract_keywords` và viết Unit Tests (CP3).
- Phối hợp đăng ký tool trong registry và schema tools.yaml.
- Phụ trách tối ưu giả thuyết cho phiên bản `v3`.

### Đóng góp cụ thể

- Tạo tool `starter_v0/tools/extract_keywords/` gồm `tool.py` và `TOOL.md` chuẩn contract.
- Đăng ký tool trong `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml`.
- Viết 3 unit tests hoàn chỉnh trong `starter_v0/tests/test_tools_todo.py` bao phủ happy path, bad input và error branch; giữ test suite 70 test passed, 0 failed.

### Bằng chứng

- Tool: `starter_v0/tools/extract_keywords/tool.py`, `TOOL.md`
- Tests: `starter_v0/tests/test_tools_todo.py`
- Commit: `1f527c4` trên branch `2A202603732_TranTrongDucTai`
