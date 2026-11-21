# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 4 — DÀNH CHO GIẢNG VIÊN
## CỔNG TRUYỀN (TRANSMISSION GATE) VÀ BỘ DỒN KÊNH MUX MỨC TRANSISTOR

Thư mục này chứa toàn bộ các file netlist SPICE hoàn chỉnh đã được kiểm chứng (runnable & verified 100%) và tài liệu đáp án chi tiết phục vụ công tác giảng dạy, chấm thi và hướng dẫn thực hành cho Bài 4.

---

### Danh mục tệp trong thư mục:

1. **`tg_transmission_dc_tran.sp`**:
   - File Netlist SPICE khảo sát và đối chiếu trực tiếp 3 nhánh: NMOS Pass Transistor (Weak '1', $V_{max} \approx 3.63\,\text{V}$), PMOS Pass Transistor (Weak '0', $V_{min} \approx 0.86\,\text{V}$), và CMOS Transmission Gate (Full Rail-to-Rail $0.0\,\text{V} \to 5.0\,\text{V}$).
   - Chứa câu lệnh `.MEAS` tự động đo điện áp đỉnh-đáy và thời gian trễ $t_{pd,TG}$.
2. **`mux2_tg_logic_tran.sp`**:
   - Mô phỏng Bộ dồn kênh MUX 2:1 dùng Cổng truyền (`mux2_tg`) với 2 luồng dữ liệu $D_0$ ($25\,\text{MHz}$) và $D_1$ ($50\,\text{MHz}$), tín hiệu chọn $S$ ($12.5\,\text{MHz}$).
   - Kiểm chứng trọn vẹn chức năng dồn kênh không xung đột và đo thời gian trễ $D_0 \to Y$, $D_1 \to Y$, và $S \to Y$.
3. **`mux4_tg_tran.sp`**:
   - Mô phỏng Bộ dồn kênh MUX 4:1 ghép từ cây phân cấp 3 tế bào `mux2_tg` (18 Transistors).
   - Kiểm chứng đầy đủ 4 tổ hợp chọn $(S_1, S_0) \in \{00, 01, 10, 11\}$.
4. **`mux2_pex_postlayout.sp`**:
   - Netlist trích xuất ký sinh Post-layout (PEX) của tế bào `mux2_tg` từ mặt nạ Electric VLSI.
5. **`dap_an_chi_tiet_lab04.md`**:
   - Tài liệu giảng dạy chuyên sâu: Dẫn xuất giải tích Body Effect, phương trình điện áp đỉnh phi tuyến, cơ chế điện trở phẳng $R_{TG}$, trễ Elmore chuỗi TG $O(N^2)$, barem điểm thang 10 và ngân hàng câu hỏi vấn đáp tại bàn.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn icon **Running Man** (`Ctrl + R`).
- Nhấn `Ctrl + L` để xem kết quả các câu lệnh `.MEAS` trong file SPICE Error Log.
