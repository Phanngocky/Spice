# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 7 — DÀNH CHO GIẢNG VIÊN
## KỸ THUẬT LOGIC ĐỘNG VÀ LOGIC DOMINO (DYNAMIC & DOMINO CMOS LOGIC)

Thư mục này chứa toàn bộ các tệp Netlist SPICE tham chiếu và tài liệu đáp án chi tiết phục vụ giảng dạy Bài 7 (đã đồng bộ với Teacher's Book Lab 07). *(Lưu ý: Sinh viên sử dụng khung Netlist trích trực tiếp trong Handout, không trỏ đường dẫn tới thư mục đáp án này).*

---

### Danh mục tệp trong thư mục:

1. **`dynamic_charge_sharing.sp`**:
   - Mô phỏng mạch thử **2-NMOS nối tiếp** ($C_X = 20\,\text{fF}, C_{int} = 14\,\text{fF}$) để quan sát hiện tượng chia sẻ điện tích giữa hai nhánh (không Keeper vs có Keeper).
2. **`domino_or4_tran.sp` / `domino_4input_tran.sp`**:
   - Mô phỏng cổng Domino OR 4-ngõ vào (`domino_or4_x1`, 9T) kèm Low-skew Inverter $16\lambda/8\lambda$ ($V_M \approx 2.27\,\text{V}$) và kiểm chứng các tổ hợp Precharge/Evaluate.
3. **`keeper_sizing_sweep.sp`**:
   - Kịch bản `.step param` quét kích thước Keeper để đo đánh đổi giữa $t_{pd,eval}$ và độ sụt áp $V_{X,min}$.
4. **`domino_pex_postlayout.sp`**:
   - Netlist tham chiếu PEX cho nội dung tùy chọn nâng cao.
5. **`dap_an_chi_tiet_lab07.md`**:
   - Tài liệu giảng dạy và đáp án chi tiết: đính chính Low-skew Inverter ($2.273\,\text{V}$), giới hạn công thức Charge Sharing, tỉ số dòng Keeper/PDN, bảng đối chuẩn $\Sigma W / C_{in}$ và đáp án 3 câu hỏi thảo luận.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn **Run** (`Ctrl + R`), sau đó nhấn `Ctrl + L` để xem kết quả `.MEAS`.
