# HƯỚNG DẪN GIẢNG VIÊN & ĐÁP ÁN MẪU: BÀI LAB 00
## NHẬP MÔN MÔ PHỎNG SPICE VỚI LTSPICE & MẠCH RC CƠ BẢN

> [!CAUTION]
> **TÀI LIỆU NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TA)**  
> Không phân phát tài liệu này cho sinh viên. Chi tiết lý thuyết chuyên sâu, kịch bản sư phạm 135'/225', 10 hình kỹ thuật và giải thích toán học đầy đủ được trình bày trong:  
> 👉 [dap_an_chi_tiet_lab00.md](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab00/dap_an_chi_tiet_lab00.md) hoặc [Lab00_Teacher_Book.md](file:///d:/tam/VLSI_Spice/Teacher_Book/Lab00_Teacher_Book.md)

---

### 1. TÓM TẮT ĐÁP ÁN LÝ THUYẾT PRE-LAB (P1 – P6)

1. **Quy ước tiền tố đơn vị SPICE (P1):**
   - `4.7M` $\to$ SPICE hiểu là $4,7 \times 10^{-3} = 0,0047$ (milli).
   - `22uF` $\to$ SPICE hiểu là $22 \times 10^{-6}$ (micro), bỏ qua chữ `F`.
   - Cú pháp đúng: $4,7\,\text{M}\Omega \implies$ `4.7Meg`; $22\,\text{pF} \implies$ `22p`.

2. **Mạch Cầu Phân áp DC (P2 - $V_{in} = 10,0\,\text{V}, R_1 = 15\,\text{k}\Omega, R_2 = 10\,\text{k}\Omega$):**
   - $V_{out} = 10,0 \times \frac{10}{15 + 10} = \mathbf{4,000\,\text{V}}$.
   - Dòng điện qua mạch: $I = \frac{10,0}{25 \times 10^3} = \mathbf{0,400\,\text{mA}} = 400\,\mu\text{A}$.
   - Độ dốc đặc tuyến truyền đạt: $\frac{dV_{out}}{dV_{in}} = \frac{10}{25} = \mathbf{0,4000}$.

3. **Mạch RC Quá độ (P3 - $R = 5\,\text{k}\Omega, C = 10\,\text{nF}, V_0 = 5,0\,\text{V}$):**
   - Hằng số thời gian: $\tau = R \times C = 5 \times 10^3 \times 10 \times 10^{-9} = \mathbf{50,0\,\mu\text{s}}$.
   - Trễ 50%: $t_{50} = \ln(2) \cdot \tau = 0,69315 \times 50\,\mu\text{s} = \mathbf{34,66\,\mu\text{s}}$.
   - Thời gian sườn tăng $t_r$ ($1010% $\\to$ 90%%): $t_r = \ln(9) \cdot \tau = 2,1972 \times 50\,\mu\text{s} = \mathbf{109,86\,\mu\text{s}} \approx 110\,\mu\text{s}$.
   - Tần số cắt $-3\,\text{dB}$: $f_c = \frac{1}{2\pi RC} \approx \mathbf{3183,1\,\text{Hz}} \approx \mathbf{3,183\,\text{kHz}}$.

4. **Thiết lập nguồn xung PULSE (P4):**
   - Để tụ nạp $> 99$% ($5\tau$): $T_{on} \ge 5\tau = \mathbf{250\,\mu\text{s}}$.
   - Để tụ xả $< 1$% ($10\tau$): $T_{period} \ge 10\tau = \mathbf{500\,\mu\text{s}}$.

5. **Độ nhạy tham số (P5):**
   - Khi $C' = 2C$: trễ $t_{pd}$ tăng gấp đôi ($2 t_{pd}$); tần số cắt $f_c$ giảm đi một nửa ($f_c / 2$).

6. **Phác thảo dạng sóng xung hẹp (P6 - $T_{on} = 3\tau$):**
   - $v_C(3\tau) = 5,0 \times (1 - e^{-3}) = \mathbf{4,751\,\text{V}}$ ($95,02\text{ pct} \cdot V_0$). Tụ chưa nạp đầy đến $5,0\,\text{V}$.

---

### 2. KẾT QUẢ MÔ PHỎNG THAM CHIẾU (BENCHMARK RESULTS)

| Phân tích | Đại lượng đo | Giá trị Lý thuyết | Giá trị Mô phỏng SPICE | Ghi chú đánh giá |
| :--- | :--- | :---: | :---: | :--- |
| **`.OP`** | $V(out)$ (Ex0.1) | $3,000\,\text{V}$ | **$3,00000\,\text{V}$** | Sai số 0,00% |
| **`.OP`** | $I(R1)$ (Ex0.1) | $0,1667\,\text{mA}$ | **$0,16667\,\text{mA}$** | Dòng điện dương từ `in` sang `out` |
| **`.DC`** | Độ dốc $\Delta V_{out}/\Delta V_{in}$ | $0,6000$ | **$0,60000$** | Tuyến tính đồng bộ |
| **`.TRAN`** | Trễ $t_{pd}$ 50% (Ex0.2) | $69,315\,\mu\text{s}$ | **$69,32\,\mu\text{s}$** | Trích xuất từ `.meas` |
| **`.TRAN`** | Sườn tăng $t_r$ ($1010% $\\to$ 90%%) | $219,72\,\mu\text{s}$ | **$219,7\,\mu\text{s}$** | $t_r \approx 2,2 \tau$ |
| **`.TRAN`** | Sườn giảm $t_f$ ($9090% $\\to$ 10%%) | $219,72\,\mu\text{s}$ | **$219,7\,\mu\text{s}$** | $t_f \approx 2,2 \tau$ |
| **`.TRAN`** | Đỉnh dòng nạp $I_{peak,chg}$ | $+0,2500\,\text{mA}$ | **$+0,25000\,\text{mA}$** | Tại thời điểm $t = 0^+$ |
| **`.TRAN`** | Đỉnh dòng xả $I_{peak,dis}$ | $-0,2483\,\text{mA}$ | **$-0,24832\,\text{mA}$** | Lệch 0,67% do $v_C(5\tau) = 4,966\,\text{V}$ |
| **`.AC`** | Độ lợi dải thông $A_{V,0}$ (Ex0.3) | $1,000$ ($0\,\text{dB}$) | **$0,000\,\text{dB}$** | Tại tần số thấp $10\,\text{Hz}$ |
| **`.AC`** | Tần số cắt $f_{-3\text{dB}}$ (`f_c`) | $1,592\,\text{kHz}$ | **$1,591 - 1,593\,\text{kHz}$** | Sai số $< 0,1$% |
| **`.AC`** | Pha tại tần số cắt | $-45,0^\circ$ | **$-44,9^\circ - -45,1^\circ$** | Trục pha bên phải |
| **Cross-check** | Tích số $t_r \cdot f_c$ | $0,3497$ | **$0,3497$** | Bất biến hai miền $\ln(9)/(2\pi)$ |
| **`.STEP`** | Hệ số góc $\frac{\Delta t_{pd}}{\Delta R}$ (Ex0.4) | $3,4657\,\mu\text{s}/\text{k}\Omega$ | **$3,466\,\mu\text{s}/\text{k}\Omega$** | Khớp $\ln(2) \cdot C = 3,4657 \times 10^{-9}\,\text{s}/\Omega$ |
| **Model** | Dòng $I_D$ NMOS C5N ($5\text{V}/5\text{V}$) | $\sim 2,22\,\text{mA}$ (Square Law) | **$1,35 - 1,45\,\text{mA}$** | Mô hình `N` Level 3 từ `C5_models.txt` |

---

### 3. CÂU HỎI VẤN ĐÁP TẠI BÀN (ORAL QUESTIONS)

1. *Hỏi:* "Tại sao khi viết `R1 in out 10M`, mạch phân áp lại cho ra kết quả gần bằng 0V hoặc sai hoàn toàn?"  
   *Trả lời chuẩn:* Vì trong chuẩn SPICE, ký tự `M` hoặc `m` đại diện cho tiền tố `milli` ($10^{-3}$), tức $0,01\,\Omega$. Để SPICE hiểu là $10\,\text{M}\Omega$ ($10 \times 10^6\,\Omega$), bắt buộc phải viết là `10Meg` hoặc `10MEG`.
2. *Hỏi:* "Nếu trong phân tích `.TRAN`, tín hiệu xung vuông có sườn tăng $10\,\text{ns}$ mà ta đặt `dTmax` là $20\,\mu\text{s}$ thì điều gì sẽ xảy ra?"  
   *Trả lời chuẩn:* SPICE sẽ nội suy bước quá thô và bỏ qua hoàn toàn sườn dốc $10\,\text{ns}$, dẫn đến dạng sóng bị gãy góc, và lệnh `.meas` sẽ báo lỗi `Measurement FAIL` do trượt qua ngưỡng điện thế.
3. *Hỏi:* "Tại sao đỉnh dòng xả đo được là $-248,3\,\mu\text{A}$, có phải SPICE đo sai so với đỉnh nạp $+250\,\mu\text{A}$ không?"  
   *Trả lời chuẩn:* Không phải lỗi SPICE. Vì độ rộng xung nạp $T_{on} = 500\,\mu\text{s} = 5\tau$, tụ chỉ mới nạp đến $v_C(5\tau) = 5,0(1 - e^{-5}) = 4,9663\,\text{V}$ (đạt 99,33%). Khi nguồn ngắt về $0\,\text{V}$, dòng xả ban đầu là $-4,9663\,\text{V} / 20\,\text{k}\Omega = -248,32\,\mu\text{A}$, lệch đúng 0,67% so với $-250\,\mu\text{A}$.
4. *Hỏi:* "Từ đồ thị Ex0.4, làm thế nào để chứng minh hệ số của công thức trễ là $\approx 0,69$ mà không cần nhìn vào công thức lý thuyết?"  
   *Trả lời chuẩn:* Lấy độ dốc thực nghiệm của đồ thị $\text{Slope} = \frac{\Delta t_{pd}}{\Delta R} = k \cdot C$. Chia độ dốc đo được ($3,466 \times 10^{-9}\,\text{s}/\Omega$) cho giá trị tụ điện $C = 5 \times 10^{-9}\,\text{F}$, ta rút ra hệ số thực nghiệm: $k = \frac{3,466 \times 10^{-9}}{5 \times 10^{-9}} \approx \mathbf{0,693} \approx \ln(2)$.
5. *Hỏi:* "Tại sao giá trị dòng $I_D$ mô phỏng ở Ex0.5 ($\approx 1,4\,\text{mA}$) lại nhỏ hơn đáng kể so với ước lượng theo mô hình bậc hai Shockley ($\approx 2,2\,\text{mA}$)?"  
   *Trả lời chuẩn:* Do transistor C5N ($L = 0,6\,\mu\text{m}$) là linh kiện kênh ngắn, xuất hiện hiệu ứng bão hòa vận tốc hạt dẫn (Velocity Saturation) và suy giảm độ linh động dưới điện trường dọc mạnh, khiến dòng bão hòa thực tế bị ghìm lại thấp hơn mô hình bậc hai lý thuyết.

---

### 4. DANH MỤC TỆP SPICE NETLIST THAM CHIẾU
- [ex01_divider.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab00/divider_op_dc.sp): Mạch phân áp DC (.op & .dc).
- [ex02_rc_tran.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab00/rc_delay.cir): Mẫu netlist chuẩn RC nạp - xả (.tran & .meas) tái sử dụng cho Lab 1–10.
- [ex03_rc_ac.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab00/rc_ac_bode.sp): Mạch lọc RC đáp ứng tần số (.ac Bode).
- [ex04_rc_step.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab00/rc_step_param.sp): Quét tham số điện trở R với .param và .step để kiểm chứng t_pd = 0.69*R*C.
- [ex05_nmos_test.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab00/nmos_test_include.sp): Kiểm tra liên kết mô hình MOSFET ngoài C5N.
