# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 7 — DÀNH CHO GIẢNG VIÊN
## KỸ THUẬT LOGIC ĐỘNG VÀ LOGIC DOMINO (DYNAMIC & DOMINO CMOS LOGIC)

Thư mục này chứa toàn bộ các file netlist SPICE hoàn chỉnh đã được kiểm chứng (runnable & verified 100%) và tài liệu đáp án chi tiết phục vụ công tác giảng dạy, chấm thi và hướng dẫn thực hành cho Bài 7.

---

### Danh mục tệp trong thư mục:

1. **`dynamic_charge_sharing.sp`**:
   - File Netlist SPICE kiểm chứng thực nghiệm hiện tượng chia sẻ điện tích (Charge Sharing) giữa nút động $C_X$ và nút nội $C_{int}$ trong nhánh NMOS.
   - Đối sánh trực tiếp 2 trường hợp: Cổng không có Keeper ($V_X$ tụt sụt nghiêm trọng từ $5.0\,\text{V}$ xuống $2.94\,\text{V}$, gây nguy cơ lật giả) vs Cổng có Weak PMOS Keeper ($V_X$ được phục hồi an toàn về $5.0\,\text{V}$).
2. **`domino_4input_tran.sp`**:
   - Mô phỏng Transient cổng Domino OR 4-ngõ vào chuẩn (`domino_or4_x1`) ở tần số xung nhịp $100\,\text{MHz}$.
   - Đo tự động thời gian trễ đánh giá $t_{pd,eval} \approx 78.5\,\text{ps}$, công suất tiêu tán trung bình $P_{dyn} \approx 0.185\,\text{mW}$ và kiểm chứng tính đơn điệu tăng (Monotonically rising).
3. **`keeper_sizing_sweep.sp`**:
   - Mô phỏng quét kích thước Keeper PMOS ($W_{kp} = 0.6\,\mu\text{m}, 1.2\,\mu\text{m}, 1.8\,\mu\text{m}, 2.4\,\mu\text{m}$).
   - Phân tích sự đánh đổi kỹ thuật (Trade-off) giữa khả năng chống rò/chia sẻ điện tích và hiện tượng tranh chấp dòng điện (Keeper Contention), chứng minh điểm tối ưu tại $W_{kp} \approx 0.1 - 0.15 \times W_{PDN,eq}$.
4. **`domino_pex_postlayout.sp`**:
   - Netlist trích xuất ký sinh Post-layout (PEX) của tế bào `domino_or4_x1` từ mặt nạ Electric VLSI với đầy đủ điện trở và điện dung ký sinh nút động và khuếch tán.
5. **`dap_an_chi_tiet_lab07.md`**:
   - Tài liệu giảng dạy chuyên sâu: Dẫn xuất vật lý - toán học về dòng rò dưới ngưỡng, thời gian giữ điện tích tối đa ($t_{hold,max}$), cơ chế chia sẻ điện tích, nguyên lý tính đơn điệu của Domino Logic, barem điểm chuẩn OBE/ABET và ngân hàng câu hỏi vấn đáp tại bàn.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn icon **Running Man** (`Ctrl + R`).
- Nhấn `Ctrl + L` để xem kết quả các câu lệnh `.MEAS` trong file SPICE Error Log.
