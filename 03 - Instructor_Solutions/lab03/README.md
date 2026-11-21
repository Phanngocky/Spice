# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 3 — DÀNH CHO GIẢNG VIÊN
## CỔNG PHỨC HỢP AOI21 VÀ TỐI ƯU TRỄ THEO PHƯƠNG PHÁP LOGICAL EFFORT

Thư mục này chứa toàn bộ các file netlist SPICE hoàn chỉnh đã được kiểm chứng (runnable & verified 100%) và tài liệu đáp án chi tiết phục vụ công tác giảng dạy, chấm thi và hướng dẫn thực hành cho Bài 3.

---

### Danh mục tệp trong thư mục:

1. **`aoi21_logic_tran.sp`**:
   - File Netlist SPICE kiểm chứng toàn bộ 8 tổ hợp bảng chân trị logic ($A, B, C \in \{0, 1\}^3$) của cổng AOI21 $Y = \overline{(A \cdot B) + C}$.
   - Chứa câu lệnh `.MEAS` tự động đo thời gian trễ $t_{pHL}, t_{pLH}$ của ngõ vào $C$ và ngõ vào $A$.
2. **`logical_effort_meas.sp`**:
   - Mạch đo 4 nhánh song song quét tỉ số Fan-out $h = 1, 2, 3, 4$ ($C_L = 20\,\text{fF}, 40\,\text{fF}, 60\,\text{fF}, 80\,\text{fF}$).
   - Dùng để xác định thực nghiệm nỗ lực logic $g_{meas}$ (độ dốc slope) và trễ ký sinh $p_{meas}$ (giao điểm intercept) qua phương pháp hồi quy tuyến tính.
3. **`buffer_chain_opt.sp`**:
   - Mô phỏng thực nghiệm bài toán chuỗi đệm lái tải cực nặng $C_L = 1.0\,\text{pF}$ ($H = 50$).
   - So sánh trực tiếp giữa Kịch bản A (Inverter đơn $1\times$ lái trực tiếp) và Kịch bản B (Chuỗi đệm 3 tầng tối ưu theo Logical Effort với $\hat{f} = 3.68$).
   - Chứng minh trễ giảm từ $2.28\,\text{ns}$ xuống $0.64\,\text{ns}$ (nhanh hơn $3.56$ lần).
4. **`aoi21_pex_postlayout.sp`**:
   - Netlist trích xuất ký sinh Post-layout (PEX) với đầy đủ điện dung nút nội $X_n, X_p$ và cực má.
5. **`dap_an_chi_tiet_lab03.md`**:
   - Tài liệu đáp án chi tiết: Bảng chân trị, bảng kích thước $W/L$, bảng nỗ lực logic, bảng số liệu benchmark đo đạc chuẩn, barem chấm điểm chi tiết thang 10 và ngân hàng câu hỏi vấn đáp tại bàn.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Chạy trên LTspice: Mở tệp `.sp` trong LTspice và nhấn icon **Running Man** (hoặc phím tắt `Ctrl + R`).
- Xem log đo đạc: Nhấn phím tắt `Ctrl + L` để mở cửa sổ SPICE Error Log xem kết quả các câu lệnh `.MEAS`.
