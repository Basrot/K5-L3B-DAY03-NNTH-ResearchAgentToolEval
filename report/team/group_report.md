# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm **Phần A** (giới thiệu agent) và **Phần B** (phân tích chi tiết, kiểm thử và bằng chứng). Các kết quả đánh giá bên dưới được dẫn đến run JSON hoặc transcript cụ thể. Tiêu chí đánh giá: [RUBRIC.md](../../RUBRIC.md).

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
- URL: [Research Agent — Streamlit Cloud](https://vinuni-research-agent-nhth.streamlit.app/)
- Source code: `starter_v0/app.py`

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin hoặc xin xác nhận trước hành động gửi | không |
| `timeline` | Lấy các bài đăng gần đây của một tài khoản Twitter/X | không |
| `social_search` | Tìm kiếm bài đăng trên mạng xã hội Twitter/X theo từ khóa | không |
| `lookup` | Tra cứu thông tin và tin tức trên Internet (web search) | không |
| `fetch` | Đọc và trích xuất nội dung từ một địa chỉ URL | không |
| `format` | Định dạng các thông tin đã thu thập thành markdown digest | không |
| `send` | Gửi bản tin văn bản lên kênh Telegram sau khi có xác nhận | không |
| `policy` | Tra cứu tài liệu chính sách và quy định nội bộ của tổ chức | không |
| `papers` | Tìm kiếm bài báo khoa học học thuật trên arXiv | không |
| `paper_text` | Tải và đọc nội dung văn bản PDF của bài báo arXiv | không |
| `extract_keywords` | Trích xuất các từ khóa quan trọng và tần suất xuất hiện từ văn bản | **có (nhóm thêm)** |
| `deduplicate_sources` | Loại bỏ các URL nguồn bị trùng lặp, chuẩn hóa danh sách link | **có (nhóm thêm)** |
| `text_stats` | Tính toán số từ, số ký tự, số câu, số đoạn và ước tính thời gian đọc văn bản | **có (nhóm thêm)** |

### A3. Câu hỏi mẫu để thử

1. **Cơ bản:** Tìm 3 ứng dụng thực tế của AI trong lĩnh vực y tế và cung cấp nguồn tham khảo.
2. **Thiếu bối cảnh:** Hãy lấy 5 bài đăng gần đây nhất của tài khoản đó trên X.
3. **Đa bước:** Tìm 3 nghiên cứu gần đây trên arXiv về AI Agent, đọc nội dung hoặc phần tóm tắt của từng nghiên cứu và tổng hợp thành một bản tin ngắn kèm nguồn.

## 3. Giải pháp

### 3.1. Tối ưu System Prompt (`system_prompt.md`)
- **Loại bỏ các chỉ dẫn sai cố ý:** Xóa bỏ hoàn toàn thói quen tự suy đoán tài khoản (`sama`) hay tự bịa URL khi người dùng chưa cung cấp đầy đủ thông tin; xóa bỏ chỉ dẫn tự ý gửi bài khi chưa có xác nhận rõ ràng.
- **Thiết lập ranh giới hoạt động (Out of Scope):** Quy định rõ ràng phạm vi của Research Agent; khi gặp các yêu cầu nằm ngoài phạm vi nghiên cứu (như giải toán tích phân, viết code thuật toán Fibonacci), agent lịch sự từ chối hoặc trả lời trực tiếp mà tuyệt đối không gọi tool (`no_tool`).
- **Ép buộc hỏi lại (`clarify`):** Yêu cầu agent phải chủ động hỏi lại người dùng để bổ sung thông tin bắt buộc thay vì tự giả định.

### 3.2. Chuẩn hóa Khai báo Tool (`tools.yaml`)
- **Viết lại mô tả chi tiết:** Xác định rõ ràng chức năng, **khi nào nên dùng** và **khi nào KHÔNG nên dùng** cho từng công cụ để tránh tình trạng model chọn nhầm tool.
- **Quy chuẩn hóa Arguments:**
  - `lookup`: Quy định khi tìm tin tức (`topic="news"`), trường `query` chỉ chứa từ khóa chủ đề cốt lõi (ví dụ `"AI"`), không lặp lại từ `"news"` hay `"tin tức"`.
  - `timeline`: Quy định tên tài khoản (`screenname`) không được chứa ký tự `@`.
  - `clarify` & `send`: Thiết lập quy trình 2 bước nghiêm ngặt đối với tác vụ gửi tin Telegram — bước đầu tiên bắt buộc gọi `clarify` với `response_type="yes_no"` để xin xác nhận; chỉ khi người dùng xác nhận ở lượt sau với `confirmed=true` thì mới được phép thực thi tool `send`.

### 3.3. Các Tool mới do nhóm tự phát triển
Nhóm đã mở rộng năng lực của hệ thống bằng 3 công cụ tự phát triển độc lập (100% Python offline, không tốn credit API):
1. **`extract_keywords`:** Trích xuất từ khóa quan trọng và tần suất xuất hiện từ văn bản dài, tự động lọc bỏ stop-words đa ngữ (Anh - Việt), hỗ trợ ký tự Unicode có dấu. Agent gọi khi người dùng muốn phân tích bài báo, trích xuất từ khóa hoặc gắn tag chủ đề.
2. **`deduplicate_sources`:** Chuẩn hóa và loại bỏ các link URL nguồn bị trùng lặp (bỏ thẻ neo `#fragment`, bỏ dấu gạch chéo cuối `/`, giữ nguyên query string) và phát hiện URL không hợp lệ. Agent gọi để làm sạch danh sách nguồn trước khi tổng hợp bản tin.
3. **`text_stats`:** Tính toán các chỉ số định lượng của văn bản (số từ, số ký tự, số câu, số đoạn) và ước tính thời gian đọc dựa trên tốc độ đọc WPM. Agent gọi khi người dùng muốn đo lường dung lượng tài liệu hoặc ước tính thời gian đọc bài viết.


## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Kết quả lấy từ [`version_log.csv`](../../starter_v0/artifacts/version_log.csv) và các run JSON được liệt kê trong bảng. Chỉ sử dụng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu trước khi sửa (`system_prompt.md` + `tools.yaml` gốc) | — | 0.65 (routing: 0.75, args: 0.65, multiturn: 1.00) | `starter_v0/runs/v0_B_base_openrouter_20261110T173950199134.json` |
| v1 | `system_prompt.md`, `tools.yaml` | Bỏ chỉ dẫn xấu trong `system_prompt.md` (ép đoán mò, ép gọi tool) và làm rõ phạm vi tool trong `tools.yaml` sẽ giúp agent gọi `clarify` khi thiếu handle/URL (`R10`, `R11`) và không gọi tool khi ngoài phạm vi (`R08`, `R14`) | 0.65 | 0.90 (routing: 0.90, args: 0.90, multiturn: 0.8333) | `starter_v0/runs/v1_B_base_openrouter_20261110T180455272193.json` |
| v2 | `tools.yaml` | Thêm boundary xác nhận vào mô tả của `send` và `clarify` trong `tools.yaml` sẽ giúp agent route sang `clarify` thay vì gọi `send` ngay khi chưa có xác nhận (`R12`) | 0.90 | 0.95 (routing: 1.00, args: 0.95, multiturn: 1.00) | `starter_v0/runs/v2_B_base_openrouter_20261110T185059346257.json` |
| v3 | `tools.yaml` | Quy định rõ trong `clarify` và `send` rằng bước đầu của mọi yêu cầu gửi/đăng Telegram bắt buộc dùng `response_type="yes_no"` (không dùng `"text"` trước bước xác nhận kể cả khi nội dung chưa nêu rõ) sẽ nâng `argument_accuracy` và `case_accuracy` lên 1.00 | 0.95 | 1.00 (routing: 1.00, args: 1.00, multiturn: 1.00) | `starter_v0/runs/v3_B_base_openrouter_20261110T191036287347.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong [run baseline v0](../../starter_v0/runs/v0_B_base_openrouter_20261110T173950199134.json). Trong 20 case của `eval_base.json`, baseline `v0` đạt **13/20 PASS (65%)** và **7/20 FAIL (35%)**:

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

Bộ `starter_v0/data/eval_group.json` hiện gồm 12 case (7 single-turn và 5 multi-turn):

- **Bộ ban đầu `G01`–`G10`:** OpenRouter/`openai/gpt-4o-mini` đạt **10/10 PASS** (`starter_v0/runs/v3_B_group_openrouter_20261110T193715824551.json`), không có lỗi provider.
- **Bộ mở rộng đầy đủ `G01`–`G12` (thêm 2 case kiểm thử tool mới):**
  - OpenRouter/`openai/gpt-4o-mini` đạt **12/12 PASS** ([run JSON 12 case](../../starter_v0/runs/v3_B_group_openrouter_20261110T224703124394.json)), không có lỗi provider.
  - Gemini `gemini-3.5-flash-lite` đạt **9/12 PASS** ([run JSON Gemini](../../starter_v0/runs/v3_B_group_gemini_20261110T224024928236.json)), không có lỗi provider (3 case chưa đạt: `G01`, `G06`, `G12`).

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
| `G11_deduplicate_sources_urls` (Single-turn) | Danh sách URL nguồn phải được chuyển nguyên dạng vào `deduplicate_sources`; tool sẽ xử lý URL trùng và URL không hợp lệ. | `deduplicate_sources(urls=[...])` | **PASS** |
| `G12_text_stats_estimate` (Single-turn) | Yêu cầu đếm số từ và ước tính thời gian đọc văn bản phải gọi tool `text_stats` với đúng `text` và `wpm=250`. | `text_stats(text="Large language models are capable of complex reasoning and tool calling across various domains.", wpm=250)` | **PASS** |

*Trong bảng trên, cột Result phản ánh kết quả của **run OpenRouter 12/12**; kết quả Gemini được báo cáo riêng bên dưới (G01, G06, G12 chưa đạt). Đây là kiểm tra định tuyến và arguments theo tiêu chí eval, không thay thế đánh giá thủ công chất lượng câu trả lời.*

#### Tổng hợp kết quả Group Eval

**1. Đánh giá chính thức — OpenRouter / `openai/gpt-4o-mini`**

- **Bộ 10 case ban đầu (`G01`–`G10`, 5 single-turn + 5 multi-turn):**
  - Passed cases: **10/10 (100%)** (`case_accuracy: 1.0`, `tool_routing_accuracy: 1.0`, `argument_accuracy: 1.0`, `multiturn_accuracy: 1.0`, `provider_error_cases: 0`)
  - Run JSON: `starter_v0/runs/v3_B_group_openrouter_20261110T193715824551.json`
- **Bộ 12 case mở rộng đầy đủ (`G01`–`G12`, 7 single-turn + 5 multi-turn):**
  - Passed cases: **12/12 (100%)** (`case_accuracy: 1.0`, `tool_routing_accuracy: 1.0`, `argument_accuracy: 1.0`, `multiturn_accuracy: 1.0`, `provider_error_cases: 0`)
  - Run JSON: [v3_B_group_openrouter_20261110T224703124394.json](../../starter_v0/runs/v3_B_group_openrouter_20261110T224703124394.json)

**2. Đánh giá mở rộng đối chứng — Gemini (`gemini-3.5-flash-lite`)**

Sau khi bổ sung `G11` (`deduplicate_sources`) và `G12` (`text_stats`), nhóm thực hiện đánh giá đối chứng bổ sung với `gemini-3.5-flash-lite` trên cấu hình Agent `v3`:
- Total cases: 12 | Measured cases: 12 | Provider errors: 0 | Passed cases: **9/12**
- Case Accuracy: 75% | Tool Routing Accuracy: 75% | Argument Accuracy: 75% | Multiturn Accuracy: 80%
- Các trường hợp chưa đạt trên Gemini: `G01` (`wrong_tool`), `G06` (`wrong_arg_value`), `G12` (`wrong_tool`)
- **Run JSON:** [v3_B_group_gemini_20261110T224024928236.json](../../starter_v0/runs/v3_B_group_gemini_20261110T224024928236.json)

**3. Nhận xét**

- Trên mô hình chính thức `openai/gpt-4o-mini` (OpenRouter), Agent `v3` đạt tuyệt đối **10/10** trên bộ 10 case cốt lõi và **12/12 (100%)** trên toàn bộ 12 case mở rộng.
- Kết quả đối chứng trên Gemini (`9/12`, không gặp lỗi provider) cho thấy cùng cấu hình Agent `v3` có thể cho kết quả Tool Calling khác nhau khi thay đổi mô hình nền tảng.

### B4. Live Chat Evidence

Giao diện Streamlit (`starter_v0/app.py`) đã được kiểm thử thực tế với phiên bản `v3` trên cả hai provider `openrouter` (`openai/gpt-4o-mini`) và `gemini` (`gemini-3.5-flash-lite`), bao phủ bốn dạng tình huống: yêu cầu thường có gọi tool mới, yêu cầu thiếu thông tin, người dùng bổ sung thông tin ở lượt sau, và yêu cầu gửi/đăng lên Telegram **ở bước xin xác nhận** (không thực hiện gửi thật):

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | `Trích xuất 3 từ khóa quan trọng trong đoạn này: AI agents can help researchers organize papers. AI agents also support literature review.` | `extract_keywords(text="AI agents can help researchers organize papers. AI agents also support literature review.", top_k=3)` | `v3+p9899d34c0a9d+t5b8bc93f0bf9` (`v3_openrouter_20261110T224752771866.transcript.json`) | **PASS** (`status: answered`) — Gọi đúng tool mới `extract_keywords` và trả về 3 từ khóa theo tần suất (kết quả mang tính thống kê, không phải đánh giá ngữ nghĩa) |
| 2 | `Lấy 3 tweet mới nhất của tài khoản đó trên X giúp mình.` | `clarify(question="Bạn vui lòng cho biết tên tài khoản mà bạn muốn lấy tweet mới nhất trên X?", response_type="text")` | `v3+p9899d34c0a9d+t5b8bc93f0bf9` (`v3_openrouter_20261110T224752771866.transcript.json`) | **PASS** (`status: waiting_for_user`) — Phát hiện thiếu tên tài khoản, chủ động hỏi lại thay vì đoán mò |
| 3 | `Tài khoản là @sama nhé.` | `timeline(screenname="sama", limit=3)` | `v3+p9899d34c0a9d+t5b8bc93f0bf9` (`v3_openrouter_20261110T224752771866.transcript.json`) | **PASS** (`status: answered`) — Nối ngữ cảnh từ lượt 2, chuẩn hóa `@sama` thành `sama` và trả về 3 bài đăng theo dữ liệu do tool `timeline` cung cấp |
| 4 | `Hãy đăng bản tóm tắt 3 tweet vừa rồi lên kênh Telegram giúp mình.` | `clarify(question="Bạn xác nhận muốn gửi bản tin này lên Telegram chứ?", response_type="yes_no")` | `v3+p9899d34c0a9d+t5b8bc93f0bf9` (`v3_openrouter_20261110T224752771866.transcript.json`) | **PASS** (`status: waiting_for_user`) — Tuân thủ ranh giới an toàn, xin xác nhận `yes_no` trước khi gửi |

**Bằng chứng:**
- Source code UI: [`starter_v0/app.py`](../../starter_v0/app.py), [cấu hình Streamlit](../../starter_v0/.streamlit/config.toml).
- Transcript `v3` (OpenRouter, 4 lượt): [v3_openrouter_20261110T224752771866.transcript.json](../../starter_v0/transcripts/v3_openrouter_20261110T224752771866.transcript.json).
- Transcript `v3` (Gemini, 2 lượt): [v3_gemini_20261110T221335666627.transcript.json](../../starter_v0/transcripts/v3_gemini_20261110T221335666627.transcript.json).
- Transcript `v0` (Gemini, dùng để đối chứng): [v0_gemini_20261110T181508022586.transcript.json](../../starter_v0/transcripts/v0_gemini_20261110T181508022586.transcript.json).
- Website deploy công khai: [Research Agent — Streamlit Cloud](https://vinuni-research-agent-nhth.streamlit.app/).

**Giới hạn bằng chứng:** Transcript này chứng minh Agent **xin xác nhận trước khi gửi Telegram**, không chứng minh tin nhắn đã được gửi lên Telegram. Việc gọi `send` trên UI được tắt theo thiết kế an toàn; ca xác nhận và `send(confirmed=true)` được kiểm thử riêng trong Group Eval [G05/G10](../../starter_v0/runs/v3_B_group_openrouter_20261110T224703124394.json).

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới: `extract_keywords` | `starter_v0/tools/extract_keywords/tool.py`, `starter_v0/tools/extract_keywords/TOOL.md` | Trích các từ xuất hiện nhiều nhất sau khi lọc stop words, trả về từ khóa cùng số lần xuất hiện; không cần gọi API bên ngoài. | Kết quả dựa trên tần suất từ và danh sách stop words, không thay thế phân tích ngữ nghĩa. Kiểm tra kiểu `text` và `top_k`; trả lỗi khi input không hợp lệ. |
| Tool mới: `deduplicate_sources` | `starter_v0/tools/deduplicate_sources/tool.py`, `starter_v0/tools/deduplicate_sources/TOOL.md` | Giữ URL hợp lệ đầu tiên theo thứ tự; bỏ trùng không phân biệt hoa thường ở scheme/host, bỏ fragment và trailing slash khi so trùng, giữ query string; đếm URL trùng và không hợp lệ. | Chỉ nhận URL HTTP(S); bỏ qua item/URL không hợp lệ và báo `invalid_count`. Không có side effect hay gửi dữ liệu ra ngoài. |
| Tool mới: `text_stats` | `starter_v0/tools/text_stats/tool.py`, `starter_v0/tools/text_stats/TOOL.md` | Tính toán số từ, số ký tự, số câu, số đoạn văn và ước tính thời gian đọc (phút) dựa trên tốc độ WPM; không cần mạng bên ngoài. | Kiểm tra kiểu dữ liệu `text` và `wpm > 0`; trả về dict báo lỗi `{error: ...}` an toàn mà không làm crash chương trình. |
| Unit test: `extract_keywords` (3 test cases) | `starter_v0/tests/test_tools_todo.py` — `test_extract_keywords_happy_path_returns_top_frequent_words`, `test_extract_keywords_bad_input_from_model_handles_gracefully`, `test_extract_keywords_failure_returns_error_dict` | Bao phủ kết quả thường, input rỗng/whitespace và xử lý input sai/top_k không hợp lệ. | Ví dụ lỗi được unit test bắt nhưng eval không kiểm tra: `text=None` phải trả `invalid_input`, hoặc `top_k=0` phải trả `invalid_top_k`. |
| Unit test: `deduplicate_sources` (3 test cases) | `starter_v0/tests/test_deduplicate_sources.py` — `test_deduplicate_sources_removes_fragments_and_trailing_slashes`, `test_deduplicate_sources_rejects_non_list_input`, `test_deduplicate_sources_skips_invalid_urls_and_items` | Bao phủ chuẩn hóa URL và giữ query string, input không phải list, cùng URL/item không hợp lệ. | Ví dụ lỗi được unit test bắt nhưng eval G11 không kiểm tra: truyền `urls` không phải list phải trả `invalid_input`; G11 chỉ kiểm tra routing và truyền một list URL. |
| Unit test: `text_stats` (3 test cases) | `starter_v0/tests/test_text_stats.py` — `test_text_stats_happy_path_calculates_metrics`, `test_text_stats_bad_input_handles_gracefully`, `test_text_stats_failure_returns_error_dict` | Bao phủ đếm từ/câu/đoạn/thời gian đọc, input rỗng, ép kiểu wpm dạng chuỗi, và xử lý an toàn lỗi input. | Bắt các lỗi biên như `text=None`, `wpm <= 0` trả về error dict thay vì ném ngoại lệ làm sập agent. |
| UI (Minimalist ChatGPT-style) | `starter_v0/app.py`, `starter_v0/.streamlit/config.toml`, `starter_v0/requirements.txt` | Chạy local tại `http://localhost:8501` và deploy trên Streamlit Cloud (`https://vinuni-research-agent-nhth.streamlit.app/`); hỗ trợ đóng/mở Sidebar mượt, chọn model ngay trong hộp soạn tin nhắn, quản lý nhiều phiên chat và xuất transcript JSON. | Loại bỏ hoàn toàn tool `send` khỏi danh sách công cụ trên UI để tránh gửi Telegram ngoài ý muốn; tự động ẩn mọi API key (`[REDACTED]`) nếu xảy ra ngoại lệ. |

**Trạng thái chạy unit test (`pytest`):** Theo kết quả kiểm thử cuối được nhóm ghi nhận, toàn bộ suite đạt **104 passed, 0 failed, 0 skipped** trong `1.26s` (14 test TODO đã hoàn thiện và có 4 regression tests mới). Kết quả này thay thế log cũ `86 passed, 14 skipped`; để tái lập, chạy `python -m pytest -q` ở thư mục gốc của repo trên commit nộp bài.

### B5. Bonus Evidence

Nhóm thực hiện phần bonus **Test Challenge**, hoàn thiện các test TODO và bổ sung regression tests. Các công cụ có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được tính là công cụ mới.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Test challenge (0 skipped / regression test) | `starter_v0/tests/test_tools_todo.py`, `starter_v0/tools/format/tool.py`, `starter_v0/tools/timeline/tool.py`, `starter_v0/tools/social_search/tool.py`, `starter_v0/tools/policy/tool.py`, `starter_v0/tools/send/tool.py`, `starter_v0/tools/lookup/tool.py` | Hoàn thiện toàn bộ 14/14 test `TODO` (0 skipped) và viết thêm 4 regression tests; tổng cộng **104 passed, 0 failed, 0 skipped**. | Tất cả unit test đều chạy hoàn toàn offline thông qua fixture `fake_http` và `block_real_http` trong `tests/conftest.py`, đảm bảo không rò rỉ request mạng thật. |

**Chi tiết các bug tìm được trong tool có sẵn, cách sửa và regression test tương ứng:**
1. **`format` (`starter_v0/tools/format/tool.py`)**: Khi một phần tử trong `items` thiếu `url` (hoặc `url=None`) và không có `source`, chuỗi kết quả bị thừa dấu gạch ngang treo ở cuối dòng (`"- **Title**: Summary - "`). **Cách sửa:** Viết hàm `_format_source()` kiểm tra an toàn kiểu chuỗi và chỉ nối `" - [source](url)"` khi có dữ liệu thật. **Regression test:** `test_regression_format_item_missing_url_does_not_leave_dangling_hyphen`.
2. **`timeline` & `social_search` (`starter_v0/tools/timeline/tool.py`, `starter_v0/tools/social_search/tool.py`)**: Dùng biểu thức `int(limit or 5)` khiến khi truyền `limit=0` lại trả về `5` bài đăng (vì `0` là falsy), còn `limit=-1` cắt mảng `items[:-1]`; ngoài ra `timeline` không tự loại bỏ ký tự `@` đầu `screenname`. **Cách sửa:** Chuẩn hóa `safe_limit = 5 if limit is None else max(0, int(limit))` và `.strip().lstrip("@")` cho `screenname`. **Regression test:** `test_regression_timeline_limit_zero_returns_empty_and_strips_at_prefix`.
3. **`policy` (`starter_v0/tools/policy/tool.py`)**: Dùng `int(top_k or 3)` khiến `top_k=0` vẫn trả về 3 kết quả thay vì danh sách rỗng `[]`. **Cách sửa:** Chuẩn hóa `limit = 3 if top_k is None else max(0, int(top_k))` và trả về ngay `[]` khi `limit == 0`. **Regression test:** `test_regression_policy_top_k_zero_returns_empty_list`.
4. **`send` (`starter_v0/tools/send/tool.py`)**: Dùng `if not confirmed:` khiến khi model truyền chuỗi `"false"` hoặc `"0"` (string khác rỗng là truthy trong Python), hàng rào bảo vệ bị vượt qua và tin nhắn được gửi thẳng lên Telegram. **Cách sửa:** Chỉ cho phép gửi khi `confirmed is True` hoặc chuỗi thuộc `{"true", "1", "yes"}`. **Regression test:** `test_regression_send_string_false_confirmation_is_blocked`.

### B7. Small Local Model Challenge (bonus)

Nhóm **không đăng ký thực hiện** phần bonus chạy Small Local Model/Ollama trong lần nộp này; vì vậy không đưa số liệu hoặc run giả định. Kết quả đối chứng Gemini ở B3 là chạy trên **cloud model**, không được tính là Small Local Model Challenge.

## 5. Khó khăn và cách xử lý

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

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và bốn báo cáo cá nhân: [Nguyễn Gia Nam](2A202603761_NguyenGiaNam.md), [Đào Ngọc Hân](2A202603779_DaoNgocHan.md), [Thiều Thế Ngọc](2A202603788_ThieuTheNgoc.md), [Trần Trọng Đức Tài](2A202603732_TranTrongDucTai.md).

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  - Các sửa đổi mang tính định hướng hành vi tổng thể và ranh giới đạo đức/phạm vi hoạt động của Agent: loại bỏ thói quen đoán mò thông tin người dùng, từ chối các câu hỏi lập trình/giải toán nằm ngoài phạm vi research, và không tự tiện gọi tool khi người dùng chỉ hỏi chào hỏi thông thường.
- **Fix nào thuộc `tools.yaml`?**
  - Các quy chuẩn cụ thể về từng công cụ kỹ thuật: định dạng và quy ước tham số (`topic="news"` thì không lặp từ `"news"` trong `query`, `screenname` không chứa `@`), mô tả điều kiện khi nào dùng/không dùng, và quy định kiểu câu hỏi xác nhận `response_type="yes_no"` cho hành động nhạy cảm của `clarify` và `send`.
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Đánh giá chất lượng ngôn ngữ của câu hỏi làm rõ (`clarify`): Câu hỏi có tự nhiên, thân thiện và đi đúng trọng tâm thông tin còn thiếu hay không.
  - Đánh giá độ trung thực (faithfulness), tính đầy đủ và khả năng tránh ảo giác trong câu trả lời tổng hợp cuối cùng cho người dùng: Hệ thống chấm tự động chỉ so khớp tên tool và tham số (`routing_correct` & `args_correct`), nhưng chưa thể đánh giá văn phong và độ chính xác của nội dung tổng hợp.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**
  - *Giả thuyết:* "Nếu bổ sung cơ chế Tự sửa sai (Self-Correction Loop: khi một tool bên thứ 3 trả về lỗi HTTP 429/503 hoặc không có dữ liệu, agent tự động chuyển sang công cụ tìm kiếm dự phòng hoặc thông báo rõ ràng cho người dùng thay vì dừng lại), thì tỷ lệ hoàn thành tác vụ nghiên cứu trong điều kiện mạng thực tế sẽ nâng cao rõ rệt."

## 8. Tài liệu tham khảo

1. OpenAI Function Calling & Structured Outputs Documentation.
2. Anthropic Tool Use Reference Guide.
3. ArXiv API & Tavily Search API Documentation.
4. Streamlit Community Cloud Documentation.

