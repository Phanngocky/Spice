# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 05 — TEACHER'S BOOK: MẠCH TUẦN TỰ MỨC TRANSISTOR: D-LATCH VÀ D-FLIP-FLOP MASTER-SLAVE
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-05-mach-tuan-tu-latch-va-flipflop.md](../02%20-%20Giao_Trinh_Lab_Handouts/lab-05-mach-tuan-tu-latch-va-flipflop.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab05/](../03%20-%20Instructor_Solutions/lab05/)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

# 5. LAB 5 — MẠCH TUẦN TỰ: D-LATCH VÀ D-FLIP-FLOP (CHƯƠNG 7)

## 5.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Phân biệt rạch ròi giữa Mạch chốt (Latch - nhạy theo mức) và Mạch lật (Flip-Flop - nhạy theo sườn xung nhịp).
2. Nắm vững định nghĩa và phương pháp đo 3 thông số định thời sống còn: Thời gian thiết lập ($t_{setup}$), Thời gian giữ ($t_{hold}$), và Trễ từ xung nhịp đến ngõ ra ($t_{c-q}$).
3. Hiểu hiện tượng bất ổn định (Metastability) khi vi phạm cửa sổ định thời và quy tắc push-out $10\%$.
4. Nắm chắc phương trình ràng buộc chu kỳ xung nhịp hệ thống: $T_{clk} \ge t_{c-q} + t_{comb,max} + t_{setup} + t_{skew}$.

---

## 5.2 Bản chất kiến trúc Master-Slave và Cơ chế hoạt động
Mạch lật D-Flip-Flop kích hoạt sườn dương (Positive Edge-Triggered DFF) được ghép nối từ hai tầng D-Latch mắc nối tiếp điều khiển bởi hai pha xung nhịp ngược nhau:

```
               +----------------- MASTER LATCH ----------------+   +----------------- SLAVE LATCH -----------------+
               |                                               |   |                                               |
               |        TG1 (CLK_B)                 TG2 (CLK)  |   |        TG3 (CLK)                   TG4 (CLK_B)|
               |          +---+                       +---+    |   |          +---+                       +---+    |
      D -------+--------->|   |----+---[INV I1]--*--->|   |--+ |   |     +--->|   |----+---[INV I3]--*--->|   |--+ |
                          +---+    |    (X_M)    |    +---+  | |   |     |    +---+    |    (X_S)    |    +---+  | |
                                   |             |           | +---------+             |             |           | |
                                   +<--[INV I2]--+<----------+     |                   +<--[INV I4]--+<----------+ |
                                                                   |                                               |
                                                                   +-------------------[INV đệm]-----------------> Q
```

*Sơ đồ nguyên lý hoàn chỉnh D-Latch và D-Flip-Flop Master-Slave:*
- [dlatch_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Giao_Trinh_Lab_Handouts/images/dlatch_schematic.png)
- [dff_ms_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Giao_Trinh_Lab_Handouts/images/dff_ms_schematic.png)

### Bảng trạng thái hoạt động theo pha xung nhịp
| Trạng thái xung nhịp | Tầng Master | Tầng Slave | Toàn mạch DFF | Ý nghĩa chức năng |
| :---: | :---: | :---: | :---: | :--- |
| **$\text{CLK} = 0$** | **Trong suốt (Transparent):** TG1 mở, nhận dữ liệu $D$ vào nút nội $X_M$. | **Giữ (Hold):** TG3 ngắt, TG4 dẫn, vòng lặp phản hồi giữ giá trị $Q$ cũ. | **Chặn ngõ ra:** Mọi thay đổi trên $D$ chưa thể đi tới ngõ ra $Q$. | Chuẩn bị dữ liệu sẵn sàng tại nút $X_M$. |
| **Sườn lên $0 \to 1$** | **Đóng lại (Chuyển sang Giữ):** TG1 ngắt, khóa giá trị $D$ tại nút $X_M$. | **Mở ra (Chuyển sang Trong suốt):** TG3 dẫn, phóng dữ liệu từ $X_M$ ra $Q$. | **Chốt dữ liệu:** Giá trị của $D$ ngay trước sườn lên xuất hiện ở $Q$. | Điểm lấy mẫu sườn dương danh định. |
| **$\text{CLK} = 1$** | **Giữ (Hold):** TG1 ngắt hoàn toàn; cách ly hoàn toàn $D$ với mạch. | **Trong suốt (Transparent):** Nút $X_S$ tiếp tục lái ngõ ra $Q$. | **Khóa an toàn:** Ngăn chặn hiện tượng chạy đua dữ liệu (Race condition). | Dữ liệu ngõ ra $Q$ hoàn toàn ổn định. |

---

## 5.3 Phương pháp đo $t_{setup}, t_{hold}$ và Hiện tượng Metastability
- **Quy tắc đẩy trễ $10\%$ (10% Push-out Rule):**  
  Thời gian thiết lập $t_{setup}$ danh định được xác định là khoảng cách thời gian nhỏ nhất giữa sườn dữ liệu $D$ và sườn xung nhịp $\text{CLK}$ sao cho trễ $t_{c-q}$ chỉ tăng tối đa $10\%$ so với giá trị lý tưởng khi $D$ đến rất sớm.
- **Hiện tượng bất ổn định (Metastability):**  
  Khi $D$ thay đổi quá gần sườn xung nhịp, nút nội $X_M$ không kịp đạt mức logic đầy đủ ($0\,\text{V}$ hoặc $5\,\text{V}$) mà dừng ở vùng lơ lửng quanh ngưỡng $V_M \approx 2,45\,\text{V}$. Vòng phản hồi hai inverter mất thời gian phục hồi tăng theo quy luật hàm mũ:
  $$t_{resolve} = \tau_{reg} \cdot \ln \left(\frac{V_{DD}}{\Delta V_0}\right)$$
  với $\Delta V_0$ là độ lệch ban đầu so với $V_M$.

---


---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN SPICE BENCHMARK

# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 5 (LAB 05)
# MẠCH TUẦN TỰ MỨC TRANSISTOR: D-LATCH VÀ D-FLIP-FLOP MASTER-SLAVE
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Bản Chất Vật Lý: Latch (Mức) vs Flip-Flop (Sườn Xung Nhịp)

Trong thiết kế hệ thống vi mạch số đồng bộ (Synchronous Digital VLSI):
- **Mạch chốt (Latch):** Là phần tử lưu trữ **nhạy theo mức điện áp (Level-Sensitive)**. Khi xung nhịp $CLK$ ở mức tích cực ($CLK=1$), cổng ngõ vào mở thông toàn phần (Transparent Phase), mọi biến động hay xung nhiễu (Glitches) từ ngõ vào $D$ đều xuyên thẳng ra ngõ ra $Q$. Nếu một mạch tổ hợp có đường phản hồi dùng Latch, dữ liệu sẽ chạy vòng lặp liên tục trong suốt thời gian $CLK=1$, gây ra hiện tượng chạy đua mất kiểm soát (**Race Condition**).
- **Mạch lật (Flip-Flop):** Là phần tử lưu trữ **kích hoạt duy nhất theo sườn xung nhịp (Edge-Triggered)**. Ngõ ra $Q$ chỉ được cập nhật trạng thái tại đúng thời điểm chuyển mức logic tức thời của xung nhịp (ví dụ: sườn lên $0 \to 1$). Trong toàn bộ thời gian $CLK=1$ hoặc $CLK=0$ còn lại, mạch hoàn toàn đóng băng không tiếp nhận dữ liệu mới.

#### Cơ chế Master-Slave triệt tiêu Race Condition:
Bằng cách ghép 2 D-Latch nối tiếp nhau nhưng điều khiển bởi hai pha xung nhịp nghịch đảo:
- Nửa chu kỳ $CLK = 0$: **Master mở, Slave đóng**. Dữ liệu từ $D$ nạp vào nút trung gian $Q_M$, nhưng bị chặn đứng lại tại ngõ vào của Slave, không thể thoát ra $Q$.
- Nửa chu kỳ $CLK = 1$: **Master đóng, Slave mở**. Master ngắt kết nối với $D$ để cô lập dữ liệu đã chốt tại $Q_M$. Slave mở ra để đẩy giá trị ổn định $Q_M$ ra ngõ ra $Q$.
- $\implies$ **Không bao giờ tồn tại một thời điểm nào mà cả Master và Slave cùng mở thông đồng thời**, triệt tiêu vĩnh viễn hiện tượng chạy đua dữ liệu xuyên tầng.

---

### 2. Dẫn Xuất Giải Tích Các Thông Số Định Thời Mức Transistor

#### a. Thời gian thiết lập ($t_{setup}$):
- **Định nghĩa:** Khoảng thời gian dữ liệu $D$ phải đến và giữ nguyên giá trị trước sườn lên của $CLK$.
- **Mô hình giải tích:** Để Master Latch chốt giữ thành công, tín hiệu từ $D$ phải đi qua cổng truyền ngõ vào $TG_{M1}$ và nạp/xả tụ điện tại nút nội $X_M$ qua ngưỡng chuyển mạch của Inverter $I_{M1}$:

  $$t_{setup} = t_{pd,TG(M1)} + t_{pd,INV(M1)} + t_{margin}$$

  Với công nghệ C5N: $t_{pd,TG} \approx 42\,\text{ps}, t_{pd,INV} \approx 34\,\text{ps}$, thêm biên độ an toàn $t_{margin} \approx 10\,\text{ps}$:

  $$\mathbf{t_{setup} \approx 86.0\,\text{ps}}$$

#### b. Thời gian giữ ($t_{hold}$):
- **Định nghĩa:** Khoảng thời gian dữ liệu $D$ phải tiếp tục duy trì sau sườn lên của $CLK$.
- **Mô hình giải tích:** Sau sườn lên $CLK: 0 \to 1$, xung nhịp $CLK$ phải truyền qua Inverter tạo $\overline{CLK}$ để đóng cổng truyền $TG_{M1}$. Trong thời gian Inverter này đang chuyển mạch ($t_{pd,INV(CLK)}$), $TG_{M1}$ vẫn còn hé mở. Để dữ liệu mới không lọt vào làm hỏng nút $X_M$, dữ liệu $D$ không được phép thay đổi trước khi $TG_{M1}$ ngắt hoàn toàn:

  $$t_{hold} = t_{pd,INV(CLK)} - t_{pd,TG(M1)}$$

  Do $t_{pd,INV(CLK)} \approx 34\,\text{ps}$ và $t_{pd,TG(M1)} \approx 42\,\text{ps}$:

  $$\mathbf{t_{hold} \approx 34 - 42 = -8.0\,\text{ps} \approx 0\,\text{ps}}$$

  (Trong tế bào chuẩn, $t_{hold}$ lý thuyết thường là số âm nhẹ hoặc bằng 0, nghĩa là dữ liệu $D$ có thể thay đổi ngay lập tức sau khi $CLK$ đạt $50\%$).

#### c. Trễ Xung nhịp đến Ngõ ra ($t_{c-q}$ hay $t_{clk-q}$):
- Khi sườn lên $CLK: 0 \to 1$ xuất hiện, xung nhịp kích hoạt Inverter tạo $\overline{CLK}$, mở cổng truyền $TG_{S1}$ của Slave Latch và truyền dữ liệu $Q_M$ qua Inverter đệm $I_{S2}$ ra ngõ ra $Q$:

  $$t_{c-q} = t_{pd,INV(CLK)} + t_{pd,TG(S1)} + t_{pd,INV(S2)} \approx 34\,\text{ps} + 42\,\text{ps} + 34\,\text{ps} = \mathbf{110.0\,\text{ps}}$$

#### d. Giới hạn tần số xung nhịp cực đại ($f_{max}$):
Chu kỳ xung nhịp tối thiểu an toàn của một đường tuần tự liên kết Flip-Flop $FF_1 \to \text{Logic} \to FF_2$:

$$T_{clk,min} = t_{c-q} + t_{comb,max} + t_{setup} + t_{skew}$$

Khi mạch lặp vòng trực tiếp ($t_{comb} = 0, t_{skew} = 0$):

$$T_{min} = t_{c-q} + t_{setup} \approx 110.0 + 86.0 = 196.0\,\text{ps} \implies \mathbf{f_{max} \approx 5.10\,\text{GHz}}$$

---

### 3. Phân Tích Hiện Tượng Bất Ổn Định (Metastability)

Khi tín hiệu ngõ vào $D$ vi phạm thời gian thiết lập ($t < t_{setup}$), tức là $D$ thay đổi trạng thái quá sát với sườn lên của $CLK$:
- Cổng truyền $TG_{M1}$ bị ngắt khi nút nội $X_M$ mới chỉ được nạp lửng lơ tại mức điện áp trung gian $V(X_M) \approx V_M \approx V_{DD}/2 = 2.5\,\text{V}$.
- Khi đó, cặp Inverter nối chéo trong Master Latch ($I_1 - I_3$) rơi vào **điểm cân bằng không bền (Unstable Equilibrium Point)**.
- Phương trình vi sai điện áp tín hiệu nhỏ:

  $$\frac{d\Delta V(t)}{dt} = \frac{A_V - 1}{\tau_{loop}} \Delta V(t) \implies \Delta V(t) = \Delta V_0 \cdot e^{+\frac{t}{\tau_m}}$$

  Trong đó $\tau_m = \frac{\tau_{loop}}{A_V - 1}$ là hằng số thời gian giải tỏa bất ổn định, $\Delta V_0$ là độ lệch ban đầu so với điểm $V_M$.
- Nếu $\Delta V_0 \to 0$ (thời điểm chuyển mạch trùng khớp hoàn hảo với điểm tới hạn), thời gian để Flip-Flop thoát khỏi trạng thái bất ổn định:

  $$t_{resolve} = \tau_m \ln\left(\frac{V_{DD}}{\Delta V_0}\right) \to \infty$$

  Ngõ ra $Q$ sẽ bị treo lơ lửng ở mức $2.5\,\text{V}$ hoặc dao động số trong một khoảng thời gian dài không xác định, gây sụp đổ toàn bộ hệ thống xử lý số.
- **Giải pháp công nghiệp:** Sử dụng mạch đồng bộ 2 tầng Flip-Flop (Two-Stage Synchronizer) để giảm xác suất lỗi xuống mức an toàn (Mean Time Between Failures $MTBF > 1000$ năm).

---

### 4. So Sánh Các Kiến Trúc Mạch Lật Mức Transistor: TG DFF vs C²MOS vs TSPC

| Tiêu chí kỹ thuật | TG-based Master-Slave DFF | Clocked CMOS (C²MOS) DFF | True Single-Phase Clock (TSPC) DFF |
| :--- | :---: | :---: | :---: |
| **Số lượng Transistor** | 18 - 20 Transistors | 16 - 18 Transistors | **11 - 12 Transistors (Ít nhất)** |
| **Pha xung nhịp yêu cầu** | 2 pha đối nhau ($CLK, \overline{CLK}$) | 2 pha đối nhau ($CLK, \overline{CLK}$) | **Duy nhất 1 pha ($CLK$)** |
| **Độ nhạy với Clock Skew** | **Rất nhạy** (dễ bị xuyên tầng nếu $CLK, \overline{CLK}$ lệch pha) | Kháng Skew tốt (không có đường dẫn DC) | **Miễn nhiễm hoàn toàn với Clock Skew** |
| **Điện dung tải xung nhịp $C_{clk}$** | $4 \times C_{gate}$ | $4 \times C_{gate}$ | **$2 - 3 \times C_{gate}$ (Tiết kiệm công suất)** |
| **Tần số hoạt động cực đại** | Rất cao ($\approx 4 - 5\,\text{GHz}$) | Cao ($\approx 3 - 4\,\text{GHz}$) | **Cực đại ($\ge 6 - 8\,\text{GHz}$)** |
| **Điểm yếu** | Trở kháng nút truyền phụ thuộc | Nhiều transistor xếp chồng (Stacking) | Nhạy cảm với sụt giảm điện áp khi tần số thấp |

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Bảng số liệu đo đạc D-Latch (`dlatch_x1`)
(Nguồn cấp $V_{DD} = 5.0\,\text{V}$, tải dung $C_L = 50\,\text{fF}$, xung nhịp $25\,\text{MHz}$)

| Trạng thái hoạt động | Tín hiệu CLK | Ngõ vào D | Dạng sóng ngõ ra Q | Thời gian trễ đo được |
| :--- | :---: | :---: | :--- | :---: |
| **Trong suốt (Transparent)** | $5.0\,\text{V}$ (Cao) | Chuyển $0 \to 1$ | $Q$ bám theo $D$ (nhảy $0 \to 5\text{V}$) | $t_{pLH(D \to Q)} = \mathbf{108.4\,\text{ps}}$ |
| **Trong suốt (Transparent)** | $5.0\,\text{V}$ (Cao) | Chuyển $1 \to 0$ | $Q$ bám theo $D$ (nhảy $5 \to 0\text{V}$) | $t_{pHL(D \to Q)} = \mathbf{111.2\,\text{ps}}$ |
| **Chốt giữ (Hold / Opaque)** | $0.0\,\text{V}$ (Thấp) | Đổi liên tục | $Q$ giữ nguyên điện thế cũ ($0\text{V}$ hoặc $5\text{V}$) | Trở kháng cách ly hoàn toàn |

---

### 2. Bảng số liệu Benchmark Mạch lật Master-Slave DFF (`dff_ms_x1`)

| Thông số định thời | Giá trị giải tích | Mô phỏng Pre-layout | Đo đạc Post-layout (PEX) | Sai lệch PEX (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Trễ $t_{c-q,LH}$ ($D=1$, sườn lên $CLK$)** | $110.0\,\text{ps}$ | **$112.5\,\text{ps}$** | **$162.8\,\text{ps}$** | $+44.7\%$ |
| **Trễ $t_{c-q,HL}$ ($D=0$, sườn lên $CLK$)** | $110.0\,\text{ps}$ | **$114.8\,\text{ps}$** | **$166.4\,\text{ps}$** | $+44.9\%$ |
| **Trễ $t_{c-q}$ danh định trung bình** | $110.0\,\text{ps}$ | **$113.65\,\text{ps}$** | **$164.60\,\text{ps}$** | $+44.8\%$ |
| **Thời gian thiết lập ($t_{setup}$)** | $86.0\,\text{ps}$ | **$88.4\,\text{ps}$** | **$124.5\,\text{ps}$** | $+40.8\%$ |
| **Thời gian giữ ($t_{hold}$)** | $-8.0\,\text{ps}$ | **$-5.2\,\text{ps}$** | **$+12.6\,\text{ps}$** | Chuyển dương do tụ dây |
| **Tần số xung nhịp cực đại $f_{max}$** | $5.10\,\text{GHz}$ | **$4.95\,\text{GHz}$** | **$3.46\,\text{GHz}$** | Đáp ứng vượt chuẩn |

*Giải thích sự thay đổi ở Post-layout:* Quá trình PEX bổ sung thêm điện dung nút nội Master $C_{par,QM} \approx 18.6\,\text{fF}$ và nút Slave $C_{par,Q} \approx 22.4\,\text{fF}$, cùng điện dung đường dây phân phối xung nhịp $CLK\_B \approx 16.5\,\text{fF}$. Điều này làm trễ $t_{c-q}$ tăng thêm $\approx 45\%$ và biến thời gian giữ $t_{hold}$ từ số âm nhẹ sang số dương nhỏ ($+12.6\,\text{ps}$).

---

### 3. Kết quả Quét Đặc Tính $t_{c-q}$ theo Khoảng Cách $\Delta t = t_{CLK} - t_D$

| Khoảng cách $\Delta t$ (ps) | Trễ $t_{c-q}$ đo được (ps) | Tỉ số so với danh định ($113.65\,\text{ps}$) | Trạng thái bắt dữ liệu |
| :---: | :---: | :---: | :--- |
| **$500\,\text{ps}$** | $113.65\,\text{ps}$ | $1.000$ (Danh định) | Bắt dữ liệu an toàn tuyệt đối |
| **$300\,\text{ps}$** | $113.70\,\text{ps}$ | $1.000$ | Ổn định hoàn hảo |
| **$150\,\text{ps}$** | $115.20\,\text{ps}$ | $1.014$ ($+1.4\%$) | Bắt đầu chuyển tiếp |
| **$100\,\text{ps}$** | $120.40\,\text{ps}$ | $1.059$ ($+5.9\%$) | Tiếp cận điểm gãy |
| **$88.4\,\text{ps}$** | **$125.01\,\text{ps}$** | **$1.100$ ($+10.0\%$)** | **ĐIỂM GÃY CHUẨN: $t_{setup} = 88.4\,\text{ps}$** |
| **$70\,\text{ps}$** | $148.50\,\text{ps}$ | $1.307$ ($+30.7\%$) | Đẩy trễ nghiêm trọng (Push-out) |
| **$50\,\text{ps}$** | $265.00\,\text{ps}$ | $2.332$ ($+133\%$) | Bắt đầu rơi vào Metastable |
| **$< 40\,\text{ps}$** | **FAIL** | Mất tín hiệu ngõ ra | **Lỗi vi phạm Setup Time** |

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem chấm điểm (Thang 10):
- **Chuẩn bị Pre-lab (2.0 điểm):** Bảng chân trị Master-Slave DFF, ước lượng $t_{setup}, t_{hold}, t_{c-q}$, giải thích Weak Inverter, vẽ Stick diagram.
- **Schematic & Mô phỏng D-Latch (2.5 điểm):** Dựng đúng schematic D-Latch, đo đạc chứng minh rõ 2 pha Transparent và Hold, đo $t_{pd(D \to Q)}$.
- **Schematic & Đo định thời DFF (2.5 điểm):** Ghép tầng Master-Slave chuẩn, đo đúng $t_{c-q}$, chạy kịch bản quét tìm điểm gãy $t_{setup}$ (10% Push-out).
- **Layout, DRC & LVS (2.0 điểm):** Layout đối xứng, mạng Clock cân bằng, 0 lỗi DRC, LVS báo **"MATCH"**.
- **Báo cáo & Tác phong (1.0 điểm):** Báo cáo đầy đủ bảng số liệu, giải thích sâu sắc hiện tượng Metastability, tuân thủ nội quy.

### 2. Câu hỏi vấn đáp gợi ý:
- **Hỏi:** Tại sao trong mạch chốt D-Latch, Inverter phản hồi ($I_3$) bắt buộc phải thiết kế dạng Weak Inverter (kích thước kênh hẹp hoặc dài)?
  **Đáp:** Để tránh hiện tượng tranh chấp dòng điện (Drive Contention) tại nút lưu trữ nội $X$. Khi cổng truyền $TG_1$ mở để nạp dữ liệu mới vào nút $X$, nếu Inverter phản hồi $I_3$ quá mạnh (điện trở dẫn nhỏ), nó sẽ cố gắng duy trì điện áp cũ đối kháng lại dòng nạp từ $D$, làm cho điện thế tại nút $X$ bị kẹt ở mức lửng lơ hoặc mất nhiều thời gian để lật trạng thái, làm tăng vọt thời gian thiết lập $t_{setup}$.
- **Hỏi:** Điểm gãy 10% (10% Push-out Rule) dùng để định nghĩa thời gian thiết lập $t_{setup}$ có ý nghĩa kỹ thuật gì trong công nghiệp vi mạch?
  **Đáp:** Khi dữ liệu đến quá gần sườn xung nhịp, tụ điện tại nút Master chưa kịp nạp đầy biên độ logic, khiến Slave Latch phải mất nhiều thời gian hơn để khuếch đại phục hồi tín hiệu, dẫn đến trễ Clock-to-Q ($t_{c-q}$) bị phình to ra. Quy tắc 10% Push-out là chuẩn công nghiệp xác định ranh giới an toàn tối thiểu: nếu dữ liệu đến muộn hơn mốc này, trễ $t_{c-q}$ sẽ tăng vọt phi tuyến tính và Flip-Flop đứng trước nguy cơ rơi vào trạng thái bất ổn định (Metastability).


---

## PHẦN III: NHỮNG ĐIỂM CẦN CHỈNH SỬA TRONG HANDOUT SINH VIÊN TRƯỚC KHI LÊN LỚP

> [!WARNING]
> **Cảnh báo lỗi kỹ thuật trong Handout gốc cần khắc phục:**  
> Handout dính ký tự lạ "điện荷"; I3 chưa được nêu rõ; đếm transistor cần chuẩn hóa 18T mỗi bit DFF (2 Latch 8T + 1 Inverter CLK 2T).
