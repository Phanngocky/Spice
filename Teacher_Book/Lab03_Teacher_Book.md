# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 03 — TEACHER'S BOOK: CỔNG PHỨC HỢP AOI21 VÀ TỐI ƯU TRỄ THEO PHƯƠNG PHÁP LOGICAL EFFORT
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-03-cong-phuc-hop-aoi-oai-logical-effort.md](../02%20-%20Student%20Workbook/lab-03-cong-phuc-hop-aoi-oai-logical-effort.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab03/](../03%20-%20Instructor_Solutions/lab03/)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda_{DR} = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

# 3. LAB 3 — CỔNG PHỨC HỢP AOI/OAI VÀ LOGICAL EFFORT (CHƯƠNG 3, 6)

## 3.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. **Bản chất của Cổng phức hợp CMOS tĩnh (AOI/OAI):** Nhận diện cách gom các cấu trúc logic nhiều tầng (AND-OR-INVERT) thành **một tầng chuyển mạch duy nhất (Single-stage)**. Hiểu rõ đánh đổi vật lý: giảm 40% số lượng transistor (từ 10 xuống 6) và giảm $\approx 18$% tổng bề rộng kênh silicon, triệt tiêu các nút ký sinh trung gian, nhưng phải trả giá bằng việc xếp chồng transistor trong mạng nạp/xả.
2. **Nắm vững phương pháp Logical Effort (Sutherland, Sproull, Harris):** Mô hình trễ tuyến tính chuẩn hóa $d = g \cdot h + p$ giúp tính toán nhẩm kích thước và dự báo trễ của các đường truyền phức tạp mà không cần chạy hàng nghìn lượt SPICE.
3. **Thành thạo phương pháp thực nghiệm đo $g$ và $p$:** Bác bỏ sai lầm định nghĩa $h$ theo Inverter (khiến hệ số góc luôn bằng $1$). Hiểu và thực hành phương pháp Testbench kép đối chuẩn trực tiếp với `INV_X1` để trích xuất $\tau$, $g_{meas}$ và $p_{meas}$.
4. **Hiểu bản chất "đáy phẳng" của bài toán Chuỗi đệm (Buffer Chain):** Số tầng tối ưu $N^*$ cho phép kỹ sư linh hoạt chọn $N$ chẵn/lẻ (để giữ hoặc đảo pha logic) hoặc chọn $N$ nhỏ hơn để tiết kiệm diện tích mà trễ tổng cộng chỉ tăng thêm vài phần trăm.
5. **Thành thạo phương pháp đường đi Euler trên Layout:** Chứng minh vì sao thứ tự dải Poly $C - A - B$ tối ưu hơn $A - B - C$ nhờ kỹ thuật chia sẻ cực má chung ngõ ra `out` (Abutment) trên dải N-Active.

---

## 3.2 Phân tích Kỹ thuật Cổng Phức hợp AOI21 vs Cổng Ghép Rời

### a. So sánh Định lượng Kiến trúc
Xét hàm logic: $Y = \overline{(A \cdot B) + C}$.

| Tiêu chí kỹ thuật | Phương án Ghép Cổng Rời (NAND2 + INV + NOR2) | Phương án Cổng Phức hợp AOI21 (`aoi21_x1`) | Mức độ Tối ưu |
| :--- | :---: | :---: | :---: |
| **Số lượng Transistor** | $4\text{T (NAND2)} + 2\text{T (INV)} + 4\text{T (NOR2)} = \mathbf{10\text{T}}$ | $3\text{T (PMOS)} + 3\text{T (NMOS)} = \mathbf{6\text{T}}$ | **Giảm 40,0%** |
| **Số tầng trễ logic** | **2 tầng chuyển mạch** (tín hiệu đi qua 2 cổng) | **1 tầng chuyển mạch duy nhất** | **Giảm 1 tầng trễ** |
| **Tổng bề rộng kênh $\sum W$** | $40\lambda + 16\lambda + 56\lambda = \mathbf{112\lambda_{DR} = 33,6\,\mu\text{m}}$ | $3(24\lambda) + 2(8\lambda) + 4\lambda = \mathbf{92\lambda_{DR} = 27,6\,\mu\text{m}}$ | **Giảm 17,86%** |
| **Nút ký sinh liên tầng** | Có 2 nút dây nối trung gian mang điện dung ký sinh | Triệt tiêu hoàn toàn nút trung gian | Giảm điện dung ký sinh |
| **Công suất động tiêu tán** | Lớn (nạp/xả tụ ký sinh tại 2 nút trung gian) | Nhỏ hơn đáng kể ($P_{dyn} = \alpha C_{tot} V_{DD}^2 f$) | Tiết kiệm năng lượng |

```
       PHƯƠNG ÁN GHÉP CỔNG RỜI (10T, 2 TẦNG)             PHƯƠNG ÁN CỔNG PHỨC HỢP AOI21 (6T, 1 TẦNG)
       A --+---[ NAND2 ]-- (Nút 1) --[ INV ]--+                             VDD
       B --+                                  |                              │
                                          (Nút 2) --[ NOR2 ]-- Y     +-------+-------+
                                              C ----+                |       |       |
                                                                   [MPA]   [MPB] (Mỗi cái 24λ)
                                                                     |       |
                                                                     +---+---+
                                                                         | (Xp)
                                                                       [MPC: 24λ]
                                                                         |
                                                                         +------------ Out (Y)
                                                                         |
                                                                     +---+---+
                                                                     |       |
                                                                   [MNA]   [MNC: 4λ]
                                                                    (8λ)     |
                                                                     |       |
                                                                   [MNB]     |
                                                                    (8λ)     |
                                                                     |       |
                                                                     +---+---+
                                                                         |
                                                                        GND
```

---

### b. Suy dẫn Toán học Định cỡ Kênh $(W/L)$ theo Điện trở Dẫn $R_{on}$
Cho Inverter chuẩn `INV_X1` ($W_n = 4\lambda, W_p = 12\lambda$):
$$R_{on,n0} \approx 969\,\Omega, \quad R_{on,p0} \approx 992\,\Omega$$

1. **Mạng kéo xuống (PDN):**
   - **Nhánh $A \cdot B$ (2 NMOS nối tiếp):** Khi $A=1, B=1$, dòng xả đi qua $M_{NA}$ và $M_{NB}$ nối tiếp. Để tổng điện trở bằng $R_{on,n0}$:
     $$R_{eq,N(AB)} = R_{on,NA} + R_{on,NB} = 2 \times \frac{R_{\Box,n}}{W_{n,AB}/L} = \frac{R_{\Box,n}}{W_{n,inv}/L}$$
     $$\implies W_{n,A} = W_{n,B} = 2 \times W_{n,inv} = 2 \times 4\lambda_{DR} = \mathbf{8\lambda_{DR} = 2,40\,\mu\text{m}}$$
     *(Mỗi NMOS có điện trở $R_{on} \approx 484,5\,\Omega \implies R_{eq} \approx 969,0\,\Omega$)*.
   - **Nhánh $C$ (1 NMOS đơn):** Khi $C=1$, chỉ có $M_{NC}$ dẫn:
     $$W_{n,C} = W_{n,inv} = \mathbf{4\lambda_{DR} = 1,20\,\mu\text{m}} \implies R_{on,NC} \approx 969,0\,\Omega$$

2. **Mạng kéo lên (PUN):**
   - Cụm $(M_{PA} \parallel M_{PB})$ mắc nối tiếp với $M_{PC}$.
   - **Tình huống xấu nhất (Worst-Case Pull-Up):** Xảy ra khi chỉ có **1 PMOS trong cụm song song dẫn** kết hợp với $M_{PC}$ (ví dụ $A=0, B=1, C=0$ hoặc $A=1, B=0, C=0$). Khi đó đường dẫn từ $V_{DD}$ xuống $Out$ đi qua đúng 2 PMOS mắc nối tiếp.
   - Để tổng điện trở nhánh xấu nhất bằng $R_{on,p0}$:
     $$R_{eq,P} = R_{on,P(A/B)} + R_{on,PC} = 2 \times \frac{R_{\Box,p}}{W_p/L} = R_{on,p0}$$
     $$\implies W_{p,A} = W_{p,B} = W_{p,C} = 2 \times W_{p,inv} = 2 \times 12\lambda_{DR} = \mathbf{24\lambda_{DR} = 7,20\,\mu\text{m}}$$
     *(Mỗi PMOS có điện trở $R_{on} \approx 496,0\,\Omega \implies R_{eq,P} \approx 992,1\,\Omega$)*.

> [!NOTE]
> **Giới hạn của mô hình:** Cách định cỡ trên chỉ dựa trên điện trở tuyến tính bậc hai và bỏ qua hiệu ứng thân (Body Effect) trên transistor $M_{PC}$ và $M_{NA}$. Trên thực tế, $M_{PC}$ có cực nguồn nối vào nút nội $X_p$ ($V_{SB} > 0$), làm tăng điện áp ngưỡng $|V_{thp}|$ lên $\sim 1,1\,\text{V}$, khiến dòng nạp thực tế nhỏ hơn và trễ sườn lên lớn hơn lý thuyết.

---

## 3.3 Phương pháp Logical Effort & Suy dẫn Giải tích

### a. Bảng Phân tích Logical Effort và Trễ Ký sinh của AOI21
Với Inverter chuẩn `INV_X1`:
$$C_{in,inv} \propto W_n + W_p = 4\lambda + 12\lambda = 16\lambda_{DR}$$

| Ngõ vào | Transistor kết nối | Tổng chiều rộng cổng $W_n + W_p$ | Nỗ lực Logic $g$ | Nỗ lực Điện chuẩn hóa | Trễ ký sinh $p$ |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **Pin A** | $M_{NA} (8\lambda) + M_{PA} (24\lambda)$ | $8\lambda + 24\lambda = 32\lambda_{DR}$ | $g_A = 32/16 = \mathbf{2,00}$ | $h_A = C_L / C_{in,A}$ | $p = 36/16 = \mathbf{2,25}$ |
| **Pin B** | $M_{NB} (8\lambda) + M_{PB} (24\lambda)$ | $8\lambda + 24\lambda = 32\lambda_{DR}$ | $g_B = 32/16 = \mathbf{2,00}$ | $h_B = C_L / C_{in,B}$ | (Cực má tại nút Out gồm: |
| **Pin C** | $M_{NC} (4\lambda) + M_{PC} (24\lambda)$ | $4\lambda + 24\lambda = 28\lambda_{DR}$ | $g_C = 28/16 = \mathbf{1,75}$ | $h_C = C_L / C_{in,C}$ | $M_{PC}(24\lambda) + M_{NA}(8\lambda) + M_{NC}(4\lambda)$) |

### b. Tế bào Đối ngẫu OAI21 ($Y = \overline{(A + B) \cdot C}$) — Bài toán Pre-lab của Sinh viên
Để tránh lộ đáp án AOI21 trong bài chuẩn bị ở nhà, đề bài Pre-lab giao cho sinh viên phân tích cổng đối ngẫu **OAI21**:
- Hàm logic bù: $\bar{Y} = (A + B) \cdot C \implies$ PDN: $(M_{NA} \parallel M_{NB})$ mắc nối tiếp với $M_{NC}$.
- Mạng kéo lên PUN: $(M_{PA} \text{ nối tiếp } M_{PB})$ mắc song song với $M_{PC}$.

#### Đáp án Định cỡ OAI21:
- **PDN:** 
  * Worst-case khi 1 trong 2 NMOS A hoặc B dẫn nối tiếp với NMOS C $\implies W_{n,A} = W_{n,B} = W_{n,C} = 2 \times 4\lambda = \mathbf{8\lambda_{DR} = 2,40\,\mu\text{m}}$.
- **PUN:**
  * Nhánh $A - B$ có 2 PMOS nối tiếp $\implies W_{p,A} = W_{p,B} = 2 \times 12\lambda = \mathbf{24\lambda_{DR} = 7,20\,\mu\text{m}}$.
  * Nhánh đơn $C$ có 1 PMOS song song độc lập $\implies W_{p,C} = W_{p,inv} = \mathbf{12\lambda_{DR} = 3,60\,\mu\text{m}}$.

#### Đáp án Logical Effort OAI21:
- $g_A = \frac{W_{nA} + W_{pA}}{16\lambda} = \frac{8\lambda + 24\lambda}{16\lambda} = \frac{32\lambda}{16\lambda} = \mathbf{2,00}$.
- $g_B = \frac{W_{nB} + W_{pB}}{16\lambda} = \frac{8\lambda + 24\lambda}{16\lambda} = \frac{32\lambda}{16\lambda} = \mathbf{2,00}$.
- $g_C = \frac{W_{nC} + W_{pC}}{16\lambda} = \frac{8\lambda + 12\lambda}{16\lambda} = \frac{20\lambda}{16\lambda} = \mathbf{1,25}$ ($5/4$).
- **Trễ ký sinh $p_{OAI21}$:**  
  Nút ngõ ra $Out$ nối với cực má của $M_{PC} (12\lambda)$, cực má $M_{PB} (24\lambda)$, cực má $M_{NA} (8\lambda)$, cực má $M_{NB} (8\lambda)$:
  $$C_{out} \propto 12\lambda + 24\lambda + 8\lambda + 8\lambda = 52\lambda_{DR} \implies p = \frac{52\lambda}{16\lambda} = \mathbf{3,25}$$
  *(Nếu bố trí $M_{NC}$ ở đỉnh PDN thì $C_{out} \propto 12 + 24 + 8 = 44\lambda \implies p = 2,75$)*.

> [!TIP]
> **Điểm so sánh vật lý sâu sắc giữa AOI21 và OAI21:**  
> Tại sao $g_C(OAI21) = 1,25$ lại nhỏ hơn rõ rệt so với $g_C(AOI21) = 1,75$?  
> - Trong AOI21, ngõ $C$ nối vào PMOS nối tiếp ($W_p = 24\lambda$) và NMOS đơn ($W_n = 4\lambda$) $\implies C_{in} = 28\lambda$.
> - Trong OAI21, ngõ $C$ nối vào PMOS đơn ($W_p = 12\lambda$) và NMOS nối tiếp ($W_n = 8\lambda$) $\implies C_{in} = 20\lambda$.  
> Nhờ PMOS nhánh $C$ của OAI21 chỉ là PMOS đơn ($12\lambda$) nên tải dung ngõ vào giảm mạnh, giúp $g_C$ chỉ còn $1,25$!

---

## 3.4 Phân tích Toán học Tối ưu Chuỗi Đệm Inverter (Inverter Buffer Chain)

### a. Thiết lập Bài toán Tối ưu
Cho tín hiệu từ một cổng logic chuẩn lái tải nặng $C_L = 1,0\,\text{pF} = 1000\,\text{fF}$.  
Giả sử ngõ vào chuỗi đệm có kích thước bằng Inverter cơ sở $1\times$ ($C_{in,inv} \approx 20\,\text{fF}$).  
Nỗ lực đường truyền:
$$F = G \cdot B \cdot H = (1 \times 1 \times \dots) \cdot 1 \cdot \left(\frac{1000\,\text{fF}}{20\,\text{fF}}ight) = H = 50,0$$

Trễ tổng cộng qua chuỗi $N$ tầng Inverter:
$$D = \sum_{i=1}^N (g_i h_i + p_i) = N \cdot \hat{f} + N \cdot p_{inv} = N \left(H^{1/N} + 1ight) \cdot \tau$$

Tìm cực tiểu của $D$ theo biến liên tục $N$:
$$\frac{\partial D}{\partial N} = \left(H^{1/N} + 1ight) + N \cdot H^{1/N} \cdot \left(-\frac{\ln H}{N^2}ight) = 0$$
$$\hat{f} + 1 - \hat{f} \ln \hat{f} = 0 \implies \hat{f} (\ln \hat{f} - 1) = 1 \implies \hat{f} \approx \mathbf{3,59} \approx 3,6$$

### b. Bảng Đánh giá Định lượng với $H = 50$:
| Số tầng $N$ | Nỗ lực mỗi tầng $\hat{f} = 50^{1/N}$ | Trễ chuẩn hóa $D / \tau$ | Tỉ lệ so với tối ưu | Ý nghĩa kỹ thuật |
| :---: | :---: | :---: | :---: | :--- |
| **$N = 1$** | $50,00$ | $1 \times (50 + 1) = \mathbf{51,00\,\tau}$ | Chậm gấp **$3,63$ lần** | Lái trực tiếp: trễ lớn, sườn xung thoái hóa |
| **$N = 2$** | $7,07$ | $2 \times (7,07 + 1) = \mathbf{16,14\,\tau}$ | Chậm hơn +14,8% | Tiết kiệm diện tích, giữ nguyên pha logic |
| **$N = 3$** | **$3,68$** | $3 \times (3,68 + 1) = \mathbf{14,05\,\tau}$ | **Cực tiểu hoàn toàn (100%)** | Tối ưu tốc độ cao nhất (Đảo pha tín hiệu) |
| **$N = 4$** | $2,66$ | $4 \times (2,66 + 1) = \mathbf{14,64\,\tau}$ | Chậm hơn +4,2% | Giữ nguyên pha logic, diện tích tăng nhẹ |
| **$N = 5$** | $2,19$ | $5 \times (2,19 + 1) = \mathbf{15,93\,\tau}$ | Chậm hơn +13,4% | Quá nhiều tầng, lãng phí công suất và diện tích |

> [!IMPORTANT]
> **Tính chất "Đáy phẳng" (Flat-Bottom Property):**  
> Chú ý rằng trễ của $N = 4$ ($14,64\tau$) chỉ lớn hơn trễ tối ưu của $N = 3$ ($14,05\tau$) đúng 4,2%. Trong thiết kế vi mạch thực tế, nếu mạch đòi hỏi tín hiệu không đảo (non-inverting), kỹ sư sẽ **chọn ngay $N = 4$** mà không cần phải thêm một Inverter phụ làm tăng thêm trễ.

---

## 3.5 Phương pháp Thực nghiệm Đo $g$ và $p$ Chuẩn xác

### Bẫy đo đạc phổ biến cần giải thích cho sinh viên:
Nếu sinh viên lấy tải $C_L = h \times C_{in,inv}$ rồi vẽ đồ thị $t_{pd}$ theo $h' = C_L / C_{in,inv}$:
Vì cổng AOI21 đã được định cỡ để có cùng điện trở kéo với Inverter ($R_{eq} = R_{on,inv}$):
$$t_{pd} = 0,69 \cdot R_{eq} \cdot C_L = 0,69 \cdot R_{on,inv} \cdot C_L = 0,69 \cdot R_{on,inv} \cdot C_{in,inv} \cdot h' = \tau \cdot h'$$
Hệ số góc của đường trễ theo $h'$ luôn bằng **$1 \cdot \tau$** đối với mọi cổng logic được định cỡ cân bằng! Sinh viên sẽ đo ra $g_{meas} \approx 1,0$ và hoang mang vì không khớp lý thuyết ($2,00$).

### Phương pháp Testbench kép đúng:
1. Nỗ lực điện $h$ của ngõ A được định nghĩa là $h = C_L / C_{in,A}$.
2. Vì $C_{in,A} = 2 \times C_{in,inv}$, để có cùng nỗ lực điện $h \in \{1, 2, 3, 4\}$, tải dung ngoài đặt vào ngõ A phải là $C_L = h \times C_{in,A} = h \times (2 C_{in,inv})$.
3. Khi đó hệ số góc của đường trễ $t_{pd,A}$ theo $h$ là:
   $$\text{Slope}_{h,A} = \frac{\Delta t_{pd,A}}{\Delta h} = g_A \cdot \tau$$
4. Trong cùng testbench, đo hệ số góc của `INV_X1` theo $h_{inv} = C_L / C_{in,inv}$:
   $$\text{Slope}_{h,inv} = 1 \cdot \tau$$
5. Lập tỉ số trực tiếp để triệt tiêu sai số mô hình:
   $$g_{meas,A} = \frac{\text{Slope}_{h,A}}{\text{Slope}_{h,inv}} \approx \mathbf{2,00}$$
   $$p_{meas} = \frac{t_{pd0,A}}{t_{pd0,inv}} \times p_{inv} \approx \frac{t_{pd0,A}}{t_{pd0,inv}} \approx \mathbf{2,25}$$

---

## 3.6 Phương pháp Đường đi Euler & Bố trí Mặt nạ Layout

### So sánh Thứ tự Poly $C - A - B$ vs $A - B - C$:
- **Nếu chọn thứ tự $A - B - C$:**
  * Dải N-Active: $[Out] - M_{NA} - [X_n] - M_{NB} - [GND] \mid\text{cắt dải}\mid [GND] - M_{NC} - [Out]$.
  * Nút `out` bị nằm ở hai đầu xa nhau của dải khuếch tán, không thể gộp thành một cực má chung, buộc phải đi dây Metal 1 vòng vèo làm tăng diện tích và điện dung ký sinh nút Out!
- **Nếu chọn thứ tự $C - A - B$:**
  * Dải N-Active: $[GND] - M_{NC} - [\mathbf{Out}] - M_{NA} - [X_n] - M_{NB} - [GND]$.
  * Cực má của $M_{NC}$ và $M_{NA}$ nằm kề sát nhau, nối liền thành **một vùng khuếch tán chia sẻ (Abutment) duy nhất nối ra `out`**!
  * Dải P-Active: $[\mathbf{Out}] - M_{PC} - [X_p] - M_{PA} - [\mathbf{VDD}] - M_{PB} - [X_p]$.
  * Cực nguồn của $M_{PA}$ và $M_{PB}$ nối chung một tiếp xúc Contact `vdd` ở giữa!
  * $\implies$ **Thứ tự $C - A - B$ là giải pháp tối ưu hoàn toàn cho Layout AOI21.**

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN SPICE BENCHMARK

## 3.7 Kế hoạch Buổi học 135 Phút & Kịch bản Can thiệp Sư phạm

### Khung giờ chi tiết:
- **00 – 10' (10 phút):** Kiểm tra bài làm Pre-lab (bảng chân trị và định cỡ OAI21, bài toán buffer chain $F=64$, Stick diagram). Ký xác nhận vào báo cáo.
- **10 – 35' (25 phút):** **Ex3.1:** Dựng Schematic `aoi21_x1{sch}`. Hướng dẫn gán 6 Export, nhấn `F5` kiểm tra. Thiết lập nguồn xung vuông quét 8 trạng thái logic trong $80\,\text{ns}$.
- **35 – 70' (35 phút):** **Ex3.2:** Dựng Testbench kép đo Logical Effort $g$ và $p$. Hướng dẫn sinh viên quét tải dung $C_L$, vẽ đồ thị hồi quy tuyến tính, trích xuất $g_{meas}$ và $p_{meas}$.
- **70 – 95' (25 phút):** **Ex3.3:** Thiết kế chuỗi đệm 3 tầng `buf_chain_3st{sch}`. Mô phỏng đối sánh với Inverter đơn $1\times$ khi lái tải nặng $1\,\text{pF}$. Đo trễ và độ dốc sườn xung.
- **95 – 125' (30 phút):** **Ex3.4:** Thiết kế Mask Layout `aoi21_x1{lay}` theo thứ tự $C - A - B$. Lưu ý khoảng cách Poly qua Contact $\ge 6\lambda_{DR} = 1,8\,\mu\text{m}$. Chạy DRC (0 lỗi) và NCC LVS ("MATCH").
- **125 – 135' (10 phút):** Nghiệm thu tại bàn, kiểm tra file `.jelib`, ký xác nhận hoàn thành In-lab.

---

## 3.8 Bảng Đáp án Chi tiết Pre-lab

### 1. Đáp án Câu hỏi 1: Cổng Đối ngẫu OAI21 ($Y = \overline{(A + B) \cdot C}$)
- Bảng chân trị OAI21:

| A | B | C | $A + B$ | $(A + B) \cdot C$ | Ngõ ra $Y$ |
| :-: | :-: | :-: | :-: | :-: | :---: |
| 0 | 0 | 0 | 0 | 0 | **1** |
| 0 | 0 | 1 | 0 | 0 | **1** |
| 0 | 1 | 0 | 1 | 0 | **1** |
| 0 | 1 | 1 | 1 | 1 | **0** |
| 1 | 0 | 0 | 1 | 0 | **1** |
| 1 | 0 | 1 | 1 | 1 | **0** |
| 1 | 1 | 0 | 1 | 0 | **1** |
| 1 | 1 | 1 | 1 | 1 | **0** |

- Kích thước định cỡ OAI21:
  * $M_{NA}, M_{NB}, M_{NC}$: $W = 8\lambda_{DR} = 2,40\,\mu\text{m}, L = 2\lambda_{DR} = 0,60\,\mu\text{m}$.
  * $M_{PA}, M_{PB}$: $W = 24\lambda_{DR} = 7,20\,\mu\text{m}, L = 2\lambda_{DR} = 0,60\,\mu\text{m}$.
  * $M_{PC}$: $W = 12\lambda_{DR} = 3,60\,\mu\text{m}, L = 2\lambda_{DR} = 0,60\,\mu\text{m}$.

### 2. Đáp án Câu hỏi 2: Logical Effort Cổng OAI21
- $g_A = \frac{8\lambda + 24\lambda}{16\lambda} = \mathbf{2,00}$.
- $g_B = \frac{8\lambda + 24\lambda}{16\lambda} = \mathbf{2,00}$.
- $g_C = \frac{8\lambda + 12\lambda}{16\lambda} = \mathbf{1,25}$ ($5/4$).
- Trễ ký sinh: $p_{OAI21} = \frac{12\lambda + 24\lambda + 8\lambda + 8\lambda}{16\lambda} = \mathbf{3,25}$ (hoặc $2,75$).
- **Giải thích:** Ngõ C của OAI21 có $g_C = 1,25$ nhỏ hơn nhiều so với ngõ C của AOI21 ($1,75$) vì PMOS nhánh C trong OAI21 là PMOS đơn ($12\lambda$) thay vì PMOS nối tiếp ($24\lambda$). Ngõ C nên nhận tín hiệu đến muộn nhất.

### 3. Đáp án Câu hỏi 3: Bài toán Chuỗi Đệm $F = 64$
| Số tầng $N$ | Nỗ lực mỗi tầng $\hat{f} = 64^{1/N}$ | Trễ chuẩn hóa $D / \tau = N(\hat{f} + 1)$ | Nhận xét |
| :---: | :---: | :---: | :--- |
| **$N = 1$** | $64,00$ | $1 \times (64 + 1) = \mathbf{65,00\,\tau}$ | Lái trực tiếp: rất chậm |
| **$N = 2$** | $8,00$ | $2 \times (8 + 1) = \mathbf{18,00\,\tau}$ | Chưa tối ưu |
| **$N = 3$** | **$4,00$** | $3 \times (4 + 1) = \mathbf{15,00\,\tau}$ | **Tối ưu hoàn toàn (100%)** |
| **$N = 4$** | $2,83$ | $4 \times (2,83 + 1) = \mathbf{15,31\,\tau}$ | Chỉ chậm hơn tối ưu +2,1% |

---

## 3.9 Bảng Đối Chuẩn Kỹ Thuật Toàn Diện (SPICE Benchmark MOSIS C5N Level 3)

| STT | Thông số đo đạc kỹ thuật | Giá trị Giải tích | Đo SPICE Pre-layout | Đo SPICE Post-layout (PEX) | Ghi chú & Nhận xét |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | **Chức năng logic AOI21** | 8 trạng thái | Đạt 100% | Đạt 100% | Lấy mẫu tại $t = 2,5\,\text{ns}, 7,5\,\text{ns}, \dots$ |
| 2 | **$t_{pd,inv}$ Inverter chuẩn ($C_L = 20\text{fF}$)** | $13,6\,\text{ps}$ | $22 - 28\,\text{ps}$ | $32 - 40\,\text{ps}$ | Đối chuẩn cơ sở |
| 3 | **Hằng số trễ $\tau$** | $\approx 10 - 13\,\text{ps}$ | $12 - 16\,\text{ps}$ | $16 - 22\,\text{ps}$ | Trích xuất từ độ dốc `INV_X1` |
| 4 | **Logical Effort ngõ A ($g_{meas,A}$)** | $2,00$ | $1,85 - 2,15$ | $1,90 - 2,20$ | Khớp trong sai lệch $\le 10$% |
| 5 | **Logical Effort ngõ C ($g_{meas,C}$)** | $1,75$ | $1,62 - 1,88$ | $1,65 - 1,92$ | Nhẹ tải hơn ngõ A |
| 6 | **Trễ ký sinh thực nghiệm ($p_{meas}$)** | $2,25$ | $1,90 - 2,40$ | $2,40 - 2,90$ | Chuẩn hóa theo $p_{inv}$ |
| 7 | **Trễ worst-case ngõ C ($50\text{fF}$)** | $34,4\,\text{ps}$ | $52 - 62\,\text{ps}$ | $74 - 88\,\text{ps}$ | $A=1, B=0$, chỉ 1 PMOS dẫn |
| 8 | **Trễ lái trực tiếp 1X ($C_L = 1\text{pF}$)** | $\approx 0,68\,\text{ns}$ | $0,95 - 1,25\,\text{ns}$ | $1,05 - 1,35\,\text{ns}$ | Sườn xung bị kéo dài rất lớn |
| 9 | **Trễ qua chuỗi đệm 3 tầng ($1\text{pF}$)** | $\approx 0,19\,\text{ns}$ | $0,28 - 0,36\,\text{ns}$ | $0,35 - 0,45\,\text{ns}$ | **Giảm trễ $> 70$% (nhanh hơn $> 3$ lần)** |
| 10 | **Sườn tăng $t_{rise}$ tại tải $1\text{pF}$** | N/A | Trực tiếp: $> 2,0\,\text{ns}$ | Chuỗi: $< 0,35\,\text{ns}$ | Sườn xung vuông vức trở lại |
| 11 | **Diện tích Layout AOI21 ($W \times H$)** | N/A | $\approx 180 - 210\,\mu\text{m}^2$ | $\approx 180 - 210\,\mu\text{m}^2$ | Thứ tự $C-A-B$, $H=60\lambda$ |
| 12 | **DRC MOSIS Errors** | 0 | 0 lỗi | 0 lỗi | Bắt buộc 0 lỗi |
| 13 | **LVS Comparison (NCC)** | N/A | **MATCH** | **MATCH** | Trùng khớp sơ đồ 100% |

---

## 3.10 Kịch bản Gỡ lỗi Socratic Dialogues cho Giảng viên

### Tình huống 1: Sinh viên thắc mắc "Tại sao em hồi quy nỗ lực logic g của AOI21 lại ra xấp xỉ bằng 1,0 thay vì 2,0?"
- **Giảng viên:** *"Em đặt trục hoành $h$ trong đồ thị hồi quy bằng công thức nào?"*
- **Sinh viên:** *"Dạ em lấy $h = C_L / 20\,\text{fF}$, với $20\,\text{fF}$ là điện dung của Inverter chuẩn ạ."*
- **Giảng viên:** *"Cổng AOI21 của em có điện trở kéo xuống bằng Inverter không?"*
- **Sinh viên:** *"Dạ bằng, em định cỡ $W_n = 8\lambda$ để có cùng $R_{on}$."*
- **Giảng viên:** *"Vậy nếu cùng $R_{on}$, thời gian trễ $t_{pd} \approx 0,69 R_{on} C_L$. Nếu em chia $C_L$ cho $C_{in,inv}$ để ra $h'$, thì $t_{pd} = \tau \cdot h'$. Hệ số góc theo $h'$ đương nhiên phải bằng $1 \cdot \tau$ rồi! Theo định nghĩa của Sutherland, nỗ lực điện $h$ của một cổng là tỉ số giữa tải ngoài với điện dung của chính cổng đó hay của Inverter?"*
- **Sinh viên:** *"Dạ của chính cổng đó ạ! Chân A có $W_n+W_p = 32\lambda$, tức $C_{in,A} = 2 \times C_{in,inv}$!"*
- **Giảng viên:** *"Chính xác! Khi em chia đúng cho $C_{in,A}$, tức $h = C_L / C_{in,A}$, thì với cùng tải $C_L$, biến $h$ giảm một nửa, làm hệ số góc tăng gấp đôi lên đúng bằng $2,0 \cdot \tau$!"*

### Tình huống 2: Sinh viên thắc mắc "Em đo trễ ngõ C thấy nhanh hơn ngõ A tới 25%, có phải do g_C < g_A không?"
- **Giảng viên:** *"Khi kích ngõ C, em đặt trạng thái tĩnh của ngõ A và B là bao nhiêu?"*
- **Sinh viên:** *"Dạ em đặt $A = 0\,\text{V}, B = 0\,\text{V}$."*
- **Giảng viên:** *"Nhìn vào sơ đồ nguyên lý: khi $A=0$ và $B=0$, hai transistor $M_{PA}$ và $M_{PB}$ dẫn thế nào?"*
- **Sinh viên:** *"Dạ cả hai cùng dẫn song song kéo lên nút $X_p$ ạ."*
- **Giảng viên:** *"Khi hai PMOS cùng dẫn song song thì điện trở cụm đó là bao nhiêu?"*
- **Sinh viên:** *"Dạ giảm một nửa còn $248\,\Omega$ ạ!"*
- **Giảng viên:** *"Đúng. Trễ sườn lên đo được nhanh hơn là vì em đang thử ở trường hợp tốt nhất (2 PMOS cùng dẫn), chứ không phải do $g_C < g_A$. Muốn đo trường hợp xấu nhất của ngõ C, em phải giữ $A=1, B=0$ để chỉ có đúng 1 PMOS dẫn!"*

### Tình huống 3: Sinh viên thắc mắc "Tại sao khi kiểm tra DRC giữa Poly C và Poly A lại bị báo lỗi khoảng cách?"
- **Giảng viên:** *"Giữa Poly C và Poly A trên layout của em có đặt cái gì không?"*
- **Sinh viên:** *"Dạ có Contact nối chân Out ra ngoài."*
- **Giảng viên:** *"Khoảng cách từ mép Contact tới mép Poly theo luật 3.2.b là bao nhiêu?"*
- **Sinh viên:** *"Dạ tối thiểu $2\lambda$ mỗi bên, cộng với bề rộng Contact $2\lambda$ là $6\lambda$ ạ! Em đặt nhầm $3\lambda$ của luật cách ly không có contact!"*

---

## 3.11 Đáp án Chi tiết Câu hỏi Post-lab

1. **Ưu thế và Giới hạn của Cổng phức hợp:**  
   - *Ưu thế:* Giảm số lượng transistor từ 30 - 40% và giảm diện tích silicon $\approx 18 - 25$%; triệt tiêu hoàn toàn các nút ký sinh liên tầng trung gian; giảm công suất tiêu tán động; giảm trễ tổng thể nhờ tín hiệu chỉ đi qua 1 tầng chuyển mạch.
   - *Giới hạn:* Việc mắc nối tiếp quá nhiều transistor ($\ge 4$) trong mạng PUN hoặc PDN làm tăng điện trở dẫn, tụ ký sinh nút nội $X_n, X_p$ tích tụ nhiều làm tăng trễ theo hàm bậc hai ($N^2$), đồng thời các transistor phía trên bị hiệu ứng thân nặng nề làm sụt giảm dòng điện nghiêm trọng.
2. **Bản chất Ưu thế của Ngõ vào C trong AOI21:**  
   - Ngõ vào C chỉ nối vào 1 NMOS đơn ($4\lambda$) và 1 PMOS nối tiếp ($24\lambda$) $\implies C_{in,C} \propto 28\lambda$ nhỏ hơn 12,5% so với ngõ A và B ($32\lambda$). Tầng logic lái phía trước khi nối vào ngõ C sẽ chịu tải nhẹ hơn và chuyển mạch nhanh hơn ($g_C = 1,75 < g_A = 2,00$).
   - Nhánh kéo xuống của ngõ C qua $M_{NC}$ đi trực tiếp từ $Out$ xuống đất, không có nút nội trung gian, loại bỏ hoàn toàn hiện tượng trễ do xả điện tích tồn dư tại nút nội.
3. **So sánh Đường rời NAND2 $\to$ INV $\to$ NOR2 với AOI21:**  
   - Phương án cổng rời:
     $$G = g_{NAND2} \times g_{INV} \times g_{NOR2} = 1,25 \times 1,00 \times 1,75 \approx \mathbf{2,19}$$
     $$\sum p = p_{NAND2} + p_{INV} + p_{NOR2} = 2,00 + 1,00 + 2,00 = \mathbf{5,00}$$
   - Phương án Cổng phức hợp AOI21:
     $$G = g_A = \mathbf{2,00} \quad (\text{hoặc } g_C = 1,75)$$
     $$p = \mathbf{2,25}$$
   - $\implies$ Cổng phức hợp AOI21 có tổng nỗ lực logic nhỏ hơn ($2,00 < 2,19$) và đặc biệt là trễ ký sinh nhỏ hơn hơn một nửa ($2,25$ so với $5,00$), chứng minh đáng kể hoàn toàn về tốc độ!

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & BỘ CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem Nghiệm thu Tại bàn (Thang 10):
- **1. Chuẩn bị Pre-lab (2.0 điểm):** Tính đúng kích thước và $g, p$ cho OAI21; giải đúng bài toán chuỗi đệm $F=64$; vẽ đúng Stick diagram $C-A-B$.
- **2. Schematic & Chân trị AOI21 (2.0 điểm):** Dựng đúng sơ đồ, 0 warning F5; kiểm chứng đủ 8 trạng thái logic sạch sẽ, xử lý tốt glitch.
- **3. Đo Logical Effort $g$ & $p$ (2.0 điểm):** Thiết lập đúng testbench kép với `INV_X1`; trích xuất thực nghiệm $g_{meas}$ và $p_{meas}$ khớp lý thuyết trong sai lệch $\le 15$%.
- **4. Tối ưu Chuỗi đệm (1.5 điểm):** Hiện thực chuẩn xác chuỗi đệm 3 tầng; chứng minh thực nghiệm trễ giảm $> 3$ lần so với lái trực tiếp 1X; phân tích rõ sườn xung.
- **5. Mask Layout, DRC & LVS (1.5 điểm):** Bố trí dải khuếch tán liền mạch $C-A-B$; khoảng cách Poly $\ge 6\lambda$ qua contact; DRC 0 errors; NCC LVS báo **"MATCH"**.
- **6. Báo cáo, Đối sánh PPA & Tác phong (1.0 điểm):** Lập bảng đối sánh đầy đủ; thái độ nghiêm túc; trả lời trôi chảy câu hỏi vấn đáp.

### 2. Bộ Câu hỏi Vấn đáp Nhanh tại Bàn Máy:
1. *Hỏi:* "Tại sao trong tế bào AOI21, các transistor PMOS lại phải định cỡ lên tới $24\lambda$ ($7,2\,\mu\text{m}$), gấp đôi kích thước của Inverter chuẩn?"  
   *Đáp chuẩn:* Vì mạng PUN của AOI21 gồm cụm song song $(A \parallel B)$ mắc nối tiếp với $C$. Trong trường hợp xấu nhất khi chỉ có 1 PMOS trong cụm song song dẫn, dòng nạp phải đi qua 2 PMOS mắc nối tiếp. Để tổng điện trở nhánh không vượt quá $R_{on,p0} \approx 992\,\Omega$, mỗi PMOS phải có chiều rộng kênh gấp đôi PMOS chuẩn ($2 \times 12\lambda = 24\lambda$).
2. *Hỏi:* "Nỗ lực logic $g$ phản ánh điều gì về mặt vật lý của cổng logic?"  
   *Đáp chuẩn:* Nỗ lực logic $g$ biểu thị tỉ số giữa điện dung ngõ vào của cổng đó so với Inverter chuẩn khi cả hai được định cỡ để có cùng khả năng tải dòng ($R_{on}$). Nó cho biết mức độ 'nặng tải' mà cổng logic đó tạo ra cho tầng lái phía trước so với một Inverter cơ sở.
3. *Hỏi:* "Tại sao thứ tự dải Polysilicon $C - A - B$ lại tối ưu hơn thứ tự $A - B - C$ khi vẽ Layout cổng AOI21?"  
   *Đáp chuẩn:* Vì với thứ tự $C - A - B$, cực má của $M_{NC}$ và $M_{NA}$ trên dải N-Active nằm kề sát nhau, cho phép dùng chung một tiếp xúc Contact ngõ ra `out` (Abutment). Ngược lại với thứ tự $A - B - C$, cực Out bị tách rời ra hai đầu dải khuếch tán, không thể chia sẻ cực má chung.
4. *Hỏi:* "Trong bài toán chuỗi đệm lái tải nặng $1\,\text{pF}$, tại sao chuỗi 3 tầng lại nhanh hơn việc lái trực tiếp bằng Inverter 1X tới hơn 3 lần?"  
   *Đáp chuẩn:* Vì Inverter 1X có kích thước quá nhỏ, nỗ lực điện $H = 50$ làm thời gian xả dòng bị kéo dài nghiêm trọng ($D = 51\tau$). Khi chèn chuỗi 3 tầng với hệ số phóng đại mỗi tầng $\hat{f} \approx 3,68$, mỗi tầng chỉ phải lái một tải dung vừa phải gấp $\approx 3,7$ lần chính nó, giúp các tầng chuyển mạch rất nhanh và tổng trễ chỉ còn $14,05\tau$ (giảm trễ 72,5%).
5. *Hỏi:* "Tính chất 'đáy phẳng' của hàm tối ưu chuỗi đệm có ý nghĩa thực tế gì đối với kỹ sư vi mạch?"  
   *Đáp chuẩn:* Đường cong trễ theo số tầng $N$ có đáy rất phẳng quanh điểm cực tiểu. Ví dụ với $H=50$, trễ của $N=4$ ($14,64\tau$) chỉ chậm hơn $N=3$ ($14,05\tau$) có 4%. Điều này cho phép kỹ sư linh hoạt chọn $N=4$ nếu cần giữ nguyên pha tín hiệu logic mà không sợ làm suy thoái tốc độ của toàn mạch.
