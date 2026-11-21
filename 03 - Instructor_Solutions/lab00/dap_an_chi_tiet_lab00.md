# ĐÁP ÁN CHI TIẾT PHIẾU BÁO CÁO: BÀI 0 (LAB 00)
## NHẬP MÔN MÔ PHỎNG MẠCH VỚI SPICE VÀ LTSPICE
*(Tài liệu chuẩn dành riêng cho Giảng viên và Trợ giảng)*

---

### a. Phần Chuẩn bị (Pre-lab)

1. **Phân biệt tiền tố đơn vị trong SPICE:**
   - Khi viết `R = 4.7M`, SPICE hiểu giá trị là: **$0.0047\,\Omega$ (hoặc $4.7\,\text{m}\Omega$)**.
   - Để biểu diễn $4.7\,\text{M}\Omega$, cách viết đúng trong SPICE là: **`4.7Meg` (hoặc `4.7MEG`)**.
   - Khi viết `C = 100p`, SPICE hiểu giá trị là: **$100 \times 10^{-12}\,\text{F}$ (hay $100\,\text{pF}$)**.
   - Khi viết `C = 50f`, SPICE hiểu giá trị là: **$50 \times 10^{-15}\,\text{F}$ (hay $50\,\text{fF}$)**.

2. **Tính toán lý thuyết Mạch Cầu Phân áp DC:**
   - Điện áp ngõ ra lý thuyết: $V_{out} = 5.0 \times \frac{20\text{k}}{30\text{k} + 20\text{k}} =$ **$2.000\,\text{V}$**.
   - Dòng điện qua mạch: $I_{in} = \frac{5.0}{50\text{k}} =$ **$0.100\,\text{mA}$ (hay $100\,\mu\text{A}$)**.
   - Tổng công suất tiêu tán: $P_{total} = 5.0 \times 0.1\,\text{mA} =$ **$0.500\,\text{mW}$ (hay $500\,\mu\text{W}$)**.

3. **Tính toán lý thuyết Mạch Lọc Thông Thấp RC ($R = 10\,\text{k}\Omega, C = 10\,\text{nF}$):**
   - Hằng số thời gian: $\tau = R \times C = 10 \times 10^3 \times 10 \times 10^{-9} =$ **$100.0\,\mu\text{s}$ (hay $0.100\,\text{ms}$)**.
   - Điện áp tại thời điểm $t = \tau$: $V_{out}(\tau) = 5.0 \times (1 - e^{-1}) =$ **$3.161\,\text{V}$** (chấp nhận $3.16\,\text{V}$).
   - Điện áp tại thời điểm $t = 5\tau$: $V_{out}(5\tau) = 5.0 \times (1 - e^{-5}) =$ **$4.966\,\text{V}$** (chấp nhận xấp xỉ $5.0\,\text{V}$).
   - Tần số cắt lý thuyết: $f_{-3\text{dB}} = \frac{1}{2\pi RC} =$ **$1591.55\,\text{Hz}$ (hay $1.592\,\text{kHz}$)**.

4. **Bản thảo Netlist SPICE viết tay cho Mạch Lọc RC:**
   ```spice
   * Netlist mach loc RC
   Vin in 0 PULSE(0 5.0 0 1n 1n 100u 200u)
   R1 in out 10k
   C1 out 0 10nF
   .tran 0.1u 500u
   .meas TRAN tau TRIG V(in)=2.5 RISE=1 TARG V(out)=3.16 RISE=1
   .end
   ```

---

### b. Phần Thực hành (In-lab)

1. **Kết quả Phân tích Điểm làm việc tĩnh `.OP`:**
   - $V(vout) =$ **$2.000\,\text{V}$** (Sai số so với lý thuyết: $0\%$).
   - $I(R1) =$ **$0.100\,\text{mA}$** (hoặc $-0.100\,\text{mA}$ tùy chiều quy ước qua linh kiện, sai số $0\%$).

2. **Kết quả Quét `.DC Sweep` ($V_{in} = 0 \to 10\,\text{V}$):**
   - Điện áp $V_{out}$ khi $V_{in} = 5.0\,\text{V}$: **$2.000\,\text{V}$**.
   - Điện áp $V_{out}$ khi $V_{in} = 10.0\,\text{V}$: **$4.000\,\text{V}$**.
   - Độ dốc đường đặc tuyến đo được: $\frac{\Delta V_{out}}{\Delta V_{in}} =$ **$0.400$** (đúng bằng $\frac{R_2}{R_1+R_2}$).

3. **Kết quả Phân tích Quá độ `.TRAN` và Đo Hằng số Thời gian $\tau$:**
   - Giá trị `tau` đo từ `.MEAS`: **$99.8\,\mu\text{s} - 100.2\,\mu\text{s}$** (Độ lệch $< 0.5\%$).
   - Dạng sóng: Đường cong hàm mũ nạp từ $0\text{V}$ tiệm cận $5\text{V}$, xả từ $5\text{V}$ tiệm cận $0\text{V}$.

4. **Kết quả Phân tích Đáp ứng Tần số `.AC` (Biểu đồ Bode):**
   - Độ lợi dải thông tại $10\,\text{Hz}$: $A_{V,0} =$ **$0.00\,\text{dB}$** (bằng $1.00$ lần).
   - Tần số cắt `f_cut` đo từ `.MEAS`: **$1.591\,\text{kHz} - 1.593\,\text{kHz}$** (Độ lệch $< 0.1\%$).
   - Góc pha đo được tại tần số cắt: **$-45.0^\circ$** (chuẩn mực lý thuyết).

5. **Kết quả Thử nghiệm Mô hình MOSFET (`C5_models.txt`):**
   - Dòng bão hòa $I_D$ NMOS ($W=1.2\mu\text{m}, L=0.6\mu\text{m}, V_{GS}=V_{DS}=5\text{V}$): **$1.3 - 2.2\,\text{mA}$** (tùy theo tham số hiệu ứng kênh ngắn Level 3).
   - Trạng thái: Mô phỏng hội tụ, không có cảnh báo lỗi model.

6. **Đáp án Câu hỏi Phân tích:**
   - *Câu 1:* Nếu không khai báo `Maximum Timestep`, SPICE sẽ dùng thuật toán tự điều chỉnh bước tính, có thể nhảy bước quá lớn ($> 1\,\mu\text{s}$) tại các đoạn dốc đứng khiến dạng sóng bị gãy nhọn, mất thông tin xung, và lệnh `.MEAS` có thể báo lỗi không tìm thấy điểm chuyển mạch.
   - *Câu 2:* Đặt `AC 1` vì độ lợi tính bằng $A_V = \frac{V_{out}}{V_{in}} = \frac{V_{out}}{1} = V_{out}$. Khi đó, giá trị điện áp $V(vout)$ đo được chính là độ lợi điện áp của mạch, biểu diễn decibel là $20\log_{10}(V_{out})$ trực tiếp trên đồ thị. Nếu đặt biên độ là $10$, đồ thị sẽ bị dời lên trên $20\log_{10}(10) = 20\,\text{dB}$.
