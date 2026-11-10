# Báo cáo cá nhân — Nguyễn Gia Nam

## 1. Thông tin thành viên

- **Họ tên:** Nguyễn Gia Nam
- **MSSV:** 2A202603761
- **Email:** 26ai.namng@vinuni.edu.vn

## 2. Phần việc phụ trách

Trong Lab 03 — Research Agent Tool Eval, em đảm nhiệm vai trò trưởng nhóm, đồng thời phụ trách phát triển giao diện người dùng (Frontend), tích hợp AI Research Agent với Streamlit, kiểm thử tương tác thực tế và phối hợp tổng hợp bằng chứng nộp bài.

Các nhiệm vụ chính của em bao gồm:

- Xây dựng giao diện web bằng Streamlit cho phép người dùng trò chuyện trực tiếp với Research Agent.
- Tích hợp giao diện với backend có sẵn, đặc biệt là luồng Tool Calling trong `chat.py`.
- Hiển thị phản hồi của Agent, các công cụ được gọi (Tool Calling), tham số và kết quả thực thi.
- Hỗ trợ hội thoại nhiều lượt, quản lý lịch sử tương tác và xuất transcript JSON.
- Kiểm thử kết nối OpenRouter/Gemini, ghi nhận kết quả và các trường hợp lỗi.
- Triển khai giao diện lên Streamlit Community Cloud, cấu hình API key qua Secrets.
- Phối hợp cập nhật `TEAM.md`, báo cáo nhóm và chuẩn bị sản phẩm demo.

## 3. Đóng góp cụ thể

### 3.1. Xây dựng giao diện Streamlit

Em xây dựng phiên bản giao diện Research Agent tại `starter_v0/app.py` để người dùng có thể nhập yêu cầu và theo dõi quá trình Agent xử lý. Giao diện hỗ trợ hiển thị phản hồi, lịch sử hội thoại, thông tin tool được gọi và kết quả thực thi.

Ở phiên bản giao diện em triển khai, người dùng có thể lựa chọn Provider/Model, điều chỉnh số lượt hội thoại giữ ngữ cảnh và số vòng gọi công cụ tối đa. Giao diện cũng hỗ trợ xuất transcript JSON để nhóm dùng làm bằng chứng kiểm thử. Sau khi phần UI được tích hợp vào `main`, nhóm tiếp tục hoàn thiện cách trình bày giao diện.

Em đã phối hợp triển khai ứng dụng lên **Streamlit Community Cloud** để các thành viên và người đánh giá có thể truy cập qua trình duyệt mà không cần thiết lập môi trường Python cục bộ.

- **Website demo:** [Research Agent — Streamlit](https://vinuni-research-agent-nhth.streamlit.app/)
- **Mã nguồn UI:** [`starter_v0/app.py`](../../starter_v0/app.py)

### 3.2. Tích hợp hệ thống Tool Calling

Em kết nối giao diện Streamlit với logic xử lý Agent có sẵn trong `chat.py`, sử dụng hàm `run_model_tool_loop()`. Nhờ đó, Agent có thể lựa chọn công cụ, truyền arguments, nhận kết quả từ tool và tiếp tục tạo câu trả lời cho người dùng trong cùng một phiên hội thoại.

Trong quá trình kiểm thử, em quan sát các luồng gọi công cụ như `lookup` để tìm kiếm thông tin và `format` để định dạng kết quả. Chẳng hạn, với yêu cầu về ứng dụng AI trong y tế, giao diện giúp theo dõi các bước tìm nguồn và tổng hợp câu trả lời. Các kết quả thực tế được lưu trong transcript để đối chiếu thay vì chỉ đánh giá bằng nội dung trả lời cuối cùng.

Một điểm an toàn của giao diện là không cung cấp trực tiếp tool `send` để tránh hành động gửi Telegram ngoài ý muốn từ website công khai. Quy trình xin xác nhận trước khi gửi được nhóm đánh giá trong các bài test của Agent.

### 3.3. Kiểm thử kết nối AI

Em đã cấu hình và kiểm thử kết nối với OpenRouter và Gemini. Khi làm việc, em gặp một số lỗi do môi trường và API bên ngoài:

- **OpenRouter HTTP 402:** Tài khoản không đủ credit cho một số lượt chạy thử.
- **Gemini HTTP 404/503:** Một số model không khả dụng hoặc dịch vụ quá tải trong thời điểm kiểm thử.
- **Thiếu API key:** Một số công cụ lấy dữ liệu bên ngoài, đặc biệt từ X/Twitter, không thể hoàn tất yêu cầu khi môi trường chưa có `RAPIDAPI_KEY`.

Sau khi kiểm tra các model khả dụng, em sử dụng `gemini-3.5-flash-lite` và chạy preflight thành công:

```text
OK provider=gemini model=gemini-3.5-flash-lite
tool=timeline
args={'screenname': 'sama'}
```

Kết quả này xác nhận model có thể tạo lời gọi tool với arguments theo định dạng mong đợi; nó không đồng nghĩa mọi công cụ bên ngoài đều thực thi thành công.

Em cũng chạy bộ Group Eval mở rộng trên Gemini và lưu kết quả **9/12 case PASS (75%)**, **12/12 case được đo**, **0 provider errors**. Ba case chưa đạt gồm `G01`, `G06` và `G12`. Đây là một kết quả kiểm thử đối chứng bổ sung, không thay thế kết quả OpenRouter của nhóm.

- **Bằng chứng Gemini:** [`v3_B_group_gemini_20261110T224024928236.json`](../../starter_v0/runs/v3_B_group_gemini_20261110T224024928236.json)
- **Commit bổ sung run Gemini:** [`1372fac`](https://github.com/Basrot/K5-L3B-DAY03-NNTH-ResearchAgentToolEval/commit/1372fac)

### 3.4. Kiểm thử hội thoại thực tế

Em kiểm thử trực tiếp giao diện Streamlit với các tình huống tìm kiếm thông tin, yêu cầu thiếu bối cảnh, sử dụng ngữ cảnh từ lượt trước và theo dõi kết quả Tool Calling.

Ở giai đoạn đầu, một transcript `v0` với 9 lượt hội thoại ghi nhận **8 lượt có trạng thái `answered`** và **1 lượt gặp lỗi provider**. Transcript này giúp em phát hiện các hạn chế của Agent trước khi nhóm hoàn thiện các phiên bản tối ưu:

- Agent có lúc tự suy đoán tên tài khoản X dù người dùng chưa cung cấp.
- Một số lời gọi công cụ X/Twitter không lấy được dữ liệu do thiếu `RAPIDAPI_KEY`.
- Các lỗi từ provider hoặc công cụ ngoài cần được phân biệt với lỗi lựa chọn tool và arguments.

Ở giai đoạn hoàn thiện, nhóm có thêm transcript `v3` gồm 4 lượt trên OpenRouter để chứng minh luồng gọi `extract_keywords`, yêu cầu `clarify` khi thiếu tên tài khoản, sử dụng thông tin người dùng bổ sung ở lượt tiếp theo và xin xác nhận trước khi gửi Telegram. Đây là bằng chứng chung của nhóm, được dùng để bổ sung cho kiểm thử UI và báo cáo B4; việc Agent hỏi xác nhận **không có nghĩa** đã gửi Telegram thành công.

**Các transcript đối chiếu:**

- [Transcript `v0` Gemini — 9 lượt](../../starter_v0/transcripts/v0_gemini_20261110T181508022586.transcript.json)
- [Transcript `v3` Gemini](../../starter_v0/transcripts/v3_gemini_20261110T221335666627.transcript.json)
- [Transcript `v3` OpenRouter — 4 lượt](../../starter_v0/transcripts/v3_openrouter_20261110T224752771866.transcript.json)

### 3.5. Quản lý mã nguồn và tích hợp GitHub

Em triển khai phần giao diện trên nhánh `feature/nam-streamlit-ui` và phối hợp tích hợp thay đổi vào `main`. Trong quá trình làm việc nhóm, em sử dụng Git để kiểm tra trạng thái file, đồng bộ code mới nhất và chỉ commit những file cần thiết nhằm tránh đưa nhầm log lỗi hoặc file cấu hình riêng lên repository.

Commit riêng của nhánh giao diện là `82b5966` (`feat(ui): integrate Streamlit Research Agent with live tool calling`). Nhóm đã tích hợp nội dung UI vào `main`; sau đó các thành viên tiếp tục cải tiến giao diện và các thành phần Agent. Em cũng cập nhật kết quả kiểm thử Gemini Group Eval lên `main` qua commit `1372fac`.

- **Repository:** [K5-L3B-DAY03-NNTH-ResearchAgentToolEval](https://github.com/Basrot/K5-L3B-DAY03-NNTH-ResearchAgentToolEval)
- **Commit phát triển UI:** [`82b5966`](https://github.com/Basrot/K5-L3B-DAY03-NNTH-ResearchAgentToolEval/commit/82b5966)
- **Merge commit tích hợp:** [`1566ce9`](https://github.com/Basrot/K5-L3B-DAY03-NNTH-ResearchAgentToolEval/commit/1566ce9)
- **Commit Group Eval Gemini:** [`1372fac`](https://github.com/Basrot/K5-L3B-DAY03-NNTH-ResearchAgentToolEval/commit/1372fac)

## 4. Bằng chứng

**Các file và đường dẫn liên quan trực tiếp:**

- [`starter_v0/app.py`](../../starter_v0/app.py) — giao diện Streamlit tích hợp Research Agent.
- [`starter_v0/chat.py`](../../starter_v0/chat.py) — backend Tool Calling được giao diện sử dụng.
- [`starter_v0/requirements.txt`](../../starter_v0/requirements.txt) — dependency chạy ứng dụng.
- [`starter_v0/transcripts/`](../../starter_v0/transcripts/) — các transcript hội thoại của nhóm.
- [`starter_v0/runs/v3_B_group_gemini_20261110T224024928236.json`](../../starter_v0/runs/v3_B_group_gemini_20261110T224024928236.json) — Group Eval Gemini 9/12.
- [`report/team/group_report.md`](group_report.md) — báo cáo nhóm, trong đó có bảng B3, B4 và B5a.
- **Website demo:** [https://vinuni-research-agent-nhth.streamlit.app/](https://vinuni-research-agent-nhth.streamlit.app/)

**Kết quả chung của nhóm để tham chiếu (không phải toàn bộ công việc cá nhân của em):**

- OpenRouter/GPT-4o-mini: baseline `v3` đạt **20/20 PASS**.
- Group Eval OpenRouter: **10/10 PASS** trên bộ ban đầu và **12/12 PASS** trên bộ mở rộng, theo các run JSON được dẫn trong báo cáo nhóm.
- Test suite mới nhất được nhóm báo cáo đạt **104 passed, 0 failed, 0 skipped** sau khi hoàn thiện các test TODO và regression tests. Kết quả này cần được đối chiếu với mã nguồn và lần chạy `pytest` ở phiên bản `main` tương ứng.

**AI/công cụ đã sử dụng:**

- **ChatGPT:** Hỗ trợ xây dựng giao diện, hướng dẫn tích hợp Agent, phân tích lỗi và đề xuất cách kiểm thử; em kiểm tra và điều chỉnh kết quả trước khi sử dụng.
- **Visual Studio Code, Python 3.11, Streamlit:** Phát triển và chạy giao diện.
- **Gemini API, OpenRouter:** Kiểm thử khả năng Tool Calling.
- **Git/GitHub:** Quản lý phiên bản và bằng chứng đóng góp.

**Cách tự kiểm tra kết quả:**

Em chạy giao diện trên môi trường local, gửi các câu hỏi thực tế, theo dõi tool calls/arguments và đối chiếu với transcript JSON. Em kiểm tra kết nối provider bằng script preflight, xem file run khi đánh giá Agent và sử dụng GitHub để lưu mã nguồn, tài liệu và bằng chứng. Với bản triển khai Cloud, em cấu hình API key bằng Streamlit Secrets thay vì đưa khóa vào repository.

## 5. Tự đánh giá

Em đã hoàn thành phần xây dựng giao diện Streamlit, tích hợp với Research Agent có sẵn và phối hợp triển khai website công khai. Qua Lab này, em hiểu rõ hơn cách một AI Agent tiếp nhận yêu cầu, chọn công cụ phù hợp, truyền arguments, sử dụng kết quả từ API và duy trì hội thoại nhiều lượt.

Em cũng học được cách kiểm tra lỗi dựa vào transcript, log đánh giá và kết quả gọi tool thay vì chỉ nhìn vào câu trả lời cuối cùng của chatbot. Những lần gặp lỗi HTTP 402/503, thiếu API key và giới hạn quota giúp em hiểu hơn về việc triển khai ứng dụng AI ở môi trường thực tế.

Hạn chế còn lại là chất lượng trả lời và khả năng truy cập dữ liệu ngoài phụ thuộc vào model, API quota, kết nối mạng và các khóa dịch vụ. Ngoài ra, nhãn phiên bản Agent hiển thị trên UI cần được đối chiếu với cấu hình prompt/tools thực tế khi sử dụng transcript làm bằng chứng.

Em đánh giá phần đóng góp của mình đáp ứng nhiệm vụ phát triển, tích hợp và kiểm thử giao diện Agent. Em đã có mã nguồn, website triển khai, commit GitHub và các transcript/run JSON liên quan để giảng viên đối chiếu. Nếu có thêm thời gian, em muốn cải thiện khả năng xử lý lỗi API, hiển thị trạng thái công cụ rõ ràng hơn và tăng độ chính xác của thông tin cấu hình lưu trong transcript.
