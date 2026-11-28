# THỰC HÀNH THIẾT KẾ VLSI — BÀI 4 (LAB 04)
# CỔNG TRUYỀN (TRANSMISSION GATE) VÀ BỘ DỒN KÊNH MUX MỨC TRANSISTOR

---
**Bộ môn:** Điện tử – Viễn thông | **Khoa:** Điện – Điện tử  
**Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Thời lượng:** 135 phút thực hành tại phòng máy (kết hợp tự học Pre-lab & hoàn thiện Post-lab)  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07+), LTspice XVII / LTspice 2025  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5µm ($\lambda = 0.30\,\mu\text{m}$, $L_{min} = 0.60\,\mu\text{m}$, $V_{DD} = 5.0\,\text{V}$)  
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Đo và giải thích suy giảm điện áp ngưỡng trên Pass Transistor:** Đo thực nghiệm $V_{out,max}$ của NMOS (Weak '1') và $V_{out,min}$ của PMOS (Weak '0') dưới tác động của hiệu ứng phân cực thân (Body Effect), đối chiếu với giá trị giải tích điểm cố định (fixed-point) từ Pre-lab.
2. **Khảo sát đặc tính điện trở dẫn $R_{TG}(V_{in})$ của Cổng truyền CMOS (Transmission Gate - TG):** Vẽ đường cong $R_{TG}$ theo $V_{in} \in [0, V_{DD}]$, chứng minh khả năng truyền tín hiệu Rail-to-Rail ở tải điện dung và giải thích tại sao $R_{TG}$ duy trì tương đối phẳng quanh $1.0 - 1.7\,\text{k}\Omega$.
3. **Thiết kế và đo kiểm bộ dồn kênh MUX 2:1 và MUX 4:1 mức Transistor:** Xây dựng tế bào `mux2_tg` (6 transistor) và `mux4_tg` (18 transistor, cây phân cấp 3 `mux2_tg`), đo trễ $t_{pd(D0 \to Y)}$, $t_{pd(D1 \to Y)}$, $t_{pd(S \to Y)}$ và quan sát hiện tượng chồng dẫn (contention) khi $S$ chuyển trạng thái.
4. **Thiết kế Mask Layout, kiểm tra DRC/NCC và trích xuất ký sinh PEX:** Bố trí layout 3 cột Poly cho `mux2_tg{lay}`, đạt 0 lỗi DRC và trạng thái NCC trùng khớp (`topologically equivalent (MATCH)`), đồng thời lượng hóa sự gia tăng trễ do tụ ký sinh nút chung `y` (gồm 4 cực má).
5. **Đánh giá trễ chuỗi cổng truyền ghép tầng (Elmore Delay):** Thực nghiệm mô phỏng chuỗi $N = 1 \dots 6$ cổng truyền nối tiếp để kiểm chứng quy luật tăng trễ bậc hai $O(N^2)$ và xác định nhu cầu chèn bộ đệm (Repeater/Inverter).

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

| Hạng mục | Chi tiết |
|---|---|
| **IP kế thừa từ các bài trước** | - Tế bào Inverter chuẩn `inv_x1` (Lab 1): $W_n = 4\lambda = 1.2\,\mu\text{m}, W_p = 12\lambda = 3.6\,\mu\text{m}, L = 2\lambda = 0.6\,\mu\text{m}$.<br>- Thư viện mô hình SPICE: `04 - Models_and_Libraries/C5_models.txt` (NMOS: `N`, PMOS: `P`).<br>- Khung chiều cao cell chuẩn $H_{cell} = 40\lambda = 12.0\,\mu\text{m}$ (hoặc theo chuẩn ray nguồn đã thống nhất). |
| **Sản phẩm bàn giao cuối buổi** | - Tế bào Cổng truyền `tg_gate{sch}` (và `tg_gate{ic}`).<br>- Tế bào MUX 2:1 `mux2_tg{sch}`, `mux2_tg{lay}` (đạt DRC 0 lỗi, NCC MATCH) và `mux2_tg{ic}`.<br>- Tế bào MUX 4:1 `mux4_tg{sch}` và `mux4_tg{ic}`.<br>- Tệp kết quả mô phỏng LTspice (.raw/.log) cho Pass Transistor, $R_{TG}(V_{in})$, MUX2 (bao gồm ca chồng dẫn), MUX4 và chuỗi Elmore (Post-lab). |
| **Kế thừa cho các bài sau** | - `tg_gate{ic}` và `inv_x1{ic}` dùng trực tiếp cho **Bài 5 (D-Latch & D-Flip-Flop)**. <br>- `mux2_tg{ic}` và `mux4_tg{ic}` dùng cho khối chọn đường dữ liệu của **Bài 10 (Capstone ALU 4-bit)**. |

---

## 3. CƠ SỞ LÝ THUYẾT NGẮN GỌN

### 3.1. Giới hạn của Transistor Truyền Đơn Lẻ (Pass Transistor) và Hiệu Ứng Thân

Khi sử dụng một transistor đơn lẻ làm khóa chuyển mạch (Pass Transistor) nối giữa nguồn $V_{in}$ và tụ tải $C_L$, transistor sẽ tự ngắt khi điện áp cổng-nguồn hiệu dụng giảm xuống bằng điện áp ngưỡng, gây ra suy giảm biên độ logic:

1. **NMOS truyền mức '1' (Weak '1'):**
   - Cổng đặt ở $V_G = V_{DD}$, cực má nối $V_{DD}$, cực nguồn nối tụ tải $V_{out}$.
   - Khi $V_{out}$ tăng, cực thân (Bulk) vẫn nối đất ($0\,\text{V}$), tạo ra điện thế phân cực ngược nguồn-thân $V_{SB} = V_{out} > 0$.
   - Theo mô hình hiệu ứng thân:
     $$V_{thn}(V_{SB}) = V_{th0,n} + \gamma_n \left( \sqrt{2\phi_{Fn} + V_{SB}} - \sqrt{2\phi_{Fn}} \right)$$
   - NMOS ngắt khi $V_{GS} = V_{DD} - V_{out} = V_{thn}(V_{out})$, dẫn đến phương trình điểm cố định (fixed-point):
     $$V_{out,max} = V_{DD} - V_{thn}(V_{out,max})$$
   - **Hệ quả:** Với tiến trình có $V_{DD} = 3.3\,\text{V}$, nếu $V_{th0} = 0.6\,\text{V}$ và $\gamma = 0.4\,\text{V}^{1/2}$, $V_{thn}$ tăng lên đáng kể làm $V_{out,max}$ sụt mất hơn $1.0\,\text{V}$. Khi mức Weak '1' này đưa vào cổng Inverter tiếp theo, PMOS của tầng sau không thể ngắt hoàn toàn, gây dòng rò tĩnh và suy giảm lề nhiễu.

2. **PMOS truyền mức '0' (Weak '0'):**
   - Cổng đặt ở $V_G = 0\,\text{V}$, cực má nối đất ($0\,\text{V}$), cực nguồn là $V_{out}$ xả từ $V_{DD}$ xuống.
   - Cực thân (Bulk/N-Well) của PMOS luôn nối lên $V_{DD}$, do đó điện áp phân cực ngược thân-nguồn là $V_{BS} = V_{DD} - V_{out} > 0$.
   - Hiệu ứng thân làm trị tuyệt đối điện áp ngưỡng $|V_{tp}|$ **cũng tăng mạnh** khi $V_{out}$ tiến về $0\,\text{V}$ (vì $V_{BS}$ tiến gần $V_{DD}$!):
     $$|V_{tp}(V_{BS})| = |V_{tp0}| + \gamma_p \left( \sqrt{2\phi_{Fp} + (V_{DD} - V_{out})} - \sqrt{2\phi_{Fp}} \right)$$
   - PMOS ngắt khi $V_{SG} = V_{out} - 0 = |V_{tp}(V_{DD} - V_{out})|$, dẫn đến điện áp đáy cực tiểu:
     $$V_{out,min} = |V_{tp}(V_{DD} - V_{out,min})|$$
   - Sinh viên lưu ý: Không được bỏ qua hiệu ứng thân của PMOS khi tính $V_{out,min}$!

### 3.2. Cổng Truyền CMOS (Transmission Gate - TG) và Điện Trở Dẫn $R_{TG}(V_{in})$

Để khắc phục hiện tượng Weak '1' và Weak '0', **Cổng truyền CMOS (TG)** mắc song song 1 NMOS (điều khiển bởi $EN$) và 1 PMOS (điều khiển bởi $\overline{EN}$):

- **Trạng thái tắt ($EN = 0, \overline{EN} = V_{DD}$):** Cả hai transistor đều ngắt, ngõ ra ở trạng thái trở kháng cao (**Hi-Z**).
- **Trạng thái dẫn ($EN = V_{DD}, \overline{EN} = 0$):** Ở tải điện dung và dòng tải nhỏ, $V_{out}$ tiến tới đầy đủ dải Rail-to-Rail ($0 \leftrightarrow V_{DD}$) nhờ NMOS dẫn tốt ở vùng điện áp thấp và PMOS dẫn tốt ở vùng điện áp cao.

#### Phân tích điện trở tương đương $R_{TG}(V_{in})$:
Trong vùng dẫn tuyến tính ($V_{DS}$ nhỏ), độ dẫn tương đương của TG là tổng độ dẫn hai nhánh:
$$G_{TG}(V_{in}) = G_n(V_{in}) + G_p(V_{in}) = \beta_n (V_{DD} - V_{in} - V_{thn}) + \beta_p (V_{in} - |V_{tp}|)$$
trong đó $\beta_n = K'_n (W/L)_n$ và $\beta_p = K'_p (W/L)_p$.

- Nếu chọn kích thước cân bằng độ linh động ($\beta_n = \beta_p = \beta$, ví dụ $W_n = 4\lambda, W_p = 12\lambda$ khi $K'_n / K'_p = 3$), trong vùng cả hai transistor cùng dẫn ($V_{thn} \le V_{in} \le V_{DD} - |V_{tp}|$) và **bỏ qua hiệu ứng thân**:
  $$G_{TG} = \beta \left( V_{DD} - V_{thn} - |V_{tp}| \right) = \text{hằng số độc lập với } V_{in}$$
- **Lưu ý quan trọng về giá trị giữa dải:** Ở $V_{in} = V_{DD}/2$, điện áp quá cổng $(V_{GS} - V_{th})$ của cả NMOS và PMOS đều giảm xuống khoảng một nửa so với mức tối đa ($V_{DD}$), nên điện trở của mỗi nhánh tăng hơn gấp đôi so với giá trị $R_{on}$ ở biên. Khi mắc song song, điện trở $R_{TG}$ theo mô hình bậc hai (chưa xét body effect) phẳng quanh mức **$1.0 - 1.2\,\text{k}\Omega$** (cao hơn khi tính thêm hiệu ứng thân, đạt đỉnh ở giữa dải khoảng $1.5 - 1.7\,\text{k}\Omega$). Sinh viên sẽ tự vẽ đường cong $R_{TG}(V_{in})$ bằng SPICE trong phần thực hành.

### 3.3. Bộ Dồn Kênh MUX 2:1, MUX 4:1 và Các Hiệu Ứng Ký Sinh

1. **MUX 2:1 dùng Cổng truyền (`mux2_tg`):**
   - Gồm 2 cổng truyền ($TG_0, TG_1$) và 1 cổng Inverter tạo tín hiệu bù $\overline{S}$ (**Tổng: 6 Transistor**, ít hơn đáng kể so với 10–12 transistor của MUX2 cổng tĩnh AOI22+INV).
   - **Tín hiệu không khôi phục (Non-restoring):** Khác với MUX cổng tĩnh, TG MUX là mạch thụ động không có tầng khuếch đại phục hồi mức; tốc độ phụ thuộc trực tiếp vào trở kháng nguồn lái tại $D_0, D_1$ và tụ tải tại $Y$. Do đó, mọi so sánh trễ PPA giữa TG MUX và Static MUX chỉ công bằng khi dùng **cùng bộ lái đầu vào** (ví dụ `inv_x1`) và **cùng tải đầu ra**.
   - **Hiện tượng chồng dẫn (Conduction Overlap / Contention):** Tín hiệu $\overline{S}$ đi qua Inverter nên bị trễ hơn $S$ một khoảng $t_{pd,inv}$. Khi $S$ chuyển từ $0 \to 1$, NMOS của $TG_1$ (nhận $S$) mở ngay lập tức trong khi NMOS của $TG_0$ (nhận $\overline{S}$) chưa kịp tắt hẳn trong khoảng $\Delta t \approx t_{pd,inv}$. Nếu $D_0 \neq D_1$ tại thời điểm chuyển mạch, hai nguồn dữ liệu sẽ tạm thời nối tắt vào nhau qua nút $Y$, tạo ra xung nhiễu (glitch) trên $Y$ và đỉnh dòng rò từ nguồn $V_{DD}$.

2. **MUX 4:1 phân cấp (`mux4_tg`):**
   - Ghép dạng cây gồm 3 tế bào `mux2_tg` (`X_MUX_A`, `X_MUX_B` ở tầng 1 nhận $S_0$; `X_MUX_C` ở tầng 2 nhận $S_1$), tổng cộng **18 Transistor**.
   - Lưu ý: Chân $S_0$ phải lái 2 tế bào MUX ở tầng 1 (tải gấp đôi $S_1$).
   - **Trễ truyền lan qua 2 tầng TG:** Theo mô hình Elmore cho hai điện trở $R$ nối tiếp với tụ nút giữa $C_1$ và tụ tải $C_L$:
     $$t_{pd,MUX4} \approx 0.69 \left( R \cdot C_1 + 2 R \cdot C_L \right) \ge 2 \times t_{pd,TG}$$
     trong đó $C_1$ bao gồm điện dung khuếch tán của 4 cực má (tầng 1) cộng với 2 cực nguồn (tầng 2).

3. **Chuỗi $N$ cổng truyền nối tiếp (Elmore Delay):**
   - Khi nối tiếp $N$ cổng truyền mà không có bộ đệm (buffer), mạng trở thành chuỗi thang $RC$ phân bố với trễ tăng theo quy luật bậc hai:
     $$t_{pd}(N) \approx 0.69 \cdot R_{TG} \cdot C_{node} \cdot \frac{N(N+1)}{2} \propto O(N^2)$$
   - Do đó, trong thiết kế thực tế, không nối quá 3–4 cổng truyền liên tiếp mà cần chèn bộ đệm Inverter để khôi phục sườn xung và đưa trễ về tuyến tính.

---

## 4. CÂU HỎI CHUẨN BỊ TRƯỚC KHI ĐẾN LỚP (PRE-LAB)

> [!IMPORTANT]
> Sinh viên phải hoàn thành toàn bộ phần tính toán và sơ đồ dưới đây trước giờ vào phòng máy để phục vụ **Cổng kiểm tra Pre-lab (10 phút đầu giờ)**.

Sử dụng tham số tiến trình MOSIS C5N trích xuất từ `04 - Models_and_Libraries/C5_models.txt`:  
$V_{DD} = 5.0\,\text{V}$, NMOS (`N`): $V_{th0,n} = 0.70\,\text{V}, K'_n = 120\,\mu\text{A/V}^2, \gamma_n = 0.40\,\text{V}^{1/2}, 2\phi_{Fn} = 0.70\,\text{V}$;  
PMOS (`P`): $|V_{th0,p}| = 0.80\,\text{V}, K'_p = 40\,\mu\text{A/V}^2, \gamma_p = 0.50\,\text{V}^{1/2}, 2\phi_{Fp} = 0.70\,\text{V}$.

1. **Giải bài toán điểm cố định cho Pass Transistor (C5N):**
   - Lập phương trình và giải số (lặp 3–4 bước) để tìm $V_{out,max}$ của NMOS truyền mức '1' (Weak '1').
   - Lập phương trình và giải số để tìm $V_{out,min}$ của PMOS truyền mức '0' (Weak '0') khi Bulk PMOS nối $V_{DD}$.
   - Giải thích tại sao đối với Cổng truyền CMOS lý tưởng ở tải điện dung, ngõ ra đạt $V_{max} = V_{DD}$ và $V_{min} = 0\,\text{V}$; nêu giới hạn thực tế khi có dòng rò hoặc tải điện trở.
2. **Định cỡ Cổng truyền cho một tải cụ thể:**
   - Giả sử cần thiết kế một cổng truyền `TG_FAST` có điện trở dẫn $R_{TG\_FAST}$ bằng **một nửa** điện trở dẫn của Inverter chuẩn `inv_x1` (trong `inv_x1`, $W_n = 4\lambda, W_p = 12\lambda, L = 2\lambda$). Hãy xác định kích thước $(W/L)_n$ và $(W/L)_p$ (theo đơn vị $\lambda$ và $\mu\text{m}$) cho `TG_FAST`.
   - Tính toán giá trị lý thuyết $R_{TG}(V_{in})$ tại 3 điểm: $V_{in} = 0\,\text{V}$, $V_{in} = 2.5\,\text{V}$, $V_{in} = 5.0\,\text{V}$ cho cổng truyền chuẩn ($4\lambda / 12\lambda$, bỏ qua body effect).
3. **Bảng chân trị và Dự đoán chồng dẫn MUX:**
   - Lập bảng chân trị cho `mux2_tg` và `mux4_tg` (sử dụng tên phân cấp: `X_MUX_A.TG0`, `X_MUX_A.TG1`, `X_MUX_B.TG0`, `X_MUX_B.TG1`, `X_MUX_C.TG0`, `X_MUX_C.TG1`).
   - Dự đoán định tính dạng sóng tại $Y$ và dòng nguồn $I(V_{DD})$ khi tín hiệu chọn $S$ chuyển từ $0 \to 1$ trong lúc $D_0 = 5\,\text{V}$ và $D_1 = 0\,\text{V}$.
4. **Phác thảo Stick Diagram cho `mux2_tg`:**
   - Bố trí 2 ray nguồn ngang `vdd` và `gnd`, vùng N-Well cho 3 PMOS, vùng P-substrate cho 3 NMOS.
   - Thiết kế sơ đồ **3 cột Poly**: Cột 1 cho Inverter ($S$), Cột 2 cho tín hiệu $S$, Cột 3 cho tín hiệu $\overline{S}$ (gợi ý: mỗi cột điều khiển chọn lọc 1 NMOS và 1 PMOS của hai TG đối xứng).

---

## 5. KẾ HOẠCH PHÂN BỔ THỜI LƯỢNG IN-LAB (135 PHÚT)

| Phân đoạn | Nội dung thực hiện | Thời lượng |
| :--- | :--- | :---: |
| **Kiểm tra đầu giờ** | Cổng kiểm tra Pre-lab (chấm bài tính tay và Stick Diagram) | 10 phút |
| **Ex4.1** | Mô phỏng Pass Transistor (NMOS, PMOS), TG (4 nhánh) và vẽ đường cong $R_{TG}(V_{in})$ trên LTspice | 20 phút |
| **Ex4.2** | Dựng Schematic `tg_gate{sch}` và `mux2_tg{sch}` trên Electric VLSI, kiểm tra lỗi (`F5`) | 20 phút |
| **Ex4.3** | Mô phỏng quá độ `mux2_tg` (đo $t_{pd(D0\to Y)}$, $t_{pd(D1\to Y)}$, $t_{pd(S\to Y)}$ và ca chồng dẫn khi $D_0 \neq D_1$) | 25 phút |
| **Ex4.4** | Thiết kế phân cấp `mux4_tg{sch}`, chạy kiểm chứng 4 tổ hợp chọn kênh $(S_1, S_0)$ | 10 phút |
| **Ex4.5** | Thiết kế Layout `mux2_tg{lay}` (dựa trên khung ray nguồn chuẩn), chạy DRC và đối chiếu NCC (LVS) | 40 phút |
| **Tổng kết** | Ghi nhận số liệu vào Phiếu báo cáo, đối chiếu bảng đối chuẩn và ký nghiệm thu tại bàn | 10 phút |
| **Tổng cộng** | | **135 phút** |

*(Các nội dung Trích xuất ký sinh PEX, Khảo sát chuỗi Elmore $N = 1 \dots 6$ TG, đóng gói Icon và hoàn thiện câu hỏi thảo luận được thực hiện trong phần **Post-lab**).*

---

## 6. NỘI DUNG THỰC HÀNH TẠI LỚP (IN-LAB)

### Ex4.1: Khảo sát Pass Transistor, Cổng Truyền TG và Đường cong $R_{TG}(V_{in})$ (LTspice)

1. Tạo mạch mô phỏng mới trên LTspice, khai báo `.include "04 - Models_and_Libraries/C5_models.txt"` (hoặc đường dẫn tương ứng trên máy phòng lab) và nguồn `Vdd = 5.0V`.
2. Dựng **4 nhánh thí nghiệm** độc lập với tải $C_L = 50\,\text{fF}$, kích thước chuẩn ($W_n = 1.2\,\mu\text{m}, W_p = 3.6\,\mu\text{m}, L = 0.6\,\mu\text{m}$):
   - **Nhánh 1 (NMOS Pass):** Gate = $5\,\text{V}$, Bulk = $0\,\text{V}$.
   - **Nhánh 2 (PMOS Pass):** Gate = $0\,\text{V}$, Bulk = $5\,\text{V}$.
   - **Nhánh 3 (CMOS TG lý tưởng):** NMOS Gate = $5\,\text{V}$, PMOS Gate = $0\,\text{V}$.
   - **Nhánh 4 (TG sau Inverter lái thực tế):** Dùng một cổng `inv_x1` (tạo từ 1 PMOS $3.6\mu$ và 1 NMOS $1.2\mu$) lái ngõ vào `in` của TG để quan sát ảnh hưởng của trở kháng nguồn lái hữu hạn lên dạng sóng và trễ.
3. Cấp nguồn xung vào `Vin`: `PULSE(0 5.0 5n 0.1n 0.1n 25n 50n)` ($T = 50\,\text{ns}$). Chạy mô phỏng với bước tích phân chặt: `.tran 0 60n 0 10p`.
4. **Cấu hình lệnh `.MEAS` (Lưu ý cửa sổ đo):**
   - Để tránh lấy nhầm điểm làm việc DC ban đầu $V(out\_pmos) = 0\,\text{V}$ tại $t=0$, **bắt buộc** đặt cửa sổ đo sau sườn xuống đầu tiên ($t = 30\,\text{ns}$):
     ```spice
     .meas tran vmax_nmos MAX v(out_nmos) FROM=15n TO=30n
     .meas tran vmin_pmos MIN v(out_pmos) FROM=35n TO=55n
     .meas tran vmax_tg   MAX v(out_tg)   FROM=15n TO=30n
     .meas tran vmin_tg   MIN v(out_tg)   FROM=35n TO=55n
     ```
   - *(Lưu ý: Điện áp nhánh NMOS tiến tiệm cận về giới hạn khi dòng nạp giảm dần nên giá trị đo tại $30\,\text{ns}$ có thể thấp hơn giới hạn tĩnh một lượng nhỏ).*
5. **Đo đường cong $R_{TG}(V_{in})$:**
   - Tạo mạch con đo điện trở tương đương: cấp nguồn áp quét `Vin` từ $0 \to 5.0\,\text{V}$ (bước $0.25\,\text{V}$), đầu ra `out` nối nguồn dòng nhỏ `I_test = 10uA` (hút dòng từ `out` xuống `Vin` hoặc nguồn áp lệch `V_diff = 10mV`: `Vout = Vin - 0.01`).
   - Chạy `.dc Vin 0 5.0 0.25`. Vẽ đồ thị biểu thức `0.01 / I(V_test)` theo `V(in)` để thu được đường cong $R_{TG}(V_{in})$ thực tế có tính đầy đủ hiệu ứng thân.

- **Sản phẩm Ex4.1:** Đồ thị dạng sóng 4 nhánh, giá trị đo `.log` của $V_{max}, V_{min}$ và đồ thị $R_{TG}(V_{in})$.
- **Câu hỏi kiểm tra nhanh:** Tại sao khi đo `MIN v(out_pmos)` trên toàn khoảng `[0, 60n]` lại cho kết quả $0\,\text{V}$ sai lệch hoàn toàn với lý thuyết?

---

### Ex4.2: Thiết kế Schematic `tg_gate{sch}` và `mux2_tg{sch}` (Electric VLSI)

1. **Tế bào Cổng truyền `tg_gate{sch}`:**
   - Mở Electric VLSI (`mocmos`, $\lambda = 0.30\,\mu\text{m}$), tạo Cell `tg_gate`, View `schematic`.
   - Đặt 1 PMOS ($W = 12\lambda = 3.60\,\mu\text{m}, L = 2\lambda = 0.60\,\mu\text{m}$, Bulk nối `vdd`) và 1 NMOS ($W = 4\lambda = 1.20\,\mu\text{m}, L = 2\lambda = 0.60\,\mu\text{m}$, Bulk nối `gnd`).
   - Nối chập Source tạo `in`, Drain tạo `out`.
   - Tạo 6 chân Export (`Ctrl+E`): `in` (Bidirectional), `out` (Bidirectional), `en` (Input - vào Gate NMOS), `en_n` (Input - vào Gate PMOS), `vdd` (Power), `gnd` (Ground).
   - Nhấn `F5` (Check Schematic) đảm bảo 0 errors, 0 warnings. Tạo biểu tượng `tg_gate{ic}` (có thể dùng khung chuẩn hoặc hình 2 tam giác đối xứng).

2. **Tế bào MUX 2:1 `mux2_tg{sch}`:**
   - Tạo Cell `mux2_tg{sch}`. Gọi 2 instance của `tg_gate{ic}` (`X_TG0`, `X_TG1`) và 1 instance `inv_x1{ic}` (tạo tín hiệu đảo `s_n` từ `s`).
   - Đấu nối theo bảng ánh xạ chuẩn:
     * `X_TG0`: `in` $\leftarrow$ `d0`, `out` $\to$ `y`, `en` $\leftarrow$ `s_n`, `en_n` $\leftarrow$ `s`.
     * `X_TG1`: `in` $\leftarrow$ `d1`, `out` $\to$ `y`, `en` $\leftarrow$ `s`, `en_n` $\leftarrow$ `s_n`.
   - Tạo 6 Export: `d0`, `d1`, `s` (Input), `y` (Output), `vdd`, `gnd`. Nhấn `F5` kiểm tra 0 lỗi. Tạo icon `mux2_tg{ic}`.

- **Sản phẩm Ex4.2:** Schematic `tg_gate{sch}` và `mux2_tg{sch}` đạt 0 lỗi kiểm tra `F5`.

---

### Ex4.3: Mô phỏng Chức năng, Đo Trễ và Kiểm chứng Chồng dẫn `mux2_tg` (LTspice)

1. Xuất SPICE Netlist từ `mux2_tg{sch}` (lưu ý đặt nguồn cấp `Vdd = 5.0V` và tải `CL y 0 50fF`). Để đánh giá trung thực mạch thụ động, khuyến khích dùng bộ đệm `inv_x1` (hoặc nguồn xung $t_r = t_f = 0.1\,\text{ns}$) lái $D_0, D_1$.
2. **Ca đo 1 — Chức năng dồn kênh và trễ dữ liệu ($D_0 \to Y, D_1 \to Y$):**
   - Cấp xung lệch pha để tránh sườn $S$ trùng với sườn $D_0, D_1$:
     ```spice
     Vd0 d0 0 PULSE(0 5.0 2n 0.1n 0.1n 18n 40n)
     Vd1 d1 0 PULSE(0 5.0 5n 0.1n 0.1n 10n 20n)
     Vs  s  0 PULSE(0 5.0 30n 0.1n 0.1n 40n 80n)
     .tran 0 120n 0 10p
     ```
   - Dùng `.meas` đo $t_{pHL}, t_{pLH}$ và $t_{pd}$ cho đường $D_0 \to Y$ (khi $S=0$, trong khoảng `[0, 30n]`) và $D_1 \to Y$ (khi $S=1$, trong khoảng `[30n, 70n]`) với ngưỡng `{0.5*5.0} = 2.5V`.
3. **Ca đo 2 — Trễ đường chọn $S \to Y$ và Hiện tượng chồng dẫn (Contention):**
   - Thiết lập kịch bản riêng: giữ cố định $D_0 = 5.0\,\text{V}$ và $D_1 = 0.0\,\text{V}$ ($D_0 \neq D_1$), cấp xung `Vs` chuyển từ $0 \to 5.0\,\text{V}$ tại $t = 20\,\text{ns}$ (`PULSE(0 5.0 20n 0.1n 0.1n 20n 40n)`).
   - Đo trễ $t_{pd(S \to Y)}$ từ $V(s) = 2.5\,\text{V}$ đến $V(y) = 2.5\,\text{V}$.
   - Phóng to vùng chuyển mạch quanh $t = 20\,\text{ns}$: quan sát đồ thị $V(s)$, $V(s\_n)$, dạng sóng $V(y)$ (tìm glitch/bậc thang) và dòng nguồn $I(V_{dd})$ hoặc dòng qua các nguồn $D_0, D_1$ để xác nhận khoảng chồng dẫn $\Delta t \approx t_{pd,inv}$.

- **Sản phẩm Ex4.3:** Bảng số liệu trễ 3 đường truyền và ảnh chụp phóng to vùng chồng dẫn ($D_0 \neq D_1$).
- **Câu hỏi kiểm tra nhanh:** Tại sao trong ca đo 1 không nên để sườn $S$ trùng đúng thời điểm $D_0$ và $D_1$ vừa cùng đổi mức?

---

### Ex4.4: Thiết kế Phân cấp Bộ Dồn Kênh MUX 4:1 (`mux4_tg{sch}`)

1. Tạo Cell `mux4_tg{sch}`. Gọi 3 instance của `mux2_tg{ic}`:
   - Tầng 1: `X_MUX_A` (nhận `d0, d1`, chọn `s0`), `X_MUX_B` (nhận `d2, d3`, chọn `s0`).
   - Tầng 2: `X_MUX_C` (nhận `y_a`, `y_b`, chọn `s1`), xuất ra `y`.
2. Tạo đầy đủ 9 chân Export: `d0, d1, d2, d3, s0, s1, y, vdd, gnd`. Nhấn `F5` kiểm tra 0 lỗi.
3. Xuất Netlist, mô phỏng kiểm chứng chức năng chọn 4 kênh $(S_1, S_0) \in \{00, 01, 10, 11\}$ với $C_L = 50\,\text{fF}$.
4. Đo trễ $t_{pd(D0 \to Y)}$ của `mux4_tg` và đối chiếu với $2 \times t_{pd,MUX2}$ (xác nhận bất đẳng thức Elmore $t_{pd,MUX4} \ge 2 \cdot t_{pd,TG}$).

- **Sản phẩm Ex4.4:** Schematic `mux4_tg{sch}`, kết quả mô phỏng kiểm chứng 4 kênh và số đo $t_{pd(D0 \to Y)}$ của MUX4.

---

### Ex4.5: Thiết kế Mask Layout `mux2_tg{lay}`, Kiểm tra DRC & NCC (Electric VLSI)

1. Tạo Cell Layout `mux2_tg{lay}` (hoặc mở khung chuẩn có sẵn ray nguồn `vdd`/`gnd` cao $H_{cell} = 40\lambda$, N-Well, Well Tap và Substrate Tap để kịp tiến độ 40 phút).
2. **Bố trí 3 cột Polysilicon:**
   - Đặt 3 PMOS ($W = 12\lambda$) trong vùng N-Well phía trên và 3 NMOS ($W = 4\lambda$) phía dưới:
     * **Cột 1 (Inverter):** Poly thẳng nối cổng PMOS và NMOS nhận tín hiệu `s`, ngõ ra nối tạo node nội `s_n`.
     * **Cột 2 (Tín hiệu `s`):** Poly nối chung Gate NMOS của `X_TG1` và Gate PMOS của `X_TG0` (có thể đảo vị trí N/P tùy cách đi dây, miễn đúng logic).
     * **Cột 3 (Tín hiệu `s_n`):** Poly nối chung Gate NMOS của `X_TG0` và Gate PMOS của `X_TG1`.
   - *Lưu ý luật thiết kế DRC:* Nếu giữa 2 cột Poly có đặt Contact khuếch tán, khoảng cách tâm-tâm giữa hai Poly phải đủ rộng (thường $\ge 6\lambda_{DR}$ theo luật SCMOS để không vi phạm khoảng cách Contact-to-Poly).
3. **Định tuyến đối xứng cực Source/Drain:**
   - Cực Source và Drain của TG có tính chất vật lý đối xứng, tuy nhiên cần gắn nhãn Export `d0`, `d1`, `y` nhất quán với Schematic (chập cực Drain hai TG ra `y`) để công cụ NCC nhận diện đúng chân.
   - Đảm bảo đầy đủ Tap nối `vdd` (trong N-Well) và `gnd` (ngoài N-Well).
4. **Kiểm chứng vật lý:**
   - Nhấn `F5` (DRC): đạt **0 errors found**.
   - Chạy *Tools $\to$ NCC $\to$ Schematic and Layout View Comparison*: kết quả báo **"topologically equivalent (MATCH)"**. Đo kích thước thực tế $W_{cell}, H_{cell}$.

- **Sản phẩm Ex4.5:** Layout `mux2_tg{lay}` đạt 0 lỗi DRC và NCC MATCH.

---

## 7. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (POST-LAB)

### 7.1. Thực nghiệm Post-lab bắt buộc
1. **Phân tích đóng góp ký sinh PEX cho `mux2_tg` (3 lần chạy):**
   - Xuất Netlist trích xuất ký sinh từ `mux2_tg{lay}` và chạy lại ca đo $D_0 \to Y$ và $S \to Y$ ($C_L = 50\,\text{fF}$) ở 3 chế độ:
     * *(1) Pre-layout* (chỉ có $W, L$).
     * *(2) Post-layout chỉ có diện tích/chu vi cực máng-nguồn* (`AS/AD/PS/PD`).
     * *(3) Post-layout đầy đủ* (bao gồm cả điện dung dây nối kim loại/Poly).
   - Nhận xét sự gia tăng tụ ký sinh tại nút chung `y` (nơi hội tụ 4 cực khuếch tán của 2 TG).
2. **Thí nghiệm chuỗi $N$ Cổng truyền nối tiếp (Elmore Delay $O(N^2)$):**
   - Trong LTspice, mắc nối tiếp chuỗi $N = 1, 2, 3, 4, 5, 6$ tế bào `tg_gate` (ở trạng thái dẫn $EN=5\text{V}, \overline{EN}=0\text{V}$), tại mỗi nút trung gian nối tụ ký sinh giả lập $C_{node} = 10\,\text{fF}$, ngõ ra cuối cùng nối $C_L = 10\,\text{fF}$.
   - Đo thời gian trễ $t_{pd}(N)$ tương ứng với $N = 1 \dots 6$.
   - Vẽ đồ thị $t_{pd}$ theo $N$ và theo $N(N+1)/2$ (hoặc $N^2$) để chứng minh độ tăng bậc hai. Đề xuất vị trí chèn bộ đệm `inv_x1` để cải thiện tốc độ.

### 7.2. Phiếu báo cáo điền khuyết (Nộp kèm file mô phỏng)

```
========================================================================================
                          BÁO CÁO THỰC HÀNH: BÀI 4
        CỔNG TRUYỀN (TRANSMISSION GATE) VÀ BỘ DỒN KÊNH MUX MỨC TRANSISTOR
Họ và Tên: ..................................................... MSSV: .................
Lớp: ....................................... Nhóm/Bàn: ......... Ngày: .................
Chữ ký Giảng viên / Điểm nghiệm thu tại bàn: ............................................
========================================================================================
```

#### a. Kết quả chuẩn bị (Pre-lab)
1. **Tính toán Body Effect (C5N):**
   - NMOS Weak '1': $V_{thn,eff} =$ ............... $\text{V}$ $\implies V_{out,max} =$ ............... $\text{V}$.
   - PMOS Weak '0': $|V_{tp,eff}| =$ ............... $\text{V}$ $\implies V_{out,min} =$ ............... $\text{V}$.
2. **Định cỡ `TG_FAST` ($R = 0.5 \times R_{inv}$):**
   - $W_n =$ ............ $\lambda$ ($........\,\mu\text{m}$), $W_p =$ ............ $\lambda$ ($........\,\mu\text{m}$), $L =$ ............ $\lambda$.
   - Giá trị $R_{TG}$ lý thuyết (không body effect) tại $V_{in} = 0\text{V} / 2.5\text{V} / 5.0\text{V}$: ............ / ............ / ............ $\Omega$.
3. **Bảng chân trị `mux4_tg` (ghi rõ tên instance TG dẫn):**

| $S_1$ | $S_0$ | TG dẫn ở Tầng 1 | TG dẫn ở Tầng 2 | Ngõ ra $Y$ |
| :-: | :-: | :---: | :---: | :---: |
| 0 | 0 | .................... | .................... | .................... |
| 0 | 1 | .................... | .................... | .................... |
| 1 | 0 | .................... | .................... | .................... |
| 1 | 1 | .................... | .................... | .................... |

#### b. Kết quả Đo đạc Thực hành (In-lab & Post-lab)
1. **Pass Transistor vs Transmission Gate ($C_L = 50\,\text{fF}$):**

| Nhánh mạch đo | Dự đoán Pre-lab ($V_{min}/V_{max}$) | Đo LTspice $V_{min}$ (V) | Đo LTspice $V_{max}$ (V) | Biên độ đỉnh-đỉnh (V) |
| :--- | :---: | :---: | :---: | :---: |
| **NMOS Pass Transistor** | ........ / ........ | ................ | ................ | ................ |
| **PMOS Pass Transistor** | ........ / ........ | ................ | ................ | ................ |
| **CMOS TG (lý tưởng)** | ........ / ........ | ................ | ................ | ................ |
| **CMOS TG (sau `inv_x1`)**| — | ................ | ................ | ................ |

*(Ghi nhận giá trị đo $R_{TG}$ thực tế từ đồ thị DC: tại $0\text{V} =$ ......... $\Omega$; tại $2.5\text{V} =$ ......... $\Omega$; tại $5.0\text{V} =$ ......... $\Omega$).*

2. **Thời gian trễ và Chồng dẫn của `mux2_tg` & `mux4_tg` ($C_L = 50\,\text{fF}$):**

| Đường truyền tín hiệu | $t_{pHL}$ (ps) | $t_{pLH}$ (ps) | $t_{pd}$ (ps) | Ghi chú / Hiện tượng |
| :--- | :---: | :---: | :---: | :--- |
| `mux2_tg`: $D_0 \to Y$ ($S=0$) | .............. | .............. | .............. | |
| `mux2_tg`: $D_1 \to Y$ ($S=1$) | .............. | .............. | .............. | |
| `mux2_tg`: $S \to Y$ ($D_0 \neq D_1$) | .............. | .............. | .............. | Độ rộng glitch $\Delta t \approx$ ........ ps; $I_{peak} \approx$ ........ $\mu\text{A}$ |
| `mux4_tg`: $D_0 \to Y$ ($S_1S_0=00$) | .............. | .............. | .............. | Tỉ lệ $t_{pd,MUX4} / t_{pd,MUX2} =$ .......... |

3. **Tách đóng góp ký sinh PEX cho `mux2_tg` ($D_0 \to Y$):**

| Chế độ mô phỏng | $t_{pHL}$ (ps) | $t_{pLH}$ (ps) | $t_{pd}$ (ps) | Tăng so với Pre-layout (%) |
| :--- | :---: | :---: | :---: | :---: |
| (1) Pre-layout | .............. | .............. | .............. | 0% |
| (2) Post-layout (chỉ `AS/AD/PS/PD`) | .............. | .............. | .............. | .............. % |
| (3) Post-layout (đầy đủ C dây) | .............. | .............. | .............. | .............. % |

4. **Kiểm tra vật lý Layout `mux2_tg{lay}`:**
   - DRC (`F5`): `....................................` | NCC (LVS): `....................................`
   - Kích thước đo: $W =$ ............ $\lambda$ ($........\,\mu\text{m}$), $H = H_{cell} =$ ............ $\lambda$ ($........\,\mu\text{m}$), Diện tích = ............ $\mu\text{m}^2$.

5. **Thí nghiệm Chuỗi $N$ Cổng truyền nối tiếp ($C_{node} = 10\,\text{fF}$):**

| Số tầng $N$ | 1 | 2 | 3 | 4 | 5 | 6 |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: |
| $t_{pd}(N)$ (ps) | ...... | ...... | ...... | ...... | ...... | ...... |
| Tỉ số $t_{pd}(N) / t_{pd}(1)$ | 1.0 | ...... | ...... | ...... | ...... | ...... |

#### c. Câu hỏi Thảo luận Chuyên sâu
1. Dựa vào bảng số liệu thí nghiệm chuỗi $N = 1 \dots 6$ TG, hãy vẽ đồ thị $t_{pd}(N)$ theo $N$ và theo $N(N+1)/2$. Giải thích bản chất vật lý Elmore tại sao trễ tăng theo $O(N^2)$ và đề xuất vị trí chèn Inverter hợp lý nhất.
2. Tại sao trong sơ đồ `tg_gate` và `mux2_tg`, cực Bulk của PMOS bắt buộc phải nối lên $V_{DD}$ mà không được nối trực tiếp vào cực Source hay cực Drain của chính nó? Điều gì xảy ra khi điện áp ngõ vào tụt xuống $0\,\text{V}$ nếu vi phạm quy tắc này?
3. Giải thích cơ chế vật lý tạo nên đường cong điện trở $R_{TG}(V_{in})$ đạt cực đại quanh vùng giữa dải ($V_{in} \approx V_{DD}/2$) khi tính đầy đủ hiệu ứng thân, trái ngược với giả định $R_{TG} = R_{on,n}(0\text{V}) \parallel R_{on,p}(5\text{V})$.
4. Khi so sánh tốc độ giữa `mux2_tg` và `MUX2` cổng logic tĩnh (`AOI22+INV`), tại sao không thể kết luận một cách hoàn toàn rằng `mux2_tg` luôn nhanh hơn khi chưa biết rõ trở kháng bộ lái đầu vào và số tầng mắc nối tiếp?

---

## 8. BẢNG KIỂM CHỨNG VÀ ĐỐI CHUẨN KỸ THUẬT (BENCHMARK)

*(Sinh viên tự đối chiếu kết quả đo của mình với dải giá trị tham chiếu lý thuyết/tiêu chuẩn nghiệm thu dưới đây. Sai số cho phép do đặc trưng mô hình Level 3 và điều kiện sườn xung $\pm 15 - 20$%).*

| Thông số kiểm chứng | Dải giá trị kỳ vọng (MOSIS C5N) | Điều kiện kiểm tra |
| :--- | :---: | :--- |
| **NMOS Weak '1' ($V_{out,max}$)** | $\approx 3.7 - 3.9\,\text{V}$ (lý thuyết $3.79\,\text{V}$) | $V_{DD} = 5\text{V}, \gamma_n = 0.40\,\text{V}^{1/2}$, đo tại cuối bán chu kỳ |
| **PMOS Weak '0' ($V_{out,min}$)** | $\approx 1.3 - 1.5\,\text{V}$ (lý thuyết $1.42\,\text{V}$) | $V_{DD} = 5\text{V}, \gamma_p = 0.50\,\text{V}^{1/2}$, đo `FROM=35n TO=55n` |
| **CMOS TG Swing ($V_{min} / V_{max}$)** | $0.00\,\text{V}$ / $5.00\,\text{V}$ | Tải điện dung thuần $C_L = 50\,\text{fF}$ |
| **Điện trở $R_{TG}$ giữa dải ($2.5\text{V}$)** | $\approx 1.19\,\text{k}\Omega$ (không body) $\to \sim 1.6 - 1.8\,\text{k}\Omega$ (thực tế) | Quét DC $V_{in} = 0 \to 5\text{V}$ |
| **Số lượng Transistor** | `mux2_tg`: $6\text{T}$; `mux4_tg`: $18\text{T}$ | Sơ đồ chuẩn không thừa linh kiện |
| **Trạng thái Layout `mux2_tg`** | 0 errors DRC, `topologically equivalent (MATCH)` | Electric VLSI, 3 cột Poly, $W \approx 28 - 32\lambda$ |

---

## 9. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP

| Hiện tượng lỗi | Nguyên nhân gốc rễ | Cách khắc phục nhanh |
| :--- | :--- | :--- |
| **Lệnh `.meas vmin_pmos` trả về đúng `0.000 V`** | Đo trên toàn khoảng thời gian `[0, 60n]` bị dính giá trị điểm làm việc DC ban đầu tại $t = 0$. | Thêm từ khóa `FROM=35n TO=55n` để đo sau sườn xuống đầu tiên của `Vin`. |
| **Ngõ ra `y` của `mux2_tg` bị sụt áp hoặc có xung nhọn (glitch) lớn khi $S$ đổi** | (1) Hiện tượng chồng dẫn ngắn khi $D_0 \neq D_1$ do $S\_n$ trễ hơn $S$.<br>(2) Đấu ngược cực điều khiển `en`/`en_n` ở một trong hai TG khiến cả hai cùng bật hoặc cùng tắt. | Kiểm tra lại kết nối: `X_TG0` (`en=s_n, en_n=s`), `X_TG1` (`en=s, en_n=s_n`). Nếu chỉ bị glitch ngắn cỡ $30-50\,\text{ps}$ lúc chuyển $S$, đó là chồng dẫn tự nhiên. |
| **NCC báo lỗi không khớp chân (`Pin mismatch`) dù đủ 6 transistor** | Cổng truyền có cực S và D đối xứng; trong Layout đặt ngược vị trí `d0`/`d1` với `y` so với Schematic, hoặc quên xuất chân Export `s`, `y`. | Kiểm tra lại tên Export trên đường Metal trong `mux2_tg{lay}`, bảo đảm hai cực nối chung ở giữa phải gắn Export `y`. |
| **DRC báo vi phạm khoảng cách Polysilicon** | Khoảng cách giữa 2 cột Poly có đặt Contact khuếch tán ở giữa nhỏ hơn luật $6\lambda_{DR}$. | Dãn khoảng cách giữa hai dải Poly có chứa Contact đạt tối thiểu $6\lambda_{DR}$ ($1.80\,\mu\text{m}$). |
| **DRC báo lỗi `N-Well` / `Substrate Tap`** | Quên đặt Tap nối `vdd` trong vùng N-Well hoặc Tap nối `gnd` ngoài vùng N-Well cho mạch TG. | Đặt bổ sung đủ $N^+$-tap lên ray `vdd` và $P^+$-tap xuống ray `gnd`. |

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

*(Áp dụng chuẩn đầu ra học phần: đánh giá dựa trên minh chứng định lượng đo được tại bàn và báo cáo Post-lab).*

| Tiêu chí đánh giá | Trọng số | Xuất sắc (8.5 – 10) | Khá (7.0 – 8.4) | Đạt (5.0 – 6.9) | Không đạt (< 5.0) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Chuẩn bị Pre-lab** | **20%** | Giải đúng phương trình điểm cố định (sai số $\le 5$%), định cỡ đúng `TG_FAST`, điền đủ bảng chân trị MUX4 và vẽ Stick 3 cột Poly hợp lệ. | Tính đúng body effect nhưng sai định cỡ `TG_FAST` hoặc Stick Diagram thiếu kết nối nhỏ. | Có bài chuẩn bị nhưng bỏ qua body effect của PMOS hoặc thiếu bảng chân trị. | Không hoàn thành Pre-lab hoặc sao chép. |
| **2. Khảo sát Pass Transistor & $R_{TG}$ (Ex4.1)** | **20%** | Đo đủ 4 nhánh với cửa sổ `.meas` chuẩn (chênh lệch $\le 15$% so với benchmark) và vẽ thành công đường cong $R_{TG}(V_{in})$. | Đo đúng Weak '1'/Weak '0' và TG, nhưng đường cong $R_{TG}(V_{in})$ chưa rõ hoặc thiếu nhánh 4. | Chạy được mô phỏng nhưng mắc lỗi `.meas vmin_pmos = 0V` do quên đặt cửa sổ đo. | Không chạy được mô phỏng LTspice. |
| **3. Schematic & Đo kiểm MUX2/MUX4 (Ex4.2–4.4)** | **25%** | Dựng đúng `tg_gate`, `mux2_tg` (6T), `mux4_tg` (18T); đo đủ 3 đường trễ MUX2, đo được glitch/dòng chồng dẫn khi $D_0 \neq D_1$, đo trễ MUX4. | Dựng đúng schematic và đo đủ 3 đường trễ MUX2, thiếu định lượng ca chồng dẫn hoặc trễ MUX4. | Dựng đúng mạch nhưng chọn pha xung sai nên không đo được $t_{pd(S \to Y)}$. | Mạch MUX sai logic hoặc không xuất được Netlist. |
| **4. Layout `mux2_tg`, DRC & NCC (Ex4.5)** | **20%** | Layout 3 cột Poly gọn gàng ($W \le 34\lambda$), **0 lỗi DRC**, NCC báo **MATCH** độc lập. | Đạt **0 lỗi DRC** và NCC **MATCH**, kích thước layout còn rộng ($W > 34\lambda$). | Layout hoàn thành nhưng còn $\le 2$ lỗi DRC nhỏ hoặc phải sửa dây mới đạt MATCH. | Không hoàn thành layout hoặc NCC báo MISMATCH. |
| **5. Post-lab PEX, Elmore & Báo cáo** | **15%** | Tách đủ 3 lần chạy PEX, đo và vẽ đúng đồ thị Elmore $N = 1 \dots 6$ (khớp $O(N^2)$), trả lời thấu đáo 4 câu hỏi thảo luận. | Hoàn thành PEX và chuỗi Elmore nhưng giải thích câu hỏi chuyên sâu chưa đầy đủ. | Chỉ làm phần điền khuyết In-lab, thiếu thí nghiệm chuỗi Elmore hoặc thiếu tách 3 bước PEX. | Nộp thiếu báo cáo hoặc số liệu không khớp file mô phỏng. |

---

## 11. TÀI LIỆU THAM KHẢO

1. N. H. E. Weste & D. M. Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th Ed., Addison-Wesley (Chương 1, 4 & 9: Pass Transistors, Transmission Gates, Muxes).
2. J. M. Rabaey, A. Chandrakasan & B. Nikolic, *Digital Integrated Circuits: A Design Perspective*, 2nd Ed., Prentice Hall (Chương 6: Designing Combinational Logic Gates — Pass-Transistor Logic & Elmore Delay).
3. R. Jacob Baker, *CMOS: Circuit Design, Layout, and Simulation*, 3rd Ed., Wiley-IEEE Press (Hướng dẫn công cụ Electric VLSI & LTspice với tiến trình C5N).
4. Thư viện mô hình SPICE chuẩn phòng thí nghiệm: `04 - Models_and_Libraries/C5_models.txt`.
