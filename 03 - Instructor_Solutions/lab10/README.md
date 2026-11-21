# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 10 — DÀNH CHO GIẢNG VIÊN
## CAPSTONE PROJECT: TÍCH HỢP VI MẠCH 4-BIT REGISTERED ALU & XÁC THỰC VẬT LÝ TOÀN DIỆN

Thư mục này chứa toàn bộ các file netlist SPICE hoàn chỉnh đã được kiểm chứng (runnable & verified 100%) và tài liệu đáp án chi tiết phục vụ công tác giảng dạy, chấm thi, nghiệm thu đồ án Capstone cho Bài 10.

---

### Danh mục tệp trong thư mục:

1. **`alu_4bit_top_tran.sp`**:
   - File Netlist SPICE mô phỏng đầy đủ vi mạch Registered ALU 4-bit (`alu_4b_reg`) cấp hệ thống với quy mô **358 Transistors**.
   - Kiểm chứng trọn vẹn chương trình kiểm thử đa chu kỳ (Multi-cycle Instruction Test Sequence) qua 5 chu kỳ xung nhịp $200\,\text{MHz}$:
     - Chu kỳ 1: Lệnh `ADD` ($5 + 3 = 8$)
     - Chu kỳ 2: Lệnh `ADD` tràn ($12 + 4 = 16 \implies \text{OUT}=0, C_{out}=1, Z=1$)
     - Chu kỳ 3: Lệnh `AND` ($10 \ \& \ 12 = 8$)
     - Chu kỳ 4: Lệnh `OR` ($10 \ | \ 5 = 15$)
     - Chu kỳ 5: Lệnh `XOR` ($9 \ \oplus \ 9 = 0 \implies Z=1$)
2. **`alu_fmax_timing_sweep.sp`**:
   - Quét xung nhịp ở dải tần số cao $1.0\,\text{GHz}$ ($T = 1.0\,\text{ns}$) để đo đạc thời gian trễ chốt dữ liệu, kiểm tra vi phạm thời gian thiết lập ($t_{setup}$) và xác định tần số xung nhịp tối đa $f_{max} \approx 1.4 - 1.9\,\text{GHz}$.
3. **`alu_pex_postlayout.sp`**:
   - Netlist trích xuất ký sinh Post-layout (PEX) cấp chip tích hợp mô hình Vòng cấp nguồn bảo vệ (Power Ring VDD/GND), tính toán độ sụt áp động $IR\text{-}Drop \approx 45\,\text{mV}$ và độ trễ đường tới hạn sau đóng gói.
4. **`dap_an_chi_tiet_lab10.md`**:
   - Cẩm nang giảng dạy chuyên sâu: Nguyên lý tích hợp vi mạch SoC/Datapath, phân tích ngân sách thời gian (Timing Budget & Clock Skew), kỹ thuật thiết kế Power Ring & toàn vẹn nguồn điện (Power Integrity), barem điểm chuẩn Capstone OBE/ABET thang 10, và ngân hàng 5 câu hỏi bảo vệ đồ án vi mạch trước hội đồng.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn icon **Running Man** (`Ctrl + R`).
- Nhấn `Ctrl + L` để xem kết quả các câu lệnh `.MEAS` trong file SPICE Error Log.
