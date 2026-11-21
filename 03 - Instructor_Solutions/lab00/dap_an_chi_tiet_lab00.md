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

#### b. Mạch Lọc Thông Thấp RC bậc 1
Phương trình vi phân nạp điện cho tụ qua điện trở:
$$R C \frac{dV_{out}(t)}{dt} + V_{out}(t) = V_{in}(t)$$
Khi đặt điện áp bước nhảy $V_{in}(t) = V_0 \cdot u(t)$ với $V_{out}(0) = 0$:
$$V_{out}(t) = V_0 \left(1 - e^{-\frac{t}{RC}}\right)$$
Hằng số thời gian $\tau = R \cdot C = (10 \times 10^3\,\Omega) \times (10 \times 10^{-9}\,\text{F}) = 100.0\,\mu\text{s}$.
- Tại $t = \tau$: $V_{out}(\tau) = V_0 (1 - e^{-1}) \approx 5.0 \times 0.63212 = 3.1606\,\text{V}$ (ngưỡng chuẩn 63.2%).
- Tại $t = 2.2\tau$: $V_{out}(2.2\tau) = V_0 (1 - e^{-2.2}) \approx 4.446\,\text{V}$ (dùng trong đo thời gian sườn tăng $10\% \to 90\%$: $t_r = 2.2\tau$).
- Tại $t = 5\tau$: $V_{out}(5\tau) = V_0 (1 - e^{-5}) \approx 5.0 \times 0.99326 = 4.9663\,\text{V}$ (xem như nạp đầy $100\%$).
- Hàm truyền đạt miền tần số:
  $$H(s) = \frac{1}{1 + sRC} \implies H(j\omega) = \frac{1}{1 + j\omega RC}$$
  Biên độ suy giảm $-3\,\text{dB}$ khi $\omega_c RC = 1$:
  $$f_{-3\text{dB}} = \frac{1}{2\pi R C} = \frac{1}{2\pi \times 100 \times 10^{-6}} \approx 1591.55\,\text{Hz} \approx 1.592\,\text{kHz}$$
  Góc pha tại tần số cắt: $\phi = -\arctan(\omega_c RC) = -\arctan(1) = -45.0^\circ$.

#### c. Mạch Phân cực Phân áp BJT và Mô hình Tín hiệu Lớn Ebers-Moll
Đối với transistor BJT NPN hoạt động ở vùng khuếch đại tích cực (Forward Active):
- Tiếp giáp Base - Emitter phân cực thuận ($V_{BE} \approx 0.65 - 0.70\,\text{V}$).
- Tiếp giáp Base - Collector phân cực nghịch ($V_{BC} < 0 \implies V_C > V_B$).

Phương pháp Thevenin tương đương ngõ vào cực Base:
$$V_{TH} = V_{CC} \frac{R_2}{R_1 + R_2} = 12.0 \times \frac{10}{33 + 10} = \frac{120}{43} \approx 2.7907\,\text{V}$$
$$R_{TH} = R_1 \parallel R_2 = \frac{33 \times 10}{33 + 10} = \frac{330}{43} \approx 7.6744\,\text{k}\Omega$$

Từ phương trình vòng Base - Emitter: $V_{TH} = I_B R_{TH} + V_{BE} + I_E R_E$ với $I_E = (\beta + 1) I_B$:
$$I_{BQ} = \frac{V_{TH} - V_{BE}}{R_{TH} + (\beta + 1) R_E}$$
Với mô hình thực tế của SPICE ($V_{BE} \approx 0.680\,\text{V}$, $\beta = 160$):
$$I_{BQ} = \frac{2.7907 - 0.680}{7.6744 \times 10^3 + 161 \times 1.0 \times 10^3} = \frac{2.1107\,\text{V}}{168.674\,\text{k}\Omega} \approx 12.513\,\mu\text{A}$$
Dòng cực Collector và Emitter:
$$I_{CQ} = \beta I_{BQ} = 160 \times 12.513\,\mu\text{A} \approx 2.002\,\text{mA}$$
$$I_{EQ} = (\beta + 1) I_{BQ} = 161 \times 12.513\,\mu\text{A} \approx 2.015\,\text{mA}$$
Điện áp các cực và điện áp làm việc tĩnh Collector - Emitter:
$$V_E = I_E R_E = 2.015\,\text{mA} \times 1.0\,\text{k}\Omega = 2.015\,\text{V}$$
$$V_B = V_E + V_{BE} = 2.015 + 0.680 = 2.695\,\text{V}$$
$$V_C = V_{CC} - I_{CQ} R_C = 12.0 - 2.002\,\text{mA} \times 2.2\,\text{k}\Omega = 12.0 - 4.404 = 7.596\,\text{V}$$
$$V_{CEQ} = V_C - V_E = 7.596 - 2.015 = 5.581\,\text{V}$$

*Hiệu ứng Early và điện trở ngõ ra tín hiệu nhỏ $r_o$:*  
Do hiện tượng điều biến độ rộng vùng nghèo Base (Base-width modulation), dòng $I_C$ tăng nhẹ theo $V_{CE}$ với độ dốc $1/r_o$:
$$I_C = \beta I_B \left( 1 + \frac{V_{CE}}{V_A} \right) \implies r_o = \frac{V_A + V_{CEQ}}{I_{CQ}} = \frac{74 + 5.581}{2.002 \times 10^{-3}} \approx 39.75\,\text{k}\Omega$$
Điểm $Q(V_{CEQ} = 5.58\,\text{V}, I_{CQ} = 2.00\,\text{mA})$ nằm lý tưởng ở khoảng giữa điện áp nguồn ($V_{CEQ} \approx V_{CC}/2 = 6\,\text{V}$), tạo biên độ dao động ngõ ra cực đại không bị cắt ngọn méo sóng.

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
   - *Hậu quả:* Transistor rơi vào chế độ đảo ngược (Reverse Active Mode) với hệ số khuếch đại dòng $\beta_R \approx 1$ thay vì $\beta_F \approx 160$, dẫn đến dòng $I_C$ tụt thấp bất thường và mạch mất hoàn toàn khả năng khuếch đại.
5. **Bẫy nhầm lẫn đơn vị dòng điện cực Base:**
   - *Lỗi:* Sinh viên ngộ nhận dòng $I_B$ tính bằng mA giống như dòng $I_C$.
   - *Hậu quả:* Khi thiết lập thang quét tham số nguồn dòng $I_B$, nếu nhập `10m` đến `50m` thay vì `10u` đến `50u`, dòng bơm vào Base lên tới hàng chục mA khiến BJT rơi vào bão hòa cực sâu, $V_{CE}$ sụt xuống gần $0\,\text{V}$ và đồ thị họ đặc tuyến biến dạng hoàn toàn.
6. **Bẫy mạch phân cực bị bão hòa do chọn điện trở tải $R_C$ quá lớn:**
   - *Lỗi:* Sinh viên tự ý nâng $R_C$ lên quá cao (ví dụ $10\,\text{k}\Omega$) với hy vọng tăng độ lợi mà không tính lại điểm tĩnh Q.
   - *Hậu quả:* Điện áp sụt trên $R_C$ vượt quá $V_{CC} - V_E$, ép điện thế Collector sụt thấp hơn Base ($V_C < V_B$), đẩy BJT rơi vào vùng bão hòa ($V_{CE} < 0.2\,\text{V}$) làm tê liệt khả năng dao động tín hiệu xoay chiều.

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
3. **Mạch Lọc RC ($R = 10\,\text{k}\Omega, C = 10\,\text{nF}$):**
   - $\tau = 100.0\,\mu\text{s}$ ; $V(\tau) = 3.161\,\text{V}$ ; $V(5\tau) = 4.966\,\text{V}$ ; $f_{-3\text{dB}} = 1591.55\,\text{Hz} \approx 1.592\,\text{kHz}$.
4. **Mạch Phân cực Phân áp BJT 2N3904 ($V_{CC}=12\,\text{V}, R_1=33\,\text{k}\Omega, R_2=10\,\text{k}\Omega, R_C=2.2\,\text{k}\Omega, R_E=1.0\,\text{k}\Omega, \beta=160$):**
   - $V_{TH} = 12 \times \frac{10}{43} = 2.791\,\text{V}$ ; $R_{TH} = \frac{33 \times 10}{43} = 7.674\,\text{k}\Omega$.
   - Dòng Base lý thuyết (với $V_{BE}=0.70\,\text{V}$): $I_B = \frac{2.791 - 0.70}{7.674 + 161 \times 1.0} \approx 12.40\,\mu\text{A}$.
   - Dòng Collector: $I_C = 160 \times 12.40\,\mu\text{A} \approx 1.984\,\text{mA}$ (mô hình SPICE $V_{BE} \approx 0.68\,\text{V} \implies I_C \approx 2.002\,\text{mA}$).
   - Điện áp các cực: $V_E \approx 2.00 - 2.02\,\text{V}$ ; $V_C \approx 7.60 - 7.63\,\text{V}$ ; $V_{CE} \approx 5.58 - 5.63\,\text{V}$.
   - Trạng thái phân cực: BJT hoạt động trong **vùng khuếch đại tích cực** vì $V_{CE} \approx 5.58\,\text{V} > 0.2\,\text{V}$ và tiếp giáp $BC$ phân cực nghịch ($V_B \approx 2.7\,\text{V} < V_C \approx 7.6\,\text{V}$).

---

### b. Phần Thực hành (In-lab Benchmark Data)

| Nội dung thí nghiệm | Thông số đo | Giá trị lý thuyết | Giá trị mô phỏng SPICE | Sai số (%) |
| :--- | :--- | :---: | :---: | :---: |
| **Phân tích `.OP` Cơ bản** | $V(vout)$ | $2.000\,\text{V}$ | **$2.0000\,\text{V}$** | $0.00\%$ |
| | $I(R1)$ | $0.100\,\text{mA}$ | **$0.1000\,\text{mA}$** | $0.00\%$ |
| **Quét `.DC` Cơ bản** | $V_{out}$ tại $V_{in}=5\text{V}$ | $2.000\,\text{V}$ | **$2.0000\,\text{V}$** | $0.00\%$ |
| | Độ dốc $\Delta V_{out}/\Delta V_{in}$ | $0.400$ | **$0.4000$** | $0.00\%$ |
| **Quá độ `.TRAN`** | Hằng số thời gian $\tau$ | $100.0\,\mu\text{s}$ | **$100.00\,\mu\text{s}$** | $< 0.05\%$ |
| **Tần số `.AC`** | Độ lợi tại $10\,\text{Hz}$ | $0.00\,\text{dB}$ | **$0.000\,\text{dB}$** | $0.00\%$ |
| | Tần số cắt $-3\,\text{dB}$ | $1591.55\,\text{Hz}$ | **$1591.5\,\text{Hz}$** | $< 0.01\%$ |
| | Góc pha tại $f_{-3\text{dB}}$ | $-45.00^\circ$ | **$-45.00^\circ$** | $0.00\%$ |
| **Mô hình MOSFET C5N** | $I_{D,sat}$ (NMOS $1.2\mu/0.6\mu$) | $2.0-2.2\,\text{mA}$ | **$2.219\,\text{mA}$** | Phù hợp BSIM3 |
| **Phân cực BJT `.OP`** | Điện áp Base $V(B)$ | $2.695\,\text{V}$ | **$2.695\,\text{V}$** | $0.00\%$ |
| | Điện áp Collector $V(C)$ | $7.600\,\text{V}$ | **$7.596\,\text{V}$** | $0.05\%$ |
| | Điện áp Emitter $V(E)$ | $2.015\,\text{V}$ | **$2.015\,\text{V}$** | $0.00\%$ |
| | Điện áp $V_{CEQ}$ | $5.585\,\text{V}$ | **$5.581\,\text{V}$** | $0.07\%$ |
| | Dòng Collector $I_{CQ}$ | $2.000\,\text{mA}$ | **$2.002\,\text{mA}$** | $0.10\%$ |
| | Dòng Base $I_{BQ}$ | $12.50\,\mu\text{A}$ | **$12.51\,\mu\text{A}$** | $0.08\%$ |
| **Đặc tuyến vào BJT** | $V_{BE}$ tại $I_B = 10\,\mu\text{A}$ | $0.67-0.70\,\text{V}$ | **$0.675\,\text{V}$** | Ngưỡng dẫn thuận |
| **Họ đặc tuyến ra BJT**| $\beta$ tại $V_{CE}=5\,\text{V}$ | $160$ | **$160.0$** | Khớp model Bf=160 |
| | Điện áp bão hòa $V_{CE,sat}$ | $< 0.25\,\text{V}$ | **$0.18 - 0.20\,\text{V}$** | Vùng bão hòa dốc |

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem chấm điểm (Thang 10):
- Chuẩn bị Pre-lab (tính tay mạch phân áp, mạch RC và điểm Q của BJT): **2.0 điểm**.
- Thao tác mô phỏng `.OP` & `.DC` mạch cơ bản: **2.0 điểm**.
- Mô phỏng `.TRAN` và dùng lệnh `.MEAS` đọc đúng $\tau$: **2.0 điểm**.
- Phân tích `.AC` và khảo sát thư viện ngoài `C5_models.txt`: **2.0 điểm**.
- Khảo sát Phân cực DC & Quét họ đặc tuyến BJT (Bài 5): **1.5 điểm**.
- Tác phong, kỷ luật phòng máy và báo cáo hoàn chỉnh: **0.5 điểm**.

### 2. Câu hỏi vấn đáp gợi ý:
- **Câu hỏi 1:** *Tại sao khi đo đáp ứng tần số mạch lọc thông thấp trong SPICE, nguồn xoay chiều luôn được gán biên độ là `AC 1`?*  
  **Đáp:** Vì độ lợi điện áp là $A_V = \frac{V_{out}}{V_{in}} = \frac{V_{out}}{1} = V_{out}$. Khi đó, giá trị điện áp hiển thị trực tiếp là độ lợi; khi chuyển sang thang decibel $20\log_{10}(V_{out})$, ta có ngay đồ thị Bode biên độ chuẩn hóa mà không phải chia cho biên độ vào.
- **Câu hỏi 2:** *Lệnh `.MEAS` hoạt động như thế nào và tại sao cần thiết hơn việc đọc đồ thị bằng trỏ chuột (Cursor)?*  
  **Đáp:** Lệnh `.MEAS` phân tích trực tiếp mảng dữ liệu tính toán của bộ giải vi phân, nội suy điểm chuyển mạch với độ phân giải toán học cực cao ($< 1\,\text{ps}$), triệt tiêu sai số chủ quan của mắt người và cho phép tự động hóa quét tham số hàng loạt.
- **Câu hỏi 3:** *Tại sao trong mạch phân cực phân áp, điện trở $R_E$ ở cực Emitter lại có tác dụng ổn định nhiệt điểm làm việc tĩnh Q? Cơ chế tự điều chỉnh diễn ra như thế nào?*  
  **Đáp:** $R_E$ tạo nên mạch hồi tiếp âm dòng điện một chiều (DC negative current feedback):  
  Khi nhiệt độ $T$ tăng $\implies I_C$ tăng $\implies I_E$ tăng $\implies$ điện áp sụt trên cực Emitter $V_E = I_E R_E$ tăng.  
  Vì điện thế Base $V_B$ được ghim cố định bởi cầu phân áp $R_1-R_2$, nên điện áp Base - Emitter $V_{BE} = V_B - V_E$ sẽ bị giảm xuống $\implies$ dòng kích thích $I_B$ giảm mạnh $\implies$ kéo dòng $I_C = \beta I_B$ giảm trở lại vị trí cân bằng ban đầu. Nhờ đó, điểm tĩnh Q được giữ ổn định trước biến thiên nhiệt độ và sự phân tán của $\beta$.
- **Câu hỏi 4:** *Dựa vào dữ liệu điện áp DC đo được tại 3 cực ($V_B, V_C, V_E$), làm thế nào để khẳng định chắc chắn BJT đang nằm trong vùng khuếch đại tích cực mà không bị rơi vào vùng bão hòa?*  
  **Đáp:** Cần thỏa mãn đồng thời hai điều kiện:  
  1. $V_{BE} = V_B - V_E \approx 0.65 - 0.75\,\text{V} > 0$ (tiếp giáp BE phân cực thuận).  
  2. $V_{BC} = V_B - V_C < 0 \iff V_C > V_B$ (tiếp giáp BC phân cực nghịch, tương đương $V_{CE} > V_{CE,sat} \approx 0.2\,\text{V}$).  
  Nếu $V_C \le V_B$ (tức $V_{CE} \le 0.2\,\text{V}$), tiếp giáp BC chuyển sang phân cực thuận và BJT bị đẩy vào vùng bão hòa.
- **Câu hỏi 5:** *Hiệu ứng Early trong BJT là gì và được thể hiện như thế nào trên đồ thị họ đặc tuyến ngõ ra $I_C(V_{CE})$?*  
  **Đáp:** Hiệu ứng Early (điều biến độ rộng Base) là hiện tượng khi điện áp phân cực nghịch $V_{CB}$ (hay $V_{CE}$) tăng lên, vùng nghèo của tiếp giáp Base-Collector mở rộng lấn sâu vào vùng Base làm giảm bề dày hiệu dụng của lớp Base. Khi lớp Base mỏng hơn, tỉ lệ tái hợp hạt dẫn giảm xuống khiến dòng thu $I_C$ tăng nhẹ.  
  Trên đồ thị $I_C - V_{CE}$, điều này khiến các đường đặc tuyến ở vùng tích cực không nằm ngang tuyệt đối mà có độ dốc dương $1/r_o$. Khi ngoại suy các đường này về phía trục điện áp âm, chúng quy tụ tại một điểm duy nhất $-V_A$ trên trục hoành ($V_A$ là điện áp Early, với 2N3904 là $74\,\text{V}$).
