---
name: vlsi-lab-bookbuilder
description: Xây dựng lại bộ giáo trình thực hành VLSI/vi mạch CMOS thành cặp Student Book (handout sinh viên) và Teacher Book (gói giảng viên có lý thuyết chi tiết, kịch bản lên lớp, đáp án) cho từng bài lab, dùng công cụ miễn phí LTspice, Electric VLSI và thư viện MOSIS C5. Dùng skill này bất cứ khi nào người dùng nhắc đến viết lại, rà soát, hoàn thiện hay tiếp tục bài lab VLSI, student book, teacher book, handout, giáo trình thực hành thiết kế vi mạch, pre-lab, rubric, đáp án giảng viên, hoặc các bài như inverter, NAND/NOR, logical effort, flip-flop, full adder, SRAM, CLA, ALU 4-bit, kể cả khi không nói chữ skill. Use for rewriting VLSI lab handouts and instructor guides with verified numbers.
---

# Dựng lại bộ giáo trình thực hành VLSI (Student Book + Teacher Book)

Skill này biến một bài lab VLSI đã có (thường là tệp .md hoặc .docx) thành **hai tài liệu tách riêng**:

- **Student Book:** handout cho sinh viên, không có đáp án.
- **Teacher Book:** gói giảng viên, đọc trước khi lên lớp: kế hoạch buổi, lý thuyết chi tiết, kịch bản từng phần, câu hỏi thường gặp, vấn đáp, đáp án và netlist tham chiếu.

Bối cảnh của người dùng: học phần Thiết kế VLSI (3 tín chỉ, 24 LT + 6 BT + 15 ĐA), sinh viên Việt Nam, **chưa có phần mềm chuyên dụng**, nên thực hành bằng LTspice + Electric VLSI + MOSIS C5 (miễn phí). Mục tiêu là sinh viên có kỹ năng thực tế: mô phỏng SPICE, đo trễ/công suất, layout, DRC, LVS, trích ký sinh.

Lab 0 đã được viết lại làm **bài mẫu**; xem `references/roadmap_labs.md` để biết trạng thái từng bài.

## Vì sao tách hai tài liệu và vì sao phải kiểm số

Handout lẫn đáp án khiến sinh viên chép số thay vì đo, và giảng viên không có chỗ ghi lý thuyết sâu hơn mức sinh viên cần. Ngoài ra, khi rà soát bộ lab gốc, nhiều lỗi nằm ở **số liệu và mâu thuẫn nội bộ** (đếm transistor sai, tiêu chí tự mâu thuẫn, số "đo" thực ra là số tính tay). Vì vậy mọi con số định lượng phải qua cổng kiểm ở bước 5.

## Quy trình

### Bước 0. Xác định trạng thái
1. Đọc `references/roadmap_labs.md` và nếu có bộ nhớ dự án thì đọc ghi chú về học phần VLSI. Xác định lab nào đã xong, lab nào đang làm.
2. Hỏi người dùng (một câu) nếu chưa rõ: bài nào, và quỹ giờ thực tế (xem bước 2). Không hỏi lại điều đã có trong lịch sử hội thoại.

### Bước 1. Nạp tài liệu gốc
- Tệp .rar: dùng `python scripts/rar5_extract.py <tệp.rar> <thư mục>` (RAR5, không nén liền khối, không bộ lọc; kiểm CRC). Nếu thất bại, nhờ người dùng gửi lại dạng .zip hoặc thư mục.
- Tệp .md/.docx/.pdf: đọc toàn bộ phần lý thuyết, pre-lab, in-lab, rubric. Đọc kỹ, không đọc lướt: lỗi hay nằm ở phần tính toán.

### Bước 2. Rà soát bài gốc
1. Chạy `python scripts/lint_lab.py <tệp> --role student` để bắt ký tự lạ, bảng hỏng, ảnh thiếu, từ tuyệt đối, rò đáp án.
2. Đối chiếu `references/fix_ledger.md`: mỗi lab đã có danh sách lỗi đã phát hiện. Sửa tất cả, và tự tìm thêm.
3. Kiểm số bằng `python scripts/quick_checks.py` (RC, V_M, R_on, trễ inverter, chuỗi đệm, SRAM). Đây là mô hình bậc hai, **không phải Level 3 của C5**; chỉ dùng để phát hiện mâu thuẫn, không dùng làm số đo.
4. Chốt phạm vi bài: bao nhiêu phút, phần nào bắt buộc/tiêu chuẩn/thử thách, có layout không. Mặc định theo `roadmap_labs.md` (layout chỉ ở Lab 1, 3, 10). Nếu quỹ giờ chưa được chốt, nêu giả định và cho người dùng sửa.

### Bước 3. Viết Student Book
Theo `assets/student_book_template.md`. Quy tắc cốt lõi:
- Mục tiêu đo được; có cổng kiểm Pre-lab; mỗi Ex có **Sản phẩm** và **Câu hỏi kiểm tra**.
- Số trong Pre-lab **khác** số trong ví dụ lý thuyết, để sinh viên không chép lại từ chính tài liệu.
- Không có đáp án, không điền sẵn kết quả đo, không trỏ tới thư mục đáp án.
- Mỗi phép đo phải được so với lý thuyết bằng sai lệch tương đối, kèm ngưỡng chấp nhận.
- Rubric thang 10, ánh xạ vào tiêu chí đánh giá của đề cương.

### Bước 4. Viết Teacher Book
Theo `assets/teacher_book_template.md` (các phần A–F). Phần **B. Kiến thức nền** là phần người dùng yêu cầu chi tiết nhất: giải thích *vì sao*, có suy dẫn ngắn, có phép kiểm chéo, có giới hạn của mô hình, và nối sang chương tương ứng của đề cương. Phần **C** là kịch bản theo phút. Phần **F** mới chứa đáp án; cột "Đo" để trống cho giảng viên điền sau khi chạy.

### Bước 5. Cổng kiểm trước khi giao
Đọc `references/verification_rules.md` và tự kiểm từng điểm:
- Mỗi con số có nguồn: suy dẫn, tính bằng script, hay đo. Gắn nhãn trạng thái; **không ghi "mô phỏng cho thấy" nếu chưa chạy**.
- Đếm transistor, tổng điểm rubric, tổng thời gian buổi đều cộng lại đúng.
- Handout không rò đáp án; teacher book không mâu thuẫn với handout.
- Chạy lại `lint_lab.py` trên bản cuối (xuất `.md` bằng Docs export nếu cần).

### Bước 6. Giao sản phẩm
- Có công cụ Claude Docs: tạo **hai tài liệu riêng** (xem `references/tool_notes.md`, phần Claude Docs). Không có: xuất hai tệp .md.
- Trả lời người dùng ngắn gọn: liên kết hai tài liệu, danh sách thay đổi chính so với bản gốc, **những gì chưa kiểm** (đặc biệt chưa chạy LTspice/Electric), và đề nghị bài kế tiếp. Cập nhật trạng thái trong `roadmap_labs.md` nếu skill được chỉnh sửa lại, hoặc ghi vào bộ nhớ dự án.

## Nguyên tắc viết (và lý do)

- **Tính trước, đo sau, so sánh, giải thích chênh lệch.** Đây là thói quen nghề cần hình thành; mọi lab xoay quanh nó.
- **Nói rõ giới hạn của mô hình.** Ví dụ 0,69·R·C thường thấp hơn trễ đo của cổng thật; để sinh viên tự phát hiện ở lab sau thay vì giấu.
- **Không kết luận định sẵn.** Câu hỏi kiểu "có xứng đáng không" làm lộ đáp án; đổi thành "dự đoán, đo, giải thích".
- **Tránh từ tuyệt đối** ("hoàn toàn", "luôn", "tuyệt đối", "100%"): viết điều kiện áp dụng.
- **Kiểm chéo hai phép đo độc lập** khi có thể (ví dụ t_r · f_c ≈ 0,35).
- **Dùng ký hiệu Unicode thay LaTeX** trong Docs; bảng không chứa ký tự gạch đứng trong ô.
- Ngôn ngữ: tiếng Việt, dấu phẩy thập phân, đơn vị SI có khoảng trắng; thuật ngữ Anh giữ lần đầu kèm giải nghĩa. Chi tiết trong `references/style_vi.md`.

## Tệp đi kèm

| Tệp | Khi nào đọc |
|---|---|
| `references/roadmap_labs.md` | Đầu mỗi phiên: trạng thái, ánh xạ chương, quỹ giờ |
| `references/fix_ledger.md` | Bước 2: lỗi đã biết của từng lab gốc |
| `references/verification_rules.md` | Bước 5: cổng kiểm |
| `references/tool_notes.md` | Khi viết lệnh LTspice/Electric hoặc tạo Docs |
| `references/style_vi.md` | Khi viết |
| `assets/student_book_template.md`, `assets/teacher_book_template.md` | Bước 3 và 4 |
| `scripts/lint_lab.py`, `scripts/quick_checks.py`, `scripts/rar5_extract.py` | Bước 1, 2, 5 |
