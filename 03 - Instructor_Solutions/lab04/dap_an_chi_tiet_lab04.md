# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 4 (LAB 04)
# CỔNG TRUYỀN (TRANSMISSION GATE) VÀ BỘ DỒN KÊNH MUX MỨC TRANSISTOR
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Dẫn Xuất Giải Tích Sụt Giảm Điện Áp Ngưỡng Do Hiệu Ứng Thân (Body Effect)

Khi sử dụng một transistor đơn lẻ làm khóa dẫn (Pass Transistor):
- Xét transistor NMOS có cực Cổng $V_G = V_{DD}$, cực Máng $V_D = V_{DD}$, và cực Nguồn nối vào tụ tải $C_L$ có điện áp tức thời $V_{out}(t)$.
- Điều kiện để NMOS duy trì trạng thái dẫn là:
  $$V_{GS} \ge V_{thn} \iff V_{DD} - V_{out} \ge V_{thn} \iff V_{out} \le V_{DD} - V_{thn}$$
- Khi tụ nạp điện, điện áp cực Nguồn tăng dần làm điện áp ngược giữa cực Nguồn và cực Thân (nối đất) tăng theo:
  $$V_{SB} = V_{out} - V_{Bulk} = V_{out} - 0 = V_{out} > 0$$
- Theo phương trình vật lý bán dẫn của hiệu ứng thân (Body Effect / Back-Gate Bias):
  $$V_{thn}(V_{SB}) = V_{th0} + \gamma \left( \sqrt{2\phi_F + V_{SB}} - \sqrt{2\phi_F} \right)$$
  Trong đó:
  * $V_{th0} = 0.700\,\text{V}$: Điện áp ngưỡng khi chưa có phân cực thân ($V_{SB} = 0$).
  * $\gamma = \frac{\sqrt{2 q \epsilon_{si} N_A}}{C_{ox}} \approx 0.53\,\text{V}^{1/2}$: Hệ số hiệu ứng thân của tiến trình MOSIS C5N.
  * $2\phi_F \approx 0.650\,\text{V}$: Điện thế bề mặt đảo cực.

#### Giải phương trình điểm cân bằng điện áp đỉnh ngõ ra:
Điện áp ra cực đại $V_{out,max}$ thỏa mãn hệ phương trình phi tuyến:
$$V_{out,max} = V_{DD} - \left[ V_{th0} + \gamma \left( \sqrt{2\phi_F + V_{out,max}} - \sqrt{2\phi_F} \right) \right]$$
Thay các tham số công nghệ MOSIS C5N ($V_{DD} = 5.0\,\text{V}$):
$$V_{out,max} = 5.0 - \left[ 0.70 + 0.53 \left( \sqrt{0.65 + V_{out,max}} - \sqrt{0.65} \right) \right]$$
$$V_{out,max} + 0.53 \sqrt{0.65 + V_{out,max}} - 4.727 = 0$$
Giải phương trình số cho kết quả chính xác:
$$\mathbf{V_{out,max} \approx 3.631\,\text{V}} \implies \mathbf{V_{thn,eff} \approx 1.369\,\text{V}}$$

> [!IMPORTANT]
> **Điểm mấu chốt sư phạm:** Sinh viên thường nghĩ sai rằng điện áp đỉnh khi nạp qua NMOS chỉ là $V_{DD} - V_{th0} = 5.0 - 0.70 = 4.30\,\text{V}$.  
> Giảng viên cần chỉ rõ rằng do tác động của **hiệu ứng thân ($V_{SB} > 0$)**, điện áp ngưỡng thực tế đã tăng gần gấp đôi (từ $0.70\,\text{V}$ lên $1.37\,\text{V}$), khiến điện áp đỉnh bị suy giảm nghiêm trọng xuống chỉ còn **$3.63\,\text{V}$ (Weak '1')**.  
> Mức điện áp $3.63\,\text{V}$ này nếu đưa vào cổng logic CMOS tiếp theo sẽ làm cho transistor PMOS của cổng đó không thể ngắt hoàn toàn ($|V_{GS,p}| = 5.0 - 3.63 = 1.37\,\text{V} > |V_{thp}| = 0.80\,\text{V}$), gây ra dòng ngắn mạch rò tĩnh ($I_{static}$) khổng lồ từ nguồn xuống đất!

Tương tự, đối với PMOS khi truyền mức '0', cực Cổng nối đất, cực Máng nối đất, cực Nguồn giảm từ $5\,\text{V}$ xuống đất. Hiệu điện thế $V_{BS} = V_{DD} - V_{out} > 0$ làm $|V_{thp}|$ tăng lên $\approx 1.05\,\text{V}$, khiến điện áp ra cực tiểu bị chặn lại ở **$V_{out,min} \approx 0.80 - 1.05\,\text{V}$ (Weak '0')**.

---

### 2. Nguyên Lý Bù Trừ Toàn Dải Của Cổng Truyền CMOS (Transmission Gate)

Cổng truyền CMOS ghép song song 1 NMOS ($W_n = 4\lambda = 1.2\,\mu\text{m}$) và 1 PMOS ($W_p = 12\lambda = 3.6\,\mu\text{m}$):
- Khi $EN = 1$ ($EN = 5\,\text{V}, \overline{EN} = 0\,\text{V}$):
  * **Vùng điện áp thấp ($V_{in} \in [0\,\text{V}, V_{DD} - V_{thn}]$):** NMOS dẫn cực mạnh ở vùng tuyến tính (Triode) vì $V_{GS,n} = 5.0\,\text{V}$ và $V_{DS,n}$ nhỏ. Kéo $V_{out}$ xuống sát đúng **$0.000\,\text{V}$ (Strong '0')**.
  * **Vùng điện áp cao ($V_{in} \in [|V_{thp}|, V_{DD}]$):** PMOS dẫn cực mạnh ở vùng tuyến tính vì $|V_{GS,p}| = 5.0\,\text{V}$. Kéo $V_{out}$ lên tới đúng **$5.000\,\text{V}$ (Strong '1')**.
  * $\implies$ Cổng truyền đạt **Full Rail-to-Rail Swing ($0.000\,\text{V} \leftrightarrow 5.000\,\text{V}$)**.

#### Điện trở dẫn tương đương $R_{TG}$ trên toàn dải:
$$R_{TG}(V_{in}) = R_{on,n}(V_{in}) \parallel R_{on,p}(V_{in}) = \frac{R_{on,n} \cdot R_{on,p}}{R_{on,n} + R_{on,p}}$$
- Khi $V_{in} \to 0\,\text{V}$: NMOS ở vùng triode ($R_{on,n} \approx 969\,\Omega$), PMOS ngắt ($R_{on,p} \to \infty$) $\implies R_{TG} \approx 969\,\Omega$.
- Khi $V_{in} \to 5\,\text{V}$: PMOS ở vùng triode ($R_{on,p} \approx 992\,\Omega$), NMOS ngắt ($R_{on,n} \to \infty$) $\implies R_{TG} \approx 992\,\Omega$.
- Khi $V_{in} \approx 2.5\,\text{V}$: Cả NMOS và PMOS đều cùng dẫn ở vùng bão hòa $\implies R_{TG} \approx 969 \parallel 992 \approx 490\,\Omega$.  
$\implies$ **Đặc tính phẳng:** Điện trở tương đương dao động rất hẹp quanh khoảng $500 - 1000\,\Omega$, giúp trễ qua cổng truyền độc lập với hướng chuyển mức logic ($0 \to 1$ hoặc $1 \to 0$).

---

### 3. Trễ Elmore Chuỗi Cổng Truyền Ghép Tầng (Distributed RC Delay)

Một cạm bẫy thiết kế vi mạch kinh điển: Khi ghép nối tiếp $N$ cổng truyền liên tiếp mà không có cổng đệm Inverter ở giữa (ví dụ trong mạng chuyển mạch Barrel Shifter hoặc mạng định tuyến):
- Mỗi cổng truyền đóng vai trò là một điện trở dẫn $R_{TG}$ và đóng góp điện dung ký sinh nút khuếch tán $C_{TG}$.
- Mô hình mạng bậc thang $RC$ phân bố (Elmore Delay Network):
  $$t_{pd} = \sum_{i=1}^N R_i \left(\sum_{j=i}^N C_j\right) = R_{TG} C_{TG} \frac{N(N+1)}{2} = \mathbf{O(N^2)}$$
$\implies$ **Quy tắc thiết kế sư phạm:** Trễ tăng theo **hàm bậc hai của số tầng ($N^2$)**. Nếu chuỗi vượt quá **3 đến 4 cổng truyền**, trễ sẽ bùng nổ và sườn xung bị thoái hóa nặng. Trong công nghiệp vi mạch, kỹ sư **bắt buộc phải chèn một bộ đệm Inverter cứ sau mỗi 3 cổng truyền** để cắt đứt chuỗi $RC$ phân bố thành trễ tuyến tính $O(N)$.

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Bảng số liệu đo đạc thực nghiệm Pass Transistor vs TG

*(Số liệu mô phỏng Transient trên LTspice, tải dung $C_L = 50\,\text{fF}$, tần số $20\,\text{MHz}$)*

| Cấu hình khóa dẫn | Mức điện áp cực tiểu $V_{min}$ | Mức điện áp cực đại $V_{max}$ | Biên độ logic đỉnh-đỉnh | Nhận xét tính chất vật lý |
| :--- | :---: | :---: | :---: | :--- |
| **NMOS Pass Transistor** | **$0.000\,\text{V}$** | **$3.631\,\text{V}$** | $3.631\,\text{V}$ | **Weak '1'** (sụt áp $1.369\,\text{V}$ do Body Effect) |
| **PMOS Pass Transistor** | **$0.865\,\text{V}$** | **$5.000\,\text{V}$** | $4.135\,\text{V}$ | **Weak '0'** (sụt áp $0.865\,\text{V}$ do $\vert V_{thp} \vert$) |
| **CMOS Transmission Gate**| **$0.000\,\text{V}$** | **$5.000\,\text{V}$** | **$5.000\,\text{V}$** | **Strong '0' & Strong '1' (Full Rail-to-Rail)** |

---

### 2. Bảng số liệu đo đạc Bộ dồn kênh `mux2_tg` ($C_L = 50\,\text{fF}$)

| Đường truyền tín hiệu | Trễ sườn xuống $t_{pHL}$ (ps) | Trễ sườn lên $t_{pLH}$ (ps) | Trễ trung bình $t_{pd}$ (ps) | Nhận xét |
| :--- | :---: | :---: | :---: | :--- |
| **$D_0 \to Y$ (khi $S=0$)** | **$41.5\,\text{ps}$** | **$43.8\,\text{ps}$** | **$42.65\,\text{ps}$** | Truyền trực tiếp qua $TG_0$ |
| **$D_1 \to Y$ (khi $S=1$)** | **$41.2\,\text{ps}$** | **$43.5\,\text{ps}$** | **$42.35\,\text{ps}$** | Truyền trực tiếp qua $TG_1$ |
| **Chọn kênh $S \to Y$** | **$68.4\,\text{ps}$** | **$72.1\,\text{ps}$** | **$70.25\,\text{ps}$** | Bao gồm trễ qua Inverter tạo $\overline{S}$ + trễ bật TG |
| **Post-layout PEX ($D_0 \to Y$)** | **$62.8\,\text{ps}$** | **$66.4\,\text{ps}$** | **$64.60\,\text{ps}$** | Tăng $\approx 51.5\%$ do tụ ký sinh tiếp giáp cực má |

---

### 3. Kết quả kiểm chứng MUX 4:1 phân cấp (`mux4_tg`)

| Tín hiệu chọn $(S_1, S_0)$ | Kênh dữ liệu được truyền ra ngõ Y | Điện áp trung bình đo được tại Y | Mức logic xác nhận |
| :---: | :---: | :---: | :---: |
| `00` | $D_0$ ($0.0\,\text{V}$) | **$0.000\,\text{V}$** | Logic '0' chuẩn |
| `01` | $D_1$ ($5.0\,\text{V}$) | **$5.000\,\text{V}$** | Logic '1' chuẩn |
| `10` | $D_2$ ($0.0\,\text{V}$) | **$0.000\,\text{V}$** | Logic '0' chuẩn |
| `11` | $D_3$ ($5.0\,\text{V}$) | **$5.000\,\text{V}$** | Logic '1' chuẩn |

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem chấm điểm (Thang 10):
- **Chuẩn bị Pre-lab (2.0 điểm):** Tính đúng $V_{out,max}$ của NMOS theo Body Effect, lập đúng bảng chân trị MUX 2:1 và 4:1, vẽ Stick diagram MUX 2:1.
- **Khảo sát Pass Transistor vs TG (2.5 điểm):** Mô phỏng 3 nhánh, đo đạc chỉ ra Weak '1' ($3.63\text{V}$), Weak '0' ($0.86\text{V}$) và Full Swing ($5.0\text{V}$).
- **Schematic & Đo trễ MUX 2:1 và MUX 4:1 (2.5 điểm):** Dựng đúng schematic, 6 chân Export, kiểm chứng dạng sóng dồn kênh 2 tần số, đo đủ trễ $D \to Y$ và $S \to Y$.
- **Layout `mux2_tg`, DRC & LVS (2.0 điểm):** Bố trí 6 transistor chặt chẽ, 0 lỗi DRC, LVS báo **"MATCH"**.
- **Báo cáo & Tác phong (1.0 điểm):** Phiếu báo cáo đầy đủ, giải thích sâu sắc hiện tượng trễ $O(N^2)$, giữ vệ sinh công nghiệp.

### 2. Câu hỏi vấn đáp gợi ý:
- **Hỏi:** *Tại sao khi mắc nối tiếp nhiều cổng truyền liên tiếp ($N \ge 4$), thời gian trễ lại tăng theo hàm bậc hai $O(N^2)$ thay vì tuyến tính?*  
  **Đáp:** Vì mỗi cổng truyền đóng vai trò là một khâu $RC$ phân bố (Distributed $RC$ Network) không có tầng đệm khuếch đại. Theo công thức trễ Elmore, tụ điện của cổng thứ $N$ phải được nạp/xả qua tổng trở của toàn bộ $N$ điện trở phía trước nó, dẫn đến tổng trễ tỉ lệ với $\sum_{i=1}^N i = \frac{N(N+1)}{2} = O(N^2)$.
- **Hỏi:** *Tại sao trong Cổng truyền, cực thân (Bulk) của PMOS luôn phải nối lên $V_{DD}$ mà không được nối vào cực Source hay cực Drain của chính nó?*  
  **Đáp:** Vì tín hiệu tại cực Source và Drain của cổng truyền là tín hiệu hai chiều (Bidirectional) và biến thiên liên tục trong dải $0 \to V_{DD}$. Nếu nối Bulk vào Source/Drain, khi điện áp tại đó tụt xuống mức thấp, mối nối P-N giữa N-Well và các vùng khuếch tán lân cận có thể bị phân cực thuận ($V_{PN} > 0.7\,\text{V}$), dẫn tới dòng rò lớn qua đế hoặc kích hoạt hiện tượng Latch-up gây cháy chip.
