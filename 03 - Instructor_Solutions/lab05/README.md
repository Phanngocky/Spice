# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 5 — DÀNH CHO GIẢNG VIÊN
## MẠCH TUẦN TỰ MỨC TRANSISTOR: D-LATCH VÀ D-FLIP-FLOP MASTER-SLAVE

Thư mục này chứa các tệp Netlist SPICE tham chiếu và tài liệu đáp án chi tiết phục vụ giảng dạy Bài 5 (đã đồng bộ với Teacher's Book Lab 05).

---

### Danh mục tệp trong thư mục:

1. **`dlatch_tran.sp`**:
   - Mô phỏng tế bào D-Latch (`dlatch_x1`, 10T) với 2 pha hoạt động: pha trong suốt (`clk = 5V`) và pha chốt giữ (`clk = 0V`), đo trễ $t_{pd(D \to Q)}$.
2. **`dff_ms_tran.sp`**:
   - Mô phỏng Master-Slave D-Flip-Flop (`dff_ms_x1`, 22T) kích hoạt sườn dương, có khởi tạo trạng thái `.ic` để đo $t_{c-q,LH}$ và $t_{c-q,HL}$.
3. **`setup_hold_sweep.sp`**:
   - Kịch bản `.step param` quét độ lệch pha $\Delta t$ để vẽ đồ thị push-out tìm $t_{setup}$ (10% push-out) và quét $t_{hold}$.
4. **`dff_pex_postlayout.sp`**:
   - Netlist tham chiếu PEX cho nội dung tùy chọn nâng cao.
5. **`dap_an_chi_tiet_lab05.md`**:
   - Tài liệu giảng dạy và đáp án chi tiết: phân tích vai trò $I_3$ (có vs không có $TG_2$), đường dẫn đầy đủ $t_{c-q}$ ($\approx 144\,\text{ps}$), nguồn gốc $t_{hold}$, bảng đối chuẩn và đáp án câu hỏi Post-lab.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn **Run** (`Ctrl + R`), sau đó nhấn `Ctrl + L` để xem kết quả `.MEAS`.
