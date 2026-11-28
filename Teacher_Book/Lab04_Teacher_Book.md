# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 04 — TEACHER'S BOOK: CỔNG TRUYỀN (TRANSMISSION GATE) VÀ BỘ DỒN KÊNH MUX
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-04-transmission-gate-va-mux.md](../02%20-%20Student%20Workbook/lab-04-transmission-gate-va-mux.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab04/](../03%20-%20Instructor_Solutions/lab04/)  
> **Script kiểm chứng số liệu:** [verify_lab04_new.py](../scripts/verify_lab04_new.py)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

### 4.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. **Hiểu cặn kẽ giới hạn của Pass Transistor đơn lẻ:** NMOS truyền mức '1' kém (Weak '1') và PMOS truyền mức '0' kém (Weak '0'). **Điểm đính chính quan trọng:** cả hai đều chịu tác động của **hiệu ứng phân cực thân (Body Effect)**. Với PMOS, Bulk luôn nối $V_{DD} = 5,0\,\text{V}$, khi ngõ ra tiến về $0\,\text{V}$ thì $V_{BS} \approx 3,6\,\text{V}$, đẩy $|V_{tp}|$ từ $0,80\,\text{V}$ lên $\approx 1,42 - 1,46\,\text{V}$!
2. **Hiểu đúng cơ chế điện trở $R_{TG}(V_{in})$:** Khi kết hợp song song NMOS ($4\lambda$) và PMOS ($12\lambda$), độ dẫn tổng $G_{TG} = \beta(V_{DD} - V_{tn} - |V_{tp}|)$ là hằng số trên dải giữa (nếu bỏ qua body effect), cho $R_{TG} \approx \mathbf{1,19\,\text{k}\Omega}$ (chứ **không** phải $490\,\Omega$). Khi tính đầy đủ body effect, $R_{TG}$ đạt đỉnh ở giữa dải khoảng $1,68\,\text{k}\Omega$.
3. **Nhận diện bản chất mạch thụ động và chồng dẫn của MUX TG:** TG MUX không khôi phục mức (non-restoring) và tồn tại khoảng chồng dẫn ngắn cỡ $t_{pd,inv}$ khi tín hiệu chọn $S$ chuyển đổi, gây xung nhiễu (glitch) khi $D_0 \neq D_1$.
4. **Nắm vững mô hình trễ Elmore trong chuỗi TG:** Trễ tăng theo hàm bậc hai $O(N^2)$, đòi hỏi phải chèn Inverter đệm sau mỗi 3–4 tầng.

---

### 4.2 Dẫn xuất giải tích Suy hao điện áp (Body Effect) và Dòng rò tĩnh

#### a. Tham số thực tế trong `C5_models.txt` vs Tham số sách giáo khoa
Giảng viên lưu ý sự khác biệt nhỏ giữa tham số mặc định trong các giáo trình (hay dùng $\gamma = 0,53\,\text{V}^{1/2}, 2\phi_F = 0,65\,\text{V}$) và tham số thực tế trong `04 - Models_and_Libraries/C5_models.txt`:
- **Trong `C5_models.txt`:**
  * NMOS (`N`): $V_{th0,n} = 0,700\,\text{V}, K'_n = 120\,\mu\text{A/V}^2, \gamma_n = 0,400\,\text{V}^{1/2}, 2\phi_{Fn} = 0,700\,\text{V}$.
  * PMOS (`P`): $|V_{th0,p}| = 0,800\,\text{V}, K'_p = 40\,\mu\text{A/V}^2, \gamma_p = 0,500\,\text{V}^{1/2}, 2\phi_{Fp} = 0,700\,\text{V}$.
- Trong Handout mới (Pre-lab), sinh viên được cung cấp chính xác tham số từ `C5_models.txt` để đối chiếu trực tiếp với LTspice.

#### b. Giải phương trình điểm cố định (Fixed-Point Iteration)
1. **NMOS Weak '1':** $V_{out,max} = V_{DD} - \left[ V_{th0,n} + \gamma_n \left(\sqrt{2\phi_{Fn} + V_{out,max}} - \sqrt{2\phi_{Fn}}\right) \right]$
   - Với tham số `C5_models.txt` ($\gamma_n = 0,40, 2\phi_F = 0,70$):
     $$V_{thn,eff} = 1,213\,\text{V} \implies \mathbf{V_{out,max} = 3,787\,\text{V}}$$
   - *(Nếu dùng tham số sách giáo khoa $\gamma = 0,53, 2\phi_F = 0,65$: $V_{thn,eff} = 1,369\,\text{V} \implies V_{out,max} = 3,631\,\text{V}$).*

2. **PMOS Weak '0' (có Body Effect):** Cực Bulk nối $V_{DD} = 5,0\,\text{V}$, cực Source nối $V_{out}$ $\implies V_{BS} = V_{DD} - V_{out}$.
   $$V_{out,min} = |V_{th0,p}| + \gamma_p \left(\sqrt{2\phi_{Fp} + (V_{DD} - V_{out,min})} - \sqrt{2\phi_{Fp}}\right)$$
   - Với tham số `C5_models.txt` ($\gamma_p = 0,50, 2\phi_F = 0,70$):
     $$|V_{tp,eff}| = 1,417\,\text{V} \implies \mathbf{V_{out,min} = 1,417\,\text{V}}$$
   - *(Nếu dùng $\gamma_p = 0,53, 2\phi_F = 0,65$: $V_{out,min} = 1,458\,\text{V}$).*
   - **Đính chính lỗi cũ:** Handout cũ ghi $V_{out,min} \approx 0,80 - 1,05\,\text{V}$ là **sai hoàn toàn** do bỏ qua hiệu ứng thân của PMOS.

#### c. Hậu quả dòng rò tĩnh ở tầng sau
Nếu đưa mức Weak '1' ($3,787\,\text{V}$) vào Inverter chuẩn `inv_x1` ($W_p = 3,6\,\mu\text{m}, L_p = 0,6\,\mu\text{m}$):
- $V_{SG,p} = 5,0 - 3,787 = 1,213\,\text{V} > |V_{tp0}| = 0,80\,\text{V}$.
- PMOS dẫn rò trong vùng bão hòa: $I_{static} \approx \frac{1}{2} K'_p \frac{W_p}{L_p} (V_{SG,p} - |V_{tp0}|)^2 \approx 0,5 \cdot 40\mu \cdot 6 \cdot (0,413)^2 \approx \mathbf{20,4\,\mu\text{A}}$ (lên tới $\sim 38,9\,\mu\text{A}$ nếu $V_{out,max} = 3,631\,\text{V}$). Đây là lý do mạch logic truyền dẫn luôn cần bộ khôi phục mức (Level Restorer).

---

### 4.3 Phân tích Điện trở Dẫn $R_{TG}(V_{in})$ và Đính chính lỗi $490\,\Omega$

**Nguyên nhân lỗi $490\,\Omega$ ở bản cũ:** Tài liệu cũ lấy $R_{on,n}(V_{GS}=5\text{V}) \approx 969\,\Omega$ mắc song song với $R_{on,p}(|V_{GS}|=5\text{V}) \approx 992\,\Omega$ để ra $490\,\Omega$ tại $V_{in} = 2,5\,\text{V}$. Điều này **sai vật lý** vì tại $V_{in} = 2,5\,\text{V}$, điện áp cổng-nguồn chỉ còn $2,5\,\text{V}$ (quá áp cổng giảm một nửa)!

Tính đúng theo mô hình bậc hai tại $V_{in} = 2,5\,\text{V}$ ($\beta_n = \beta_p = 240\,\mu\text{A/V}^2$):
- $V_{ov,n} = 5,0 - 2,5 - 0,7 = 1,8\,\text{V} \implies R_{on,n} = \frac{1}{240\mu \times 1,8} = \mathbf{2\,315\,\Omega}$
- $V_{ov,p} = 2,5 - 0,8 = 1,7\,\text{V} \implies R_{on,p} = \frac{1}{240\mu \times 1,7} = \mathbf{2\,451\,\Omega}$
- Song song: $R_{TG} = 2\,315 \parallel 2\,451 = \mathbf{1\,190,5\,\Omega \approx 1,19\,\text{k}\Omega}$.

**Bảng giá trị suy dẫn $R_{TG}(V_{in})$ theo `verify_lab04_new.py`:**

| $V_{in}$ (V) | $R_{on,n}$ không Body ($\Omega$) | $R_{on,p}$ không Body ($\Omega$) | $R_{TG}$ không Body ($\Omega$) | $R_{TG}$ có Body ($\Omega$, minh họa $\gamma=0,53$) |
| :---: | :---: | :---: | :---: | :---: |
| 0,0 | 969 | Tắt | 969 | 969 |
| 0,5 | 1 096 | Tắt | 1 096 | 1 139 |
| 1,0 | 1 263 | 20 833 | **1 190** | 1 368 |
| 1,5 | 1 488 | 5 952 | **1 190** | 1 668 |
| 2,0 | 1 812 | 3 472 | **1 190** | 1 681 |
| 2,5 | 2 315 | 2 451 | **1 190** | **1 685** |
| 3,0 | 3 205 | 1 894 | **1 190** | 1 681 |
| 3,5 | 5 208 | 1 543 | **1 190** | 1 668 |
| 4,0 | 13 889 | 1 302 | **1 190** | 1 414 |
| 4,5 | Tắt | 1 126 | 1 126 | 1 171 |
| 5,0 | Tắt | 992 | 992 | 992 |

---

### 4.4 Hiện tượng Chồng dẫn (Contention) & Trễ Elmore Chuỗi TG

1. **Chồng dẫn khi chuyển kênh $S$:** Trong `mux2_tg`, $\overline{S}$ đi qua Inverter tạo độ trễ $\Delta t \approx t_{pd,inv} \approx 30 - 45\,\text{ps}$. Khi $S$ lên $0 \to 1$, NMOS của `TG1` mở ngay trong khi NMOS của `TG0` (nhận $\overline{S}$) vẫn dẫn thêm một khoảng $\Delta t$. Khi $S$ xuống $1 \to 0$, cả hai PMOS đều mở đồng thời trong khoảng $\Delta t$. Nếu $D_0 \neq D_1$, xuất hiện dòng ngắn mạch thoáng qua giữa hai nguồn lái và xung nhiễu (glitch) trên ngõ ra $Y$.
2. **Mô hình Elmore cho chuỗi $N$ TG ($C_{node} = 10\,\text{fF}, R_{TG} = 1,19\,\text{k}\Omega$):**
   $$t_{pd}(N) \approx 0,69 \cdot R_{TG} \cdot C_{node} \cdot \frac{N(N+1)}{2}$$
   - $N = 1$: $8,2\,\text{ps}$ ($1\times$)
   - $N = 2$: $24,6\,\text{ps}$ ($3\times$)
   - $N = 3$: $49,3\,\text{ps}$ ($6\times$)
   - $N = 4$: $82,1\,\text{ps}$ ($10\times$)
   - $N = 5$: $123,2\,\text{ps}$ ($15\times$)
   - $N = 6$: $172,4\,\text{ps}$ ($21\times$)
   $\implies$ Trễ tăng theo $O(N^2)$. Quy tắc thiết kế: chèn `inv_x1` lặp lại cứ sau mỗi 3–4 cổng truyền.

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN

### 4.5 Kế hoạch Buổi học 135 Phút & Điều phối Phòng máy
- **00–10':** Cổng kiểm tra Pre-lab. Yêu cầu sinh viên nộp bài tính tay fixed-point và Stick Diagram 3 cột Poly. Nhắc nhở ngay trên bảng về lỗi phổ biến khi đo `.meas MIN` tại $t=0$.
- **10–30' (Ex4.1):** Sinh viên mô phỏng LTspice 4 nhánh và vẽ đường cong $R_{TG}(V_{in})$. Giảng viên đi kiểm tra các bạn đo được `vmin_pmos ≈ 1,4 V` (chứng tỏ đã đặt cửa sổ đo `FROM=35n TO=55n` đúng).
- **30–50' (Ex4.2):** Dựng `tg_gate{sch}` và `mux2_tg{sch}`. Nhắc sinh viên kiểm tra kỹ chân `en` (NMOS) và `en_n` (PMOS) của `TG0` và `TG1`.
- **50–75' (Ex4.3):** Mô phỏng `mux2_tg`. Kiểm tra sinh viên có chạy ca đo riêng $D_0=5\text{V}, D_1=0\text{V}$ để quan sát glitch chồng dẫn khi $S$ chuyển hay không.
- **75–85' (Ex4.4):** Ghép nhanh `mux4_tg{sch}` từ 3 instance `mux2_tg` và kiểm chứng 4 tổ hợp.
- **85–125' (Ex4.5):** Layout `mux2_tg{lay}`. Khuyến khích sinh viên dùng file khung chuẩn có sẵn ray nguồn $H_{cell}=40\lambda$ để tập trung vào việc đi 3 cột Poly và đấu dây đối xứng, kịp hoàn thành DRC và NCC trong 40 phút.
- **125–135':** Tổng kết và nghiệm thu tại bàn.

---

### 4.6 Đáp án Chi tiết Pre-lab

1. **Giải bài toán Body Effect (C5N):**
   - NMOS Weak '1': $V_{out} = 5,0 - [0,70 + 0,40(\sqrt{0,70 + V_{out}} - \sqrt{0,70})] \implies \mathbf{V_{out,max} = 3,787\,\text{V}}, V_{thn,eff} = 1,213\,\text{V}$.
   - PMOS Weak '0': $V_{out} = 0,80 + 0,50(\sqrt{0,70 + 5,0 - V_{out}} - \sqrt{0,70}) \implies \mathbf{V_{out,min} = 1,417\,\text{V}}, |V_{tp,eff}| = 1,417\,\text{V}$.
   - Giải thích TG: Do NMOS bù vùng thấp và PMOS bù vùng cao nên luôn có ít nhất 1 transistor hoạt động ở vùng tuyến tính với $V_{GS}$ lớn, kéo tụ tải $C_L$ đạt đủ $0\,\text{V}$ và $5,0\,\text{V}$ khi dòng tải tĩnh bằng 0. Nếu có tải trở nhỏ hoặc dòng rò lớn sẽ tạo sụt áp $\Delta V = I_{load} \cdot R_{TG}$.

2. **Định cỡ `TG_FAST` ($R = 0,5 \times R_{inv}$):**
   - Để điện trở giảm một nửa, kích thước độ rộng kênh phải **tăng gấp đôi** so với kích thước chuẩn (`inv_x1` $4\lambda / 12\lambda$):
     $$W_n = 8\lambda = 2,40\,\mu\text{m}, \quad W_p = 24\lambda = 7,20\,\mu\text{m}, \quad L = 2\lambda = 0,60\,\mu\text{m}$$
   - Với TG chuẩn ($4\lambda / 12\lambda$), tính $R_{TG}$ (không body effect):
     * $V_{in} = 0\,\text{V}$: $R_{TG} = R_{on,n} = \frac{1}{240\mu \cdot (5,0 - 0,7)} = \mathbf{969\,\Omega}$.
     * $V_{in} = 2,5\,\text{V}$: $R_{on,n} = 2\,315\,\Omega$, $R_{on,p} = 2\,451\,\Omega \implies R_{TG} = \mathbf{1\,190\,\Omega}$.
     * $V_{in} = 5,0\,\text{V}$: $R_{TG} = R_{on,p} = \frac{1}{240\mu \cdot (5,0 - 0,8)} = \mathbf{992\,\Omega}$.

3. **Bảng chân trị `mux4_tg`:**

| $S_1$ | $S_0$ | TG dẫn ở Tầng 1 | TG dẫn ở Tầng 2 | Ngõ ra $Y$ |
| :-: | :-: | :---: | :---: | :---: |
| 0 | 0 | `X_MUX_A.TG0` & `X_MUX_B.TG0` | `X_MUX_C.TG0` | $D_0$ |
| 0 | 1 | `X_MUX_A.TG1` & `X_MUX_B.TG1` | `X_MUX_C.TG0` | $D_1$ |
| 1 | 0 | `X_MUX_A.TG0` & `X_MUX_B.TG0` | `X_MUX_C.TG1` | $D_2$ |
| 1 | 1 | `X_MUX_A.TG1` & `X_MUX_B.TG1` | `X_MUX_C.TG1` | $D_3$ |

4. **Dự đoán chồng dẫn & Stick Diagram:**
   - Khi $S: 0 \to 1$ ($D_0=5\text{V}, D_1=0\text{V}$), `TG1` mở trước khi `TG0` tắt hẳn $\implies$ xuất hiện xung nhiễu kéo $V(y)$ giảm không đều (hoặc rung nhẹ) và đỉnh dòng nguồn ngắn mạch $I(V_{DD})$ trong khoảng $\sim 30-45\,\text{ps}$.
   - Stick Diagram 3 cột Poly chuẩn: Cột 1 = Inverter ($S \to \overline{S}$), Cột 2 = $S$ (kéo thẳng qua NMOS `TG1` và PMOS `TG0`), Cột 3 = $\overline{S}$ (kéo thẳng qua NMOS `TG0` và PMOS `TG1`).

---

### 4.7 Bảng Đối Chuẩn Kỹ Thuật Tham Chiếu (SPICE Benchmark)

*(Số liệu giải tích/suy dẫn chuẩn hóa cho mô hình MOSIS C5N $V_{DD}=5,0\,\text{V}, C_L=50\,\text{fF}$; giảng viên đối chiếu thêm với kết quả chạy LTspice trực tiếp trên máy phòng lab).*

| Hạng mục đo kiểm | Giá trị kỳ vọng | Ghi chú kỹ thuật |
| :--- | :---: | :--- |
| NMOS Weak '1' ($V_{out,max}$) | $\approx 3,79\,\text{V}$ (C5N) / $3,63\,\text{V}$ ($\gamma=0,53$) | Thực đo cuối bán chu kỳ $30\,\text{ns}$ thường thấp hơn nhẹ do tiệm cận. |
| PMOS Weak '0' ($V_{out,min}$) | $\approx 1,42\,\text{V}$ (C5N) / $1,46\,\text{V}$ ($\gamma=0,53$) | Bắt buộc đo ở cửa sổ `FROM=35n TO=55n`. |
| $R_{TG}$ tại $V_{in} = 2,5\,\text{V}$ | $\approx 1,19\,\text{k}\Omega$ (không body) $\to \sim 1,68\,\text{k}\Omega$ (có body) | Không bao giờ ra $490\,\Omega$. |
| Trễ `mux2_tg` $D \to Y$ (nguồn lý tưởng) | $\approx 40 - 50\,\text{ps}$ | $t_{pd} \approx 0,69 \cdot R_{TG} \cdot (C_L + C_{node})$. |
| Trễ `mux2_tg` $S \to Y$ | $\approx 65 - 80\,\text{ps}$ | Bao gồm $t_{pd,inv} + t_{pd,TG}$. |
| Trễ `mux4_tg` $D_0 \to Y$ | $\ge 2 \times t_{pd,MUX2}$ ($\approx 90 - 115\,\text{ps}$) | $0,69 \cdot (R \cdot C_1 + 2R \cdot C_L)$. |
| Kích thước Layout `mux2_tg{lay}` | $W \approx 29 - 32\lambda$ ($\approx 9\,\mu\text{m}$), $H = 40\lambda$ ($12\,\mu\text{m}$) | 3 cột Poly + Contact $\ge 6\lambda_{DR}$ + Taps. |

---

### 4.8 Kịch bản Gỡ lỗi Socratic cho Giảng viên (4 tình huống điển hình)

1. **Sinh viên báo: *"Thầy ơi, em đo PMOS Pass Transistor ra $V_{min} = 0,000\,\text{V}$, vậy là PMOS truyền '0' tốt chứ đâu bị Weak '0'?"***
   - *Gợi ý Socratic:* "Em hãy mở dạng sóng $V(out\_pmos)$ từ $t=0$ đến $60\,\text{ns}$ lên xem! Tại $t=0$ điện áp nó bằng mấy? Lệnh `.meas MIN` của em quét từ giây thứ mấy đến giây thứ mấy?" $\implies$ Sinh viên tự phát hiện do điểm làm việc DC khởi đầu bằng $0\,\text{V}$ và biết cách thêm `FROM=35n TO=55n`.

2. **Sinh viên thắc mắc: *"Tại sao đường $R_{TG}$ em vẽ trong LTspice lại vồng lên ở giữa tới $1,7\,\text{k}\Omega$ chứ không phẳng $490\,\Omega$ như một số sách ghi?"***
   - *Gợi ý Socratic:* "Ở $V_{in} = 2,5\,\text{V}$, $V_{GS}$ của NMOS có còn là $5\,\text{V}$ nữa không? Và hiệu ứng phân cực thân $V_{SB} = 2,5\,\text{V}$ làm điện áp ngưỡng $V_{th}$ thay đổi thế nào?" $\implies$ Sinh viên hiểu bản chất quá áp cổng giảm một nửa + body effect.

3. **Sinh viên gặp lỗi: *"Khi $S$ chuyển trạng thái, ngõ ra $Y$ của em bị sụt nhẹ một xung nhọn rồi mới lên đúng mức, có phải mạch em đấu sai không?"***
   - *Gợi ý Socratic:* "Em hãy vẽ chồng thêm hai đồ thị $V(s)$ và $V(s\_n)$ tại đúng thời điểm đó. Có khoảnh khắc nào cả NMOS của `TG0` và NMOS của `TG1` cùng mở một lúc không?" $\implies$ Sinh viên tự khám phá ra hiện tượng chồng dẫn do trễ Inverter.

4. **Sinh viên bị NCC báo lỗi `Pin mismatch` trên `mux2_tg{lay}` dù DRC báo 0 lỗi:**
   - *Gợi ý Socratic:* "Cổng truyền có phân biệt cực Source và Drain không? Nếu em hoán đổi chân `d0` và `y` trong layout thì trên phương diện vật lý nó có đối xứng không, và tại sao NCC lại báo lỗi?" $\implies$ Hướng dẫn sinh viên kiểm tra lại vị trí đặt nhãn Export `y` tại nút nối chung ở giữa.

---

### 4.9 Đáp án Chi tiết Câu hỏi Thảo luận Post-lab

1. **Câu 1 (Chuỗi $N$ TG & Elmore $O(N^2)$):**
   - Đồ thị $t_{pd}(N)$ theo $N$ là đường cong parabol, nhưng theo $N(N+1)/2$ là đường thẳng tuyến tính.
   - Do không có bộ đệm khuếch đại dòng giữa các tầng, tụ điện tại nút thứ $k$ phải nạp/xả qua tổng điện trở của toàn bộ $k$ cổng truyền đứng trước nó: $t_{pd} = 0,69 \sum_{k=1}^N k R_{TG} C_{node} = 0,69 R_{TG} C_{node} \frac{N(N+1)}{2}$. Khuyến nghị chèn `inv_x1` sau mỗi 3–4 tầng TG để khôi phục sườn xung.
2. **Câu 2 (Cực Bulk của PMOS trong TG):**
   - TG truyền tín hiệu hai chiều ($0 \leftrightarrow V_{DD}$), nên cả hai cực S và D đều có lúc tụt xuống $0\,\text{V}$. Nếu nối Bulk (N-Well) của PMOS vào S hoặc D, khi nút đó xuống thấp hơn cực còn lại $> 0,7\,\text{V}$ (hoặc xuống đất trong khi cực kia ở mức cao), tiếp giáp P-N giữa vùng khuếch tán $P^+$ và giếng $N$-Well sẽ bị phân cực thuận, gây dòng rò lớn làm hỏng mức logic và kích hoạt Latch-up.
3. **Câu 3 (Đỉnh của $R_{TG}(V_{in})$ tại $V_{DD}/2$):**
   - Tại $V_{in} = 2,5\,\text{V}$, cả NMOS ($V_{SB} = 2,5\,\text{V}$) và PMOS ($V_{BS} = 2,5\,\text{V}$) đều chịu hiệu ứng thân làm $V_{thn}$ và $|V_{tp}|$ tăng lên đáng kể, làm giảm $(V_{DD} - V_{thn} - |V_{tp}|)$ trong công thức độ dẫn $G_{TG}$, khiến điện trở $R_{TG}$ vồng lên đạt đỉnh ở vùng giữa dải thay vì phẳng hoàn toàn.
4. **Câu 4 (So sánh công bằng TG MUX vs Static MUX):**
   - TG MUX là mạch thụ động không khôi phục mức. Nếu đo bằng nguồn áp lý tưởng ($R_{src} = 0$), TG MUX trông rất nhanh; nhưng nếu được lái bởi cổng logic yếu (trở kháng nguồn lớn) hoặc mắc nối tiếp nhiều tầng, trễ sẽ tăng nhanh theo $O(N^2)$ và có thể chậm hơn Static CMOS MUX (vốn có tầng khuếch đại khôi phục sườn xung ở mỗi cổng).

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & BỘ CÂU HỎI VẤN ĐÁP TẠI BÀN

### 4.10 Barem chấm điểm nhanh tại bàn (Thang 10)
- **Pre-lab (2,0 điểm):** Giải đúng điểm cố định Weak '1' ($\approx 3,79\,\text{V}$), Weak '0' ($\approx 1,42\,\text{V}$), định cỡ đúng `TG_FAST` ($8\lambda/24\lambda$), Stick Diagram 3 cột Poly hợp lệ.
- **Ex4.1 (2,0 điểm):** Đo đủ 4 nhánh với cửa sổ đúng (`vmin_pmos ≈ 1,4 V`), vẽ được $R_{TG}(V_{in})$ thấy đỉnh $\sim 1,6-1,8\,\text{k}\Omega$.
- **Ex4.2–Ex4.4 (2,5 điểm):** Schematic `mux2_tg` (6T), `mux4_tg` (18T) chuẩn; đo đủ 3 đường trễ, thấy glitch/dòng chồng dẫn khi $D_0 \neq D_1$.
- **Ex4.5 (2,0 điểm):** Layout `mux2_tg{lay}` 3 cột Poly đạt **0 errors DRC** và **NCC MATCH**.
- **Post-lab & Báo cáo (1,5 điểm):** Có số liệu PEX (3 chế độ), thí nghiệm chuỗi Elmore $N = 1 \dots 6$ và trả lời đúng vấn đáp.

### 4.11 Bộ câu hỏi vấn đáp nhanh tại bàn (3 câu chọn lọc)
1. *"Nếu anh/chị nối chung dây `s` vào cả hai chân `en` của `TG0` và `TG1`, mạch `mux2_tg` sẽ chạy ra cái gì?"* (Đáp: Cả hai kênh cùng mở hoặc cùng tắt $\to$ xung đột $D_0$ với $D_1$ hoặc ngõ ra thả nổi Hi-Z).
2. *"Tại sao trong `mux4_tg`, chân chọn $S_0$ lại có tải điện dung đầu vào lớn gấp đôi chân $S_1$?"* (Đáp: $S_0$ điều khiển 2 tế bào MUX tầng 1 — tức 2 Inverter và 4 TG — còn $S_1$ chỉ điều khiển 1 tế bào MUX tầng 2).
3. *"Khi làm Post-layout PEX cho `mux2_tg`, tại sao nút `y` lại có điện dung ký sinh lớn hơn hẳn so với một cổng truyền `tg_gate` đứng một mình?"* (Đáp: Nút `y` là nơi hội tụ của **4 cực khuếch tán Drain** từ cả `TG0` và `TG1` — 2 NMOS và 2 PMOS — cộng thêm dây nối Metal gộp ngõ ra).
