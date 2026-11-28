# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 07 — TEACHER'S BOOK: KỸ THUẬT LOGIC ĐỘNG VÀ LOGIC DOMINO
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-07-logic-dong-dynamic-cmos.md](../02%20-%20Student%20Workbook/lab-07-logic-dong-dynamic-cmos.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab07/](../03%20-%20Instructor_Solutions/lab07/)  
> **Script kiểm chứng số liệu:** [verify_lab07_new.py](../scripts/verify_lab07_new.py)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

### 7.0 Khái niệm chung, Định nghĩa chuẩn & Vai trò các tầng/tham số trong thực tế
*(Phần trình bày nhanh trên bảng 5–7 phút trước khi vào bài)*

1. **Khái niệm chung:**
   - **Dynamic CMOS Logic (Logic động):** Thay thế toàn bộ mạng kéo lên PMOS (PUN) cồng kềnh bằng **duy nhất 1 PMOS nạp trước ($M_{pre}$)** và **1 Foot NMOS ($M_{eval}$)** điều khiển bởi xung nhịp `CLK`, giúp giảm mạnh tổng bề rộng $\Sigma W$ và điện dung ngõ vào $C_{in}$ trên mỗi chân so với logic tĩnh.
   - **Domino CMOS Logic:** Gắn thêm một **Inverter tĩnh** ở ngõ ra nút động $X$ để đảm bảo tín hiệu ra $Y$ luôn bằng $0$ trong pha Precharge và chỉ có thể tăng đơn điệu ($0 \to 1$) trong pha Evaluate, cho phép ghép nối nhiều tầng liên tiếp.
2. **Định nghĩa chuẩn:**
   - **Pha Precharge (`CLK=0`) & Pha Evaluate (`CLK=1`):** Ở Precharge, $M_{pre}$ nạp $X$ lên $V_{DD}$ (Foot ngắt không cho xả); ở Evaluate, $M_{pre}$ ngắt và $M_{eval}$ mở để $X$ giữ mức cao hoặc xả qua PDN.
   - **Charge Sharing (Chia sẻ điện tích):** Hiện tượng tụ ký sinh nút nội cô lập $C_{int}$ (đang ở $0\,\text{V}$) hút bớt điện tích từ nút động $C_X$ (đang ở $V_{DD}$) khi transistor trên mở và transistor dưới khóa trong pha Evaluate.
   - **Tính đơn điệu (Monotonicity):** Tính chất ngõ ra $Y$ của cổng Domino chỉ chuyển $0 \to 1$ trong pha Evaluate (không thể chuyển $1 \to 0$ giữa chừng).
3. **Vai trò từng tầng mạch & tham số trong thực tế:**

| Tầng / Tham số | Vai trò trong mạch & Ý nghĩa thực tế khi thiết kế chip |
| :--- | :--- |
| **PMOS Precharge $M_{pre}$ & Foot $M_{eval}$** | $M_{pre}$ nạp nhanh nút $X$ lúc `CLK=0`; Foot $M_{eval}$ ngắt đường đất lúc `CLK=0` tránh ngắn mạch. Trong một số mạch Domino tốc độ cao có thể bỏ Foot (footless) ở tầng sau nhưng dễ gặp chia sẻ điện tích hơn. |
| **Mạng PDN (chỉ dùng NMOS)** | Chỉ cần $N$ NMOS cho hàm $N$ ngõ vào; mỗi chân chỉ lái $1$ NMOS ($C_{in} = 4\lambda$ ở OR4 vs $52\lambda$ ở Static OR4), giúp giảm tải cho tầng trước gấp nhiều lần. |
| **Inverter đệm Low-skew ($16\lambda/8\lambda$)** | Chuyển cực tính thành $0 \to 1$ đơn điệu để ghép tầng Domino; tỉ số $W_p/W_n = 2 < 3$ hạ $V_M \approx 2,27\,\text{V}$ giúp tăng lề nhiễu mức cao $NM_H$ chống lật giả khi $X$ bị sụt nhẹ. |
| **Transistor Keeper $M_{kp}$ ($W \ge 3\lambda, L$ dài)** | Bù dòng rò dưới ngưỡng (subthreshold leakage) ở tần số thấp và giảm sụt áp Charge Sharing. Nếu Keeper quá lớn ($\ge 6-8\lambda$ với $L=2\lambda$), dòng tranh chấp sẽ thắng PDN và làm cổng kẹt ở mức 0. |

---

### 7.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. **Ưu thế thực sự của Dynamic/Domino CMOS nằm ở $\Sigma W$ và $C_{in}$, không phải chỉ ở số lượng transistor:** Domino OR4 có $9\text{T}$ (so với $10\text{T}$ của Static OR4 = NOR4+INV), nhưng tổng bề rộng giảm từ $224\lambda$ xuống $\mathbf{62-64\lambda}$ và điện dung mỗi ngõ vào $C_{in}$ giảm từ $52\lambda$ xuống **$4\lambda$** ($13\times$!).
2. **Điều kiện xảy ra Charge Sharing:** Cổng Domino OR4 có Foot NMOS **không thể** có chia sẻ điện tích trong pha Evaluate vì nút `n_eval` nối thẳng đất qua $M_{eval}$. Phải dùng mạch **2 NMOS nối tiếp** (tạo nút nội cô lập giữa `Mn_top` và `Mn_bot`).
3. **Đính chính Low-skew Inverter & Giới hạn công thức Charge Sharing:** Inverter đệm $16\lambda/8\lambda$ ($W_p/W_n = 2$) có $V_M \approx \mathbf{2,273\,\text{V}} < 2,45\,\text{V}$ nên là **Low-skew** (bản cũ gọi nhầm là High-skew và dùng $V_M=2,45\,\text{V}$). Công thức cân bằng $V_X' = V_{DD} \frac{C_X}{C_X + C_{int}}$ chỉ đúng khi $V_X' \le V_G - V_{thn} \approx 3,79\,\text{V}$ (C5N).
4. **Đánh đổi Keeper (Trade-off) & Luật hình học:** Không vẽ được layout với $W_{kp}=2\lambda$ (vi phạm bề rộng Active tối thiểu $3\lambda$ của SCMOS); thực tế dùng $W_{kp}=3\lambda - 4\lambda$ với $L_{kp}=4\lambda - 8\lambda$. Trong Ex7.3, bắt buộc đo **cả 2 đại lượng** ($t_{pd,eval}$ và $V_{X,min}$) để thấy sự đánh đổi.

---

### 7.2 Phân tích Vật lý Chi tiết (Theo `verify_lab07_new.py`)

#### a. Ngưỡng chuyển mạch $V_M$ của Inverter $16\lambda/8\lambda$
$$r = \sqrt{\frac{K'_p (W_p/L_p)}{K'_n (W_n/L_n)}} = \sqrt{\frac{40 \cdot 8}{120 \cdot 4}} = \sqrt{0,6667} = 0,8165$$
$$V_M = \frac{V_{tn0} + r(V_{DD} - |V_{tp0}|)}{1 + r} = \frac{0,70 + 0,8165 \cdot (5,0 - 0,80)}{1 + 0,8165} = \mathbf{2,273\,\text{V}}$$
- Với bài toán Pre-lab ($C_X = 20\,\text{fF}, C_{int} = 14\,\text{fF}$):
  $$V_X' = 5,0 \cdot \frac{20}{20 + 14} = \mathbf{2,941\,\text{V}}, \quad \Delta V_X = \mathbf{2,059\,\text{V}}$$
  $$NM_H = 2,941 - 2,273 = \mathbf{0,668\,\text{V}}$$
  Điều kiện lật giả ($V_X' \le 2,273\,\text{V}$): $C_{int} \ge \mathbf{1,20 \cdot C_X}$.

#### b. Giới hạn vật lý của Transistor trên (`Mn_top`)
Do `Mn_top` nạp $C_{int}$ theo kiểu source-follower, nó tự ngắt khi $V_{int} = V_{DD} - V_{thn}(V_{int}) \approx 3,787\,\text{V}$ (C5N).
- Công thức cân bằng hoàn toàn chỉ đúng khi $\frac{C_{int}}{C_X + C_{int}} \ge \frac{5,0 - 3,787}{5,0} = \mathbf{0,243}$ (hoặc $0,27$ với $\gamma=0,53$).
- Ở bài Pre-lab ($\frac{14}{34} = 0,412 \ge 0,243$), công thức cân bằng hoàn toàn hợp lệ.
- Ngược lại, nếu $C_{int}/C_X = 0,1$ ($C_{int}=2\,\text{fF}, C_X=20\,\text{fF}$), công thức cân bằng cho $\Delta V = 0,455\,\text{V}$, nhưng giới hạn vật lý cho $\Delta V \le 3,79 \cdot 0,1 = \mathbf{0,379\,\text{V}}$.

#### c. Tỉ số dòng Keeper / PDN đơn ở $V_X = 2,5\,\text{V}$
- Một nhánh PDN đơn ($4\lambda$ nối tiếp foot $8\lambda$, $R_{eq} \approx 969 + 485 = 1\,454\,\Omega$) có dòng xấp xỉ $I_{PDN} \approx \frac{2,5}{1454} \approx \mathbf{1,72\,\text{mA}}$.
- Keeper PMOS ($L=2\lambda$, ở $V_G=0, V_{SD}=2,5\text{V}$):
  * $W_{kp} = 2\lambda$: $I_{kp} \approx 0,30\,\text{mA}$ (17% $I_{PDN}$)
  * $W_{kp} = 4\lambda$: $I_{kp} \approx 0,59\,\text{mA}$ (34% $I_{PDN}$)
  * $W_{kp} = 6\lambda$: $I_{kp} \approx 0,89\,\text{mA}$ (51% $I_{PDN}$)
  * $W_{kp} = 8\lambda$: $I_{kp} \approx 1,18\,\text{mA}$ (69% $I_{PDN}$ $\implies$ nguy cơ cao PDN không thắng nổi Keeper, `.meas` báo `FAILED`!).

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN

### 7.3 Kế hoạch Buổi học 135 Phút & Điều phối Phòng máy
- **00–10':** Cổng kiểm tra Pre-lab. Rà nhanh $V_M = 2,27\,\text{V}$ và sơ đồ mạch thử 2-NMOS.
- **10–35' (Ex7.1):** Sinh viên chạy mạch thử 2-NMOS nối tiếp trên LTspice (dùng khung từ Handout, không trỏ vào thư mục `03 - Instructor_Solutions`). Kiểm tra độ sụt áp trên `x_nokp` vs `x_kp`.
- **35–55' (Ex7.2):** Dựng nhanh `domino_or4_x1{sch}` ($9\text{T}$, nhớ nối `clk` vào cả $M_{pre}$ và $M_{eval}$) và chạy kiểm tra 6 tổ hợp.
- **55–85' (Ex7.3):** Quét `.step param Wkp LIST 0.6u 1.2u 1.8u 2.4u` đo đồng thời $t_{pd,eval}$ và $V_{X,min}$. Hướng dẫn sinh viên cách xử lý nếu ở `2.4u` lệnh `.meas` báo `FAILED`.
- **85–105' (Ex7.4):** Mô phỏng 2 cổng Dynamic nối trực tiếp vs có Inverter đệm (Domino) để chứng kiến lỗi xả sớm ở `X2`.
- **105–125' (Ex7.5):** Chạy so sánh PPA giữa Domino OR4 và Static OR4 (`NOR4 + INV`) dùng `.meas INTEG`.
- **125–135':** Tổng kết và nghiệm thu tại bàn.

---

### 7.4 Đáp án Chi tiết Pre-lab & Bảng Đối Chuẩn

1. **Pre-lab Câu 1:** $V_M = 2,273\,\text{V}$ (Low-skew); $V_X' = 2,941\,\text{V}$; $\Delta V_X = 2,059\,\text{V}$; $NM_H = 0,668\,\text{V}$; $C_{int} \ge 1,20\,C_X$; với $C_{int}/C_X=0,1$: công thức cho $0,455\,\text{V}$, thực tế giới hạn $\le 0,379\,\text{V}$.
2. **Pre-lab Câu 2:** Khi không có Inverter, trong pha Precharge $X_1 = 5\,\text{V}$ làm PDN của cổng Dynamic 2 bật sẵn; sang pha Evaluate cả 2 cổng xả cùng lúc, cổng 2 bị xả mất điện tích của `X2` trước khi `X1` kịp xuống dưới $V_{thn}$.
3. **Pre-lab Câu 3 & 4:** Như khung Netlist trong `Ex7.1` và bảng tỉ số dòng Mục 7.2c ($0,17; 0,34; 0,51; 0,69$).

**Bảng Đối chuẩn Kỹ thuật Tham chiếu (MOSIS C5N):**

| Hạng mục | Giá trị kỳ vọng | Ghi chú |
| :--- | :---: | :--- |
| $V_M$ (Inverter $16\lambda/8\lambda$) | $2,27\,\text{V}$ | Low-skew |
| $V_{X,min}$ (Ex7.1, không Keeper) | $\approx 2,85 - 3,05\,\text{V}$ | Tụ $C_X=20\text{fF}, C_{int}=14\text{fF}$ |
| Domino OR4: $\Sigma W$ / $C_{in}$ | $62 - 64\lambda$ / $4\lambda$ | $9\text{T}$ |
| Static OR4: $\Sigma W$ / $C_{in}$ | $224\lambda$ / $52\lambda$ | $10\text{T}$ (`NOR4 + INV`) |

---

### 7.5 Kịch bản Gỡ lỗi Socratic cho Giảng viên

1. **Sinh viên báo: *"Thầy ơi, ở `Wkp = 2.4u` ($8\lambda$), lệnh `.meas t_pd_eval` của em bị `FAILED` luôn rồi!"***
   - *Gợi ý Socratic:* "Em mở dạng sóng `V(x)` và `V(y)` tại lần chạy thứ 4 đó lên xem! Nút `V(x)` có kéo xuống được dưới ngưỡng $2,27\,\text{V}$ không, hay bị Keeper PMOS ghìm ở trên cao?" $\implies$ Sinh viên hiểu giới hạn tranh chấp của Keeper.
2. **Sinh viên thắc mắc: *"Em thử chạy Charge Sharing trên cổng Domino OR4 trong Ex7.2 mà chẳng thấy nút `x` bị sụt áp gì cả!"***
   - *Gợi ý Socratic:* "Trong mạch OR4 có 4 NMOS mắc song song xuống nút `n_eval`, còn dưới `n_eval` là `M_eval` nối đất. Khi vào pha Evaluate ($CLK = 5\,\text{V}$), điện áp của `n_eval` bằng mấy? Có còn nút nội nào bị cô lập để tích điện hay chia sẻ điện tích không?" $\implies$ Sinh viên nhận ra điều kiện cần của Charge Sharing là nút nội cô lập giữa 2 transistor nối tiếp.

---

### 7.6 Đáp án 3 Câu hỏi Thảo luận Post-lab
1. **OR4 không có Charge Sharing ở Evaluate:** Vì 4 NMOS mắc song song nối xuống `n_eval`, khi `M_eval` mở thì `n_eval` nối đất, không tồn tại nút nội cô lập như mạch xếp chồng nối tiếp 2 NMOS.
2. **Low-skew Inverter ($16\lambda/8\lambda$):** Vì tỉ số $W_p/W_n = 2 < 3$, nên NMOS tương đối mạnh hơn PMOS, kéo ngưỡng $V_M$ xuống $2,27\,\text{V}$ (thấp hơn $2,45\,\text{V}$), giúp tăng lề nhiễu mức cao $NM_H = V_X' - V_M$ chống lật giả khi $X$ bị sụt áp nhẹ.
3. **Thiết kế Keeper hợp lệ DRC:** Giữ bề rộng Active tối thiểu $W_{kp} = 3\lambda$ hoặc $4\lambda$ và tăng chiều dài kênh **$L_{kp} = 4\lambda - 8\lambda$** để làm yếu dòng Keeper mà không vi phạm DRC.

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & BỘ CÂU HỎI VẤN ĐÁP TẠI BÀN

### 7.7 Barem chấm điểm nhanh tại bàn (Thang 10)
- **Pre-lab (2,0 điểm):** Tính đúng $V_M = 2,27\,\text{V}$, $V_X' = 2,94\,\text{V}$, $NM_H = 0,67\,\text{V}$, viết Netlist 2-NMOS và tỉ số dòng Keeper.
- **Ex7.1–7.2 (2,5 điểm):** Đo đúng $V_{X,min}$ có/không Keeper trên 2-NMOS; dựng đúng `domino_or4_x1` ($9\text{T}$) và kiểm chứng 6/6 tổ hợp.
- **Ex7.3 (2,5 điểm):** Quét đủ 4 mức Keeper, vẽ cả 2 đường ($t_{pd,eval}$ và $V_{X,min}$), giải thích được lỗi `.meas` ở $8\lambda$.
- **Ex7.4–7.5 (2,0 điểm):** Chứng minh lỗi xả sớm Dynamic trực tiếp vs Domino; đo đủ bảng đối sánh PPA với Static OR4.
- **Báo cáo & Vấn đáp (1,0 điểm):** Đầy đủ số liệu và trả lời đúng vấn đáp.

### 7.8 Bộ câu hỏi vấn đáp nhanh tại bàn (3 câu chọn lọc)
1. *"Tại sao nếu đặt Keeper PMOS bằng kích thước Inverter chuẩn ($W_{kp}=12\lambda, L=2\lambda$) thì cổng Domino OR4 gần như chắc chắn bị chết cứng ở mức 0?"* (Đáp: Dòng kéo lên của PMOS $12\lambda$ tương đương dòng kéo xuống của 1 nhánh NMOS $4\lambda$, nên PDN không kéo nổi $X$ qua ngưỡng $V_M$).
2. *"Tại sao ở pha Evaluate của Domino Logic, ngõ vào $A$ không được phép chuyển từ $1 \to 0$ giữa chừng?"* (Đáp: Vì nếu $A=1$ lúc đầu thì nút $X$ đã bị xả về $0\,\text{V}$; sau đó dù $A$ về $0$ thì $M_{pre}$ đang tắt nên $X$ không thể tự nạp lại lên $5\,\text{V}$ cho đến pha Precharge kế tiếp).
3. *"Vì sao một cổng Domino OR4 chỉ cần tải đầu vào $C_{in} = 4\lambda$ trên mỗi chân, nhỏ hơn $13$ lần so với cổng Static OR4 ($52\lambda$)?"* (Đáp: Vì mỗi ngõ vào của Domino chỉ lái đúng $1$ NMOS $4\lambda$, trong khi Static OR4 gồm NOR4 phải dùng thêm $4$ PMOS mắc nối tiếp kích thước lớn $48\lambda$ ở mỗi chân).
