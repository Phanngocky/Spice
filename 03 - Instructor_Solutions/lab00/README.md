# HƯỚNG DẪN GIẢNG VIÊN & ĐÁP ÁN MẪU: BÀI LAB 00
## NHẬP MÔN MÔ PHỎNG MẠCH VỚI SPICE VÀ LTSPICE

> [!CAUTION]
> **TÀI LIỆU NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TA)**  
> Tuyệt đối không phân phát tài liệu này cho sinh viên. Tài liệu này cung cấp các giá trị chuẩn, kết quả tính toán giải tích và hướng dẫn chấm thi thực hành tại bàn.

---

### 1. ĐÁP ÁN TÍNH TOÁN LÝ THUYẾT (PRE-LAB)

1. **Phân biệt tiền tố đơn vị trong SPICE:**
   - `R = 4.7M` $\to$ SPICE hiểu là $4.7 \times 10^{-3}\,\Omega = 4.7\,\text{m}\Omega = 0.0047\,\Omega$.
   - Để biểu diễn $4.7\,\text{M}\Omega$, cách viết đúng: `4.7Meg` hoặc `4.7MEG`.
   - `C = 100p` $\to$ SPICE hiểu là $100 \times 10^{-12}\,\text{F} = 100\,\text{pF}$.
   - `C = 50f` $\to$ SPICE hiểu là $50 \times 10^{-15}\,\text{F} = 50\,\text{fF}$.

2. **Mạch Cầu Phân áp DC ($V_{in} = 5.0\,\text{V}, R_1 = 30\,\text{k}\Omega, R_2 = 20\,\text{k}\Omega$):**
   - $V_{out} = 5.0 \times \frac{20}{30 + 20} = 2.000\,\text{V}$.
   - Dòng điện qua mạch: $I_{in} = \frac{5.0}{50 \times 10^3} = 0.100\,\text{mA} = 100\,\mu\text{A}$.
   - Tổng công suất tiêu tán: $P_{total} = 5.0 \times 0.1 \times 10^{-3} = 0.500\,\text{mW} = 500\,\mu\text{W}$.

3. **Mạch Lọc Thông Thấp RC ($R = 10\,\text{k}\Omega, C = 10\,\text{nF}$):**
   - Hằng số thời gian: $\tau = R \times C = 10 \times 10^3 \times 10 \times 10^{-9} = 100.0\,\mu\text{s} = 0.100\,\text{ms}$.
   - Điện áp tại $t = \tau$: $V_{out}(\tau) = 5.0 \times (1 - e^{-1}) \approx 5.0 \times 0.63212 = 3.161\,\text{V}$.
   - Điện áp tại $t = 5\tau$: $V_{out}(5\tau) = 5.0 \times (1 - e^{-5}) \approx 5.0 \times 0.99326 = 4.966\,\text{V}$.
   - Tần số cắt lý thuyết:
     $$f_{-3\text{dB}} = \frac{1}{2\pi RC} = \frac{1}{2\pi \times 100 \times 10^{-6}} \approx \frac{1}{6.28318 \times 10^{-4}} \approx 1591.55\,\text{Hz} \approx 1.592\,\text{kHz}$$

4. **Đặc tuyến I-V của BJT 2N3904 ($I_S = 10^{-14}\,\text{A}, \beta = 160, V_A = 74\,\text{V}, V_T = 25.85\,\text{mV}$):**
   - Dòng Base lý thuyết: $I_B(0.50\text{V}) = 0.0157\,\mu\text{A}$ ; $I_B(0.65\text{V}) = 5.203\,\mu\text{A}$ ; $I_B(0.70\text{V}) = 36.00\,\mu\text{A}$.
   - Ngưỡng mở $V_{BE}$: Tại $I_B = 10\,\mu\text{A} \implies V_{BE} = 0.667\,\text{V}$ (SPICE: $0.675\,\text{V}$) ; tại $I_B = 20\,\mu\text{A} \implies V_{BE} = 0.685\,\text{V}$ (SPICE: $0.693\,\text{V}$).
   - Dòng Collector có xét Early $I_C = \beta I_B (1 + V_{CE}/V_A)$:
     * Với $I_B = 10\,\mu\text{A}$: $I_C(1\text{V}) = 1.622\,\text{mA}$, $I_C(5\text{V}) = 1.708\,\text{mA}$, $I_C(10\text{V}) = 1.816\,\text{mA}$.
     * Với $I_B = 20\,\mu\text{A}$: $I_C(1\text{V}) = 3.243\,\text{mA}$, $I_C(5\text{V}) = 3.416\,\text{mA}$, $I_C(10\text{V}) = 3.632\,\text{mA}$.
   - Hệ số $\beta$ tại $V_{CE} = 5.0\,\text{V}$: $\beta = \frac{3.416 - 1.708}{0.010} = 170.8$.
   - Điện trở ngõ ra $r_o$ tại $I_B = 10\,\mu\text{A}$: $r_o = \frac{74}{160 \times 10\,\mu\text{A}} \approx 46.25\,\text{k}\Omega$.

---

### 2. KẾT QUẢ MÔ PHỎNG THAM CHIẾU (BENCHMARK RESULTS)

| Phân tích | Đại lượng đo | Giá trị Lý thuyết | Giá trị Mô phỏng SPICE | Ghi chú đánh giá |
| :--- | :--- | :---: | :---: | :--- |
| **`.OP`** | $V(vout)$ | $2.000\,\text{V}$ | **$2.00000\,\text{V}$** | Sai số $0\%$ |
| **`.OP`** | $I(R1)$ | $0.100\,\text{mA}$ | **$0.10000\,\text{mA}$** | Dòng điện âm nếu đo qua cực âm |
| **`.DC`** | $V_{out}$ tại $V_{in}=10\text{V}$ | $4.000\,\text{V}$ | **$4.00000\,\text{V}$** | Tuyến tính hoàn hảo |
| **`.TRAN`** | Hằng số $\tau$ (`tau`) | $100.0\,\mu\text{s}$ | **$99.8 - 100.2\,\mu\text{s}$** | Trích xuất từ `.MEAS` |
| **`.TRAN`** | Thời gian tăng $t_{rise}$ | $220.0\,\mu\text{s}$ | **$219.5 - 220.5\,\mu\text{s}$** | $t_r \approx 2.2 \tau$ |
| **`.AC`** | Độ lợi dải thông $A_{V,0}$ | $1.000$ ($0\,\text{dB}$) | **$0.000\,\text{dB}$** | Tại tần số thấp $10\,\text{Hz}$ |
| **`.AC`** | Tần số cắt $f_{-3\text{dB}}$ (`f_cut`) | $1.592\,\text{kHz}$ | **$1.591 - 1.593\,\text{kHz}$** | Sai số $< 0.1\%$ |
| **`.AC`** | Pha tại tần số cắt | $-45.0^\circ$ | **$-44.9^\circ - -45.1^\circ$** | Trục pha bên phải |
| **Model** | Dòng $I_D$ NMOS C5N ($5\text{V}/5\text{V}$)| $\sim 1.35\,\text{mA}$ | **$1.30 - 1.40\,\text{mA}$** | Mô hình `N` từ `C5_models.txt` |
| **BJT Vào** | Ngưỡng dẫn $V_{BE,on}$ tại $10\mu\text{A}$ | $0.667\,\text{V}$ | **$0.675\,\text{V}$** | Dẫn hàm mũ Diode $p-n$ |
| **BJT Vào** | Ngưỡng dẫn $V_{BE,on}$ tại $20\mu\text{A}$ | $0.685\,\text{V}$ | **$0.693\,\text{V}$** | Sai số $< 1.2\%$ |
| **BJT Ra** | Dòng $I_C$ ($5\text{V}, 10\mu\text{A}$)| $1.708\,\text{mA}$ | **$1.708\,\text{mA}$** | Quét 2 tham số lồng nhau |
| **BJT Ra** | Dòng $I_C$ ($5\text{V}, 20\mu\text{A}$)| $3.416\,\text{mA}$ | **$3.416\,\text{mA}$** | Sai số $0.00\%$ |
| **BJT Ra** | Hệ số khuếch đại dòng $\beta$ | $170.8$ | **$170.8$** | Đo tại $V_{CE} = 5.0\,\text{V}$ |
| **BJT Ra** | Điện áp bão hòa $V_{CE,sat}$ | $< 0.25\,\text{V}$ | **$0.18 - 0.20\,\text{V}$** | Vùng bão hòa dốc |
| **BJT Ra** | Điện trở vi sai $r_o$ ($10\mu\text{A}$) | $46.25\,\text{k}\Omega$ | **$46.2\,\text{k}\Omega$** | Khớp độ dốc Early |

---

### 3. CÂU HỎI VẤN ĐÁP TẠI BÀN (ORAL QUESTIONS)

1. *Hỏi:* "Tại sao khi viết `R1 in out 10M`, mạch phân áp lại cho ra kết quả gần bằng 0V hoặc sai hoàn toàn?"  
   *Trả lời chuẩn:* Vì trong chuẩn SPICE, ký tự `M` hoặc `m` đại diện cho tiền tố `milli` ($10^{-3}$), tức $0.01\,\Omega$. Để SPICE hiểu là $10\,\text{M}\Omega$ ($10 \times 10^6\,\Omega$), bắt buộc phải viết là `10Meg` hoặc `10MEG`.
2. *Hỏi:* "Nếu trong phân tích `.TRAN`, tín hiệu xung vuông có sườn tăng $1\,\text{ns}$ mà ta đặt `Maximum Timestep` là $10\,\mu\text{s}$ thì điều gì sẽ xảy ra?"  
   *Trả lời chuẩn:* SPICE sẽ nội suy bước quá thô và bỏ qua (miss) hoàn toàn sườn dốc $1\,\text{ns}$, dẫn đến dạng sóng bị méo mó, góc bị gãy, và lệnh `.MEAS` sẽ báo lỗi không tìm thấy điểm chuyển mạch (Trigger not found).
3. *Hỏi:* "Ý nghĩa của việc khai báo nguồn `AC 1 0` trong phân tích đáp ứng tần số là gì?"  
   *Trả lời chuẩn:* Hàm truyền độ lợi được tính là $A_V = \frac{V_{out}}{V_{in}}$. Khi đặt biên độ $V_{in} = 1\,\text{V}$, thì điện áp đo được tại $V_{out}$ chính là độ lợi $A_V$. Khi biểu diễn trên thang decibel: $20 \log_{10}(V_{out}/1) = 20 \log_{10}(V_{out})$, giúp việc quan sát và tính toán độ lợi trực tiếp và thuận tiện nhất.
4. *Hỏi:* "Trong họ đặc tuyến ngõ ra $I_C(V_{CE})$, tại sao ở vùng bão hòa ($V_{CE} < 0.25\,\text{V}$), tỉ số $I_C / I_B$ lại giảm mạnh xuống dưới hệ số khuếch đại $\beta$?"  
   *Trả lời chuẩn:* Ở vùng bão hòa, điện áp $V_{CE}$ sụt xuống thấp khiến tiếp giáp Base - Collector cũng bị phân cực thuận ($V_{BC} > 0$). Cả hai tiếp giáp $BE$ và $BC$ đều bơm hạt dẫn vào Base, làm mất khả năng thu hút hạt dẫn của Collector. Khi đó dòng $I_C$ bị khống chế bởi mạch ngoài chứ không còn tuân theo $I_C = \beta I_B$, dẫn đến $\beta_{sat} < \beta_F$.
5. *Hỏi:* "Tại sao khi đo họ đặc tuyến ngõ ra $I_C(V_{CE})$, ta dùng nguồn dòng $I_B$ làm tham số quét mà không dùng nguồn điện áp $V_{BE}$?"  
   *Trả lời chuẩn:* Do đặc tuyến ngõ vào $I_B(V_{BE})$ là hàm số mũ dốc đứng. Nếu chia đều bước quét $V_{BE}$, dòng $I_C$ sẽ dãn cách bất đối xứng nghiêm trọng theo cấp số nhân khiến các đường đặc tuyến chồng lấn hoặc vọt lên quá cao. Sử dụng nguồn dòng $I_B$ với các bước nhảy tuyến tính cách đều ($10\mu\text{A}, 20\mu\text{A}, \dots$) sẽ cho ra họ đặc tuyến $I_C$ phân bố đều, song song và dễ dàng trích xuất hệ số khuếch đại $\beta = \Delta I_C / \Delta I_B$.

---

### 4. DANH MỤC TỆP SPICE NETLIST THAM CHIẾU
- [divider_op_dc.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/divider_op_dc.sp): Mạch phân áp DC (.op & .dc).
- [rc_transient_meas.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_transient_meas.sp): Mạch lọc RC quá độ (.tran & .meas).
- [rc_ac_bode.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_ac_bode.sp): Mạch lọc RC đáp ứng tần số (.ac Bode).
- [nmos_test_include.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/nmos_test_include.sp): Kiểm tra mô hình MOSFET ngoài C5N.
- [bjt_input_curve.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/bjt_input_curve.sp): Quét DC đặc tuyến ngõ vào $I_B(V_{BE})$.
- [bjt_output_family.sp](file:///d:/tam/Spice/03%20-%20Instructor_Solutions/lab00/bjt_output_family.sp): Quét DC 2 tham số họ đặc tuyến ngõ ra $I_C(V_{CE}, I_B)$.
