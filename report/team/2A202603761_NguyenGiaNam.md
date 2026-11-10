# Báo cáo cá nhân — Nguyễn Gia Nam

## 1. Thông tin thành viên

- **Họ tên:** Nguyễn Gia Nam
- **MSSV:** 2A202603761
- **Email:** 26ai.namng@vinuni.edu.vn

## 2. Phần việc phụ trách

Trong Lab 03 — Research Agent Tool Eval, em phụ trách phát triển giao diện người dùng (Frontend), tích hợp AI Research Agent với Streamlit và kiểm thử tương tác thực tế.

Các nhiệm vụ chính của em bao gồm:

- Xây dựng giao diện web bằng Streamlit cho phép người dùng trò chuyện trực tiếp với Research Agent.
- Tích hợp giao diện với backend có sẵn trong `agent.py` và `chat.py`.
- Hiển thị phản hồi của Agent, các công cụ được gọi (Tool Calling), tham số và kết quả thực thi.
- Hỗ trợ hội thoại nhiều lượt và lưu lịch sử tương tác.
- Kiểm thử Agent với API Gemini, ghi nhận kết quả và các trường hợp lỗi.
- Lưu transcript JSON phục vụ đánh giá và làm bằng chứng.
- Phối hợp hoàn thiện tài liệu và chuẩn bị giao diện demo cho nhóm.

## 3. Đóng góp cụ thể

### 3.1. Xây dựng giao diện Streamlit

Em đã tạo file `starter_v0/app.py` để xây dựng giao diện Research Agent.

Giao diện bao gồm khu vực nhập câu hỏi, hiển thị phản hồi của AI, lịch sử hội thoại và thanh sidebar quản lý cấu hình.

Người dùng có thể lựa chọn provider, model, phiên bản Agent, số lượt hội thoại giữ ngữ cảnh và số vòng gọi công cụ tối đa.

### 3.2. Tích hợp hệ thống Tool Calling

Em đã kết nối giao diện Streamlit với logic xử lý Agent có sẵn trong `chat.py`, sử dụng `run_model_tool_loop()`.

Hệ thống cho phép Agent tự lựa chọn và thực thi các công cụ theo yêu cầu của người dùng.

Trong quá trình kiểm thử, Agent đã thực hiện được chuỗi gọi công cụ:

`lookup → format → trả lời người dùng`

Ví dụ: Khi yêu cầu tìm 5 thông tin về ứng dụng AI trong chẩn đoán y tế, Agent sử dụng `lookup` để tìm nguồn trên web, sau đó dùng `format` để tạo bản tổng hợp Markdown kèm nguồn tham khảo.

### 3.3. Kiểm thử kết nối AI

Em đã cấu hình và kiểm thử kết nối với các provider OpenRouter và Gemini.

Ban đầu, OpenRouter gặp lỗi 402 do không đủ credit. Một số model Gemini gặp lỗi 404 hoặc 503.

Sau khi kiểm tra các model khả dụng, em đã sử dụng `gemini-3.5-flash-lite` và chạy thành công preflight:

```text
OK provider=gemini model=gemini-3.5-flash-lite
tool=timeline
args={'screenname': 'sama'}
```

Kết quả này xác nhận model có khả năng tạo lời gọi công cụ với arguments.

### 3.4. Kiểm thử hội thoại thực tế

Em đã thực hiện kiểm thử trực tiếp trên giao diện Streamlit, gồm 9 lượt hội thoại trong một transcript.

Kết quả ghi nhận:

- 8 lượt có trạng thái `answered`.
- 1 lượt gặp lỗi provider.
- Agent gọi được các công cụ `lookup`, `format`, `timeline`, `social_search`.
- Agent thực hiện được việc tìm kiếm và tổng hợp thông tin có nguồn tham khảo.
- Hội thoại có khả năng sử dụng ngữ cảnh từ các lượt trước.

Trong quá trình kiểm thử, em cũng phát hiện các hạn chế:

- Agent tự suy đoán tên tài khoản X khi người dùng chưa cung cấp đầy đủ thông tin.
- Các công cụ lấy dữ liệu X không thực thi thành công do thiếu `RAPIDAPI_KEY` trong môi trường kiểm thử.
- Một số yêu cầu gặp lỗi Gemini 503 do dịch vụ quá tải.

Những lỗi này được giữ lại trong transcript làm bằng chứng để nhóm phân tích và tối ưu.

### 3.5. Quản lý mã nguồn và tích hợp GitHub

Em thực hiện công việc trên branch `feature/nam-streamlit-ui`, sau đó merge thay đổi vào `main` trên máy.

Các thay đổi bao gồm giao diện Streamlit, cập nhật thư viện trong `requirements.txt` và bổ sung transcript kiểm thử.

Em sử dụng Git để quản lý phiên bản, commit mã nguồn và đồng bộ các thay đổi với repository của nhóm.

## 4. Bằng chứng

**File đã thực hiện:**

- `starter_v0/app.py` — giao diện Streamlit tích hợp Research Agent.
- `starter_v0/requirements.txt` — bổ sung dependency Streamlit.
- `starter_v0/transcripts/v0_gemini_20261110T181508022586.transcript.json` — bằng chứng kiểm thử thực tế.

**Commit GitHub:**

- Merge commit cục bộ: `1566ce9`.
- Link commit/PR trên GitHub: [Bổ sung sau khi xác nhận đã push thành công].

**AI/công cụ đã sử dụng:**

- ChatGPT: Hỗ trợ xây dựng code Streamlit, hướng dẫn tích hợp Agent, phân tích lỗi và đề xuất phương pháp kiểm thử.
- Visual Studio Code: Viết, chỉnh sửa và chạy mã nguồn.
- Python 3.11, Streamlit: Xây dựng và vận hành giao diện.
- Gemini API: Kiểm thử mô hình AI và khả năng Tool Calling.
- Git/GitHub: Quản lý mã nguồn và ghi nhận đóng góp.

**Cách tự kiểm tra kết quả:**

Em trực tiếp chạy ứng dụng trên môi trường local, gửi câu hỏi thực tế, quan sát các tool được gọi và đối chiếu với transcript JSON. Em cũng kiểm tra trạng thái hoạt động của provider thông qua script preflight và xem log khi Agent gặp lỗi.

## 5. Tự đánh giá

Em đã hoàn thành phần xây dựng giao diện Streamlit, tích hợp với Research Agent có sẵn và thực hiện kiểm thử hội thoại thực tế.

Qua bài Lab này, em hiểu rõ hơn cách một AI Agent nhận yêu cầu, quyết định sử dụng công cụ, truyền arguments và xử lý kết quả từ các API bên ngoài.

Em cũng học được cách kiểm tra lỗi dựa trên transcript thay vì chỉ nhìn vào câu trả lời cuối cùng của chatbot.

Điểm còn hạn chế là giao diện và quá trình kiểm thử vẫn phụ thuộc vào chất lượng kết nối của provider, quota API và cấu hình của các công cụ bên ngoài. Em cần tiếp tục kiểm tra phiên bản Agent cuối cùng sau khi nhóm hoàn thành tối ưu v1–v3, đồng thời hoàn thiện việc triển khai website công khai để phục vụ demo.

Em đánh giá phần đóng góp của mình đã đáp ứng mục tiêu xây dựng và kiểm thử giao diện Agent, có mã nguồn và bằng chứng thực nghiệm để đối chiếu.