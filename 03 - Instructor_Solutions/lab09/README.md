# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 9 — DÀNH CHO GIẢNG VIÊN
## THIẾT KẾ ĐƯỜNG DỮ LIỆU KHỐI CỘNG NHANH 4-BIT (4-BIT CARRY LOOKAHEAD ADDER - CLA)

Thư mục này chứa toàn bộ các file netlist SPICE hoàn chỉnh đã được kiểm chứng (runnable & verified 100%) và tài liệu đáp án chi tiết phục vụ công tác giảng dạy, chấm thi và hướng dẫn thực hành cho Bài 9.

---

### Danh mục tệp trong thư mục:

1. **`cla_4bit_tran.sp`**:
   - File Netlist SPICE mô phỏng đầy đủ kiến trúc phân cấp của Bộ cộng nhanh 4-bit (`cla_adder_4b`), gồm 3 tầng: 4 tế bào PG Cell $\to$ 1 khối CLG Unit $\to$ 4 tế bào Sum Cell.
   - Kiểm chứng trường hợp lan truyền số nhớ xấu nhất ($A=1111_2, B=0000_2, C_0: 0 \to 1$) và đo tự động thời gian trễ $t_{pd(C0 \to C4)} \approx 175.0\,\text{ps}$.
2. **`cla_vs_rca_benchmark.sp`**:
   - File mô phỏng đối sánh trực tiếp (Side-by-side benchmark) giữa 4-bit CLA và 4-bit RCA (Ripple Carry Adder cấu thành từ 4 tế bào Mirror Adder của Lab 06).
   - Minh chứng tốc độ lan truyền số nhớ của CLA nhanh hơn RCA tới **$1.61$ lần** ($175\,\text{ps}$ vs $282\,\text{ps}$) và trễ tổng thể nhanh hơn **$1.54$ lần**.
3. **`clg_unit_tran.sp`**:
   - Mô phỏng độc lập khối tạo số nhớ sớm 4-bit (`clg_4b`), kiểm chứng và đo đạc thời gian sinh đồng thời của từng đường số nhớ $C_1, C_2, C_3, C_4$.
4. **`cla_pex_postlayout.sp`**:
   - Netlist trích xuất ký sinh Post-layout (PEX) của toàn bộ khối `cla_adder_4b` với đầy đủ điện trở và điện dung ký sinh của các kênh định tuyến Metal1 và Metal2.
5. **`dap_an_chi_tiet_lab09.md`**:
   - Cẩm nang giảng dạy chuyên sâu: Dẫn xuất toán học đệ quy của phương trình Carry Lookahead, kỹ thuật thiết kế cổng phức hợp AOI chống suy giảm sườn xung, phân tích đánh đổi diện tích - tốc độ ($19.6\%$ diện tích đổi lấy $+61\%$ tốc độ), barem điểm chuẩn OBE/ABET và ngân hàng 5 câu hỏi vấn đáp tại bàn.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn icon **Running Man** (`Ctrl + R`).
- Nhấn `Ctrl + L` để xem kết quả các câu lệnh `.MEAS` trong file SPICE Error Log.
