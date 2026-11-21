# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 2 (LAB 02)
# THIẾT KẾ CỔNG LOGIC TĨNH NAND2 VÀ NOR2 CMOS
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Nguyên lý Đối Ngẫu (Duality Principle) và Định Cỡ Trường Hợp Xấu Nhất
Trong mạch số CMOS tĩnh, hàm logic bù $\bar{Y}$ được thực hiện bởi mạng kéo xuống (PDN - gồm các NMOS), trong khi hàm logic $Y$ được thực hiện bởi mạng kéo lên (PUN - gồm các PMOS). Theo định lý De Morgan:
- Phép VÀ ($A \cdot B$) trong PDN (nối tiếp) biến thành phép HOẶC ($A + B$) trong PUN (song song).
- Phép HOẶC ($A + B$) trong PDN (song song) biến thành phép VÀ ($A \cdot B$) trong PUN (nối tiếp).

#### Nguyên lý định cỡ trường hợp xấu nhất (Worst-Case Sizing):
Cổng logic đa ngõ vào phải được định cỡ sao cho trong tình huống dẫn điện bất lợi nhất, dòng điện nạp/xả tương đương Inverter chuẩn `INV_X1` ($R_{on,n0} \approx 969\,\Omega, R_{on,p0} \approx 992\,\Omega$):

1. **Cổng NAND2 ($Y = \overline{A \cdot B}$):**
   - **PDN:** 2 NMOS mắc nối tiếp. Khi cả hai cùng dẫn, điện trở tương đương là $R_{on,NA} + R_{on,NB}$. Để tổng điện trở bằng $R_{on,n0}$:

     $$R_{eq,N} = 2 \times \left(\frac{R_{\Box,n}}{W_n / L}\right) = \frac{R_{\Box,n}}{W_{n,inv} / L} \implies W_n = 2 \times W_{n,inv} = 2 \times 4\lambda = \mathbf{8\lambda = 2.40\,\mu\text{m}}$$

   - **PUN:** 2 PMOS mắc song song. Tình huống xấu nhất là chỉ có **1 PMOS dẫn** (ví dụ $A=0, B=1$ hoặc $A=1, B=0$). Để thời gian sườn lên đạt chuẩn:

     $$W_p = W_{p,inv} = \mathbf{12\lambda = 3.60\,\mu\text{m}}$$

   - (Khi cả hai PMOS cùng dẫn $A=0, B=0$, điện trở giảm một nửa $R_{eq,P} = R_{on,p0} / 2$, trễ $t_{pLH}$ nhanh gấp đôi).

2. **Cổng NOR2 ($Y = \overline{A + B}$):**
   - **PDN:** 2 NMOS mắc song song. Tình huống xấu nhất là chỉ có **1 NMOS dẫn**:

     $$W_n = W_{n,inv} = \mathbf{4\lambda = 1.20\,\mu\text{m}}$$

   - **PUN:** 2 PMOS mắc nối tiếp. Bắt buộc cả hai PMOS phải cùng dẫn để kéo lên nguồn:

     $$R_{eq,P} = R_{on,PA} + R_{on,PB} = R_{on,p0} \implies W_p = 2 \times W_{p,inv} = 2 \times 12\lambda = \mathbf{24\lambda = 7.20\,\mu\text{m}}$$

---

### 2. Phân Tích PPA: Bản Chất Vật Lý Tại Sao Cổng NAND Luôn Tốt Hơn Cổng NOR

Bảng đối sánh sâu sắc dành cho giảng viên giải thích cho sinh viên:

| Tiêu chí PPA | Cổng NAND2 (`nand2_x1`) | Cổng NOR2 (`nor2_x1`) | Mức độ chênh lệch |
| :--- | :---: | :---: | :---: |
| **Tổng bề rộng kênh $\sum W$** | $2(8\lambda) + 2(12\lambda) = \mathbf{40\lambda = 12.0\,\mu\text{m}}$ | $2(4\lambda) + 2(24\lambda) = \mathbf{56\lambda = 16.8\,\mu\text{m}}$ | NOR2 lớn hơn **$+40.0\%$** |
| **Diện tích Layout tế bào** | $\approx 24\lambda \times 44\lambda = \mathbf{1056\,\lambda^2}$ | $\approx 36\lambda \times 44\lambda = \mathbf{1584\,\lambda^2}$ | NOR2 tốn diện tích hơn **$+50.0\%$** |
| **Điện dung ngõ vào ($C_{in,A}$)** | $C_{ox} L (8\lambda + 12\lambda) = \mathbf{20\lambda \cdot C'}$ | $C_{ox} L (4\lambda + 24\lambda) = \mathbf{28\lambda \cdot C'}$ | NOR2 nặng tải hơn **$+40.0\%$** |
| **Logical Effort ($g$)** | $g_{NAND2} = \frac{20\lambda}{16\lambda} = \mathbf{1.250} \quad (4/3)$ | $g_{NOR2} = \frac{28\lambda}{16\lambda} = \mathbf{1.750} \quad (5/3)$ | NOR2 kém hiệu quả hơn **$+40.0\%$** |
| **Trễ sườn lên xấu nhất ($t_{pLH}$)** | Nhanh ($W_p = 12\lambda$ song song) | Chậm (chuỗi 2 PMOS $24\lambda$ bị Body Effect) | NOR2 chậm hơn $\approx 35 - 50\%$ |

> [!IMPORTANT]
> **Kết luận sư phạm:** Do độ linh động lỗ trống yếu ($\mu_p \approx \mu_n / 3$), việc mắc nối tiếp PMOS trong cổng NOR đòi hỏi kích thước $W_p$ khổng lồ ($24\lambda = 7.2\,\mu\text{m}$), gây nổ diện tích và tăng đột biến điện dung ký sinh. Do đó, trong thiết kế vi mạch công nghiệp (Standard Cell Library & ASIC Flow), **cổng NAND luôn được ưu tiên tuyệt đối so với cổng NOR**.

---

### 3. Hiệu Ứng Nút Nội ($C_{int}$) & Trễ Phụ Thuộc Vector Ngõ Vào

Xét 2 NMOS mắc nối tiếp trong cổng NAND2 với nút nội $X_n$ ở giữa:
Điện dung ký sinh tại nút nội: $C_{int} = C_{db,MN2} + C_{sb,MN1}$.

**Phân tích bằng mô hình trễ Elmore:**
- **Trường hợp A (Ngõ $A$ chuyển $0 \to 1$, ngõ $B=1$ từ trước):**
  Nút $X_n$ đã được xả điện tích xuống $0\,\text{V}$ qua $M_{N2}$ từ trước. Dòng điện qua $M_{N1}$ chỉ cần xả tụ tải $C_L$ tại nút ngõ ra $Out$:

  $$t_{pd,A} \approx 0.69 \left[ (R_{on,MN1} + R_{on,MN2}) C_L \right]$$

- **Trường hợp B (Ngõ $B$ chuyển $0 \to 1$, ngõ $A=1$ từ trước):**
  Trước thời điểm chuyển mạch, $A=1$ và $B=0$, ngõ ra đang ở mức $V_{DD} = 5\,\text{V}$. Transistor $M_{N1}$ dẫn, nạp điện tích từ ngõ ra vào nút nội $X_n$ lên điện thế $V(X_n) \approx V_{DD} - V_{thn} \approx 4.3\,\text{V}$.
  Khi $B$ nhảy từ $0 \to 1$, dòng qua $M_{N2}$ phải đồng thời xả cả tụ tải $C_L$ lẫn lượng điện tích tích trữ trên tụ nút nội $C_{int}$:

  $$t_{pd,B} \approx 0.69 \left[ (R_{on,MN1} + R_{on,MN2}) C_L + R_{on,MN2} C_{int} \right]$$

  $\implies$ **Hệ quả:** $t_{pd,B} > t_{pd,A}$ từ $15\%$ đến $25\%$. Kỹ sư vi mạch luôn nối tín hiệu đến muộn nhất vào chân $A$ (gần ngõ ra nhất) để tối ưu trễ!

---

### 4. Phương Pháp Đường Đi Euler và Kỹ Thuật Chia Sẻ Khuếch Tán (Abutment)

1. **Khái niệm:** Một đường đi Euler là đường đi trong đồ thị đi qua mỗi cạnh (mỗi transistor) đúng một lần.
2. **Quy tắc:**
   - Biểu diễn mạng PUN thành đồ thị: các nút là $V_{DD}, Out$, các cạnh là transistor $M_{P1}, M_{P2}$.
   - Biểu diễn mạng PDN thành đồ thị: các nút là $Out, X_n, GND$, các cạnh là $M_{N1}, M_{N2}$.
   - Tìm thứ tự biến cổng sao cho chu trình Euler trên PUN trùng khớp với PDN: thứ tự tối ưu là **$A - B$** (hoặc $B - A$).
3. **Kỹ thuật Abutment:**
   - Khi thứ tự cổng trùng nhau, ta đặt một dải Polysilicon liên tục chạy dọc từ PUN xuống PDN.
   - Các transistor cạnh nhau có cùng nút điện thế (ví dụ cực Drain chung nối ra $Out$) được **nối liền vùng bán dẫn khuếch tán (Diffusion Abutment)** mà không cần cắt rời cách ly $3\lambda$ và không cần tiếp xúc Contact kim loại, triệt tiêu điện dung ký sinh cực má $C_{db}$ và thu nhỏ diện tích tế bào $\approx 30\%$.

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Bảng kích thước transistor định cỡ lý thuyết

| Cổng logic | Transistor | Vai trò | Kích thước $(W/L)$ theo $\lambda$ | Kích thước $(W/L)$ theo $\mu\text{m}$ | $R_{on}$ hiệu dụng ($\Omega$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **NAND2** | $M_{N1}, M_{N2}$ | PDN (nối tiếp) | $8\lambda / 2\lambda$ | $2.40\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,N1} = R_{on,N2} = \mathbf{485\,\Omega}$ |
| **NAND2** | $M_{P1}, M_{P2}$ | PUN (song song) | $12\lambda / 2\lambda$ | $3.60\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,P1} = R_{on,P2} = \mathbf{992\,\Omega}$ |
| **NOR2** | $M_{N1}, M_{N2}$ | PDN (song song) | $4\lambda / 2\lambda$ | $1.20\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,N1} = R_{on,N2} = \mathbf{969\,\Omega}$ |
| **NOR2** | $M_{P1}, M_{P2}$ | PUN (nối tiếp) | $24\lambda / 2\lambda$ | $7.20\,\mu\text{m} / 0.60\,\mu\text{m}$ | $R_{on,P1} = R_{on,P2} = \mathbf{496\,\Omega}$ |

### 2. Bảng số liệu đo đạc thực nghiệm Benchmark SPICE ($C_L = 50\,\text{fF}$)

| Phép đo kỹ thuật | Cổng NAND2 (`nand2_x1`) | Cổng NOR2 (`nor2_x1`) | Nhận xét phân tích |
| :--- | :---: | :---: | :--- |
| **Ngưỡng chuyển mạch $V_M$ (1 ngõ quét)** | **$2.44\,\text{V}$** | **$2.46\,\text{V}$** | Cân bằng hoàn hảo quanh $V_{DD}/2$ |
| **Ngưỡng chuyển mạch $V_M$ (2 ngõ quét chung)** | **$2.58\,\text{V}$** | **$2.38\,\text{V}$** | Dời do cả 2 transistor cùng dẫn song song |
| **Trễ sườn xuống $t_{pHL}$ (Ca A: kích ngõ A)** | **$48.5\,\text{ps}$** | **$46.2\,\text{ps}$** | Dòng xả qua 2 NMOS nối tiếp |
| **Trễ sườn xuống $t_{pHL}$ (Ca B: kích ngõ B)** | **$58.2\,\text{ps}$** | **$46.2\,\text{ps}$** | **Chậm hơn $20.0\%$ do tụ nút nội $C_{int}$** |
| **Trễ sườn lên $t_{pLH}$ (Xấu nhất: 1 PMOS)** | **$51.4\,\text{ps}$** | **$52.8\,\text{ps}$** | Khớp thiết kế cân bằng $R_{on}$ |
| **Trễ sườn lên $t_{pLH}$ (Tốt nhất: 2 PMOS)** | **$26.8\,\text{ps}$** | **$52.8\,\text{ps}$** | NAND2 nhanh gấp đôi khi 2 PMOS cùng dẫn |
| **Diện tích Layout trích xuất** | **$96.8\,\mu\text{m}^2$** | **$138.5\,\mu\text{m}^2$** | **NOR2 tốn diện tích hơn $43.1\%$** |

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem chấm điểm (Thang 10):
- **Chuẩn bị Pre-lab (2.0 điểm):** Tính đúng $W/L$, $R_{on}$, trễ $RC$ lý thuyết; vẽ đúng đồ thị Euler và sơ đồ que.
- **Schematic & VTC NAND2 (2.0 điểm):** Dựng đúng Schematic, đo $V_M$ ca 1 ngõ và 2 ngõ nối chung.
- **Đo trễ quá độ & Hiệu ứng nút nội (2.0 điểm):** Đo đạc và chỉ ra được sự chênh lệch trễ giữa kích ngõ A và kích ngõ B.
- **Schematic & Đo trễ NOR2 (1.5 điểm):** Dựng đúng NOR2 ($W_p = 24\lambda$), kiểm chứng sườn lên/sườn xuống.
- **Layout NAND2, DRC & LVS (1.5 điểm):** Layout chia sẻ cực má (Abutment), 0 lỗi DRC, LVS báo **"MATCH"**.
- **Báo cáo, so sánh PPA & Tác phong (1.0 điểm):** Lập bảng so sánh PPA đầy đủ, thái độ nghiêm túc.

### 2. Câu hỏi vấn đáp gợi ý:
- **Hỏi:** Tại sao khi đo trễ sườn xuống $t_{pHL}$ của cổng NAND2, việc kích ngõ B lại chậm hơn kích ngõ A?
  **Đáp:** Do hiệu ứng tích lũy điện tích tại nút nội $X_n$. Khi kích ngõ B (ngõ A đã ở mức 1), tụ nút nội $C_{int}$ đã bị nạp lên gần $V_{DD}$. Khi ngõ B chuyển trạng thái, dòng qua transistor dưới phải đồng thời xả cả tụ tải $C_L$ lẫn tụ nút nội $C_{int}$ xuống đất, làm tăng thời gian trễ từ $15-25\%$.
- **Hỏi:** *Phương pháp đường đi Euler giúp ích gì cho kỹ sư thiết kế mặt nạ Layout vi mạch?*  
  **Đáp:** Giúp xác định thứ tự các dải Polysilicon liên tục cắt qua cả P-Active và N-Active. Nhờ đó, các cực má hoặc cực nguồn kề nhau có thể dùng chung một vùng khuếch tán (Abutment), loại bỏ hoàn toàn các khoảng cách ly cách điện ($3\lambda$), giúp thu nhỏ diện tích cell từ $25-35\%$ và giảm điện dung ký sinh dây nối.
