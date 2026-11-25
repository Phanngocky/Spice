# TÀI LIỆU QUẢN TRỊ KỸ THUẬT: MASTER ERRATA & KẾ HOẠCH KIỂM CHỨNG
## BỘ GIÁO TRÌNH THỰC HÀNH THIẾT KẾ VI MẠCH VLSI (LAB 00 ĐẾN LAB 10)

> **Tài liệu lưu hành nội bộ dành cho Giảng viên & Trợ giảng**  
> Bản tổng hợp toàn bộ các điểm sai lệch, mâu thuẫn kỹ thuật trong Handout gốc và quy trình 6 bước nghiệm thu thực tế trước ngày khai giảng.

---

# 11. BẢNG TỔNG HỢP CÁC ĐIỂM CẦN CHỈNH SỬA TRONG HANDOUT GỐC (MASTER ERRATA)

| Bài Lab | Vị trí trong Handout | Lỗi kỹ thuật / Mâu thuẫn phát hiện | Mức độ | Hướng điều chỉnh chính xác trước khi lên lớp |
| :---: | :--- | :--- | :---: | :--- |
| **Chung** | Toàn bộ 10 bài | Tham chiếu ảnh `images/` bị lỗi đường dẫn; lộ thư mục đáp án `03 - Instructor_Solutions/`. | **C** | Thay đường dẫn ảnh chuẩn nội bộ; xóa bỏ toàn bộ dấu vết thư mục đáp án trong bản phát cho SV. |
| **Lab 1** | Mục I & Pre-lab | Ghi $W_p/W_n = 3,0$ cho $V_M = 2,50\,\text{V}$; dùng lẫn lộn $\lambda_{kênh}$ và $\lambda_{lưới}$. | **C** | Đính chính: $3/1$ cho $V_M = 2,45\,\text{V}$; muốn $2,50\,\text{V}$ cần $3,36$. Viết tách biệt $\lambda_{kênh}$ và $\lambda_{lưới}$ trên bảng. |
| **Lab 2** | Mục III.3 & III.4 | Sơ đồ Stick NAND2 vẽ thiếu chân Out; khẳng định tuyệt đối "NAND luôn nhanh hơn NOR". | **C** | Bổ sung nút Out vào sơ đồ Euler; ghi rõ điều kiện "nhanh hơn khi độ linh động electron lớn hơn lỗ trống". |
| **Lab 3** | Mục III.1 & III.4 | Ghi "AOI21 giảm diện tích 40%"; ghi "cải thiện tốc độ 363%"; $C_{in} = 20\,\text{fF}$ không khớp. | **C** | Sửa thành "giảm $40\%$ số transistor, giảm $18\%$ tổng chiều rộng kênh"; sửa thành "nhanh hơn $3,63$ lần (giảm $72\%$ trễ)". |
| **Lab 4** | Mục III.1 & III.2 | $R_{TG}$ tại $2,5\,\text{V}$ ghi $490\,\Omega$; Weak 0 của PMOS ghi $0,8-1,05\,\text{V}$ (quên Body Effect). | **C** | Đính chính: $R_{TG}(2,5\,\text{V}) \approx 1,19\,\text{k}\Omega$. Điện áp Weak 0 thực tế dâng lên $\approx 1,4\,\text{V}$ do hiệu ứng thân PMOS. |
| **Lab 5** | Mục III.3 | Lỗi font ký tự tiếng Hoa ("điện荷"); vẽ thiếu inverter đệm ngõ ra làm sai số transistor. | **C** | Xóa ký tự lạ; chuẩn hóa sơ đồ DFF 18T (gồm 2 Latch 8T + 1 Inverter xung nhịp 2T). |
| **Lab 6** | Mục III.2 & III.3 | Khối Carry ghi nhầm "4 NMOS + 4 PMOS"; công thức Sum bị sai vế trái; đếm transistor mơ hồ. | **C** | Sửa thành 5 NMOS + 5 PMOS ($10\text{T}$); vế trái là $\overline{Sum}$; chốt cứng tổng 28 Transistors. |
| **Lab 7** | Mục III.4 | Lấy ví dụ OR4 để giải thích chia sẻ điện tích; gọi inverter $16\lambda/8\lambda$ là "high-skew". | **C** | Thay ví dụ OR4 bằng AND3/AND4 (có nút nội xếp chồng); đính chính inverter $16\lambda/8\lambda$ là **low-skew** ($V_M \approx 2,27\,\text{V}$). |
| **Lab 8** | Mục III.2a | Công thức $V_Q \approx \frac{V_{DD}-V_{tn}}{2CR}$ cho $1,08\,\text{V} > V_{tn}$, tự mâu thuẫn tiêu chí. | **C** | Thay bằng công thức giải tích đúng $V_Q \approx 0,789\,\text{V}$; tiêu chí an toàn là so với ngưỡng lật $V_{trip} \approx 1,48\,\text{V}$. |
| **Lab 9** | Mục III.3 | Định cỡ chuỗi 5 NMOS chỉ cho $8\lambda$; câu hỏi Pre-lab lộ đáp án "hoàn toàn xứng đáng". | **C** | Giải thích sự đánh đổi diện tích ($8\lambda$ chấp nhận điện trở lớn gấp 2,5 lần); đổi câu hỏi thành "Dự đoán, đo và so sánh". |
| **Lab 10** | Mục I & III | Đếm transistor vênh giữa MUX4 ($64\text{T}$ vs $72\text{T}$); mục tiêu $1\,\text{GHz}$ chưa có cơ sở thực nghiệm. | **C** | Thống nhất cách đếm 358 Transistors toàn chip; khẳng định $f_{max,PEX} \approx 1,42\,\text{GHz}$ đủ sức đạt chuẩn $1,0\,\text{GHz}$. |

*(Quy ước mức độ: **C** = Chắc chắn sai lệch lý thuyết/toán học, bắt buộc phải đính chính trước khi giảng dạy).*

---

# 12. KẾ HOẠCH HÀNH ĐỘNG VÀ GIẢI QUYẾT TRIỆT ĐỂ CÁC ĐIỂM CHƯA KIỂM

Nhằm chuyển đổi toàn bộ các nhãn "Chưa kiểm" thành "Đã kiểm chứng $100\%$", bộ phận giảng viên và trợ giảng thực hiện theo quy trình 6 bước sau trước tuần lễ bắt đầu học kỳ:

1. **Khóa cứng tham số mô hình PDK C5N:**
   Toàn bộ máy tính phòng lab sử dụng duy nhất tệp [C5_models.txt](file:///d:/tam/VLSI_Spice/04%20-%20Models_and_Libraries/C5_models.txt). Tên model trong netlist SPICE là `N` cho NMOS và `P` cho PMOS (cú pháp: `M1 Out In GND GND N W=... L=...`).
2. **Chạy đối chuẩn tự động bằng mã Python:**
   Trước buổi học, trợ giảng chạy toàn bộ chuỗi script kiểm chứng tự động trong thư mục `scripts/`:
   ```powershell
   python scripts/verify_lab01_new.py
   python scripts/verify_lab02.py
   python scripts/verify_lab03.py
   python scripts/verify_lab04.py
   python scripts/verify_lab05.py
   python scripts/verify_lab06.py
   python scripts/verify_lab07.py
   python scripts/verify_lab08.py
   python scripts/verify_lab09.py
   python scripts/verify_lab10.py
   ```
3. **Thực thi mô phỏng SPICE mẫu:**
   Mở LTspice và chạy lần lượt các tệp netlist nghiệm thu chuẩn trong `03 - Instructor_Solutions/` để nắm vững các điểm đo `.meas` và dạng sóng chuẩn:
   - Đo VTC và trễ Inverter: `03 - Instructor_Solutions/lab01/cmos_inverter_vtc_tran.sp`
   - Quét dịch pha $t_{setup}, t_{hold}$: `03 - Instructor_Solutions/lab05/setup_hold_sweep.sp`
   - Đo đường cong bướm SNM: `03 - Instructor_Solutions/lab08/sram_snm_butterfly.sp`
   - Quét tần số tới hạn ALU: `03 - Instructor_Solutions/lab10/alu_fmax_timing_sweep.sp`
4. **Cập nhật số liệu vào cột "Đo thực nghiệm":**
   Điền các giá trị đo thực tế ghi nhận được từ dàn máy phòng lab vào các cột `[ Đo ]` trong các bảng đối chiếu từ Lab 1 đến Lab 10 để làm đáp án chuẩn thống nhất cho toàn bộ cán bộ chấm thi.
5. **Đồng bộ hóa thư viện Layout trong Electric VLSI:**
   Kiểm tra tệp thư viện `lab_vlsi.jelib` trong Electric, xác nhận công nghệ đang chọn là `mocmos` (MOSIS CMOS Submicron, $\lambda = 0,30\,\mu\text{m}$). Kiểm tra luật N-well bao P-active tối thiểu $6\lambda$ và Active bao Contact tối thiểu $1,5\lambda$.
6. **Lưu trữ và phân quyền:**
   Tài liệu Giáo trình nội bộ này được lưu trữ độc quyền trong thư mục quản trị `03 - Instructor_Solutions/Teacher_Book_VLSI_Lab01_Lab10.md`. Khi xuất bản tài liệu cho sinh viên, chỉ trích xuất các phần bài tập thực hành trong `02 - Student Workbook/` và tuyệt đối loại bỏ các gợi ý giải thích cơ chế, đáp án giải tích và các netlist tham chiếu.

