# THỰC HÀNH THIẾT KẾ VLSI — BÀI 8 (LAB 08)
# THIẾT KẾ Ô NHỚ BÁN DẪN TĨNH (6T SRAM CELL) VÀ MẠCH KHUẾCH ĐẠI CẢM NHẬN (VLSA)

---
**Bộ môn:** Điện tử – Viễn thông | **Khoa:** Điện – Điện tử  
**Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Thời lượng:** 135 phút thực hành tại phòng máy (kết hợp tự học Pre-lab & hoàn thiện Post-lab)  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07+), LTspice XVII / LTspice 2025  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5µm ($\lambda = 0.30\,\mu\text{m}$, $L_{min} = 0.60\,\mu\text{m}$, $V_{DD} = 5.0\,\text{V}$)  
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Phân tích 3 chế độ hoạt động của Ô nhớ 6T SRAM (`sram_6t_cell`):** Giải thích cơ chế giữ dữ liệu (Hold), đọc (Read với Bitline thả nổi có $C_{BL}$) và ghi đè (Write), xác định đúng vai trò từng transistor (Driver, Access, Load).
2. **Tính toán định cỡ tỉ số $CR$ và $PR$:** Giải phương trình cân bằng dòng bậc hai tính điện áp dâng $V_Q$ khi đọc và so sánh với ngưỡng lật $V_M$ của Inverter đối diện (thay vì đòi hỏi quá nghiêm $V_Q < V_{tn}$); tính tỉ số sức kéo khi ghi có xét hệ số độ linh động $K'_n / K'_p$.
3. **Vẽ Đường cong Bướm (Butterfly Curve) và đo Lề nhiễu tĩnh ($SNM$):** Dùng phép quét DC và phương pháp xoay trục $45^\circ$ để đo $SNM_{hold}$ và $SNM_{read}$ tại thùy nhỏ hơn của hai Inverter.
4. **Thiết kế và mô phỏng Mạch khuếch đại cảm nhận (VLSA):** Dựng sơ đồ `sense_amp_vlsa`, đo thời gian chốt $t_{latch}$ cho cả hai chiều lệch vi sai $\Delta V_{in} = \pm 150\,\text{mV}$, và so sánh tốc độ lẫn năng lượng giữa phương pháp đọc có VLSA với phương pháp đọc không VLSA (chờ Bitline tự xả xuống ngưỡng Inverter).

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

| Hạng mục | Chi tiết |
|---|---|
| **IP kế thừa từ các bài trước** | - Tế bào Inverter chuẩn `inv_x1` (Bài 1).<br>- Thư viện mô hình SPICE: `04 - Models_and_Libraries/C5_models.txt` (NMOS: `N`, PMOS: `P`). |
| **Sản phẩm bàn giao cuối buổi** | - Netlist & đồ thị Butterfly đo $SNM_{hold}$ và $SNM_{read}$ của `sram_6t_cell`.<br>- Kết quả mô phỏng Đọc tĩnh ($V_Q$), Đọc động ($\Delta V_{BL}(t)$ trên $C_{BL}=1\,\text{pF}$) và Ghi ($t_{write\_0}, t_{write\_1}$).<br>- Schematic `sense_amp_vlsa{sch}` và kết quả đo $t_{latch}$ ($\pm 150\,\text{mV}$) cùng bảng so sánh đọc có/không VLSA. |
| **Kế thừa cho các bài sau** | - Nền tảng thiết kế khối nhớ đệm / thanh ghi cho đề tài đồ án môn học (Lưu ý: Bài 8 là bài tự chọn/đồ án, không bắt buộc vẽ Layout trong giờ thực hành). |

---

## 3. CƠ SỞ LÝ THUYẾT NGẮN GỌN

### 3.1. Ô nhớ 6T SRAM và Ràng buộc Tỉ số $CR$, $PR$

Ô nhớ 6T SRAM gồm 2 Inverter ghép chéo ($M_{D1}/M_{L1}$ tạo nút $Q$, $M_{D2}/M_{L2}$ tạo nút $QB$) và 2 Access NMOS ($M_{AX1}$ nối $Q$ với $BL$, $M_{AX2}$ nối $QB$ với $BLB$) điều khiển bởi $WL$.

1. **Độ ổn định Đọc (Read Stability) và Cell Ratio ($CR$):**
   - Trong pha Đọc ($BL, BLB$ nạp trước $V_{DD}$ rồi thả nổi, bật $WL = V_{DD}$), phía lưu mức `'0'` ($Q=0\,\text{V}$) xuất hiện dòng từ $BL$ qua $M_{AX1}$ (vùng bão hòa) và $M_{D1}$ (vùng tuyến tính) xuống đất, làm điện áp nút $Q$ dâng lên một mức $V_Q$.
   - Với $CR = \frac{(W/L)_{driver}}{(W/L)_{access}}$ và đặt $u = V_{DD} - V_{tn}$, cân bằng dòng cho phương trình bậc hai chính xác:
     $$V_Q = u \left[ 1 - \sqrt{\frac{CR}{1 + CR}} \right] \qquad \left(\text{xấp xỉ bậc nhất: } V_Q \approx \frac{V_{DD} - V_{tn}}{2 \cdot CR}\right)$$
   - **Điều kiện chống lật đọc (Read Disturb):** Để không làm lật Inverter đối diện, điện áp $V_Q$ phải nhỏ hơn **ngưỡng chuyển mạch $V_M$ của Inverter đối diện** (có biên độ dự phòng an toàn), chứ không nhất thiết phải nhỏ hơn $V_{tn}$ (vì để $V_Q < 0.70\,\text{V}$ đòi hỏi $CR \ge 2.5 - 3.0$).

2. **Khả năng Ghi (Writability) và Pull-up Ratio ($PR$):**
   - Khi ghi `'0'` vào nút $Q$ đang lưu `'1'` ($BL=0\,\text{V}, WL=V_{DD}$), $M_{AX1}$ phải kéo nút $Q$ xuống dưới ngưỡng $V_M$ của Inverter đối diện chống lại dòng kéo lên của PMOS tải $M_{L1}$.
   - Tỉ số hình học $PR = \frac{(W/L)_{load}}{(W/L)_{access}}$. Tuy nhiên sức kéo thực tế phụ thuộc vào độ linh động $\frac{K'_n}{K'_p} \approx 3$, nên tỉ số dòng giữa Access NMOS và Load PMOS là $\frac{K'_n (W/L)_{access}}{K'_p (W/L)_{load}} = \frac{3}{PR}$.
   - *Ví dụ minh họa:* Nếu chọn $W_D = 12\lambda, W_{AX} = 4\lambda, W_L = 3\lambda$ ($L=2\lambda$), ta có $CR = 3.0$ và $PR = 0.75$ (tỉ số sức kéo Access/Load = $4\times$).

### 3.2. Lề Nhiễu Tĩnh (Static Noise Margin - SNM) & Phương pháp Xoay Trục $45^\circ$

- **Định nghĩa:** $SNM$ là độ dài cạnh hình vuông lớn nhất lọt vừa vào **thùy nhỏ hơn** của hai đường đặc tính truyền đạt VTC lồng nhau (Butterfly Curve) khi đảo trục $(x, f(x))$ và $(f(x), x)$.
- **Phương pháp đo trong LTspice bằng xoay trục $45^\circ$:**
  Đặt tọa độ xoay:
  $$u = \frac{V_{in} - V_{out}}{\sqrt{2}}, \qquad v = \frac{V_{in} + V_{out}}{\sqrt{2}}$$
  Trên đồ thị vẽ $v_1(u)$ của nửa 1 và $v_2(u)$ của nửa 2, độ dài cạnh hình vuông lớn nhất chính là $\max |v_1(u) - v_2(u)| / \sqrt{2}$. Khi đọc ($WL=V_{DD}$), đường VTC bị dịch làm $SNM_{read}$ giảm mạnh so với $SNM_{hold}$ ($WL=0$).

### 3.3. Mạch Khuếch Đại Cảm Nhận Chốt Điện Áp (VLSA)

Khi cột Bitline có điện dung lớn ($C_{BL} \approx 1\,\text{pF}$), việc chờ ô nhớ xả Bitline tới ngưỡng lật Inverter đọc sẽ rất chậm và tốn năng lượng. **VLSA (`sense_amp_vlsa`)** dùng cặp Inverter ghép chéo (`Mp1/Mp2` $12\lambda$, `Mn1/Mn2` $8\lambda$) nối qua transistor chân `Mn_tail` ($12\lambda$, cổng `saen`) và hai cổng truyền đầu vào `Mn_pass1/Mn_pass2` ($4\lambda$).
- Khi `saen = 0`: Hai nút `so, sob` được nạp/nhận chênh lệch nhỏ $\Delta V_{in} = \pm 150\,\text{mV}$ từ $BL, BLB$.
- Khi kích `saen = 5V`: Phản hồi dương khuếch đại chênh lệch $\Delta V_{in}$ lên toàn dải Rail-to-Rail với thời gian chốt xấp xỉ:
  $$t_{latch} \approx \frac{C_{node}}{g_m} \ln\left(\frac{\Delta V_{out}}{\Delta V_{in}}\right)$$

---

## 4. CÂU HỎI CHUẨN BỊ TRƯỚC KHI ĐẾN LỚP (PRE-LAB)

> [!IMPORTANT]
> Sinh viên phải hoàn thành phần tính toán dưới đây vào **Mục 7.2.a** trước khi vào phòng máy để phục vụ **Cổng kiểm tra Pre-lab (10 phút đầu giờ)**.

Cho bộ kích thước ô nhớ 6T SRAM trong công nghệ MOSIS C5N ($V_{DD}=5.0\,\text{V}, V_{tn0}=0.70\,\text{V}, |V_{tp0}|=0.80\,\text{V}, K'_n=120\,\mu\text{A/V}^2, K'_p=40\,\mu\text{A/V}^2, L=2\lambda$):  
**Driver $W_D = 8\lambda$ ($2.4\,\mu\text{m}$), Access $W_{AX} = 4\lambda$ ($1.2\,\mu\text{m}$), Load $W_L = 2\lambda$ ($0.6\,\mu\text{m}$)**. *(Lưu ý: $W_L=2\lambda$ chỉ dùng để mô phỏng SPICE; nếu vẽ Layout phải dùng $W_L \ge 3\lambda$ và tăng $L$ tương ứng để không vi phạm bề rộng Active tối thiểu).*

1. **Tính toán $CR$ và $V_Q$ khi đọc `'0'`:**
   - Tính $CR$. Tính $V_Q$ bằng **công thức chính xác bậc hai** (thử cả trường hợp bỏ qua và có xét body effect với $\gamma=0.53, 2\phi_F=0.65$) và so với công thức xấp xỉ bậc nhất $\frac{V_{DD}-V_{tn}}{2\cdot CR}$.
   - Tính ngưỡng chuyển mạch $V_M$ của Inverter đối diện ($W_D=8\lambda, W_L=2\lambda$) ở chế độ Hold. So sánh $V_Q$ vừa tính với $V_M$ và với $V_{tn}=0.70\,\text{V}$ để kết luận về độ an toàn đọc.
2. **Tính toán $PR$ và mức $Q$ khi ghi `'0'`:**
   - Tính $PR$ theo $W/L$ và tính tỉ số sức kéo thực tế Access/Load có xét $K'_n / K'_p$.
   - Tính điện áp cân bằng của nút $Q$ khi ghi `'0'` ($BL=0, WL=5\text{V}$, Access tuyến tính cân bằng với Load bão hòa) và so sánh với $V_M$.
3. **Phác thảo Butterfly Curve:** Vẽ phác thảo 2 đường VTC lồng nhau cho chế độ Hold và Read, đánh dấu vị trí **thùy nhỏ hơn** dùng để đo $SNM$.
4. **Ước lượng $t_{latch}$ cho VLSA:** Với $C_{node} = 20\,\text{fF}$, $\Delta V_{in} = 150\,\text{mV}$, $\Delta V_{out} = 4.5\,\text{V}$ và ước lượng $C/g_m \approx 25 - 50\,\text{ps}$, tính khoảng giá trị dự kiến cho $t_{latch}$.
5. **Viết khung Netlist ô 6T:** Dựa vào sơ đồ 6T, viết định nghĩa `.subckt sram_6t_cell bl blb wl q qb vdd gnd` với kích thước $8\lambda / 4\lambda / 2\lambda$.

---

## 5. KẾ HOẠCH PHÂN BỔ THỜI LƯỢNG IN-LAB (135 PHÚT)

| Phân đoạn | Nội dung thực hiện | Thời lượng |
| :--- | :--- | :---: |
| **Kiểm tra đầu giờ** | Cổng kiểm tra Pre-lab (tính $V_Q$ bậc hai, $V_M$, sức kéo ghi và $t_{latch}$) | 10 phút |
| **Ex8.1** | Mô phỏng DC vẽ Butterfly Curve và đo $SNM_{hold}, SNM_{read}$ bằng phép xoay trục $45^\circ$ | 30 phút |
| **Ex8.2** | Mô phỏng Đọc tĩnh ($V_Q$), Đọc động ($\Delta V_{BL}$ trên $C_{BL}=1\,\text{pF}$) và Ghi ($t_{write\_0}, t_{write\_1}$) | 25 phút |
| **Ex8.3** | Dựng Schematic `sense_amp_vlsa{sch}` trên Electric và đo $t_{latch}$ 2 chiều ($\pm 150\,\text{mV}$) | 35 phút |
| **Ex8.4** | So sánh đường đọc có VLSA vs đường đọc không VLSA (chờ xả $C_{BL}$ tới $V_{DD}/2$, đo năng lượng) | 25 phút |
| **Tổng kết** | Ghi nhận số liệu vào Phiếu báo cáo và ký nghiệm thu tại bàn | 10 phút |
| **Tổng cộng** | | **135 phút** |

*(Lưu ý: Theo lộ trình, Lab 8 là bài tự chọn/đồ án, không bắt buộc thực hiện Layout/PEX trong buổi 135 phút).*

---

## 6. NỘI DUNG THỰC HÀNH TẠI LỚP (IN-LAB)

### Ex8.1: Đo Lề Nhiễu Tĩnh ($SNM_{hold}$ và $SNM_{read}$) bằng Butterfly Curve (LTspice)

1. Sử dụng `.subckt sram_6t_cell` vừa viết ở Pre-lab, dựng 2 mạch tách nửa (mỗi mạch là 1 Inverter $8\lambda/2\lambda$ + 1 Access $4\lambda/2\lambda$ nối `bl = 5V`):
   - **Mạch Hold:** `wl = 0V`. Quét `.dc Vin 0 5.0 0.01`, thu được `V(out_hold)` theo `V(in)`.
   - **Mạch Read:** `wl = 5.0V` (`bl = 5.0V`). Thu được `V(out_read)` theo `V(in)`.
2. **Cách đo $SNM$ bằng xoay trục $45^\circ$ trong LTspice:**
   - Tạo 2 nguồn phụ thuộc (Behavioral Voltage Source `BV`) để xuất trực tiếp tọa độ xoay $u, v$:
     * Cách 1 (đồ thị trực tiếp): Đổi trục hoành của LTspice thành `(V(in) - V(out_hold))/sqrt(2)` và vẽ hai đường `(V(in) + V(out_hold))/sqrt(2)` cùng đường đối xứng (từ nửa Inverter thứ 2 có đầu vào là `V(in)` quét ngược hoặc dùng 2 bản sao: một bản `x = V(in), y = V(out)` và một bản `x = V(out2), y = V(in)`).
     * Đo khoảng cách cực đại theo trục tung $v$ giữa hai đường trong thùy nhỏ hơn rồi chia cho $\sqrt{2}$ để nhận $SNM_{hold}$ và $SNM_{read}$.

- **Sản phẩm Ex8.1:** Đồ thị Butterfly Curve (hoặc đồ thị xoay $45^\circ$) và giá trị đo $SNM_{hold}, SNM_{read}$.

---

### Ex8.2: Mô phỏng Đọc tĩnh, Đọc động ($C_{BL}=1\,\text{pF}$) và Ghi dữ liệu (LTspice)

Chạy mô phỏng với bước tích phân chặt `.tran 0 50n 0 10p`, khởi tạo trạng thái ban đầu của ô nhớ bằng `.ic V(q)=0 V(qb)=5.0`.

1. **Ca A — Đọc tĩnh kiểm tra $V_Q$:**
   - Cố định `bl = 5.0V`, `blb = 5.0V`, bật xung `wl = 5.0V` trong $5\,\text{ns}$. Đo điện áp dâng cực đại `V_Q_bump = MAX V(q)` và đối chiếu với giá trị Pre-lab.
2. **Ca B — Đọc động kiểm tra $\Delta V_{BL}(t)$:**
   - Gắn hai tụ Bitline thực tế: `C_bl bl 0 1pF` và `C_blb blb 0 1pF`.
   - Khởi tạo trước khi đọc: `.ic V(bl)=5.0 V(blb)=5.0 V(q)=0 V(qb)=5.0` (hai cột thả nổi).
   - Kích `wl` lên $5.0\,\text{V}$ trong $4\,\text{ns}$ (ví dụ từ $t=10\text{ns}$ đến $14\text{ns}$). Đo độ lệch vi sai $\Delta V_{BL} = V(blb) - V(bl)$ tại $t = 12\,\text{ns}$ và $14\,\text{ns}$.
3. **Ca C — Ghi dữ liệu ($t_{write\_1}$ và $t_{write\_0}$):**
   - Sau khi ô đang giữ `Q = 0, QB = 5V`, đặt `bl = 5V, blb = 0V` và kích `wl` lên $5\text{V}$ tại $t = 20\,\text{ns}$ để ghi `'1'`. Đo $t_{write\_1}$ từ `V(wl)=2.5V` sườn lên đến `V(q)=2.5V` sườn lên.
   - Tương tự, đặt `bl = 0V, blb = 5V` và kích `wl` tại $t = 35\,\text{ns}$ để ghi `'0'`. Đo $t_{write\_0}$ từ `V(wl)=2.5V` sườn lên đến `V(q)=2.5V` sườn xuống.

- **Sản phẩm Ex8.2:** Đồ thị dạng sóng cho 3 ca đo và các giá trị $V_{Q,bump}$, $\Delta V_{BL}$, $t_{write\_1}, t_{write\_0}$.

---

### Ex8.3: Thiết kế Schematic & Mô phỏng VLSA (`sense_amp_vlsa`)

1. Trên Electric VLSI, tạo Cell `sense_amp_vlsa{sch}` theo cấu trúc chuẩn:
   - Cặp Inverter ghép chéo: `Mp1, Mp2` ($W=12\lambda, L=2\lambda$), `Mn1, Mn2` ($W=8\lambda, L=2\lambda$) chung nút nguồn `n_tail`.
   - Transistor chân kích hoạt: `Mn_tail` ($W=12\lambda, L=2\lambda$, Gate nối `saen`, Source nối `gnd`).
   - 2 transistor truyền đầu vào: `Mn_pass1` (nối `so` với nguồn/cổng `bl`), `Mn_pass2` (nối `sob` với `blb`), kích thước $W=4\lambda, L=2\lambda$.
   - Tạo Export: `bl, blb, saen` (Input), `so, sob` (Output), `vdd, gnd`. Kiểm tra `F5` đạt 0 lỗi.
2. Xuất Netlist sang LTspice, gắn tải `C_so so 0 20fF`, `C_sob sob 0 20fF`, chạy `.tran 0 5n 0 10p`:
   - **Chiều 1 ($\Delta V_{in} = +150\,\text{mV}$):** Đặt `bl = 5.00V, blb = 4.85V`, `.ic V(so)=5.00 V(sob)=4.85`, kích `Vsaen` lên $5\text{V}$ tại $t = 2.0\,\text{ns}$. Đo $t_{latch,1}$ từ `V(saen)=2.5V` đến `V(sob)=0.5V` (hoặc `2.5V`).
   - **Chiều 2 ($\Delta V_{in} = -150\,\text{mV}$):** Đảo lại `bl = 4.85V, blb = 5.00V`, `.ic V(so)=4.85 V(sob)=5.00`, đo $t_{latch,2}$ cho `V(so)`.

- **Sản phẩm Ex8.3:** Schematic `sense_amp_vlsa{sch}` và số đo $t_{latch}$ cho cả hai chiều.

---

### Ex8.4: So sánh Đọc có VLSA vs Đọc không VLSA (LTspice)

1. Dùng mạch ô nhớ 6T nối vào Bitline `C_bl = 1pF, C_blb = 1pF` (đọc động như Ex8.2 Ca B):
   - **Phương pháp 1 (Không VLSA):** Nối `bl` vào một Inverter đọc chuẩn `inv_x1`, bật `wl` và đo thời gian `t_no_sa` từ lúc `wl=2.5V` đến lúc `V(bl)` tụt xuống ngưỡng $V_{DD}/2 = 2.5\,\text{V}$ (Inverter đọc lật trạng thái). Đo năng lượng tiêu thụ từ nguồn bằng `.meas INTEG`.
   - **Phương pháp 2 (Có VLSA):** Bật `wl` để tạo $\Delta V_{BL} = 150\,\text{mV}$, sau đó kích `saen` bật VLSA. Tổng thời gian đọc `t_with_sa = t(dV=150mV) + t_latch`.
2. Tính tỉ số tăng tốc và mức tiết kiệm năng lượng (xét cả năng lượng nạp lại $C_{BL}$ ở chu kỳ kế tiếp: $\Delta E = C_{BL} V_{DD} \Delta V_{BL}$).

- **Sản phẩm Ex8.4:** Bảng so sánh định lượng giữa đọc có VLSA và đọc không VLSA.

---

## 7. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (POST-LAB)

### 7.1. Phân tích Post-lab & Nội dung Tùy chọn
1. Hoàn thiện bảng đối sánh năng lượng và thời gian từ Ex8.4, tính năng lượng nạp lại Bitline $E = C_{BL} \cdot V_{DD} \cdot \Delta V_{BL}$ cho cả hai phương pháp.
2. *(Tùy chọn nâng cao - Không bắt buộc):* Nếu thiết kế Layout `sram_6t_cell{lay}`, lưu ý đổi Load PMOS thành $W_L \ge 3\lambda$ (và điều chỉnh $L_L$ để giữ $PR$) nhằm thỏa mãn luật bề rộng Active tối thiểu DRC.

### 7.2. Phiếu báo cáo điền khuyết (Nộp kèm file mô phỏng)

```
========================================================================================
                          BÁO CÁO THỰC HÀNH: BÀI 8
        THIẾT KẾ Ô NHỚ BÁN DẪN TĨNH (6T SRAM) VÀ MẠCH KHUẾCH ĐẠI CẢM NHẬN (VLSA)
Họ và Tên: ..................................................... MSSV: .................
Lớp: ....................................... Nhóm/Bàn: ......... Ngày: .................
Chữ ký Giảng viên / Điểm nghiệm thu tại bàn: ............................................
========================================================================================
```

#### a. Phần Chuẩn bị (Pre-lab)
1. **Tính toán đọc ổn định ($CR = 2.0$):**
   - $V_Q$ (công thức chính xác không body / có body): ............ V / ............ V (xấp xỉ bậc nhất: ............ V).
   - Ngưỡng $V_M$ của Inverter đối diện ($8\lambda/2\lambda$): ............ V $\implies$ Kết luận an toàn đọc: ....................
2. **Tính toán ghi ($PR = 0.5$):**
   - Tỉ số sức kéo Access/Load có xét $K'_n/K'_p$: ............ lần.
   - Điện áp cân bằng nút $Q$ khi ghi `'0'`: ............ V.
3. **Ước lượng $t_{latch}$ cho VLSA:** Khoảng dự kiến: ............ ps.

#### b. Kết quả Đo đạc Thực hành (In-lab & Post-lab)
1. **Ex8.1 — Lề nhiễu tĩnh ($SNM$):**

| Chế độ hoạt động | Dự đoán định tính | Đo $SNM$ (thùy nhỏ hơn) | Tỉ lệ $\text{ pct} V_{DD}$ |
| :--- | :---: | :---: | :---: |
| **Chế độ Giữ ($SNM_{hold}$, $WL=0$)** | Lớn nhất | ................ V | ................ % |
| **Chế độ Đọc ($SNM_{read}$, $WL=5\text{V}$)** | Giảm mạnh | ................ V | ................ % |

2. **Ex8.2 — Đọc tĩnh, Đọc động ($C_{BL}=1\,\text{pF}$) và Ghi:**

| Thông số đo kiểm | Giá trị đo LTspice | Điều kiện đo |
| :--- | :---: | :--- |
| Điện áp dâng đọc tĩnh $V_{Q,bump}$ | ................ V | `bl = blb = 5V` cố định |
| Độ lệch vi sai động $\Delta V_{BL}$ | ................ mV (tại `12n`) / ................ mV (tại `14n`) | `C_bl = C_blb = 1pF` thả nổi |
| Thời gian ghi `'1'` ($t_{write\_1}$) | ................ ps | Từ `wl=2.5V` đến `q=2.5V` |
| Thời gian ghi `'0'` ($t_{write\_0}$) | ................ ps | Từ `wl=2.5V` đến `q=2.5V` |

3. **Ex8.3 & Ex8.4 — Kiểm chứng VLSA & Đối sánh đường đọc:**
   - $t_{latch}$ ($\Delta V_{in}=+150\,\text{mV}$): ............ ps | $t_{latch}$ ($\Delta V_{in}=-150\,\text{mV}$): ............ ps.

| Phương pháp đọc ($C_{BL} = 1\,\text{pF}$) | Thời gian đọc tổng | Độ sụt áp Bitline $\Delta V_{BL}$ | Năng lượng nạp lại Bitline ($C_{BL} V_{DD} \Delta V_{BL}$) |
| :--- | :---: | :---: | :---: |
| **Không VLSA** (xả tới $V_{DD}/2 = 2.5\text{V}$) | ................ ns | $2.50\,\text{V}$ | ................ pJ |
| **Có VLSA** (kích tại $\Delta V_{BL}=150\,\text{mV}$) | ................ ns | $0.15\,\text{V}$ | ................ pJ |

#### c. Câu hỏi Thảo luận Chuyên sâu
1. Tại sao trong thiết kế ô nhớ 6T SRAM ($CR = 2.0$), công thức bậc nhất cho $V_Q \approx 1.075\,\text{V} > V_{tn} = 0.70\,\text{V}$ nhưng ô nhớ vẫn hoạt động ổn định khi đọc? Tiêu chí vật lý đúng để đánh giá Read Disturb là gì?
2. Tại sao với $PR = 0.5$ theo tỉ số $W/L$, Access NMOS ($4\lambda$) lại kéo thắng dễ dàng Load PMOS ($2\lambda$) để ghi dữ liệu `'0'`?
3. Nếu quá trình chế tạo làm hai transistor `Mn1, Mn2` của VLSA bị lệch điện áp ngưỡng (Input Offset) $\Delta V_{os} = 100\,\text{mV}$, điều gì sẽ xảy ra khi cố đọc ở $\Delta V_{BL} = 80\,\text{mV}$?

---

## 8. BẢNG KIỂM CHỨNG VÀ ĐỐI CHUẨN KỸ THUẬT (BENCHMARK)

| Thông số kiểm chứng | Dải giá trị kỳ vọng (MOSIS C5N) | Điều kiện kiểm tra |
| :--- | :---: | :--- |
| **Đọc tĩnh $V_Q$ ($CR = 2.0$)** | $\approx 0.72 - 0.79\,\text{V}$ (nhỏ hơn $V_M \approx 1.49\,\text{V}$) | `bl = blb = 5V`, `wl = 5V` |
| **Mức $Q$ khi ghi `'0'`** | $\approx 0.35\,\text{V}$ | `bl = 0V`, `wl = 5V` |
| **Lề nhiễu tĩnh ($SNM_{hold}$ / $SNM_{read}$)** | $SNM_{hold} \approx 1.25 - 1.35\,\text{V}$; $SNM_{read} \approx 0.30 - 0.40\,\text{V}$ | Butterfly xoay $45^\circ$, thùy nhỏ hơn |
| **VLSA $t_{latch}$ ($\pm 150\,\text{mV}$)** | Khoảng $70 - 200\,\text{ps}$ (tùy mô hình Level 3) | $C_{so} = C_{sob} = 20\,\text{fF}$ |

---

## 9. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP

| Hiện tượng lỗi | Nguyên nhân gốc rễ | Cách khắc phục nhanh |
| :--- | :--- | :--- |
| **Ô nhớ tự rơi về trạng thái lơ lửng (~1.5V) lúc bắt đầu `.tran`** | Quên đặt điều kiện khởi tạo `.ic V(q)=0 V(qb)=5.0`, làm điểm làm việc DC rơi vào trạng thái cân bằng không bền. | Thêm `.ic V(q)=0 V(qb)=5.0` (và `.ic V(bl)=5.0 V(blb)=5.0` cho đọc động). |
| **Đo $\Delta V_{BL}$ bằng `0.000 V` trong Ex8.2** | Để `bl` và `blb` nối trực tiếp với nguồn áp lý tưởng `5.0V` thay vì tụ `1pF` thả nổi. | Chuyển sang tụ `C_bl bl 0 1pF` và dùng `.ic V(bl)=5.0` cho ca đọc động. |
| **Đo `SNM_read` ra quá lớn hoặc không đúng thùy** | Xác định nhầm khoảng `u` hoặc lấy hiệu hai đường bên ngoài thùy nhỏ hơn trên đồ thị xoay $45^\circ$. | Kiểm tra lại đồ thị: lấy khoảng cách cực đại theo trục $v$ bên trong vùng kín của **thùy nhỏ hơn**. |

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

| Tiêu chí đánh giá | Trọng số | Xuất sắc (8.5 – 10) | Khá (7.0 – 8.4) | Đạt (5.0 – 6.9) | Không đạt (< 5.0) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Chuẩn bị Pre-lab** | **20%** | Giải đúng $V_Q$ bậc hai ($\approx 0.73 - 0.79\,\text{V}$), đúng $V_M \approx 1.49\,\text{V}$, tính đúng tỉ số ghi $6\times$, $t_{latch}$ và viết được Netlist 6T. | Tính đúng $V_Q$ và $V_M$, còn sai sót nhỏ ở cân bằng ghi hoặc ước lượng $t_{latch}$. | Chỉ dùng công thức bậc nhất $1.075\,\text{V}$ và kết luận sai về an toàn đọc. | Không làm Pre-lab hoặc sao chép. |
| **2. Butterfly & SNM (Ex8.1)** | **25%** | Vẽ đúng Butterfly Hold và Read, áp dụng đúng phép xoay $45^\circ$ đo được $SNM_{hold}$ và $SNM_{read}$ tại thùy nhỏ hơn. | Vẽ đúng Butterfly và đo được $SNM_{hold}$, còn lúng túng khi trích xuất $SNM_{read}$. | Chỉ vẽ được 1 nửa VTC (chưa lồng 2 đường thành Butterfly). | Không hoàn thành Ex8.1. |
| **3. Đọc tĩnh, Đọc động & Ghi (Ex8.2)** | **25%** | Đo đủ 3 ca ($V_{Q,bump}$, $\Delta V_{BL}$ trên $C_{BL}=1\,\text{pF}$, $t_{write\_0}/t_{write\_1}$) với khởi tạo `.ic` chuẩn. | Đo được đọc tĩnh và ghi, thiếu hoặc nhầm ca đọc động trên tụ $C_{BL}$. | Quên `.ic` làm ô nhớ khởi tạo sai trạng thái. | Không hoàn thành Ex8.2. |
| **4. VLSA & Đối sánh đọc (Ex8.3–8.4)** | **20%** | Dựng đúng `sense_amp_vlsa`, đo đủ $t_{latch}$ cả 2 chiều ($\pm 150\,\text{mV}$) và hoàn thành bảng đối sánh tốc độ/năng lượng có/không VLSA. | Đo được VLSA 1 chiều và đối sánh được thời gian đọc với không VLSA. | Chỉ mô phỏng được VLSA, thiếu phép so sánh đường đọc không VLSA. | Không hoàn thành VLSA. |
| **5. Báo cáo & Thảo luận** | **10%** | Báo cáo đầy đủ số liệu khớp `.log`, trả lời chính xác 3 câu hỏi thảo luận (Read Disturb, PR, Offset). | Báo cáo đầy đủ, trả lời được 2/3 câu hỏi thảo luận. | Báo cáo thiếu số liệu hoặc trả lời câu hỏi chưa rõ ràng. | Nộp thiếu báo cáo hoặc số liệu không khớp mô phỏng. |

---

## 11. TÀI LIỆU THAM KHẢO

1. N. H. E. Weste & D. M. Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th Ed., Addison-Wesley (Chương 12: Memory Subsystems — 6T SRAM & Sense Amplifiers).
2. J. M. Rabaey, A. Chandrakasan & B. Nikolic, *Digital Integrated Circuits: A Design Perspective*, 2nd Ed., Prentice Hall (Chương 12: Designing Memory and Array Structures).
3. E. Seevinck, F. J. List, & J. Lohstroh, *"Static-Noise Margin Analysis of MOS SRAM Cells"*, IEEE JSSC, Vol. SC-22, No. 5, 1987 (Phương pháp xoay trục $45^\circ$ đo SNM).
4. Thư viện mô hình SPICE chuẩn phòng thí nghiệm: `04 - Models_and_Libraries/C5_models.txt`.
