# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 01 — TEACHER'S BOOK: ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-01-dac-tinh-mosfet-va-cmos-inverter.md](../02%20-%20Student%20Workbook/lab-01-dac-tinh-mosfet-va-cmos-inverter.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab01/](../03%20-%20Instructor_Solutions/lab01/)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda_{DR} = 0,30\,\mu\text{m}, L_{min} = 2\lambda_{DR} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

# 1. LAB 1 — ĐẶC TÍNH I-V CỦA MOSFET VÀ CMOS INVERTER (CHƯƠNG 2, 4)

## 1.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. **Nhận biết và đo đạc chính xác 3 vùng hoạt động của MOSFET** (Cut-off, Triode, Saturation) trên họ đặc tuyến thực tế; giải thích được vì sao dòng bão hòa bị uốn cong lên (hiệu ứng điều chế chiều dài kênh $\lambda_{CLM}$).
2. **Hiểu bản chất điểm điện áp chuyển mạch $V_M$:** do tỉ số độ dẫn dòng $r = \beta_p / \beta_n$ quyết định và tính được chính xác trước khi bật máy.
3. **Nắm vững bản chất trễ truyền lan $t_{pd}$:** công thức $0,69 \cdot R_{on} \cdot C_L$ là cận dưới giải tích; trễ đo thực tế phản ánh quá trình xả dòng qua vùng bão hòa trước khi tới vùng tuyến tính.
4. **Nắm chắc quy trình thiết kế vật lý vi mạch (Full-Flow IC Design):** Schematic $\to$ VTC $\to$ Layout $\to$ DRC $\to$ LVS (NCC) $\to$ PEX. Không có LVS và DRC sạch, sơ đồ nguyên lý không có giá trị sản xuất.

---

## 1.2 Bản chất vật lý & Giải thích chuyên sâu cho giảng viên

### a. Phân biệt rõ hai ký hiệu $\lambda$
Ngay đầu buổi học, giảng viên viết lên bảng hai định nghĩa tách biệt hoàn toàn để sinh viên không nhầm lẫn:
- **$\lambda_{CLM}$ (Channel Length Modulation, đơn vị $\text{V}^{-1}$):** Hệ số điều chế chiều dài kênh trong phương trình dòng điện SPICE $I_{DS} = I_{DS0}(1 + \lambda_{CLM} V_{DS})$.
- **$\lambda_{DR}$ (Design Rule Grid, đơn vị $\mu\text{m}$):** Đơn vị chiều dài cơ sở của lưới layout theo luật Mead-Conway SCMOS ($\lambda_{DR} = 0,30\,\mu\text{m}$ trong tiến trình C5N $0,5\,\mu\text{m}$).

### b. Suy dẫn điểm chuyển mạch $V_M$
Tại điểm chuyển mạch $V_{in} = V_{out} = V_M$, cả hai transistor NMOS và PMOS đều cùng ở trạng thái bão hòa:
$$I_{DS,n} = \frac{1}{2} K'_n \left(\frac{W}{L}\right)_n (V_M - V_{thn})^2$$
$$I_{DS,p} = \frac{1}{2} K'_p \left(\frac{W}{L}\right)_p (V_{DD} - V_M - |V_{thp}|)^2$$

Cân bằng dòng điện $I_{DS,n} = I_{DS,p}$ và đặt tỉ số độ dẫn:
$$r = \frac{\beta_p}{\beta_n} = \frac{K'_p (W/L)_p}{K'_n (W/L)_n}$$

Khai căn hai vế và rút ra biểu thức tổng quát:
$$V_M = \frac{V_{thn} + \sqrt{r} (V_{DD} - |V_{thp}|)}{1 + \sqrt{r}}$$

**Đối chiếu định lượng quan trọng:**
- Khi $r = 1$ (tức chọn $W_p / W_n = K'_n / K'_p = 3,0$):
  $$V_M = \frac{0,70 + 1,0 \cdot (5,0 - 0,80)}{2} = \frac{4,90}{2} = \mathbf{2,450\,\text{V}}$$
- **Nguyên nhân $V_M \neq 2,50\,\text{V}$:** Điểm $V_M$ không nằm đúng giữa nguồn ($2,50\,\text{V}$) vì có sự bất đối xứng bản chất giữa hai điện áp ngưỡng chế tạo: $V_{thn} = 0,70\,\text{V} \neq |V_{thp}| = 0,80\,\text{V}$.
- **Để đạt được $V_M = 2,500\,\text{V}$:**
  $$\sqrt{r} = \frac{2,50 - 0,70}{5,0 - 2,50 - 0,80} = \frac{1,80}{1,70} \approx 1,0588 \implies r \approx 1,1211$$
  $$\left(\frac{W}{L}\right)_p = 3 \cdot 1,1211 \cdot \left(\frac{W}{L}\right)_n \approx \mathbf{3,363} \cdot \left(\frac{W}{L}\right)_n$$
  Với $W_n = 4\lambda_{DR} = 1,20\,\mu\text{m} \implies W_p = 13,45\lambda_{DR} \approx 4,04\,\mu\text{m}$.
- **Lý do chọn $W_p = 12\lambda_{DR} = 3,60\,\mu\text{m}$ ($W_p/W_n = 3,0$):**  
  Do quy tắc thiết kế yêu cầu số nguyên $\lambda_{DR}$, việc chọn $W_p = 12\lambda_{DR}$ và $W_n = 4\lambda_{DR}$ là giải pháp tối ưu thực tế, chấp nhận độ lệch $V_M$ chỉ $2\%$ ($-50\,\text{mV}$) để đạt được tính mô-đun hóa và đối xứng ô chuẩn khi xếp layout.

### c. Bảng đối chiếu điểm chuyển mạch $V_M$
| $W_p / W_n$ | Tỉ số $r$ | $V_M$ Suy dẫn bậc 2 | $V_M$ SPICE Level 3 | Cột Đo thực nghiệm | Nhận xét sư phạm |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **1,0** | 0,333 | $1,98\,\text{V}$ | $2,05\,\text{V}$ | `[        ]` | Kéo xuống thắng thế; VTC lệch mạnh sang trái. |
| **2,0** | 0,667 | $2,27\,\text{V}$ | $2,31\,\text{V}$ | `[        ]` | Low-skew inverter; dùng trong domino logic. |
| **3,0** | 1,000 | **$2,45\,\text{V}$** | **$2,47\,\text{V}$** | `[        ]` | Thiết kế chuẩn cân bằng trễ $t_{pHL} \approx t_{pLH}$. |
| **3,36** | 1,121 | $2,50\,\text{V}$ | $2,51\,\text{V}$ | `[        ]` | Cân bằng tuyệt đối điểm đối xứng $V_{DD}/2$. |

---

## 1.3 Hình minh họa chi tiết & Sơ đồ giải phẫu tế bào Inverter

```
                      VDD (5.0V)
                          │
                   +------+------+
                   │    PMOS     │
                   │  W=12λ, L=2λ│
    Vin -----------+--||---------+-------- Vout
                   │  W=4λ,  L=2λ│
                   │    NMOS     │
                   +------+------+
                          │
                         GND
```

*Sơ đồ nguyên lý và mặt cắt vật lý tế bào CMOS Inverter chuẩn (`INV_X1`). Vùng N-well bảo bọc PMOS; các tiếp xúc Well-Tap ($N^+$ nối $V_{DD}$) và Substrate-Tap ($P^+$ nối GND) triệt tiêu ký sinh SCR chống Latch-up.*

*Mã nguồn SPICE tham chiếu sẵn sàng trong kho học liệu:*
- Mô phỏng VTC & Đo trễ: [cmos_inverter_vtc_tran.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_vtc_tran.sp)
- Kiểm chứng trích xuất PEX: [cmos_inverter_pex_postlayout.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_pex_postlayout.sp)

---

## 1.4 Giải thích bản chất trễ $t_{pd}$ và sai lệch với mô hình $0,69 \cdot RC$
- **Nguồn gốc công thức $0,69$:** Xuất phát từ phương trình vi phân phóng nạp mạch RC tuyến tính thuần túy: $V(t) = V_{DD} \cdot e^{-t/RC}$. Tại ngưỡng $50\%$ ($V(t) = 0,5 V_{DD}$), ta có $e^{-t/RC} = 0,5 \implies t_{50\%} = RC \ln 2 \approx 0,693 \cdot RC$.
- **Tại sao số đo SPICE luôn lớn hơn $\sim 1,5$ đến $1,8$ lần:**  
  Điện trở $R_{on,n} = 969\,\Omega$ được tính tại điểm cuối của quá trình xả ($V_{DS} \to 0$, vùng tuyến tính sâu). Tuy nhiên, khi ngõ vào chuyển từ $0 \to 5\,\text{V}$, tụ tải $C_L$ đang ở mức $5\,\text{V}$, làm NMOS hoạt động trong vùng **Bão hòa** trong suốt giai đoạn đầu ($V_{out} > 5,0 - 0,7 = 4,3\,\text{V}$) với dòng bão hòa bị chặn ở mức:
  $$I_{sat,n} \approx \frac{1}{2} K'_n \left(\frac{W}{L}\right)_n (V_{DD} - V_{thn})^2 = \frac{1}{2} (120\mu) (2) (4,3)^2 \approx 2,22\,\text{mA}$$
  Để xả điện áp từ $5,0\,\text{V}$ xuống ngưỡng $50\%$ ($2,5\,\text{V}$), thời gian xả dòng xấp xỉ bằng:
  $$t \approx \frac{C_L \cdot \Delta V}{I_{sat,n}} = \frac{50\,\text{fF} \cdot 2,5\,\text{V}}{2,22\,\text{mA}} \approx 56,3\,\text{ps}$$
  Con số $56,3\,\text{ps}$ này khớp chặt chẽ với kết quả tích phân giải tích số ($49,8\,\text{ps}$) và SPICE Level 3 ($50 - 56\,\text{ps}$), cao hơn rõ rệt so với con số tính nhanh $0,69 \cdot 969\,\Omega \cdot 50\,\text{fF} = 33,6\,\text{ps}$.

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN SPICE BENCHMARK

## A. KẾ HOẠCH BUỔI VÀ VIỆC CHUẨN BỊ

### A1. Mục đích của buổi học
Buổi học thực hành Lab 1 là bước chuyển bản lề từ mô phỏng linh kiện rời rạc thụ động (Lab 0) sang thiết kế tế bào logic vi mạch tích hợp CMOS cơ sở. Sau buổi học, sinh viên cần mang ra khỏi phòng máy 3 thói quen kỹ thuật cốt lõi:
1. **Thói quen "Tính trước, đo sau, so sánh và giải thích sai lệch":** Tránh chấp nhận thụ động một con số từ phần mềm mà phải luôn có giá trị ước lượng giải tích để đối chứng.
2. **Kỹ năng kiểm chứng vật lý đa chiều (Full-Flow IC Design):** Nắm vững chu trình thiết kế vi mạch hoàn chỉnh từ Schematic $\to$ Phân tích VTC $\to$ Đo trễ Transient $\to$ Mask Layout $\to$ Kiểm tra luật DRC $\to$ So khớp sơ đồ LVS.
3. **Ý thức kỷ luật thiết kế vi mạch chống phá hủy:** Thấu hiểu nguyên lý vật lý của hiện tượng Latch-up và quy tắc bố trí đầy đủ tiếp xúc phân cực Substrate Tap và Well Tap.

### A2. Phân bổ 135 phút thực hành tại phòng máy

| Thời lượng | Phân đoạn | Nội dung hoạt động chính | Ghi chú hướng dẫn cho Giảng viên |
| :---: | :--- | :--- | :--- |
| **10 phút** (00–10') | **C0. Cổng kiểm tra Pre-lab** | Kiểm tra bài chuẩn bị ở nhà (P1–P7) tại bàn; ký phiếu kiểm tra đầu giờ. | SV thiếu P2 hoặc P4 chưa được bật máy tính. Nhắc nhở quy ước lưới $\lambda_{DR} = 0,30\,\mu\text{m}$. |
| **25 phút** (10–35') | **C1. Ex1.1: Đặc tính I-V MOSFET** | Quét DC hai biến trên LTspice; vẽ họ đặc tuyến $I_{DS}-V_{DS}$ và $I_{DS}-V_{GS}$; đo $V_{th}, \lambda_{CLM}$. | Hướng dẫn đo $\lambda_{CLM}$ trên nhánh $V_{GS}=3\,\text{V}$ ($V_{DS1}=3\text{V}, V_{DS2}=5\text{V}$). |
| **25 phút** (35–60') | **C2. Ex1.2: Schematic & VTC** | Dựng Schematic `inv_x1` trong Electric, xuất netlist sang LTspice; quét DC $V_{in}$; đo $V_M, NM_L, NM_H$. | Hướng dẫn vẽ đạo hàm `d(V(out))/d(V(in))` để tìm chính xác điểm dốc $-1$. |
| **20 phút** (60–80') | **C3. Ex1.3: Đo trễ với `.meas`** | Đặt nguồn PULSE ($50\,\text{MHz}$), tải dung $C_L = 50\,\text{fF}$; chạy `.meas` trích xuất trễ ở 3 mức tải. | Mở SPICE Error Log (`Ctrl+L`) để đọc số; đối chiếu với công thức $0,69 R C$. |
| **45 phút** (80–125')| **C4. Ex1.4: Mask Layout & LVS** | Vẽ Layout trong Electric tuân thủ quy tắc MOSIS ($H_{cell}=40\lambda$, ray $6\lambda$); DRC (`F5`); NCC (LVS). | Hướng dẫn đặt Taps chống Latch-up; sửa lỗi lệch tên Export làm LVS không match. |
| **10 phút** (125–135')| **C5. Nghiệm thu & Tổng kết** | Vấn đáp nhanh tại bàn (1 câu hỏi); ký phiếu nghiệm thu kết quả; giao việc Post-lab. | Đánh giá thái độ, kiểm tra thư viện `lab_vlsi.jelib` đã lưu đủ các cell hay chưa. |

---

## B. ĐÁP ÁN CHI TIẾT CÂU HỎI PRE-LAB (P1 – P7)

### P1. Trích xuất tham số từ `C5_models.txt` (Level 3)
- **NMOS (Model N):**
  * `LEVEL` = $3$
  * `VTO` = $0,7000\,\text{V}$
  * `KP` = $120,0\,\mu\text{A/V}^2$ ($1,2 \times 10^{-4}\,\text{A/V}^2$)
  * `TOX` = $9,5 \times 10^{-9}\,\text{m}$ ($9,5\,\text{nm}$)
  * `GAMMA` = $0,4000\,\text{V}^{1/2}$
  * `VMAX` = $1,0 \times 10^5\,\text{m/s}$
  * `THETA` = $0,0500\,\text{V}^{-1}$
  * `KAPPA` = $0,1000$
- **PMOS (Model P):**
  * `LEVEL` = $3$
  * `VTO` = $-0,8000\,\text{V}$
  * `KP` = $40,0\,\mu\text{A/V}^2$ ($4,0 \times 10^{-5}\,\text{A/V}^2$)
  * `TOX` = $9,5 \times 10^{-9}\,\text{m}$
  * `GAMMA` = $0,5000\,\text{V}^{1/2}$
  * `VMAX` = $1,0 \times 10^5\,\text{m/s}$
  * `THETA` = $0,1000\,\text{V}^{-1}$
  * `KAPPA` = $0,2000$
- **Trả lời câu hỏi phụ:** Trong mô hình SPICE Level 3, **không có tham số `LAMBDA` trực tiếp** (tham số `LAMBDA` chỉ dùng trong Level 1 và Level 2). Hiện tượng điều chế chiều dài kênh dẫn và suy giảm rào thế do cực má (DIBL) được mô tả thông qua các tham số **`KAPPA`**, **`ETA`** và giới hạn vận tốc **`VMAX`**.

### P2. Tính toán giải tích tỉ số $(W_p/W_n)$ và điểm $V_M$
1. Tỉ số để $V_M = 2,50\,\text{V}$:
   $$\sqrt{r} = \frac{V_M - V_{thn}}{V_{DD} - V_M - |V_{thp}|} = \frac{2,50 - 0,70}{5,0 - 2,50 - 0,80} = \frac{1,80}{1,70} \approx 1,0588$$
   $$r = 1,0588^2 \approx 1,1211 \implies \left[\frac{(W/L)_p}{(W/L)_n}\right]_{\text{target}} = 1,1211 \times \frac{K_n'}{K_p'} = 1,1211 \times 3,00 = \mathbf{3,363}$$
2. Khi chọn $W_n = 4\lambda_{DR} = 1,2\,\mu\text{m}$ và $W_p = 12\lambda_{DR} = 3,6\,\mu\text{m}$ ($W_p/W_n = 3,0$):
   $$r = \frac{40 \times (3,6/0,6)}{120 \times (1,2/0,6)} = \frac{240}{240} = \mathbf{1,0000}$$
   $$V_M = \frac{0,70 + 1,0 \times (5,0 - 0,80)}{1 + 1,0} = \frac{4,90}{2} = \mathbf{2,450\,\text{V}}$$
   Độ lệch so với $2,50\,\text{V}$ là: $|2,45 - 2,50| = \mathbf{0,050\,\text{V}} = 50\,\text{mV}$ (sai lệch tương đối $2,0\%$).

### P3. Ước lượng điện trở dẫn $R_{on}$ và trễ $0,69 R C$
- $R_{on,n} = \frac{1}{(240 \times 10^{-6}) \times (5,0 - 0,70)} = \mathbf{969,0\,\Omega}$.
- $R_{on,p} = \frac{1}{(240 \times 10^{-6}) \times (5,0 - 0,80)} = \mathbf{992,1\,\Omega}$.
- Với $C_L = 50\,\text{fF}$:
  * $t_{pHL} \approx 0,69315 \times 969,0\,\Omega \times 50\,\text{fF} = \mathbf{33,58\,\text{ps}}$.
  * $t_{pLH} \approx 0,69315 \times 992,1\,\Omega \times 50\,\text{fF} = \mathbf{34,37\,\text{ps}}$.
  * $t_{pd} \approx \frac{33,58 + 34,37}{2} = \mathbf{33,98\,\text{ps}} \approx 34\,\text{ps}$.
- **Dự đoán:** Trễ đo thực tế trong LTspice sẽ **lớn hơn** giá trị này khoảng 1,5 đến 1,8 lần vì quá trình nạp xả thực tế bắt đầu từ vùng bão hòa với điện trở tức thời cao hơn vùng triode sâu.

### P4. Bản vẽ sơ đồ que Stick Diagram
- Đường đi Euler: $[In]$ (đơn biến).
- Đủ 2 thanh nguồn $V_{DD}, GND$ bằng Metal 1.
- Dải Poly chạy liên tục từ PMOS xuống NMOS làm cực cổng.
- Dây ra `out` bằng Metal 1 dẫn sang phía bên phải.
- Tiếp xúc $N^+$-tap nối N-Well lên $V_{DD}$, $P^+$-tap nối P-Substrate xuống $GND$.

### P5. Khung Netlist hoàn chỉnh
```spice
* Netlist CMOS Inverter - MOSIS C5N 0.5um
.include C5_models.txt
.param Vdd=5.0
.param CL_val=50f

Vdd vdd 0 DC {Vdd}
Vin in  0 PULSE(0 {Vdd} 0 100p 100p 9.9n 20n)

MP out in vdd vdd P L=0.6u W=3.6u
MN out in 0   0   N L=0.6u W=1.2u

CL out 0 {CL_val}

.tran 0 50n 0 1p
.meas TRAN tpHL TRIG V(in)={0.5*Vdd} RISE=1 TARG V(out)={0.5*Vdd} FALL=1
.meas TRAN tpLH TRIG V(in)={0.5*Vdd} FALL=1 TARG V(out)={0.5*Vdd} RISE=1
.meas TRAN tpd  PARAM (tpHL + tpLH)/2
.meas TRAN trise TRIG V(out)={0.1*Vdd} RISE=1 TARG V(out)={0.9*Vdd} RISE=1
.meas TRAN tfall TRIG V(out)={0.9*Vdd} FALL=1 TARG V(out)={0.1*Vdd} FALL=1
.end
```

### P6. Dự đoán lề nhiễu logic
- Bằng mô hình giải tích bậc hai:
  * $V_{IL} = \frac{2 V_{out} - V_{DD} + |V_{thp}| + r V_{thn}}{1 + r} \approx \mathbf{2,01\,\text{V}}$
  * $V_{IH} = \frac{V_{DD} - |V_{thp}| + r (2 V_{out} + V_{thn})}{1 + r} \approx \mathbf{2,89\,\text{V}}$
  * $NM_L = V_{IL} - V_{OL} = 2,01 - 0 = \mathbf{2,01\,\text{V}}$
  * $NM_H = V_{OH} - V_{IH} = 5,0 - 2,89 = \mathbf{2,11\,\text{V}}$
- Dự đoán: $NM_H$ hơi lớn hơn $NM_L$ một lượng nhỏ do $|V_{thp}| > V_{thn}$.

### P7. Ước lượng điện dung ngõ vào $C_{in}$
- $C_{ox} = \frac{3,45 \times 10^{-11}\,\text{F/m}}{9,5 \times 10^{-9}\,\text{m}} \approx \mathbf{3,632\,\text{fF}/\mu\text{m}^2}$.
- Diện tích kênh dẫn:
  * NMOS: $1,2\,\mu\text{m} \times 0,6\,\mu\text{m} = 0,72\,\mu\text{m}^2$.
  * PMOS: $3,6\,\mu\text{m} \times 0,6\,\mu\text{m} = 2,16\,\mu\text{m}^2$.
  * Tổng diện tích kênh: $2,88\,\mu\text{m}^2$.
- Điện dung cổng nội tại: $C_{gate} = 3,632\,\text{fF}/\mu\text{m}^2 \times 2,88\,\mu\text{m}^2 \approx \mathbf{10,46\,\text{fF}}$.
- Cộng thêm điện dung chồng lấp cực má và cực nguồn ($CGSO, CGDO$): $C_{in} \approx \mathbf{12 - 14\,\text{fF}}$.

---

## C. HƯỚNG DẪN THỰC HÀNH VÀ BẢNG SỐ LIỆU ĐỐI CHUẨN BENCHMARK

### C1. Đo hệ số điều chế kênh $\lambda_{CLM}$ trong Ex1.1
- **Lưu ý kỹ thuật then chốt:** Ở $V_{GS} = 5,0\,\text{V}$, điện áp bão hòa cần thiết là $V_{DS} \ge V_{GS} - V_{thn} = 5,0 - 0,70 = 4,3\,\text{V}$. Do đó, điểm $V_{DS} = 3,0\,\text{V}$ trên nhánh $5\,\text{V}$ **vẫn còn nằm trong vùng tuyến tính (triode)**.
- **Giải pháp chuẩn:** Chọn đường cong $V_{GS} = 3,0\,\text{V}$ (tại đây $V_{DS,sat} = 3,0 - 0,70 = 2,3\,\text{V}$). Tại nhánh này, cả $V_{DS1} = 3,0\,\text{V}$ và $V_{DS2} = 5,0\,\text{V}$ đều đã nằm sâu trong vùng bão hòa.
- Dùng công thức chính xác:
  $$\lambda_{CLM} = \frac{I_2 - I_1}{I_1 V_{DS2} - I_2 V_{DS1}}$$
  (Với $I_1$ đo tại $3,0\,\text{V}$ và $I_2$ đo tại $5,0\,\text{V}$).

### C2. Bảng kết quả mô phỏng tham chiếu (SPICE Benchmark)

| Thông số kỹ thuật | [Suy dẫn] Bậc 2 | [Script số] Tích phân | [Benchmark SPICE] Pre-layout | [Benchmark SPICE] Post-layout (PEX) | [Đo] Thực tế phòng máy |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$V_{thn}$** | $0,70\,\text{V}$ | $0,70\,\text{V}$ | **$0,69 - 0,71\,\text{V}$** | $0,69 - 0,71\,\text{V}$ | |
| **$V_{thp}$** | $-0,80\,\text{V}$ | $-0,80\,\text{V}$ | **$-0,79 - -0,81\,\text{V}$** | $-0,79 - -0,81\,\text{V}$ | |
| **$\lambda_{CLM}$ ($V_{GS}=3\text{V}$)** | — | $0,050\,\text{V}^{-1}$ | **$0,045 - 0,055\,\text{V}^{-1}$** | $0,045 - 0,055\,\text{V}^{-1}$ | |
| **$I_{DS,max(n)}$ ($5\text{V}, 5\text{V}$)** | $2,22\,\text{mA}$ | $2,77\,\text{mA}$ | **$2,70 - 2,85\,\text{mA}$** | $2,70 - 2,85\,\text{mA}$ | |
| **$I_{DS,max(p)}$ ($5\text{V}, 5\text{V}$)** | $2,12\,\text{mA}$ | $2,65\,\text{mA}$ | **$2,58 - 2,72\,\text{mA}$** | $2,58 - 2,72\,\text{mA}$ | |
| **Điện áp $V_M$** | $2,450\,\text{V}$ | $2,450\,\text{V}$ | **$2,448 - 2,455\,\text{V}$** | $2,445 - 2,452\,\text{V}$ | |
| **$V_{IL}$ (slope = $-1$)** | $2,01\,\text{V}$ | $1,655\,\text{V}$ | **$1,65 - 1,82\,\text{V}$** | $1,65 - 1,81\,\text{V}$ | |
| **$V_{IH}$ (slope = $-1$)** | $2,89\,\text{V}$ | $2,825\,\text{V}$ | **$2,78 - 2,85\,\text{V}$** | $2,78 - 2,85\,\text{V}$ | |
| **Lề nhiễu $NM_L$** | $2,01\,\text{V}$ | $1,655\,\text{V}$ | **$\ge 1,65\,\text{V}$** | $\ge 1,65\,\text{V}$ | |
| **Lề nhiễu $NM_H$** | $2,11\,\text{V}$ | $2,175\,\text{V}$ | **$\ge 2,15\,\text{V}$** | $\ge 2,15\,\text{V}$ | |
| **$t_{pHL}$ ($C_L = 50\,\text{fF}$)** | $33,58\,\text{ps}$ ($0,69RC$) | $49,80\,\text{ps}$ | **$48 - 55\,\text{ps}$** | $70 - 78\,\text{ps}$ | |
| **$t_{pLH}$ ($C_L = 50\,\text{fF}$)** | $34,37\,\text{ps}$ ($0,69RC$) | $51,91\,\text{ps}$ | **$50 - 58\,\text{ps}$** | $73 - 82\,\text{ps}$ | |
| **$t_{pd}$ ($C_L = 50\,\text{fF}$)** | $33,98\,\text{ps}$ ($0,69RC$) | $50,86\,\text{ps}$ | **$49 - 56\,\text{ps}$** | $72 - 80\,\text{ps}$ | |
| **Độ tăng trễ PEX vs Pre** | — | $+47,0\%$ | — | **$+42 - 48\%$** | |

---

## D. ĐÁP ÁN CÂU HỎI POST-LAB

1. **Thiết kế không đối xứng $W_p = W_n = 4\lambda_{DR} = 1,2\,\mu\text{m}$:**
   - Hệ số dẫn nạp $r = \frac{40 \times (1,2/0,6)}{120 \times (1,2/0,6)} = \frac{1}{3} \approx 0,3333 \implies \sqrt{r} \approx 0,5774$.
   - Điểm chuyển mạch:
     $$V_M = \frac{0,70 + 0,5774 \times (5,0 - 0,80)}{1 + 0,5774} = \frac{0,70 + 2,425}{1,5774} \approx \mathbf{1,98\,\text{V}}$$
     Đặc tuyến VTC bị kéo lệch mạnh sang trái. Lề nhiễu mức thấp $NM_L$ sụt giảm từ $\sim 1,65\,\text{V}$ xuống chỉ còn $\sim 1,1\,\text{V}$, làm cổng rất nhạy với nhiễu đất.
   - Trễ sườn lên $t_{pLH}$ tăng gấp 3 lần ($R_{on,p} \approx 3 \times 992 \approx 3\,\text{k}\Omega \implies t_{pLH} \approx 150\,\text{ps}$), trong khi $t_{pHL}$ giữ nguyên $\approx 50\,\text{ps}$.
   - Thiết kế này chỉ dùng khi ưu tiên tiết kiệm tối đa diện tích hoặc trong mạch nạp trước (precharge) nơi ngõ ra chỉ cần xả nhanh.

2. **Cơ chế vật lý của tụ khuếch tán má $C_{db}$ và ảnh hưởng khi tải lớn:**
   - Vùng khuếch tán má tạo tiếp giáp $p-n$ phân cực ngược với đế/giếng, hình thành tụ tiếp giáp phẳng $C_{bottom} = CJ \cdot AD$ và tụ thành bên $C_{sidewall} = CJSW \cdot PD$.
   - Khi tải ngoài rất lớn ($C_L = 1\,\text{pF} = 1000\,\text{fF}$): Tụ ký sinh $C_{par} \approx 23,5\,\text{fF}$ chỉ chiếm $\approx 2,3\%$ tổng tải. Lúc này tải ngoài chiếm ưu thế hoàn toàn, nên độ tăng trễ phần trăm sau PEX trở nên không đáng kể.

3. **Cơ chế chống Latch-up của Guard Rings:**
   - Các tiếp xúc Tap rời rạc chỉ dập điện thế cục bộ tại một điểm. Dòng hạt dẫn thiểu số vẫn có thể khuếch tán ngang và kích hoạt BJT ký sinh ở xa.
   - Vòng bảo vệ Guard Ring khép kín tạo một bức tường chắn điện thế thấp, hấp thụ toàn bộ hạt dẫn thiểu số trôi dạt và ép điện trở $R_{well}, R_{sub} \to 0$ trên toàn bộ chu vi, ngăn không cho tiếp giáp E-B đạt ngưỡng phân cực thuận $0,7\,\text{V}$.

---

## E. BAREM CHẤM ĐIỂM CHI TIẾT (THANG 10)

| STT | Hạng mục đánh giá | Điểm tối đa | Tiêu chí chấm chi tiết |
| :---: | :--- | :---: | :--- |
| **1** | **Chuẩn bị Pre-lab (Mục 4)** | **2,0 điểm** | - Trích xuất đúng tham số P1: 0,5 đ.<br>- Tính đúng $W_p/W_n$ và $V_M = 2,45\,\text{V}$ tại P2: 0,5 đ.<br>- Tính đúng $R_{on}$, trễ P3 và có dự đoán đúng: 0,5 đ.<br>- Vẽ Stick diagram P4 có Taps; netlist P5 đúng; làm P6, P7: 0,5 đ. |
| **2** | **Đo đạc I-V & Phân tích VTC (Ex1.1, Ex1.2)** | **2,5 điểm** | - Chạy đúng họ đặc tuyến ra và truyền dẫn: 1,0 đ.<br>- Trích xuất đúng $V_{th}$ và $\lambda_{CLM}$ trên nhánh $3\text{V}$: 0,5 đ.<br>- Dựng Schematic Inverter và chạy mô phỏng VTC ra dạng sóng chuẩn: 0,5 đ.<br>- Đo chính xác điểm $V_M \approx 2,45\,\text{V}$ và vẽ đạo hàm xác định $NM_L, NM_H$: 0,5 đ. |
| **3** | **Mô phỏng Transient & Lệnh `.meas` (Ex1.3)** | **2,0 điểm** | - Cấu hình nguồn PULSE và tải $50\,\text{fF}$ chính xác: 0,5 đ.<br>- Soạn đúng khối lệnh `.meas` và trích xuất kết quả không báo lỗi FAIL: 1,0 đ.<br>- Lập bảng số liệu theo 3 mức tải dung ($10\text{f}, 50\text{f}, 100\text{f}$): 0,5 đ. |
| **4** | **Mask Layout, DRC & LVS (Ex1.4)** | **2,5 điểm** | - Vẽ Layout đúng chuẩn SCMOS Submicron ($H_{cell} = 40\lambda$, ray $6\lambda$): 1,0 đ.<br>- Có đầy đủ tiếp xúc Well Tap và Substrate Tap: 0,5 đ.<br>- Kiểm tra DRC đạt **"0 errors found"**: 0,5 đ.<br>- Đối chiếu NCC (LVS) báo **"Cells are topologically equivalent (MATCH)"**: 0,5 đ. |
| **5** | **Trích xuất PEX & Post-lab (Ex1.5, Mục 7)** | **1,0 điểm** | - Trích xuất netlist PEX và chạy mô phỏng đo độ tăng trễ: 0,5 đ.<br>- Trả lời đúng, lập luận chặt chẽ 3 câu hỏi Post-lab: 0,5 đ. |
| **TỔNG**| **TOÀN BÀI LAB 1** | **10,0 điểm** | **Đạt yêu cầu khi tổng điểm $\ge 5,0$ và LVS đạt MATCH.** |\n