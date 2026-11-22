# HƯỚNG DẪN GIẢNG VIÊN & ĐÁP ÁN MẪU: BÀI LAB 00
## LÀM QUEN MÔ PHỎNG SPICE VỚI LTSPICE

> [!CAUTION]
> **TÀI LIỆU NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TA)**  
> Tuyệt đối không phân phát tài liệu này cho sinh viên. Tài liệu này cung cấp các giá trị chuẩn, kết quả tính toán giải tích và hướng dẫn chấm thi thực hành tại bàn.

---

### 1. ĐÁP ÁN TÍNH TOÁN LÝ THUYẾT (PRE-LAB P1 – P5)

1. **Phân biệt tiền tố đơn vị trong SPICE (P1):**
   - `2.2M` $\to$ SPICE hiểu là $2.2 \times 10^{-3} = 0.0022$ (milli).
   - `2.2Meg` $\to$ SPICE hiểu là $2.2 \times 10^6 = 2\,200\,000$ (mega).
   - `47n` $\to$ SPICE hiểu là $47 \times 10^{-9}$ (nano).
   - `30f` $\to$ SPICE hiểu là $30 \times 10^{-15}$ (femto).

2. **Mạch Cầu Phân áp DC (P2 - $V_{in} = 5.0\,\text{V}, R_1 = 12\,\text{k}\Omega, R_2 = 18\,\text{k}\Omega$):**
   - $V_{out} = 5.0 \times \frac{18}{12 + 18} = \mathbf{3.000\,\text{V}}$.
   - Dòng điện qua mạch: $I = \frac{5.0}{30 \times 10^3} = \mathbf{0.1667\,\text{mA}} = 166.7\,\mu\text{A}$.
   - Tổng công suất tiêu tán: $P_{total} = 5.0 \times 0.1667 \times 10^{-3} = \mathbf{0.8333\,\text{mW}} = 833.3\,\mu\text{W}$.

3. **Mạch RC Nạp - Xả Quá độ (P3 - $R = 20\,\text{k}\Omega, C = 5\,\text{nF}, V_0 = 5.0\,\text{V}$):**
   - Hằng số thời gian: $\tau = R \times C = 20 \times 10^3 \times 5 \times 10^{-9} = \mathbf{100.0\,\mu\text{s}} = 0.100\,\text{ms}$.
   - Điện áp tại $t = \tau$: $v_C(\tau) = 5.0 \times (1 - e^{-1}) \approx \mathbf{3.161\,\text{V}}$ ($63.2\%$).
   - Trễ 50%: $t_{50} = \ln(2) \cdot \tau = \mathbf{69.32\,\mu\text{s}}$.
   - Thời gian tăng $t_r$ ($10\% \to 90\%$): $t_r = \ln(9) \cdot \tau = \mathbf{219.72\,\mu\text{s}} \approx 2.2\tau = 220\,\mu\text{s}$.
   - Tần số cắt $-3\,\text{dB}$:

     $$f_{-3\text{dB}} = \frac{1}{2\pi RC} = \frac{1}{2\pi \times 100 \times 10^{-6}} \approx \mathbf{1591.55\,\text{Hz}} \approx \mathbf{1.592\,\text{kHz}}$$

   - Đỉnh dòng nạp: $I_{peak} = \frac{5.0}{20\,\text{k}\Omega} = \mathbf{0.250\,\text{mA}} = 250\,\mu\text{A}$.
   - *Dự đoán khi $C \to 2C$:* $\tau' = 2\tau \implies t_{50}$ tăng gấp đôi (chậm gấp 2 lần) và $f_{-3\text{dB}}$ giảm một nửa.

4. **Khung Netlist SPICE (P4):**
   `V1 in 0 PULSE(0 5.0 0 10n 10n 500u 1000u)`, `R1 in out 20k`, `C1 out 0 5n`, `.tran 0 1m 0 0.1u`.

5. **Ước lượng Trễ VLSI (P5):**
   $R = 1\,\text{k}\Omega, C_L = 50\,\text{fF} \implies t_{50} = 0.69315 \times 1\,\text{k}\Omega \times 50\,\text{fF} = \mathbf{34.7\,\text{ps}}$ (khớp với Inverter Lab 1).

---

### 2. KẾT QUẢ MÔ PHỎNG THAM CHIẾU (BENCHMARK RESULTS)

| Phân tích | Đại lượng đo | Giá trị Lý thuyết | Giá trị Mô phỏng SPICE | Ghi chú đánh giá |
| :--- | :--- | :---: | :---: | :--- |
| **`.OP`** | $V(vout)$ (Ex0.1) | $3.000\,\text{V}$ | **$3.00000\,\text{V}$** | Sai số $0.00\%$ |
| **`.OP`** | $I(R1)$ (Ex0.1) | $0.1667\,\text{mA}$ | **$0.16667\,\text{mA}$** | Dòng điện dương qua R1 |
| **`.DC`** | Độ dốc $\Delta V_{out}/\Delta V_{in}$ | $0.6000$ | **$0.60000$** | Tuyến tính hoàn hảo |
| **`.TRAN`** | Trễ $t_{pd}$ 50% (Ex0.2) | $69.315\,\mu\text{s}$ | **$69.31 - 69.33\,\mu\text{s}$** | Trích xuất từ `.MEAS` |
| **`.TRAN`** | Sườn tăng $t_r$ ($10\% \to 90\%$) | $219.72\,\mu\text{s}$ | **$219.5 - 220.0\,\mu\text{s}$** | $t_r \approx 2.2 \tau$ |
| **`.TRAN`** | Sườn giảm $t_f$ ($90\% \to 10\%$) | $219.72\,\mu\text{s}$ | **$219.5 - 220.0\,\mu\text{s}$** | $t_f \approx 2.2 \tau$ |
| **`.TRAN`** | Đỉnh dòng nạp $I_{peak,chg}$ | $+0.250\,\text{mA}$ | **$+0.25000\,\text{mA}$** | Tại thời điểm $t = 0^+$ |
| **`.TRAN`** | Đỉnh dòng xả $I_{peak,dis}$ | $-0.250\,\text{mA}$ | **$-0.25000\,\text{mA}$** | Đảo chiều khi xung ngắt |
| **`.AC`** | Độ lợi dải thông $A_{V,0}$ (Ex0.3) | $1.000$ ($0\,\text{dB}$) | **$0.000\,\text{dB}$** | Tại tần số thấp $10\,\text{Hz}$ |
| **`.AC`** | Tần số cắt $f_{-3\text{dB}}$ (`f_c`) | $1.592\,\text{kHz}$ | **$1.591 - 1.593\,\text{kHz}$** | Sai số $< 0.1\%$ |
| **`.AC`** | Pha tại tần số cắt | $-45.0^\circ$ | **$-44.9^\circ - -45.1^\circ$** | Trục pha bên phải |
| **`.STEP`** | Hệ số góc $\frac{\Delta t_{pd}}{\Delta R}$ (Ex0.4) | $3.4657\,\text{ns}/\text{k}\Omega$ | **$3.466\,\text{ns}/\text{k}\Omega$** | Khớp $\ln(2) \cdot C$ |
| **Model** | Dòng $I_D$ NMOS C5N ($5\text{V}/5\text{V}$) | $\sim 2.2\,\text{mA}$ (Square Law) | **$1.35 - 1.45\,\text{mA}$** | Mô hình `N` từ `C5_models.txt` |

---

### 3. CÂU HỎI VẤN ĐÁP TẠI BÀN (ORAL QUESTIONS)

1. *Hỏi:* "Tại sao khi viết `R1 in out 10M`, mạch phân áp lại cho ra kết quả gần bằng 0V hoặc sai hoàn toàn?"  
   *Trả lời chuẩn:* Vì trong chuẩn SPICE, ký tự `M` hoặc `m` đại diện cho tiền tố `milli` ($10^{-3}$), tức $0.01\,\Omega$. Để SPICE hiểu là $10\,\text{M}\Omega$ ($10 \times 10^6\,\Omega$), bắt buộc phải viết là `10Meg` hoặc `10MEG`.
2. *Hỏi:* "Nếu trong phân tích `.TRAN`, tín hiệu xung vuông có sườn tăng $10\,\text{ns}$ mà ta đặt `dTmax` là $20\,\mu\text{s}$ thì điều gì sẽ xảy ra?"  
   *Trả lời chuẩn:* SPICE sẽ nội suy bước quá thô và bỏ qua hoàn toàn sườn dốc $10\,\text{ns}$, dẫn đến dạng sóng bị gãy góc, và lệnh `.MEAS` sẽ báo lỗi `Measurement FAIL` do trượt qua ngưỡng điện thế.
3. *Hỏi:* "Từ đồ thị Ex0.4, làm thế nào để chứng minh hệ số của công thức trễ là $\approx 0.69$ mà không cần nhìn vào công thức lý thuyết?"  
   *Trả lời chuẩn:* Lấy độ dốc thực nghiệm của đồ thị $\text{Slope} = \frac{\Delta t_{pd}}{\Delta R}$. Ta có $\text{Slope} = k \cdot C$. Chia độ dốc đo được ($3.466 \times 10^{-9}$) cho giá trị tụ điện $C = 5 \times 10^{-9}\,\text{F}$, ta rút ra hệ số thực nghiệm: $k = \frac{3.466 \times 10^{-9}}{5 \times 10^{-9}} \approx \mathbf{0.693} \approx \ln(2)$.
4. *Hỏi:* "Tại sao giá trị dòng $I_D$ mô phỏng ở Ex0.5 ($\approx 1.4\,\text{mA}$) lại nhỏ hơn đáng kể so với ước lượng theo mô hình bậc hai Shockley ($\approx 2.2\,\text{mA}$)?"  
   *Trả lời chuẩn:* Do transistor C5N ($L = 0.6\,\mu\text{m}$) là linh kiện kênh ngắn, xuất hiện hiệu ứng bão hòa vận tốc hạt dẫn (Velocity Saturation) và suy giảm độ linh động dưới điện trường dọc mạnh, khiến dòng bão hòa thực tế bị ghìm lại thấp hơn mô hình bậc hai lý thuyết.

---

### 4. DANH MỤC TỆP SPICE NETLIST THAM CHIẾU
- [divider_op_dc.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/divider_op_dc.sp): Mạch phân áp DC (.op & .dc).
- [rc_delay.cir](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_delay.cir): Mẫu netlist chuẩn RC nạp - xả (.tran & .meas) tái sử dụng cho Lab 1–10.
- [rc_charge_discharge.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_charge_discharge.sp): Khảo sát chi tiết quá trình nạp và xả tụ điện RC cơ bản.
- [rc_ac_bode.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_ac_bode.sp): Mạch lọc RC đáp ứng tần số (.ac Bode).
- [rc_step_param.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_step_param.sp): Quét tham số điện trở R với .param và .step để kiểm chứng t_pd = 0.69*R*C.
- [nmos_test_include.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/nmos_test_include.sp): Kiểm tra liên kết mô hình MOSFET ngoài C5N.
