# THỰC HÀNH THIẾT KẾ VLSI — BÀI 5 (LAB 05)
# MẠCH TUẦN TỰ MỨC TRANSISTOR: D-LATCH VÀ D-FLIP-FLOP MASTER-SLAVE

---
**Bộ môn:** Điện tử – Viễn thông | **Khoa:** Điện – Điện tử  
**Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Thời lượng:** 135 phút thực hành tại phòng máy (kết hợp tự học Pre-lab & hoàn thiện Post-lab)  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07+), LTspice XVII / LTspice 2025  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5µm ($\lambda = 0.30\,\mu\text{m}$, $L_{min} = 0.60\,\mu\text{m}$, $V_{DD} = 5.0\,\text{V}$)  
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Phân biệt và kiểm chứng cơ chế nhạy mức (Level-Sensitive) vs nhạy sườn (Edge-Triggered):** Đo kiểm thực nghiệm pha trong suốt (Transparent) và pha chốt giữ (Hold) của mạch chốt `dlatch_x1` so với hoạt động lấy mẫu theo sườn dương của mạch lật `dff_ms_x1`.
2. **Thiết kế D-Latch dùng Cổng truyền (`dlatch_x1`):** Xây dựng sơ đồ nguyên lý gồm 2 cổng truyền ($TG_1, TG_2$) và 3 Inverter ($I_1, I_2, I_3$), giải thích vai trò giữ trạng thái của $I_3$ khi có khóa cách ly $TG_2$ và phân tích điều kiện định cỡ nếu bỏ $TG_2$.
3. **Thiết kế Mạch lật D-Flip-Flop Master-Slave (`dff_ms_x1`):** Ghép nối phân cấp 2 tầng D-Latch đối pha ($22$ transistor), phân tích nguyên nhân tồn tại khoảng chồng dẫn ngắn do trễ $\overline{CLK}$ và mối liên hệ trực tiếp với thời gian giữ $t_{hold}$.
4. **Thực hiện Quét Đặc tính Định thời (Timing Characterization) trên LTspice:**
   - Khởi tạo trạng thái bằng `.ic` để đo chính xác $t_{c-q,LH}$ và $t_{c-q,HL}$.
   - Quét độ lệch pha $\Delta t$ (tính giữa hai mốc $50$–$50$) cho cả sườn lên và sườn xuống của $D$ để xác định $t_{setup}$ theo quy ước đẩy trễ 10% (10% push-out).
   - Quét mốc $D$ quanh sườn $CLK$ từ $-50\,\text{ps}$ đến $+100\,\text{ps}$ (bước $5\,\text{ps}$) bằng lệnh `.meas FIND` để xác định ngưỡng và dấu của $t_{hold}$, đồng thời quan sát hiện tượng bất ổn định (Metastability).
5. **Đóng gói IP Tế bào chuẩn:** Tạo Cell Icon `dlatch_x1{ic}` và `dff_ms_x1{ic}` phục vụ khối thanh ghi tích lũy của **Bài 10 (Capstone ALU 4-bit)**.

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

| Hạng mục | Chi tiết |
|---|---|
| **IP kế thừa từ các bài trước** | - Tế bào Inverter chuẩn `inv_x1` (Bài 1) và số đo trễ $t_{pd,inv}$ của sinh viên.<br>- Tế bào Cổng truyền `tg_gate` (Bài 4 — hoặc sử dụng tệp `tg_gate` dựng sẵn trong gói thư viện Lab 5 nếu không thực hành Bài 4 độc lập) và số đo trễ $t_{pd,tg}$.<br>- Thư viện mô hình SPICE: `04 - Models_and_Libraries/C5_models.txt` (NMOS: `N`, PMOS: `P`). |
| **Sản phẩm bàn giao cuối buổi** | - Tế bào D-Latch `dlatch_x1{sch}` và `dlatch_x1{ic}` ($10$ transistor).<br>- Tế bào D-Flip-Flop Master-Slave `dff_ms_x1{sch}` và `dff_ms_x1{ic}` ($22$ transistor).<br>- Tệp mô phỏng LTspice (.raw/.log) đo $t_{pd(D\to Q)}$ của Latch; $t_{c-q}$ (LH, HL), đồ thị quét $t_{setup}$ (sườn lên/xuống), ngưỡng $t_{hold}$ và dạng sóng Metastability của DFF. |
| **Kế thừa cho các bài sau** | - `dff_ms_x1{ic}` và bảng thông số định thời ($t_{c-q}, t_{setup}, t_{hold}$) dùng để tính ngân sách thời gian $T_{clk}$ cho **Bài 10 (Capstone ALU 4-bit)**. |

---

## 3. CƠ SỞ LÝ THUYẾT NGẮN GỌN

### 3.1. Kiến trúc Mạch chốt D dùng Cổng truyền (`dlatch_x1`)

Mạch chốt D tĩnh gồm 2 cổng truyền ($TG_1, TG_2$) và 3 Inverter ($I_1, I_2, I_3$), tổng cộng **10 Transistor**:
- **Cổng truyền ngõ vào ($TG_1$):** Nối ngõ vào $D$ với nút lưu trữ $X$. NMOS nhận `clk`, PMOS nhận `clk_n`.
- **Cặp Inverter thuận ($I_1, I_2$):** $I_1$ đảo nút $X$ thành $\bar{Q}$; $I_2$ đảo $\bar{Q}$ thành ngõ ra $Q$.
- **Vòng phản hồi giữ trạng thái ($I_3, TG_2$):** Ngõ ra $I_1$ ($\bar{Q}$) đi qua Inverter hồi tiếp $I_3$ và cổng truyền $TG_2$ (NMOS nhận `clk_n`, PMOS nhận `clk`) quay về nút $X$.

#### Nguyên lý hoạt động & Vai trò của $I_3$:
- **Pha trong suốt (`clk = 1`, `clk_n = 0`):** $TG_1$ dẫn, $TG_2$ ngắt. Dữ liệu từ $D$ truyền qua $TG_1 \to I_1 \to I_2 \to Q$ với độ trễ $t_{pd(D \to Q)} = t_{pd,TG1} + t_{pd,I1} + t_{pd,I2}$.
- **Pha chốt giữ (`clk = 0`, `clk_n = 1`):** $TG_1$ ngắt, $TG_2$ dẫn. Vòng phản hồi kín $I_1 - I_3 - TG_2$ giữ mức logic tại nút $X$ chống lại dòng rò và nhiễu (lưu ý: khi $CLK$ chuyển trạng thái, nút $X$ có thể bị nhiễu nhẹ do chia sẻ điện tích và xuyên dẫn xung nhịp — clock feedthrough).
- **Lựa chọn kích thước cho $I_3$:** Vì mạch đã có khóa cách ly $TG_2$ mắc nối tiếp với $I_3$, ở trạng thái xác lập $TG_1$ và $TG_2$ không dẫn đồng thời (chỉ có khoảng chồng dẫn ngắn cỡ $t_{pd,inv}$ do trễ $\overline{CLK}$). Do đó $I_3$ **không cần phải thắng $TG_1$** và có thể lấy kích thước tối thiểu ($W_n = 4\lambda, W_p = 4\lambda, L = 2\lambda$) chỉ để giữ trạng thái nút $X$. *(Ngược lại, nếu thiết kế không dùng $TG_2$ — mạch chốt kiểu Inverter yếu — thì bắt buộc $R_{TG1} \ll R_{out,I3}$, khi đó $I_3$ phải tăng chiều dài kênh $L$ lên $4\lambda$ hoặc giảm $W$ để tránh tranh chấp làm hỏng mức ghi).*

### 3.2. Kiến trúc Mạch lật D-Flip-Flop Master-Slave (`dff_ms_x1`)

Để giảm thiểu hiện tượng chạy đua dữ liệu (Race Condition) của Latch nhạy mức, ta ghép 2 D-Latch nối tiếp điều khiển bởi xung nhịp nghịch đảo (`clk` và `clk_n` tạo bởi `X_CLK_INV`), tổng cộng **22 Transistor**:
- **Master Latch:** Nhận `clk_n` vào chân mở ($TG_{M1}$). Khi `clk = 0` (`clk_n = 1`), Master mở đón $D$ vào nút trung gian $Q_M$; Slave đóng giữ $Q$ cũ.
- **Sườn lên của xung nhịp (`clk`: $0 \to 1$):** Master chuyển sang đóng (khóa $Q_M$), Slave chuyển sang mở (đưa $Q_M$ ra $Q$).
- **Hiện tượng chồng dẫn do trễ $\overline{CLK}$:** Vì `clk_n` đi qua `X_CLK_INV` bị trễ một khoảng $\approx t_{pd,inv}$ so với `clk`, nên ngay sau sườn lên của `clk`, PMOS của $TG_{M1}$ (nhận `clk`) ngắt ngay nhưng NMOS của $TG_{M1}$ (nhận `clk_n`) vẫn còn dẫn trong khoảng ngắn $\Delta t \approx t_{pd,inv}$, trong khi NMOS của Slave $TG_{S1}$ (nhận `clk`) đã mở. Do đó, cấu trúc Master-Slave chỉ loại bỏ race khi $\overline{CLK}$ đến đủ gần $CLK$; phần chồng dẫn còn lại chính là nguyên nhân vật lý sinh ra yêu cầu thời gian giữ $t_{hold}$.

### 3.3. Thông số Định thời ($t_{setup}, t_{hold}, t_{c-q}$) và Metastability

```
                     ◄── t_setup ──►◄── t_hold ──►
   D:    ───────────────[  D ổn định quanh sườn  ]────────────────
                                   │
   CLK:  ──────────────────────────┌──────────────────────────────
                                   │       ◄── t_c-q ──►
   Q:    ──────────────────────────┴───────────────────XXXXXXXX───
                                   │                   ▲
                            Sườn lên 50% CLK      Q đổi mức 50%
```

1. **Thời gian thiết lập ($t_{setup}$):** Khoảng thời gian tối thiểu $D$ phải ổn định **trước** sườn lên $50$ của $CLK$ để điện tích nạp/xả qua $TG_{M1}$ kịp lật trạng thái nút $X_M$ qua $I_{M1}$:
   $$t_{setup} \approx t_{pd,TG(M1)} + t_{pd,I(M1)}$$
   - **Quy ước đo $t_{setup}$ (10% Push-out Rule):** Khi giảm dần $\Delta t = t_{CLK,50} - t_{D,50}$, trễ $t_{c-q}$ tăng vọt lên (hiệu ứng đẩy trễ — push-out). Theo quy ước thường dùng trong đặc trưng hóa thư viện, $t_{setup}$ là giá trị $\Delta t$ tại điểm $t_{c-q}(\Delta t) = 1.10 \times t_{c-q,nominal}$ (một số hãng dùng ngưỡng 5%).
2. **Thời gian giữ ($t_{hold}$):** Khoảng thời gian tối thiểu $D$ phải giữ nguyên **sau** sườn lên $50$ của $CLK$ cho tới khi $TG_{M1}$ đóng hẳn:
   $$t_{hold} \approx t_{pd,INV(CLK)}$$
   - Lưu ý: Khác với $t_{setup}$, **không áp dụng quy tắc đẩy trễ 10% cho $t_{hold}$**. Hold là điều kiện nhị phân (ngõ ra $Q$ giữ đúng giá trị cũ hay bị dữ liệu mới ghi đè sai).
3. **Trễ từ Xung nhịp đến Ngõ ra ($t_{c-q}$):** Khoảng thời gian từ mốc $50$ sườn lên $CLK$ tới mốc $50$ ngõ ra $Q$. Đường truyền đầy đủ đi qua bộ đảo xung nhịp, cổng truyền Slave và cặp Inverter ngõ ra ($I_{S1}, I_{S2}$):
   $$t_{c-q} \approx t_{pd,INV(CLK)} + t_{pd,TG(S1)} + t_{pd,I(S1)} + t_{pd,I(S2)}$$
4. **Hiện tượng Bất ổn định (Metastability):** Nếu $D$ chuyển mức quá sát trong cửa sổ setup-hold, nút $X_M$ rơi vào trạng thái cân bằng lơ lửng quanh $V_M \approx V_{DD}/2$. Vòng phản hồi cần thời gian giải quyết (resolve time) rất dài và không bị chặn trên về mặt lý thuyết trước khi rơi về 0 hoặc 1.
5. **Ràng buộc chu kỳ xung nhịp hệ thống:**
   $$T_{clk} \ge t_{c-q} + t_{comb,max} + t_{setup} + t_{skew} \implies T_{min,no-logic} = t_{c-q} + t_{setup}$$

---

## 4. CÂU HỎI CHUẨN BỊ TRƯỚC KHI ĐẾN LỚP (PRE-LAB)

> [!IMPORTANT]
> Sinh viên phải hoàn thành phần tính toán và bảng chân trị vào **Mục 7.2.a** trước khi vào phòng máy để phục vụ **Cổng kiểm tra Pre-lab (10 phút đầu giờ)**.

1. **Bảng chân trị Master-Slave DFF:**
   - Tự hoàn thiện bảng trạng thái hoạt động của Master Latch, Slave Latch và ngõ ra $Q_{next}$ tương ứng với các trạng thái $CLK = 0, CLK = 1$, và sườn lên $CLK \uparrow$.
2. **Ước lượng các thông số định thời từ số đo thực tế của bạn:**
   - Sử dụng giá trị trễ $t_{pd,inv}$ (đo được ở **Bài 1**) và $t_{pd,tg}$ (đo được ở **Bài 4**, hoặc giá trị tham chiếu do giảng viên cấp) để tính dự đoán:
     * Trễ D-Latch trong suốt $t_{pd(D \to Q)}$.
     * $t_{setup}$, $t_{hold}$, $t_{c-q}$ (theo đúng đường dẫn đầy đủ qua $I_1, I_2$) và chu kỳ nhỏ nhất $T_{min,no-logic}$ của DFF.
3. **Phân tích định cỡ Inverter phản hồi $I_3$ (Bài toán tư duy):**
   - Giả sử ta **bỏ cổng truyền $TG_2$** (chỉ nối thẳng ngõ ra $I_3$ vào nút $X$ để tạo mạch chốt kiểu "weak feedback inverter"). Biết $R_{TG1} \approx 1.19\,\text{k}\Omega$, ngưỡng chuyển $I_1$ là $V_M \approx 2.45\,\text{V}$, $K'_n = 120\,\mu\text{A/V}^2, V_{DD} = 5.0\,\text{V}, V_{th0,n} = 0.70\,\text{V}$.
   - Hãy dùng công thức chia điện áp tính điện áp $V_X$ khi $TG_1$ ghi mức '1' đè lên $I_3$ (đang giữ '0') với 2 cấu hình của $I_3$: **(a)** $W_n = 4\lambda, L_n = 2\lambda$ và **(b)** $W_n = 4\lambda, L_n = 4\lambda$. Cấu hình nào đủ yếu để ghi dữ liệu thành công?
4. **Dự đoán ảnh hưởng của bộ đảo xung nhịp:**
   - Nếu thay `X_CLK_INV` từ kích thước `inv_x1` sang `inv_x2` (công suất lái gấp đôi, trễ giảm đi), thời gian giữ $t_{hold}$ của DFF sẽ tăng hay giảm? Giải thích ngắn gọn.

---

## 5. KẾ HOẠCH PHÂN BỔ THỜI LƯỢNG IN-LAB (135 PHÚT)

| Phân đoạn | Nội dung thực hiện | Thời lượng |
| :--- | :--- | :---: |
| **Kiểm tra đầu giờ** | Cổng kiểm tra Pre-lab (bảng chân trị, tính chia áp $I_3$ và dự đoán định thời) | 10 phút |
| **Ex5.1** | Thiết kế Schematic `dlatch_x1{sch}` (dùng `tg_gate` và `inv_x1`), kiểm tra `F5` | 15 phút |
| **Ex5.2** | Mô phỏng D-Latch trên LTspice (xác nhận pha trong suốt, pha chốt giữ và đo $t_{pd(D \to Q)}$) | 20 phút |
| **Ex5.3** | Thiết kế Schematic `dff_ms_x1{sch}` ghép phân cấp từ 2 D-Latch và `X_CLK_INV` | 15 phút |
| **Ex5.4** | Đo đặc tính định thời DFF: khởi tạo `.ic`, đo $t_{c-q}$ (LH/HL), quét $t_{setup}$ (10% push-out), quét $t_{hold}$ và quan sát Metastability | 55 phút |
| **Phân tích & Tổng kết** | Thảo luận hiện tượng Metastability, ghi nhận số liệu và ký nghiệm thu tại bàn | 20 phút |
| **Tổng cộng** | | **135 phút** |

*(Lưu ý theo lộ trình môn học: Bài 5 tập trung hoàn toàn vào thiết kế mạch tuần tự và đo kiểm định thời chuyên sâu; Layout/PEX của `dff_ms_x1` là nội dung tùy chọn nâng cao trong phần Post-lab).*

---

## 6. NỘI DUNG THỰC HÀNH TẠI LỚP (IN-LAB)

### Ex5.1: Thiết kế Schematic Tế bào D-Latch (`dlatch_x1{sch}`) (Electric VLSI)

1. Mở Electric VLSI (`mocmos`, $\lambda = 0.30\,\mu\text{m}$), tạo Cell `dlatch_x1`, View `schematic`.
2. Đặt các Instance linh kiện:
   - 2 `tg_gate{ic}`: `X_TG1` (cổng vào) và `X_TG2` (cổng phản hồi).
   - 2 `inv_x1{ic}`: `X_INV1` (đảo nút $X$ thành $\bar{Q}$) và `X_INV2` (đệm ra $Q$).
   - 1 Inverter giữ trạng thái `X_INV3`: dùng 1 PMOS ($W=4\lambda, L=2\lambda$) và 1 NMOS ($W=4\lambda, L=2\lambda$) — *vì có $TG_2$ cách ly nên $I_3$ không cần định cỡ yếu bằng $L=4\lambda$*.
3. **Đấu nối mạch và ánh xạ chân xung nhịp thống nhất (`clk`, `clk_n`):**
   - `d` $\to$ `X_TG1.in`; `X_TG1.out` $\to$ nút $X$ $\to$ `X_INV1.in`.
   - `X_INV1.out` ($\bar{Q}$) $\to$ `X_INV2.in` và `X_INV3.in`.
   - `X_INV2.out` $\to$ Export `q`.
   - `X_INV3.out` $\to$ `X_TG2.in`; `X_TG2.out` $\to$ nút $X$.
   - **Ánh xạ chân điều khiển TG:**
     * `X_TG1`: `en` $\leftarrow$ `clk`, `en_n` $\leftarrow$ `clk_n`.
     * `X_TG2`: `en` $\leftarrow$ `clk_n`, `en_n` $\leftarrow$ `clk`.
4. Tạo 6 chân Export (`Ctrl+E`): `d`, `clk`, `clk_n` (Input), `q` (Output), `vdd` (Power), `gnd` (Ground).
5. Nhấn `F5` kiểm tra đạt 0 lỗi, 0 cảnh báo. Đóng gói Icon `dlatch_x1{ic}`.

- **Sản phẩm Ex5.1:** Schematic `dlatch_x1{sch}` và Icon `dlatch_x1{ic}` đạt 0 lỗi `F5`.

---

### Ex5.2: Mô phỏng Kiểm chứng D-Latch trên LTspice

1. Xuất Netlist của `dlatch_x1`, thêm `.include "04 - Models_and_Libraries/C5_models.txt"`, nguồn `Vdd = 5.0V`, tải `CL q 0 50fF`.
2. Cấp kích thích để `D` đổi mức **ít nhất 1 lần trong pha trong suốt (`clk = 5V`)** và **1 lần trong pha chốt (`clk = 0V`)**:
   ```spice
   Vclk   clk   0 PULSE(0 5.0 20n 0.1n 0.1n 20n 40n)
   Vclk_n clk_n 0 PULSE(5.0 0 20n 0.1n 0.1n 20n 40n)
   Vd     d     0 PULSE(0 5.0 10n 0.1n 0.1n 40n 80n)
   .tran 0 160n 0 1p
   ```
3. Dùng lệnh `.meas` đo trễ $t_{pd(D \to Q)}$ trong pha trong suốt (`clk = 5V`, ví dụ từ $t = 60\,\text{ns}$ đến $80\,\text{ns}$):
   ```spice
   .meas tran tpd_lh TRIG v(d) VAL=2.5 RISE=1 TARG v(q) VAL=2.5 RISE=1
   .meas tran tpd_hl TRIG v(d) VAL=2.5 FALL=1 TARG v(q) VAL=2.5 FALL=1
   ```
   *(Lưu ý: kiểm tra dạng sóng xem sườn đầu tiên của `d` ở $t=10\text{ns}$ rơi vào pha chốt `clk=0`, nên `q` chỉ cập nhật khi `clk` lên $5\text{V}$ tại $t=20\text{ns}$. Hãy chọn sườn `d` chuyển mức nằm hẳn bên trong cửa sổ `clk=5V` bằng `TD=` để đo đúng $t_{pd(D\to Q)}$!).*
4. Quan sát $V(q)$: xác nhận trong pha chốt (`clk = 0V`), $V(q)$ giữ nguyên mức logic trong sai số vài chục mV dù $V(d)$ thay đổi; ghi nhận $V_{Q,high}$ và $V_{Q,low}$.

- **Sản phẩm Ex5.2:** Đồ thị dạng sóng 2 pha hoạt động của `dlatch_x1` và số đo $t_{pd(D \to Q)}$, $V_{Q,high}, V_{Q,low}$.

---

### Ex5.3: Thiết kế Schematic Master-Slave DFF (`dff_ms_x1{sch}`) (Electric VLSI)

1. Tạo Cell `dff_ms_x1`, View `schematic`.
2. Đặt 2 instance `dlatch_x1{ic}` (`X_MASTER`, `X_SLAVE`) và 1 instance `inv_x1{ic}` (`X_CLK_INV`).
3. Đấu nối phân cấp:
   - `d` $\to$ `X_MASTER.d`; `X_MASTER.q` (nút $Q_M$) $\to$ `X_SLAVE.d`; `X_SLAVE.q` $\to$ Export `q`.
   - `clk` $\to$ `X_CLK_INV.in` tạo tín hiệu đảo `clk_n`.
   - `X_MASTER`: `clk` $\leftarrow$ `clk_n`, `clk_n` $\leftarrow$ `clk` (Master mở khi `clk = 0`).
   - `X_SLAVE`: `clk` $\leftarrow$ `clk`, `clk_n` $\leftarrow$ `clk_n` (Slave mở khi `clk = 1`).
4. Tạo 5 Export (`Ctrl+E`): `d`, `clk` (Input), `q` (Output), `vdd`, `gnd`.
5. Nhấn `F5` đạt 0 lỗi. Tạo biểu tượng `dff_ms_x1{ic}` (hình chữ nhật có ký hiệu tam giác tại chân `clk`).

- **Sản phẩm Ex5.3:** Schematic `dff_ms_x1{sch}` và Icon `dff_ms_x1{ic}` đạt 0 lỗi `F5`.

---

### Ex5.4: Đo Đạc Đặc tính Định thời DFF ($t_{c-q}, t_{setup}, t_{hold}$) và Metastability (LTspice)

Xuất Netlist `dff_ms_x1`, gắn tải `CL q 0 50fF` và chạy với bước tích phân chặt `.tran 0 40n 0 1p`.

1. **Khởi tạo trạng thái ban đầu và Đo $t_{c-q}$ (cả LH và HL):**
   - Để điểm làm việc DC `.op` của mạch nhớ không rơi vào trạng thái ngẫu nhiên làm `.meas` báo lỗi hoặc bắt nhầm sườn của chu kỳ sau, **bắt buộc** khởi tạo bằng `.ic V(q)=0` (và cho $D$ ổn định ở $0$ trong chu kỳ đầu tiên trước khi lên $1$, hoặc dùng `.ic` cho nút $X_M, X_S$).
   - Cho `CLK` có sườn lên tại $t = 20\,\text{ns}$ (`PULSE(0 5.0 20n 0.1n 0.1n 10n 20n)`).
   - **Đo $t_{c-q,LH}$:** Cho `D` lên $5\,\text{V}$ sớm (tại $t = 10\,\text{ns}$), đo sườn lên $Q$ quanh $t = 20\,\text{ns}$:
     ```spice
     .meas tran t_cq_lh TRIG v(clk) VAL=2.5 RISE=2 TARG v(q) VAL=2.5 RISE=1 TD=19n
     ```
     *(Điều chỉnh `RISE=1` hoặc `RISE=2` khớp với thời điểm sườn `CLK` mà bạn thiết lập).*
   - **Đo $t_{c-q,HL}$:** Khởi tạo $Q=5\text{V}$ (hoặc nạp 1 ở chu kỳ trước), sau đó cho $D=0\text{V}$ trước sườn lên tiếp theo của `CLK`, đo `TARG v(q) VAL=2.5 FALL=1`.

2. **Quét xác định $t_{setup}$ (cho cả $D$ lên và $D$ xuống):**
   - Định nghĩa $\Delta t = t_{CLK,50} - t_{D,50}$ (giữa hai mốc $2.5\,\text{V}$). Nếu `CLK` và `D` có cùng $t_r = t_f = 0.1\,\text{ns}$ thì khoảng dịch `delay` đúng bằng $\Delta t$.
   - Quét thô $\Delta t$ từ $500\,\text{ps}$ xuống $20\,\text{ps}$, sau đó quét mịn quanh vùng sườn dốc (knee):
     ```spice
     .step param dt LIST 0.5n 0.3n 0.2n 0.15n 0.12n 0.10n 0.08n 0.06n 0.04n 0.02n
     ```
   - Vẽ đồ thị $t_{c-q}(\Delta t)$ từ bảng `.log`, xác định giá trị $\Delta t$ tại điểm $t_{c-q} = 1.10 \times t_{c-q,nominal}$ (10% push-out). Chú ý: khi $\Delta t$ quá nhỏ, $Q$ sẽ **không chuyển mức** ở sườn này mà chờ tới sườn sau — loại bỏ các điểm bị trượt chu kỳ đó khỏi đồ thị setup.
   - Thực hiện tương tự cho cả hai trường hợp: **$D$ chuyển $0 \to 1$ ($t_{setup,LH}$)** và **$D$ chuyển $1 \to 0$ ($t_{setup,HL}$)**.

3. **Quét xác định $t_{hold}$ (ngưỡng nhị phân):**
   - Cho $D$ ổn định trước sườn lên `CLK` ($t_C = 20\,\text{ns}$), sau đó thay đổi $D$ tại thời điểm $t_C + \Delta t_{hold}$ với $\Delta t_{hold}$ quét từ $-50\,\text{ps}$ đến $+100\,\text{ps}$ (bước $5\,\text{ps}$):
     ```spice
     .step param dt_h -50p 100p 5p
     .meas tran q_final FIND v(q) AT=25n
     ```
   - Quan sát giá trị `q_final` sau khi ngõ ra đã ổn định (tại $t = 25\,\text{ns}$): ngưỡng $\Delta t_{hold}$ nhỏ nhất mà `q_final` giữ đúng giá trị cũ (không bị dữ liệu mới ghi đè) chính là $t_{hold}$ (ghi rõ dấu dương hay âm).

4. **Quan sát Metastability:**
   - Chọn một giá trị $\Delta t$ sát ngay biên giới thất bại (ví dụ tại ranh giới chuyển từ giữ được sang mất dữ liệu khi quét $t_{setup}$ hoặc $t_{hold}$), phóng to đồ thị nút nội $V(Q_M)$ và ngõ ra $V(q)$ để ghi nhận hiện tượng điện áp trôi lơ lửng quanh $V_{DD}/2$ một khoảng thời gian dài trước khi rơi về 0 hoặc 5 V.

- **Sản phẩm Ex5.4:** Bảng số liệu $t_{c-q}$ (LH, HL), đồ thị push-out xác định $t_{setup}$ (LH, HL), ngưỡng $t_{hold}$ và ảnh chụp dạng sóng Metastability.
- **Câu hỏi kiểm tra nhanh:** Tại sao trong phép đo $t_{hold}$ ta phải dùng `.meas FIND v(q) AT=...` thay vì dùng tiêu chí đẩy trễ 10% như ở $t_{setup}$?

---

## 7. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (POST-LAB)

### 7.1. Thực nghiệm Post-lab
1. **Đánh giá ảnh hưởng của kích thước bộ đảo xung nhịp (`X_CLK_INV`):**
   - Trong file mô phỏng `dff_ms_x1`, tăng kích thước `X_CLK_INV` lên gấp đôi (`inv_x2`: $W_n = 8\lambda, W_p = 24\lambda$) và chạy lại phép quét $t_{hold}$. So sánh $t_{hold}$ giữa trường hợp `inv_x1` và `inv_x2`, giải thích kết quả dựa trên lý thuyết chồng dẫn $\overline{CLK}$.
2. **Đánh giá chu kỳ xung nhịp tối thiểu $T_{min}$:**
   - Tính $T_{min,no-logic} = t_{c-q,max} + t_{setup,max}$ từ số đo thực tế và tính tần số tối đa lý thuyết khi chưa có logic tổ hợp.
3. *(Tùy chọn nâng cao - Không bắt buộc):* Thiết kế Layout phân cấp `dff_ms_x1{lay}` từ 2 instance `dlatch_x1{lay}` và `inv_x1{lay}`, kiểm tra DRC/NCC và chạy trích xuất ký sinh PEX.

### 7.2. Phiếu báo cáo điền khuyết (Nộp kèm file mô phỏng)

```
========================================================================================
                          BÁO CÁO THỰC HÀNH: BÀI 5
     MẠCH TUẦN TỰ MỨC TRANSISTOR: D-LATCH VÀ D-FLIP-FLOP MASTER-SLAVE
Họ và Tên: ..................................................... MSSV: .................
Lớp: ....................................... Nhóm/Bàn: ......... Ngày: .................
Chữ ký Giảng viên / Điểm nghiệm thu tại bàn: ............................................
========================================================================================
```

#### a. Phần Chuẩn bị (Pre-lab)
1. **Bảng chân trị hoạt động của Master-Slave DFF (Tự điền):**

| $CLK$ | Ngõ vào $D$ | Trạng thái Master Latch | Trạng thái Slave Latch | Ngõ ra $Q_{next}$ | Chế độ hoạt động |
| :---: | :---: | :---: | :---: | :---: | :--- |
| 0 | 0 | ............................. | ............................. | ................... | ............................. |
| 0 | 1 | ............................. | ............................. | ................... | ............................. |
| 1 | X | ............................. | ............................. | ................... | ............................. |
| $\uparrow$ (Sườn lên) | 0 | ............................. | ............................. | ................... | ............................. |
| $\uparrow$ (Sườn lên) | 1 | ............................. | ............................. | ................... | ............................. |

2. **Ước lượng định thời (dùng $t_{pd,inv} =$ ........ ps từ Bài 1 và $t_{pd,tg} =$ ........ ps từ Bài 4):**
   - $t_{pd(D \to Q)}$ (D-Latch) $\approx$ ................ ps.
   - $t_{c-q}$ (DFF, đường đầy đủ $I_1, I_2$) $\approx$ ................ ps.
   - $t_{setup}$ $\approx$ ................ ps ; $t_{hold}$ $\approx$ ................ ps.
   - $T_{min,no-logic} = t_{c-q} + t_{setup} =$ ................ ps.

3. **Tính toán $V_X$ nếu bỏ $TG_2$ (Ratioed Weak Feedback):**
   - Với $I_3$ kích thước $W=4\lambda, L=2\lambda$: $V_X =$ ................ V (Đạt / Không đạt? ................).
   - Với $I_3$ kích thước $W=4\lambda, L=4\lambda$: $V_X =$ ................ V (Đạt / Không đạt? ................).

#### b. Kết quả Đo đạc Thực hành (In-lab & Post-lab)
1. **Kết quả đo đạc D-Latch (`dlatch_x1`, $C_L = 50\,\text{fF}$):**

| Thông số đo | Dự đoán Pre-lab | Giá trị đo LTspice | Sai lệch (%) |
| :--- | :---: | :---: | :---: |
| Trễ trong suốt $t_{pd,LH}$ ($D \to Q$) | ................ ps | ................ ps | ................ % |
| Trễ trong suốt $t_{pd,HL}$ ($D \to Q$) | ................ ps | ................ ps | ................ % |
| Điện áp chốt mức cao $V_{Q,high}$ | $5.00\,\text{V}$ | ................ V | — |
| Điện áp chốt mức thấp $V_{Q,low}$ | $0.00\,\text{V}$ | ................ V | — |

2. **Kết quả đo đặc tính định thời DFF (`dff_ms_x1`, $C_L = 50\,\text{fF}$):**

| Thông số định thời | Dự đoán Pre-lab | Đo kiểm với `X_CLK_INV` (`inv_x1`) | Ghi chú / Quy ước đo |
| :--- | :---: | :---: | :--- |
| **$t_{c-q,LH}$** | ................ ps | ................ ps | Khởi tạo `.ic V(q)=0` |
| **$t_{c-q,HL}$** | ................ ps | ................ ps | |
| **$t_{c-q,nominal}$ trung bình** | ................ ps | ................ ps | |
| **$t_{setup,LH}$ ($D: 0 \to 1$)** | ................ ps | ................ ps | Quy ước đẩy trễ 10% |
| **$t_{setup,HL}$ ($D: 1 \to 0$)** | ................ ps | ................ ps | Quy ước đẩy trễ 10% |
| **$t_{hold}$ (ngưỡng & dấu)** | ................ ps | ................ ps | Quét `-50p..+100p`, bước `5p` |
| **$t_{hold}$ khi dùng `inv_x2` (Post-lab)** | — | ................ ps | Chênh lệch tuyệt đối: ........ ps |
| **$T_{min,no-logic}$** | ................ ps | ................ ps | Tương ứng $1/T_{min} =$ ........ GHz |

#### c. Câu hỏi Thảo luận Chuyên sâu
1. Dựa vào dạng sóng Metastability quan sát được trong Ex5.4, hãy giải thích điều gì xảy ra tại nút lưu trữ nội $Q_M$ khi vi phạm $t_{setup}$ hoặc $t_{hold}$. Trong hệ thống số thực tế nhận tín hiệu bất đồng bộ từ bên ngoài, kỹ sư thường dùng cấu trúc đồng bộ hóa (Synchronizer) gì để giảm xác suất lỗi?
2. Giải thích tại sao khi thay `X_CLK_INV` từ `inv_x1` lên `inv_x2`, giá trị $t_{hold}$ lại thay đổi theo chiều hướng bạn đã đo được ở Post-lab.
3. *(Tùy chọn)* Trình bày nguyên lý hoạt động cơ bản của DFF dùng xung nhịp đơn pha (TSPC - True Single-Phase Clock DFF) và nêu ưu/nhược điểm so với TG Master-Slave DFF trong bài học này.

---

## 8. BẢNG KIỂM CHỨNG VÀ ĐỐI CHUẨN KỸ THUẬT (BENCHMARK)

*(Số liệu tham chiếu cho công nghệ MOSIS C5N $V_{DD} = 5.0\,\text{V}, C_L = 50\,\text{fF}$; giá trị thực tế phụ thuộc vào thời gian sườn xung $t_r/t_f$ và mô hình Level 3).*

| Thông số kiểm chứng | Dải giá trị kỳ vọng (MOSIS C5N) | Điều kiện kiểm tra |
| :--- | :---: | :--- |
| **Số lượng Transistor** | `dlatch_x1`: $10\text{T}$; `dff_ms_x1`: $22\text{T}$ | Sơ đồ chuẩn có $TG_2$ |
| **Mức chốt giữ Latch ($V_{Q,high}/V_{Q,low}$)** | $5.00\,\text{V}$ / $0.00\,\text{V}$ (sai số $\le 20\,\text{mV}$) | Trong pha chốt `clk = 0` |
| **Trễ $t_{c-q}$ danh định** | $\approx 130 - 160\,\text{ps}$ (suy dẫn $144\,\text{ps}$) | Đường $CLK \to \overline{CLK} \to TG_{S1} \to I_{S1} \to I_{S2}$ |
| **Thời gian thiết lập $t_{setup}$** | $\approx 70 - 100\,\text{ps}$ | Quy ước 10% push-out |
| **Thời gian giữ $t_{hold}$** | Dương, cỡ $15 - 45\,\text{ps}$ | Quét bước $5\,\text{ps}$ với `X_CLK_INV` (`inv_x1`) |

---

## 9. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP

| Hiện tượng lỗi | Nguyên nhân gốc rễ | Cách khắc phục nhanh |
| :--- | :--- | :--- |
| **Lệnh `.meas t_cq_lh` báo `Measurement FAILED`** | (1) Điểm làm việc DC `.op` ban đầu đưa $Q$ lên $5\text{V}$ sẵn nên không có sườn lên.<br>(2) Không đặt `TD=` khiến `.meas` bắt nhầm sườn khác. | Khởi tạo mạch bằng `.ic V(q)=0` (và cho $D=0$ ở chu kỳ đầu), thêm `TD=` ngay trước sườn `CLK` cần đo. |
| **Khi quét $\Delta t$ nhỏ, $t_{c-q}$ bỗng tăng vọt lên tới hàng chục `ns` (bằng cả 1 chu kỳ)** | Dữ liệu $D$ đến quá trễ bị trượt sang sườn `CLK` của chu kỳ kế tiếp nên `TARG v(q)=2.5 RISE=1` bắt nhầm sườn chu kỳ sau. | Giới hạn vùng kiểm tra và loại bỏ các điểm $\Delta t$ bị trượt chu kỳ (lỗi chốt dữ liệu) khỏi đường cong tính $t_{setup}$. |
| **DFF hoạt động như DFF sườn âm (Negative Edge) thay vì sườn dương** | Đấu ngược cặp chân `clk` và `clk_n` giữa `X_MASTER` và `X_SLAVE`. | Kiểm tra lại: `X_MASTER` nhận `clk_n` vào chân `clk` (mở khi $CLK=0$); `X_SLAVE` nhận `clk` vào chân `clk` (mở khi $CLK=1$). |
| **Trong `dlatch_x1`, ngõ ra $Q$ không giữ được giá trị khi `clk = 0`** | Đấu nhầm `en`/`en_n` của `X_TG2` giống với `X_TG1`, làm cả hai cùng ngắt khi `clk = 0`. | Kiểm tra bảng ánh xạ: `X_TG2` có `en = clk_n`, `en_n = clk`. |

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

*(Đánh giá dựa trên minh chứng mô phỏng, độ chính xác phương pháp đo và báo cáo phân tích).*

| Tiêu chí đánh giá | Trọng số | Xuất sắc (8.5 – 10) | Khá (7.0 – 8.4) | Đạt (5.0 – 6.9) | Không đạt (< 5.0) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Chuẩn bị Pre-lab** | **20%** | Tự điền đúng bảng chân trị DFF, tính đúng đường trễ đầy đủ từ số liệu Lab 1/4, giải đúng bài toán chia áp $I_3$ ($4\lambda/2\lambda$ vs $4\lambda/4\lambda$). | Lập đúng bảng chân trị và tính đúng đường trễ, giải bài toán chia áp $I_3$ còn sai số nhỏ. | Có bài chuẩn bị nhưng thiếu phần tính toán $I_3$ hoặc thiếu $I_2$ trong công thức $t_{c-q}$. | Không làm Pre-lab hoặc sao chép. |
| **2. Schematic & Mô phỏng D-Latch (Ex5.1–5.2)** | **20%** | Schematic `dlatch_x1` (10T) đạt 0 lỗi `F5`; mô phỏng đúng 2 pha trong suốt/chốt giữ và đo đúng $t_{pd(D\to Q)}$. | Schematic đạt 0 lỗi, mô phỏng đúng 2 pha nhưng đo trễ $D \to Q$ chọn nhầm cửa sổ sườn. | Dựng đúng schematic nhưng đấu ngược chân `clk`/`clk_n` của `TG2` phải sửa lại. | Không hoàn thành mô phỏng D-Latch. |
| **3. Schematic DFF & Đo $t_{c-q}$ (Ex5.3–5.4a)** | **20%** | Ghép phân cấp `dff_ms_x1` (22T) chuẩn, biết dùng `.ic` khởi tạo và đo đủ $t_{c-q,LH}$ và $t_{c-q,HL}$. | Ghép đúng schematic và đo được $t_{c-q,LH}$, thiếu $t_{c-q,HL}$. | Mắc lỗi `.meas FAILED` do quên khởi tạo `.ic` hoặc quên `TD=`. | DFF sai cực tính sườn hoặc không chạy. |
| **4. Quét $t_{setup}, t_{hold}$ & Metastability (Ex5.4b)** | **25%** | Quét đủ cả 2 hướng $D$ cho $t_{setup}$ (10% push-out), quét $t_{hold}$ bước $5\,\text{ps}$ dùng `.meas FIND` và chụp được dạng sóng Metastability. | Quét được $t_{setup}$ (1 hướng) và tìm được ngưỡng $t_{hold}$, chưa chụp được Metastability. | Chỉ đo được $t_{setup}$ thô chưa tìm điểm 10%, hoặc nhầm tiêu chí push-out cho $t_{hold}$. | Không thực hiện quét định thời. |
| **5. Post-lab & Báo cáo phân tích** | **15%** | Hoàn thành thí nghiệm `inv_x2` cho $t_{hold}$, tính đúng $T_{min}$ và trả lời sâu sắc các câu hỏi thảo luận. | Hoàn thành thí nghiệm `inv_x2` nhưng phần giải thích cơ chế còn sơ sài. | Chỉ nộp số liệu In-lab, thiếu phần khảo sát Post-lab `inv_x2`. | Nộp thiếu báo cáo hoặc số liệu không khớp file `.log`. |

---

## 11. TÀI LIỆU THAM KHẢO

1. N. H. E. Weste & D. M. Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th Ed., Addison-Wesley (Chương 10: Sequential Circuit Design — Latches, Flip-Flops, Timing & Metastability).
2. J. M. Rabaey, A. Chandrakasan & B. Nikolic, *Digital Integrated Circuits: A Design Perspective*, 2nd Ed., Prentice Hall (Chương 7: Designing Sequential Logic Circuits).
3. R. Jacob Baker, *CMOS: Circuit Design, Layout, and Simulation*, 3rd Ed., Wiley-IEEE Press (Hướng dẫn mô phỏng LTspice và Electric VLSI).
4. Thư viện mô hình SPICE chuẩn phòng thí nghiệm: `04 - Models_and_Libraries/C5_models.txt`.
