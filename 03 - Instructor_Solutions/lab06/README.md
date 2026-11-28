# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 6 — DÀNH CHO GIẢNG VIÊN
## THIẾT KẾ MẠCH CỘNG TOÀN PHẦN 1-BIT (MIRROR ADDER 28T VÀ TG ADDER)

Thư mục này chứa toàn bộ các tệp Netlist SPICE tham chiếu và tài liệu đáp án chi tiết phục vụ công tác giảng dạy cho Bài 6 (đã đồng bộ với Teacher's Book Lab 06).

---

### Danh mục tệp trong thư mục:

1. **`mirror_adder_tran.sp`**:
   - Netlist chuẩn của Mirror Adder 28T (`5N+5P+2T` Carry + `7N+7P+2T` Sum), kiểm chứng 8 tổ hợp bằng `.meas FIND` và đo các đường trễ $C_{in} \to C_{out}, A \to C_{out}, C_{in} \to Sum, A \to Sum$.
2. **`tg_adder_tran.sp`**:
   - Netlist của TG Full Adder ghép từ `xor_tg` (8T), `inv_p` (2T), `xor_tg` (8T) và MUX2 2 TG (4T) = 22 Transistors.
3. **`carry_chain_cascade.sp`**:
   - Netlist ghép nối chuỗi 4-bit Ripple Carry Adder ($N = 1 \dots 4$) để khảo sát tính tuyến tính $O(N)$ và đo $C_{out,3}, Sum_3$.
4. **`fa_pex_postlayout.sp`**:
   - Netlist tham chiếu PEX cho nội dung tùy chọn nâng cao.
5. **`dap_an_chi_tiet_lab06.md`**:
   - Tài liệu giảng dạy và đáp án chi tiết: đính chính công thức $\overline{Sum}$ và số đếm 28T/22T, đường Euler 5 transistor `B - A - Cin - A - B`, tính toán $W_{Cin} = 128\lambda$, bảng đối chuẩn và đáp án 3 câu hỏi thảo luận.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn **Run** (`Ctrl + R`), sau đó nhấn `Ctrl + L` để xem kết quả `.MEAS`.
