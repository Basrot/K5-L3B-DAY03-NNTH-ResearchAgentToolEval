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

Research Agent là hệ thống trợ lý AI có khả năng hỗ trợ nghiên cứu, tìm kiếm thông tin trên Internet, đọc nội dung website, tìm kiếm tài liệu khoa học trên arXiv và phân tích thông tin mạng xã hội X/Twitter.

Hệ thống sử dụng cơ chế Tool Calling để AI tự lựa chọn và thực thi công cụ phù hợp với yêu cầu của người dùng. Khi thiếu thông tin quan trọng, Agent có thể yêu cầu người dùng bổ sung thay vì tự suy đoán.

Nhóm phát triển giao diện bằng Streamlit, cho phép:
- Trò chuyện trực tiếp với Research Agent.
- Lựa chọn Provider và Model AI.
- Theo dõi công cụ được gọi và tham số truyền vào.
- Xem kết quả thực thi của từng công cụ.
- Hội thoại nhiều lượt và duy trì ngữ cảnh.
- Lưu và tải transcript JSON phục vụ kiểm thử.

**Cách chạy UI:**

```powershell
cd starter_v0
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

**Link dùng thử (deploy):**

- Nền tảng: Streamlit Community Cloud
- URL: [(https://vinuni-research-agent-nhth.streamlit.app/)]
- Source code: `starter_v0/app.py`

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. **Cơ bản:** Tìm 3 ứng dụng thực tế của AI trong lĩnh vực y tế và cung cấp nguồn tham khảo.
2. **Thiếu bối cảnh:** Hãy lấy 5 bài đăng gần đây nhất của tài khoản đó trên X.
3. **Đa bước:** Tìm 3 nghiên cứu gần đây trên arXiv về AI Agent, đọc nội dung hoặc phần tóm tắt của từng nghiên cứu và tổng hợp thành một bản tin ngắn kèm nguồn.

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

`starter_v0/data/eval_group.json` hiện có 11 case (6 single-turn + 5 multi-turn). Run v3 dưới đây được tạo trước khi thêm G11 và chỉ đo G01–G10: **10/10 PASS** (`case_accuracy: 1.0`, `tool_routing_accuracy: 1.0`, `argument_accuracy: 1.0`, `multiturn_accuracy: 1.0`, `provider_error_cases: 0`). G11 chưa có kết quả chạy, không tính vào các metric này.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_extract_keywords_route` (Single-turn) | Yêu cầu trích từ khóa từ văn bản đã cho phải gọi tool mới `extract_keywords` và truyền đúng văn bản cùng `top_k=3`. | `extract_keywords(text="AI agents can help researchers organize papers. AI agents also support literature review.", top_k=3)` | **PASS** |
| `G02_arxiv_paper_search` (Single-turn) | Yêu cầu tìm bài báo khoa học trên arXiv phải gọi `papers` thay vì `lookup` web. | `papers(query="retrieval-augmented generation", max_results=3)` | **PASS** |
| `G03_internal_data_privacy_policy` (Single-turn) | Câu hỏi về quy định nội bộ quyền riêng tư phải tra cứu `policy_area="data_privacy"`, không tìm trên web công khai. | `policy(policy_area="data_privacy")` | **PASS** |
| `G04_missing_arxiv_identifier` (Single-turn) | Thiếu arXiv ID hoặc URL thì hỏi người dùng bổ sung, không đoán bài và không gọi `paper_text`. | `clarify(response_type="text")` | **PASS** |
| `G05_confirm_before_telegram_send` (Single-turn) | Trước hành động gửi ra ngoài, phải xin xác nhận `yes_no` và không gọi `send` ngay trong cùng yêu cầu. | `clarify(response_type="yes_no")` | **PASS** |
| `G06_multiturn_extract_keywords` (Multi-turn) | Qua 3 lượt hội thoại: mang ngữ cảnh đoạn văn từ lượt trước sang lượt sau và gọi tool `extract_keywords` với `top_k=3`. | `extract_keywords(text="Machine learning and deep learning models have revolutionized natural language processing tasks.", top_k=3)` | **PASS** |
| `G07_multiturn_switch_to_arxiv` (Multi-turn) | Hủy yêu cầu tìm web ở lượt đầu, chuyển hẳn sang gọi tool `papers` với đúng từ khóa và giới hạn 3 kết quả. | `papers(query="Reasoning Models", max_results=3)` | **PASS** |
| `G08_multiturn_timeline_correction` (Multi-turn) | Cập nhật tài khoản sang Yann LeCun (handle `"ylecun"`) và giảm giới hạn số lượng bài đăng từ 5 xuống 3. | `timeline(screenname="ylecun", limit=3)` | **PASS** |
| `G09_multiturn_lookup_timeframe` (Multi-turn) | Chuyển `topic="general"` sang `topic="news"` và cập nhật `timeframe="month"` cho chủ đề `semiconductor` qua nhiều lượt. | `lookup(query="semiconductor", topic="news", timeframe="month")` | **PASS** |
| `G10_multiturn_confirmed_send` (Multi-turn) | Sau khi bot đã hỏi xác nhận và user đã xác nhận rõ ràng ở lượt 3, agent gọi tool `send` với `confirmed=true`. | `send(text="Nghiên cứu mới về Agentic AI vừa được công bố.", confirmed=true)` | **PASS** |
| `G11_deduplicate_sources_urls` (Single-turn) | Danh sách URL nguồn phải được chuyển nguyên dạng vào `deduplicate_sources`; tool sẽ xử lý URL trùng và URL không hợp lệ. | `deduplicate_sources(urls=[...])` | **Chưa chạy** |

### B4. Live Chat Evidence

Giao diện Streamlit đã được kiểm thử với mô hình Gemini `gemini-3.5-flash-lite`.

Các tình huống kiểm thử gồm: yêu cầu cơ bản, duy trì ngữ cảnh hội thoại, tìm kiếm thông tin mạng xã hội và xử lý yêu cầu thiếu thông tin.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Xin chào! Bạn có thể giúp tôi làm những công việc gì? | Không cần tool | Transcript kiểm thử Gemini | PASS — Agent giới thiệu đúng chức năng |
| 2 | Tìm 5 thông tin về ứng dụng AI trong chẩn đoán y tế, kèm nguồn tham khảo. | `lookup`, `format` (cần đối chiếu transcript) | Transcript kiểm thử Gemini | PASS sơ bộ — Trả lời có nội dung và nguồn |
| 3 | Tóm tắt 3 ý quan trọng nhất từ các thông tin vừa tìm được. | Kiểm tra transcript | Transcript kiểm thử Gemini | PASS — Sử dụng ngữ cảnh câu trước |
| 4 | Hãy lấy 5 bài đăng gần đây của tài khoản @OpenAI trên X. | Cần xác minh tool thực tế | Transcript kiểm thử Gemini | Cần kiểm tra dữ liệu trả về từ API |
| 5 | Hãy tìm thông tin về một tài khoản X nhưng tôi chưa cung cấp tên tài khoản. | `clarify` nếu log xác nhận | Transcript kiểm thử Gemini | PASS hành vi — Agent hỏi lại tên tài khoản |
**Bằng chứng:**
- Source code: `starter_v0/app.py`
- Transcript: `starter_v0/transcripts/*.transcript.json`
- Website: [(https://vinuni-research-agent-nhth.streamlit.app/)]
### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới: `extract_keywords` | `starter_v0/tools/extract_keywords/tool.py`, `starter_v0/tools/extract_keywords/TOOL.md` | Trích các từ xuất hiện nhiều nhất sau khi lọc stop words, trả về từ khóa cùng số lần xuất hiện; không cần gọi API bên ngoài. | Kết quả dựa trên tần suất từ và danh sách stop words, không thay thế phân tích ngữ nghĩa. Kiểm tra kiểu `text` và `top_k`; trả lỗi khi input không hợp lệ. |
| Tool mới: `deduplicate_sources` | `starter_v0/tools/deduplicate_sources/tool.py`, `starter_v0/tools/deduplicate_sources/TOOL.md` | Giữ URL hợp lệ đầu tiên theo thứ tự; bỏ trùng không phân biệt hoa thường ở scheme/host, bỏ fragment và trailing slash khi so trùng, giữ query string; đếm URL trùng và không hợp lệ. | Chỉ nhận URL HTTP(S); bỏ qua item/URL không hợp lệ và báo `invalid_count`. Không có side effect hay gửi dữ liệu ra ngoài. |
| Unit test: `extract_keywords` (3 test cases) | `starter_v0/tests/test_tools_todo.py` — `test_extract_keywords_happy_path_returns_top_frequent_words`, `test_extract_keywords_bad_input_from_model_handles_gracefully`, `test_extract_keywords_failure_returns_error_dict` | Bao phủ kết quả thường, input rỗng/whitespace và xử lý input sai/top_k không hợp lệ. | Ví dụ lỗi được unit test bắt nhưng eval không kiểm tra: `text=None` phải trả `invalid_input`, hoặc `top_k=0` phải trả `invalid_top_k`. |
| Unit test: `deduplicate_sources` (3 test cases) | `starter_v0/tests/test_deduplicate_sources.py` — `test_deduplicate_sources_removes_fragments_and_trailing_slashes`, `test_deduplicate_sources_rejects_non_list_input`, `test_deduplicate_sources_skips_invalid_urls_and_items` | Bao phủ chuẩn hóa URL và giữ query string, input không phải list, cùng URL/item không hợp lệ. | Ví dụ lỗi được unit test bắt nhưng eval G11 không kiểm tra: truyền `urls` không phải list phải trả `invalid_input`; G11 chỉ kiểm tra routing và truyền một list URL. |
| UI | `starter_v0/app.py`, `starter_v0/requirements.txt` | Chạy local bằng `cd starter_v0` rồi `python -m streamlit run app.py`; UI mặc định mở tại `http://localhost:8501`. | Chưa có link deploy công khai được ghi nhận. Cần cấu hình API key cho provider đã chọn; không đưa key vào báo cáo hoặc transcript. |

**Trạng thái chạy unit test:** các test mới được liệt kê ở trên trong source; chưa ghi nhận output chạy pytest cho riêng các test này trong phần bằng chứng B5a.

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
### 5.1. Cấu hình môi trường Python

**Khó khăn:** Quá trình cài đặt thư viện ban đầu gặp vấn đề tương thích với phiên bản Python.

**Cách xử lý:** Sử dụng Python 3.11 và môi trường ảo `.venv`, sau đó cài đặt các dependency trong `requirements.txt`.
### 5.2. Kết nối AI Provider

**Khó khăn:**
- OpenRouter từng trả về HTTP 402 do giới hạn credit.
- Một số model Gemini gặp lỗi không khả dụng hoặc HTTP 503 khi dịch vụ quá tải.

**Cách xử lý:** Kiểm tra kết nối bằng script preflight và lựa chọn model Gemini `gemini-3.5-flash-lite` đã chạy thành công trong quá trình thử nghiệm.

### 5.3. Triển khai Streamlit Community Cloud

**Khó khăn:** Website sau khi deploy gặp lỗi `Missing API key env var: GEMINI_API_KEY` vì môi trường cloud không sử dụng trực tiếp file `.env` trên máy cá nhân.

**Cách xử lý:** Cấu hình API key trong Streamlit Cloud Secrets, sau đó kiểm thử lại giao diện và khả năng kết nối Gemini.

### 5.4. Đánh giá hành vi Tool Calling

**Khó khăn:** Trong quá trình kiểm thử, Agent có trường hợp tự suy đoán tài khoản X khi người dùng chưa cung cấp đầy đủ thông tin. Ngoài ra, một số công cụ phụ thuộc API bên ngoài nên có thể gặp lỗi khi thiếu key.

**Cách xử lý:** Lưu transcript JSON để phân tích các lượt thực thi công cụ, kiểm tra arguments và so sánh kết quả trả về. Nhóm tiếp tục cải tiến System Prompt và Tool Declaration nhằm xử lý tốt hơn các yêu cầu thiếu thông tin.

### 5.5. Quản lý mã nguồn và làm việc nhóm

**Khó khăn:** Các thành viên làm việc song song trên GitHub nên có thể phát sinh thay đổi mới trên nhánh `main` trong quá trình tích hợp.

**Cách xử lý:** Sử dụng Git branch để phát triển từng phần, đồng bộ các commit của nhóm trước khi merge và push lên `main`, hạn chế ghi đè mã nguồn của thành viên khác.
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
