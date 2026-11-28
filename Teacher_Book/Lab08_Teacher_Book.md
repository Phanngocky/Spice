# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 08 — TEACHER'S BOOK: Ô NHỚ SRAM 6T VÀ MẠCH KHUẾCH ĐẠI CẢM NHẬN (VLSA)
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-08-o-nho-sram-6t-va-sense-amplifier.md](../02%20-%20Student%20Workbook/lab-08-o-nho-sram-6t-va-sense-amplifier.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab08/](../03%20-%20Instructor_Solutions/lab08/)  
> **Script kiểm chứng số liệu:** [verify_lab08_new.py](../scripts/verify_lab08_new.py)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

### 8.0 Khái niệm chung, Định nghĩa chuẩn & Vai trò các tầng/tham số trong thực tế
*(Phần trình bày nhanh trên bảng 5–7 phút trước khi vào bài)*

1. **Khái niệm chung:**
   - **Ô nhớ tĩnh 6T SRAM (`sram_6t_cell`):** Phần tử lưu trữ 1-bit dùng cặp Inverter ghép chéo (giữ dữ liệu vô thời hạn khi còn nguồn, không cần làm tươi như DRAM) kết hợp 2 Access NMOS nối với cặp Bitline vi sai (`BL`, `BLB`). Chiếm phần lớn diện tích trong bộ nhớ đệm Cache L1/L2/L3 của vi xử lý.
   - **Mạch khuếch đại cảm nhận (VLSA - Voltage Latch Sense Amplifier):** Mạch khuếch đại vi sai dùng hồi tiếp dương để phát hiện độ lệch áp rất nhỏ trên Bitline ($\Delta V_{BL} \approx 100 - 200\,\text{mV}$) và chốt nhanh thành mức logic $0/V_{DD}$, tránh phải chờ ô nhớ xả toàn dải trên tụ Bitline lớn ($C_{BL} \approx 1\,\text{pF}$).
2. **Định nghĩa chuẩn:**
   - **Cell Ratio ($CR = \frac{(W/L)_{driver}}{(W/L)_{access}}$):** Tỉ số kích thước giữa Driver NMOS và Access NMOS, quyết định độ ổn định khi Đọc (chống Read Disturb).
   - **Pull-up Ratio ($PR = \frac{(W/L)_{load}}{(W/L)_{access}}$):** Tỉ số kích thước giữa Load PMOS và Access NMOS, quyết định khả năng Ghi đè (Writability).
   - **Static Noise Margin ($SNM$):** Độ lớn nhiễu DC tối đa mà cặp Inverter ghép chéo chịu được trước khi lật trạng thái; đo bằng cạnh hình vuông lớn nhất nội tiếp trong **thùy nhỏ hơn** của đường cong Butterfly.
3. **Vai trò từng tầng mạch & tham số trong thực tế:**

| Tầng / Tham số | Vai trò trong mạch & Ý nghĩa thực tế khi thiết kế chip |
| :--- | :--- |
| **Driver NMOS ($M_{D1}, M_{D2}$, $8\lambda$)** | Kéo giữ nút `'0'` xuống đất trong cả Hold và Read. Phải mạnh hơn Access ($CR \ge 1,5 - 2,0$) để điện áp dâng $V_Q$ khi đọc ($\approx 0,73 - 0,79\,\text{V}$) nằm an toàn dưới ngưỡng lật $V_M \approx 1,49\,\text{V}$ của Inverter đối diện. |
| **Access NMOS ($M_{AX1}, M_{AX2}$, $4\lambda$)** | Đóng mở cổng nối với `BL`/`BLB` theo tín hiệu hàng `WL`. Nằm ở giao điểm của hai mâu thuẫn: to quá thì hỏng Đọc, nhỏ quá thì không Ghi được! |
| **Load PMOS ($M_{L1}, M_{L2}$, $2\lambda$)** | Giữ nút `'1'` chống dòng rò lúc Hold; phải yếu hơn Access (nhờ $\mu_n \approx 3\mu_p$, $PR=0,5$ cho sức kéo Access/Load $= 6\times$) để khi ghi `'0'` kéo tụt được nút lưu trữ xuống $\approx 0,36\,\text{V} \ll V_M$. *(Layout thực tế dùng $W_L \ge 3\lambda$, tăng $L_L$)*. |
| **Cụm VLSA & Chân `saen`** | Khi `saen` bật lên $V_{DD}$, cặp Inverter ghép chéo khuếch đại vi sai $\pm 150\,\text{mV}$ thành $0/5\,\text{V}$ chỉ trong $\sim 70-200\,\text{ps}$, giúp tiết kiệm $>90$% năng lượng nạp xả `BL`/`BLB`. |

---

### 8.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. **Giải quyết triệt để mâu thuẫn công thức $V_Q$ khi đọc `'0'`:** Công thức xấp xỉ bậc nhất $\frac{V_{DD}-V_{tn}}{2\cdot CR}$ cho $1,075\,\text{V}$ ở $CR=2$ (lớn hơn $V_{tn}=0,70\,\text{V}$). Giải phương trình bậc hai chính xác cho $V_Q = \mathbf{0,789\,\text{V}}$ (không body effect) hoặc $\mathbf{0,725\,\text{V}}$ (có body effect trên Access NMOS). Tiêu chí vật lý đúng không phải $V_Q < V_{tn}$, mà là **$V_Q < V_M$ của Inverter đối diện** ($V_M \approx \mathbf{1,485\,\text{V}}$ với $8\lambda/2\lambda$).
2. **Hiểu đúng sức kéo khi ghi `'0'` (`PR`):** Dù $PR = 0,5$ theo tỉ số $W/L$, nhưng vì $K'_n / K'_p = 3$ nên tỉ số dòng thực tế giữa Access ($4\lambda$) và Load ($2\lambda$) là **$6\times$**, kéo nút $Q$ xuống cân bằng ở $\mathbf{0,357\,\text{V}} \ll V_M = 1,485\,\text{V}$.
3. **Nắm chính xác định nghĩa & giá trị $SNM$:** $SNM_{hold} \approx \mathbf{1,303\,\text{V}}$ (26,1% $V_{DD}$) và $SNM_{read} \approx \mathbf{0,359\,\text{V}}$ (7,2% $V_{DD}$, do $V_M$ dịch từ $1,485\,\text{V}$ lên $2,090\,\text{V}$), không phải $0,62\,\text{V}$ như bản cũ ghi nhầm.
4. **Tách bạch Đọc tĩnh ($V_Q$) vs Đọc động ($\Delta V_{BL}$) và đo đối sánh VLSA tường minh:** Phải gắn $C_{BL}=1\,\text{pF}$ thả nổi mới đo được $\Delta V_{BL}(t)$ và so sánh công bằng tốc độ/năng lượng giữa đọc có VLSA với đọc không VLSA (chờ Bitline xả xuống $V_{DD}/2$).

---

### 8.2 Bảng Đối chiếu $V_Q$ theo $CR$ (Theo `verify_lab08_new.py`)

| $CR = W_D / W_{AX}$ | $V_Q$ bậc hai (không body) | $V_Q$ bậc hai (có body trên Access) | Xấp xỉ bậc nhất $\frac{4,3}{2\cdot CR}$ | Đánh giá so với $V_M = 1,485\,\text{V}$ |
| :---: | :---: | :---: | :---: | :--- |
| 1,00 | $1,259\,\text{V}$ | $1,123\,\text{V}$ | $2,150\,\text{V}$ | Lề an toàn quá hẹp (nguy hiểm) |
| 1,50 | $0,969\,\text{V}$ | $0,880\,\text{V}$ | $1,433\,\text{V}$ | Bắt đầu đạt chuẩn |
| **2,00** | **$0,789\,\text{V}$** | **$0,725\,\text{V}$** | **$1,075\,\text{V}$** | **Chuẩn thiết kế ($< V_M$, dư biên)** |
| 2,50 | $0,666\,\text{V}$ | $0,618\,\text{V}$ | $0,860\,\text{V}$ | Rất ổn định |
| 3,00 | $0,576\,\text{V}$ | $0,539\,\text{V}$ | $0,717\,\text{V}$ | Đạt cả tiêu chí khắt khe $V_Q < V_{tn}$ |
| 3,07 | $0,565\,\text{V}$ | $0,530\,\text{V}$ | $0,700\,\text{V}$ | Biên lý thuyết của công thức bậc nhất |

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN

### 8.3 Kế hoạch Buổi học 135 Phút & Điều phối Phòng máy
- **00–10':** Cổng kiểm tra Pre-lab. Rà nhanh phép tính $V_Q$ ($0,725-0,789\,\text{V}$), $V_M$ ($1,485\,\text{V}$) và sức kéo ghi $6\times$.
- **10–40' (Ex8.1):** Hướng dẫn sinh viên vẽ 2 đường VTC lồng nhau trên LTspice bằng cách xoay trục $45^\circ$ ($u = (x-y)/\sqrt{2}, v = (x+y)/\sqrt{2}$) để đọc $SNM_{hold}$ và $SNM_{read}$ ở thùy nhỏ hơn.
- **40–65' (Ex8.2):** Yêu cầu sinh viên chạy tách bạch 3 ca: Đọc tĩnh (nguồn $5\text{V}$ cố định đo $V_Q$), Đọc động (tụ $C_{BL}=1\,\text{pF}$ thả nổi đo $\Delta V_{BL}$) và Ghi (có `.ic`).
- **65–100' (Ex8.3):** Dựng schematic `sense_amp_vlsa{sch}` theo thông số cụ thể (`Mp` $12\lambda$, `Mn` $8\lambda$, `Mn_tail` $12\lambda$, `Mn_pass` $4\lambda$) và đo $t_{latch}$ cho cả $\Delta V_{in} = +150\,\text{mV}$ và $-150\,\text{mV}$.
- **100–125' (Ex8.4):** So sánh trực tiếp đường đọc có VLSA vs đường đọc không VLSA (chờ xả $C_{BL}$ tới $2,5\,\text{V}$) và đo năng lượng `.meas INTEG`.
- **125–135':** Tổng kết và nghiệm thu tại bàn.

---

### 8.4 Đáp án Chi tiết Pre-lab & Bảng Đối Chuẩn

1. **Pre-lab Câu 1:** $CR = 2,0$. Công thức bậc hai cho $V_Q = \mathbf{0,789\,\text{V}}$ (không body) / $\mathbf{0,725\,\text{V}}$ (có body); xấp xỉ bậc nhất cho $1,075\,\text{V}$. Ngưỡng lật Inverter đối diện là $V_M = \mathbf{1,485\,\text{V}}$. Vì $V_Q \approx 0,73\,\text{V} \ll 1,485\,\text{V}$, ô nhớ hoàn toàn an toàn trước Read Disturb (dù $V_Q$ hơi nhỉnh hơn $V_{tn} = 0,70\,\text{V}$).
2. **Pre-lab Câu 2:** $PR = 0,5$ theo $W/L$. Có xét $\frac{K'_n}{K'_p} = 3$, tỉ số sức kéo Access/Load là $(120 \cdot 2)/(40 \cdot 1) = \mathbf{6,0\times}$. Nút $Q$ cân bằng khi ghi `'0'` ở $\mathbf{0,357\,\text{V}} \ll 1,485\,\text{V} \implies$ ghi thành công dễ dàng.
3. **Pre-lab Câu 4:** $t_{latch} \approx (25 \text{ đến } 50\,\text{ps}) \cdot \ln(4,5/0,15) \approx 3,4 \times (25 \text{ đến } 50\,\text{ps}) \approx \mathbf{85 - 170\,\text{ps}}$ (ước lượng thô $70 - 200\,\text{ps}$).

**Bảng Đối chuẩn Kỹ thuật Tham chiếu (MOSIS C5N):**

| Hạng mục | Giá trị suy dẫn / Tham chiếu | Ghi chú |
| :--- | :---: | :--- |
| $V_Q$ đọc `'0'` ($CR = 2,0$) | $0,725 - 0,789\,\text{V}$ | Phép thử đọc tĩnh (`bl=5V` cố định) |
| $SNM_{hold}$ / $SNM_{read}$ | $1,30\,\text{V}$ / $0,36\,\text{V}$ | Butterfly xoay $45^\circ$ (bài cũ ghi nhầm $0,62\,\text{V}$) |
| Tỉ số $SNM_{read} / SNM_{hold}$ | $\approx 0,276$ | |
| Mức $Q$ khi ghi `'0'` | $\approx 0,357\,\text{V}$ | Trước khi cặp chéo lật hẳn về 0 |
| VLSA $t_{latch}$ ($\pm 150\,\text{mV}$) | $\approx 70 - 200\,\text{ps}$ | $C_{so} = C_{sob} = 20\,\text{fF}$ |

---

### 8.5 Kịch bản Gỡ lỗi Socratic cho Giảng viên

1. **Sinh viên báo: *"Thầy ơi, trong Ex8.2 em đo $\Delta V_{BL}$ mà nó ra bằng đúng `0.000 V` luôn!"***
   - *Gợi ý Socratic:* "Trong testbench đó, chân `bl` của em đang nối vào nguồn áp DC `5.0V` hay nối vào tụ `C_bl = 1pF` thả nổi? Một nguồn áp lý tưởng có bao giờ bị sụt áp khi ô nhớ kéo dòng không?" $\implies$ Sinh viên hiểu sự khác biệt giữa Ca A (đọc tĩnh) và Ca B (đọc động).
2. **Sinh viên thắc mắc: *"Tại sao công thức $V_Q$ trong sách cho ra $1,075\,\text{V}$ lớn hơn $V_{tn} = 0,70\,\text{V}$, vậy là ô nhớ $CR=2$ của em bị lật đọc rồi sao thầy?"***
   - *Gợi ý Socratic:* "Công thức $1,075\,\text{V}$ đã bỏ qua số hạng $V_Q^2$ nên cho kết quả lớn hơn thực tế ($0,73-0,79\,\text{V}$). Hơn nữa, nút $Q$ đi vào cổng Inverter đối diện có PMOS rất yếu ($2\lambda$) và NMOS rất mạnh ($8\lambda$). Ngưỡng lật thực sự $V_M$ của Inverter đó bằng mấy volt?" $\implies$ Sinh viên nhận ra $V_M = 1,485\,\text{V}$ mới là ngưỡng lật thực sự.

---

### 8.6 Đáp án 3 Câu hỏi Thảo luận Post-lab
1. **Tiêu chí đọc ổn định:** Vì công thức bậc nhất ước lượng cao ($1,075\,\text{V}$ vs $0,73-0,79\,\text{V}$ thực tế) và tiêu chí vật lý chống lật đọc là $V_Q < V_M$ của Inverter đối diện ($1,485\,\text{V}$), không phải $V_{tn} = 0,70\,\text{V}$.
2. **Sức kéo ghi `'0'`:** Do độ linh động electron lớn gấp $3\times$ lỗ trống ($K'_n = 3 K'_p$), nên $PR = 0,5$ thực chất cho tỉ số sức kéo Access/Load tới $6\times$, kéo nút $Q$ xuống $0,357\,\text{V} \ll 1,485\,\text{V}$.
3. **Input Offset của VLSA:** Nếu $\Delta V_{os} = 100\,\text{mV} > \Delta V_{BL} = 80\,\text{mV}$ (ngược dấu), cặp Inverter ghép chéo sẽ khuếch đại nhầm theo hướng của sai lệch Offset và **xuất ra bit logic sai**! Do đó các mạch VLSA thực tế đòi hỏi kích thước lớn hơn hoặc mạch khử Offset.

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & BỘ CÂU HỎI VẤN ĐÁP TẠI BÀN

### 8.7 Barem chấm điểm nhanh tại bàn (Thang 10)
- **Pre-lab (2,0 điểm):** Giải đúng $V_Q$ bậc hai, $V_M = 1,485\,\text{V}$, sức kéo ghi $6\times$, $t_{latch}$ và Netlist 6T.
- **Ex8.1 (2,5 điểm):** Vẽ đúng Butterfly Hold/Read và đo đúng $SNM_{hold}, SNM_{read}$ bằng xoay trục $45^\circ$.
- **Ex8.2 (2,5 điểm):** Tách bạch và đo đúng đọc tĩnh ($V_Q$), đọc động ($\Delta V_{BL}$ trên $1\,\text{pF}$) và ghi ($t_{write}$).
- **Ex8.3–8.4 (2,0 điểm):** Dựng `sense_amp_vlsa`, đo $t_{latch}$ cả 2 chiều ($\pm 150\,\text{mV}$) và đối sánh đọc có/không VLSA.
- **Báo cáo & Vấn đáp (1,0 điểm):** Đầy đủ số liệu và trả lời đúng vấn đáp.

### 8.8 Bộ câu hỏi vấn đáp nhanh tại bàn (3 câu chọn lọc)
1. *"Nếu anh/chị tăng chiều rộng Access NMOS lên bằng Driver NMOS ($CR = 1,0$) để ghi nhanh hơn, hiện tượng gì xảy ra ở đường cong Butterfly chế độ Read?"* (Đáp: $V_Q$ dâng lên $\approx 1,12 - 1,26\,\text{V}$, hai thùy Butterfly ép sát lại làm $SNM_{read} \to 0$, ô nhớ mất dữ liệu ngay khi đọc).
2. *"Vì sao trong thiết kế layout SRAM 6T không nên dùng $W_L = 2\lambda$ nếu quy trình DRC yêu cầu Active tối thiểu $3\lambda$?"* (Đáp: Sẽ vi phạm DRC; phải tăng $W_L \ge 3\lambda$ và tăng chiều dài kênh $L_L$ tương ứng để giữ nguyên tỉ số $PR$ yếu cho phép ghi).
3. *"Khi đọc mảng nhớ $C_{BL} = 1\,\text{pF}$, năng lượng nạp lại Bitline tiết kiệm được bao nhiêu lần khi dùng VLSA kích ở $\Delta V_{BL}=150\,\text{mV}$ so với đọc thường xả $2,5\,\text{V}$?"* (Đáp: Năng lượng tỉ lệ thuận với $\Delta V_{BL}$, tiết kiệm $\frac{2,50 - 0,15}{2,50} = \mathbf{94\text{ pct}}$, tức giảm $\sim 16,7$ lần!).
