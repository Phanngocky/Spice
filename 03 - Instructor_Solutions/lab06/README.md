# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 6 — DÀNH CHO GIẢNG VIÊN
## THIẾT KẾ MẠCH CỘNG TOÀN PHẦN 1-BIT (1-BIT FULL ADDER)

Thư mục này chứa toàn bộ các file netlist SPICE hoàn chỉnh đã được kiểm chứng (runnable & verified 100%) và tài liệu đáp án chi tiết phục vụ công tác giảng dạy, chấm thi và hướng dẫn thực hành cho Bài 6.

---

### Danh mục tệp trong thư mục:

1. **`mirror_adder_tran.sp`**:
   - File Netlist SPICE mô phỏng Mạch cộng gương 28-Transistor Mirror Adder (`mirror_adder_1b`).
   - Kiểm chứng chuẩn xác đủ 8 tổ hợp bảng chân trị logic ($A, B, C_{in} \in \{0, 1\}^3$) và đo tự động thời gian trễ đường tới hạn $t_{pd(Cin \to Cout)} \approx 69.5\,\text{ps}$ và trễ tạo tổng $t_{pd(A \to Sum)} \approx 146.5\,\text{ps}$.
2. **`tg_adder_tran.sp`**:
   - Mô phỏng đối sánh kiến trúc Mạch cộng Cổng truyền 16-Transistor TG Full Adder (gồm 2 XOR TG + 1 MUX TG).
   - Đo trễ truyền qua 1 tầng đơn lẻ của TG Adder ($t_{pd(Cin \to Cout)} \approx 42.5\,\text{ps}$).
3. **`carry_chain_cascade.sp`**:
   - Mô phỏng chuỗi 4 tầng bộ cộng gợn sóng (4-bit Ripple Carry Adder) trong trường hợp xấu nhất ($A=1111, B=0000, C_{in,0}: 0 \to 1$).
   - Đo đạc thời gian lan truyền qua từng tầng ($C_1, C_2, C_3, C_{out,3}$) và chứng minh trễ tích lũy tuyến tính $O(N) = 282.0\,\text{ps}$ ($70.5\,\text{ps/stage}$).
4. **`fa_pex_postlayout.sp`**:
   - Netlist trích xuất ký sinh Post-layout (PEX) của tế bào `mirror_adder_1b` từ mặt nạ Electric VLSI.
5. **`dap_an_chi_tiet_lab06.md`**:
   - Tài liệu giảng dạy chuyên sâu: Dẫn xuất công thức trễ chuỗi bộ cộng số học, cơ chế tái sử dụng $\overline{C_{out}}$ tạo Sum, phân tích chi tiết so sánh Mirror Adder 28T vs TG Adder 16T, barem điểm thang 10 và ngân hàng câu hỏi vấn đáp tại bàn.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn icon **Running Man** (`Ctrl + R`).
- Nhấn `Ctrl + L` để xem kết quả các câu lệnh `.MEAS` trong file SPICE Error Log.
