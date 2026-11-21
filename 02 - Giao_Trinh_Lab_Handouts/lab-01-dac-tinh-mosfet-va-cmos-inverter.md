# THỰC HÀNH THIẾT KẾ VLSI — BÀI 1
# ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER

---
**Bộ môn:** Điện tử - Viễn thông | **Khoa:** Điện - Điện tử  
**Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Thời lượng:** 5 tiết thực hành tại phòng máy (kết hợp tự học Pre-lab & hoàn thiện Post-lab)  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07+), LTspice XVII / LTspice 2025  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5µm ($\lambda = 0.30\,\mu\text{m}$, 3 Metal layers, $V_{DD} = 5.0\,\text{V}$)  
---

## I. MỤC TIÊU

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Trích xuất tham số vật lý MOSFET:** Sử dụng LTspice để quét DC họ đặc tuyến $I_{DS}-V_{DS}$ và $I_{DS}-V_{GS}$ của NMOS và PMOS; trích xuất thực nghiệm điện áp ngưỡng ($V_{thn}, V_{thp}$), hệ số dẫn suất transconductance ($K_n', K_p'$), và hệ số điều chế chiều dài kênh ($\lambda$).
2. **Thiết kế & Tối ưu Schematic Inverter:** Xây dựng sơ đồ nguyên lý CMOS Inverter trên Electric VLSI; định kích thước cân bằng $(W/L)_p / (W/L)_n \approx 3/1$ để đạt điện áp chuyển mạch đối xứng $V_M = V_{DD}/2 = 2.50\,\text{V}$ và cân bằng thời gian chuyển đổi.
3. **Phân tích VTC & Đo đạc Lề nhiễu:** Mô phỏng đường cong truyền đạt điện áp (VTC); xác định các điểm dốc đơn vị $dV_{out}/dV_{in} = -1$ để tính các mức điện thế logic $V_{IL}, V_{IH}$ và lề nhiễu logic $NM_L, NM_H$.
4. **Đo đạc Động học Quá độ bằng Lệnh SPICE:** Mô phỏng Transient đáp ứng thời gian thực; sử dụng cú pháp lệnh `.MEAS` để tự động trích xuất thời gian tăng ($t_r$), thời gian giảm ($t_f$) và trễ truyền lan trung bình ($t_{pd}$) với các mức tải dung $C_L = 10\,\text{fF}, 50\,\text{fF}, 100\,\text{fF}$.
5. **Thiết kế Mặt nạ Vật lý (Physical Layout):** Vẽ Layout hoàn chỉnh cho Inverter tuân thủ luật hình học MOSIS SCMOS ($\lambda = 0.30\,\mu\text{m}$); kiểm tra luật thiết kế DRC đạt 0 lỗi và đối chiếu LVS đạt trùng khớp 100%.
6. **Trích xuất Ký sinh (PEX) & Phân tích Post-layout:** Trích xuất tụ ký sinh khuếch tán ($C_{db}, C_{sb}$) và điện dung dây dẫn kim loại; lập bảng đối chiếu định lượng sự suy giảm tốc độ giữa Pre-layout và Post-layout.
7. **Đóng gói Thư viện Chuẩn:** Tạo tế bào chuẩn `INV_X1` kèm Icon View để tái sử dụng làm thư viện cơ sở cho toàn bộ các bài Lab tiếp theo.

---

## II. CÔNG CỤ VÀ THƯ VIỆN MÔ HÌNH

1. **Phần mềm thiết kế vi mạch:**
   - **Electric VLSI Design System:** Phiên bản 9.07 trở lên (cấu hình công nghệ `mocmos`, đơn vị $\lambda = 0.30\,\mu\text{m}$).
   - **LTspice:** Phiên bản XVII hoặc 2025 (thiết lập liên kết tự động trong Electric: *Preferences $\to$ Tools $\to$ Spice/CDL*).
2. **Thư viện mô hình SPICE (PDK):**
   - Tệp mô hình: `04 - Models_and_Libraries/C5_models.txt` chứa tham số NMOS (Model: `N`) và PMOS (Model: `P`) tiến trình C5N 0.5µm chuẩn Level 3 MOSIS.

---

## III. CƠ SỞ LÝ THUYẾT VÀ NGUYÊN LÝ THIẾT KẾ

### 1. Mô hình dòng điện của MOSFET
Trong tiến trình CMOS n-well, dòng điện má-nguồn $I_{DS}$ của NMOS được mô hình hóa theo ba chế độ hoạt động:
- **Vùng ngưng dẫn (Cut-off):** $V_{GS} < V_{thn}$

  $$I_{DS} \approx 0$$

- **Vùng tuyến tính (Linear / Triode):** $V_{GS} \ge V_{thn}$ và $V_{DS} < V_{GS} - V_{thn}$

  $$I_{DS} = K_n' \left(\frac{W}{L}\right)_n \left[ (V_{GS} - V_{thn}) V_{DS} - \frac{V_{DS}^2}{2} \right] (1 + \lambda V_{DS})$$

- **Vùng bão hòa (Saturation):** $V_{GS} \ge V_{thn}$ và $V_{DS} \ge V_{GS} - V_{thn}$

  $$I_{DS} = \frac{K_n'}{2} \left(\frac{W}{L}\right)_n (V_{GS} - V_{thn})^2 (1 + \lambda V_{DS})$$

Trong đó:
- $K_n' = \mu_n C_{ox}$ là hệ số dẫn suất truyền dẫn (Process Transconductance Parameter).
- $V_{thn}$ là điện áp ngưỡng của NMOS.
- $\lambda$ là hệ số điều chế chiều dài kênh (Channel Length Modulation).
- Đối với PMOS, các phương trình tương tự áp dụng với $V_{GS}, V_{DS}, V_{thp}$ đổi cực tính và thay $K_n'$ bằng $K_p' = \mu_p C_{ox}$. Do độ linh động của lỗ trống nhỏ hơn điện tử ($\mu_n \approx 2.5 - 3 \times \mu_p$), nên $K_n' \approx 3 K_p'$.

---

### 2. Đường cong truyền đạt điện áp VTC của CMOS Inverter

Sơ đồ nguyên lý CMOS Inverter gồm 1 PMOS kéo lên nguồn ($V_{DD}$) và 1 NMOS kéo xuống đất ($GND$):

```
             VDD (5.0V)
                 │
             ┌───┴───┐
             │  PMOS │ (Wp, Lp)
     In ─────┤       ├─────┬───── Out
             └───┬───┘     │
                 │         │
             ┌───┴───┐     │
             │  NMOS │     │
     In ─────┤       ├─────┘   (Wn, Ln)
             └───┬───┘
                 │
                GND (0V)
```

Đường cong truyền đạt điện áp $V_{out} = f(V_{in})$ chia thành 5 vùng hoạt động tùy thuộc trạng thái của 2 transistor:

| Vùng | Điện áp vào $V_{in}$ | Trạng thái NMOS | Trạng thái PMOS | Điện áp ra $V_{out}$ |
| :---: | :---: | :---: | :---: | :---: |
| **A** | $0 \le V_{in} < V_{thn}$ | Ngưng dẫn (Cut-off) | Tuyến tính (Linear) | $V_{OH} = V_{DD}$ |
| **B** | $V_{thn} \le V_{in} < V_M$ | Bão hòa (Saturation) | Tuyến tính (Linear) | Giảm chậm |
| **C** | $V_{in} = V_M \approx V_{DD}/2$ | Bão hòa (Saturation) | Bão hòa (Saturation) | Giảm dốc đứng (Khuếch đại cao) |
| **D** | $V_M < V_{in} \le V_{DD} - \vert V_{thp} \vert$ | Tuyến tính (Linear) | Bão hòa (Saturation) | Giảm chậm về mức thấp |
| **E** | $V_{in} > V_{DD} - \vert V_{thp} \vert$ | Tuyến tính (Linear) | Ngưng dẫn (Cut-off) | $V_{OL} = 0\,\text{V}$ |

#### a. Điện áp ngưỡng chuyển mạch $V_M$ (Switching Threshold)
Điểm chuyển mạch $V_M$ được định nghĩa tại vị trí $V_{out} = V_{in} = V_M$. Tại điểm này, cả NMOS và PMOS đều ở vùng bão hòa. Cân bằng phương trình dòng điện:

$$I_{D,sat(n)} = I_{D,sat(p)} \iff \frac{K_n'}{2}\left(\frac{W}{L}\right)_n (V_M - V_{thn})^2 = \frac{K_p'}{2}\left(\frac{W}{L}\right)_p (V_{DD} - V_M - |V_{thp}|)^2$$

Đặt $r = \frac{K_p' (W/L)_p}{K_n' (W/L)_n}$, ta có biểu thức tính $V_M$:

$$V_M = \frac{V_{thn} + \sqrt{r} (V_{DD} - |V_{thp}|)}{1 + \sqrt{r}}$$

Để mạch đối xứng lý tưởng $V_M = V_{DD}/2$:

$$r = 1 \implies \frac{(W/L)_p}{(W/L)_n} = \frac{K_n'}{K_p'} = \frac{\mu_n}{\mu_p} \approx 3.0$$

#### b. Lề nhiễu logic (Noise Margins)
Lề nhiễu đặc trưng cho khả năng chống nhiễu điện áp của cổng logic:
- $V_{IL}$ (Điện áp vào mức thấp cực đại): Điểm trên VTC mà tại đó độ dốc $\frac{dV_{out}}{dV_{in}} = -1$ (khi $V_{in}$ thấp).
- $V_{IH}$ (Điện áp vào mức cao cực tiểu): Điểm trên VTC mà tại đó độ dốc $\frac{dV_{out}}{dV_{in}} = -1$ (khi $V_{in}$ cao).
- Lề nhiễu mức thấp: $NM_L = V_{IL} - V_{OL} = V_{IL} - 0 = V_{IL}$.
- Lề nhiễu mức cao: $NM_H = V_{OH} - V_{IH} = V_{DD} - V_{IH}$.

---

### 3. Động học Quá độ và Phân tích Trễ truyền lan
Khi có tải dung $C_L$ tại ngõ ra, thời gian chuyển mạch phụ thuộc tốc độ nạp/xả dòng qua kênh dẫn:
- **Trễ sườn xuống $t_{pHL}$:** Thời gian ngõ ra chuyển từ mức cao xuống mức thấp qua NMOS.
- **Trễ sườn lên $t_{pLH}$:** Thời gian ngõ ra chuyển từ mức thấp lên mức cao qua PMOS.
- **Trễ truyền lan trung bình:** $t_{pd} = \frac{t_{pHL} + t_{pLH}}{2}$.
- **Thời gian sườn tăng $t_r$:** Thời gian $V_{out}$ tăng từ $10\%$ ($0.5\,\text{V}$) lên $90\%$ ($4.5\,\text{V}$).
- **Thời gian sườn giảm $t_f$:** Thời gian $V_{out}$ giảm từ $90\%$ ($4.5\,\text{V}$) xuống $10\%$ ($0.5\,\text{V}$).

Ước lượng qua mô hình điện trở hiệu dụng trung bình $R_{on}$:

$$t_{pHL} \approx 0.69 \times R_{on,n} \times C_L, \quad t_{pLH} \approx 0.69 \times R_{on,p} \times C_L$$

---

### 4. Quy tắc Thiết kế Hình học MOSIS SCMOS ($\lambda = 0.30\,\mu\text{m}$)
- **Độ rộng tối thiểu:** Polysilicon $= 2\lambda$ ($0.60\,\mu\text{m}$); Metal 1 $= 3\lambda$ ($0.90\,\mu\text{m}$); Active $= 3\lambda$ ($0.90\,\mu\text{m}$).
- **Khoảng cách tối thiểu:** Poly – Poly $= 3\lambda$; Metal 1 – Metal 1 $= 3\lambda$; Active – Active $= 3\lambda$.
- **Khoảng vươn ra (Overhang):** Poly vươn qua mép Active $\ge 2\lambda$ ($0.60\,\mu\text{m}$).
- **Lỗ tiếp xúc (Contact):** Kích thước cố định $2\lambda \times 2\lambda$ ($0.6\,\mu\text{m} \times 0.6\,\mu\text{m}$); Phần kim loại/Active bao quanh tiếp xúc (Enclosure) $\ge 1\lambda$.
- **Phân cực chất nền (Taps):** Bắt buộc phải có $N^+$-tap nối N-Well lên $V_{DD}$ và $P^+$-tap nối P-Substrate xuống $GND$ để ngăn chặn hiện tượng kích hoạt Latch-up.

---

### 5. Cú pháp Lệnh Đo đạc Tự động SPICE (.MEASURE)
Trong LTspice, các thông số trễ và lề nhiễu được đo tự động bằng cách chèn câu lệnh SPICE Directive (nhấn phím tắt `S`):
```spice
* Đo trễ sườn xuống tpHL (tính từ điểm 50% Vin đến điểm 50% Vout)
.MEASURE TRAN tpHL TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 FALL=1

* Đo trễ sườn lên tpLH
.MEASURE TRAN tpLH TRIG V(in)=2.5 FALL=1 TARG V(out)=2.5 RISE=1

* Tính trễ trung bình tpd
.MEASURE TRAN tpd PARAM (tpHL + tpLH)/2

* Đo thời gian tăng trise (10% lên 90%) và thời gian giảm tfall (90% xuống 10%)
.MEASURE TRAN trise TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1
.MEASURE TRAN tfall TRIG V(out)=4.5 FALL=1 TARG V(out)=0.5 FALL=1
```
> Kết quả đo từ các câu lệnh `.MEAS` được lưu và đọc trực tiếp trong mục **View $\to$ SPICE Error Log** (phím tắt `Ctrl + L`).

---

## IV. CHUẨN BỊ TRƯỚC THỰC HÀNH (PRE-LAB - Ở NHÀ)

> [!IMPORTANT]
> Toàn bộ phần IV phải được sinh viên chuẩn bị trước vào **Mục VI.a (Phần chuẩn bị)** trong Phiếu báo cáo ở cuối bài này. Giảng viên kiểm tra và ký xác nhận đầu giờ; sinh viên không làm bài chuẩn bị sẽ không được cấp quyền thực hành trên máy tính.

1. **Khảo sát tham số công nghệ:**  
   Mở tệp `C5_models.txt` tại thư mục `04 - Models_and_Libraries/`. Trích xuất các giá trị tham số sau của NMOS và PMOS:
   - Điện áp ngưỡng không phân cực đế: `VTO`
   - Hệ số transconductance: `KP`
   - Chiều dày lớp oxit cổng: `TOX`
   - Chiều sâu tiếp giáp: `XJ`
2. **Tính toán giải tích tỉ số $(W_p/W_n)$:**  
   Với $V_{DD} = 5.0\,\text{V}$, $V_{thn} = 0.70\,\text{V}$, $|V_{thp}| = 0.80\,\text{V}$, $K_n' = 120\,\mu\text{A/V}^2$, $K_p' = 40\,\mu\text{A/V}^2$:
   - Tính tỉ số định kích thước $\frac{(W/L)_p}{(W/L)_n}$ chính xác để $V_M = 2.50\,\text{V}$.
   - Nếu chọn $L_n = L_p = 2\lambda = 0.60\,\mu\text{m}$ và $W_n = 4\lambda = 1.20\,\mu\text{m}$, hãy xác định độ rộng $W_p$ tương ứng.
3. **Ước lượng điện trở dẫn và thời gian trễ lý thuyết:**  
   - Tính giá trị điện trở dẫn hiệu dụng $R_{on,n}$ và $R_{on,p}$ theo công thức ở mục III.3.
   - Ước lượng trễ sườn xuống $t_{pHL}$ và sườn lên $t_{pLH}$ khi kéo tải dung $C_L = 50\,\text{fF}$.
4. **Vẽ sơ đồ que (Stick Diagram):**  
   Vẽ sơ đồ que của CMOS Inverter lên giấy kẻ ô ly với quy ước:
   - Đường ray $V_{DD}$ (trên) và $GND$ (dưới) bằng Metal 1.
   - Vùng P-Active trong N-Well, vùng N-Active trên P-Substrate.
   - Dải Poly chạy dọc làm cực cổng chung nối ngõ vào `in`.
   - Cực Drain chung nối bằng Metal 1 ra ngõ xuất `out`.
   - Vị trí đầy đủ của các nút tiếp xúc Contact và các tiếp xúc phân cực Substrate/Well Taps.
5. **Soạn thảo Netlist SPICE:**  
   Viết trước mã Netlist SPICE cho CMOS Inverter kết hợp nguồn xung vuông $50\,\text{MHz}$ và các câu lệnh `.MEAS` để chuẩn bị chạy mô phỏng.

---

## V. NỘI DUNG THỰC HÀNH TẠI PHÒNG LAB (IN-LAB)

### 1. Khảo sát Đặc tính I-V của NMOS và PMOS trên LTspice
1. Mở LTspice, tạo mạch thử nghiệm cho transistor NMOS (`nmos_iv.asc`):
   - Đặt 1 NMOS từ thư viện linh kiện (phím `F2` $\to$ chọn `nmos4`). Đặt kích thước: `L=0.6u`, `W=1.2u`.
   - Đặt nguồn $V_{DS}$ nối vào cực Drain, nguồn $V_{GS}$ nối vào cực Gate. Cực Source và Bulk nối đất ($GND$).
   - Thêm câu lệnh gọi thư viện: `.include C5_models.txt`.
2. **Khảo sát họ đặc tuyến ra $I_{DS}-V_{DS}$:**
   - Cấu hình quét DC kép:
     ```spice
     .dc VDS 0 5 0.01 VGS 1 5 1
     ```
   - Chạy mô phỏng, thêm trace dòng $I(M1)$.
   - Quan sát 5 đường đặc tuyến tương ứng $V_{GS} = 1\text{V}, 2\text{V}, 3\text{V}, 4\text{V}, 5\text{V}$.
   - Đặt con trỏ đo (Cursor) tại đoạn bão hòa của đường $V_{GS} = 5.0\,\text{V}$, tính toán hệ số điều chế kênh $\lambda$:

     $$\lambda = \frac{1}{I_{DS}(V_{DS1})} \times \frac{I_{DS}(V_{DS2}) - I_{DS}(V_{DS1})}{V_{DS2} - V_{DS1}}$$

3. **Khảo sát đặc tuyến truyền dẫn $I_{DS}-V_{GS}$ và trích xuất điện áp ngưỡng $V_{thn}$:**
   - Đặt cố định $V_{DS} = 5.0\,\text{V}$. Cấu hình quét: `.dc VGS 0 5 0.01`.
   - Thêm biểu thức đo căn bậc hai của dòng: `sqrt(I(M1))`.
   - Kẻ đường tiếp tuyến với đoạn tuyến tính của đồ thị $\sqrt{I_{DS}}$ cắt trục hoành $V_{GS}$ tại điểm nào thì điểm đó chính là $V_{thn}$.
4. Lặp lại các bước trên cho PMOS ($W = 3.60\,\mu\text{m}, L = 0.60\,\mu\text{m}$, dùng linh kiện `pmos4`), trích xuất $V_{thp}$ và hệ số $\lambda_p$.

---

### 2. Thiết kế Schematic CMOS Inverter và Phân tích VTC
1. Mở Electric VLSI, tạo Cell mới: **Name:** `inv_x1`, **View:** `schematic`.
2. Đặt linh kiện:
   - 1 PMOS: $W = 12\lambda$ ($3.6\,\mu\text{m}$), $L = 2\lambda$ ($0.6\,\mu\text{m}$).
   - 1 NMOS: $W = 4\lambda$ ($1.2\,\mu\text{m}$), $L = 2\lambda$ ($0.6\,\mu\text{m}$).
   - Kết nối dây kim loại và gán nhãn Export chân: `in` (Input), `out` (Output), `vdd` (Power), `gnd` (Ground).
3. Nhấn `F5` để kiểm tra kết nối mạch logic.
4. Xuất Netlist SPICE (*Tools $\to$ Simulation (Spice) $\to$ Write Spice Deck*) sang LTspice.
5. Cấu hình mô phỏng quét DC:
   ```spice
   .dc Vin 0 5 0.005
   ```
6. Chạy mô phỏng, hiển thị dạng sóng $V_{out} = f(V_{in})$.
7. Dùng Cursor xác định điện áp chuyển mạch $V_M$ tại giao điểm $V_{out} = V_{in}$.
8. Thêm trace đạo hàm `d(V(out))/d(V(in))`. Xác định hai điểm có độ dốc bằng $-1.00$ để suy ra $V_{IL}$ và $V_{IH}$, sau đó tính $NM_L$ và $NM_H$.

---

### 3. Đo đạc Động học Quá độ (Transient) & Đóng gói Icon
1. Cấu hình nguồn kích xung ngõ vào $V_{in}$:
   ```spice
   Vin in 0 PULSE(0 5.0 0 100p 100p 9.9n 20n)
   ```
2. Đặt tải dung $C_L = 50\,\text{fF}$ tại ngõ ra `out`.
3. Chèn khối lệnh `.MEAS` đã chuẩn bị ở mục III.5 và cấu hình mô phỏng:
   ```spice
   .tran 1p 50n
   ```
4. Chạy mô phỏng. Mở **SPICE Error Log** (`Ctrl + L`) để đọc trực tiếp các giá trị trễ: $t_{pHL}, t_{pLH}, t_{pd}, t_r, t_f$.
5. Khảo sát ảnh hưởng của tải dung: Thay đổi lần lượt $C_L = 10\,\text{fF}$ và $100\,\text{fF}$, ghi lại các giá trị trễ tương ứng.
6. **Đóng gói Icon trong Electric:** Vào menu **View $\to$ Make Icon View**, vẽ biểu tượng cổng NOT chuẩn IEEE với các chân `in` (trái), `out` (phải), `vdd` (trên) và `gnd` (dưới).

---

### 4. Thiết kế Mask Layout, Chạy DRC & Đối chiếu LVS
1. Trong Electric, tạo Cell mới: **Name:** `inv_x1`, **View:** `layout`.
2. Tạo 2 đường ray nguồn Metal 1 nằm ngang có độ rộng tối thiểu $6\lambda$ ($1.8\,\mu\text{m}$): thanh trên gán nhãn `vdd`, thanh dưới gán nhãn `gnd`.
3. Vẽ vùng N-Well ở nửa trên; đặt vùng P-Active ($W = 12\lambda, L = 2\lambda$) trong N-Well.
4. Đặt vùng N-Active ($W = 4\lambda, L = 2\lambda$) ở nửa dưới.
5. Vẽ dải Polysilicon liên tục cắt ngang qua cả hai vùng Active làm cổng chung. Poly phải vươn thừa ra ngoài mép Active tối thiểu $2\lambda$ ($0.6\,\mu\text{m}$). Gán Export port tên `in` tại đầu dải Poly.
6. Đặt các nút tiếp xúc Contact nối cực Source của PMOS lên `vdd`, cực Source của NMOS xuống `gnd`.
7. Nối cực Drain của hai transistor lại với nhau bằng Metal 1, tạo Export port tên `out`.
8. Đặt tiếp xúc $N^+$-tap nối N-Well lên `vdd` và $P^+$-tap nối chất nền xuống `gnd`.
9. **Kiểm tra luật thiết kế DRC:** Nhấn phím `F5`. Yêu cầu sửa toàn bộ lỗi hình học cho đến khi hệ thống báo: **"0 errors found"**.
10. **Đối chiếu sơ đồ nguyên lý LVS:** Vào menu **Tools $\to$ NCC $\to$ Schematic and Layout Comparison**. Yêu cầu kết quả đạt: **"Cells are topologically equivalent (MATCH)"**.

---

### 5. Trích xuất Ký sinh (PEX) & Phân tích Post-layout
1. Trong cửa sổ Layout của `inv_x1`, vào menu **Tools $\to$ Simulation (Spice) $\to$ Options**, đánh dấu chọn **"Extract Parasitic Capacitances"**.
2. Xuất Netlist sau trích xuất: **Tools $\to$ Simulation (Spice) $\to$ Write Spice Deck**.
3. Mở file Netlist vừa sinh ra, kiểm tra sự xuất hiện của các tham số hình học khuếch tán (`AS, AD, PS, PD`) và các tụ ký sinh dây dẫn kim loại.
4. Chạy mô phỏng quá độ Transient trên LTspice với Netlist Post-layout này dưới cùng điều kiện đo của mục 3 ($C_L = 50\,\text{fF}$).
5. Đọc các thông số trễ sau đóng gói ($t_{pHL,post}, t_{pLH,post}, t_{pd,post}$) và tính độ suy giảm hiệu năng so với Pre-layout.

---

## VI. BÁO CÁO THỰC HÀNH (MẪU PHIẾU ĐIỀN KHUYẾT CHO SINH VIÊN)

```
========================================================================================
                          BÁO CÁO THỰC HÀNH: BÀI 1
            ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER
Họ và Tên: ..................................................... MSSV: .................
Lớp: ....................................... Nhóm/Bàn: ......... Ngày: .................
Chữ ký Giảng viên / Điểm nghiệm thu tại bàn: ............................................
========================================================================================
```

### a. Phần Chuẩn bị (Pre-lab)

1. **Trích xuất tham số từ `C5_models.txt`:**
   - NMOS: `VTO` = ................. V ; `KP` = ................. µA/V² ; `TOX` = ................. m
   - PMOS: `VTO` = ................. V ; `KP` = ................. µA/V² ; `TOX` = ................. m

2. **Tính toán kích thước và trễ lý thuyết ($V_{DD} = 5.0\,\text{V}$):**
   - Tỉ số kích thước lý thuyết: $\frac{(W/L)_p}{(W/L)_n} =$ ........................
   - Kích thước lựa chọn: NMOS ($W_n/L_n$) = ................. / ................. ; PMOS ($W_p/L_p$) = ................. / .................
   - Điện trở dẫn hiệu dụng: $R_{on,n} =$ ........................ $\Omega$ ; $R_{on,p} =$ ........................ $\Omega$
   - Dự đoán trễ với $C_L = 50\,\text{fF}$: $t_{pHL} =$ ................. ps ; $t_{pLH} =$ ................. ps ; $t_{pd} =$ ................. ps

3. **Sơ đồ que (Stick Diagram):**  
   *(Vẽ sơ đồ que hoàn chỉnh của CMOS Inverter vào khung dưới đây, chú thích rõ tên các lớp Metal 1, Poly, Active, N-Well, Contact và các Taps)*

   ```
   ┌──────────────────────────────────────────────────────────────────────────────────┐
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   └──────────────────────────────────────────────────────────────────────────────────┘
   ```

4. **Câu lệnh SPICE đo trễ (.MEAS) đã soạn:**
   ```spice
   ......................................................................................
   ......................................................................................
   ......................................................................................
   ```

---

### b. Phần Thực hành (In-lab)

1. **Kết quả đo đặc tính I-V của MOSFET:**

   | Tham số trích xuất | NMOS ($W=1.2\mu\text{m}, L=0.6\mu\text{m}$) | PMOS ($W=3.6\mu\text{m}, L=0.6\mu\text{m}$) |
   | :--- | :---: | :---: |
   | **Điện áp ngưỡng thực nghiệm ($V_{th}$)** | .................... V | .................... V |
   | **Dòng bão hòa cực đại $I_{DS,max}$ ($V_{GS}=5\text{V}, V_{DS}=5\text{V}$)** | .................... mA | .................... mA |
   | **Hệ số điều chế kênh $\lambda$** | .................... $\text{V}^{-1}$ | .................... $\text{V}^{-1}$ |

   **Vẽ hoặc dán đồ thị đặc tuyến $I_{DS}-V_{DS}$ của NMOS vào khung dưới đây:**
   ```
   ┌──────────────────────────────────────────────────────────────────────────────────┐
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   │                                                                                  │
   └──────────────────────────────────────────────────────────────────────────────────┘
   ```

2. **Kết quả phân tích đường cong truyền đạt VTC:**
   - Điện áp chuyển mạch đo được: $V_M =$ .................... V (Độ lệch so với $2.5\,\text{V}$: ............. %)
   - Điện áp vào mức thấp: $V_{IL} =$ .................... V
   - Điện áp vào mức cao: $V_{IH} =$ .................... V
   - Lề nhiễu logic mức thấp: $NM_L =$ .................... V
   - Lề nhiễu logic mức cao: $NM_H =$ .................... V

3. **Kết quả đo trễ quá độ (Transient) Pre-layout:**

   | Tải dung $C_L$ | $t_{pHL}$ (ps) | $t_{pLH}$ (ps) | $t_{pd}$ trung bình (ps) | Thời gian tăng $t_r$ (ps) | Thời gian giảm $t_f$ (ps) |
   | :---: | :---: | :---: | :---: | :---: | :---: |
   | **$10\,\text{fF}$** | ................ | ................ | ................ | ................ | ................ |
   | **$50\,\text{fF}$** | ................ | ................ | ................ | ................ | ................ |
   | **$100\,\text{fF}$** | ................ | ................ | ................ | ................ | ................ |

   **Nhận xét về mối quan hệ giữa trễ truyền lan $t_{pd}$ và tải dung $C_L$:**
   ....................................................................................................................................................  
   ....................................................................................................................................................

4. **Kết quả Thiết kế Mask Layout và Kiểm chứng Vật lý:**
   - Kích thước hình học tế bào: Chiều rộng $W =$ ............. $\lambda$ ($.............\,\mu\text{m}$); Chiều cao $H =$ ............. $\lambda$ ($.............\,\mu\text{m}$)
   - Diện tích tế bào (Area): ........................ $\mu\text{m}^2$
   - Số lỗi kiểm tra DRC: .................... lỗi
   - Kết quả đối chiếu LVS: ....................................................................................................................

5. **Bảng Đối chiếu Tổng hợp 3 Chiều (Lý thuyết vs Pre-layout vs Post-layout):**  
   (Với tải dung chuẩn $C_L = 50\,\text{fF}$)

   | Đại lượng kỹ thuật | [1] Lý thuyết tính tay | [2] SPICE Pre-layout | [3] SPICE Post-layout (PEX) | Sai số PEX vs Pre-layout ($\frac{[3]-[2]}{[2]} \times 100\%$) |
   | :--- | :---: | :---: | :---: | :---: |
   | **Điện áp $V_M$ (V)** | $2.50\,\text{V}$ | .............. V | .............. V | .............. % |
   | **Lề nhiễu $NM_L$ (V)** | .............. V | .............. V | .............. V | .............. % |
   | **Lề nhiễu $NM_H$ (V)** | .............. V | .............. V | .............. V | .............. % |
   | **Trễ sườn xuống $t_{pHL}$ (ps)** | .............. ps | .............. ps | .............. ps | .............. % |
   | **Trễ sườn lên $t_{pLH}$ (ps)** | .............. ps | .............. ps | .............. ps | .............. % |
   | **Trễ trung bình $t_{pd}$ (ps)** | .............. ps | .............. ps | .............. ps | .............. % |

6. **Phân tích và Biện luận Kỹ thuật:**
   - *Câu hỏi 1: Tại sao thời gian trễ trong mô phỏng Post-layout lại tăng lên so với mô phỏng Pre-layout? Các thành phần ký sinh nào đóng góp chính vào sự gia tăng này?*  
     ................................................................................................................................................  
     ................................................................................................................................................  
     ................................................................................................................................................
   - **Câu hỏi 2:** Nếu trong Layout ta quên đặt tiếp xúc phân cực N-Well Tap lên $V_{DD}$ và Substrate Tap xuống $GND$, vi mạch thực tế sẽ đối mặt với nguy cơ gì? Giải thích cơ chế vật lý.
     ................................................................................................................................................  
     ................................................................................................................................................  
     ................................................................................................................................................
   - **Câu hỏi 3:** Nếu một kỹ sư định kích thước $W_p = W_n$, đường cong VTC và thời gian trễ của Inverter sẽ bị biến đổi như thế nào? Trong trường hợp nào thì thiết kế $W_p = W_n$ được chấp nhận?
     ................................................................................................................................................  
     ................................................................................................................................................  
     ................................................................................................................................................

---

## VII. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

| Tiêu chí | Trọng số | Mức Xuất sắc (8.5 – 10) | Mức Khá (7.0 – 8.4) | Mức Đạt (5.0 – 6.9) | Mức Không đạt (< 5.0) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Chuẩn bị Pre-lab (Mục VI.a)** | **20%** | Tính đúng $W_p/W_n$, $R_{on}$, trễ lý thuyết; Stick diagram chính xác, đủ các lớp và tiếp xúc Taps; chuẩn bị đủ câu lệnh `.MEAS`. | Tính toán đúng các công thức chính; Stick diagram đúng nhưng chưa ghi chú đầy đủ các lớp; có lệnh `.MEAS`. | Tính toán còn sai lệch số học; Stick diagram vẽ sơ sài, thiếu tiếp xúc Taps. | Không chuẩn bị bài trước ở nhà hoặc sao chép bài của bạn. |
| **2. Đo đạc I-V & Phân tích VTC** | **25%** | Trích xuất chính xác họ đặc tuyến MOSFET ($V_{th}, \lambda$); Schematic chuẩn; Đo đạc VTC chính xác $V_M, V_{IL}, V_{IH}, NM_L, NM_H$. | Trích xuất đúng đặc tuyến; Schematic đúng; Đo được $V_M$ và lề nhiễu nhưng thao tác còn chậm. | Dựng được Schematic; Chạy được VTC nhưng đo đạc lề nhiễu chưa chính xác. | Không hoàn thành mô phỏng hoặc mạch báo lỗi không hội tụ (Convergence Error). |
| **3. Mô phỏng Transient & Lệnh .MEAS** | **20%** | Dạng sóng Transient chuẩn xác; Sử dụng thành thạo `.MEAS` tự động trích xuất đủ $t_r, t_f, t_{pHL}, t_{pLH}$ ở 3 mức tải; Đóng gói Icon chuẩn. | Đo được các thông số trễ với `.MEAS`; Tạo được Icon nhưng chưa chuẩn hóa vị trí chân. | Đo trễ bằng con trỏ thủ công do chưa chạy được lệnh `.MEAS`; Icon vẽ sơ sài. | Không đo được thông số trễ hoặc không tạo được Icon View. |
| **4. Physical Layout, DRC & LVS** | **25%** | Layout gọn gàng, tối ưu diện tích; Kiểm tra DRC đạt 0 lỗi; Đối chiếu LVS báo MATCH 100% độc lập tại bàn. | Layout đúng chuẩn; DRC đạt 0 lỗi; LVS match sau 1 lần hướng dẫn sửa lỗi nhãn port. | Layout còn cồng kềnh, vi phạm một vài lỗi DRC nhưng tự sửa được; LVS match. | Vi phạm nhiều lỗi DRC nghiêm trọng; LVS không match; không hoàn thành layout. |
| **5. Trích xuất PEX & Biện luận Báo cáo** | **10%** | Trích xuất PEX thành công; Hoàn thành bảng đối chiếu 3 chiều; Trả lời sắc bén, chính xác các câu hỏi phân tích vật lý. | Trích xuất PEX thành công; Điền đủ bảng số liệu; Trả lời đúng các câu hỏi bản chất. | Trích xuất được PEX nhưng phần phân tích nguyên nhân sai lệch còn mơ hồ. | Không thực hiện được bước PEX hoặc nộp báo cáo để trống nhiều phần. |
