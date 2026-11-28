# THỰC HÀNH THIẾT KẾ VLSI — BÀI 6 (LAB 06)
# THIẾT KẾ MẠCH CỘNG TOÀN PHẦN 1-BIT (MIRROR ADDER 28T VÀ TG ADDER)

---
**Bộ môn:** Điện tử – Viễn thông | **Khoa:** Điện – Điện tử  
**Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Thời lượng:** 135 phút thực hành tại phòng máy (kết hợp tự học Pre-lab & hoàn thiện Post-lab)  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07+), LTspice XVII / LTspice 2025  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5µm ($\lambda = 0.30\,\mu\text{m}$, $L_{min} = 0.60\,\mu\text{m}$, $V_{DD} = 5.0\,\text{V}$)  
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Đếm và định cỡ transistor cho Mirror Adder 28T:** Thiết lập phương trình chuẩn $\overline{C_{out}}$ và $\overline{Sum}$ (tái sử dụng $\overline{C_{out}}$), đếm đúng $28$ transistor ($12\text{T}$ khối Carry + $16\text{T}$ khối Sum) và định cỡ độ rộng kênh $W$ đảm bảo sức kéo tương đương Inverter chuẩn `inv_x1`.
2. **Dựng Schematic và kiểm chứng 8 tổ hợp logic:** Xây dựng `mirror_adder_1b{sch}` và `tg_adder_1b{sch}` (sử dụng `tg_gate` và `inv_x1`), kiểm chứng đầy đủ 8 trạng thái bảng chân trị bằng lệnh lấy mẫu `.meas FIND` và nhận diện xung nhiễu (glitch) khi nhiều ngõ vào đổi cùng lúc.
3. **Đo trễ các đường truyền lan và khảo sát vị trí chân $C_{in}$:** Đo $t_{pd}$ của bốn đường tín hiệu ($C_{in} \to C_{out}$, $A \to C_{out}$, $C_{in} \to Sum$, $A \to Sum$), giải thích đường nào chậm nhất và thực nghiệm đảo vị trí transistor $C_{in}$ (sát ngõ ra so với sát nguồn/đất) để đánh giá ảnh hưởng lên trễ.
4. **Đo trễ chuỗi Bộ cộng gợn sóng 4-bit (4-bit RCA):** Ghép nối $N = 1, 2, 3, 4$ tầng Full Adder, đo $t_{chain}(N)$ để kiểm chứng quy luật tăng trễ tuyến tính $O(N)$ của Mirror Adder so với suy giảm của TG Adder khi chưa có bộ đệm, đồng thời đóng gói Icon `full_adder_1b{ic}` phục vụ **Bài 10 (Capstone ALU 4-bit)**.

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

| Hạng mục | Chi tiết |
|---|---|
| **IP kế thừa từ các bài trước** | - Tế bào Inverter chuẩn `inv_x1` (Bài 1): $W_n = 4\lambda = 1.2\,\mu\text{m}, W_p = 12\lambda = 3.6\,\mu\text{m}, L = 2\lambda = 0.6\,\mu\text{m}$.<br>- Tế bào Cổng truyền `tg_gate` (Bài 4 — hoặc bản dựng sẵn trong gói thư viện Lab 6).<br>- Thư viện mô hình SPICE: `04 - Models_and_Libraries/C5_models.txt` (NMOS: `N`, PMOS: `P`). |
| **Sản phẩm bàn giao cuối buổi** | - Tế bào Mirror Adder `mirror_adder_1b{sch}` và `mirror_adder_1b{ic}` ($28$ transistor).<br>- Tế bào TG Full Adder `tg_adder_1b{sch}` ($22$ transistor theo khối ghép chuẩn `xor_tg`).<br>- Kết quả mô phỏng LTspice (.raw/.log) cho 8 tổ hợp, 4 đường trễ, thí nghiệm đảo vị trí $C_{in}$, và chuỗi RCA $N = 1 \dots 4$. |
| **Kế thừa cho các bài sau** | - `full_adder_1b{ic}` (`mirror_adder_1b{ic}`) và số đo trễ $t_{pd(Cin \to Cout)}, t_{pd(Cin \to Sum)}$ dùng cho **Bài 9 (4-bit CLA)** và **Bài 10 (Capstone ALU 4-bit)**. |

---

## 3. CƠ SỞ LÝ THUYẾT NGẮN GỌN

### 3.1. Hàm Logic của Bộ Cộng Toàn Phần 1-bit

Mạch cộng toàn phần 1-bit nhận 3 ngõ vào $A, B, C_{in}$ và xuất ra Tổng $Sum$ cùng Số nhớ $C_{out}$:

$$Sum = A \oplus B \oplus C_{in}$$
$$C_{out} = A \cdot B + C_{in} \cdot (A + B)$$

### 3.2. Kiến trúc Mạch Cộng Gương 28-Transistor (Mirror Adder)

**Mirror Adder** là cấu trúc Full Adder cổng tĩnh khôi phục mức (level-restoring) phổ biến trong các thư viện tế bào chuẩn.

1. **Khối tạo số nhớ mang đi ($\overline{C_{out}}$ và $C_{out}$):**
   $$\overline{C_{out}} = \overline{A \cdot B + C_{in} \cdot (A + B)}$$
   - **Mạng PDN (5 NMOS):** Gồm nhánh $A$ nối tiếp $B$ mắc song song với nhánh $C_{in}$ nối tiếp cụm $(A \parallel B)$.
   - **Mạng PUN (5 PMOS):** Nhờ tính chất **tự đối ngẫu (self-dual)** của hàm đa số $C_{out}$, mạng PUN sử dụng **cùng cấu trúc topo** với PDN: nhánh $A$ nối tiếp $B$ mắc song song với nhánh $C_{in}$ nối tiếp cụm $(A \parallel B)$. Việc PDN và PUN có cấu trúc giống hệt nhau (đối xứng qua gương) giúp điện dung các chân $A, B, C_{in}$ cân bằng giữa N và P và dùng chung một đường đi Euler.
   - Thêm 1 Inverter đệm (`INV_Cout`, 2T) để tạo $C_{out}$ $\implies$ **Tổng khối Carry: $5\text{N} + 5\text{P} + 2\text{T} = 12$ Transistors**.

2. **Khối tạo tổng ($\overline{Sum}$ và $Sum$):**
   Tái sử dụng tín hiệu bù $\overline{C_{out}}$ giúp rút gọn đáng kể số transistor:
   $$Sum = A \cdot B \cdot C_{in} + \overline{C_{out}} \cdot (A + B + C_{in})$$
   - Hàm $Sum$ trên chính là biểu thức của **mạng PDN**; do tính chất đảo của cổng CMOS tĩnh, nút ngõ ra của tầng sẽ là $\overline{Sum}$:
     $$\overline{Sum} = \overline{A \cdot B \cdot C_{in} + \overline{C_{out}} \cdot (A + B + C_{in})}$$
   - **Mạng PDN (7 NMOS) và PUN (7 PMOS):** Cùng cấu trúc gồm nhánh 3 transistor nối tiếp ($A \cdot B \cdot C_{in}$) mắc song song với nhánh $\overline{C_{out}}$ nối tiếp cụm 3 transistor song song $(A \parallel B \parallel C_{in})$.
   - Thêm 1 Inverter đệm (`INV_Sum`, 2T) để tạo ngõ ra $Sum$ $\implies$ **Tổng khối Sum: $7\text{N} + 7\text{P} + 2\text{T} = 16$ Transistors**.
   - **Tổng toàn mạch Mirror Adder:** $12\text{T} + 16\text{T} = \mathbf{28 \text{ Transistors}}$.

3. **Vị trí transistor $C_{in}$ trên đường tới hạn:**
   Trong bộ cộng nối tiếp nhiều bit, $C_{in}$ thường đến muộn hơn $A$ và $B$. Khi đặt transistor nhận $C_{in}$ ở **vị trí sát nút ngõ ra $\overline{C_{out}}$** (thay vì sát đường nguồn $V_{DD}$ hay $GND$), các nút nội bên dưới đã được $A$ và $B$ thiết lập sẵn trạng thái ở nhiều tổ hợp đầu vào, giúp giảm lượng điện tích cần nạp/xả khi $C_{in}$ chuyển mức. Sinh viên sẽ tự kiểm chứng mức độ cải thiện này bằng thực nghiệm đảo vị trí $C_{in}$ trong Ex6.3.

### 3.3. Kiến trúc Mạch Cộng Cổng Truyền (TG Full Adder)

Dựa trên nhận xét: đặt tín hiệu truyền $P = A \oplus B$, khi $P = 1$ thì $C_{out} = C_{in}$, và khi $P = 0$ thì $C_{out} = A$.
Ta xây dựng `tg_adder_1b` từ các tế bào cơ bản:
- **Khối 1 ($P = A \oplus B$):** 1 cổng `xor_tg` (gồm 2 `inv_x1` đảo $A, B$ và 2 `tg_gate` = **8T**) + 1 `inv_x1` tạo $\bar{P}$ (**2T**).
- **Khối 2 ($Sum = P \oplus C_{in}$):** 1 cổng `xor_tg` (**8T**). *(Lưu ý: nếu chia sẻ $\bar{P}$ sẵn có từ Khối 1 và tối ưu bỏ bớt Inverter nội, tổng số transistor có thể giảm xuống 16T; khi ghép trực tiếp từ cell `xor_tg` chuẩn, tổng mạch là **22 Transistors**).*
- **Khối 3 ($C_{out}$):** Dùng 2 `tg_gate` (**4T**) điều khiển trực tiếp bởi cặp tín hiệu $(P, \bar{P})$ để chọn giữa $C_{in}$ và $A$.

### 3.4. Tiêu chí Đối sánh PPA (Mirror Adder vs TG Adder)

*(Sinh viên tự điền số đo vào cột kết quả sau khi chạy mô phỏng cùng điều kiện bộ lái `inv_x1` và cùng tải $C_L = 50\,\text{fF}$).*

| Tiêu chí đối sánh | Mirror Adder (28T) | TG Full Adder (22T / 16T) | Ghi chú kỹ thuật |
| :--- | :---: | :---: | :--- |
| **Số lượng Transistor** | 28T | 22T (dạng module) / 16T (tối ưu) | |
| **Khả năng khôi phục mức** | Có (tầng CMOS tĩnh + đệm) | Không khôi phục ở nhánh TG MUX | |
| **Trễ $C_{in} \to C_{out}$ (1 tầng đơn)** | *(Sinh viên đo)* | *(Sinh viên đo)* | Đo cùng bộ lái và tải $50\,\text{fF}$ |
| **Quy luật trễ chuỗi $N = 1 \dots 4$ tầng** | Tuyến tính $O(N)$ | Bậc hai $O(N^2)$ nếu không chèn đệm | Do chuỗi TG tạo thang $RC$ phân bố |

---

## 4. CÂU HỎI CHUẨN BỊ TRƯỚC KHI ĐẾN LỚP (PRE-LAB)

> [!IMPORTANT]
> Sinh viên phải hoàn thành phần tính toán và phân tích vào **Mục 7.2.a** trước khi vào phòng máy để phục vụ **Cổng kiểm tra Pre-lab (10 phút đầu giờ)**.

1. **Kiểm chứng hàm logic Mirror Adder:**
   - Lập bảng chân trị 8 tổ hợp của $(A, B, C_{in})$ và chứng minh trực tiếp rằng biểu thức $Sum = A B C_{in} + \overline{C_{out}}(A + B + C_{in})$ cho đúng kết quả với mọi tổ hợp.
2. **Tự đếm và định cỡ Transistor cho Mirror Adder 28T:**
   - Từ hai biểu thức $\overline{C_{out}}$ và $\overline{Sum}$, hãy liệt kê số transistor NMOS, PMOS cho từng nhánh và tính kích thước $(W/L)_n, (W/L)_p$ (theo $\lambda$) sao cho đường dẫn xấu nhất của mỗi mạng có điện trở tương đương với Inverter chuẩn `inv_x1` ($W_n = 4\lambda, W_p = 12\lambda, L = 2\lambda$). *(Gợi ý: chú ý số transistor mắc nối tiếp tối đa trên mỗi nhánh Carry là 2, trên nhánh Sum là 3).*
   - Tính tổng bề rộng cổng (Total Gate Width) nối vào chân $C_{in}$ của một tế bào Mirror Adder và so sánh với bề rộng cổng của một Inverter chuẩn `inv_x1` ($16\lambda$).
3. **Phân tích đường trễ tới hạn của Bộ cộng 4-bit RCA:**
   - Viết biểu thức tổng trễ $T_{total}$ từ ngõ vào $(A_0, B_0, C_{in,0})$ tới ngõ ra **$C_{out,3}$** và tới ngõ ra **$Sum_3$** của bộ cộng 4-bit RCA. Chỉ rõ đường $C_{in} \to C_{out}$ xuất hiện với hệ số bằng bao nhiêu trong mỗi công thức.
4. *(Tùy chọn cho Layout)* Tìm một **đường đi Euler (Euler Path)** hợp lệ gồm đủ 5 transistor cho mạng PDN (và PUN) của khối Carry. *(Gợi ý: xác định các nút bậc lẻ của đồ thị mạch Carry trước khi chọn dãy 5 cổng).*

---

## 5. KẾ HOẠCH PHÂN BỔ THỜI LƯỢNG IN-LAB (135 PHÚT)

| Phân đoạn | Nội dung thực hiện | Thời lượng |
| :--- | :--- | :---: |
| **Kiểm tra đầu giờ** | Cổng kiểm tra Pre-lab (chứng minh hàm Sum, định cỡ 28T và công thức 4-bit RCA) | 10 phút |
| **Ex6.1** | Thiết kế Schematic `mirror_adder_1b{sch}` trên Electric VLSI (dùng khung khối Carry dựng sẵn để hoàn thiện khối Sum và kết nối) | 30 phút |
| **Ex6.2** | Mô phỏng kiểm chứng trọn vẹn 8 tổ hợp bảng chân trị trên LTspice bằng `.meas FIND` | 15 phút |
| **Ex6.3** | Đo trễ 4 đường tín hiệu ($C_{in} \to C_{out}, A \to C_{out}, C_{in} \to Sum, A \to Sum$) và thực nghiệm đảo vị trí transistor $C_{in}$ | 25 phút |
| **Ex6.4** | Ghép chuỗi 4-bit RCA ($N = 1, 2, 3, 4$), đo $t_{chain}(N)$ cho $C_{out,3}$ và $Sum_3$ | 20 phút |
| **Ex6.5** | Thiết kế và mô phỏng `tg_adder_1b` (từ `tg_gate`, `inv_x1`), đo so sánh với Mirror Adder cùng điều kiện lái/tải | 25 phút |
| **Tổng kết** | Ghi nhận số liệu, đối chiếu bảng đối chuẩn và ký nghiệm thu tại bàn | 10 phút |
| **Tổng cộng** | | **135 phút** |

*(Lưu ý theo lộ trình: Bài 6 không bắt buộc thực hiện Layout/PEX cho mạch 28T trong giờ thực hành; Layout 1-bit ALU slice sẽ được thực hiện ở Bài 10 hoặc trong phần tùy chọn nâng cao).*

---

## 6. NỘI DUNG THỰC HÀNH TẠI LỚP (IN-LAB)

### Ex6.1: Thiết kế Schematic Mirror Adder 28T (`mirror_adder_1b{sch}`) (Electric VLSI)

1. Mở Electric VLSI (`mocmos`, $\lambda = 0.30\,\mu\text{m}$), tạo Cell `mirror_adder_1b`, View `schematic` (hoặc mở khung có sẵn khối Carry `10T + 2T` để hoàn thiện nhanh khối Sum `14T + 2T`).
2. **Đặt tên nút nội cố định:** Đặt tên dây nối giữa tầng Carry và tầng Inverter đệm là `cob` ($\overline{C_{out}}$); dây nối từ tầng Sum ra Inverter đệm là `sb` ($\overline{Sum}$).
3. **Đặt kích thước theo kết quả Pre-lab:**
   - Khối Carry (5N + 5P): giữ $C_{in}$ ở vị trí **sát nút `cob`** nhất.
   - Khối Sum (7N + 7P): nhận `a`, `b`, `cin` và `cob` (cố định từ khối Carry).
   - 2 Inverter đệm ngõ ra `INV_Cout` và `INV_Sum`: dùng `inv_x1{ic}`.
4. Tạo 7 chân Export (`Ctrl+E`): `a`, `b`, `cin` (Input), `sum`, `cout` (Output), `vdd` (Power), `gnd` (Ground).
5. Nhấn `F5` kiểm tra đạt 0 lỗi, 0 cảnh báo. Đóng gói Icon `mirror_adder_1b{ic}` (có thể dùng chung tên `full_adder_1b{ic}`).

- **Sản phẩm Ex6.1:** Schematic `mirror_adder_1b{sch}` đủ 28 transistor, đạt 0 lỗi `F5`.

---

### Ex6.2: Kiểm chứng 8 Trạng thái Bảng Chân trị (LTspice)

1. Xuất Netlist cho `mirror_adder_1b`, thêm `.include "04 - Models_and_Libraries/C5_models.txt"`, nguồn `Vdd = 5.0V`, tải `CL_sum sum 0 50fF` và `CL_cout cout 0 50fF`.
2. Cấp 3 nguồn xung vuông tạo đủ 8 tổ hợp $(A, B, C_{in})$ từ `000` đến `111`, mỗi trạng thái giữ $10\,\text{ns}$:
   ```spice
   Va   a   0 PULSE(0 5.0 0 0.1n 0.1n 40n 80n)
   Vb   b   0 PULSE(0 5.0 0 0.1n 0.1n 20n 40n)
   Vcin cin 0 PULSE(0 5.0 0 0.1n 0.1n 10n 20n)
   .tran 0 80n 0 1p
   ```
3. **Lấy mẫu cuối mỗi trạng thái bằng `.meas`:** Vì tại một số bước chuyển (như `011 -> 100`), cả 3 ngõ vào đổi cùng lúc gây ra xung nhiễu thoáng qua (glitch) trên `sum`/`cout`, hãy dùng lệnh lấy mẫu ở cuối mỗi khoảng $10\,\text{ns}$ (ví dụ tại `5n, 15n, ..., 75n`):
   ```spice
   .meas tran sum_000 FIND v(sum) AT=5n
   .meas tran cout_000 FIND v(cout) AT=5n
   ...
   .meas tran sum_111 FIND v(sum) AT=75n
   .meas tran cout_111 FIND v(cout) AT=75n
   ```
4. Đối chiếu cả 8 cặp giá trị đo được với bảng chân trị lý thuyết.

- **Sản phẩm Ex6.2:** Dạng sóng 8 trạng thái và kết quả `.log` kiểm chứng 8 tổ hợp đúng 100%.

---

### Ex6.3: Đo Trễ các Đường Truyền lan & Thí nghiệm Đảo vị trí $C_{in}$ (LTspice)

1. Dùng cùng tải $C_L = 50\,\text{fF}$ (khuyến khích dùng `inv_x1` lái các ngõ vào để phản ánh đúng sườn xung thực tế), đo thời gian trễ $t_{pd} = (t_{pHL} + t_{pLH})/2$ tại ngưỡng `{0.5*5.0} = 2.5V` cho 4 trường hợp:
   - **Ca 1 ($C_{in} \to C_{out}$):** Đặt $A = 5\,\text{V}, B = 0\,\text{V}$ (điều kiện truyền $P=1$), cấp xung tại $C_{in}$. *(Lưu ý: do $C_{out} = \overline{\overline{C_{out}}}$ cùng pha với $C_{in}$, $C_{in} \uparrow \implies C_{out} \uparrow$).*
   - **Ca 2 ($A \to C_{out}$):** Đặt $B = 5\,\text{V}, C_{in} = 0\,\text{V}$, cấp xung tại $A$.
   - **Ca 3 ($C_{in} \to Sum$):** Đặt $A = 5\,\text{V}, B = 0\,\text{V}$, cấp xung tại $C_{in}$ (đây là đường đi qua cả `cob` và `sb`).
   - **Ca 4 ($A \to Sum$):** Đo ở 2 trường hợp: $B = 0, C_{in} = 0$ (không đảo $C_{out}$) và $B = 5\,\text{V}, C_{in} = 0$ (có chuyển trạng thái $C_{out}$).
2. **Thí nghiệm đảo vị trí transistor $C_{in}$:**
   - Trong bản sao tệp Netlist, hoán đổi vị trí transistor $C_{in}$ trong khối Carry từ vị trí **sát nút `cob`** xuống **sát nguồn `vdd` / đất `gnd`** (đặt cụm $A \parallel B$ lên sát `cob`).
   - Chạy lại phép đo Ca 1 ($t_{pd(Cin \to Cout)}$) và ghi nhận độ chênh lệch trễ.

- **Sản phẩm Ex6.3:** Bảng trễ 4 đường truyền, xác định đường chậm nhất và số liệu trước/sau khi đảo vị trí $C_{in}$.
- **Câu hỏi kiểm tra nhanh:** Tại sao đường $C_{in} \to Sum$ (khi $A=1, B=0$) lại chậm hơn đường $C_{in} \to C_{out}$?

---

### Ex6.4: Ghép Chuỗi 4-bit Ripple Carry Adder ($N = 1 \dots 4$) (LTspice)

1. Trong Netlist LTspice, ghép nối tiếp $N = 1, 2, 3, 4$ khối `mirror_adder_1b` (`cout` của tầng $i$ nối vào `cin` của tầng $i+1$).
2. Thiết lập vectơ kiểm tra trường hợp xấu nhất cho chuỗi truyền số nhớ:
   - $A[3:0] = \text{1111}$ ($5\,\text{V}$), $B[3:0] = \text{0000}$ ($0\,\text{V}$).
   - Cấp xung $0 \to 5\,\text{V}$ vào $C_{in,0}$; tải cuối $C_L = 50\,\text{fF}$ tại $C_{out,3}$ và $Sum_3$.
3. Đo tổng thời gian trễ $t_{chain}(N)$ tại ngõ ra $C_{out,N-1}$ ứng với $N = 1, 2, 3, 4$ (và đo thêm trễ tại $Sum_3$ cho $N=4$).
4. Vẽ đồ thị $t_{chain}(N)$ theo $N$ để xác nhận độ dốc tuyến tính ($O(N)$). So sánh độ dốc (trễ mỗi tầng bên trong chuỗi thật, nơi tải là $C_{in}$ của tầng sau) với $t_{pd(Cin \to Cout)}$ đo đơn lẻ ở tải $C_L = 50\,\text{fF}$ trong Ex6.3.

- **Sản phẩm Ex6.4:** Bảng và đồ thị $t_{chain}(N)$ cho $N = 1 \dots 4$ và nhận xét về tải liên tầng $C_{in}$.

---

### Ex6.5: Thiết kế và Đối sánh TG Full Adder (`tg_adder_1b`)

1. Dựng tế bào `xor_tg{sch}` (2 `inv_x1` + 2 `tg_gate` = $8\text{T}$) và ghép thành `tg_adder_1b{sch}` ($22\text{T}$) theo sơ đồ mục 3.3 (`X_xor1`, `X_inv_p`, `X_xor2`, 2 `tg_gate` cho $C_{out}$).
2. Kiểm chứng 8 tổ hợp logic bằng `.meas FIND` tương tự Ex6.2.
3. Đo trễ $t_{pd(Cin \to Cout)}$ của `tg_adder_1b` dưới **cùng điều kiện bộ lái `inv_x1` và tải $C_L = 50\,\text{fF}$** như Mirror Adder.
4. Nếu ghép chuỗi 4 tầng `tg_adder_1b` (không có bộ đệm ở đường carry), quan sát hiện tượng tăng trễ bậc hai $O(N^2)$ và suy giảm tốc độ sườn xung ở tầng cuối.

- **Sản phẩm Ex6.5:** Kết quả kiểm chứng 8 tổ hợp và số liệu đối sánh công bằng giữa `tg_adder_1b` và `mirror_adder_1b`.

---

## 7. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (POST-LAB)

### 7.1. Thực nghiệm và Phân tích Post-lab
1. Hoàn thiện đồ thị $t_{chain}(N)$ theo $N$ cho cả Mirror Adder và TG Adder (nếu đo chuỗi 4 tầng TG) để đối chiếu trực quan độ tăng tuyến tính $O(N)$ vs bậc hai $O(N^2)$.
2. *(Tùy chọn nâng cao - Không bắt buộc):* Thiết kế Layout khối Carry 10T (dùng đường đi Euler 5 transistor `B - A - Cin - A - B`) và kiểm tra DRC/NCC.

### 7.2. Phiếu báo cáo điền khuyết (Nộp kèm file mô phỏng)

```
========================================================================================
                          BÁO CÁO THỰC HÀNH: BÀI 6
         THIẾT KẾ MẠCH CỘNG TOÀN PHẦN 1-BIT (MIRROR ADDER 28T & TG ADDER)
Họ và Tên: ..................................................... MSSV: .................
Lớp: ....................................... Nhóm/Bàn: ......... Ngày: .................
Chữ ký Giảng viên / Điểm nghiệm thu tại bàn: ............................................
========================================================================================
```

#### a. Phần Chuẩn bị (Pre-lab)
1. **Số lượng và Kích thước Transistor Mirror Adder (tự điền từ kết quả tính toán):**

| Khối chức năng | Số NMOS / Số PMOS | Kích thước $(W/L)_n$ ($\lambda$) | Kích thước $(W/L)_p$ ($\lambda$) | Tổng số T |
| :--- | :---: | :---: | :---: | :---: |
| **Mạng logic Carry ($\overline{C_{out}}$)** | ...... N / ...... P | ................ | ................ | ........ |
| **Mạng logic Sum ($\overline{Sum}$)** | ...... N / ...... P | ................ | ................ | ........ |
| **2 Inverter đệm (`INV_Cout`, `INV_Sum`)** | ...... N / ...... P | ................ | ................ | ........ |
| **Tổng cộng toàn tế bào** | **...... N / ...... P** | — | — | **...... T** |

2. **Tổng bề rộng cổng chân $C_{in}$:** $W_{Cin} =$ ............ $\lambda$ (gấp .......... lần `inv_x1`).
3. **Biểu thức trễ 4-bit RCA:**
   - $T_{Cout3} =$ ....................................................................................
   - $T_{Sum3} =$ ....................................................................................

#### b. Kết quả Đo đạc Thực hành (In-lab & Post-lab)
1. **Kiểm chứng 8 tổ hợp & Đo trễ 4 đường truyền của `mirror_adder_1b` ($C_L = 50\,\text{fF}$):**
   - Trạng thái kiểm chứng 8 tổ hợp (`Ex6.2`): Đạt / Chưa đạt: `.................` (Ghi nhận glitch tại bước chuyển: `...............`).

| Đường truyền tín hiệu | $t_{pHL}$ (ps) | $t_{pLH}$ (ps) | $t_{pd}$ (ps) | Ghi chú |
| :--- | :---: | :---: | :---: | :--- |
| $C_{in} \to C_{out}$ ($A=1, B=0$, $C_{in}$ sát `cob`) | .............. | .............. | .............. | Chuẩn tối ưu |
| $C_{in} \to C_{out}$ ($C_{in}$ sát rail `vdd`/`gnd`) | .............. | .............. | .............. | Chênh lệch: .......... ps |
| $A \to C_{out}$ ($B=1, C_{in}=0$) | .............. | .............. | .............. | |
| $C_{in} \to Sum$ ($A=1, B=0$) | .............. | .............. | .............. | Đường tới hạn Sum |
| $A \to Sum$ ($B=0, C_{in}=0$ / $B=1, C_{in}=0$) | ...... / ...... | ...... / ...... | ...... / ...... | |

2. **Kết quả chuỗi 4-bit RCA (`mirror_adder_1b`, $A=1111, B=0000$):**

| Số tầng $N$ | 1 | 2 | 3 | 4 ($C_{out,3}$) | 4 ($Sum_3$) |
| :--- | :-: | :-: | :-: | :-: | :-: |
| $t_{chain}(N)$ (ps) | ...... | ...... | ...... | ...... | ...... |

- Độ dốc trung bình (trễ mỗi tầng trong chuỗi): $\Delta t / \Delta N =$ ................ ps/tầng.

3. **Đối sánh Mirror Adder vs TG Full Adder (cùng bộ lái `inv_x1`, $C_L = 50\,\text{fF}$):**

| Chỉ số | Mirror Adder | TG Full Adder | Nhận xét |
| :--- | :---: | :---: | :--- |
| Số transistor thực tế | ...... T | ...... T | |
| $t_{pd(Cin \to Cout)}$ (1 tầng đơn) | ............ ps | ............ ps | |
| $t_{chain}$ ($N=4$ tầng nối tiếp) | ............ ps | ............ ps | |

#### c. Câu hỏi Thảo luận Chuyên sâu
1. Dựa vào kết quả thí nghiệm đảo vị trí transistor $C_{in}$ trong Ex6.3, hãy giải thích tại sao việc đặt $C_{in}$ sát ngõ ra $\overline{C_{out}}$ lại giúp cải thiện tốc độ truyền lan, và điều kiện tổ hợp $(A, B)$ nào mang lại lợi ích rõ rệt nhất.
2. So sánh độ dốc $\Delta t / \Delta N$ đo được trong chuỗi RCA 4-bit (Ex6.4) với $t_{pd(Cin \to Cout)}$ đo đơn lẻ ở tải $C_L = 50\,\text{fF}$ (Ex6.3). Tại sao hai giá trị này lại khác nhau? *(Gợi ý: liên hệ với tổng bề rộng cổng chân $C_{in}$ đã tính ở Pre-lab).*
3. Dựa vào quy luật tăng trễ của bộ cộng RCA ($O(N)$), nếu thiết kế bộ cộng 32-bit bằng kiến trúc RCA thì độ trễ sẽ lớn gấp bao nhiêu lần? Đề xuất 2 kiến trúc bộ cộng tốc độ cao (như CLA hoặc Carry-Select) để phá vỡ nút thắt cổ chai này.

---

## 8. BẢNG KIỂM CHỨNG VÀ ĐỐI CHUẨN KỸ THUẬT (BENCHMARK)

| Thông số kiểm chứng | Dải giá trị kỳ vọng (MOSIS C5N) | Điều kiện kiểm tra |
| :--- | :---: | :--- |
| **Số lượng Transistor** | Mirror Adder: **$28\text{T}$**; TG Adder: **$22\text{T}$** (module) | Không thừa/thiếu linh kiện |
| **Kiểm chứng 8 tổ hợp** | Đúng 8/8 trạng thái tại điểm lấy mẫu cuối chu kỳ | `.meas FIND` tại `5n, 15n, ..., 75n` |
| **Đường chậm nhất (Mirror Adder)** | $C_{in} \to Sum$ (hoặc $A \to Sum$ qua $C_{out}$) chậm hơn $C_{in} \to C_{out}$ | Tỷ số phụ thuộc tải và sườn lái |
| **Quy luật chuỗi RCA ($N=1\dots 4$)** | Tuyến tính theo $N$ cho Mirror Adder | Độ dốc phản ánh tải $C_{in}$ thật của tầng sau |

---

## 9. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP

| Hiện tượng lỗi | Nguyên nhân gốc rễ | Cách khắc phục nhanh |
| :--- | :--- | :--- |
| **Hàm $Sum$ bị đảo logic ở tất cả 8 trạng thái** | Nối nhầm ngõ ra của Inverter đệm $C_{out}$ (tức $C_{out}$ thay vì $\overline{C_{out}}$) sang khối Sum. | Kiểm tra dây nối chéo: khối Sum phải nhận nút **`cob`** ($\overline{C_{out}}$, trước Inverter đệm). |
| **Mạch Mirror Adder chạy sai ở một số tổ hợp hoặc bị treo mức lửng** | Đếm thiếu transistor (chỉ đặt 4N/4P cho Carry hoặc 6N/6P cho Sum), hoặc đấu sai thứ tự nhánh PUN/PDN. | Kiểm tra đủ 5N+5P cho Carry, 7N+7P cho Sum, cả hai mạng dùng cùng topology. |
| **Ngõ ra `sum`/`cout` có xung nhọn (glitch) tại thời điểm chuyển trạng thái** | Ở các bước như `011 -> 100`, cả $A, B, C_{in}$ cùng đổi một lúc nên có độ lệch trễ ngắn qua nhánh Carry trước khi Sum ổn định. | Hiện tượng bình thường của mạch tổ hợp; dùng `.meas FIND` ở cuối mỗi khoảng $10\,\text{ns}$ để kiểm tra logic xác lập. |
| **Đo trễ $t_{pd(Cin \to Cout)}$ ra kết quả âm hoặc báo `FAILED`** | Quên đặt $A=5\text{V}, B=0\text{V}$ (nếu $A=B=0$ hoặc $A=B=1$ thì $C_{out}$ không phụ thuộc $C_{in}$!). | Kiểm tra điều kiện truyền số nhớ $P=1$ ($A=5\text{V}, B=0\text{V}$). |

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

| Tiêu chí đánh giá | Trọng số | Xuất sắc (8.5 – 10) | Khá (7.0 – 8.4) | Đạt (5.0 – 6.9) | Không đạt (< 5.0) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Chuẩn bị Pre-lab** | **20%** | Chứng minh đúng hàm Sum, đếm đúng 28T, định cỡ hợp lý $W_n/W_p$, tính đúng $W_{Cin}$ và viết đúng công thức $T_{Cout3}, T_{Sum3}$. | Đếm và định cỡ đúng 28T, thiếu hệ số chính xác trong $T_{Sum3}$ hoặc $W_{Cin}$. | Có bài chuẩn bị nhưng đếm sai số T hoặc định cỡ chưa bù suy hao nối tiếp. | Không làm Pre-lab hoặc sao chép. |
| **2. Schematic & Kiểm chứng 8 tổ hợp (Ex6.1–6.2)** | **20%** | Dựng đúng `mirror_adder_1b` (28T), đạt 0 lỗi `F5` và kiểm chứng 8/8 trạng thái bằng `.meas FIND`. | Dựng đúng schematic và kiểm chứng 8/8 trạng thái bằng đồ thị nhưng thiếu `.meas FIND`. | Đấu nhầm chân `cob` hoặc thiếu transistor phải sửa lại mới đúng 8 trạng thái. | Mạch sai chức năng. |
| **3. Đo trễ 4 đường & Đảo vị trí $C_{in}$ (Ex6.3)** | **20%** | Đo đủ 4 đường trễ, giải thích đúng đường chậm nhất và hoàn thành thí nghiệm đảo vị trí $C_{in}$. | Đo đủ 4 đường trễ nhưng thiếu thí nghiệm đảo vị trí $C_{in}$. | Chỉ đo được $C_{in} \to C_{out}$, thiếu các đường $Sum$. | Không đo được trễ. |
| **4. Chuỗi 4-bit RCA & TG Adder (Ex6.4–6.5)** | **25%** | Đo đủ $t_{chain}(N)$ cho $N=1\dots 4$, vẽ đồ thị $O(N)$ và dựng/đo đối sánh công bằng `tg_adder_1b` (22T). | Hoàn thành chuỗi RCA $N=1\dots 4$ và dựng được `tg_adder_1b`, thiếu so sánh cùng điều kiện tải/lái. | Chỉ chạy được RCA ở $N=4$ (thiếu $N=1\dots 3$) hoặc chưa hoàn thành TG Adder. | Không hoàn thành cả Ex6.4 và Ex6.5. |
| **5. Báo cáo & Thảo luận chuyên sâu** | **15%** | Nộp đầy đủ số liệu khớp `.log`, trả lời sâu sắc 3 câu hỏi thảo luận (đặc biệt giải thích tải $C_{in}$ và CLA). | Báo cáo đầy đủ số liệu nhưng giải thích sự khác biệt độ dốc $t_{chain}$ chưa rõ. | Báo cáo thiếu một số bảng đo hoặc thiếu câu trả lời mở rộng. | Nộp thiếu báo cáo hoặc số liệu không khớp mô phỏng. |

---

## 11. TÀI LIỆU THAM KHẢO

1. N. H. E. Weste & D. M. Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th Ed., Addison-Wesley (Chương 11: Datapath Subsystems — Adders).
2. J. M. Rabaey, A. Chandrakasan & B. Nikolic, *Digital Integrated Circuits: A Design Perspective*, 2nd Ed., Prentice Hall (Chương 11: Designing Arithmetic Building Blocks — Mirror Adder & TG Adder).
3. R. Jacob Baker, *CMOS: Circuit Design, Layout, and Simulation*, 3rd Ed., Wiley-IEEE Press.
4. Thư viện mô hình SPICE chuẩn phòng thí nghiệm: `04 - Models_and_Libraries/C5_models.txt`.
