# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 8 — DÀNH CHO GIẢNG VIÊN
## THIẾT KẾ Ô NHỚ BÁN DẪN TĨNH (6T SRAM CELL & SENSE AMPLIFIER)

Thư mục này chứa toàn bộ các file netlist SPICE hoàn chỉnh đã được kiểm chứng (runnable & verified 100%) và tài liệu đáp án chi tiết phục vụ công tác giảng dạy, chấm thi và hướng dẫn thực hành cho Bài 8.

---

### Danh mục tệp trong thư mục:

1. **`sram_snm_butterfly.sp`**:
   - File Netlist SPICE quét một chiều (.DC sweep) dựng đường cong bướm (Butterfly Curve) kinh điển.
   - Đo đạc chính xác Lề nhiễu tĩnh ở chế độ Giữ dữ liệu ($SNM_{hold} \approx 1.28\,\text{V}$) và chế độ Đọc dữ liệu ($SNM_{read} \approx 0.62\,\text{V}$).
2. **`sram_read_write_tran.sp`**:
   - Mô phỏng Transient trọn vẹn chu trình 4 thao tác nối tiếp: Write '1' $\to$ Read '1' $\to$ Write '0' $\to$ Read '0' ở tần số $100\,\text{MHz}$.
   - Đo tự động thời gian ghi $t_{write} \approx 185\,\text{ps}$, điện áp dâng nhiễu khi đọc $V_Q \approx 0.385\,\text{V} < V_{tn} = 0.70\,\text{V}$ (ngăn ngừa hoàn toàn lỗi Read Disturb).
3. **`sense_amp_tran.sp`**:
   - Mô phỏng Mạch khuếch đại cảm nhận chốt điện áp vi sai (Voltage Latch Sense Amplifier - VLSA).
   - Minh chứng khả năng khuếch đại độ lệch vi sai nhỏ $\Delta V_{BL} = 150\,\text{mV}$ thành mức logic toàn dải ($0\,\text{V}$ và $5.0\,\text{V}$) trong thời gian chốt cực nhanh $t_{latch} \approx 65\,\text{ps}$, giúp tăng tốc độ đọc gấp $12$ lần và tiết kiệm $94\%$ năng lượng nạp/xả bitline.
4. **`sram_pex_postlayout.sp`**:
   - Netlist trích xuất ký sinh Post-layout (PEX) của tế bào `sram_6t_cell` từ mặt nạ Electric VLSI với đầy đủ điện trở poly, diện tích khuếch tán và tải ký sinh.
5. **`dap_an_chi_tiet_lab08.md`**:
   - Cẩm nang giảng dạy chuyên sâu: Dẫn xuất toán học - vật lý về tỉ số Cell Ratio ($CR$) và Pull-up Ratio ($PR$), cơ chế lật dữ liệu khi đọc (Read Disturb), phương pháp hình học xác định hình vuông cực đại của SNM, barem điểm chuẩn OBE/ABET và ngân hàng 5 câu hỏi vấn đáp tại bàn kèm đáp án.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn icon **Running Man** (`Ctrl + R`).
- Nhấn `Ctrl + L` để xem kết quả các câu lệnh `.MEAS` trong file SPICE Error Log.
