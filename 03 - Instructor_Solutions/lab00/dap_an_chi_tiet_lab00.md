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

---

### b. Phần Thực hành (In-lab Benchmark Data)

| Nội dung thí nghiệm | Thông số đo | Giá trị lý thuyết | Giá trị mô phỏng SPICE | Sai số (%) |
| :--- | :--- | :---: | :---: | :---: |
| **Phân tích `.OP`** | $V(vout)$ | $2.000\,\text{V}$ | **$2.0000\,\text{V}$** | $0.00\%$ |
| | $I(R1)$ | $0.100\,\text{mA}$ | **$0.1000\,\text{mA}$** | $0.00\%$ |
| **Quét `.DC`** | $V_{out}$ tại $V_{in}=5\text{V}$ | $2.000\,\text{V}$ | **$2.0000\,\text{V}$** | $0.00\%$ |
| | Độ dốc $\Delta V_{out}/\Delta V_{in}$ | $0.400$ | **$0.4000$** | $0.00\%$ |
| **Quá độ `.TRAN`** | Hằng số thời gian $\tau$ | $100.0\,\mu\text{s}$ | **$100.00\,\mu\text{s}$** | $< 0.05\%$ |
| **Tần số `.AC`** | Độ lợi tại $10\,\text{Hz}$ | $0.00\,\text{dB}$ | **$0.000\,\text{dB}$** | $0.00\%$ |
| | Tần số cắt $-3\,\text{dB}$ | $1591.55\,\text{Hz}$ | **$1591.5\,\text{Hz}$** | $< 0.01\%$ |
| | Góc pha tại $f_{-3\text{dB}}$ | $-45.00^\circ$ | **$-45.00^\circ$** | $0.00\%$ |
| **Mô hình MOSFET C5N** | $I_{D,sat}$ (NMOS $1.2\mu/0.6\mu$) | $2.0-2.2\,\text{mA}$ | **$2.219\,\text{mA}$** | Phù hợp BSIM3 |

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem chấm điểm (Thang 10):
- Chuẩn bị Pre-lab (tính tay, đổi đơn vị, soạn sẵn netlist): **2.0 điểm**.
- Thao tác mô phỏng `.OP` & `.DC` chính xác: **2.5 điểm**.
- Mô phỏng `.TRAN` và dùng lệnh `.MEAS` đọc đúng $\tau$: **2.5 điểm**.
- Phân tích `.AC` và khảo sát thư viện ngoài `C5_models.txt`: **2.0 điểm**.
- Tác phong, kỷ luật phòng máy và báo cáo hoàn chỉnh: **1.0 điểm**.

### 2. Câu hỏi vấn đáp gợi ý:
- **Câu hỏi 1:** *Tại sao khi đo đáp ứng tần số mạch lọc thông thấp trong SPICE, nguồn xoay chiều luôn được gán biên độ là `AC 1`?*  
  **Đáp:** Vì độ lợi điện áp là $A_V = \frac{V_{out}}{V_{in}} = \frac{V_{out}}{1} = V_{out}$. Khi đó, giá trị điện áp hiển thị trực tiếp là độ lợi; khi chuyển sang thang decibel $20\log_{10}(V_{out})$, ta có ngay đồ thị Bode biên độ chuẩn hóa mà không phải chia cho biên độ vào.
- **Câu hỏi 2:** *Lệnh `.MEAS` hoạt động như thế nào và tại sao cần thiết hơn việc đọc đồ thị bằng trỏ chuột (Cursor)?*  
  **Đáp:** Lệnh `.MEAS` phân tích trực tiếp mảng dữ liệu tính toán của bộ giải vi phân, nội suy điểm chuyển mạch với độ phân giải toán học cực cao ($< 1\,\text{ps}$), triệt tiêu sai số chủ quan của mắt người và cho phép tự động hóa quét tham số hàng loạt.
