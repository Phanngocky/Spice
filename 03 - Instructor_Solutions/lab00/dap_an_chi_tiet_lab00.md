# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 0 (LAB 00)
# LÀM QUEN MÔ PHỎNG SPICE VỚI LTSPICE
*(Tài liệu chuyên môn nội bộ dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Bản chất Toán học và Thuật toán Giải Mạch của SPICE
SPICE (*Simulation Program with Integrated Circuit Emphasis*) giải bài toán mạch điện bằng cách chuyển đổi sơ đồ phần cứng thành hệ phương trình vi phân phi tuyến tính thông qua **Phương pháp Điện áp Nút Cải biên (Modified Nodal Analysis - MNA)**:

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

   - Điều kiện hội tụ: Khi sai số dòng điện $\le \text{reltol} \times I + \text{abstol}$ và sai số điện áp $\le \text{reltol} \times V + \text{vntol}$.
2. **Quét một chiều `.DC` (DC Sweep):**
   - Thực hiện chuỗi các phân tích `.OP` liên tiếp khi một hoặc nhiều nguồn độc lập thay đổi giá trị theo bước quét đã định. Dùng để khảo sát đặc tuyến tĩnh $I-V$ hoặc hàm truyền đạt $V_{out} = f(V_{in})$.
3. **Phân tích quá độ `.TRAN` (Transient Analysis):**
   - Giải phương trình vi phân theo miền thời gian bằng phương pháp tích phân số (Numerical Integration): **Trapezoidal Rule** (mặc định) hoặc **Gear Method**.
   - Rất nhạy cảm với bước thời gian: Nếu $T_{step}$ quá lớn, thuật toán sẽ bỏ qua sườn dốc và gây ra hiện tượng dao động số giả tạo (Numerical Ringing). Cần chỉ định `dTmax` nhỏ (ví dụ `0.1u`).
4. **Phân tích tín hiệu nhỏ tần số `.AC` (AC Small-Signal Analysis):**
   - Tuyến tính hóa mạch quanh điểm tĩnh DC và giải hệ phương trình tuyến tính phức theo từng tần số để vẽ biểu đồ Bode biên độ ($20\log_{10}|H(j\omega)|$) và góc pha ($\arg H(j\omega)$).

---

### 2. Dẫn xuất Giải tích Mạch Chuẩn

#### a. Mạch Cầu Phân áp DC ($V_{in} = 5.0\,\text{V}, R_1 = 12\,\text{k}\Omega, R_2 = 18\,\text{k}\Omega$)
Áp dụng định luật Ohm và phân áp Kirchhoff:

$$V_{out} = V_{in} \cdot \frac{R_2}{R_1 + R_2} = 5.0 \times \frac{18\,\text{k}\Omega}{12\,\text{k}\Omega + 18\,\text{k}\Omega} = 5.0 \times 0.600 = \mathbf{3.000\,\text{V}}$$

Dòng điện qua mạch:

$$I = \frac{V_{in}}{R_1 + R_2} = \frac{5.0}{30 \times 10^3} = \mathbf{0.1667\,\text{mA}} = 166.7\,\mu\text{A}$$

Tổng công suất tiêu tán toàn mạch:

$$P_{total} = V_{in} \cdot I = 5.0\,\text{V} \times 0.1667\,\text{mA} = \mathbf{0.8333\,\text{mW}} = 833.3\,\mu\text{W}$$

Độ dốc hàm truyền đạt khi quét $V_{in}$ từ $0 \to 10\,\text{V}$:

$$\text{Slope} = \frac{\Delta V_{out}}{\Delta V_{in}} = \frac{R_2}{R_1 + R_2} = \frac{18}{30} = \mathbf{0.6000}$$

#### b. Mạch RC Nạp - Xả Quá độ ($R = 20\,\text{k}\Omega, C = 5\,\text{nF}, V_0 = 5.0\,\text{V}$)
Hằng số thời gian mạch RC:

$$\tau = R \cdot C = (20 \times 10^3\,\Omega) \times (5 \times 10^{-9}\,\text{F}) = 100.0\,\mu\text{s} = 0.100\,\text{ms}$$

1. **Giai đoạn Nạp điện ($0 \le t < T_{on} = 500\,\mu\text{s}$):**
   - Phương trình điện áp: $v_C(t) = V_0 (1 - e^{-t/\tau})$.
   - Dòng điện nạp cực đại tại $t=0^+$:

     $$I_{peak,charge} = +\frac{V_0}{R} = +\frac{5.0}{20 \times 10^3} = +\mathbf{0.250\,\text{mA}} \quad (+250.0\,\mu\text{A})$$

   - Tại $t = \tau = 100\,\mu\text{s}$: $v_C(\tau) = 5.0 \times (1 - e^{-1}) \approx 5.0 \times 0.63212 = \mathbf{3.1606\,\text{V}}$ ($63.2\%$).
   - Thời gian trễ 50%: $t_{50} = t_{pd} = \tau \ln(2) \approx 100\,\mu\text{s} \times 0.69315 = \mathbf{69.315\,\mu\text{s}}$.
   - Thời gian sườn tăng 10% đến 90%:

     $$t_r = t_{90\%} - t_{10\%} = \tau \ln(9) \approx 2.1972 \cdot \tau = \mathbf{219.72\,\mu\text{s}} \approx 2.2 \cdot \tau$$

   - Tại $t = 5\tau = 500\,\mu\text{s}$: $v_C(5\tau) = 5.0 \times (1 - e^{-5}) = \mathbf{4.9663\,\text{V}}$ ($99.33\% \approx 100\%$, nạp đầy hoàn toàn).

2. **Giai đoạn Xả điện ($500\,\mu\text{s} \le t < 1000\,\mu\text{s}$, đặt $t' = t - 500\,\mu\text{s}$):**
   - Phương trình điện áp: $v_C(t') = V_0 e^{-t'/\tau}$.
   - Dòng điện xả cực đại tại $t'=0^+$: $I_{peak,discharge} = -\frac{V_0}{R} = -\mathbf{0.250\,\text{mA}}$ (dòng âm phóng từ tụ về đất).
   - Tại $t' = \tau = 100\,\mu\text{s}$: $v_C = 5.0 \times e^{-1} = \mathbf{1.8394\,\text{V}}$ ($36.8\%$).
   - Thời gian sườn giảm 90% về 10%: $t_f = 2.2 \cdot \tau = \mathbf{219.72\,\mu\text{s}}$.
   - Tại $t' = 5\tau$: $v_C = 5.0 \times e^{-5} = \mathbf{0.0337\,\text{V}}$ ($0.67\% \approx 0\,\text{V}$, xả kiệt).

3. **Đáp ứng tần số AC (.AC):**
   - Tần số cắt $-3\,\text{dB}$:

     $$f_{-3\text{dB}} = \frac{1}{2\pi R C} = \frac{1}{2\pi \times 100 \times 10^{-6}} \approx \mathbf{1591.55\,\text{Hz}} \approx \mathbf{1.592\,\text{kHz}}$$

   - Góc pha tại tần số cắt: $\phi = -\arctan(2\pi f_c R C) = -\arctan(1) = \mathbf{-45.0^\circ}$.

4. **Quét tham số R với `.param` và `.step` (Ex0.4):**
   Phương trình trễ: $t_{pd}(R) = \ln(2) \cdot C \cdot R$.
   - Khi $R = 5\,\text{k}\Omega$: $t_{pd} = 0.69315 \times 5 \times 10^3 \times 5 \times 10^{-9} = \mathbf{17.329\,\mu\text{s}}$
   - Khi $R = 10\,\text{k}\Omega$: $t_{pd} = \mathbf{34.657\,\mu\text{s}}$
   - Khi $R = 20\,\text{k}\Omega$: $t_{pd} = \mathbf{69.315\,\mu\text{s}}$
   - Khi $R = 40\,\text{k}\Omega$: $t_{pd} = \mathbf{138.629\,\mu\text{s}}$
   - Độ dốc đường thẳng: $\text{Slope} = \ln(2) \cdot C = 0.69315 \times 5 \times 10^{-9} = \mathbf{3.4657 \times 10^{-9}\,\text{s}/\Omega} = \mathbf{3.4657\,\text{ns}/\text{k}\Omega}$.

---

## PHẦN II: ĐÁP ÁN CHI TIẾT PRE-LAB (CHUẨN BỊ Ở NHÀ)

### P1. Quy ước đơn vị
- `2.2M` $\to$ **$2.2 \times 10^{-3} = 0.0022$** (milli).
- `2.2Meg` $\to$ **$2.2 \times 10^6 = 2\,200\,000$** (mega).
- `47n` $\to$ **$47 \times 10^{-9} = 0.000000047$** (nano).
- `30f` $\to$ **$30 \times 10^{-15}$** (femto).

### P2. Mạch cầu phân áp DC
- $V_{out} = 5.0 \times \frac{18}{12 + 18} = \mathbf{3.000\,\text{V}}$.
- $I = \frac{5.0}{30 \times 10^3} = \mathbf{0.1667\,\text{mA}} = 166.7\,\mu\text{A}$.
- $P_{total} = 5.0 \times 0.1667 \times 10^{-3} = \mathbf{0.8333\,\text{mW}} = 833.3\,\mu\text{W}$.

### P3. Mạch RC nạp - xả
- $\tau = 20\,\text{k}\Omega \times 5\,\text{nF} = \mathbf{100.0\,\mu\text{s}} = 0.100\,\text{ms}$.
- $v_C(\tau) = 5.0 \times (1 - e^{-1}) = \mathbf{3.161\,\text{V}}$.
- $t_{50} = \ln(2) \times 100\,\mu\text{s} = \mathbf{69.32\,\mu\text{s}}$.
- $t_r = \ln(9) \times 100\,\mu\text{s} = \mathbf{219.72\,\mu\text{s}} \approx 2.2\tau = 220\,\mu\text{s}$.
- $f_{-3\text{dB}} = \frac{1}{2\pi \times 100\,\mu\text{s}} = \mathbf{1.592\,\text{kHz}}$.
- Đỉnh dòng nạp: $I_{peak} = \frac{5.0}{20\,\text{k}\Omega} = \mathbf{0.250\,\text{mA}} = 250\,\mu\text{A}$.
- *Dự đoán khi $C \to 2C$:* Khi điện dung tăng gấp đôi ($C' = 2C$), hằng số thời gian $\tau' = 2\tau$ tăng gấp đôi, do đó trễ $t_{50}$ **tăng gấp đôi** (mạch chạy chậm gấp 2 lần) và tần số cắt $f_{-3\text{dB}}$ **giảm một nửa** (băng thông hẹp đi một nửa).

### P4. Khung Netlist SPICE hoàn chỉnh
```spice
* Lab0 RC Circuit Transient Netlist
V1 in 0 PULSE(0 5.0 0 10n 10n 500u 1000u)
R1 in out 20k
C1 out 0 5n
.tran 0 1m 0 0.1u
.meas TRAN t_pd TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 RISE=1
.end
```

### P5. Liên hệ thực tế VLSI
Với $R_{on} = 1\,\text{k}\Omega$ và $C_L = 50\,\text{fF}$:

$$t_{50} = 0.69315 \times (1 \times 10^3\,\Omega) \times (50 \times 10^{-15}\,\text{F}) = 3.466 \times 10^{-11}\,\text{s} = \mathbf{34.66\,\text{ps}} \approx \mathbf{34.7\,\text{ps}}$$

*(Giá trị $34.7\,\text{ps}$ này khớp hoàn toàn với kết quả mô phỏng trễ $t_{pHL}, t_{pLH}$ của Inverter C5N ở Lab 1).*

---

## PHẦN III: KẾT QUẢ MÔ PHỎNG THỰC HÀNH BENCHMARK (IN-LAB)

| Bài tập | Tham số đo | Giá trị Lý thuyết | Kết quả SPICE `.meas` | Sai lệch tương đối | Đánh giá đạt chuẩn |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Ex0.1** | $V(vout)$ (.op) | $3.0000\,\text{V}$ | **$3.0000\,\text{V}$** | $0.00\%$ | Chuẩn xác tuyệt đối |
| **Ex0.1** | $I(R1)$ (.op) | $0.1667\,\text{mA}$ | **$0.1667\,\text{mA}$** | $0.00\%$ | Dòng chạy từ in sang out |
| **Ex0.1** | Độ dốc $\Delta V_{out}/\Delta V_{in}$ | $0.6000$ | **$0.6000$** | $0.00\%$ | Tuyến tính hoàn hảo |
| **Ex0.2** | Trễ $t_{pd}$ ($50\%$) | $69.315\,\mu\text{s}$ | **$69.31 - 69.33\,\mu\text{s}$** | $< 0.05\%$ | $\le 2.0\%$ |
| **Ex0.2** | Sườn tăng $t_r$ ($10\% \to 90\%$) | $219.72\,\mu\text{s}$ | **$219.5 - 220.0\,\mu\text{s}$** | $< 0.15\%$ | $\le 2.0\%$ |
| **Ex0.2** | Sườn giảm $t_f$ ($90\% \to 10\%$) | $219.72\,\mu\text{s}$ | **$219.5 - 220.0\,\mu\text{s}$** | $< 0.15\%$ | $\le 2.0\%$ |
| **Ex0.2** | Đỉnh dòng nạp $I_{peak,chg}$ | $+0.2500\,\text{mA}$ | **$+0.2500\,\text{mA}$** | $0.00\%$ | Tại $t = 0^+$ |
| **Ex0.2** | Đỉnh dòng xả $I_{peak,dis}$ | $-0.2500\,\text{mA}$ | **$-0.2500\,\text{mA}$** | $0.00\%$ | Đảo chiều tại $t = 500\,\mu\text{s}$ |
| **Ex0.3** | Độ lợi dải thông $A_{V,0}$ | $1.000$ ($0\,\text{dB}$) | **$0.000\,\text{dB}$** | $0.00\%$ | Tần số thấp $10\,\text{Hz}$ |
| **Ex0.3** | Tần số cắt $f_{-3\text{dB}}$ | $1591.55\,\text{Hz}$ | **$1591 - 1593\,\text{Hz}$** | $< 0.10\%$ | $\le 2.0\%$ |
| **Ex0.3** | Góc pha tại $f_{-3\text{dB}}$ | $-45.0^\circ$ | **$-44.9^\circ - -45.1^\circ$** | $< 0.20\%$ | Trục pha bên phải |
| **Ex0.4** | $t_{pd}$ tại $R=5\,\text{k}\Omega$ | $17.329\,\mu\text{s}$ | **$17.33\,\mu\text{s}$** | $0.00\%$ | Quét bước 1 |
| **Ex0.4** | $t_{pd}$ tại $R=10\,\text{k}\Omega$ | $34.657\,\mu\text{s}$ | **$34.66\,\mu\text{s}$** | $0.00\%$ | Quét bước 2 |
| **Ex0.4** | $t_{pd}$ tại $R=20\,\text{k}\Omega$ | $69.315\,\mu\text{s}$ | **$69.32\,\mu\text{s}$** | $0.00\%$ | Quét bước 3 |
| **Ex0.4** | $t_{pd}$ tại $R=40\,\text{k}\Omega$ | $138.629\,\mu\text{s}$ | **$138.63\,\mu\text{s}$** | $0.00\%$ | Quét bước 4 |
| **Ex0.4** | Hệ số góc $\frac{\Delta t_{pd}}{\Delta R}$ | $3.4657\,\text{ns}/\text{k}\Omega$ | **$3.466\,\text{ns}/\text{k}\Omega$** | $< 0.05\%$ | Trùng khớp $\ln(2) \cdot C$ |
| **Ex0.5** | Dòng $I_D$ NMOS C5N ($5\text{V}/5\text{V}$) | Ước lượng $\sim 2.2\,\text{mA}$ | **$1.35 - 1.45\,\text{mA}$** | Sai lệch mô hình | Do hiệu ứng vận tốc bão hòa |

---

## PHẦN IV: ĐÁP ÁN CÂU HỎI POST-LAB

1. **Tại sao $T_{on} \ge 5\tau$? Nếu $T_{on} = 2\tau$ thì điện áp đỉnh đạt bao nhiêu?**
   - *Đáp:* Trong mạch RC, sau $5\tau$, điện áp nạp đạt $1 - e^{-5} \approx 99.33\% \approx 100\%$ giá trị nguồn $V_0$. Nếu đặt $T_{on} < 5\tau$, tụ chưa nạp no đã chuyển sang xả. Với $T_{on} = 2\tau$, điện áp đỉnh chỉ đạt:

     $$v_C(2\tau) = 5.0 \times (1 - e^{-2}) \approx 5.0 \times 0.8647 = \mathbf{4.323\,\text{V}}$$

     Bị sụt mất $0.677\,\text{V}$ ($13.5\%$) so với $5.0\,\text{V}$, làm các phép đo thời gian sườn $t_r$ ($10\% \to 90\%$) bị hỏng hoàn toàn.
2. **Chứng minh $t_{50} = \ln(2) \cdot \tau$ từ phương trình nạp:**
   - *Chứng minh:*
     Đặt $v_C(t_{50}) = 0.5 V_0$:

     $$V_0 \left(1 - e^{-\frac{t_{50}}{\tau}}\right) = 0.5 V_0 \iff 1 - e^{-\frac{t_{50}}{\tau}} = 0.5 \iff e^{-\frac{t_{50}}{\tau}} = 0.5$$

     Lấy logarit tự nhiên hai vế:

     $$-\frac{t_{50}}{\tau} = \ln(0.5) = -\ln(2) \implies t_{50} = \ln(2) \cdot \tau \approx 0.69315 \cdot \tau$$

3. **Mối liên hệ giữa bảng ước lượng trễ P5 và thực tế Lab 1:**
   - *Đáp:* Ở Lab 1, CMOS Inverter chuẩn có $W_n = 1.2\,\mu\text{m}, W_p = 3.6\,\mu\text{m}$ với điện trở hiệu dụng trung bình $R_{on} \approx 1\,\text{k}\Omega$. Khi kéo tải dung $C_L = 50\,\text{fF}$, mô phỏng thực tế cho ra trễ truyền lan $t_{pd} \approx 33.8 - 34.5\,\text{ps}$. Kết quả này trùng khớp gần như hoàn hảo với ước lượng $34.7\,\text{ps}$ ở bài tập P5, khẳng định mô hình $RC$ bậc nhất là công cụ ước lượng trễ đầu tiên cực kỳ tin cậy trong thiết kế VLSI.
4. **Hai lỗi thường gặp và giải pháp:**
   - *Lỗi 1:* Khai báo `10M` khiến mạch hiểu là $10\,\text{m}\Omega$, điện trở quá bé làm phân áp sai. Khắc phục: đổi thành `10Meg`.
   - *Lỗi 2:* Quên ngoặc nhọn `{Rval}` khi dùng `.step param Rval list ...`, khiến LTspice coi `{Rval}` là một chuỗi văn bản tĩnh và kết quả các bước không thay đổi. Khắc phục: bọc tên biến trong cặp ngoặc `{}`.

---

## PHẦN V: HƯỚNG DẪN CHẤM THI VẤN ĐÁP TẠI BÀN (ORAL QUESTIONS)

1. *Hỏi:* "Tại sao khi chạy mô phỏng `.tran`, lệnh `.meas` của bạn lại báo lỗi `Measurement FAIL` hoặc không tìm thấy điểm chuyển mạch?"  
   *Đáp:* Do chưa khai báo bước thời gian tối đa `dTmax` (hoặc để `dTmax` quá lớn). Khi bước thời gian quá thô, SPICE nội suy nhảy cóc qua mốc điện áp $2.5\,\text{V}$ khiến thuật toán tìm nghiệm không thỏa mãn điều kiện `TRIGGER`. Cần đặt `dTmax = 0.1u`.
2. *Hỏi:* "Ý nghĩa của việc khai báo nguồn `AC 1 0` trong phân tích Bode là gì? Nếu tôi đổi thành `AC 10 0` thì đồ thị có đổi không?"  
   *Đáp:* Hàm truyền độ lợi là $A_V = \frac{V_{out}}{V_{in}}$. Khi đặt $V_{in} = 1\,\text{V}$, thì điện thế $V(out)$ chính là $A_V$ và thang decibel $20\log_{10}(V(out)/1) = 20\log_{10}(V(out))$, giúp đo trực tiếp không cần chia. Nếu đặt $V_{in} = 10\,\text{V}$ mà chỉ vẽ $V(out)$ thì đồ thị sẽ bị dời lên $+20\,\text{dB}$; khi đó bắt buộc phải gõ biểu thức đo là `V(out)/V(in)`.
3. *Hỏi:* "Tại sao khi đo dòng điện qua tụ $I(C1)$ ở thời điểm nạp, đồ thị của bạn lại hiển thị giá trị âm $-0.25\,\text{mA}$ thay vì dương $+0.25\,\text{mA}$?"  
   *Đáp:* Do trong LTspice, linh kiện thụ động có quy ước chiều dòng điện đi từ cực 1 sang cực 2. Nếu khi vẽ ta vô tình đặt tụ bị lộn ngược cực thì dòng nạp sẽ bị đo ngược dấu. Khắc phục bằng cách chọn linh kiện và xoay `Ctrl + R` hai lần.
4. *Hỏi:* "Từ đồ thị Ex0.4, làm thế nào để chứng minh hệ số của công thức trễ là $\approx 0.69$ mà không cần nhìn vào công thức lý thuyết?"  
   *Đáp:* Lấy độ dốc thực nghiệm của đồ thị $\text{Slope} = \frac{\Delta t_{pd}}{\Delta R}$. Ta có $\text{Slope} = k \cdot C$. Chia độ dốc đo được ($3.466 \times 10^{-9}$) cho giá trị tụ điện $C = 5 \times 10^{-9}\,\text{F}$, ta rút ra hệ số thực nghiệm: $k = \frac{3.466 \times 10^{-9}}{5 \times 10^{-9}} \approx \mathbf{0.693} \approx \ln(2)$.
