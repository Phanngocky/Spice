# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 05 — TEACHER'S BOOK: MẠCH TUẦN TỰ MỨC TRANSISTOR: D-LATCH VÀ D-FLIP-FLOP MASTER-SLAVE
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-05-mach-tuan-tu-latch-va-flipflop.md](../02%20-%20Student%20Workbook/lab-05-mach-tuan-tu-latch-va-flipflop.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab05/](../03%20-%20Instructor_Solutions/lab05/)  
> **Script kiểm chứng số liệu:** [verify_lab05_new.py](../scripts/verify_lab05_new.py)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

### 5.0 Khái niệm chung, Định nghĩa chuẩn & Vai trò các tầng/tham số trong thực tế
*(Phần trình bày nhanh trên bảng 5–7 phút trước khi vào bài)*

1. **Khái niệm chung:**
   - **Mạch tuần tự (Sequential Logic):** Khác với mạch tổ hợp (ngõ ra chỉ phụ thuộc ngõ vào hiện tại), mạch tuần tự có khả năng lưu giữ trạng thái quá khứ nhờ vòng phản hồi dương (Cross-coupled Inverters).
   - **D-Latch vs D-Flip-Flop (DFF):** D-Latch nhạy theo mức xung nhịp (trong suốt khi `CLK=1`, chốt khi `CLK=0`), dễ bị nhiễu xuyên tầng (Race) nếu mắc nối tiếp. DFF Master-Slave ghép 2 D-Latch đối pha để chỉ lấy mẫu dữ liệu quanh sườn xung nhịp, làm phần tử nhớ chuẩn cho hệ thống số đồng bộ (thanh ghi, pipeline, ALU).
2. **Định nghĩa chuẩn:**
   - **$t_{setup}$ (Thời gian thiết lập):** Khoảng thời gian tối thiểu $D$ phải ổn định **trước** mốc $50\%$ sườn lên `CLK` (đo bằng quy ước đẩy trễ $10\%$ của $t_{c-q}$).
   - **$t_{hold}$ (Thời gian giữ):** Khoảng thời gian tối thiểu $D$ phải giữ nguyên **sau** mốc $50\%$ sườn lên `CLK` để dữ liệu mới không ghi đè làm hỏng trạng thái vừa chốt (điều kiện nhị phân).
   - **$t_{c-q}$ (Clock-to-Q Delay):** Độ trễ từ mốc $50\%$ sườn lên `CLK` đến mốc $50\%$ ngõ ra $Q$ ổn định.
   - **Metastability:** Trạng thái cân bằng không bền quanh $V_M \approx V_{DD}/2$ khi vi phạm cửa sổ setup/hold, đòi hỏi thời gian giải quyết kéo dài theo hàm mũ.
3. **Vai trò từng tầng mạch & tham số trong thực tế:**

| Tầng / Tham số | Vai trò trong mạch & Ý nghĩa thực tế khi thiết kế chip |
| :--- | :--- |
| **Khóa $TG_1, TG_2$ trong Latch** | $TG_1$ nạp $D$ vào nút $X$; $TG_2$ đóng vòng phản hồi khi chốt. Vì $TG_1$ và $TG_2$ mở đối pha, $I_3$ được cách ly nên chỉ cần cỡ tối thiểu ($4\lambda/2\lambda$) để giữ rò, không tranh chấp với $TG_1$. |
| **Tầng Master & Slave** | Master đón $D$ lúc `CLK=0` và khóa lúc `CLK` lên; Slave mở lúc `CLK=1` đẩy $Q_M$ ra $Q$. Giúp cô lập ngõ vào với ngõ ra trong phần lớn chu kỳ. |
| **Bộ đảo xung nhịp `X_CLK_INV`** | Tạo `clk_n` bị trễ $\approx t_{pd,inv}$ so với `clk`. Khoảng trễ này khiến $TG_{M1}$ đóng chậm một chút sau sườn lên `CLK`, chính là nguyên nhân vật lý sinh ra $t_{hold} > 0$. |
| **Cặp đệm ngõ ra $I_{S1}, I_{S2}$** | $I_{S1}$ tạo $\bar{Q}$ trong vòng chốt, $I_{S2}$ đệm ra $Q$ cách ly tụ tải ngoài $C_L$ khỏi vòng nhớ (tránh nhiễu tải ngoài làm lật Slave) và nằm trực tiếp trên đường $t_{c-q}$. |
| **Ràng buộc $T_{clk} \ge t_{c-q} + t_{comb} + t_{setup} + t_{skew}$** | Quyết định tần số xung nhịp cực đại $f_{max}$ của toàn bộ chip; vi phạm $t_{setup}$ có thể sửa bằng giảm tần số $f_{clk}$, nhưng vi phạm $t_{hold}$ sẽ làm chip hỏng ở mọi tần số! |

---

### 5.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. **Phân biệt rạch ròi Latch (nhạy mức) và Flip-Flop (nhạy sườn)** và hiểu rõ tại sao D-Latch có khóa cách ly $TG_2$ lại **không** cần Inverter $I_3$ phải "yếu" để chống tranh chấp như mạch chốt không có $TG_2$.
2. **Hiểu nguồn gốc vật lý của $t_{hold}$ và Race condition:** Cấu trúc Master-Slave chỉ giảm thiểu race khi $\overline{CLK}$ bám sát $CLK$. Độ trễ qua `X_CLK_INV` ($\approx t_{pd,inv}$) tạo ra khoảng chồng dẫn ngắn khi Master chưa kịp khóa hoàn toàn mà Slave đã mở $\implies$ sinh ra yêu cầu $t_{hold}$.
3. **Làm chủ phương pháp đo định thời chuẩn xác:** Khởi tạo `.ic`, phân biệt quy ước 10% push-out (cho $t_{setup}$) với ngưỡng nhị phân (cho $t_{hold}$), và nhận diện được hiện tượng Metastability.
4. **Nắm vững phương trình ràng buộc đồng bộ thực tế:** $T_{clk} \ge t_{c-q} + t_{comb,max} + t_{setup} + t_{skew}$.

---

### 5.2 Phân tích Cấu trúc D-Latch & Định cỡ Inverter Phản hồi $I_3$

**Đính chính quan trọng từ Audit Lab 5:**
- **Kiến trúc A (Có $TG_2$ — Chuẩn trong Hình 5.1 và `dlatch_tran.sp`):** Vì $TG_1$ (`en=clk, en_n=clk_n`) và $TG_2$ (`en=clk_n, en_n=clk`) nhận xung nhịp đối pha nên ở trạng thái xác lập chúng **không bao giờ dẫn cùng lúc**. Do đó $I_3$ không hề tranh chấp với $TG_1$ khi ghi dữ liệu; $I_3$ có thể dùng kích thước nhỏ nhất ($W=4\lambda, L=2\lambda$) chỉ để giữ nút $X$ trước dòng rò.
- **Kiến trúc B (Bỏ $TG_2$ — Mạch chốt kiểu Weak Feedback):** Nếu bỏ $TG_2$, $TG_1$ ($R_{TG} \approx 1,19\,\text{k}\Omega$) phải thắng được $I_3$ để lật nút $X$ qua ngưỡng $V_M \approx 2,45\,\text{V}$ của $I_1$. Theo tính toán từ `verify_lab05_new.py`:
  * Nếu $I_3$ có $W = 4\lambda, L = 2\lambda$ ($R_n = 969\,\Omega, R_p = 2\,976\,\Omega$): khi $TG_1$ ghi '1' đè lên '0', cầu phân áp cho $V_X = 5,0 \cdot \frac{969}{969+1190} = \mathbf{2,244\,\text{V}} < 2,45\,\text{V} \implies$ **THẤT BẠI, không đủ yếu!**
  * Nếu $I_3$ tăng $L = 4\lambda$ ($R_n = 1\,938\,\Omega, R_p = 5\,952\,\Omega$): ghi '1' đạt $V_X = \mathbf{3,098\,\text{V}} > 2,45\,\text{V}$ (ĐẠT), ghi '0' đạt $V_X = \mathbf{0,833\,\text{V}} < 2,45\,\text{V}$ (ĐẠT).

---

### 5.3 Dẫn xuất Đường trễ và các Thông số Định thời

Sử dụng bộ số liệu minh họa từ Lab 1 & Lab 4 ($t_{pd,inv} \approx 34\,\text{ps}, t_{pd,tg} \approx 42\,\text{ps}$ — giảng viên lưu ý sinh viên dùng số đo thực tế của chính họ):

| Đại lượng | Đường truyền & Công thức đầy đủ | Giá trị suy dẫn | Ghi chú đính chính |
| :--- | :--- | :---: | :--- |
| $t_{pd(D \to Q)}$ (Latch) | $TG_1 + I_1 + I_2$ | $\approx 110\,\text{ps}$ | Pha trong suốt |
| $t_{c-q}$ (DFF) | `X_CLK_INV` $+ TG_{S1} + I_{S1} + I_{S2}$ | $\mathbf{144\,\text{ps}}$ | Bản cũ ghi thiếu $I_2$ nên ra nhầm $110\,\text{ps}$! |
| $t_{setup}$ (DFF) | $TG_{M1} + I_{M1}$ | $\approx 76\,\text{ps}$ | Đo thực nghiệm theo quy ước 10% push-out |
| $t_{hold}$ (DFF) | Độ trễ đảo xung nhịp `X_CLK_INV` | $\approx \mathbf{34\,\text{ps}}$ | Đo thực nghiệm bằng quét ngưỡng nhị phân |
| $T_{min,no-logic}$ | $t_{c-q} + t_{setup}$ | $\approx \mathbf{220\,\text{ps}}$ | Tương ứng $1/T_{min} \approx 4,55\,\text{GHz}$ (chỉ là giới hạn không logic tổ hợp, không phải $f_{max}$ an toàn) |

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN

### 5.4 Kế hoạch Buổi học 135 Phút & Điều phối Phòng máy
- **00–10':** Cổng kiểm tra Pre-lab. Kiểm tra sinh viên tự điền bảng chân trị, hiểu cách tính chia áp cho $I_3$ và biết đưa $I_2$ vào đường $t_{c-q}$.
- **10–25' (Ex5.1):** Dựng `dlatch_x1{sch}` ($10\text{T}$). Nhắc sinh viên dùng `tg_gate` dựng sẵn (nếu lớp chưa học Lab 4) và kiểm tra kỹ bảng ánh xạ `clk`/`clk_n` của `TG1` và `TG2`.
- **25–45' (Ex5.2):** Mô phỏng Latch với `.tran 0 160n 0 1p`. Chú ý chỉ sinh viên chọn sườn $D$ nằm trong khoảng `clk = 5V` khi dùng `.meas` đo $t_{pd(D \to Q)}$.
- **45–60' (Ex5.3):** Dựng phân cấp `dff_ms_x1{sch}` ($22\text{T}$). Nhấn mạnh `X_CLK_INV` (`inv_x1`) đang phải lái đồng thời cả `X_MASTER.clk` và `X_SLAVE.clk_n`.
- **60–115' (Ex5.4 — Trọng tâm 55 phút):**
  * Hướng dẫn `.ic V(q)=0` để tránh `.meas t_cq` bị lỗi do điểm làm việc DC `.op`.
  * Giải thích rõ định nghĩa $\Delta t$ giữa hai mốc $50\%$–$50\%$, quét cả $D$ lên và $D$ xuống, loại bỏ các điểm bị trượt chu kỳ khỏi đồ thị push-out.
  * Cho chạy quét `dt_h` từ `-50p` đến `+100p` (step `5p`) với `.meas FIND v(q) AT=25n` để xác định ngưỡng $t_{hold}$.
  * Dành 10 phút cho sinh viên phóng to 1 ca sát biên giới để quan sát trực quan Metastability.
- **115–135':** Phân tích tập thể và nghiệm thu tại bàn.

---

### 5.5 Đáp án Chi tiết Pre-lab

1. **Bảng chân trị Master-Slave DFF:**

| $CLK$ | $D$ | Master Latch | Slave Latch | $Q_{next}$ | Chế độ hoạt động |
| :---: | :---: | :---: | :---: | :---: | :--- |
| 0 | 0 | Trong suốt ($Q_M = 0$) | Chốt giữ ($Q = Q_{prev}$) | $Q_{prev}$ | Master nạp '0', Slave giữ |
| 0 | 1 | Trong suốt ($Q_M = 1$) | Chốt giữ ($Q = Q_{prev}$) | $Q_{prev}$ | Master nạp '1', Slave giữ |
| 1 | X | Chốt giữ ($Q_M$ khóa) | Trong suốt ($Q = Q_M$) | $Q_M$ | Master cách ly, Slave xuất |
| $\uparrow$ | 0 | Chuyển sang chốt | Chuyển sang mở | **0** | Lấy mẫu sườn dương ('0') |
| $\uparrow$ | 1 | Chuyển sang chốt | Chuyển sang mở | **1** | Lấy mẫu sườn dương ('1') |

2. **Ước lượng định thời (với $t_{pd,inv} \approx 34\,\text{ps}, t_{pd,tg} \approx 42\,\text{ps}$):**
   - $t_{pd(D\to Q)} \approx 110\,\text{ps}$; $t_{c-q} \approx 144\,\text{ps}$; $t_{setup} \approx 76\,\text{ps}$; $t_{hold} \approx 34\,\text{ps}$; $T_{min,no-logic} \approx 220\,\text{ps}$.

3. **Bài toán chia áp $I_3$ (nếu bỏ $TG_2$):**
   - $W=4\lambda, L=2\lambda$: $R_n = 969\,\Omega \implies V_X = 5,0 \cdot \frac{969}{969+1190} = \mathbf{2,244\,\text{V}} < V_M \approx 2,45\,\text{V} \implies$ **Không đạt**.
   - $W=4\lambda, L=4\lambda$: $R_n = 1\,938\,\Omega \implies V_X = 5,0 \cdot \frac{1938}{1938+1190} = \mathbf{3,098\,\text{V}} > 2,45\,\text{V} \implies$ **Đạt**.

4. **Thay `X_CLK_INV` bằng `inv_x2`:**
   - Vì `inv_x2` có dòng lái gấp đôi, độ trễ tạo tín hiệu `clk_n` giảm đi $\implies$ NMOS của $TG_{M1}$ đóng nhanh hơn sau sườn lên $CLK$ $\implies$ **$t_{hold}$ sẽ giảm xuống**!

---

### 5.6 Bảng Đối Chuẩn Kỹ Thuật Tham Chiếu (MOSIS C5N, $C_L = 50\,\text{fF}$)

| Hạng mục đo kiểm | Giá trị kỳ vọng (Suy dẫn / Tham chiếu) | Ghi chú |
| :--- | :---: | :--- |
| D-Latch $t_{pd(D \to Q)}$ | $\approx 100 - 125\,\text{ps}$ | Pha trong suốt (`clk = 5V`) |
| Mức chốt Latch $V_{Q,high} / V_{Q,low}$ | $5,00\,\text{V} / 0,00\,\text{V}$ ($\pm 20\,\text{mV}$) | Trong pha chốt (`clk = 0V`) |
| DFF $t_{c-q,nominal}$ (LH / HL) | $\approx 130 - 160\,\text{ps}$ | Đầy đủ qua $I_{S1}, I_{S2}$ |
| DFF $t_{setup}$ (10% push-out) | $\approx 70 - 100\,\text{ps}$ | Có thể khác nhẹ giữa LH và HL |
| DFF $t_{hold}$ (`inv_x1`) | $\approx +15 \text{ đến } +45\,\text{ps}$ | Giảm khi đổi sang `inv_x2` |

---

### 5.7 Kịch bản Gỡ lỗi Socratic cho Giảng viên (4 tình huống điển hình)

1. **Sinh viên báo: *"Thầy ơi, em chạy `.meas t_cq_lh` mà LTspice toàn báo `Measurement FAILED` dù mạch em nối đúng 100%!"***
   - *Gợi ý Socratic:* "Em hãy vẽ đồ thị $V(q)$ từ $t=0$. Trước sườn lên đầu tiên của $CLK$, $V(q)$ đang ở mức $0\,\text{V}$ hay $5\,\text{V}$? Nếu phần mềm giải điểm DC ban đầu `.op` đẩy $Q$ lên sẵn $5\,\text{V}$ rồi thì có sườn lên `RISE` nào xảy ra nữa không?" $\implies$ Sinh viên tự biết thêm `.ic V(q)=0`.

2. **Sinh viên thắc mắc: *"Khi em quét `dt` xuống dưới $50\,\text{ps}$, $t_{c-q}$ của em nhảy vọt từ $150\,\text{ps}$ lên hẳn $20\,150\,\text{ps}$!"***
   - *Gợi ý Socratic:* "Chu kỳ xung nhịp `CLK` của em là bao nhiêu `ns` ($20\,\text{ns} = 20\,000\,\text{ps}$)? Vậy ở lần quét đó dữ liệu $D$ có kịp được bắt ở sườn này không, hay `.meas` đã chạy sang bắt sườn của chu kỳ sau?" $\implies$ Sinh viên hiểu giới hạn vùng hợp lệ khi vẽ đường cong push-out.

3. **Sinh viên hỏi: *"Tại sao khi em giữ $D$ đổi ngay tại $t = 20,02\,\text{ns}$ (tức $20\,\text{ps}$ sau sườn lên `CLK`), ngõ ra $Q$ lại bị lật theo dữ liệu mới?"***
   - *Gợi ý Socratic:* "Em hãy vẽ chồng $V(clk)$ và $V(clk\_n)$ quanh $t = 20\,\text{ns}$. Ở thời điểm $20,02\,\text{ns}$, tín hiệu `clk_n` đã tụt xuống $0\,\text{V}$ để khóa NMOS của Master Latch chưa?" $\implies$ Sinh viên hiểu bản chất vật lý của $t_{hold}$.

4. **Sinh viên hỏi: *"Trong `dlatch_x1`, thầy bảo dùng $I_3$ kích thước $4\lambda/2\lambda$, vậy có bị xung đột dòng với $TG_1$ như sách hay nói không?"***
   - *Gợi ý Socratic:* "Em nhìn lại sơ đồ Hình 5.1 xem giữa ngõ ra $I_3$ và nút $X$ có thêm linh kiện gì? Khi `clk = 1` để $TG_1$ ghi dữ liệu thì công tắc $TG_2$ đang mở hay đóng?" $\implies$ Sinh viên tự nhận ra vai trò cách ly của $TG_2$.

---

### 5.8 Đáp án Chi tiết Câu hỏi Thảo luận Post-lab

1. **Câu 1 (Metastability & Synchronizer):**
   - Khi vi phạm $t_{setup}$/$t_{hold}$, nút lưu trữ $Q_M$ không kịp đạt 0 hay $V_{DD}$ mà dừng gần điểm cân bằng không bền $V_M \approx V_{DD}/2$. Vòng phản hồi khuếch đại độ lệch $\Delta V_0$ theo hàm mũ $V(t) - V_M = \Delta V_0 e^{t/\tau_{reg}}$, khiến thời gian giải quyết $t_{resolve} = \tau_{reg} \ln(V_{DD}/\Delta V_0)$ có thể rất lớn nếu $\Delta V_0 \to 0$.
   - *Cách xử lý:* Dùng **Bộ đồng bộ hóa 2 tầng Flip-Flop (2-FF Synchronizer)** mắc nối tiếp để cho phép tầng FF đầu tiên có trọn một chu kỳ xung nhịp $T_{clk}$ để tự giải quyết metastability trước khi tầng FF thứ 2 lấy mẫu.
2. **Câu 2 (Ảnh hưởng của `inv_x2` lên $t_{hold}$):**
   - `inv_x2` giảm trễ $t_{pd,INV(CLK)}$ giữa `clk` và `clk_n`, giúp cổng truyền $TG_{M1}$ của Master ngắt nhanh hơn sau sườn lên `clk` $\implies$ giảm khoảng chồng dẫn $\implies$ $t_{hold}$ giảm xuống.
3. **Câu 3 (TSPC DFF vs TG-DFF):**
   - TSPC (True Single-Phase Clock) chỉ dùng duy nhất một pha xung nhịp `clk` (không cần `clk_n`, tiết kiệm Inverter và giảm tải/lệch pha xung nhịp, số transistor ít hơn $\approx 9-11\text{T}$), đạt tốc độ rất cao; nhược điểm là mạch động (dynamic) nhạy với nhiễu, chia sẻ điện tích và không hoạt động được ở tần số thấp/DC nếu không thêm mạch giữ tĩnh. Ngược lại, TG-DFF hoàn toàn tĩnh (static), giữ dữ liệu vô thời hạn khi dừng xung nhịp và ít nhạy nhiễu hơn.

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & BỘ CÂU HỎI VẤN ĐÁP TẠI BÀN

### 5.9 Barem chấm điểm nhanh tại bàn (Thang 10)
- **Pre-lab (2,0 điểm):** Điền đúng bảng chân trị, dùng đúng công thức $t_{c-q}$ đủ $I_1, I_2$, tính đúng bài toán chia áp $I_3$.
- **Ex5.1–5.2 (2,0 điểm):** Schematic `dlatch_x1` ($10\text{T}$) 0 lỗi; chứng minh pha trong suốt, pha chốt giữ và đo đúng $t_{pd(D\to Q)}$.
- **Ex5.3–5.4a (2,0 điểm):** Schematic `dff_ms_x1` ($22\text{T}$) 0 lỗi; khởi tạo `.ic` và đo đủ $t_{c-q,LH}, t_{c-q,HL}$.
- **Ex5.4b (2,5 điểm):** Quét $t_{setup}$ (cả 2 sườn $D$, 10% push-out), quét $t_{hold}$ (bước $5\,\text{ps}$, `.meas FIND`) và có ảnh Metastability.
- **Post-lab & Báo cáo (1,5 điểm):** Thí nghiệm `inv_x2` với $t_{hold}$, tính $T_{min}$ và trả lời đúng vấn đáp.

### 5.10 Bộ câu hỏi vấn đáp nhanh tại bàn (3 câu chọn lọc)
1. *"Nếu anh/chị quên câu lệnh `.ic V(q)=0` khi chạy mô phỏng đo $t_{c-q,LH}$, điều gì có thể xảy ra?"* (Đáp: Bộ giải `.op` có thể khởi tạo $Q = 5\,\text{V}$ sẵn nên không có sườn lên $0 \to 1$, làm `.meas` báo `FAILED` hoặc đo nhầm chu kỳ sau).
2. *"Vì sao trong bảng thông số định thời của DFF ta không tính sai lệch phần trăm (%) cho $t_{hold}$?"* (Đáp: Vì $t_{hold}$ có giá trị nhỏ, có thể bằng $0$ hoặc mang dấu âm tùy độ trễ đường dữ liệu so với đường clock, nên chia phần trăm sẽ vô nghĩa hoặc gây chia cho 0; phải dùng chênh lệch tuyệt đối tính bằng `ps`).
3. *"Nếu xung nhịp $CLK$ hoạt động ở tần số rất thấp ($1\,\text{kHz}$) hoặc bị tạm dừng (Clock Gating), mạch `dff_ms_x1` này có bị mất dữ liệu không?"* (Đáp: Không, vì đây là mạch tĩnh hoàn toàn nhờ vòng phản hồi kín $I_1-I_3-TG_2$ trong cả Master và Slave).
