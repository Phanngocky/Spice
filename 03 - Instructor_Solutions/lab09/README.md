# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 9 — DÀNH CHO GIẢNG VIÊN
## THIẾT KẾ ĐƯỜNG DỮ LIỆU KHỐI CỘNG NHANH 4-BIT (4-BIT CLA)

Thư mục này chứa toàn bộ các tệp Netlist SPICE tham chiếu và tài liệu đáp án chi tiết phục vụ giảng dạy Bài 9 (đã đồng bộ với Teacher's Book Lab 09). *(Lưu ý: Sinh viên tự dựng mạch và testbench theo hướng dẫn trong Handout, không trỏ đường dẫn tới thư mục đáp án này).*

---

### Danh mục tệp trong thư mục:

1. **`clg_unit_tran.sp`**:
   - Netlist kiểm chứng khối tạo số nhớ song song `clg_4b` (4 cổng AOI + 4 INV = 76T).
2. **`cla_4bit_tran.sp`**:
   - Mô phỏng khối `cla_adder_4b` tích hợp 3 tầng (`pg_cell`, `clg_4b`, `sum_cell`), kiểm chứng chức năng và đo trễ $C_0 \to C_4, C_0 \to S_3$ và $A, B \to C_4, S_3$.
3. **`cla_vs_rca_benchmark.sp`**:
   - Kịch bản chạy song song CLA 4-bit và RCA 4-bit (`mirror_adder_1b` từ Bài 6) dưới cùng điều kiện lái và tải $50\,\text{fF}$.
4. **`cla_pex_postlayout.sp`**:
   - Netlist tham chiếu PEX cho nội dung tùy chọn nâng cao.
5. **`dap_an_chi_tiet_lab09.md`**:
   - Tài liệu giảng dạy và đáp án chi tiết: kiểm kê $76\text{T}$ CLG, tổng $132\text{T}/148\text{T}/164\text{T}$, phân tích $\Sigma W$ ($1152\lambda$ vs $2288\lambda$), tải Fan-in trên $P_1, P_2$ ($192\lambda$) và đáp án 3 câu hỏi thảo luận.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn **Run** (`Ctrl + R`), sau đó nhấn `Ctrl + L` để xem kết quả `.MEAS`.
