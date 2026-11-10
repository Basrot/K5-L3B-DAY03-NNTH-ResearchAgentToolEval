# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: **NNTH** (Lớp L3B)
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: `openrouter` / `openai/gpt-4o-mini`

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu trước khi sửa (`system_prompt.md` + `tools.yaml` gốc) | — | 0.65 (routing: 0.75, args: 0.65, multiturn: 1.00) | `starter_v0/runs/v0_B_base_openrouter_20261110T173950199134.json` |
| v1 | `system_prompt.md`, `tools.yaml` | Bỏ chỉ dẫn xấu trong `system_prompt.md` (ép đoán mò, ép gọi tool) và làm rõ phạm vi tool trong `tools.yaml` sẽ giúp agent gọi `clarify` khi thiếu handle/URL (`R10`, `R11`) và không gọi tool khi ngoài phạm vi (`R08`, `R14`) | 0.65 | 0.90 (routing: 0.90, args: 0.90, multiturn: 0.8333) | `starter_v0/runs/v1_B_base_openrouter_20261110T180455272193.json` |
| v2 | `tools.yaml` | Thêm boundary xác nhận vào mô tả của `send` và `clarify` trong `tools.yaml` sẽ giúp agent route sang `clarify` thay vì gọi `send` ngay khi chưa có xác nhận (`R12`) | 0.90 | 0.95 (routing: 1.00, args: 0.95, multiturn: 1.00) | `starter_v0/runs/v2_B_base_openrouter_20261110T185059346257.json` |
| v3 | `tools.yaml` | Quy định rõ trong `clarify` và `send` rằng bước đầu của mọi yêu cầu gửi/đăng Telegram bắt buộc dùng `response_type="yes_no"` (không dùng `"text"` trước bước xác nhận kể cả khi nội dung chưa nêu rõ) sẽ nâng `argument_accuracy` và `case_accuracy` lên 1.00 | 0.95 | 1.00 (routing: 1.00, args: 1.00, multiturn: 1.00) | `starter_v0/runs/v3_B_base_openrouter_20261110T191036287347.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON (`starter_v0/runs/v0_B_base_openrouter_20261110T173950199134.json`). Trong 20 case của `eval_base.json`, baseline `v0` đạt **13/20 PASS (65%)** và **7/20 FAIL (35%)**:

| Case ID | Failure Type (`observed_mismatch`) | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R03_web_news_routing` | `wrong_tool` (`wrong_arg_value`) | `lookup(query="AI news", topic="news", timeframe="day", max_results=5)` | `query: expected 'AI', got 'AI news'` — Model chọn đúng tool `lookup` và `topic="news"`, nhưng nhét thêm từ `"news"` vào `query` thay vì chỉ giữ chủ đề cốt lõi `"AI"`. | Sửa `starter_v0/artifacts/tools.yaml` (mô tả tham số `query` và `topic` của `lookup`): khi `topic="news"`, `query` chỉ chứa tên chủ đề chính (ví dụ `"AI"`), không lặp lại chữ `"news"` hay `"tin tức"`. |
| `R08_out_of_scope` | `out_of_scope` (`unexpected_tool_call`) | `send(text="Nguyên hàm của x^2 là ...")` | `expected no tool call` — Câu hỏi giải toán tích phân nằm ngoài phạm vi research agent, nhưng model tự giải rồi gọi `send` để gửi đi do prompt gốc ép *"Pick one tool and fill in its arguments"*. | Sửa `starter_v0/artifacts/system_prompt.md` và `tools.yaml`: bỏ chỉ dẫn ép gọi tool bằng mọi giá; quy định rõ nếu câu hỏi ngoài phạm vi research (toán học, lập trình, kiến thức phổ thông...) thì trả lời trực tiếp / từ chối lịch sự và **không gọi tool nào** (`no_tool`). |
| `R10_missing_handle` | `missing_info` (`missing_tool_call`) | `timeline(screenname="sama")` | `missing tool call clarify; extra tool call timeline` — User yêu cầu *"Tóm tắt 5 tweet mới nhất giúp mình"* mà không nêu tài khoản nào; model tự đoán `"sama"` vì prompt gốc dạy *"do not ask them back — pick a well-known account like Sam Altman"*. | Sửa `starter_v0/artifacts/system_prompt.md` và `tools.yaml`: xóa chỉ dẫn đoán mò tài khoản; bắt buộc gọi `clarify` khi thiếu thông tin bắt buộc như tên tài khoản/handle. |
| `R11_missing_url` | `missing_info` (`missing_tool_call`) | `fetch(url="https://example.com/article")` | `missing tool call clarify; extra tool call fetch` — User nói *"Tóm tắt bài viết này hộ mình"* nhưng không đưa URL; model tự bịa URL `https://example.com/article` do prompt gốc bảo *"assume a likely URL and read it"*. | Sửa `starter_v0/artifacts/system_prompt.md` và `tools.yaml`: xóa chỉ dẫn tự giả định URL; bắt buộc gọi `clarify` để hỏi URL khi user nói mơ hồ (*"bài viết này"*, *"link này"*) mà chưa cung cấp URL hợp lệ. |
| `R12_confirm_before_send` | `wrong_boundary` (`missing_tool_call`) | `send(text="Bản tin này")` | `missing tool call clarify; extra tool call send` — User yêu cầu *"Đăng bản tin này lên Telegram giúp mình"* khi chưa có nội dung cụ thể và chưa xác nhận gửi; model gọi thẳng `send` vì prompt gốc dặn *"When the user wants to send, post, or publish something, just go ahead and do it"*. | Sửa `starter_v0/artifacts/system_prompt.md` và `tools.yaml`: thiết lập boundary xác nhận nghiêm ngặt cho `send` — không bao giờ gọi `send` ngay ở lượt đầu khi chưa xác nhận rõ nội dung/chưa có xác nhận của user; phải gọi `clarify` (`response_type="yes_no"`) để xin xác nhận trước. |
| `R13_parallel_web_and_tweets` | `wrong_tool` (`wrong_arg_value`) | `lookup(query="AI news", timeframe="day", max_results=5)`, `social_search(query="AI", search_type="Latest", limit=5)` | `query: expected 'AI', got 'AI news'; topic: expected 'news', got None` — Model gọi song song đúng 2 tool (`lookup` và `social_search`), nhưng ở `lookup` quên truyền `topic="news"` và lại thêm chữ `"news"` vào `query`. | Sửa `starter_v0/artifacts/tools.yaml` (tool `lookup`) và `system_prompt.md`: quy định khi user tìm "tin / tin tức / news" trên web thì bắt buộc đặt `topic="news"` và giữ `query` ngắn gọn chỉ gồm từ khóa chủ đề (`"AI"`). |
| `R14_out_of_scope_coding` | `out_of_scope` (`unexpected_tool_call`) | `send(text="Dưới đây là một hàm Python tính số Fibonacci...")` | `expected no tool call` — Yêu cầu viết code Python tính Fibonacci bằng đệ quy nằm ngoài phạm vi công cụ research, nhưng model lại gọi `send` để gửi đoạn code. | Sửa `starter_v0/artifacts/system_prompt.md` và `tools.yaml`: làm rõ `send` chỉ dùng để đăng/gửi bản tin lên Telegram sau khi user đã xác nhận, tuyệt đối không dùng `send` để trả lời câu hỏi thông thường hay câu hỏi ngoài phạm vi (viết code, giải toán). |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
