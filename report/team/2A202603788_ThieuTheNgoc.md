# Báo cáo cá nhân — Thiều Thế Ngọc

## 1. Thông tin thành viên

- Họ tên: Thiều Thế Ngọc
- MSSV: 2A202603788
- Email: 26ai.ngoctt@vinuni.edu.vn

## 2. Phần việc phụ trách

- CP2 — phân tích lỗi còn lại của baseline v1 và tối ưu khai báo tool cho v2.
- Hỗ trợ phần evaluation: kiểm tra expected behavior của case R12 và chuẩn bị đối chiếu kết quả sau khi nhóm chạy v2 với đủ API key.

## 3. Đóng góp cụ thể

- Đọc kết quả `R12_confirm_before_send` trong run v1: agent gọi `send` với `confirmed=false` thay vì hỏi người dùng xác nhận trước.
- Chỉnh riêng khai báo `clarify` và `send` trong `starter_v0/artifacts/tools.yaml`: yêu cầu `clarify` dùng `response_type="yes_no"` trước hành động gửi, không coi yêu cầu gửi ban đầu là xác nhận, và chỉ gọi `send` sau khi người dùng xác nhận rõ ràng ở lượt sau với `confirmed=true`.
- Giữ thay đổi v2 tập trung vào lỗi R12; không thay đổi system prompt hoặc quy tắc chuyển nguồn ở M06 trong phần chỉnh sửa này.
- Chưa ghi nhận kết quả v2: cần nhóm chạy lại bằng cấu hình API đầy đủ để xác minh và lưu run hợp lệ.

## 4. Bằng chứng

- File/commit/PR:
    - `starter_v0/artifacts/tools.yaml`
    - Commit `55fb0c7` (`fix: update R12 tool.yaml`)
    - Run v1 tham chiếu: `starter_v0/runs/v1_B_base_openrouter_20261110T180455272193.json`, case `R12_confirm_before_send`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
    - Dùng Copilot/ChatGPT để hỗ trợ đọc run và rà soát wording của tool declaration.
    - Tự đối chiếu expected behavior của R12 trong `starter_v0/data/eval_base.json` với actual tool call trong run v1 và kiểm tra diff của commit.

## 5. Tự đánh giá

- Thay đổi bám đúng lỗi R12 và chỉ sửa khai báo liên quan đến xác nhận gửi. Cần phối hợp chạy eval v2 bằng cấu hình đầy đủ, kiểm tra R12 pass và các case khác không bị hồi quy trước khi kết luận hiệu quả.
