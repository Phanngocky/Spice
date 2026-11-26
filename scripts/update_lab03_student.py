#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to update '02 - Student Workbook/lab-03-cong-phuc-hop-aoi-oai-logical-effort.md'
Standard 11-section template, rigorous physics, no answer leaks (OAI21 in Pre-lab), LF line endings.
"""

content = """# THỰC HÀNH THIẾT KẾ VLSI — BÀI 3
# CỔNG PHỨC HỢP (AOI/OAI) VÀ TỐI ƯU TRỄ THEO PHƯƠNG PHÁP LOGICAL EFFORT

---
**Bộ môn:** Điện tử - Viễn thông | **Khoa:** Điện - Điện tử  
**Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Thời lượng:** 135 phút (3 tiết tiêu chuẩn trên phòng máy) + Tự học Pre-lab & Hoàn thiện Post-lab  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07+), LTspice XVII / LTspice 2025  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5µm ($\lambda_{DR} = 0,30\,\mu\\text{m}$, 3 Metal layers, $V_{DD} = 5,0\,\\text{V}$)  
**Thư mục làm việc chuẩn:** `D:\\lab_vlsi\\lab03_MSSV_HoTen\\`  
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Phân tích nguyên lý Cổng phức hợp CMOS (Complex Logic Gates):** Hiểu rõ cách hiện thực hàm logic dạng AND-OR-INVERT (`AOI`) và OR-AND-INVERT (`OAI`) chỉ trong **một tầng logic duy nhất (Single-stage Gate)**; lượng hóa ưu thế giảm số transistor (từ 10 xuống 6, giảm $40\\%$) và giảm tổng bề rộng kênh (giảm $\\approx 18\\%$) so với phương án ghép các cổng rời (NAND2, Inverter, NOR2) (CLO1).
2. **Thành thạo phương pháp định kích thước theo trường hợp xấu nhất (Worst-Case Sizing):** Định cỡ bề rộng kênh $(W/L)$ cho mạng kéo lên (PUN) và kéo xuống (PDN) không đối xứng, bảo đảm điện trở kéo tương đương bằng Inverter chuẩn `INV_X1` ($R_{eq,N} \\approx 969\,\\Omega, R_{eq,P} \\approx 992\,\\Omega$) (CLO1).
3. **Làm chủ Lý thuyết Nỗ lực Logic (Logical Effort Theory):** 
   - Xác định chính xác nỗ lực logic $g$ (Logical Effort) và trễ ký sinh $p$ (Parasitic Delay) cho từng ngõ vào của cổng phức hợp.
   - Nắm vững phương pháp thực nghiệm đo đạc đường trễ $t_{pd}$ theo nỗ lực điện $h$ bằng testbench kép đối chuẩn trực tiếp với `INV_X1` để trích xuất $g_{meas}$ và $p_{meas}$ (CLO2).
4. **Giải bài toán Tối ưu hóa Chuỗi đệm (Inverter Buffer Chain Optimization):** Tính toán số tầng đệm tối ưu $N$, hệ số phóng đại từng tầng $\\hat{f}$, và thiết kế chuỗi Inverter nhiều tầng để lái tải dung lớn ($C_L = 1\,\text{pF}$) đạt mức giảm trễ $\\approx 72,5\\%$ (nhanh hơn $3,63$ lần) so với lái trực tiếp (CLO1, CLO2).
5. **Thiết kế Mask Layout cho Cổng phức hợp:** Áp dụng phương pháp đường đi Euler để tìm thứ tự cổng Polysilicon tối ưu $C - A - B$, thực hiện kỹ thuật chia sẻ cực má chung nối ra `out` (Abutment), kiểm tra DRC đạt 0 lỗi và đối chiếu sơ đồ LVS (NCC) đạt kết quả trùng khớp hoàn hảo (CLO4).
6. **Đóng gói IP Tế bào chuẩn:** Tạo Cell Icon `aoi21_x1{ic}` và tế bào chuỗi đệm `buf_chain_3st{ic}` bàn giao làm linh kiện thành phần cho các bài thực hành tiếp theo (CLO4).

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

### 2.1 Kế thừa từ Bài 1 và Bài 2
- **Thư viện mô hình SPICE:** Tệp mô hình MOSIS C5N Level 3 [C5_models.txt](file:///d:/tam/VLSI_Spice/04%20-%20Models_and_Libraries/C5_models.txt) ($V_{DD} = 5,0\,\\text{V}, V_{tn0} = 0,70\,\\text{V}, |V_{tp0}| = 0,80\,\\text{V}, K'_n = 120\,\\mu\\text{A/V}^2, K'_p = 40\,\\mu\\text{A/V}^2, \\text{TOX} = 9,5\,\\text{nm}$).
- **Tế bào chuẩn Inverter cơ sở (`INV_X1`):** $W_n = 4\\lambda_{DR} = 1,20\,\\mu\\text{m}, W_p = 12\\lambda_{DR} = 3,60\,\\mu\\text{m}, L = 2\\lambda_{DR} = 0,60\,\\mu\\text{m}$, $R_{on,n0} \\approx 969\,\\Omega, R_{on,p0} \\approx 992\,\\Omega, C_{in,inv} \\approx 10 - 13\,\\text{fF}$.
- **Quy chuẩn ô mở rộng:** Với tế bào có transistor $W_p = 24\\lambda_{DR}$ chưa gập ngón (unfolded), chiều cao ô chuẩn mở rộng là $H_{cell} = 60\\lambda_{DR} = 18,0\,\\mu\\text{m}$; hai ray nguồn kim loại Metal 1 có độ rộng $\\ge 6\\lambda_{DR} = 1,80\,\\mu\\text{m}$.
- **Kỹ năng thiết kế & Kiểm chứng:** Thao tác vẽ Schematic, đóng gói Icon, tạo Layout, kiểm tra DRC, NCC LVS và trích xuất PEX trong Electric VLSI kết hợp mô phỏng LTspice.

### 2.2 Sản phẩm bàn giao sau buổi thực hành
1. **Thư viện Electric:** `D:\\lab_vlsi\\lab03_MSSV_HoTen\\lab03_MSSV.jelib` chứa đủ các cell:
   - `aoi21_x1{sch}`: Sơ đồ nguyên lý cổng AOI21 3 ngõ vào.
   - `aoi21_x1{ic}`: Icon ký hiệu cổng AOI21 chuẩn.
   - `aoi21_x1{lay}`: Mặt nạ Layout cổng AOI21 đạt 0 lỗi DRC và LVS MATCH.
   - `buf_chain_3st{sch}`: Sơ đồ nguyên lý chuỗi đệm 3 tầng tối ưu lái tải $1\,\\text{pF}$.
   - `buf_chain_3st{ic}`: Icon chuỗi đệm 3 tầng.
2. **Tập tin Netlist mô phỏng SPICE:**
   - `aoi21_func.sp`: Mô phỏng kiểm chứng bảng chân trị 8 trạng thái.
   - `logical_effort_meas.sp`: Mô phỏng testbench kép đo $g$ và $p$ của AOI21 đối chuẩn với `INV_X1`.
   - `buffer_chain_opt.sp`: Mô phỏng đối sánh chuỗi đệm tối ưu vs lái trực tiếp tải $1\,\\text{pF}$.
   - `aoi21_pex.sp`: Mô phỏng sau trích xuất ký sinh PEX.
3. **Báo cáo thực hành cá nhân:** Điền đầy đủ các bảng số liệu đo, đồ thị hồi quy tuyến tính và câu hỏi thảo luận chuyên sâu.

---

## 3. CƠ SỞ LÝ THUYẾT NGẮN GỌN

### 3.1 Cấu trúc Cổng Phức Hợp AOI21 ($Y = \\overline{(A \\cdot B) + C}$)

Trong thiết kế vi mạch CMOS tĩnh, việc hiện thực một hàm logic phức tạp bằng cách ghép các cổng đơn lẻ (ví dụ dùng 1 cổng AND2 và 1 cổng NOR2 để tạo $Y = \\overline{(A \\cdot B) + C}$) đòi hỏi:
- Cổng AND2 cần: 4 transistor (NAND2) + 2 transistor (Inverter) = 6 transistor.
- Cổng NOR2 cần: 4 transistor.
- $\\implies$ **Phương án ghép cổng rời:** Cần **10 transistor**, tín hiệu phải truyền qua **2 tầng trễ logic**. Tổng chiều rộng kênh: $\\sum W = 40\\lambda \\text{ (NAND2)} + 16\\lambda \\text{ (INV)} + 56\\lambda \\text{ (NOR2)} = \\mathbf{112\\lambda_{DR} = 33,6\,\\mu\\text{m}}$.

Thay vào đó, cấu trúc **Cổng phức hợp AOI21 (And-Or-Invert 2-1)** tích hợp toàn bộ hàm logic vào duy nhất một tế bào chuyển mạch:
- **Mạng kéo xuống (PDN):** Thực hiện hàm logic không đảo $F = (A \\cdot B) + C$. Nhánh $A \\cdot B$ gồm 2 NMOS mắc nối tiếp ($M_{NA}, M_{NB}$); nhánh này mắc song song với 1 NMOS đơn ($M_{NC}$) đại diện cho biến $C$.
- **Mạng kéo lên (PUN):** Thực hiện hàm bù bằng định lý De Morgan:
  $$Y = \\overline{(A \\cdot B) + C} = \\overline{(A \\cdot B)} \\cdot \\bar{C} = (\\bar{A} + \\bar{B}) \\cdot \\bar{C}$$
  Mạng gồm 2 PMOS mắc song song ($M_{PA} \\parallel M_{PB}$), sau đó nối tiếp với 1 PMOS đại diện cho biến $C$ ($M_{PC}$).
- $\\implies$ **Tổng số transistor chỉ còn: 6 transistor (3 PMOS + 3 NMOS)**. Tín hiệu chỉ đi qua **1 tầng chuyển mạch duy nhất**, giúp:
  * Giảm $40\\%$ số lượng transistor (từ 10 xuống 6).
  * Giảm $\\approx 18\\%$ tổng bề rộng kênh silicon (từ $112\\lambda$ xuống $92\\lambda$).
  * Triệt tiêu hoàn toàn nút ký sinh liên tầng trung gian giữa các cổng rời.

```
                       VDD (5.0V)
                           │
                     ┌─────┴─────┐
                     │           │
                 ┌───┴───┐   ┌───┴───┐
                 │  MPA  │   │  MPB  │ (Mỗi cái 24λ)
                 └───┬───┘   └───┬───┘
                     └─────┬─────┘
                           │ (Nút nội Xp)
                       ┌───┴───┐
                   C ──┤  MPC  │ (24λ)
                       └───┬───┘
                           ├───────────────────── Out (Y)
                           │
                     ┌─────┴─────┐
                     │           │
                 ┌───┴───┐       │
             A ──┤  MNA  │ (8λ)  │
                 └───┬───┘   ┌───┴───┐
                     │ (Xn)  │  MNC  │ (4λ)
                 ┌───┴───┐   └───┬───┘
             B ──┤  MNB  │ (8λ)  │
                 └───┬───┘       │
                     └─────┬─────┘
                           │
                          GND
```

*Sơ đồ nguyên lý tế bào AOI21_X1 và Chuỗi đệm Inverter tối ưu:*
- [aoi21_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/aoi21_schematic.png)
- [buffer_chain_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/buffer_chain_schematic.png)

---

### 3.2 Định Kích thước Transistor theo Điện trở Dẫn $R_{on}$ Trường hợp Xấu nhất

Để cổng `AOI21_X1` có khả năng kéo dòng nạp/xả cân bằng với Inverter chuẩn `INV_X1` ($R_{on,n0} \\approx 969\,\\Omega, R_{on,p0} \\approx 992\,\\Omega$):

#### a. Mạng kéo xuống (PDN)
- **Nhánh $A \\cdot B$ (2 NMOS nối tiếp):** Khi cả $A=1, B=1$, dòng xả đi qua 2 NMOS nối tiếp. Để tổng điện trở bằng $R_{on,n0}$:
  $$R_{eq} = R_{on,NA} + R_{on,NB} = R_{on,n0} \\implies W_{n,A} = W_{n,B} = 2 \\times W_{n,inv} = 2 \\times 4\\lambda_{DR} = \\mathbf{8\\lambda_{DR} = 2,40\,\\mu\\text{m}}$$
- **Nhánh $C$ (1 NMOS đơn):** Khi chỉ có $C=1$, dòng xả đi qua 1 NMOS độc lập. Để điện trở bằng $R_{on,n0}$:
  $$W_{n,C} = W_{n,inv} = \\mathbf{4\\lambda_{DR} = 1,20\,\\mu\\text{m}}$$

#### b. Mạng kéo lên (PUN)
- Mạng gồm cụm $(M_{PA} \\parallel M_{PB})$ mắc nối tiếp với $M_{PC}$.
- **Trường hợp xấu nhất (Worst-Case):** Xảy ra khi chỉ có **1 PMOS trong cụm song song dẫn** kết hợp với $M_{PC}$ (ví dụ $A=0, B=1, C=0$ hoặc $A=1, B=0, C=0$). Khi đó đường dẫn từ $V_{DD}$ xuống $Out$ đi qua đúng 2 PMOS mắc nối tiếp.
- Do đó để điện trở tương đương tổng bằng $R_{on,p0}$:
  $$R_{eq} = R_{on,P(A/B)} + R_{on,PC} = R_{on,p0} \\implies W_{p,A} = W_{p,B} = W_{p,C} = 2 \\times W_{p,inv} = 2 \\times 12\\lambda_{DR} = \\mathbf{24\\lambda_{DR} = 7,20\,\\mu\\text{m}}$$

---

### 3.3 Phương pháp Logical Effort (Sutherland, Sproull, Harris)

Mô hình trễ tuyến tính chuẩn hóa:
$$d = \\frac{t_{pd}}{\\tau} = f + p = g \\cdot h + p$$

Trong đó:
- $\\tau$: **Hằng số trễ cơ bản**, được định nghĩa là hệ số góc của đường trễ Inverter chuẩn `INV_X1` theo nỗ lực điện $h$ ($t_{pd,inv} = \\tau(h + p_{inv})$).
- $p$: **Trễ ký sinh (Parasitic Delay)** do điện dung cực má tại nút ngõ ra khi không mang tải ngoài ($h=0$).
- $h = \\frac{C_{out}}{C_{in,\\text{pin}}}$: **Nỗ lực điện (Electrical Effort)**, tỉ số giữa tải dung ngoài và điện dung ngõ vào của chính chân đang xét.
- $g$: **Nỗ lực logic (Logical Effort)**, biểu thị mức độ kém hiệu quả của cổng logic so với Inverter chuẩn trong việc cấp dòng khi có cùng điện dung ngõ vào:
  $$g = \\frac{C_{in,\\text{pin}}}{C_{in,inv}}$$

#### a. Tính toán Logical Effort cho cổng AOI21:
Với Inverter chuẩn `INV_X1`:
$$C_{in,inv} \\propto W_n + W_p = 4\\lambda_{DR} + 12\\lambda_{DR} = 16\\lambda_{DR}$$

Với cổng `AOI21_X1`:
- **Ngõ vào $A$:** Nối vào $M_{NA}$ ($8\\lambda$) và $M_{PA}$ ($24\\lambda$):
  $$C_{in,A} \\propto 8\\lambda + 24\\lambda = 32\\lambda_{DR} \\implies g_A = \\frac{32\\lambda}{16\\lambda} = \\mathbf{2,000}$$
- **Ngõ vào $B$:** Nối vào $M_{NB}$ ($8\\lambda$) và $M_{PB}$ ($24\\lambda$):
  $$C_{in,B} \\propto 8\\lambda + 24\\lambda = 32\\lambda_{DR} \\implies g_B = \\frac{32\\lambda}{16\\lambda} = \\mathbf{2,000}$$
- **Ngõ vào $C$:** Nối vào $M_{NC}$ ($4\\lambda$) và $M_{PC}$ ($24\\lambda$):
  $$C_{in,C} \\propto 4\\lambda + 24\\lambda = 28\\lambda_{DR} \\implies g_C = \\frac{28\\lambda}{16\\lambda} = \\mathbf{1,750}$$

#### b. Trễ ký sinh $p$ của AOI21:
Điện dung cực má tại nút ngõ ra $Out$ gồm: Drain của $M_{PC}$ ($24\\lambda$), Drain của $M_{NA}$ ($8\\lambda$), và Drain của $M_{NC}$ ($4\\lambda$):
$$C_{out,parasitic} \\propto 24\\lambda + 8\\lambda + 4\\lambda = 36\\lambda_{DR}$$
So với Inverter chuẩn có $C_{out,inv} \\propto 12\\lambda + 4\\lambda = 16\\lambda_{DR}$:
$$p_{AOI21} = \\frac{36\\lambda}{16\\lambda} = \\mathbf{2,250} \\quad (p_{AOI21} \\approx 2,25 \\cdot p_{inv})$$

> [!TIP]
> **Ưu thế của ngõ vào C:** Ngõ vào $C$ có nỗ lực logic $g_C = 1,75$ nhỏ hơn $12,5\\%$ so với ngõ $A, B$ ($g=2,0$). Đồng thời nhánh kéo xuống qua $M_{NC}$ đi thẳng xuống đất mà không qua nút nội trung gian. Do đó trong thiết kế vi mạch, tín hiệu đến muộn nhất trên đường tới hạn (Critical Path) thường được ưu tiên gán vào ngõ vào $C$.

---

### 3.4 Phương pháp Thực nghiệm Đo $g$ và $p$ Chuẩn xác

Để tránh sai số do định nghĩa $h$ theo Inverter làm hệ số góc bị triệt tiêu về $1$, phương pháp đo chuẩn tắc gồm các bước:
1. **Dựng Testbench kép:** Đặt song song cổng Inverter chuẩn `INV_X1` và cổng `AOI21_X1` trong cùng một file mô phỏng SPICE.
2. **Khảo sát Inverter chuẩn:** Quét tải dung $C_L \\in \\{10, 20, 30, 40\\}\\,\\text{fF}$. Đường trễ đo được là:
   $$t_{pd,inv}(C_L) = \\text{Slope}_{inv} \\cdot C_L + t_{pd0,inv}$$
   Từ đó xác định hằng số trễ $\\tau = \\text{Slope}_{inv} \\cdot C_{in,inv}$.
3. **Khảo sát cổng AOI21:** 
   - Với ngõ vào A: Đặt tải $C_L$ tương ứng với các tỉ số nỗ lực điện $h = C_L / C_{in,A}$ (với $C_{in,A} = 2 \\times C_{in,inv}$).
   - Đo đường trễ $t_{pd,A}(h) = \\text{Slope}_{h,A} \\cdot h + t_{pd0,A}$.
4. **Trích xuất thông số thực nghiệm:**
   $$g_{meas,A} = \\frac{\\text{Slope}_{h,A}}{\\text{Slope}_{h,inv}} \\qquad p_{meas,A} = \\frac{t_{pd0,A}}{t_{pd0,inv}} \\times p_{inv}$$

---

### 3.5 Tối ưu Hóa Chuỗi Đệm Inverter (Inverter Buffer Chain)

Khi một cổng logic cần lái tải dung cực lớn (ví dụ đường bus dài trên chip, chân I/O Pad $C_L = 1\,\text{pF}$):
- Nếu lái trực tiếp bằng Inverter cơ sở $1\\times$ ($C_{in} \\approx 20\,\\text{fF}$): Tỉ số nỗ lực điện $H = C_L / C_{in} = 50$. Trễ danh định: $D = 1 \\times 50 + 1 = 51\,\\tau$.
- **Chèn chuỗi $N$ tầng Inverter:**
  * Nỗ lực tối ưu mỗi tầng: $\\hat{f} = H^{1/N} = 50^{1/N}$.
  * Tổng thời gian trễ: $D = N(\\hat{f} + p_{inv})\\tau = N(50^{1/N} + 1)\\tau$.

| Số tầng $N$ | Nỗ lực mỗi tầng $\\hat{f} = 50^{1/N}$ | Trễ chuẩn hóa $D / \\tau$ | Đánh giá so sánh | Kích thước các tầng ($W_n / W_p$) |
| :---: | :---: | :---: | :--- | :--- |
| **$N = 1$** | $50,00$ | $51,00\\,\\tau$ | Lái trực tiếp | Tầng 1 ($1,0\\times$): $4\\lambda / 12\\lambda$ ($1,2\\,\\mu\\text{m} / 3,6\\,\\mu\\text{m}$) |
| **$N = 2$** | $7,07$ | $16,14\\,\\tau$ | Chậm hơn $+14,8\\%$ | Tầng 2 ($7,1\\times$): $28\\lambda / 85\\lambda$ |
| **$N = 3$** | **$3,68$** | **$14,05\\,\\tau$** | **Tối ưu cực tiểu ($100\\%$)** | Tầng 1: $1\\times$; Tầng 2: $3,68\\times$ ($15\\lambda / 44\\lambda$); Tầng 3: $13,57\\times$ ($54\\lambda / 163\\lambda$) |
| **$N = 4$** | $2,66$ | $14,64\\,\\tau$ | Chậm hơn $+4,2\\%$ | Tầng 1: $1\\times$; Tầng 2: $2,66\\times$; Tầng 3: $7,07\\times$; Tầng 4: $18,8\\times$ |
| **$N = 5$** | $2,19$ | $15,93\\,\\tau$ | Chậm hơn $+13,4\\%$ | Quá nhiều tầng, tốn diện tích và công suất |

$\\implies$ **Kết luận:** Chuỗi đệm 3 tầng ($N=3$) giúp giảm thời gian trễ từ $51,0\\,\\tau$ xuống còn $14,05\\,\\tau$, tức **giảm trễ $\\approx 72,5\\%$ (tốc độ nhanh hơn $3,63$ lần)**!

---

### 3.6 Phương pháp Đường đi Euler và Bố trí Mask Layout

Để tối ưu diện tích và giảm tụ cực má, ta tìm đường đi Euler chung cho cả hai mạng:
- **Thứ tự dải Polysilicon tối ưu: $C - A - B$**.
- **Mạng PDN (N-Active):**
  $$[\\text{GND}] \\xrightarrow{\\text{Gate C}} [\\mathbf{Out}] \\xrightarrow{\\text{Gate A}} [X_n] \\xrightarrow{\\text{Gate B}} [\\text{GND}]$$
  Cực má của $M_{NC}$ và $M_{NA}$ nối liền nhau và chia sẻ chung **một tiếp xúc Contact `out` duy nhất**!
- **Mạng PUN (P-Active):**
  $$[\\mathbf{Out}] \\xrightarrow{\\text{Gate C}} [X_p] \\xrightarrow{\\text{Gate A}} [\\mathbf{VDD}] \\xrightarrow{\\text{Gate B}} [X_p]$$
  Cực nguồn của $M_{PA}$ và $M_{PB}$ nối liền nhau và chia sẻ chung **một tiếp xúc Contact `vdd` ở giữa**!

```
                  SƠ ĐỒ QUE (STICK DIAGRAM) TỐI ƯU CỔNG AOI21 (THỨ TỰ C - A - B)
     VDD ───────────────────────────────────────────────────────────── (Metal 1)
                                           │ (Contact VDD chung)
             ┌─────────────────────────────┴────────────────────┐
             │ (Out)      (Xp)             (VDD)           (Xp) │  P-Diffusion (24λ)
             └────┬─────────┬────────────────┬───────────────┬──┘
                  │         │                │               │
     In_C ────────┼─────────┼                │               │  (Poly C)
                  │         │                │               │
     In_A ────────┼─────────┼────────────────┼               │  (Poly A)
                  │         │                │               │
     In_B ────────┼─────────┼────────────────┼───────────────┼  (Poly B)
                  │         │                │               │
             ┌────┴─────────┴────────────────┴───────────────┴──┐
             │  (GND)     (Drain: Out chung)(Xn: Abutted)  (GND)│  N-Diffusion
             └────┬─────────┬────────────────────────────────┬──┘
                  │         │ (Contact Out)                  │
                 GND       Out (Metal 1)                    GND
```

> [!WARNING]
> **Quy tắc khoảng cách hình học DRC:**  
> Tại vị trí có Contact ngõ ra `out` nằm giữa Poly C và Poly A, khoảng cách giữa 2 dải Poly bắt buộc phải $\\ge 6\\lambda_{DR} = 1,80\,\\mu\\text{m}$ (Rule 3.2.b).

---

## 4. CÂU HỎI CHUẨN BỊ TRƯỚC KHI ĐẾN LỚP (PRE-LAB)

> [!IMPORTANT]
> Toàn bộ nội dung chuẩn bị Pre-lab phải được sinh viên tính toán chi tiết vào vở hoặc Phiếu báo cáo trước khi bước vào phòng máy. Cán bộ hướng dẫn sẽ kiểm tra và ký xác nhận ở 10 phút đầu giờ.

### Câu hỏi 1: Bảng Chân Trị và Định Cỡ Cổng Đối Ngẫu OAI21 ($Y = \\overline{(A + B) \\cdot C}$)
1. Lập bảng chân trị đầy đủ gồm 8 trạng thái ngõ vào ($A, B, C \\in \\{0, 1\\}^3$), xác định giá trị logic ngõ ra $Y$ của cổng OAI21.
2. Vẽ sơ đồ nguyên lý của cổng OAI21 (chỉ rõ cấu trúc mạng PDN và PUN).
3. Định kích thước hình học $(W/L)$ theo $\\lambda_{DR}$ và $\\mu\\text{m}$ cho cả 6 transistor của tế bào `OAI21_X1` để có điện trở kéo xấu nhất tương đương Inverter chuẩn `INV_X1`.

### Câu hỏi 2: Tính toán Logical Effort Cổng OAI21
1. Dựa trên kích thước đã định cỡ ở Câu 1, hãy tính nỗ lực logic $g_A, g_B, g_C$ cho 3 chân ngõ vào của cổng OAI21.
2. Tính trễ ký sinh $p$ của cổng OAI21 tại nút ngõ ra.
3. So sánh $g_C$ của OAI21 với $g_C$ của AOI21 ($1,75$) và giải thích nguyên nhân vật lý vì sao có sự khác biệt này. Ngõ vào nào của OAI21 nên nhận tín hiệu đến muộn nhất trên đường tới hạn?

### Câu hỏi 3: Bài toán Tối ưu Hóa Chuỗi Đệm Inverter ($F = 64$)
Một đường truyền tín hiệu có tổng nỗ lực đường truyền $F = 64$. Nếu chỉ sử dụng các cổng Inverter ($p_{inv} = 1$):
1. Lập bảng tính tổng trễ chuẩn hóa $D/\\tau = N(F^{1/N} + 1)$ cho các trường hợp số tầng $N \\in \\{1, 2, 3, 4\\}$.
2. Xác định số tầng tối ưu $N^*$ và hệ số nỗ lực mỗi tầng $\\hat{f}$.
3. So sánh tổng trễ giữa $N = 3$ và $N = 4$ để kiểm chứng tính chất "đáy phẳng" của hàm tối ưu chuỗi đệm.

### Câu hỏi 4: Đồ thị Euler và Sơ đồ que Stick Diagram Cổng AOI21
1. Vẽ đồ thị mạch cho mạng PUN và PDN của cổng AOI21.
2. Chứng minh rằng thứ tự cổng $C - A - B$ cho phép chia sẻ cực má chung nối ra `out` trên dải N-Active, trong khi thứ tự $A - B - C$ sẽ làm cực `out` bị chia tách ra hai đầu dải khuếch tán.
3. Vẽ phác thảo sơ đồ que Stick Diagram của cổng `AOI21_X1` theo thứ tự $C - A - B$ lên giấy kẻ ô ly.

---

## 5. KẾ HOẠCH PHÂN BỔ THỜI LƯỢNG IN-LAB (135 PHÚT)

| Mốc thời gian | Thời lượng | Nội dung thực hiện chính | Sản phẩm nghiệm thu tại chỗ |
| :---: | :---: | :--- | :--- |
| **00 – 10'** | 10 phút | Kiểm tra Pre-lab tại bàn máy, thống nhất quy định an toàn và thư mục làm việc. | Chữ ký xác nhận Pre-lab vào Phiếu báo cáo. |
| **10 – 35'** | 25 phút | **Ex3.1:** Dựng Schematic `aoi21_x1{sch}`, gán 6 Export, chạy mô phỏng kiểm chứng 8 trạng thái bảng chân trị logic. | Dạng sóng 8 trạng thái logic đúng $100\\%$. |
| **35 – 70'** | 35 phút | **Ex3.2:** Dựng Testbench kép đo Logical Effort $g$ và $p$ của AOI21 đối chuẩn trực tiếp với `INV_X1`. | Trích xuất đồ thị hồi quy, tính $g_{meas}$ và $p_{meas}$. |
| **70 – 95'** | 25 phút | **Ex3.3:** Thiết kế chuỗi đệm Inverter 3 tầng `buf_chain_3st{sch}`, mô phỏng lái tải nặng $C_L = 1\\,\\text{pF}$ vs lái trực tiếp. | Đo được trễ giảm $> 3$ lần, sườn xung phục hồi. |
| **95 – 125'** | 30 phút | **Ex3.4:** Thiết kế Mask Layout `aoi21_x1{lay}` (thứ tự $C-A-B$), chạy DRC đạt 0 lỗi, chạy NCC LVS đạt MATCH. | Cửa sổ NCC thông báo so khớp hoàn hảo. |
| **125 – 135'** | 10 phút | Nghiệm thu tại bàn, đóng gói thư viện `lab03_MSSV.jelib`, dọn dẹp vệ sinh phòng máy. | Chữ ký nghiệm thu In-lab của Giảng viên. |

---

## 6. NỘI DUNG THỰC HÀNH TẠI LỚP (IN-LAB)

### 6.1 Bài tập Ex3.1: Thiết kế Schematic Cổng AOI21 và Kiểm chứng Bảng Chân Trị

![Sơ đồ nguyên lý aoi21_x1](images/aoi21_schematic.png)

1. **Khởi tạo Cell Schematic:**
   - Trong Electric VLSI, mở thư viện `lab03_MSSV.jelib`.
   - Chọn menu `Cell -> New Cell...` (`Ctrl + N`), đặt tên `aoi21_x1`, chọn kiểu `schematic`.
2. **Bố trí linh kiện và gán kích thước chuẩn:**
   - **Mạng kéo lên (PUN):**
     * Đặt 3 PMOS: $W = 24\\lambda_{DR} = 7,20\,\\mu\\text{m}, L = 2\\lambda_{DR} = 0,60\,\\mu\\text{m}$.
     * $M_{PA}, M_{PB}$ mắc song song: Source nối lên `vdd`, Drain nối chập tại nút nội $X_p$.
     * $M_{PC}$: Source nối vào nút $X_p$, Drain nối ra nút ngõ ra `out`.
     * Cực Thân của cả 3 PMOS nối lên `vdd`.
   - **Mạng kéo xuống (PDN):**
     * Đặt 2 NMOS nhánh nối tiếp: $W = 8\\lambda_{DR} = 2,40\,\\mu\\text{m}, L = 2\\lambda_{DR} = 0,60\,\\mu\\text{m}$.
       Drain $M_{NA}$ nối ra `out`, Source $M_{NA}$ nối với Drain $M_{NB}$ (tạo nút nội $X_n$), Source $M_{NB}$ nối xuống `gnd`.
     * Đặt 1 NMOS nhánh đơn: $W = 4\\lambda_{DR} = 1,20\,\\mu\\text{m}, L = 2\\lambda_{DR} = 0,60\,\\mu\\text{m}$.
       Drain $M_{NC}$ nối ra `out`, Source $M_{NC}$ nối xuống `gnd`.
     * Cực Thân của cả 3 NMOS nối xuống `gnd`.
   - **Đấu nối cực Cổng:** Cổng chung $M_{PA}, M_{NA}$ làm ngõ `A`; cổng chung $M_{PB}, M_{NB}$ làm ngõ `B`; cổng chung $M_{PC}, M_{NC}$ làm ngõ `C`.
3. **Tạo 6 chân Export chuẩn (`Ctrl + E`):** `A` (In), `B` (In), `C` (In), `out` (Out), `vdd` (Power), `gnd` (Ground).
4. Nhấn phím `F5` kiểm tra kết nối mạng (bảo đảm **0 errors, 0 warnings**).
5. Đóng gói Cell Icon `aoi21_x1{ic}`.
6. **Mô phỏng kiểm chứng chức năng logic trên LTspice (`aoi21_func.sp`):**
   - Thiết lập 3 nguồn xung vuông `PULSE` với chu kỳ: $T_A = 40\,\text{ns}, T_B = 20\,\text{ns}, T_C = 10\,\text{ns}$ để quét đủ 8 tổ hợp từ `000` đến `111` trong khoảng thời gian $80\,\text{ns}$:
     ```spice
     Va A 0 PULSE(0 5.0 0 100p 100p 19.9n 40n)
     Vb B 0 PULSE(0 5.0 0 100p 100p 9.9n 20n)
     Vc C 0 PULSE(0 5.0 0 100p 100p 4.9n 10n)
     .tran 0 80n 0 1p
     ```
   - Dùng lệnh `.MEAS` đọc điện áp $V(out)$ tại thời điểm ổn định cuối mỗi chu kỳ (ví dụ $t = 2.5\,\text{ns}, 7.5\,\text{ns}, \dots$) để xác nhận bảng chân trị.

---

### 6.2 Bài tập Ex3.2: Thực Nghiệm Đo Logical Effort $g$ và Trễ Ký Sinh $p$

1. **Thiết lập Testbench kép trong LTspice (`logical_effort_meas.sp`):**
   - Đặt đồng thời cổng `INV_X1` và cổng `AOI21_X1` trong cùng một file mô phỏng.
   - Cấp xung kích thích ngõ vào biên độ $0 \to 5\,\text{V}$, thời gian sườn xung $t_r = t_f = 50\,\text{ps}$.
2. **Khảo sát đường trễ Inverter cơ sở:**
   - Nối ngõ ra Inverter vào tải $C_L$. Sử dụng lệnh `.step param CL 10f 40f 10f`.
   - Dùng `.MEAS` đo trễ truyền lan $t_{pd,inv} = (t_{pHL} + t_{pLH})/2$.
   - Trích xuất hệ số góc $\text{Slope}_{inv}$ (ps/fF) và giao điểm $t_{pd0,inv}$ (ps).
3. **Khảo sát ngõ vào A của cổng AOI21:**
   - Giữ ngõ $B = 5,0\,\text{V}$ tĩnh, $C = 0,0\,\text{V}$ tĩnh. Cấp xung vào ngõ $A$.
   - Quét tải $C_L \\in \\{20, 40, 60, 80\\}\\,\\text{fF}$ (tương ứng nỗ lực điện $h = C_L / C_{in,A} \\in \\{1, 2, 3, 4\\}$).
   - Đo trễ truyền lan $t_{pd,A}$ tại từng bước tải.
4. **Khảo sát trường hợp xấu nhất của ngõ vào C:**
   - Giữ ngõ $A = 5,0\,\text{V}$ tĩnh, $B = 0,0\,\text{V}$ tĩnh (chỉ 1 PMOS trong cụm song song dẫn). Cấp xung vào ngõ $C$.
   - Đo trễ worst-case của ngõ C ở tải $C_L = 50\,\text{fF}$.
5. **Hồi quy tuyến tính & Tính toán:**
   - Xác định $g_{meas,A} = \\frac{\\text{Slope}_{h,A}}{\\text{Slope}_{h,inv}}$ và so sánh với giá trị lý thuyết $2,00$.
   - Xác định $p_{meas} = \\frac{t_{pd0,A}}{t_{pd0,inv}}$ và so sánh với giá trị lý thuyết $2,25$.

---

### 6.3 Bài tập Ex3.3: Thiết kế và Mô phỏng Tối ưu Chuỗi Đệm Inverter 3 Tầng

![Chuỗi đệm Inverter](images/buffer_chain_schematic.png)

1. **Tạo Cell Schematic `buf_chain_3st{sch}`:**
   - Đặt 3 Inverter mắc nối tiếp nhau:
     * **Tầng 1 ($1,0\\times$):** $W_n = 4\\lambda_{DR} = 1,20\,\\mu\\text{m}, W_p = 12\\lambda_{DR} = 3,60\,\\mu\\text{m}$.
     * **Tầng 2 ($3,7\\times$):** $W_n = 15\\lambda_{DR} = 4,50\,\\mu\\text{m}, W_p = 44\\lambda_{DR} = 13,20\,\\mu\\text{m}$.
     * **Tầng 3 ($13,6\\times$):** $W_n = 54\\lambda_{DR} = 16,20\,\\mu\\text{m}, W_p = 163\\lambda_{DR} = 48,90\,\\mu\\text{m}$.
   - Gán chân Export: `in`, `out`, `vdd`, `gnd`.
   - Nhấn `F5` kiểm tra đạt 0 errors, 0 warnings. Đóng gói Icon `buf_chain_3st{ic}`.
2. **Mô phỏng đối sánh hiệu năng trên LTspice (`buffer_chain_opt.sp`):**
   - **Kịch bản A:** Đặt 1 Inverter đơn `INV_X1` lái trực tiếp tải nặng $C_L = 1,0\,\text{pF}$.
   - **Kịch bản B:** Đặt chuỗi đệm 3 tầng `buf_chain_3st` lái tải nặng $C_L = 1,0\,\text{pF}$.
   - Tần số xung kích thích: $20\,\text{MHz}$ (chu kỳ $50\,\text{ns}$).
   - Dùng lệnh `.MEAS` đo trễ truyền lan $t_{pd}$, thời gian sườn tăng $t_{rise}$ và sườn giảm $t_{fall}$ tại tải $1\,\text{pF}$ cho cả hai kịch bản.
   - Tính tỉ số cải thiện tốc độ $\\frac{t_{pd,direct}}{t_{pd,chain}}$ và phần trăm giảm trễ $\\frac{t_{pd,direct} - t_{pd,chain}}{t_{pd,direct}} \\times 100\\%$.

---

### 6.4 Bài tập Ex3.4: Thiết kế Mask Layout Cổng AOI21 (Thứ tự C - A - B)

1. Trong Electric VLSI, tạo cell mới kiểu layout: `aoi21_x1{lay}`.
2. Bố trí hai đường ray nguồn Metal 1 nằm ngang `vdd` (ở đỉnh) và `gnd` (ở đáy) với bề rộng $\\ge 6\\lambda_{DR} = 1,80\,\\mu\\text{m}$, khoảng cách chiều cao ô chuẩn mở rộng $H_{cell} = 60\\lambda_{DR} = 18,0\,\\mu\\text{m}$.
3. Đặt dải P-Active liên tục ở nửa trên ($W_p = 24\\lambda_{DR}$) nằm trọn trong vùng N-Well.
4. Đặt dải N-Active ở nửa dưới.
5. **Vẽ 3 dải Polysilicon thẳng đứng theo thứ tự Euler tối ưu: $C - A - B$:**
   - Dải Poly C ở bên trái, dải Poly A ở giữa, dải Poly B ở bên phải.
   - Khoảng cách giữa Poly C và Poly A đặt $\\ge 6\\lambda_{DR} = 1,80\,\\mu\\text{m}$ (để đủ không gian đặt Contact cực má chung `out`).
6. **Thực hiện đấu nối chia sẻ khuếch tán (Abutment):**
   - **Mạng PDN:** Cực má của $M_{NC}$ và $M_{NA}$ dùng chung 1 tiếp xúc Contact ở giữa nối ra chân `out`. Cực nguồn $M_{NC}$ nối xuống `gnd`. Nút nội $X_n$ giữa $M_{NA}$ và $M_{NB}$ nằm liền mạch trong dải khuếch tán, không đặt contact. Cực nguồn ngoài cùng của $M_{NB}$ nối xuống `gnd`.
   - **Mạng PUN:** Cực nguồn của $M_{PA}$ và $M_{PB}$ dùng chung 1 tiếp xúc Contact ở giữa nối lên ray `vdd`. Nút nội $X_p$ nối cực má của cụm $(A, B)$ sang cực nguồn của $M_{PC}$. Cực má của $M_{PC}$ đặt Contact nối ra chân `out`.
7. Đặt tiếp xúc phân cực phiến: $N^+$-Well Tap lên `vdd` và $P^+$-Substrate Tap xuống `gnd`.
8. Gán đầy đủ 6 nhãn chân Export trên lớp kim loại tương ứng (`A`, `B`, `C`, `out`, `vdd`, `gnd`).
9. Nhấn phím `F5` kiểm tra DRC. Sửa toàn bộ lỗi hình học đạt **0 errors found**.
10. Chạy công cụ NCC LVS (*Tools -> NCC -> Schematic and Layout Comparison*). Xác nhận kết quả hiển thị thông báo **MATCH**.

---

## 7. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (POST-LAB)

### 7.1 Trích xuất Ký sinh PEX & Mô phỏng Sau Layout
1. Bật tùy chọn trích xuất tụ ký sinh trong Electric, xuất file Netlist Post-layout cho `aoi21_x1`.
2. Chạy mô phỏng quá độ tại $C_L = 50\,\\text{fF}$ và đo đạc độ tăng trễ hậu thiết kế (Post-layout vs Pre-layout) do các tụ cực má và tụ nút nội $X_n, X_p$.

### 7.2 Báo Cáo Thực Hành (Mẫu Phiếu Điền Khuyết Cho Sinh Viên)

```
========================================================================================
                          BÁO CÁO THỰC HÀNH: BÀI 3
          CỔNG PHỨC HỢP AOI21 VÀ TỐI ƯU TRỄ THEO PHƯƠNG PHÁP LOGICAL EFFORT
Họ và Tên: ..................................................... MSSV: .................
Lớp: ....................................... Nhóm/Bàn: ......... Ngày: .................
Chữ ký Giảng viên / Điểm nghiệm thu tại bàn: ............................................
========================================================================================
```

#### a. Bảng kiểm chứng Bảng chân trị Cổng AOI21 ($Y = \overline{(A \cdot B) + C}$):

| A | B | C | $V(out)$ Mô phỏng (V) | Mức Logic Thực nghiệm | Trạng thái Logic Lý thuyết | Đánh giá |
| :-: | :-: | :-: | :---: | :---: | :---: | :---: |
| 0 | 0 | 0 | `..............` | `......` | 1 | `[      ]` |
| 0 | 0 | 1 | `..............` | `......` | 0 | `[      ]` |
| 0 | 1 | 0 | `..............` | `......` | 1 | `[      ]` |
| 0 | 1 | 1 | `..............` | `......` | 0 | `[      ]` |
| 1 | 0 | 0 | `..............` | `......` | 1 | `[      ]` |
| 1 | 0 | 1 | `..............` | `......` | 0 | `[      ]` |
| 1 | 1 | 0 | `..............` | `......` | 0 | `[      ]` |
| 1 | 1 | 1 | `..............` | `......` | 0 | `[      ]` |

#### b. Kết quả Đo đạc Hồi quy Tuyến tính Logical Effort (Chân A):

| Fan-out $h$ | Tải dung $C_L$ (fF) | $t_{pHL}$ (ps) | $t_{pLH}$ (ps) | $t_{pd}$ trung bình (ps) |
| :---: | :---: | :---: | :---: | :---: |
| **$h = 1$** | $20\,\text{fF}$ | `..............` | `..............` | `..............` |
| **$h = 2$** | $40\,\text{fF}$ | `..............` | `..............` | `..............` |
| **$h = 3$** | $60\,\text{fF}$ | `..............` | `..............` | `..............` |
| **$h = 4$** | $80\,\text{fF}$ | `..............` | `..............` | `..............` |

- Phương trình hồi quy tuyến tính: $t_{pd}(h) = (\text{Slope}) \cdot h + (\text{Intercept})$
  $$t_{pd}(h) = \text{....................} \cdot h + \text{....................} \quad (\text{ps})$$
- Hằng số trễ Inverter chuẩn đo được: $\tau =$ `....................` ps
- Nỗ lực logic thực nghiệm: $g_{meas,A} = \text{Slope} / \tau =$ `....................` *(Dự đoán Pre-lab: 2,00)*
- Trễ ký sinh thực nghiệm: $p_{meas} = \text{Intercept} / \tau =$ `....................` *(Dự đoán Pre-lab: 2,25)*

#### c. Kết quả Thực nghiệm Tối ưu Chuỗi đệm Lái tải Nặng $C_L = 1\,\text{pF}$:

| Thông số kỹ thuật | Kịch bản A (Lái trực tiếp 1X) | Kịch bản B (Chuỗi đệm 3 tầng) | Tỉ số cải thiện ($\frac{\text{A}}{\text{B}}$) | Mức giảm trễ ($\%$) |
| :--- | :---: | :---: | :---: | :---: |
| **Thời gian trễ $t_{pd}$** | `..............` ns | `..............` ns | Nhanh hơn `......` lần | Giảm `......` $\%$ |
| **Sườn tăng $t_{rise}$ (10%–90%)** | `..............` ns | `..............` ns | Nhanh hơn `......` lần | — |
| **Sườn giảm $t_{fall}$ (90%–10%)** | `..............` ns | `..............` ns | Nhanh hơn `......` lần | — |

---

### 7.3 Câu hỏi Phân tích Chuyên sâu Post-lab

1. **Ưu thế và Giới hạn của Cổng phức hợp trong Thư viện Chuẩn:**  
   Nêu hai lý do vì sao cổng phức hợp (AOI, OAI) được các bộ tổng hợp logic (Logic Synthesis) sử dụng với tần suất rất cao trong các thiết kế ASIC. Nêu một giới hạn vật lý quan trọng khiến người ta không thể tăng số ngõ vào của cổng phức hợp lên quá lớn ($\ge 4$ biến nối tiếp)?
2. **Bản chất Vật lý Ưu thế của Ngõ vào C:**  
   Dựa trên cấu trúc mạch và các số đo trễ thực nghiệm, hãy phân tích tại sao ngõ vào C lại có nỗ lực logic $g_C = 1,75$ nhỏ hơn ngõ A và B ($g=2,0$). Trong thiết kế vi mạch số tốc độ cao, điều này đem lại lợi ích gì cho việc định tuyến các tín hiệu trên đường tới hạn?
3. **So sánh Đường rời NAND2 $\to$ INV $\to$ NOR2 với AOI21:**  
   Tính tổng nỗ lực logic đường truyền $G = g_1 \cdot g_2 \dots$ và tổng trễ ký sinh $\sum p$ cho phương án ghép 3 cổng rời (NAND2 $\to$ INV $\to$ NOR2). So sánh với thông số của cổng phức hợp AOI21 ($g=2,0, p=2,25$) để giải thích vì sao cổng phức hợp lại có ưu thế vượt trội về hiệu năng.

---

### 7.4 Cấu trúc Thư mục Nộp bài Chuẩn (`lab03_MSSV_HoTen/`)
```
lab03_MSSV_HoTen/
│
├── schematics/             # Các tệp mô phỏng schematic (.asc)
│   ├── aoi21_func.asc
│   ├── logical_effort_meas.asc
│   └── buffer_chain_opt.asc
│
├── netlists/               # Các tệp Netlist SPICE (.sp)
│   ├── aoi21_func.sp
│   ├── logical_effort_meas.sp
│   ├── buffer_chain_opt.sp
│   └── aoi21_pex.sp
│
├── waveforms/              # Ảnh chụp dạng sóng và kết quả đo
│   ├── aoi21_func_plot.png
│   ├── logical_effort_plot.png
│   ├── buffer_chain_plot.png
│   ├── aoi21_drc_clean.png
│   └── aoi21_ncc_match.png
│
├── lab03_MSSV.jelib        # Thư viện Electric chứa aoi21_x1 và buf_chain_3st
├── C5_models.txt           # Thư viện mô hình công nghệ
└── Bao_Cao_Lab03_MSSV.pdf  # Báo cáo kỹ thuật tổng kết (từ 3 đến 4 trang)
```

---

## 8. BẢNG KIỂM CHỨNG VÀ ĐỐI CHUẨN KỸ THUẬT (BENCHMARK)

Bảng đối chuẩn kỹ thuật giúp sinh viên tự rà soát kết quả trước khi nộp sản phẩm:

| STT | Hạng mục kiểm tra kỹ thuật | Tiêu chí đạt chuẩn | Trạng thái (Đạt / Chưa đạt) |
| :---: | :--- | :--- | :---: |
| 1 | **Schematic AOI21 & Chuỗi đệm** | 0 lỗi DRC kết nối mạng F5; gán đủ 6 Export cho AOI21; Icon chuẩn. | `[        ]` |
| 2 | **Kiểm chứng Bảng chân trị** | Đúng tuyệt đối 8 trạng thái logic $Y = \overline{(A \cdot B) + C}$. | `[        ]` |
| 3 | **Đo Logical Effort $g_A$** | Sai lệch giữa $g_{meas}$ thực nghiệm và lý thuyết ($2,00$) $\le 15\\%$. | `[        ]` |
| 4 | **Trễ ký sinh thực nghiệm $p$** | Giá trị đo được nằm trong dải $1,8 - 2,6$ (chuẩn hóa theo $p_{inv}$). | `[        ]` |
| 5 | **Hiệu quả Chuỗi đệm 3 tầng** | Thời gian trễ $t_{pd}$ giảm tối thiểu $3,0$ lần so với lái trực tiếp 1X. | `[        ]` |
| 6 | **Mặt nạ Layout AOI21** | Thứ tự Poly $C-A-B$; chia sẻ cực má chung Out; chiều cao $H_{cell} = 60\\lambda_{DR}$. | `[        ]` |
| 7 | **DRC & LVS AOI21** | DRC đạt **0 errors found**; LVS NCC báo **MATCH** hoàn hảo. | `[        ]` |
| 8 | **Báo cáo & Phân tích chuyên sâu** | Hoàn thành đủ các bảng số liệu, giải thích rõ cơ chế vật lý của $g, p$. | `[        ]` |

---

## 9. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP

1. **Lỗi đo $g_{meas} \approx 1,0$ không khớp lý thuyết ($2,00$):**
   - *Hiện tượng:* Hồi quy trễ theo $h$ ra hệ số góc xấp xỉ bằng $1 \cdot \tau$.
   - *Nguyên nhân:* Sinh viên định nghĩa sai nỗ lực điện $h = C_L / C_{in,inv}$. Vì cổng đã định cỡ cùng $R_{on}$, trễ theo $C_L / C_{in,inv}$ luôn có hệ số góc bằng $1$.
   - *Khắc phục:* Đặt $h = C_L / C_{in,A}$ (với $C_{in,A} = 2 C_{in,inv}$) và tính $g_{meas} = \text{Slope}_{h,A} / \text{Slope}_{h,inv}$.
2. **Lỗi đo ngõ C ra kết quả quá nhanh không phản ánh trường hợp xấu nhất:**
   - *Hiện tượng:* Đo trễ sườn lên ngõ C thấy nhanh hơn ngõ A tới $25\%$.
   - *Nguyên nhân:* Sinh viên đặt $A = B = 0$ khi kích C. Khi đó cả 2 PMOS A và B cùng dẫn song song, làm điện trở kéo lên giảm còn $744\,\Omega$ thay vì $992\,\Omega$.
   - *Khắc phục:* Đặt $A = 1, B = 0$ (hoặc $A = 0, B = 1$) khi kích C để đo đúng trường hợp xấu nhất (chỉ 1 PMOS trong cụm song song dẫn).
3. **Lỗi DRC khoảng cách Poly-to-Poly trên Layout:**
   - *Hiện tượng:* Báo lỗi khoảng cách tối thiểu giữa Poly C và Poly A.
   - *Nguyên nhân:* Đặt khoảng cách $3\lambda_{DR}$ tại nơi có đặt Contact ngõ ra `out`.
   - *Khắc phục:* Khoảng cách giữa 2 dải Poly có Contact ở giữa bắt buộc phải $\ge 6\lambda_{DR} = 1,80\,\mu\text{m}$.
4. **Hiện tượng Glitch khi mô phỏng bảng chân trị logic:**
   - *Hiện tượng:* Xuất hiện gai điện áp nhọn tại các thời điểm chuyển mạch ngõ vào.
   - *Nguyên nhân:* Các nguồn xung $A, B, C$ đổi trạng thái đồng thời gây ra hiện tượng chạy đua tín hiệu (Race Condition).
   - *Khắc phục:* Lấy mẫu điện áp ở thời điểm ổn định cuối chu kỳ (cách xa thời điểm sườn xung) bằng lệnh `.MEAS FIND V(out) AT=...`.

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

| Tiêu chí đánh giá | Trọng số | Chuẩn đầu ra | Mức Xuất sắc (8.5 – 10) | Mức Khá (7.0 – 8.4) | Mức Đạt (5.0 – 6.9) | Mức Không đạt (< 5.0) |
| :--- | :---: | :---: | :--- | :--- | :--- | :--- |
| **1. Chuẩn bị Pre-lab** | **20%** | CLO1 | Tính toán chính xác $100\\%$ kích thước và $g, p$ cho OAI21; giải bài toán buffer chain $F=64$ chính xác; vẽ đúng Stick diagram $C-A-B$. | Tính đúng các công thức chính; bài toán buffer chain đúng; Stick diagram đúng nguyên lý. | Tính toán còn sai lệch số học; Stick diagram vẽ sơ sài, thiếu tiếp xúc Taps. | Không làm Pre-lab hoặc sao chép bài người khác. |
| **2. Schematic & Chân trị AOI21** | **20%** | CLO2 | Dựng Schematic chuẩn kích thước, 0 lỗi F5; kiểm chứng đủ 8 trạng thái logic sạch sẽ, xử lý tốt glitch. | Dựng đúng mạch; kiểm chứng được 8 trạng thái logic; thao tác SPICE tương đối tốt. | Dựng được mạch nhưng kết nối còn cảnh báo F5; đo chân trị còn nhầm lẫn. | Không dựng được mạch hoặc sơ đồ báo lỗi cú pháp. |
| **3. Đo Logical Effort $g$ & $p$** | **20%** | CLO2 | Thiết lập đúng testbench kép với `INV_X1`; quét đủ các mức tải; trích xuất thực nghiệm $g_{meas}$ và $p_{meas}$ khớp lý thuyết trong sai lệch $\le 15\\%$. | Thiết lập được testbench; đo được trễ nhưng thao tác hồi quy còn chậm. | Đo trễ thủ công; hệ số $g_{meas}$ sai lệch nhiều do chưa chuẩn hóa đúng theo $h$. | Không đo được Logical Effort hoặc số liệu phi lý. |
| **4. Tối ưu Chuỗi đệm** | **15%** | CLO2 | Hiện thực chuẩn xác chuỗi đệm 3 tầng; chứng minh thực nghiệm trễ giảm $> 3$ lần so với lái trực tiếp 1X; phân tích rõ sườn xung. | Thiết kế được chuỗi đệm 3 tầng; đo được độ giảm trễ nhưng tính toán kích thước tầng còn làm tròn lệch. | Lắp ráp được chuỗi đệm nhưng trễ đo đạc chưa tối ưu; thao tác đo lúng túng. | Không hiện thực được bài toán chuỗi đệm. |
| **5. Mask Layout, DRC & LVS** | **15%** | CLO4 | Layout AOI21 tối ưu dải khuếch tán $C-A-B$, khoảng cách Poly $\ge 6\\lambda$ qua contact; 0 lỗi DRC; LVS MATCH 100% độc lập. | Layout đúng chuẩn, 0 lỗi DRC; LVS match sau 1 lần chỉnh sửa nhỏ nhãn chân. | Layout cồng kềnh, vi phạm một vài lỗi DRC khoảng cách nhưng tự sửa được; LVS match. | Vi phạm nhiều lỗi DRC nghiêm trọng; LVS không match; bỏ dở layout. |
| **6. Báo cáo, Đối sánh & Vấn đáp** | **10%** | CLO1, CLO4 | Báo cáo đầy đủ, số liệu trung thực; trả lời xuất sắc 3 câu hỏi biện luận chuyên sâu và câu hỏi vấn đáp tại bàn của giảng viên. | Điền đủ số liệu; trả lời đúng các câu hỏi lý thuyết chính. | Báo cáo hoàn thành nhưng phần biện luận ưu thế ngõ C còn sơ sài. | Báo cáo để trống nhiều phần; không trả lời được vấn đáp. |

---

## 11. TÀI LIỆU THAM KHẢO

1. **Giáo trình chính:** I. Sutherland, R. F. Sproull, D. M. Harris, *Logical Effort: Designing Fast CMOS Circuits*, Morgan Kaufmann, 1999 (Chương 1: Introduction; Chương 3: Designing Combinational Gates).
2. **Sách tham khảo chuẩn:** J. M. Rabaey, A. Chandrakasan, B. Nikolić, *Digital Integrated Circuits: A Design Perspective*, 2nd ed., Prentice Hall, 2003 (Chương 6: Designing Combinational Logic Gates in CMOS).
3. **Thư viện mô hình:** MOSIS SCMOS Submicron C5N 0.5µm Model Parameters ([C5_models.txt](file:///d:/tam/VLSI_Spice/04%20-%20Models_and_Libraries/C5_models.txt)).
4. **Tài liệu công cụ:** Electric VLSI Design System User Manual, Version 9.07+, Static Free Software.
"""

target_path = r"d:\tam\VLSI_Spice\02 - Student Workbook\lab-03-cong-phuc-hop-aoi-oai-logical-effort.md"
with open(target_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print(f"Successfully updated {target_path} ({len(content)} bytes, LF newlines)")
