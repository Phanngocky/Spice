# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 03 — TEACHER'S BOOK: CỔNG PHỨC HỢP AOI21 VÀ TỐI ƯU TRỄ THEO PHƯƠNG PHÁP LOGICAL EFFORT
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-03-cong-phuc-hop-aoi-oai-logical-effort.md](../02%20-%20Giao_Trinh_Lab_Handouts/lab-03-cong-phuc-hop-aoi-oai-logical-effort.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab03/](../03%20-%20Instructor_Solutions/lab03/)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

# 3. LAB 3 — CỔNG PHỨC HỢP AOI/OAI VÀ LOGICAL EFFORT (CHƯƠNG 3, 6)

## 3.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Cổng logic phức hợp (Complex CMOS Gate AOI/OAI) giúp gom nhiều tầng logic thành một tầng duy nhất, loại bỏ các cổng inverter trung gian nhưng phải trả giá bằng việc xếp chồng transistor.
2. Nắm vững phương pháp Logical Effort (Sutherland-Sproull): mô hình trễ chuẩn hóa $d = g \cdot h + p$ để tính nhẩm kích thước và số tầng tối ưu của đường truyền mà không cần chạy SPICE.
3. Hiểu tính chất "đáy phẳng" của hàm tối ưu chuỗi đệm: số tầng tối ưu $N^*$ cho phép linh hoạt lựa chọn theo diện tích và công suất mà không làm suy giảm trễ quá mức.

---

## 3.2 Phân tích tế bào AOI21 và Định cỡ
Cổng AOI21 thực hiện hàm logic: $Y = \overline{(A \cdot B) + C}$.
- PDN: Nhánh nối tiếp $A-B$ mắc song song với nhánh $C$.
- PUN: Nhánh song song $A \parallel B$ mắc nối tiếp với nhánh $C$.

```
                       VDD (5.0V)
                           |
                     +-----+-----+
                     |           |
                 [PMOS A]    [PMOS B] (Mỗi cái 24λ)
                     |           |
                     +-----+-----+
                           |
                       (Nút nội P)
                           |
                       [PMOS C: 24λ]
                           |
                           +----------------- Out (Y)
                           |
                     +-----+-----+
                     |           |
                 [NMOS A]    [NMOS C: 4λ]
                  (8λ)       |
                     |           |
                 [NMOS B]        |
                  (8λ)           |
                     |           |
                     +-----+-----+
                           |
                          GND
```

*Sơ đồ nguyên lý tế bào AOI21_X1 và Chuỗi đệm Inverter tối ưu:*
- [aoi21_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Giao_Trinh_Lab_Handouts/images/aoi21_schematic.png)
- [buffer_chain_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Giao_Trinh_Lab_Handouts/images/buffer_chain_schematic.png)

### Bảng phân tích Logical Effort và Ký sinh của AOI21
| Ngõ vào | Cấu trúc dẫn điện tương ứng | Chiều rộng kênh $W_n + W_p$ | Logical Effort $g$ | Parasitic Delay $p$ |
| :---: | :--- | :---: | :---: | :---: |
| **Pin A** | 2 NMOS nối tiếp ($8\lambda$) + 2 PMOS nối tiếp ($24\lambda$) | $8\lambda + 24\lambda = 32\lambda$ | $g_A = 32/16 = \mathbf{2,00}$ | $p = 36/16 = \mathbf{2,25}$ |
| **Pin B** | 2 NMOS nối tiếp ($8\lambda$) + 2 PMOS nối tiếp ($24\lambda$) | $8\lambda + 24\lambda = 32\lambda$ | $g_B = 32/16 = \mathbf{2,00}$ | (Ngõ ra Out nối với cực má |
| **Pin C** | 1 NMOS đơn ($4\lambda$) + 2 PMOS nối tiếp ($24\lambda$) | $4\lambda + 24\lambda = 28\lambda$ | $g_C = 28/16 = \mathbf{1,75}$ | của $M_{PC}, M_{NA}, M_{NC}$) |

---

## 3.3 Tối ưu hóa chuỗi đệm Inverter (Inverter Buffer Chain)
- Cho tải lớn $C_L = 1,0\,\text{pF}$, ngõ vào lái $C_{in} = 20\,\text{fF} \implies$ Hệ số nỗ lực điện dung $H = C_L / C_{in} = 50,0$.
- Trễ tổng chuẩn hóa qua chuỗi $N$ tầng: $D = N \cdot H^{1/N} + N \cdot p_{inv}$. Lấy đạo hàm theo $N$ và giải nghiệm cho thấy nỗ lực tầng tối ưu là $\hat{f} \approx 3,6$ (khi $p_{inv} = 1$).

| Số tầng $N$ | Nỗ lực mỗi tầng $\hat{f} = H^{1/N}$ | Trễ chuẩn hóa $D/\tau$ | Tỉ lệ so với tối ưu | Kích thước các tầng ($W/L$) |
| :---: | :---: | :---: | :---: | :--- |
| **1 tầng** | 50,00 | $51,00\,\tau$ | Chậm gấp **$3,63$ lần** | Tầng 1: $1\text{X}$ ($4\lambda / 12\lambda$) lái thẳng $1\,\text{pF}$. |
| **2 tầng** | 7,07 | $16,14\,\tau$ | Chậm hơn $+14,8\%$ | $1\text{X} \to 7,07\text{X}$. |
| **3 tầng** | **3,68** | **$14,05\,\tau$** | **Tối ưu cực tiểu ($100\%$)** | $1\text{X} \to 3,68\text{X} \to 13,57\text{X}$. |
| **4 tầng** | 2,66 | $14,64\,\tau$ | Chậm hơn $+4,2\%$ | $1\text{X} \to 2,66\text{X} \to 7,07\text{X} \to 18,8\text{X}$. |
| **5 tầng** | 2,19 | $15,93\,\tau$ | Chậm hơn $+13,4\%$ | $1\text{X} \to 2,19\text{X} \to 4,78\text{X} \to 10,4\text{X} \to 22,9\text{X}$. |

**Chỗ cần chỉnh trong Handout gốc:** Handout ghi "tối ưu nhanh hơn $3,63$ lần (cải thiện $363\%$)". Giảng viên cần sửa cách dùng từ: Trễ giảm từ $51\,\tau$ xuống $14,05\,\tau$, tức tốc độ tăng $3,63$ lần, tương ứng thời gian trễ giảm $\frac{51 - 14,05}{51} \approx 72,5\%$. Không được dùng cụm từ "cải thiện $363\%$".

---


---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN SPICE BENCHMARK

# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 3 (LAB 03)
# CỔNG PHỨC HỢP AOI21 VÀ TỐI ƯU TRỄ THEO PHƯƠNG PHÁP LOGICAL EFFORT
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Kiến Trúc Cổng Phức Hợp (AOI/OAI) So Với Cổng Ghép Rời
Trong thiết kế vi mạch chuyên dụng (Full-Custom & Standard Cell ASIC Flow), việc hiện thực một biểu thức hàm logic phức hợp như $Y = \overline{(A \cdot B) + C}$ nếu sử dụng các cổng rời:
- **Phương án ghép cổng rời (Discrete Gates):** Cần 1 cổng AND2 (gồm 1 NAND2 4T + 1 Inverter 2T = 6T) nối sang 1 cổng NOR2 (4T).  
  $\implies$ **Tổng số transistor: $6 + 4 = \mathbf{10}$ transistor.**  
  $\implies$ **Số tầng trễ logic: 2 tầng chuyển mạch** (tín hiệu phải nạp/xả tụ ký sinh tại nút trung gian giữa 2 cổng).
- **Phương án Cổng phức hợp AOI21 (Complex CMOS Gate):** Tích hợp toàn bộ hàm logic vào duy nhất một tầng chuyển mạch:
  * PDN: Nhánh $A \cdot B$ gồm 2 NMOS nối tiếp mắc song song với 1 NMOS đơn $C$ (3 NMOS).
  * PUN: Cụm $(A \parallel B)$ gồm 2 PMOS song song mắc nối tiếp với 1 PMOS đơn $C$ (3 PMOS).  
  $\implies$ **Tổng số transistor: Đúng $\mathbf{6}$ transistor (3 PMOS + 3 NMOS).**  
  $\implies$ **Số tầng trễ logic: Duy nhất $\mathbf{1}$ tầng chuyển mạch.**  
  $\implies$ **Hiệu quả:** Tiết kiệm **$40\%$ số transistor**, giảm diện tích silicon $\approx 35\%$, triệt tiêu nút ký sinh liên tầng, giảm công suất tiêu tán động ($P_{dyn} = C V^2 f$).

---

### 2. Dẫn Xuất Định Cỡ Bề Rộng Kênh $(W/L)$ Cho Cổng AOI21
Mục tiêu: Đảm bảo khả năng kéo dòng của cổng `AOI21_X1` trong trường hợp xấu nhất tương đương Inverter chuẩn `INV_X1` ($R_{on,n0} \approx 969\,\Omega, R_{on,p0} \approx 992\,\Omega$):

1. **Mạng kéo xuống (PDN):**
   - Nhánh $A \cdot B$: Dòng xả đi qua 2 NMOS nối tiếp ($M_{NA}, M_{NB}$). Để tổng điện trở bằng $R_{on,n0}$:

     $$R_{eq,N} = R_{on,NA} + R_{on,NB} = R_{on,n0} \implies W_{n,A} = W_{n,B} = 2 \times W_{n,inv} = 2 \times 4\lambda = \mathbf{8\lambda = 2.40\,\mu\text{m}}$$

   - Nhánh $C$: Dòng xả đi qua 1 NMOS độc lập ($M_{NC}$). Để điện trở bằng $R_{on,n0}$:

     $$W_{n,C} = W_{n,inv} = \mathbf{4\lambda = 1.20\,\mu\text{m}}$$

2. **Mạng kéo lên (PUN):**
   - Biểu thức De Morgan: $Y = (\bar{A} + \bar{B}) \cdot \bar{C}$.
   - Tình huống xấu nhất (Worst-Case Pull-Up): Xảy ra khi chỉ có **1 PMOS trong cụm song song dẫn** kết hợp với $M_{PC}$ (ví dụ $A=0, B=1, C=0$ hoặc $A=1, B=0, C=0$). Khi đó, đường dẫn từ $V_{DD}$ xuống $Out$ đi qua đúng 2 PMOS mắc nối tiếp.
   - Để tổng điện trở nhánh kéo lên xấu nhất bằng $R_{on,p0}$:

     $$R_{eq,P} = R_{on,P(A/B)} + R_{on,PC} = R_{on,p0} \implies W_{p,A} = W_{p,B} = W_{p,C} = 2 \times W_{p,inv} = 2 \times 12\lambda = \mathbf{24\lambda = 7.20\,\mu\text{m}}$$

---

### 3. Phương Pháp Logical Effort (Nỗ Lực Logic) & Trễ Ký Sinh

Mô hình trễ tuyến tính chuẩn hóa của Sutherland, Sproull & Harris:

$$d = g \cdot h + p$$

#### a. Tính toán Logical Effort ($g$):
$$g = \frac{C_{in,\text{gate}}}{C_{in,\text{inverter}}} \quad (\text{with } C_{in,inv} \propto W_n + W_p = 4\lambda + 12\lambda = 16\lambda)$$

- **Ngõ vào A:** $C_{in,A} \propto W_{n,A} + W_{p,A} = 8\lambda + 24\lambda = 32\lambda \implies g_A = \frac{32\lambda}{16\lambda} = \mathbf{2.000} \quad (6/3)$.
- **Ngõ vào B:** $C_{in,B} \propto W_{n,B} + W_{p,B} = 8\lambda + 24\lambda = 32\lambda \implies g_B = \frac{32\lambda}{16\lambda} = \mathbf{2.000} \quad (6/3)$.
- **Ngõ vào C:** $C_{in,C} \propto W_{n,C} + W_{p,C} = 4\lambda + 24\lambda = 28\lambda \implies g_C = \frac{28\lambda}{16\lambda} = \mathbf{1.750} \quad (7/4)$.

> [!TIP]
> **Ý nghĩa sư phạm:** Ngõ vào $C$ chỉ nối vào 1 NMOS đơn $4\lambda$ thay vì NMOS $8\lambda$ như ngõ $A, B$, làm giảm điện dung ngõ vào từ $32\lambda$ xuống $28\lambda$, dẫn đến $g_C = 1.75 < g_{A,B} = 2.0$.  
> Do đó, trong thiết kế vi mạch số, ngõ vào $C$ được gọi là **Fast Input (Ngõ vào nhanh)** và luôn được ưu tiên gán cho tín hiệu trễ nhất trong đường truyền tới hạn (Critical Path).

#### b. Tính toán Trễ ký sinh ($p$):
Trễ ký sinh tỉ lệ với tổng điện dung cực má nối vào nút ngõ ra $Out$:

$$C_{out,parasitic} \propto W_{drain}(M_{PC}) + W_{drain}(M_{NA}) + W_{drain}(M_{NC}) = 24\lambda + 8\lambda + 4\lambda = 36\lambda$$

So với Inverter chuẩn có $C_{out,inv} \propto 12\lambda + 4\lambda = 16\lambda$:

$$p_{AOI21} = \frac{36\lambda}{16\lambda} = \mathbf{2.250} \quad (9/4\,\tau)$$

---

### 4. Dẫn Xuất Vi Tích Phân Cho Bài Toán Chuỗi Đệm Inverter Tối Ưu

Xét bài toán truyền tín hiệu từ cổng logic có điện dung ngõ vào $C_{in}$ tới tải dung nặng $C_L$. Tỉ số nỗ lực điện toàn phần: $H = \frac{C_L}{C_{in}}$.  
Nếu chèn một chuỗi gồm $N$ Inverter có kích thước tăng dần theo cấp số nhân:
- Tổng nỗ lực đường dẫn: $F = G \cdot B \cdot H = 1 \cdot 1 \cdot H = H$.
- Theo bất đẳng thức Cauchy-Schwarz, tổng trễ đạt giá trị cực tiểu khi nỗ lực trên mọi tầng bằng nhau:

  $$f_1 = f_2 = \dots = f_N = \hat{f} = H^{1/N}$$

- Tổng thời gian trễ của chuỗi:

  $$D(N) = N \cdot \hat{f} + N \cdot p_{inv} = N \left( H^{1/N} + 1 \right) \cdot \tau$$

**Dẫn xuất tìm số tầng tối ưu $N_{opt}$:**
Coi $N$ là biến số thực liên tục và lấy đạo hàm theo $N$:

$$\frac{dD}{dN} = \left(H^{1/N} + 1\right) + N \cdot \frac{d}{dN}\left(e^{\frac{\ln H}{N}}\right) = H^{1/N} + 1 + N \cdot H^{1/N} \left(-\frac{\ln H}{N^2}\right)$$

$$\frac{dD}{dN} = H^{1/N} + 1 - H^{1/N} \frac{\ln H}{N} = 0$$

Thay $\hat{f} = H^{1/N} \implies \ln \hat{f} = \frac{\ln H}{N}$:

$$\hat{f} + 1 - \hat{f} \ln \hat{f} = 0 \iff \hat{f} (\ln \hat{f} - 1) = 1$$

Giải phương trình siêu việt này bằng phương pháp lặp số:

$$\mathbf{\hat{f} \approx 3.59 \approx 3.6 - 3.7}$$

*(Nếu trễ ký sinh $p=0$, phương trình trở thành $\ln \hat{f} = 1 \implies \hat{f} = e \approx 2.718$).*

**Ứng dụng vào đề bài:** $C_{in} = 20\,\text{fF}, C_L = 1.0\,\text{pF} \implies H = \frac{1000}{20} = 50$:

$$N_{opt} = \frac{\ln(50)}{\ln(3.59)} \approx \frac{3.912}{1.278} \approx \mathbf{3.06} \implies \text{Select } \mathbf{N = 3 \text{ stages}}$$

Nỗ lực tầng thực tế: $\hat{f} = 50^{1/3} \approx \mathbf{3.684}$.

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Bảng chân trị logic của AOI21 ($Y = \overline{(A \cdot B) + C}$)

| A | B | C | $A \cdot B$ | $(A \cdot B) + C$ | Ngõ ra Y | Nhánh dẫn điện |
| :-: | :-: | :-: | :-: | :-: | :---: | :--- |
| 0 | 0 | 0 | 0 | 0 | **1** | PUN: Cả 3 PMOS cùng dẫn |
| 0 | 0 | 1 | 0 | 1 | **0** | PDN: Nhánh $M_{NC}$ dẫn |
| 0 | 1 | 0 | 0 | 0 | **1** | PUN: Chuỗi $M_{PA} - M_{PC}$ dẫn |
| 0 | 1 | 1 | 0 | 1 | **0** | PDN: Nhánh $M_{NC}$ dẫn |
| 1 | 0 | 0 | 0 | 0 | **1** | PUN: Chuỗi $M_{PB} - M_{PC}$ dẫn |
| 1 | 0 | 1 | 0 | 1 | **0** | PDN: Nhánh $M_{NC}$ dẫn |
| 1 | 1 | 0 | 1 | 1 | **0** | PDN: Chuỗi $M_{NA} - M_{NB}$ dẫn |
| 1 | 1 | 1 | 1 | 1 | **0** | PDN: Cả 2 nhánh cùng xả |

### 2. Bảng kích thước transistor định cỡ của tế bào `AOI21_X1`
- $M_{PA}, M_{PB}, M_{PC}$: $W = 24\lambda = 7.20\,\mu\text{m}, L = 2\lambda = 0.60\,\mu\text{m}$ ($R_{on,P} \approx 496\,\Omega$).
- $M_{NA}, M_{NB}$: $W = 8\lambda = 2.40\,\mu\text{m}, L = 2\lambda = 0.60\,\mu\text{m}$ ($R_{on,N} \approx 485\,\Omega$).
- $M_{NC}$: $W = 4\lambda = 1.20\,\mu\text{m}, L = 2\lambda = 0.60\,\mu\text{m}$ ($R_{on,N} \approx 969\,\Omega$).

### 3. Bảng số liệu đo đạc thực nghiệm Benchmark SPICE

| Phép đo kỹ thuật | Giá trị giải tích | Mô phỏng SPICE | Nhận xét phân tích |
| :--- | :---: | :---: | :--- |
| **Trễ ngõ A ($B=5\text{V}, C=0\text{V}, C_L=50\text{fF}$)** | $118.0\,\text{ps}$ | **$118.65\,\text{ps}$** | Xả qua 2 NMOS nối tiếp |
| **Trễ ngõ C ($A=0\text{V}, B=0\text{V}, C_L=50\text{fF}$)** | $98.0\,\text{ps}$ | **$99.30\,\text{ps}$** | **Nhanh hơn $16.3\%$ (khớp $g_C < g_A$)** |
| **Nỗ lực logic thực nghiệm $g_A$** | $2.000$ | **$2.002$** | Sai số so với lý thuyết $< 0.2\%$ |
| **Trễ ký sinh thực nghiệm $p_{AOI}$** | $2.25\,\tau$ | **$2.28\,\tau$** | Đo qua điểm chặn trục tung ($h=0$) |
| **Trễ lái tải $1\text{pF}$ (Inverter đơn 1X)** | $51.0\,\tau \approx 2.30\text{ns}$ | **$2.28\,\text{ns}$** | Sườn xung thoái hóa nghiêm trọng ($t_r = 4.85\text{ns}$) |
| **Trễ lái tải $1\text{pF}$ (Chuỗi đệm 3 tầng)** | $14.05\,\tau \approx 0.63\text{ns}$ | **$0.64\,\text{ns}$** | **Tốc độ nhanh hơn $3.56$ lần (cải thiện $356\%$)** |

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem chấm điểm (Thang 10):
- **Chuẩn bị Pre-lab (2.0 điểm):** Bảng chân trị, định cỡ $W/L$, tính $g_A, g_B, g_C, p$, giải bài toán buffer chain $N=1..5$.
- **Schematic & Kiểm chứng Logic AOI21 (3.0 điểm):** Dựng đúng cell, 6 chân Export, kiểm chứng đủ 8 trạng thái logic, đo trễ ngõ A vs ngõ C.
- **Thực nghiệm Chuỗi đệm 3 tầng (2.0 điểm):** Dựng đúng chuỗi 3 tầng Inverter ($1\times, 3.7\times, 13.6\times$), đo chứng minh trễ giảm $\ge 3.5$ lần.
- **Layout, DRC & LVS (2.0 điểm):** Layout áp dụng Abutment, 0 lỗi DRC, LVS báo **"MATCH"**.
- **Phiếu báo cáo & Tác phong (1.0 điểm):** Báo cáo đầy đủ, nhận xét sâu sắc, tuân thủ nội quy.

### 2. Câu hỏi vấn đáp gợi ý:
- **Hỏi:** *Tại sao khi thiết kế vi mạch, ngõ vào C của cổng AOI21 lại được ưu tiên gán cho đường trễ tới hạn (Critical Path)?*  
  **Đáp:** Vì nỗ lực logic của ngõ C ($g_C = 1.75$) nhỏ hơn ngõ A và B ($g = 2.0$), đồng thời trong mạng PDN nhánh C chỉ gồm duy nhất 1 transistor $M_{NC}$ dẫn thẳng xuống đất mà không bị mắc nối tiếp, giúp giảm điện dung ngõ vào và triệt tiêu điện dung nút nội, mang lại tốc độ chuyển đổi nhanh nhất.
- **Hỏi:** *Tại sao khi số tầng chuỗi đệm tăng lên $N = 4$ hay $N = 5$, tổng trễ $D$ không tiếp tục giảm mà lại tăng lên?*  
  **Đáp:** Dù nỗ lực tầng $\hat{f} = H^{1/N}$ giảm xuống khi $N$ tăng, nhưng mỗi tầng Inverter chèn thêm đều đóng góp một lượng trễ ký sinh cố định $p_{inv} \approx 1.0\,\tau$. Khi $N$ vượt quá giá trị tối ưu ($N > 3$), sự gia tăng của tổng trễ ký sinh ($N \cdot p$) sẽ vượt trội hơn mức giảm của trễ nỗ lực, làm tổng trễ toàn chuỗi tăng lên.


---

## PHẦN III: NHỮNG ĐIỂM CẦN CHỈNH SỬA TRONG HANDOUT SINH VIÊN TRƯỚC KHI LÊN LỚP

> [!WARNING]
> **Cảnh báo lỗi kỹ thuật trong Handout gốc cần khắc phục:**  
> Ghi "AOI21 giảm diện tích 40%" thực ra là giảm 40% số transistor (6T vs 10T), diện tích thực giảm ~18%; ghi "cải thiện tốc độ 363%" thực ra là trễ giảm 72% (tốc độ tăng 3,63 lần); C_in = 20 fF không khớp INV_X1 (~11,4 fF).
