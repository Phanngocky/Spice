# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 1 (LAB 01)
# ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Mô hình Dòng Hạt dẫn MOSFET Mức Transistor
Trong công nghệ MOSIS SCMOS C5N 0.5µm ($t_{ox} = 9.5\,\text{nm}$, $\lambda = 0.30\,\mu\text{m}$, $V_{DD} = 5.0\,\text{V}$), phương trình dòng điện má $I_{DS}$ của NMOS được mô tả qua 3 vùng hoạt động:

1. **Vùng ngắt (Cut-off):** Khi $V_{GS} < V_{thn}$
   $$I_{DS} \approx 0 \quad (\text{Dòng rò dưới ngưỡng } I_{sub} \propto e^{\frac{V_{GS} - V_{thn}}{n k T / q}})$$
2. **Vùng tuyến tính / Triode:** Khi $V_{GS} \ge V_{thn}$ và $V_{DS} < V_{GS} - V_{thn}$
   $$I_{DS} = \mu_n C_{ox} \frac{W}{L} \left[ (V_{GS} - V_{thn})V_{DS} - \frac{1}{2} V_{DS}^2 \right] (1 + \lambda V_{DS})$$
   Điện trở kênh dẫn khi $V_{DS} \to 0$: $r_{ds} = \frac{1}{\mu_n C_{ox} \frac{W}{L} (V_{GS} - V_{thn})}$.
3. **Vùng bão hòa (Saturation):** Khi $V_{GS} \ge V_{thn}$ và $V_{DS} \ge V_{GS} - V_{thn}$ (kênh dẫn bị nghẽn tại cực má - Pinch-off)
   $$I_{DS} = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_{thn})^2 (1 + \lambda V_{DS})$$
   Độ dẫn truyền: $g_m = \frac{\partial I_{DS}}{\partial V_{GS}} = \sqrt{2 \mu_n C_{ox} \frac{W}{L} I_{DS}}$.  
   Trở kháng ngõ ra tín hiệu nhỏ: $r_o = \frac{\partial V_{DS}}{\partial I_{DS}} \approx \frac{1}{\lambda I_{DS}}$.

---

### 2. Dẫn xuất Giải tích Điểm Ngưỡng Chuyển Mạch $V_M$ của CMOS Inverter

Đặc tuyến truyền đạt tĩnh (Voltage Transfer Characteristic - VTC) thể hiện mối quan hệ $V_{out} = f(V_{in})$.
Điểm chuyển mạch $V_M$ (Switching Threshold) được định nghĩa là vị trí điện áp ngõ vào bằng đúng điện áp ngõ ra:
$$V_{in} = V_{out} = V_M$$

**Dẫn xuất toán học:**
Tại điểm $V_{in} = V_{out} = V_M$, điều kiện bão hòa của cả hai transistor:
- NMOS: $V_{DS,n} = V_M$, điều kiện $V_{DS,n} \ge V_{GS,n} - V_{thn} \iff V_M \ge V_M - V_{thn}$ (luôn thỏa mãn vì $V_{thn} > 0$).
- PMOS: $|V_{DS,p}| = V_{DD} - V_M$, điều kiện $|V_{DS,p}| \ge |V_{GS,p}| - |V_{thp}| \iff V_{DD} - V_M \ge V_{DD} - V_M - |V_{thp}|$ (luôn thỏa mãn vì $|V_{thp}| > 0$).

Do đó, **cả NMOS và PMOS đều hoạt động trong vùng bão hòa**. Cân bằng dòng điện Kirchhoff tại nút ngõ ra $Out$:
$$I_{D,n} = |I_{D,p}| \implies \frac{1}{2} k_n \left(V_M - V_{thn}\right)^2 = \frac{1}{2} k_p \left(V_{DD} - V_M - |V_{thp}|\right)^2$$
Trong đó hệ số dẫn: $k_n = \mu_n C_{ox} \left(\frac{W}{L}\right)_n$ và $k_p = \mu_p C_{ox} \left(\frac{W}{L}\right)_p$.

Lấy căn bậc hai hai vế và đặt $r = \sqrt{\frac{k_p}{k_n}} = \sqrt{\frac{\mu_p (W/L)_p}{\mu_n (W/L)_n}}$:
$$V_M - V_{thn} = r \left(V_{DD} - V_M - |V_{thp}|\right)$$
$$(1 + r) V_M = V_{thn} + r (V_{DD} - |V_{thp}|)$$
$$\implies V_M = \frac{V_{thn} + r (V_{DD} - |V_{thp}|)}{1 + r}$$

#### Chứng minh tỉ số kích thước tối ưu:
Để Inverter có đặc tính đối xứng hoàn hảo, tối đa hóa biên độ chống nhiễu ($NM_L = NM_H$), ta yêu cầu:
$$V_M = \frac{V_{DD}}{2} = 2.50\,\text{V}$$
- **Trường hợp 1 (Giả thiết sách giáo khoa: $V_{thn} = |V_{thp}|$):**
  $$V_M = \frac{V_{DD}}{2} \iff r = 1 \iff k_p = k_n \iff \frac{(W/L)_p}{(W/L)_n} = \frac{\mu_n}{\mu_p} = \frac{120}{40} = \mathbf{3.00}$$
- **Trường hợp 2 (Giải tích chính xác với tham số MOSIS C5N: $V_{thn} = 0.70\,\text{V}, |V_{thp}| = 0.80\,\text{V}$):**
  $$2.50 = \frac{0.70 + r(5.0 - 0.80)}{1 + r} = \frac{0.70 + 4.20 r}{1 + r}$$
  $$2.50 + 2.50 r = 0.70 + 4.20 r \implies 1.70 r = 1.80 \implies r = \frac{1.80}{1.70} \approx 1.0588$$
  $$\implies \frac{k_p}{k_n} = r^2 = 1.0588^2 \approx 1.121$$
  $$\implies \left[\frac{(W/L)_p}{(W/L)_n}\right]_{\text{lý tưởng}} = 1.121 \times \frac{\mu_n}{\mu_p} = 1.121 \times 3.00 = \mathbf{3.36}$$

> [!TIP]
> **Điểm mấu chốt sư phạm:** Khi ta chọn tỉ số định cỡ số nguyên chuẩn lưới $\lambda$ là $\frac{W_p}{W_n} = \frac{12\lambda}{4\lambda} = 3.00$ (thay vì $3.36$), điểm chuyển mạch thực tế sẽ hơi dịch nhẹ xuống dưới:
> $$V_M = \frac{0.70 + 1.0 \times (5.0 - 0.80)}{1 + 1.0} = \frac{0.70 + 4.20}{2} = \mathbf{2.450\,\text{V}}$$
> Độ lệch so với $2.50\,\text{V}$ chỉ là $0.05\,\text{V}$ ($2\%$), hoàn toàn chấp nhận được trong tiêu chuẩn thiết kế tế bào chuẩn công nghiệp.

---

### 3. Phương pháp Tính Điện trở Dẫn $R_{on}$ và Trễ Truyền Lan $RC$

Khi tụ tải $C_L$ được xả từ $V_{DD}$ xuống $0\,\text{V}$ qua transistor NMOS, điểm làm việc của NMOS chuyển dịch từ vùng bão hòa ($V_{out} \in [V_{DD}, V_{DD}-V_{thn}]$) sang vùng tuyến tính ($V_{out} \in [V_{DD}-V_{thn}, 0]$).  
Điện trở dẫn hiệu dụng $R_{on,n}$ được tính bằng trung bình tích phân:
$$R_{on,n} = \frac{1}{V_{DD}/2} \int_{V_{DD}/2}^{V_{DD}} \frac{V}{I_{DS}(V)} dV \approx \frac{3}{4} \frac{V_{DD}}{I_{D,sat}} \left(1 - \frac{7}{9}\lambda V_{DD}\right)$$
Với các tham số thực nghiệm đo được từ file `C5_models.txt`:
- NMOS ($W_n = 1.2\,\mu\text{m}, L = 0.6\,\mu\text{m}$): $R_{on,n} \approx \mathbf{969\,\Omega}$.
- PMOS ($W_p = 3.6\,\mu\text{m}, L = 0.6\,\mu\text{m}$): $R_{on,p} \approx \mathbf{992\,\Omega}$.

**Dẫn xuất hệ số $\ln(2) \approx 0.69$ trong tính trễ:**
Điện áp xả quá độ qua mạch tương đương $RC$:
$$V_{out}(t) = V_{DD} \cdot e^{-\frac{t}{R_{on} C_L}}$$
Thời gian trễ sườn xuống $t_{pHL}$ được định nghĩa tại điểm $V_{out}(t) = 50\% V_{DD}$:
$$0.5 V_{DD} = V_{DD} \cdot e^{-\frac{t_{pHL}}{R_{on} C_L}} \implies e^{\frac{t_{pHL}}{R_{on} C_L}} = 2 \implies t_{pHL} = R_{on} C_L \ln(2) \approx \mathbf{0.693 \cdot R_{on} C_L}$$

---

### 4. Các Bẫy Kỹ thuật & Sai lầm Sinh viên Thường gặp

1. **Quên đặt Well-Tap hoặc Substrate-Tap:**
   - *Hậu quả vật lý:* N-Well bị thả nổi (Floating Well) hoặc P-Substrate không được nối đất. Hiện tượng phân cực ngược mối nối P-N bị phá vỡ, dẫn tới nguy cơ **Latch-up** kích hoạt cặp transistor lưỡng cực ký sinh (Parasitic BJT $pnp-npn$) gây ngắn mạch nguồn $V_{DD}-GND$ phá hủy vi mạch.
   - *Trên công cụ Electric:* Kiểm tra DRC có thể không bắt được lỗi này, nhưng công cụ NCC (LVS) sẽ báo lỗi không khớp nút nguồn/đất hoặc cảnh báo `Unconnected well`.
2. **Nhầm lẫn giữa kích thước hình học ($W/L$) và giá trị $\lambda$:**
   - Trong công nghệ MOSIS SCMOS Submicron, $\lambda = 0.30\,\mu\text{m}$. Kích thước cực tiểu của cổng là $2\lambda = 0.60\,\mu\text{m}$.
   - Sinh viên thường nhập nhầm $W = 4$ thành $4\,\mu\text{m}$ thay vì $4\lambda = 1.2\,\mu\text{m}$.
3. **Lỗi đối chiếu LVS do đặt sai tên Export:**
   - Port trên Schematic đặt tên `In` nhưng Layout đặt tên `IN` hoặc `A`. Electric phân biệt chữ hoa/thường, dẫn đến kết quả LVS báo `Netlists do NOT match`.

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Trích xuất tham số từ `C5_models.txt`
- NMOS: `VTO` = $0.7000\,\text{V}$, `KP` = $120.0\,\mu\text{A/V}^2$, $t_{ox} = 9.5\,\text{nm}$.
- PMOS: `VTO` = $-0.8000\,\text{V}$, `KP` = $40.0\,\mu\text{A/V}^2$, $t_{ox} = 9.5\,\text{nm}$.

### 2. Bảng số liệu đo đạc thực nghiệm Benchmark SPICE

| Thông số đo đạc | Giá trị giải tích | Giá trị mô phỏng Pre-layout | Đo đạc Post-layout (PEX) |
| :--- | :---: | :---: | :---: |
| **Điện áp ngưỡng chuyển mạch $V_M$** | $2.450\,\text{V}$ | **$2.450\,\text{V}$** | $2.448\,\text{V}$ |
| **Điện áp vào mức thấp $V_{IL}$** | $1.820\,\text{V}$ | **$1.815\,\text{V}$** | $1.810\,\text{V}$ |
| **Điện áp vào mức cao $V_{IH}$** | $2.780\,\text{V}$ | **$2.785\,\text{V}$** | $2.790\,\text{V}$ |
| **Lề nhiễu mức thấp $NM_L = V_{IL}$** | $1.820\,\text{V}$ | **$1.815\,\text{V}$** | $1.810\,\text{V}$ |
| **Lề nhiễu mức cao $NM_H = V_{DD} - V_{IH}$**| $2.220\,\text{V}$ | **$2.215\,\text{V}$** | $2.210\,\text{V}$ |
| **Trễ sườn xuống $t_{pHL}$ ($C_L = 50\,\text{fF}$)** | $33.43\,\text{ps}$ | **$34.12\,\text{ps}$** | **$49.85\,\text{ps}$** (+46%) |
| **Trễ sườn lên $t_{pLH}$ ($C_L = 50\,\text{fF}$)** | $34.23\,\text{ps}$ | **$34.85\,\text{ps}$** | **$51.20\,\text{ps}$** (+47%) |
| **Trễ trung bình $t_{pd}$ ($C_L = 50\,\text{fF}$)** | $33.83\,\text{ps}$ | **$34.48\,\text{ps}$** | **$50.52\,\text{ps}$** (+46.5%) |

*Giải thích độ tăng trễ Post-layout:* Quá trình PEX trích xuất thêm điện dung ký sinh cực má $C_{db,n} \approx 8.5\,\text{fF}$, $C_{db,p} \approx 12.0\,\text{fF}$ và điện dung dây kim loại Metal 1 $C_{wire} \approx 3.0\,\text{fF}$. Tổng tải hiệu dụng thực tế tăng từ $50\,\text{fF}$ lên $\approx 73.5\,\text{fF}$, làm trễ tăng thêm xấp xỉ $47\%$.

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem chấm điểm (Thang 10):
- **Chuẩn bị Pre-lab (2.0 điểm):** Tính đúng $W/L$, $V_M$, trễ $RC$, vẽ Stick diagram có Taps.
- **Mô phỏng I-V & VTC Pre-layout (3.0 điểm):** Vẽ đúng dạng sóng, đo chính xác $V_{th}, V_M, NM_L, NM_H$.
- **Layout Inverter, DRC & LVS (3.0 điểm):** Layout gọn gàng, 0 lỗi DRC, LVS báo **"MATCH"**.
- **Trích xuất PEX & Post-layout (1.0 điểm):** Xuất netlist PEX, đo và giải thích được nguyên nhân tăng trễ.
- **Báo cáo & Tác phong (1.0 điểm):** Báo cáo đầy đủ, trung thực, giữ vệ sinh công nghiệp.

### 2. Câu hỏi vấn đáp gợi ý:
- **Hỏi:** *Tại sao bề rộng PMOS phải thiết kế gấp 3 lần NMOS? Nếu thiết kế $W_p = W_n$ thì điều gì xảy ra?*  
  **Đáp:** Do độ linh động của lỗ trống ($\mu_p \approx 40\,\text{cm}^2/\text{V}\cdot\text{s}$) nhỏ hơn 3 lần electron ($\mu_n \approx 120\,\text{cm}^2/\text{V}\cdot\text{s}$) vì hiện tượng tán xạ mạng tinh thể. Nếu $W_p = W_n$, dòng nạp sẽ yếu hơn 3 lần dòng xả, điểm chuyển mạch $V_M$ sẽ bị tụt sâu xuống $\approx 1.7\,\text{V}$, làm lề nhiễu mức thấp $NM_L$ bị bóp hẹp nghiêm trọng và trễ sườn lên $t_{pLH}$ chậm gấp 3 lần $t_{pHL}$.
- **Hỏi:** *Tại sao trong Layout bắt buộc phải có N-Well Tap và Substrate Tap?*  
  **Đáp:** Để dập tắt hiện tượng Latch-up. N-Well Tap giữ điện thế N-Well luôn ở mức cao nhất ($5\,\text{V}$), Substrate Tap giữ điện thế đế luôn ở mức thấp nhất ($0\,\text{V}$), ngăn chặn các mối nối P-N phân cực thuận làm kích hoạt cấu trúc Thyristor ký sinh.
