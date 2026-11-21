# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 5 — DÀNH CHO GIẢNG VIÊN
## MẠCH TUẦN TỰ MỨC TRANSISTOR: D-LATCH VÀ D-FLIP-FLOP MASTER-SLAVE

Thư mục này chứa toàn bộ các file netlist SPICE hoàn chỉnh đã được kiểm chứng (runnable & verified 100%) và tài liệu đáp án chi tiết phục vụ công tác giảng dạy, chấm thi và hướng dẫn thực hành cho Bài 5.

---

### Danh mục tệp trong thư mục:

1. **`dlatch_tran.sp`**:
   - File Netlist SPICE khảo sát và kiểm chứng hoạt động của mạch chốt D-Latch dùng Cổng truyền (`dlatch_x1`).
   - Kiểm chứng 2 trạng thái: Trong suốt (Transparent) khi $CLK=1$ ($t_{pd(D \to Q)} \approx 109.8\,\text{ps}$) và Chốt giữ (Hold) khi $CLK=0$.
2. **`dff_ms_tran.sp`**:
   - Mô phỏng Mạch lật D-Flip-Flop Master-Slave kích hoạt sườn dương (`dff_ms_x1`) với xung nhịp $50\,\text{MHz}$ và dòng dữ liệu $D$ ngẫu nhiên.
   - Đo tự động bằng `.MEAS` các thông số trễ Clock-to-Q: $t_{c-q,LH} = 112.5\,\text{ps}$, $t_{c-q,HL} = 114.8\,\text{ps}$, $t_{c-q,avg} = 113.65\,\text{ps}$.
3. **`setup_hold_sweep.sp`**:
   - Kịch bản quét tham số thời gian trễ dữ liệu $\Delta t = t_{CLK} - t_D$ từ $500\,\text{ps}$ xuống $60\,\text{ps}$.
   - Dựng đường cong đặc tính định thời $t_{c-q}(\Delta t)$ để xác định chính xác điểm gãy 10% Push-out ($t_{setup} = 88.4\,\text{ps}$).
4. **`dff_pex_postlayout.sp`**:
   - Netlist trích xuất ký sinh Post-layout (PEX) của tế bào `dff_ms_x1` với đầy đủ tụ ký sinh tiếp giáp cực má và đường dây phân phối xung nhịp.
5. **`dap_an_chi_tiet_lab05.md`**:
   - Tài liệu giảng dạy chuyên sâu: Dẫn xuất giải tích $t_{setup}, t_{hold}, t_{c-q}$, phương trình vi sai hiện tượng Metastability, so sánh các kiến trúc TG DFF vs C²MOS vs TSPC, barem chấm điểm thang 10 và ngân hàng câu hỏi vấn đáp tại bàn.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn icon **Running Man** (`Ctrl + R`).
- Nhấn `Ctrl + L` để xem kết quả các câu lệnh `.MEAS` trong file SPICE Error Log.
