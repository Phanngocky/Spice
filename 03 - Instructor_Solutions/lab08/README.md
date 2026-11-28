# GÓI ĐÁP ÁN VÀ FILE MÔ PHỎNG MẪU BÀI 8 — DÀNH CHO GIẢNG VIÊN
## THIẾT KẾ Ô NHỚ BÁN DẪN TĨNH (6T SRAM CELL) VÀ MẠCH KHUẾCH ĐẠI CẢM NHẬN (VLSA)

Thư mục này chứa toàn bộ các tệp Netlist SPICE tham chiếu và tài liệu đáp án chi tiết phục vụ giảng dạy Bài 8 (đã đồng bộ với Teacher's Book Lab 08). *(Lưu ý: Sinh viên tự dựng Netlist từ Pre-lab và khung trong Handout, không trỏ đường dẫn tới thư mục đáp án này).*

---

### Danh mục tệp trong thư mục:

1. **`sram_snm_butterfly.sp`**:
   - Mô phỏng quét DC cho 2 chế độ Hold ($WL=0$) và Read ($WL=5\text{V}$), dùng phương pháp xoay trục $45^\circ$ xác định $SNM_{hold}$ ($\approx 1.30\,\text{V}$) và $SNM_{read}$ ($\approx 0.36\,\text{V}$).
2. **`sram_read_write_tran.sp`**:
   - Mô phỏng quá độ Đọc tĩnh ($V_Q$), Đọc động ($C_{BL}=1\,\text{pF}$) và Ghi dữ liệu ($t_{write\_1}, t_{write\_0}$) với khởi tạo `.ic`.
3. **`sense_amp_tran.sp`**:
   - Mô phỏng VLSA (`sense_amp_vlsa`) với $\Delta V_{in} = \pm 150\,\text{mV}$ đo thời gian chốt $t_{latch}$.
4. **`sram_pex_postlayout.sp`**:
   - Netlist tham chiếu PEX cho nội dung tùy chọn nâng cao.
5. **`dap_an_chi_tiet_lab08.md`**:
   - Tài liệu giảng dạy và đáp án chi tiết: nghiệm bậc hai chính xác $V_Q$, bảng $CR$, $V_M$ Hold/Read, $SNM$ bằng xoay trục $45^\circ$ và đáp án 3 câu hỏi thảo luận.

---

### Hướng dẫn chạy kiểm chứng nhanh:
- Mở tệp `.sp` trong LTspice và nhấn **Run** (`Ctrl + R`), sau đó nhấn `Ctrl + L` để xem kết quả `.MEAS`.
