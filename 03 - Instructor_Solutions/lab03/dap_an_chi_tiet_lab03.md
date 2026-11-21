# ĐÁP ÁN CHI TIẾT VÀ HƯỚNG DẪN CHẤM BÀI THỰC HÀNH 3
# CỔNG PHỨC HỢP AOI21 VÀ TỐI ƯU TRỄ THEO PHƯƠNG PHÁP LOGICAL EFFORT
*(Dành riêng cho Giảng viên & Trợ giảng — Không phát cho sinh viên)*

---

## I. ĐÁP ÁN TÍNH TOÁN LÝ THUYẾT (PRE-LAB)

### 1. Bảng chân trị logic của AOI21 ($Y = \overline{(A \cdot B) + C}$)

| A | B | C | $A \cdot B$ | $(A \cdot B) + C$ | Ngõ ra Y lý thuyết | Trạng thái dẫn điện của mạng |
| :-: | :-: | :-: | :-: | :-: | :---: | :--- |
| 0 | 0 | 0 | 0 | 0 | **1** | PUN dẫn: $M_{PA}, M_{PB}, M_{PC}$ cùng dẫn |
| 0 | 0 | 1 | 0 | 1 | **0** | PDN dẫn qua nhánh $M_{NC}$ |
| 0 | 1 | 0 | 0 | 0 | **1** | PUN dẫn: $M_{PA}, M_{PC}$ dẫn nối tiếp |
| 0 | 1 | 1 | 0 | 1 | **0** | PDN dẫn qua nhánh $M_{NC}$ |
| 1 | 0 | 0 | 0 | 0 | **1** | PUN dẫn: $M_{PB}, M_{PC}$ dẫn nối tiếp |
| 1 | 0 | 1 | 0 | 1 | **0** | PDN dẫn qua nhánh $M_{NC}$ |
| 1 | 1 | 0 | 1 | 1 | **0** | PDN dẫn qua chuỗi $M_{NA} - M_{NB}$ |
| 1 | 1 | 1 | 1 | 1 | **0** | PDN dẫn qua cả hai nhánh ($M_{NA}-M_{NB}$ và $M_{NC}$) |

---

### 2. Kích thước định cỡ Transistor tế bào `AOI21_X1`
- Chuẩn tham chiếu: Inverter `INV_X1` ($W_n = 4\lambda = 1.20\,\mu\text{m}, W_p = 12\lambda = 3.60\,\mu\text{m}, L = 2\lambda = 0.60\,\mu\text{m}$).
- Điện trở dẫn chuẩn: $R_{on,n0} \approx 969\,\Omega, R_{on,p0} \approx 992\,\Omega$.

| Transistor | Vị trí mạch | Kích thước $(W/L)$ theo $\lambda$ | Kích thước $(W/L)$ theo $\mu\text{m}$ | Điện trở tương đương $R_{on}$ ($\Omega$) |
| :--- | :---: | :---: | :---: | :---: |
| **$M_{PA}$** | PUN (nhánh A) | $24\lambda / 2\lambda$ | $7.20\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,PA} \approx 496\,\Omega$ |
| **$M_{PB}$** | PUN (nhánh B) | $24\lambda / 2\lambda$ | $7.20\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,PB} \approx 496\,\Omega$ |
| **$M_{PC}$** | PUN (nhánh C) | $24\lambda / 2\lambda$ | $7.20\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,PC} \approx 496\,\Omega$ |
| **$M_{NA}$** | PDN (nhánh nối tiếp) | $8\lambda / 2\lambda$ | $2.40\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,NA} \approx 485\,\Omega$ |
| **$M_{NB}$** | PDN (nhánh nối tiếp) | $8\lambda / 2\lambda$ | $2.40\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,NB} \approx 485\,\Omega$ |
| **$M_{NC}$** | PDN (nhánh đơn C) | $4\lambda / 2\lambda$ | $1.20\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,NC} \approx 969\,\Omega$ |

- **Kiểm tra điện trở tương đương tổng:**
  * Kéo lên xấu nhất (chỉ $M_{PA}$ và $M_{PC}$ dẫn): $R_{eq,P} = 496 + 496 = 992\,\Omega \equiv R_{on,p0}$ (Cân bằng chuẩn).
  * Kéo xuống qua nhánh nối tiếp ($M_{NA}$ và $M_{NB}$ dẫn): $R_{eq,N} = 485 + 485 = 970\,\Omega \equiv R_{on,n0}$ (Cân bằng chuẩn).
  * Kéo xuống qua nhánh đơn ($M_{NC}$ dẫn): $R_{eq,N} = 969\,\Omega \equiv R_{on,n0}$ (Cân bằng chuẩn).

---

### 3. Nỗ lực Logic (Logical Effort) và Trễ Ký Sinh
- Điện dung Inverter chuẩn: $C_{in,inv} \propto 4\lambda + 12\lambda = 16\lambda$.
- **Nỗ lực logic:**
  $$g_A = \frac{8\lambda + 24\lambda}{16\lambda} = \frac{32}{16} = \mathbf{2.000} \quad \left(=\frac{6}{3}\right)$$
  $$g_B = \frac{8\lambda + 24\lambda}{16\lambda} = \frac{32}{16} = \mathbf{2.000} \quad \left(=\frac{6}{3}\right)$$
  $$g_C = \frac{4\lambda + 24\lambda}{16\lambda} = \frac{28}{16} = \mathbf{1.750} \quad \left(=\frac{7}{4}\right)$$
- **Trễ ký sinh:**
  $C_{out,parasitic} \propto 24\lambda (\text{Drain } M_{PC}) + 8\lambda (\text{Drain } M_{NA}) + 4\lambda (\text{Drain } M_{NC}) = 36\lambda$.
  $$p_{AOI21} = \frac{36\lambda}{16\lambda} = \mathbf{2.250} \quad \left(=\frac{9}{4}\right)$$

---

### 4. Tối ưu Hóa Chuỗi Đệm Inverter ($C_{in} = 20\,\text{fF}, C_L = 1\,\text{pF} \implies H = 50$)

| Số tầng $N$ | Nỗ lực tầng $\hat{f} = 50^{1/N}$ | Trễ nỗ lực $N \cdot \hat{f}$ | Trễ ký sinh $N \cdot p$ ($p=1$) | Tổng trễ chuẩn hóa $D / \tau$ | Đánh giá kỹ thuật |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **$N = 1$** | $50.00$ | $50.00\,\tau$ | $1.00\,\tau$ | **$51.00\,\tau$** | Tải quá nặng, trễ cực lớn, sườn xung biến dạng |
| **$N = 2$** | $7.071$ | $14.14\,\tau$ | $2.00\,\tau$ | **$16.14\,\tau$** | Tốt, nhưng $\hat{f} = 7.07$ vẫn hơi lớn |
| **$N = 3$** | **$3.684$** | **$11.05\,\tau$** | **$3.00\,\tau$** | **$14.05\,\tau$** | **CỰC TIỂU TỐI ƯU ($\hat{f} \approx 3.7$)** |
| **$N = 4$** | $2.659$ | $10.64\,\tau$ | $4.00\,\tau$ | **$14.64\,\tau$** | Bắt đầu bị phạt bởi trễ ký sinh của 4 tầng |
| **$N = 5$** | $2.187$ | $10.93\,\tau$ | $5.00\,\tau$ | **$15.93\,\tau$** | Quá nhiều tầng, diện tích lớn, trễ tăng |

- **Định kích thước chuỗi tối ưu $N = 3$ ($\hat{f} = 3.684$):**
  * Tầng 1: Size $1.0\times$ $\implies W_n = 1.20\,\mu\text{m}, W_p = 3.60\,\mu\text{m}$.
  * Tầng 2: Size $3.68\times$ $\implies W_n = 4.42\,\mu\text{m}, W_p = 13.26\,\mu\text{m}$.
  * Tầng 3: Size $13.57\times$ $\implies W_n = 16.29\,\mu\text{m}, W_p = 48.86\,\mu\text{m}$.

---

## II. BẢNG SỐ LIỆU ĐO ĐẠC BENCHMARK SPICE (KIỂM CHỨNG)

*(Số liệu mô phỏng trực tiếp từ thư viện C5_models.txt trên LTspice)*

### 1. Thời gian trễ cổng AOI21 ($C_L = 50\,\text{fF}$)

| Kịch bản kích thích | $t_{pHL}$ (ps) | $t_{pLH}$ (ps) | $t_{pd}$ trung bình (ps) | Nhận xét đối chiếu |
| :--- | :---: | :---: | :---: | :--- |
| **Kích ngõ A** ($B=5\,\text{V}, C=0\,\text{V}$) | $112.5$ | $124.8$ | **$118.65$** | Dòng xả qua 2 NMOS nối tiếp |
| **Kích ngõ C** ($A=0\,\text{V}, B=0\,\text{V}$) | $76.2$ | $122.4$ | **$99.30$** | Dòng xả qua 1 NMOS đơn $\to$ Nhanh hơn **$16.3\%$** |

### 2. Đo đạc thực nghiệm Logical Effort ngõ vào A (Quét Fan-out $h$)

| Fan-out $h$ | Tải dung $C_L$ (fF) | $t_{pHL}$ (ps) | $t_{pLH}$ (ps) | $t_{pd}$ (ps) |
| :---: | :---: | :---: | :---: | :---: |
| **$h = 1$** | $20\,\text{fF}$ | $72.1$ | $86.4$ | **$79.25$** |
| **$h = 2$** | $40\,\text{fF}$ | $99.8$ | $111.5$ | **$105.65$** |
| **$h = 3$** | $60\,\text{fF}$ | $127.4$ | $136.2$ | **$131.80$** |
| **$h = 4$** | $80\,\text{fF}$ | $154.9$ | $161.0$ | **$157.95$** |

- **Độ dốc (Slope):** $\frac{\Delta t_{pd}}{\Delta h} = \frac{157.95 - 79.25}{3} \approx 26.23\,\text{ps/unit-effort}$.
- Với $\tau \approx 13.1\,\text{ps}$ của Inverter chuẩn C5N:
  $$g_{meas} = \frac{26.23}{13.1} \approx \mathbf{2.002} \quad (\text{Khớp lý thuyết } 2.000 \text{ với sai số } < 0.2\%)$$
- **Giao điểm trục tung (Y-intercept tại $h=0$):**
  $$t_{pd}(h=0) \approx 79.25 - 26.23 = 53.02\,\text{ps} \implies p_{meas} = \frac{53.02}{13.1} \approx \mathbf{4.05} \times \tau_{step}$$

### 3. Kết quả mô phỏng Tối ưu Chuỗi đệm lái tải $C_L = 1.0\,\text{pF}$

| Thông số đo đạc | Kịch bản A (Inverter đơn 1X) | Kịch bản B (Chuỗi đệm 3 tầng) | Tỉ số cải thiện (Speed-up) |
| :--- | :---: | :---: | :---: |
| **Thời gian trễ $t_{pd}$** | **$2.28\,\text{ns}$** | **$0.64\,\text{ns}$** | **Nhanh hơn $3.56$ lần (cải thiện $356\%$)** |
| **Thời gian sườn lên $t_{rise}$ ($10\% \to 90\%$)** | $4.85\,\text{ns}$ | $0.88\,\text{ns}$ | Nhanh hơn $5.51$ lần |
| **Thời gian sườn xuống $t_{fall}$ ($90\% \to 10\%$)**| $2.35\,\text{ns}$ | $0.62\,\text{ns}$ | Nhanh hơn $3.79$ lần |

---

## III. HƯỚNG DẪN CHẤM VÀ CÂU HỎI VẤN ĐÁP TẠI BÀN

### Barem chấm điểm (Thang 10):
1. **Kiểm tra Pre-lab (2.0 điểm):**
   - Lập đúng bảng chân trị 8 trạng thái và kích thước $W/L$ 6 transistor: **0.75 đ**.
   - Tính đúng $g_A=2.0, g_B=2.0, g_C=1.75$ và $p=2.25$: **0.75 đ**.
   - Tính đúng bài toán chuỗi đệm $N=1..5$, xác định $N=3$ tối ưu: **0.5 đ**.
2. **Schematic & Mô phỏng Logic AOI21 (3.0 điểm):**
   - Tạo Cell `aoi21_x1{sch}` đúng kích thước, đủ 6 chân Export: **1.0 đ**.
   - Dạng sóng quá độ kiểm chứng đủ 8 trạng thái logic: **1.0 đ**.
   - Đo trễ sườn lên/sườn xuống ngõ $A$ và ngõ $C$: **1.0 đ**.
3. **Thực nghiệm Chuỗi đệm Buffer Chain (2.0 điểm):**
   - Dựng đúng chuỗi 3 tầng với kích thước định cỡ theo nỗ lực $\hat{f} \approx 3.7$: **1.0 đ**.
   - Đo được thời gian trễ $t_{pd}$ và chứng minh tốc độ nhanh hơn Inverter đơn $\ge 3$ lần: **1.0 đ**.
4. **Layout, DRC & LVS (2.0 điểm):**
   - Layout hoàn thành, áp dụng Abutment chia sẻ cực má: **1.0 đ**.
   - Kiểm tra DRC báo 0 lỗi, LVS báo **"MATCH"**: **1.0 đ**.
5. **Phiếu báo cáo & Tác phong (1.0 điểm):**
   - Điền đầy đủ số liệu, giải thích hiện tượng logic sâu sắc, tuân thủ nội quy: **1.0 đ**.

### Câu hỏi vấn đáp gợi ý:
- **Hỏi:** *Tại sao ngõ vào C lại có thời gian trễ $t_{pHL}$ nhanh hơn đáng kể so với ngõ vào A?*  
  **Đáp:** Vì khi kích ngõ C, dòng phóng điện từ tụ tải $C_L$ chỉ đi qua đúng **1 transistor NMOS đơn ($M_{NC}$)** xuống đất, trong khi kích ngõ A dòng phải đi qua **chuỗi 2 NMOS nối tiếp ($M_{NA} - M_{NB}$)** và phải chịu thêm điện dung ký sinh của nút nội $X_n$.
- **Hỏi:** *Nếu cần lái tải cực lớn $C_L = 10\,\text{pF}$ từ ngõ vào $C_{in} = 20\,\text{fF}$ ($H = 500$), số tầng tối ưu $N$ sẽ là bao nhiêu?*  
  **Đáp:** $N_{opt} \approx \ln(500) \approx 6.2 \implies$ Chọn $N = 6$ hoặc $N = 7$ tầng để đạt $\hat{f} \approx 500^{1/6} \approx 2.82$.
