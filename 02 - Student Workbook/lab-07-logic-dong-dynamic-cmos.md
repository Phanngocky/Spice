# THỰC HÀNH THIẾT KẾ VLSI — BÀI 7 (LAB 07)
# KỸ THUẬT LOGIC ĐỘNG VÀ LOGIC DOMINO (DYNAMIC & DOMINO CMOS LOGIC)

---
**Bộ môn:** Điện tử – Viễn thông | **Khoa:** Điện – Điện tử  
**Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Thời lượng:** 135 phút thực hành tại phòng máy (kết hợp tự học Pre-lab & hoàn thiện Post-lab)  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07+), LTspice XVII / LTspice 2025  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5µm ($\lambda = 0.30\,\mu\text{m}$, $L_{min} = 0.60\,\mu\text{m}$, $V_{DD} = 5.0\,\text{V}$)  
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Phân tích ưu thế điện dung ngõ vào ($C_{in}$) và tổng bề rộng ($\Sigma W$) của Dynamic CMOS:** Giải thích chu trình 2 pha Precharge ($CLK=0$) / Evaluate ($CLK=1$), hạn chế giữ điện tích hữu hạn (dòng rò) và chứng minh Domino OR4 giảm mạnh $\Sigma W$ và $C_{in}$ mỗi ngõ vào so với Static OR4.
2. **Đo độ sụt áp chia sẻ điện tích (Charge Sharing) trên mạch có nút nội cô lập:** Xây dựng mạch thử nghiệm 2 NMOS nối tiếp (chồng AND-style), đo độ sụt áp $V_{X,min}$ trên LTspice, đối chiếu với công thức bảo toàn điện tích và giới hạn nạp $V_G - V_{thn}$ từ Pre-lab.
3. **Đo đánh đổi khi định cỡ Keeper (`M_kp`):** Quét kích thước Keeper và đo đồng thời **hai đại lượng** ($t_{pd,eval}$ và độ sụt áp $V_{X,min}$ trong ca chia sẻ điện tích) để lựa chọn kích thước Keeper hợp lý và giải thích ngưỡng mà Keeper thắng mạng PDN.
4. **Thực nghiệm tính đơn điệu (Monotonicity) của Domino ghép chuỗi:** Mô phỏng so sánh hai cổng Dynamic nối trực tiếp (lỗi xả sớm) với hai cổng Domino nối tiếp có Inverter đệm.
5. **Đối sánh PPA Domino OR4 vs Static OR4:** Đo đạc thời gian trễ $t_{pd,eval}$, $\Sigma W$, $C_{in}$ và năng lượng tiêu tán mỗi chu kỳ giữa `domino_or4_x1` và `static_or4` dưới cùng điều kiện tải và bộ lái.

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

| Hạng mục | Chi tiết |
|---|---|
| **IP kế thừa từ các bài trước** | - Tế bào Inverter chuẩn `inv_x1` (Bài 1).<br>- Thư viện mô hình SPICE: `04 - Models_and_Libraries/C5_models.txt` (NMOS: `N`, PMOS: `P`). |
| **Sản phẩm bàn giao cuối buổi** | - Mạch mô phỏng Charge Sharing 2-NMOS nối tiếp (có/không có Keeper).<br>- Tế bào Domino OR4 `domino_or4_x1{sch}` ($9\text{T}$) và bảng đo kiểm 6 tổ hợp.<br>- Đồ thị quét hai đại lượng ($t_{pd,eval}$ và $V_{X,min}$) theo kích thước Keeper.<br>- Kết quả mô phỏng chuỗi 2 tầng Dynamic vs Domino và bảng so sánh PPA với Static OR4. |
| **Kế thừa cho các bài sau** | - Kiến thức thiết kế thanh ghi/cổng tốc độ cao và kỹ thuật kiểm soát nhiễu nút động (hữu ích cho các mạch giải mã hoặc cộng nhanh nâng cao). |

---

## 3. CƠ SỞ LÝ THUYẾT NGẮN GỌN

### 3.1. Chu trình 2 Pha của Logic Động (Dynamic CMOS)

Thay vì dùng $N$ PMOS trong mạng PUN như logic tĩnh, cổng Dynamic CMOS dùng $N$ NMOS trong mạng PDN kết hợp với PMOS nạp trước $M_{pre}$ và Foot NMOS đánh giá $M_{eval}$, cùng điều khiển bởi xung nhịp $CLK$:

1. **Pha Nạp trước (Precharge - $CLK = 0\,\text{V}$):** $M_{pre}$ dẫn, $M_{eval}$ ngắt; nút động $X$ được nạp lên $V_{DD}$. Vì $M_{eval}$ ngắt nên không có dòng tĩnh xuyên đất.
2. **Pha Đánh giá (Evaluate - $CLK = V_{DD}$):** $M_{pre}$ ngắt, $M_{eval}$ dẫn. Nút $X$ giữ điện áp trên tụ $C_X$ trong thời gian hữu hạn (bị suy giảm nếu có dòng rò dưới ngưỡng khi tần số quá thấp). Nếu PDN thông mạch xuống $M_{eval}$, $C_X$ xả về $0\,\text{V}$; ngược lại $X$ giữ mức cao.
3. **Điều kiện ổn định ngõ vào:** Trong pha Evaluate của mạch Domino chuẩn, mọi ngõ vào phải ổn định trước sườn lên $CLK$ (hoặc chỉ được chuyển theo hướng $0 \to 1$, không được chuyển $1 \to 0$ sau khi Evaluate đã bắt đầu vì nút động $X$ không thể tự nạp lại cho đến chu kỳ Precharge kế tiếp).

### 3.2. Hiện Tượng Chia Sẻ Điện Tích (Charge Sharing) và Điều Kiện Áp Dụng

Xét mạch PDN có **hai NMOS mắc nối tiếp** ($M_{top}$ nối nút động $X$, $M_{bot}$ nối đất/foot, nút nội ở giữa có tụ ký sinh $C_{int}$). *Lưu ý: Cổng OR4 dùng 4 NMOS song song có Foot NMOS sẽ **không** gặp chia sẻ điện tích trong pha Evaluate vì nút nội `n_eval` được nối thẳng xuống đất qua $M_{eval}$; hiện tượng này chỉ xuất hiện khi có nút nội bị cô lập bởi transistor dưới đang khóa.*

Khi bước vào pha Evaluate ($M_{top}$ dẫn, $M_{bot}$ khóa), điện tích từ $C_X$ (đang ở $V_{DD}$) san sẻ sang $C_{int}$ (đang ở $0\,\text{V}$):
$$V_X' = V_{DD} \cdot \frac{C_X}{C_X + C_{int}}, \qquad \Delta V_X = V_{DD} \cdot \frac{C_{int}}{C_X + C_{int}}$$

- **Điều kiện áp dụng công thức cân bằng:** Transistor NMOS trên ($M_{top}$) chỉ có thể nạp $C_{int}$ lên tối đa $V_{max,int} = V_G - V_{thn}(V_{SB})$ (giới hạn ngưỡng có hiệu ứng thân, khoảng $3.6 - 3.8\,\text{V}$ với $V_{DD}=5\text{V}$). Do đó công thức cân bằng điện tích trên chỉ đúng khi $V_X' \le V_{max,int}$ (tức $\frac{C_{int}}{C_X + C_{int}} \ge 0.24 - 0.27$). Nếu $C_{int}$ rất nhỏ, $M_{top}$ sẽ tự ngắt trước khi $C_{int}$ kịp lên tới $V_X'$.
- **Ví dụ minh họa:** Với $C_X = 30\,\text{fF}, C_{int} = 6\,\text{fF}$ ($\frac{C_{int}}{C_X+C_{int}} = 0.167 < 0.24$), công thức lý tưởng cho $V_X' = 4.17\,\text{V}$, nhưng thực tế $M_{top}$ ngắt sớm hơn nên độ sụt áp thực tế nhỏ hơn mức dự đoán tuyến tính.

### 3.3. Transistor Duy Trì (Keeper) và Định Cỡ Inverter Đệm

- **Keeper PMOS ($M_{kp}$):** Mắc song song $M_{pre}$, cổng nối hồi tiếp với ngõ ra $Y$ của Inverter đệm. Khi $X$ cao ($Y=0$), Keeper dẫn nhẹ bù dòng rò và làm chậm/giảm sụt áp chia sẻ điện tích (lưu ý: Keeper không triệt tiêu hoàn toàn xung sụt tức thời nếu chia sẻ diễn ra quá nhanh).
- **Tranh chấp (Contention) & Luật hình học:** Khi PDN xả nút $X$, mạng PDN (đặc biệt trường hợp xấu nhất là chỉ có **1 nhánh đơn** dẫn nối tiếp qua $M_{eval}$) phải kéo thắng dòng nạp của Keeper. Trong thiết kế layout thực tế (SCMOS DRC), bề rộng Active tối thiểu thường là $3\lambda$, nên tránh dùng $W_{kp} = 2\lambda$ nếu có ý định vẽ layout; thay vào đó kỹ sư thường dùng $W_{kp} = 3\lambda - 4\lambda$ kết hợp tăng chiều dài kênh **$L_{kp} = 4\lambda - 8\lambda$** để giảm sức kéo mà vẫn đạt DRC. Việc chọn giá trị Keeper tối ưu phải dựa trên mô phỏng đánh đổi giữa độ bền nhiễu và độ tăng trễ $t_{pd,eval}$.
- **Inverter đệm ngõ ra:** Khi dùng Inverter có $W_p = 16\lambda, W_n = 8\lambda$ ($W_p / W_n = 2$), do tỉ số độ linh động $K'_n/K'_p = 3$, ngưỡng chuyển mạch $V_M$ của Inverter này **thấp hơn** ngưỡng đối xứng của `inv_x1` ($2.45\,\text{V}$). Đây là Inverter **Low-skew** (NMOS tương đối mạnh hơn), giúp tăng lề nhiễu mức cao $NM_H = V_X' - V_M$ chống lật giả khi $X$ bị sụt áp nhẹ, đổi lại sườn lên của $Y$ sẽ chậm hơn một chút.

### 3.4. So sánh $\Sigma W$ và $C_{in}$ giữa Domino OR4 và Static OR4

Cổng Domino OR4 chỉ cần $9$ transistor ($1$ $M_{pre}$, $1$ $M_{eval}$, $4$ NMOS PDN, $1$ Keeper, $2$ T Inverter) và mỗi ngõ vào chỉ lái duy nhất $1$ NMOS ($C_{in} \approx 4\lambda$), nhỏ hơn rất nhiều so với cổng Static OR4 (`NOR4 + INV`: $10\text{T}$, trong đó $4$ PMOS mắc nối tiếp của NOR4 phải định cỡ rất lớn để giữ cùng sức kéo, làm $C_{in}$ mỗi ngõ vào tăng lên gấp nhiều lần).

---

## 4. CÂU HỎI CHUẨN BỊ TRƯỚC KHI ĐẾN LỚP (PRE-LAB)

> [!IMPORTANT]
> Sinh viên phải hoàn thành phần tính toán và sơ đồ dưới đây vào **Mục 7.2.a** trước giờ vào phòng máy để phục vụ **Cổng kiểm tra Pre-lab (10 phút đầu giờ)**.

1. **Tính toán Ngưỡng $V_M$ và Hiện tượng Chia sẻ Điện tích:**
   - Cho Inverter đệm của cổng Domino có kích thước $W_p = 16\lambda, W_n = 8\lambda, L = 2\lambda$ ($K'_n = 120\,\mu\text{A/V}^2, K'_p = 40\,\mu\text{A/V}^2, V_{tn0} = 0.70\,\text{V}, |V_{tp0}| = 0.80\,\text{V}, V_{DD} = 5.0\,\text{V}$). Hãy **tự tính điện áp ngưỡng chuyển mạch $V_M$** của Inverter này.
   - Với $C_X = 20\,\text{fF}$ và $C_{int} = 14\,\text{fF}$ (nút nội ở $0\,\text{V}$), tính $V_X'$, $\Delta V_X$, lề nhiễu mức cao $NM_H = V_X' - V_M$ và điều kiện tỉ số $C_{int}/C_X$ để xảy ra lật giả ($V_X' \le V_M$).
   - *(Mở rộng):* Nếu $C_{int}/C_X = 0.1$, công thức cân bằng cho $\Delta V_X$ bằng bao nhiêu, và giới hạn nạp thực tế của NMOS trên ($V_G - V_{thn}(V_{SB})$) ảnh hưởng thế nào đến kết quả?
2. **Tính đơn điệu & Ghép chuỗi Dynamic thuần:**
   - Vẽ giản đồ xung dự đoán cho $X_1$ (ngõ ra cổng Dynamic 1) và $X_2$ (ngõ ra cổng Dynamic 2 nối trực tiếp vào $X_1$ không qua Inverter) khi bước vào pha Evaluate ($CLK = 1$), biết trong pha Evaluate ngõ vào cổng 1 lên mức '1'. Giải thích tại sao cổng Dynamic 2 bị lỗi xả sớm.
3. **Viết Netlist mạch thử Charge Sharing (2-NMOS nối tiếp):**
   - Dựa vào sơ đồ nguyên lý mạch thử **2-NMOS nối tiếp** (`M_top` cực cổng `in_top` nối nút `x`, `M_bot` cực cổng `in_bot` nối `m_eval`), hãy viết đoạn mã Netlist SPICE hoàn chỉnh với $C_X = 20\,\text{fF}, C_{int} = 14\,\text{fF}$, thiết lập xung sao cho trong pha Precharge ($CLK=0$) đặt `in_bot = 5V, in_top = 0V` (để xả $C_{int}$ về 0), và khi sang pha Evaluate ($CLK=5V$) đặt `in_top = 5V, in_bot = 0V` (để cô lập $C_{int}$ và kích hoạt chia sẻ điện tích).
4. **Ước lượng tỉ số dòng Keeper / PDN:**
   - Ở điểm giữa dải $V_X = 2.5\,\text{V}$, tính xấp xỉ dòng điện qua một nhánh đơn PDN ($W=4\lambda$ nối tiếp foot $8\lambda$, tổng $R_{eq} \approx 1.45\,\text{k}\Omega$) và dòng qua Keeper PMOS ($L=2\lambda$) với các bề rộng $W_{kp} = 2\lambda, 4\lambda, 6\lambda, 8\lambda$. Dự đoán ngưỡng $W_{kp}$ mà Keeper bắt đầu tranh chấp nặng với PDN.

---

## 5. KẾ HOẠCH PHÂN BỔ THỜI LƯỢNG IN-LAB (135 PHÚT)

| Phân đoạn | Nội dung thực hiện | Thời lượng |
| :--- | :--- | :---: |
| **Kiểm tra đầu giờ** | Cổng kiểm tra Pre-lab (tính $V_M$, bài toán $C_X=20\text{fF}/C_{int}=14\text{fF}$, tỉ số dòng Keeper) | 10 phút |
| **Ex7.1** | Mô phỏng Charge Sharing trên mạch 2-NMOS nối tiếp (có/không có Keeper) trên LTspice | 25 phút |
| **Ex7.2** | Dựng Schematic `domino_or4_x1{sch}` trên Electric và kiểm tra 6 tổ hợp (Precharge/Evaluate) | 20 phút |
| **Ex7.3** | Quét kích thước Keeper (`W_kp` hoặc `L_kp`), đo đồng thời $t_{pd,eval}$ và $V_{X,min}$ | 30 phút |
| **Ex7.4** | Thực nghiệm Domino ghép chuỗi 2 tầng (so sánh nối trực tiếp Dynamic vs nối qua Inverter Domino) | 20 phút |
| **Ex7.5** | Đối sánh PPA giữa Domino OR4 và Static OR4 (`NOR4 + INV`: trễ, $\Sigma W$, $C_{in}$, năng lượng/chu kỳ) | 20 phút |
| **Tổng kết** | Ghi nhận số liệu vào Phiếu báo cáo và ký nghiệm thu tại bàn | 10 phút |
| **Tổng cộng** | | **135 phút** |

*(Lưu ý theo lộ trình: Lab 7 là bài tự chọn chuyên sâu về thiết kế mạch động, không bắt buộc thực hiện Layout/PEX trong giờ thực hành).*

---

## 6. NỘI DUNG THỰC HÀNH TẠI LỚP (IN-LAB)

### Ex7.1: Mô phỏng Charge Sharing trên Mạch 2-NMOS Nối tiếp (LTspice)

1. Mở LTspice, sử dụng khung mạch thử nghiệm **2-NMOS nối tiếp** (tạo 2 bản sao song song trong cùng tệp `.sp`: nhánh không Keeper cho nút `x_nokp`/`y_nokp` và nhánh có Keeper cho nút `x_kp`/`y_kp` với `W_kp = 4λ, L_kp = 4λ`):
   ```spice
   .include "04 - Models_and_Libraries/C5_models.txt"
   Vdd vdd 0 DC 5.0
   * Vi du nhanh khong Keeper (tao tuong tu nhanh co Keeper PMOS noi y_kp -> x_kp)
   Mp_pre  x_nokp clk vdd vdd P W=3.6u L=0.6u
   Mn_top  x_nokp in_top n_int 0 N W=1.2u L=0.6u
   Mn_bot  n_int  in_bot n_foot 0 N W=1.2u L=0.6u
   Mn_foot n_foot clk    0     0 N W=2.4u L=0.6u
   Cx_nokp x_nokp 0 20fF
   Cint    n_int  0 14fF
   * Inverter dem 16lambda/8lambda (Wp=4.8u, Wn=2.4u)
   Mp_inv y_nokp x_nokp vdd vdd P W=4.8u L=0.6u
   Mn_inv y_nokp x_nokp 0   0   N W=2.4u L=0.6u
   ```
2. **Thiết lập xung kích thích:**
   - `Vclk`: `PULSE(0 5.0 0 0.1n 0.1n 10n 20n)` (Precharge `0-10n`, Evaluate `10n-20n`).
   - Trong Precharge ($0-10\text{ns}$): đặt `in_bot = 5V`, `in_top = 0V` để xả `n_int` về $0\text{V}$ (chú ý trong Precharge foot tắt, nên để xả `n_int` hoàn toàn từ đầu hãy đặt `.ic V(n_int)=0` hoặc cho `in_bot=5V` ở chu kỳ trước).
   - Tại $t = 11\,\text{ns}$ (trong pha Evaluate): chuyển `in_bot` xuống `0V` và bật `in_top` lên `5V` để kích hoạt chia sẻ điện tích giữa $C_X$ và $C_{int}$.
3. Chạy `.tran 0 25n 0 10p`.
4. Dùng `.meas` đo điện áp cực tiểu $V_{X,min}$ và điện áp nhiễu đỉnh $V_{Y,max}$ trong cửa sổ `FROM=10.5n TO=19n` cho cả hai nhánh (không Keeper vs có Keeper).

- **Sản phẩm Ex7.1:** Đồ thị so sánh `V(x_nokp)` vs `V(x_kp)` và `V(y_nokp)` vs `V(y_kp)`, kèm số đo `.log`.

---

### Ex7.2: Thiết kế Schematic Domino OR4 (`domino_or4_x1{sch}`) (Electric VLSI)

1. Mở Electric VLSI (`mocmos`, $\lambda = 0.30\,\mu\text{m}$), tạo Cell `domino_or4_x1{sch}`.
2. Đặt các transistor theo bảng kích thước chuẩn:
   - `M_pre` (PMOS): $W=12\lambda, L=2\lambda$ (Gate nối `clk`).
   - `M_eval` (Foot NMOS): $W=8\lambda, L=2\lambda$ (Gate nối `clk`).
   - 4 NMOS PDN ($M_A, M_B, M_C, M_D$): $W=4\lambda, L=2\lambda$, mắc song song giữa nút động `x` và nút `n_eval`.
   - `M_kp` (Keeper PMOS): $W=4\lambda, L=4\lambda$ (đạt chuẩn kích thước hình học $\ge 3\lambda$, Gate nối `y`).
   - Inverter đệm (Low-skew): PMOS $W=16\lambda, L=2\lambda$ và NMOS $W=8\lambda, L=2\lambda$.
3. Tạo Export: `a, b, c, d, clk` (Input), `y` (Output), `vdd, gnd`. Nhấn `F5` kiểm tra 0 lỗi.
4. Xuất Netlist sang LTspice (tải `CL y 0 50fF`), chạy kiểm tra chức năng với 6 tổ hợp đầu vào `(a,b,c,d)`: `0000`, `1000`, `0100`, `0010`, `0001`, `1111`. Ghi nhận $V(x), V(y)$ tại mốc **cuối pha Precharge** ($t=9.5\,\text{ns}$) và **cuối pha Evaluate** ($t=19.5\,\text{ns}$).
5. Đo $t_{pd,eval}$ từ thời điểm `V(clk)=2.5` sườn lên đến `V(y)=2.5` sườn lên khi một ngõ vào đã ổn định ở mức `5V` (ví dụ `1000`).

- **Sản phẩm Ex7.2:** Schematic `domino_or4_x1{sch}` và bảng đo kiểm 6 tổ hợp.

---

### Ex7.3: Quét Kích thước Keeper — Đo Hai Đại lượng Đánh đổi (LTspice)

1. Sử dụng mạch `domino_or4_x1` (hoặc mạch 2-NMOS nối tiếp ở Ex7.1) với thông số quét `W_kp` ($L_{kp}=2\lambda$ cố định để khảo sát rộng dải dòng):
   ```spice
   .step param Wkp LIST 0.6u 1.2u 1.8u 2.4u
   ```
   *(Tương ứng $W_{kp} = 2\lambda, 4\lambda, 6\lambda, 8\lambda$; hoặc giữ $W_{kp}=1.2\mu\text{m}$ và quét $L_{kp} = 0.6\mu, 1.2\mu, 1.8\mu, 2.4\mu$)*.
2. Với **mỗi giá trị `Wkp`**, đo đồng thời **2 đại lượng**:
   - **(1) Trễ đánh giá $t_{pd,eval}$:** Khi chỉ có 1 nhánh PDN đơn ($A=5\text{V}, B=C=D=0\text{V}$) xả nút $X$. *(Lưu ý: nếu tại `Wkp = 2.4u` ($8\lambda$) Keeper kéo quá mạnh làm $X$ không rớt qua $V_M$ và $Y$ không lật, `.meas` sẽ báo `FAILED` — hãy ghi nhận đó là trạng thái "Không đánh giá được / Tranh chấp thắng PDN")*.
   - **(2) Độ sụt áp $V_{X,min}$ trong ca chia sẻ điện tích:** Đo khả năng giữ điện áp của Keeper ở mạch thử Ex7.1.
3. Vẽ cả hai đường ($t_{pd,eval}$ và $V_{X,min}$) trên cùng một biểu đồ theo `Wkp` để chọn kích thước Keeper tối ưu.

- **Sản phẩm Ex7.3:** Biểu đồ 2 đường trade-off và lựa chọn giá trị Keeper hợp lý.

---

### Ex7.4: Thực nghiệm Chuỗi 2 Tầng Dynamic vs Domino (LTspice)

1. Ghép nối tiếp **2 cổng Dynamic** (`DYN1` và `DYN2`) dùng chung xung nhịp `clk`:
   - **Trường hợp A (Dynamic nối trực tiếp):** Ngõ động $X_1$ của `DYN1` nối thẳng vào ngõ vào của `DYN2` (không qua Inverter). Trong pha Precharge, $X_1 = 5\text{V}$. Khi $CLK$ vừa lên $5\text{V}$ (Evaluate), kích thích ngõ vào `DYN1` để $X_1$ xả về $0\text{V}$. Quan sát dạng sóng $X_2$: giải thích tại sao $X_2$ bị xả sai ngay đầu pha Evaluate trước khi $X_1$ kịp rớt xuống $0\text{V}$.
   - **Trường hợp B (Domino chuẩn):** Chèn Inverter đệm giữa $X_1$ và `DYN2` ($Y_1 = \overline{X_1}$). Quan sát dạng sóng $Y_1$ và $Y_2$ để kiểm chứng tính đơn điệu ($0 \to 1$) loại bỏ lỗi xả sớm.

- **Sản phẩm Ex7.4:** Đồ thị so sánh $X_2$ (Dynamic trực tiếp) vs $Y_2$ (Domino) chứng minh vai trò của Inverter đệm.

---

### Ex7.5: Đối sánh PPA giữa Domino OR4 và Static OR4 (LTspice)

1. Dựng mạch `static_or4` gồm `NOR4` ($4$ NMOS $4\lambda$ song song + $4$ PMOS $48\lambda$ nối tiếp) theo sau bởi `inv_x1` ($16\lambda$).
2. Đặt cả `domino_or4_x1` và `static_or4` dưới **cùng bộ lái đầu vào `inv_x1`** và **cùng tải ngõ ra $C_L = 50\,\text{fF}$**.
3. Đo và so sánh:
   - Tổng bề rộng kênh $\Sigma W$ và bề rộng cổng đầu vào $C_{in}$ trên chân `A`.
   - Trễ truyền lan $t_{pd}$ (sườn lên $Y$ khi $A: 0 \to 1$ hoặc $CLK: 0 \to 1$).
   - Năng lượng tiêu tán mỗi chu kỳ $E_{cycle}$: dùng `.meas tran E_dyn INTEG (-V(vdd)*I(Vdd)) FROM=0 TO=20n`.

- **Sản phẩm Ex7.5:** Bảng đối sánh định lượng Domino OR4 vs Static OR4.

---

## 7. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (POST-LAB)

### 7.1. Hoàn thiện Báo cáo & Nội dung Tùy chọn
1. Hoàn thiện biểu đồ 2 đường trade-off từ Ex7.3 và phân tích bảng so sánh PPA từ Ex7.5.
2. *(Tùy chọn nâng cao - Không bắt buộc):* Thiết kế Layout cho `domino_or4_x1{lay}` bằng kỹ thuật chia sẻ khuếch tán 4 NMOS (`[S] A [D] B [S] C [D] D [S]`, với 3 cực Nguồn nối về `n_eval` và 2 cực Máng nối về `x`), lưu ý dùng Keeper $W_{kp} \ge 3\lambda, L_{kp} \ge 4\lambda$ để vượt qua DRC.

### 7.2. Phiếu báo cáo điền khuyết (Nộp kèm file mô phỏng)

```
========================================================================================
                          BÁO CÁO THỰC HÀNH: BÀI 7
            KỸ THUẬT LOGIC ĐỘNG VÀ LOGIC DOMINO (DYNAMIC & DOMINO CMOS)
Họ và Tên: ..................................................... MSSV: .................
Lớp: ....................................... Nhóm/Bàn: ......... Ngày: .................
Chữ ký Giảng viên / Điểm nghiệm thu tại bàn: ............................................
========================================================================================
```

#### a. Phần Chuẩn bị (Pre-lab)
1. **Tính toán Ngưỡng $V_M$ và Charge Sharing ($C_X = 20\,\text{fF}, C_{int} = 14\,\text{fF}$):**
   - Ngưỡng chuyển mạch Inverter $16\lambda/8\lambda$: $V_M =$ ............ $\text{V}$ (Low-skew / High-skew: ................).
   - $V_X' =$ ............ $\text{V}$; $\Delta V_X =$ ............ $\text{V}$; Lề nhiễu $NM_H = V_X' - V_M =$ ............ $\text{V}$.
   - Điều kiện lật giả ($V_X' \le V_M$): $C_{int} \ge$ ............ $\times C_X$.
   - Với $C_{int}/C_X = 0.1$: công thức cân bằng cho $\Delta V_X =$ ............ $\text{V}$ (so với giới hạn thực của NMOS trên).
2. **Ước lượng tỉ số dòng Keeper / PDN ở $V_X = 2.5\,\text{V}$ ($L_{kp}=2\lambda$):**
   - $W_{kp} = 2\lambda / 4\lambda / 6\lambda / 8\lambda \implies I_{kp}/I_{PDN} \approx$ ............ / ............ / ............ / ............

#### b. Kết quả Đo đạc Thực hành (In-lab)
1. **Ex7.1 — Hiện tượng Chia sẻ Điện tích (`FROM=10.5n TO=19n`):**

| Cấu hình mạch 2-NMOS nối tiếp | Dự đoán Pre-lab $V_X'$ (V) | Đo $V_{X,min}$ (V) | Đo $V_{Y,max}$ (V) | Có bị lật giả không? |
| :--- | :---: | :---: | :---: | :---: |
| **Không có Keeper (`x_nokp`)** | .............. | .............. | .............. | .................... |
| **Có Keeper (`x_kp`, $4\lambda/4\lambda$)** | — | .............. | .............. | .................... |

2. **Ex7.2 — Kiểm chứng 6 tổ hợp `domino_or4_x1` ($t_{pd,eval} =$ ............ ps tại `1000`):**

| Tổ hợp $(A,B,C,D)$ | Cuối Precharge ($9.5\text{ns}$): $V(X) / V(Y)$ | Cuối Evaluate ($19.5\text{ns}$): $V(X) / V(Y)$ | Đúng logic? |
| :---: | :---: | :---: | :---: |
| `0000` | ......... / ......... V | ......... / ......... V | ............ |
| `1000` | ......... / ......... V | ......... / ......... V | ............ |
| `0100` | ......... / ......... V | ......... / ......... V | ............ |
| `0010` | ......... / ......... V | ......... / ......... V | ............ |
| `0001` | ......... / ......... V | ......... / ......... V | ............ |
| `1111` | ......... / ......... V | ......... / ......... V | ............ |

3. **Ex7.3 — Quét kích thước Keeper ($L_{kp} = 2\lambda$):**

| $W_{kp}$ | Độ trễ đánh giá $t_{pd,eval}$ (ps) | Độ sụt áp $V_{X,min}$ ca Charge Sharing (V) | Ghi chú (Đánh giá được / Lỗi `.meas`?) |
| :---: | :---: | :---: | :--- |
| $0.6\,\mu\text{m}$ ($2\lambda$) | .............. | .............. | |
| $1.2\,\mu\text{m}$ ($4\lambda$) | .............. | .............. | |
| $1.8\,\mu\text{m}$ ($6\lambda$) | .............. | .............. | |
| $2.4\,\mu\text{m}$ ($8\lambda$) | .............. | .............. | |

4. **Ex7.4 & Ex7.5 — Chuỗi Domino & Đối sánh PPA Domino OR4 vs Static OR4:**
   - Kết quả Ex7.4: Mức tụt áp sai ở `X2` (Dynamic trực tiếp): ............ V; ở `Y2` (Domino): hoạt động ............
   - Kết quả Ex7.5:

| Chỉ số PPA ($C_L = 50\,\text{fF}$, lái `inv_x1`) | Domino OR4 (`domino_or4_x1`) | Static OR4 (`NOR4 + INV`) | Tỉ lệ cải thiện |
| :--- | :---: | :---: | :---: |
| Số transistor / Tổng $\Sigma W$ | ...... T / ........ $\lambda$ | ...... T / ........ $\lambda$ | |
| Bề rộng cổng đầu vào $C_{in}$ (1 chân) | .............. $\lambda$ | .............. $\lambda$ | |
| Trễ đánh giá / truyền lan $t_{pd}$ (ps) | .............. | .............. | |
| Năng lượng mỗi chu kỳ $E_{cycle}$ (fJ) | .............. | .............. | |

#### c. Câu hỏi Thảo luận Chuyên sâu
1. Tại sao cổng Domino OR4 có Foot NMOS trong Ex7.2 lại **không** gặp hiện tượng chia sẻ điện tích trong pha Evaluate, trong khi mạch thử 2-NMOS nối tiếp ở Ex7.1 lại gặp?
2. Giải thích tại sao Inverter đệm $16\lambda/8\lambda$ lại được gọi là **Low-skew** (có $V_M \approx 2.27\,\text{V}$) và nó ảnh hưởng như thế nào đến khả năng chống nhiễu Charge Sharing của mạch Domino?
3. Nếu không muốn dùng $W_{kp} = 2\lambda$ (vì có thể vi phạm luật chiều rộng Active tối thiểu $3\lambda$ khi vẽ Layout), kỹ sư thiết kế cần điều chỉnh kích thước Keeper theo cách nào để giữ nguyên độ yếu của dòng giữ?

---

## 8. BẢNG KIỂM CHỨNG VÀ ĐỐI CHUẨN KỸ THUẬT (BENCHMARK)

| Thông số kiểm chứng | Dải giá trị kỳ vọng (MOSIS C5N) | Điều kiện kiểm tra |
| :--- | :---: | :--- |
| **Ngưỡng chuyển $V_M$ Inverter $16\lambda/8\lambda$** | $\approx 2.25 - 2.30\,\text{V}$ (lý thuyết $2.27\,\text{V}$) | Low-skew Inverter |
| **Charge Sharing ($C_X=20\text{fF}, C_{int}=14\text{fF}$)** | $V_{X,min} \approx 2.94\,\text{V}$ (không Keeper) | Mạch 2-NMOS nối tiếp, `FROM=10.5n TO=19n` |
| **Ngưỡng Keeper thắng PDN** | Khoảng $W_{kp} \approx 6\lambda - 8\lambda$ ($L=2\lambda$) | 1 nhánh PDN đơn $4\lambda$ + foot $8\lambda$ |
| **$\Sigma W$ và $C_{in}$ (OR4)** | Domino: $\Sigma W \approx 62-64\lambda, C_{in}=4\lambda$ | Static OR4: $\Sigma W = 224\lambda, C_{in}=52\lambda$ |

---

## 9. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP

| Hiện tượng lỗi | Nguyên nhân gốc rễ | Cách khắc phục nhanh |
| :--- | :--- | :--- |
| **Lệnh `.meas` báo `Measurement FAILED` ở mức $W_{kp} = 8\lambda$** | Dòng nạp của Keeper PMOS quá lớn so với nhánh PDN đơn ($\approx 69$%), khiến nút $X$ không kéo xuống dưới ngưỡng $V_M$ nên $Y$ không lật. | Đây là **kết quả vật lý hợp lệ** chứng minh Keeper contention quá mức; ghi nhận trạng thái thất bại vào bảng. |
| **Thử Charge Sharing trên cổng Domino OR4 thấy $V(x)$ không hề sụt** | Mạng OR4 mắc song song, khi $M_{eval}$ mở trong pha Evaluate thì nút `n_eval` nối đất, không có nút nội cô lập. | Phải dùng mạch thử **2-NMOS nối tiếp** (`Mn_top`, `Mn_bot`) như hướng dẫn trong Ex7.1. |
| **Nút động $X$ bị trôi áp bất thường khi tần số xung nhịp thấp** | Do bước tích phân quá lớn hoặc dòng rò nút động làm mất điện tích ở chu kỳ dài. | Đặt bước tích phân chặt `.tran 0 25n 0 10p` và kiểm tra nối đúng Keeper PMOS hồi tiếp từ `y`. |

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

| Tiêu chí đánh giá | Trọng số | Xuất sắc (8.5 – 10) | Khá (7.0 – 8.4) | Đạt (5.0 – 6.9) | Không đạt (< 5.0) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Chuẩn bị Pre-lab** | **20%** | Tính đúng $V_M \approx 2.27\,\text{V}$, đúng $V_X'=2.94\,\text{V}, NM_H=0.67\,\text{V}$, viết được Netlist 2-NMOS và tính tỉ số dòng Keeper. | Tính đúng Charge Sharing và $V_M$, còn sai sót nhỏ ở tỉ số dòng Keeper hoặc phần mở rộng. | Dùng nhầm $V_M = 2.45\,\text{V}$ hoặc thiếu Netlist 2-NMOS. | Không làm Pre-lab hoặc sao chép. |
| **2. Charge Sharing & Domino OR4 (Ex7.1–7.2)** | **25%** | Đo đúng $V_{X,min}, V_{Y,max}$ trên mạch 2-NMOS (có/không Keeper), dựng đúng `domino_or4_x1` ($9\text{T}$) và kiểm chứng 6/6 tổ hợp. | Đo được Charge Sharing và kiểm chứng Domino OR4 nhưng thiếu một vài tổ hợp đo mốc. | Chạy được mô phỏng nhưng đặt cửa sổ `.meas` sai hoặc quên nối `clk` vào Foot. | Không hoàn thành mô phỏng mạch động. |
| **3. Quét Keeper 2 đại lượng (Ex7.3)** | **25%** | Quét đủ 4 mức Keeper, đo và vẽ đủ cả 2 đường ($t_{pd,eval}$ và $V_{X,min}$), giải thích được lỗi `.meas` ở ngưỡng contention cao. | Quét đủ 4 mức Keeper và đo được $t_{pd,eval}$, thiếu đường $V_{X,min}$ hoặc giải thích chưa sâu. | Chỉ chạy được 1–2 điểm quét hoặc không vẽ đồ thị đánh đổi. | Không hoàn thành Ex7.3. |
| **4. Chuỗi Domino & PPA (Ex7.4–7.5)** | **20%** | Chứng minh thực nghiệm lỗi xả sớm khi nối thẳng Dynamic vs Domino, đo đủ trễ, $\Sigma W, C_{in}$ và năng lượng $E_{cycle}$ so với Static OR4. | Hoàn thành Ex7.4 và so sánh trễ/diện tích với Static OR4, thiếu đo năng lượng `.meas INTEG`. | Chỉ làm được Ex7.4 hoặc Ex7.5. | Không hoàn thành cả Ex7.4 và Ex7.5. |
| **5. Báo cáo & Thảo luận** | **10%** | Báo cáo đầy đủ số liệu khớp `.log`, trả lời chính xác 3 câu hỏi thảo luận chuyên sâu. | Báo cáo đầy đủ, trả lời được 2/3 câu hỏi thảo luận. | Báo cáo thiếu số liệu hoặc giải thích sai bản chất Low-skew. | Nộp thiếu báo cáo hoặc số liệu không khớp mô phỏng. |

---

## 11. TÀI LIỆU THAM KHẢO

1. N. H. E. Weste & D. M. Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th Ed., Addison-Wesley (Chương 9: Dynamic & Domino Logic).
2. J. M. Rabaey, A. Chandrakasan & B. Nikolic, *Digital Integrated Circuits: A Design Perspective*, 2nd Ed., Prentice Hall (Chương 6: Designing Combinational Logic Gates — Dynamic CMOS).
3. R. Jacob Baker, *CMOS: Circuit Design, Layout, and Simulation*, 3rd Ed., Wiley-IEEE Press.
4. Thư viện mô hình SPICE chuẩn phòng thí nghiệm: `04 - Models_and_Libraries/C5_models.txt`.
