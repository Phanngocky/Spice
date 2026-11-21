# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 0 (LAB 00)
# NHẬP MÔN MÔ PHỎNG MẠCH VỚI SPICE VÀ LTSPICE
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Bản chất Toán học và Thuật toán Giải Mạch của SPICE
SPICE (Simulation Program with Integrated Circuit Emphasis) giải bài toán mạch điện bằng cách chuyển đổi sơ đồ phần cứng thành hệ phương trình vi phân phi tuyến tính thông qua **Phương pháp Điện áp Nút Cải biên (Modified Nodal Analysis - MNA)**:
$$[\mathbf{G}] \cdot [\mathbf{V}] + [\mathbf{C}] \cdot \left[\frac{d\mathbf{V}}{dt}\right] = [\mathbf{I}]$$
Trong đó:
- $[\mathbf{G}]$: Ma trận dẫn nạp (Conductance Matrix) đại diện cho các phần tử điện trở, nguồn phụ thuộc.
- $[\mathbf{C}]$: Ma trận điện dung và điện cảm (Capacitance/Inductance Matrix).
- $[\mathbf{V}]$: Véctơ điện thế tại các nút cần tìm.
- $[\mathbf{I}]$: Véctơ dòng điện kích thích từ các nguồn độc lập.

**Nguyên lý 4 chế độ mô phỏng cơ bản:**
1. **Điểm làm việc tĩnh `.OP` (Operating Point):**
   - Triệt tiêu thành phần đạo hàm: $\frac{d\mathbf{V}}{dt} = 0$ (Tụ điện xem như hở mạch, cuộn cảm xem như ngắn mạch).
   - Giải hệ phương trình đại số phi tuyến bằng **phương pháp lặp Newton-Raphson**:
     $$\mathbf{V}^{(k+1)} = \mathbf{V}^{(k)} - \left[\mathbf{J}(\mathbf{V}^{(k)})\right]^{-1} \cdot \mathbf{F}(\mathbf{V}^{(k)})$$
   - Điều kiện dừng: Khi sai số dòng điện $\le \text{reltol} \times I + \text{abstol}$ và sai số điện áp $\le \text{reltol} \times V + \text{vntol}$.
2. **Quét một chiều `.DC` (DC Sweep):**
   - Thực hiện chuỗi các phân tích `.OP` liên tiếp khi một hoặc nhiều nguồn độc lập thay đổi giá trị theo bước quét đã định. Dùng để dựng đặc tuyến tĩnh $I-V$ hoặc hàm truyền đạt $VTC$.
3. **Phân tích quá độ `.TRAN` (Transient Analysis):**
   - Giải phương trình vi phân theo miền thời gian bằng phương pháp tích phân số (Numerical Integration): **Trapezoidal Rule** (mặc định) hoặc **Gear Method**.
   - Cực kỳ nhạy cảm với bước thời gian: Nếu $T_{step}$ quá lớn, thuật toán sẽ bỏ qua các sườn xung dốc và gây ra hiện tượng dao động số giả tạo (Numerical Ringing).
4. **Phân tích tín hiệu nhỏ tần số `.AC` (AC Small-Signal Analysis):**
   - Bước 1: Tính điểm tĩnh `.OP` để tuyến tính hóa các phần tử phi tuyến (MOSFET, Diode) thành các tham số tín hiệu nhỏ ($g_m, r_o, C_{gs}, C_{gd}$).
   - Bước 2: Thay thế nguồn xoay chiều có biên độ phức và giải hệ phương trình tuyến tính phức theo từng tần số $f \in [f_{start}, f_{stop}]$ để vẽ đồ thị Bode biên độ ($20\log_{10}|H(j\omega)|$) và góc pha ($\arg H(j\omega)$).

---

### 2. Dẫn xuất Giải tích Mạch Kiểm chứng Chuẩn

#### a. Mạch Cầu Phân áp DC
Áp dụng định luật Ohm và Kirchhoff:
$$V_{out} = V_{in} \cdot \frac{R_2}{R_1 + R_2} = 5.0 \times \frac{20\,\text{k}\Omega}{30\,\text{k}\Omega + 20\,\text{k}\Omega} = 2.000\,\text{V}$$
Dòng điện qua mạch và công suất tiêu tán toàn phần:
$$I_{in} = \frac{V_{in}}{R_1 + R_2} = \frac{5.0}{50 \times 10^3} = 0.100\,\text{mA} = 100.0\,\mu\text{A}$$
$$P_{total} = V_{in} \times I_{in} = 5.0\,\text{V} \times 0.100\,\text{mA} = 0.500\,\text{mW} = 500.0\,\mu\text{W}$$

#### b. Mạch Nạp và Xả Tụ điện RC Bậc 1 (Bài mẫu Cơ bản)
Phương trình vi phân quá độ tổng quát của mạch RC:
$$R C \frac{dv_C(t)}{dt} + v_C(t) = v_{in}(t)$$
Hằng số thời gian $\tau = R \cdot C = (10 \times 10^3\,\Omega) \times (10 \times 10^{-9}\,\text{F}) = 100.0\,\mu\text{s} = 0.100\,\text{ms}$.

1. **Giai đoạn Nạp điện ($0 \le t < T_{on}$, nguồn cấp $v_{in} = V_0 = 5.0\,\text{V}$, điện áp đầu $v_C(0) = 0$):**
   $$v_C(t) = V_0 \left(1 - e^{-\frac{t}{\tau}}\right), \quad i(t) = \frac{V_0}{R} e^{-\frac{t}{\tau}} > 0$$
   - Dòng nạp đỉnh tức thời tại $t = 0$: $I_{peak,charge} = +\frac{V_0}{R} = +\frac{5.0}{10\,\text{k}\Omega} = +0.500\,\text{mA}$ ($+500.0\,\mu\text{A}$).
   - Tại $t = \tau = 100\,\mu\text{s}$: $v_C(\tau) = V_0 (1 - e^{-1}) \approx 5.0 \times 0.63212 = 3.1606\,\text{V}$ (ngưỡng nạp chuẩn $63.2\%$).
   - Thời gian sườn tăng $10\% \to 90\%$: $t_{rise} = \tau \ln(9) \approx 2.1972\tau \approx 220.0\,\mu\text{s}$.
   - Tại $t = 5\tau = 500\,\mu\text{s}$: $v_C(5\tau) = V_0 (1 - e^{-5}) \approx 5.0 \times 0.99326 = 4.9663\,\text{V}$ ($99.3\% \approx 100\%$, tụ nạp đầy).
   - Năng lượng điện trường tích lũy cực đại: $W_{max} = \frac{1}{2} C V_0^2 = 0.5 \times 10^{-8} \times 25 = 0.125\,\mu\text{J}$.

2. **Giai đoạn Xả điện ($T_{on} \le t < T_{period}$, nguồn ngắt $v_{in} = 0\,\text{V}$, đặt $t' = t - T_{on} \ge 0$):**
   $$v_C(t') = V_0 e^{-\frac{t'}{\tau}}, \quad i(t') = -\frac{V_0}{R} e^{-\frac{t'}{\tau}} < 0$$
   - Dòng xả đỉnh tức thời tại $t' = 0$: $I_{peak,discharge} = -\frac{V_0}{R} = -0.500\,\text{mA}$ (dòng âm phóng từ tụ về đất).
   - Tại $t' = \tau = 100\,\mu\text{s}$: $v_C(\tau) = V_0 e^{-1} \approx 5.0 \times 0.36788 = 1.8394\,\text{V}$ (còn lại $36.8\%$, đã phóng $63.2\%$).
   - Thời gian sườn giảm $90\% \to 10\%$: $t_{fall} = 2.2\tau = 220.0\,\mu\text{s}$.
   - Tại $t' = 5\tau = 500\,\mu\text{s}$: $v_C(5\tau) = V_0 e^{-5} \approx 5.0 \times 0.00674 = 0.0337\,\text{V}$ ($0.7\% \approx 0\,\text{V}$, xả cạn hoàn toàn).

3. **Mạch Lọc Thông Thấp RC và Đáp ứng Tần số (.AC):**
   $$H(j\omega) = \frac{1}{1 + j\omega RC} \implies f_{-3\text{dB}} = \frac{1}{2\pi RC} \approx 1591.55\,\text{Hz} \approx 1.592\,\text{kHz}$$
   Góc pha tại tần số cắt: $\phi = -\arctan(1) = -45.0^\circ$.

#### c. Lý thuyết Giải tích Đặc tuyến I-V của BJT và Mô hình Ebers-Moll
Đối với transistor BJT NPN:
- **Đặc tuyến ngõ vào $I_B - V_{BE}$:**
  Tiếp giáp Base - Emitter tương đương một tiếp giáp $p-n$ bán dẫn. Dòng cực Base tuân theo định luật hàm mũ Ebers-Moll:
  $$I_B(V_{BE}) = \frac{I_S}{\beta} \left( e^{\frac{V_{BE}}{V_T}} - 1 \right)$$
  Trong đó thế nhiệt $V_T = \frac{k_B T}{q} \approx 25.85\,\text{mV}$ tại $300\,\text{K}$.
  - Khi $V_{BE} < 0.60\,\text{V}$: $I_B \approx 0$ (vùng ngưng dẫn).
  - Ngưỡng mở (Knee voltage): Tại $I_B = 10\,\mu\text{A} \implies V_{BE} \approx 0.667 - 0.675\,\text{V}$; tại $I_B = 20\,\mu\text{A} \implies V_{BE} \approx 0.685 - 0.693\,\text{V}$.

- **Họ đặc tuyến ngõ ra $I_C - V_{CE}$ (tham số theo $I_B$):**
  1. **Vùng Bão hòa ($V_{CE} < V_{CE,sat} \approx 0.20 - 0.25\,\text{V}$):** Cả hai tiếp giáp $BE$ và $BC$ đều phân cực thuận ($V_{BC} > 0$). Dòng $I_C$ sụt giảm phụ thuộc vào điện áp ngoài và tỉ số dòng $\frac{I_C}{I_B} < \beta$.
  2. **Vùng Khuếch đại Tích cực ($V_{CE} \ge 0.25\,\text{V}$):** Tiếp giáp $BE$ phân cực thuận, $BC$ phân cực nghịch. Dòng $I_C$ khuếch đại theo $I_B$ kèm hiệu ứng Early:
     $$I_C = \beta I_B \left( 1 + \frac{V_{CE}}{V_A} \right)$$
     * Hệ số khuếch đại dòng: $\beta = \frac{\Delta I_C}{\Delta I_B}$.
     * Độ dốc đường đặc tuyến do điện áp Early ($V_A = 74\,\text{V}$):
       $$\frac{\partial I_C}{\partial V_{CE}} = \frac{\beta I_B}{V_A} = \frac{1}{r_o} \implies r_o = \frac{V_A}{\beta I_B}$$
       (Tại $I_B = 10\,\mu\text{A} \implies r_o \approx 46.25\,\text{k}\Omega$; tại $I_B = 20\,\mu\text{A} \implies r_o \approx 23.12\,\text{k}\Omega$).
  3. **Vùng Ngưng dẫn ($I_B = 0\,\mu\text{A}$):** Cả hai tiếp giáp đều phân cực nghịch, dòng qua các cực chỉ là dòng rò $I_{CEO} \approx 0$.

---

### 3. Các Bẫy Kỹ thuật & Sai lầm Sinh viên Thường gặp (Pedagogical Traps)

1. **Bẫy tiền tố đơn vị `M` vs `Meg`:**
   - *Lỗi:* Sinh viên viết `R1 in out 4.7M` với ý định tạo điện trở $4.7\,\text{M}\Omega$.
   - *Hậu quả vật lý:* SPICE không phân biệt chữ hoa/chữ thường và quy ước `m`/`M` là **milli** ($10^{-3}$). Do đó mạch hiểu là $4.7\,\text{m}\Omega$, gây ngắn mạch, dòng tăng vọt hàng trăm Ampe và mô phỏng sai lệch hoàn toàn.
   - *Hướng dẫn của giảng viên:* Nhấn mạnh tiền tố Mega bắt buộc phải viết là `Meg` hoặc `MEG`.
2. **Bẫy nút đất lơ lửng (Floating Node / No Ground):**
   - *Lỗi:* Sinh viên quên đặt nhãn nút `0` hoặc không nối cực đất `GND`.
   - *Hậu quả:* SPICE không thể thiết lập ma trận $MNA$ vì thiếu nút điện thế tham chiếu $0\,\text{V}$, xuất hiện lỗi kinh điển: `Singular Matrix` hoặc `Node is floating`.
3. **Bẫy bước thời gian trong `.TRAN`:**
   - *Lỗi:* Chỉ khai báo `.tran 500u` mà không chỉ định `Tstep_max`.
   - *Hậu quả:* Đồ thị hiển thị các đường gấp khúc gãy đoạn, câu lệnh `.MEAS` tìm ngưỡng điện thế bị trượt qua dẫn đến lỗi `Measurement FAIL`.
   - *Khắc phục:* Luôn hướng dẫn sinh viên đặt bước tính cực đại: `.tran 0.1u 500u 0 0.1u`.
4. **Bẫy thứ tự cực BJT trong SPICE Netlist:**
   - *Lỗi:* Sinh viên khai báo BJT sai thứ tự chân: `Q1 Base Collector Emitter Model` thay vì chuẩn `Q1 Collector Base Emitter Model` (hoặc nhầm chiều Collector và Emitter trên sơ đồ Schematic).
   - *Hậu quả:* Transistor rơi vào chế độ đảo ngược (Reverse Active Mode) với hệ số khuếch đại dòng $\beta_R \approx 1$ thay vì $\beta_F \approx 160$, dẫn đến dòng $I_C$ tụt thấp bất thường.
5. **Bẫy nhầm lẫn đơn vị dòng điện cực Base:**
   - *Lỗi:* Sinh viên ngộ nhận dòng $I_B$ tính bằng mA giống như dòng $I_C$.
   - *Hậu quả:* Khi thiết lập thang quét tham số nguồn dòng $I_B$, nếu nhập `10m` đến `50m` thay vì `10u` đến `50u`, dòng bơm vào Base lên tới hàng chục mA khiến BJT rơi vào bão hòa cực sâu, $V_{CE}$ sụt xuống gần $0\,\text{V}$ và đồ thị họ đặc tuyến biến dạng hoàn toàn.
6. **Bẫy đảo thứ tự nguồn trong quét DC Sweep 2 tham số (Nested Sweep):**
   - *Lỗi:* Sinh viên nhập `1st Source: Ib` và `2nd Source: Vce` trong cửa sổ Edit Simulation Command.
   - *Hậu quả:* Trục hoành biến thành trục dòng điện $I_B$ thay vì điện áp $V_{CE}$, làm mất dạng họ đặc tuyến ngõ ra kinh điển của BJT. Giảng viên cần nhắc sinh viên: *1st Source luôn là biến trục hoành ($V_{CE}$), 2nd Source là tham số phân nhánh đường cong ($I_B$)*.

---

## PHẦN II: ĐÁP ÁN CHI TIẾT PHIẾU BÁO CÁO THỰC HÀNH

### a. Phần Chuẩn bị (Pre-lab)
1. **Bảng tiền tố đơn vị quy ước:**
   - `4.7M` $\to 4.7 \times 10^{-3}\,\Omega = 4.7\,\text{m}\Omega$.
   - Cách viết đúng $4.7\,\text{M}\Omega \to$ `4.7Meg`.
   - `100p` $\to 100 \times 10^{-12}\,\text{F} = 100\,\text{pF}$.
   - `50f` $\to 50 \times 10^{-15}\,\text{F} = 50\,\text{fF}$.
2. **Mạch Cầu Phân áp DC:**
   - $V_{out} = 2.000\,\text{V}$ ; $I_{in} = 0.100\,\text{mA}$ ($100\,\mu\text{A}$) ; $P_{total} = 0.500\,\text{mW}$ ($500\,\mu\text{W}$).
3. **Mạch Nạp - Xả Tụ điện RC ($R = 10\,\text{k}\Omega, C = 10\,\text{nF}, V_0 = 5.0\text{V}$):**
   - Hằng số thời gian $\tau = 100.0\,\mu\text{s}$.
   - Giai đoạn Nạp: $I_{peak,charge} = +0.500\,\text{mA}$ ($+500\,\mu\text{A}$) ; $V_C(\tau) = 3.161\,\text{V}$ ($63.2\%$) ; $V_C(5\tau) = 4.966\,\text{V}$ ($99.3\%$) ; $t_{rise} = 220.0\,\mu\text{s}$.
   - Giai đoạn Xả: $I_{peak,discharge} = -0.500\,\text{mA}$ ($-500\,\mu\text{A}$) ; $V_C(\tau) = 1.839\,\text{V}$ ($36.8\%$) ; $V_C(5\tau) = 0.034\,\text{V}$ ($0.7\%$) ; $t_{fall} = 220.0\,\mu\text{s}$.
   - Năng lượng tích trữ: $W_{max} = 0.125\,\mu\text{J}$ ; Tần số cắt: $f_{-3\text{dB}} = 1.592\,\text{kHz}$.
4. **Đặc tuyến I-V của BJT 2N3904 ($I_S = 10^{-14}\,\text{A}, \beta = 160, V_A = 74\,\text{V}, V_T = 25.85\,\text{mV}$):**
   - Dòng Base lý thuyết theo Ebers-Moll:
     * $I_B(0.50\text{V}) = 0.0157\,\mu\text{A}$
     * $I_B(0.65\text{V}) = 5.203\,\mu\text{A}$
     * $I_B(0.70\text{V}) = 36.00\,\mu\text{A}$
   - Ngưỡng mở $V_{BE}$ tính toán:
     * Tại $I_B = 10\,\mu\text{A} \implies V_{BE} = 0.6669\,\text{V}$ (xấp xỉ $0.675\,\text{V}$ trong SPICE)
     * Tại $I_B = 20\,\mu\text{A} \implies V_{BE} = 0.6848\,\text{V}$ (xấp xỉ $0.693\,\text{V}$ trong SPICE)
   - Dòng Collector có xét hiệu ứng Early $I_C = \beta I_B (1 + V_{CE}/V_A)$:
     * Khi $I_B = 10\,\mu\text{A}$: $I_C(1\text{V}) = 1.622\,\text{mA}$ ; $I_C(5\text{V}) = 1.708\,\text{mA}$ ; $I_C(10\text{V}) = 1.816\,\text{mA}$
     * Khi $I_B = 20\,\mu\text{A}$: $I_C(1\text{V}) = 3.243\,\text{mA}$ ; $I_C(5\text{V}) = 3.416\,\text{mA}$ ; $I_C(10\text{V}) = 3.632\,\text{mA}$
   - Hệ số $\beta$ tại $V_{CE} = 5.0\,\text{V}$: $\beta = \frac{3.416 - 1.708}{0.010} = 170.8$
   - Điện trở ngõ ra $r_o$ tại $I_B = 10\,\mu\text{A}$: $r_o = \frac{74}{160 \times 10\,\mu\text{A}} \approx 46.25\,\text{k}\Omega$

---

### b. Phần Thực hành (In-lab Benchmark Data)

| Nội dung thí nghiệm | Thông số đo | Giá trị lý thuyết | Giá trị mô phỏng SPICE | Sai số (%) |
| :--- | :--- | :---: | :---: | :---: |
| **Phân tích `.OP` Cơ bản** | $V(vout)$ | $2.000\,\text{V}$ | **$2.0000\,\text{V}$** | $0.00\%$ |
| | $I(R1)$ | $0.100\,\text{mA}$ | **$0.1000\,\text{mA}$** | $0.00\%$ |
| **Quét `.DC` Cơ bản** | $V_{out}$ tại $V_{in}=5\text{V}$ | $2.000\,\text{V}$ | **$2.0000\,\text{V}$** | $0.00\%$ |
| | Độ dốc $\Delta V_{out}/\Delta V_{in}$ | $0.400$ | **$0.4000$** | $0.00\%$ |
| **Nạp tụ `.TRAN`** | Hằng số thời gian nạp `tau_charge` | $100.0\,\mu\text{s}$ | **$100.00\,\mu\text{s}$** | $< 0.05\%$ |
| | Thời gian sườn tăng `t_rise` | $220.0\,\mu\text{s}$ | **$219.7\,\mu\text{s}$** | $< 0.2\%$ |
| | Dòng nạp cực đại `I_peak_charge` | $+0.500\,\text{mA}$ | **$+0.499\,\text{mA}$** | $< 0.2\%$ |
| | Điện áp nạp sau $5\tau$ | $4.966\,\text{V}$ | **$4.966\,\text{V}$** | $0.00\%$ |
| **Xả tụ `.TRAN`** | Hằng số thời gian xả `tau_discharge` | $100.0\,\mu\text{s}$ | **$100.00\,\mu\text{s}$** | $< 0.05\%$ |
| | Thời gian sườn giảm `t_fall` | $220.0\,\mu\text{s}$ | **$219.7\,\mu\text{s}$** | $< 0.2\%$ |
| | Dòng xả cực đại `I_peak_discharge` | $-0.500\,\text{mA}$ | **$-0.499\,\text{mA}$** | $< 0.2\%$ |
| | Điện áp xả sau $5\tau$ | $0.034\,\text{V}$ | **$0.034\,\text{V}$** | $0.00\%$ |
| **Tần số `.AC`** | Độ lợi tại $10\,\text{Hz}$ | $0.00\,\text{dB}$ | **$0.000\,\text{dB}$** | $0.00\%$ |
| | Tần số cắt $-3\,\text{dB}$ | $1591.55\,\text{Hz}$ | **$1591.5\,\text{Hz}$** | $< 0.01\%$ |
| | Góc pha tại $f_{-3\text{dB}}$ | $-45.00^\circ$ | **$-45.00^\circ$** | $0.00\%$ |
| **Mô hình MOSFET C5N** | $I_{D,sat}$ (NMOS $1.2\mu/0.6\mu$) | $2.0-2.2\,\text{mA}$ | **$2.219\,\text{mA}$** | Phù hợp BSIM3 |
| **Đặc tuyến vào BJT** | $V_{BE}$ tại $I_B = 10\,\mu\text{A}$ | $0.667\,\text{V}$ | **$0.675\,\text{V}$** | Sai số $< 1.2\%$ |
| | $V_{BE}$ tại $I_B = 20\,\mu\text{A}$ | $0.685\,\text{V}$ | **$0.693\,\text{V}$** | Sai số $< 1.2\%$ |
| **Họ đặc tuyến ra BJT**| $I_C$ tại $V_{CE}=5\text{V}, I_B=10\mu\text{A}$ | $1.708\,\text{mA}$ | **$1.708\,\text{mA}$** | $0.00\%$ |
| | $I_C$ tại $V_{CE}=5\text{V}, I_B=20\mu\text{A}$ | $3.416\,\text{mA}$ | **$3.416\,\text{mA}$** | $0.00\%$ |
| | Hệ số $\beta$ tại $V_{CE}=5\,\text{V}$ | $170.8$ | **$170.8$** | Khớp lý thuyết Early |
| | Điện áp bão hòa $V_{CE,sat}$ | $< 0.25\,\text{V}$ | **$0.18 - 0.20\,\text{V}$** | Vùng bão hòa dốc |
| | Điện trở vi sai $r_o$ ($10\mu\text{A}$)| $46.25\,\text{k}\Omega$ | **$46.2\,\text{k}\Omega$** | Khớp độ dốc Early |

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem chấm điểm (Thang 10):
- Chuẩn bị Pre-lab (tính tay mạch phân áp, mạch RC và đặc tuyến BJT): **2.0 điểm**.
- Thao tác mô phỏng `.OP` & `.DC` mạch cơ bản: **2.0 điểm**.
- Mô phỏng `.TRAN` và dùng lệnh `.MEAS` đọc đúng $\tau$: **2.0 điểm**.
- Phân tích `.AC` và khảo sát thư viện ngoài `C5_models.txt`: **2.0 điểm**.
- Khảo sát Họ Đặc tuyến Vào / Ra BJT (Bài 5): **1.5 điểm**.
- Tác phong, kỷ luật phòng máy và báo cáo hoàn chỉnh: **0.5 điểm**.

### 2. Câu hỏi vấn đáp gợi ý:
- **Câu hỏi 1:** *Tại sao khi đo đáp ứng tần số mạch lọc thông thấp trong SPICE, nguồn xoay chiều luôn được gán biên độ là `AC 1`?*  
  **Đáp:** Vì độ lợi điện áp là $A_V = \frac{V_{out}}{V_{in}} = \frac{V_{out}}{1} = V_{out}$. Khi đó, giá trị điện áp hiển thị trực tiếp là độ lợi; khi chuyển sang thang decibel $20\log_{10}(V_{out})$, ta có ngay đồ thị Bode biên độ chuẩn hóa mà không phải chia cho biên độ vào.
- **Câu hỏi 2:** *Lệnh `.MEAS` hoạt động như thế nào và tại sao cần thiết hơn việc đọc đồ thị bằng trỏ chuột (Cursor)?*  
  **Đáp:** Lệnh `.MEAS` phân tích trực tiếp mảng dữ liệu tính toán của bộ giải vi phân, nội suy điểm chuyển mạch với độ phân giải toán học cực cao ($< 1\,\text{ps}$), triệt tiêu sai số chủ quan của mắt người và cho phép tự động hóa quét tham số hàng loạt.
- **Câu hỏi 3:** *Trong họ đặc tuyến ngõ ra $I_C(V_{CE})$, tại sao ở vùng bão hòa ($V_{CE} < 0.25\,\text{V}$), tỉ số $I_C / I_B$ lại sụt giảm mạnh xuống dưới hệ số khuếch đại $\beta$? Bản chất vật lý lúc này là gì?*  
  **Đáp:** Ở vùng bão hòa, điện áp $V_{CE}$ quá nhỏ khiến tiếp giáp Base - Collector cũng bị phân cực thuận ($V_{BC} > 0$). Cả hai tiếp giáp $BE$ và $BC$ đều bơm điện tử vào vùng Base, làm mất tác dụng thu hút hạt dẫn của Collector. Lúc này dòng $I_C$ không còn do dòng kích thích $I_B$ khống chế mà bị giới hạn bởi điện áp nguồn và trở kháng bên ngoài, dẫn đến $\beta_{sat} = \frac{I_C}{I_B} < \beta_F$.
- **Câu hỏi 4:** *Hiệu ứng Early trong BJT là gì và được thể hiện như thế nào trên đồ thị họ đặc tuyến ngõ ra $I_C(V_{CE})$?*  
  **Đáp:** Hiệu ứng Early (điều biến độ rộng Base) là hiện tượng khi điện áp phân cực nghịch $V_{CB}$ (hay $V_{CE}$) tăng lên, vùng nghèo của tiếp giáp Base-Collector mở rộng lấn sâu vào vùng Base làm giảm bề dày hiệu dụng của lớp Base. Khi lớp Base mỏng hơn, tỉ lệ tái hợp hạt dẫn giảm xuống khiến dòng thu $I_C$ tăng nhẹ.  
  Trên đồ thị $I_C - V_{CE}$, điều này khiến các đường đặc tuyến ở vùng tích cực không nằm ngang tuyệt đối mà có độ dốc dương $1/r_o$. Khi ngoại suy các đường này về phía trục điện áp âm, chúng quy tụ tại một điểm duy nhất $-V_A$ trên trục hoành ($V_A$ là điện áp Early, với 2N3904 là $74\,\text{V}$).
- **Câu hỏi 5:** *Tại sao khi đo họ đặc tuyến ngõ ra $I_C(V_{CE})$, người ta phải dùng nguồn dòng $I_B$ làm tham số quét mà không dùng nguồn điện áp $V_{BE}$?*  
  **Đáp:** Vì đặc tuyến ngõ vào $I_B(V_{BE})$ là hàm số mũ dốc đứng ($I_B \propto e^{V_{BE}/V_T}$). Nếu quét theo $V_{BE}$ với các bước điện áp đều nhau (ví dụ mỗi bước $50\,\text{mV}$), dòng $I_C$ sẽ tăng vọt theo cấp số nhân ($e^{\Delta V/V_T} \approx e^2 \approx 7.4$ lần mỗi bước), khiến các đường đặc tuyến bị giãn cách bất đối xứng nghiêm trọng và transistor nhanh chóng bị quá tải dòng điện. Dùng các bước dòng $I_B$ đều nhau ($10\mu\text{A}, 20\mu\text{A}, 30\mu\text{A}, \dots$) sẽ cho ra các đường đặc tuyến $I_C$ song song cách đều nhau rất trực quan và dễ đo $\beta$.
