# THỰC HÀNH THIẾT KẾ VLSI — BÀI 9 (LAB 09)
# THIẾT KẾ ĐƯỜNG DỮ LIỆU KHỐI CỘNG NHANH 4-BIT (4-BIT CARRY LOOKAHEAD ADDER - CLA)

---
**Bộ môn:** Điện tử – Viễn thông | **Khoa:** Điện – Điện tử  
**Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Thời lượng:** 135 phút thực hành tại phòng máy (kết hợp tự học Pre-lab & hoàn thiện Post-lab)  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07+), LTspice XVII / LTspice 2025  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5µm ($\lambda = 0.30\,\mu\text{m}$, $L_{min} = 0.60\,\mu\text{m}$, $V_{DD} = 5.0\,\text{V}$)  
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Dựng và kiểm kê phần cứng Bộ cộng nhanh 4-bit CLA:** Thiết kế 3 tầng phân cấp (`pg_cell`, `clg_4b`, `sum_cell`), tự đếm chính xác số lượng transistor và tổng bề rộng kênh $\Sigma W$ cho kiến trúc đã chọn.
2. **Hiểu cấu trúc 2 tầng của khối tạo số nhớ song song (`clg_4b`):** Hiện thực $C_1 \dots C_4$ qua 2 tầng (cổng phức hợp AOI + Inverter đệm), nhận diện giới hạn **Fan-in** khi chuỗi NMOS/PMOS tăng lên 5 transistor nối tiếp ở $C_4$ và tải nặng lên các cờ $P_1, P_2$.
3. **Đo kiểm đầy đủ các đường trễ tới hạn:** Đo $t_{pd}(C_0 \to C_4)$, $t_{pd}(C_0 \to S_3)$ và các đường chuyển mạch từ toán hạng đầu vào ($A, B \to C_4$ và $A, B \to S_3$) vốn đi qua cả tầng `PG` chịu tải lớn.
4. **Đối sánh có điều kiện giữa CLA 4-bit và RCA 4-bit (Bài 6):** So sánh hai kiến trúc dưới cùng điều kiện nguồn lái và tải $C_L = 50\,\text{fF}$, đo hệ số cải thiện thực tế và nêu rõ điều kiện kích thước/số bit để CLA đạt lợi thế tốc độ so với RCA.

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

| Hạng mục | Chi tiết |
|---|---|
| **IP kế thừa từ các bài trước** | - Tế bào Inverter chuẩn `inv_x1` (Bài 1).<br>- Tế bào Cổng truyền `tg_gate` (Bài 4 — hoặc bản dựng sẵn trong gói thư viện).<br>- Khối Full Adder `mirror_adder_1b` (Bài 6, dùng ghép chuỗi 4-bit RCA để đối sánh).<br>- Thư viện mô hình SPICE: `04 - Models_and_Libraries/C5_models.txt` (NMOS: `N`, PMOS: `P`). |
| **Sản phẩm bàn giao cuối buổi** | - Tế bào `pg_cell{sch}`, `clg_4b{sch}`, `sum_cell{sch}` và khối tích hợp `cla_adder_4b{sch}`.<br>- Kết quả kiểm chứng 6 tổ hợp chức năng tĩnh và số đo trễ 4 đường ($C_0 \to C_4$, $C_0 \to S_3$, $A/B \to C_4$, $A/B \to S_3$).<br>- Bảng đối sánh trực tiếp giữa CLA 4-bit và RCA 4-bit cùng điều kiện. |
| **Kế thừa cho các bài sau** | - Phương án bộ cộng tốc độ cao tùy chọn nâng cao cho **Bài 10 (Capstone ALU 4-bit)** (Bài 10 chuẩn sử dụng `full_adder_1b` từ Bài 6; Bài 9 là đề tài tự chọn/nâng cao). |

---

## 3. CƠ SỞ LÝ THUYẾT NGẮN GỌN

### 3.1. Kiến trúc 3 Tầng của Bộ cộng nhanh 4-bit CLA

Bộ cộng CLA 4-bit tính trước đồng thời các bit số nhớ $C_1, C_2, C_3, C_4$ từ $A[3:0], B[3:0]$ và $C_0$:
1. **Tầng 1 — `pg_cell`:** Tạo cờ sinh $G_i = A_i \cdot B_i$ (`NAND2 + INV`) và cờ truyền $P_i = A_i \oplus B_i$ (`XOR2` dùng TG).
2. **Tầng 2 — `clg_4b`:** Hiện thực hệ phương trình $C_1 \dots C_4$ qua **2 tầng** (mỗi ngõ ra gồm 1 cổng phức hợp **AOI** và 1 **Inverter đệm**):
   - $C_1 = G_0 + P_0 C_0$ (`AOI21 + INV`)
   - $C_2 = G_1 + P_1 G_0 + P_1 P_0 C_0$ (`AOI321 + INV`)
   - $C_3 = G_2 + P_2 G_1 + P_2 P_1 G_0 + P_2 P_1 P_0 C_0$ (`AOI4321 + INV`)
   - $C_4 = G_3 + P_3 G_2 + P_3 P_2 G_1 + P_3 P_2 P_1 G_0 + P_3 P_2 P_1 P_0 C_0$ (`AOI54321 + INV`)
3. **Tầng 3 — `sum_cell`:** Tính tổng $S_i = P_i \oplus C_i$ (`XOR2` dùng TG).

### 3.2. Chiến lược Định cỡ và Thách thức Fan-in

- **Độ sâu chuỗi & Kích thước:** Các cổng `AOI21` đến `AOI54321` có độ sâu chuỗi nối tiếp tăng dần từ $2$ lên $5$ transistor (cả PDN và PUN).
  * Nếu áp dụng **quy tắc cùng sức kéo với `inv_x1`** ($4\lambda/12\lambda$), các cổng $C_1, C_2, C_3, C_4$ cần kích thước tăng tuyến tính theo độ sâu: NMOS $= 8, 12, 16, 20\lambda$ và PMOS $= 24, 36, 48, 60\lambda$ (làm tổng bề rộng $\Sigma W$ rất lớn).
  * Để cân bằng giữa diện tích và độ phức tạp định tuyến trong bài thực hành này, ta áp dụng **chiến lược kích thước cố định $W_n = 8\lambda$ ($2.4\,\mu\text{m}$) và $W_p = 24\lambda$ ($7.2\,\mu\text{m}$)** cho tất cả các nhánh AOI (tương ứng $\approx 40\%$ sức kéo của `inv_x1` ở chuỗi 5 transistor của $C_4$), kết hợp Inverter đệm ngõ ra chuẩn `inv_x1`.
- **Thách thức Fan-in & Tải trên $P_i$:** Khi mở rộng số bit $N$, độ sâu chuỗi và số transistor trong CLG tăng nhanh theo $O(N^2)$, đồng thời các đường cờ như $P_1, P_2$ phải kéo rất nhiều cực cổng trong CLG (tạo tải lớn cho tầng `PG`). Do đó với bộ cộng lớn ($8, 16, 32$ bit), kỹ sư không xây CLG phẳng 1 khối mà phải chia nhóm 4-bit phân cấp (Hierarchical CLA).
- **Lưu ý về Diện tích:** Số lượng transistor không đại diện trực tiếp cho diện tích silicon; cần đánh giá thêm qua tổng bề rộng kênh $\Sigma W$ (và diện tích Layout thực tế nếu có).

---

## 4. CÂU HỎI CHUẨN BỊ TRƯỚC KHI ĐẾN LỚP (PRE-LAB)

> [!IMPORTANT]
> Sinh viên phải hoàn thành phần tính toán dưới đây vào **Mục 7.2.a** trước khi vào phòng máy để phục vụ **Cổng kiểm tra Pre-lab (10 phút đầu giờ)**.

1. **Khai triển biến thể CLA & Vẽ mạng PUN/PDN:**
   - Cho một khối **CLA 3-bit** (hoặc khối nhóm 2-bit dùng cờ nhóm $P_G = P_1 P_0, G_G = G_1 + P_1 G_0$): hãy khai triển biểu thức $C_3$ theo $G_0, G_1, G_2, P_0, P_1, P_2, C_0$.
   - Vẽ sơ đồ mạch mức transistor (cả mạng PDN và mạng PUN) cho cổng phức hợp AOI321 tạo $\overline{C_2}$ kèm Inverter đệm ra $C_2$.
2. **Tự đếm Transistor và $\Sigma W$ cho CLA 4-bit:**
   - Chọn một kiến trúc `XOR2` dùng Cổng truyền (ví dụ dùng 2 Inverter + 2 TG = $8\text{T}$, hoặc bản tối ưu $6\text{T}$). Từ đó tự đếm tổng số transistor của `pg_cell`, `clg_4b` (`AOI21 + AOI321 + AOI4321 + AOI54321 + 4 INV`), `sum_cell` và toàn bộ khối `cla_adder_4b`.
   - Tính tổng bề rộng kênh $\Sigma W$ (theo $\lambda$) của khối `clg_4b` với kích thước cố định ($8\lambda/24\lambda$ cho AOI, $4\lambda/12\lambda$ cho INV) và so sánh với $\Sigma W$ của chuỗi 4-bit RCA (`4 x 528λ = 2112λ` từ Bài 6).
   - Nêu **một điều kiện** để kiến trúc CLA có lợi thế rõ rệt hơn RCA và **một điều kiện** để kiến trúc RCA có lợi hơn CLA.
3. **Phân tích tải Fan-in và Đường xấu nhất:**
   - Đếm số lần xuất hiện của từng tín hiệu $P_0, P_1, P_2, P_3, G_0 \dots G_3, C_0$ bên trong khối `clg_4b`. Tính tổng bề rộng cổng $W_{gate}$ mà ngõ ra $P_1$ của `pg_cell` phải lái.
   - Dự đoán đường nào trong hai đường ($C_0 \to C_4$ hay $G_0 \to C_4$ khi $A_0=B_0$ chuyển mạch) có trễ lớn hơn và giải thích tại sao.
   - Viết khung kích thích SPICE cho trường hợp $A = 1111_2, B = 0000_2, C_0: 0 \to 1$ và dự đoán trạng thái đầu ra của $S[3:0]$ và $C_4$.

---

## 5. KẾ HOẠCH PHÂN BỔ THỜI LƯỢNG IN-LAB (135 PHÚT)

| Phân đoạn | Nội dung thực hiện | Thời lượng |
| :--- | :--- | :---: |
| **Kiểm tra đầu giờ** | Cổng kiểm tra Pre-lab (khai triển biến thể, đếm T/$\Sigma W$, phân tích tải $P_1$) | 10 phút |
| **Ex9.1** | Dựng Schematic `pg_cell{sch}` (`NAND2+INV` + `XOR_TG`) và `sum_cell{sch}` trên Electric | 20 phút |
| **Ex9.2** | Dựng Schematic `clg_4b{sch}` (4 cổng AOI + 4 INV; có khung sẵn 1 cổng để tăng tốc) | 35 phút |
| **Ex9.3** | Ghép nối phân cấp `cla_adder_4b{sch}` và kiểm chứng 6 tổ hợp chức năng tĩnh | 15 phút |
| **Ex9.4** | Mô phỏng đo trễ 4 đường ($C_0 \to C_4, C_0 \to S_3$ và $A/B \to C_4, A/B \to S_3$) | 25 phút |
| **Ex9.5** | Ghép đối sánh trực tiếp CLA 4-bit vs RCA 4-bit (Bài 6) dưới cùng tải và bộ lái | 20 phút |
| **Tổng kết** | Ghi nhận số liệu vào Phiếu báo cáo và ký nghiệm thu tại bàn | 10 phút |
| **Tổng cộng** | | **135 phút** |

*(Lưu ý: Theo lộ trình, Lab 9 là bài tự chọn/đồ án, không bắt buộc thực hiện Layout/PEX trong giờ thực hành).*

---

## 6. NỘI DUNG THỰC HÀNH TẠI LỚP (IN-LAB)

### Ex9.1: Thiết kế `pg_cell{sch}` và `sum_cell{sch}` (Electric VLSI)

1. Tạo tế bào `xor_tg{sch}` ($8\text{T}$: 2 `inv_x1` đảo $A, B$ + 2 `tg_gate` với $W_n=4\lambda, W_p=8\lambda$) hoặc dùng khung `xor_tg` sẵn có.
2. Tạo tế bào `pg_cell{sch}`:
   - Nhánh $G$: 1 cổng `NAND2` ($W_p=12\lambda, W_n=8\lambda$) nối qua `inv_x1` tạo $G_i = A_i \cdot B_i$.
   - Nhánh $P$: 1 cổng `xor_tg` tạo $P_i = A_i \oplus B_i$.
   - Tạo Export: `a, b` (Input), `p, g` (Output), `vdd, gnd`. Kiểm tra `F5` đạt 0 lỗi.
3. Tạo tế bào `sum_cell{sch}` dùng 1 cổng `xor_tg` (`p, c` $\to$ `s`).

- **Sản phẩm Ex9.1:** `pg_cell{sch}` ($14\text{T}$) và `sum_cell{sch}` ($8\text{T}$) đạt 0 lỗi `F5`.

---

### Ex9.2: Thiết kế Khối tạo số nhớ `clg_4b{sch}` (Electric VLSI)

1. Tạo Cell `clg_4b{sch}` (hoặc mở khung có sẵn cổng `AOI54321` để tiết kiệm thời gian đi dây).
2. Dựng 4 cổng `AOI21`, `AOI321`, `AOI4321`, `AOI54321` với kích thước $W_n = 8\lambda$ ($2.4\,\mu\text{m}$), $W_p = 24\lambda$ ($7.2\,\mu\text{m}$), $L = 2\lambda$ ($0.6\,\mu\text{m}$). Đặt tên nút nội trước Inverter là `c1_b, c2_b, c3_b, c4_b` để dễ quan sát dạng sóng.
   - *Lưu ý thứ tự chuỗi:* Đặt chân $C_0$ (và $G_0$) ở vị trí thuận lợi gần nút ngõ ra `c_b` trong nhánh dài nhất.
3. Nối `c1_b .. c4_b` qua 4 Inverter đệm `inv_x1{ic}` để xuất ra `c1, c2, c3, c4`.
4. Tạo Export: `p0..p3, g0..g3, c0` (Input), `c1..c4` (Output), `vdd, gnd`. Kiểm tra `F5` đạt 0 lỗi.

- **Sản phẩm Ex9.2:** `clg_4b{sch}` ($76\text{T}$) đạt 0 lỗi `F5`.

---

### Ex9.3: Tích hợp `cla_adder_4b{sch}` & Kiểm chứng 6 Tổ hợp (LTspice)

1. Tạo Cell `cla_adder_4b{sch}`, ghép nối 4 `pg_cell{ic}`, 1 `clg_4b{ic}` và 4 `sum_cell{ic}`. Kiểm tra `F5` đạt 0 lỗi.
2. Xuất Netlist sang LTspice (`CL = 50fF` trên mỗi chân `s0..s3, c4`), chạy kiểm chứng 6 tổ hợp chức năng tĩnh (bao gồm cả $C_0 = 1$ và tổ hợp $P, G$ hỗn hợp):
   - Ca 1: $5 + 3 + 0$ ($A=0101, B=0011, C_0=0$)
   - Ca 2: $9 + 6 + 0$ ($A=1001, B=0110, C_0=0$)
   - Ca 3: $12 + 7 + 0$ ($A=1100, B=0111, C_0=0$)
   - Ca 4: $7 + 8 + 1$ ($A=0111, B=1000, C_0=1$)
   - Ca 5: $5 + 10 + 1$ ($A=0101, B=1010, C_0=1$ — truyền carry toàn dải)
   - Ca 6: $15 + 15 + 1$ ($A=1111, B=1111, C_0=1$)

- **Sản phẩm Ex9.3:** Kết quả mô phỏng 6 tổ hợp đúng 100% bảng chân trị.

---

### Ex9.4: Đo Trễ các Đường Tới hạn ($C_0$ và $A, B$) (LTspice)

Chạy mô phỏng với bước tích phân chặt `.tran 0 15n 0 5p`, các xung kích thích có $t_r = t_f = 100\,\text{ps}$, đo trễ giữa hai mốc $50\%$–$50\%$ (`2.5V`):

1. **Ca 1 — Đường $C_0$ truyền qua CLG tĩnh ($P = 1111, G = 0000$):**
   - Đặt $A = 1111_2, B = 0000_2$, cấp xung `Vc0` chuyển $0 \to 5\,\text{V}$ tại $t = 5\,\text{ns}$ (`PULSE(0 5.0 5n 0.1n 0.1n 5n 10n)`).
   - Đo $t_{pd(C0 \to C4)}$ và $t_{pd(C0 \to S3)}$ (chú ý quan sát glitch trên $S_3$ trước khi ổn định).
2. **Ca 2 — Đường từ toán hạng $A, B$ (đi qua tầng `PG` chịu tải nặng):**
   - **Ca 2a ($G_0$ chuyển):** Đặt $A[3:1] = 111, B[3:1] = 000$ ($P_1=P_2=P_3=1$), $B_0 = 5\,\text{V}, C_0 = 0\,\text{V}$, cho xung `Va0` chuyển $0 \to 5\,\text{V}$ tại $t = 5\,\text{ns}$ để $G_0$ nhảy $0 \to 1$. Đo $t_{pd(A0 \to C4)}$ và $t_{pd(A0 \to S3)}$.
   - **Ca 2b ($P_0$ chuyển):** Đặt $A[3:1] = 111, B[3:0] = 0000, C_0 = 5\,\text{V}$, cho `Va0` chuyển $0 \to 5\,\text{V}$ tại $t = 5\,\text{ns}$. Đo $t_{pd(A0 \to C4)}$.

- **Sản phẩm Ex9.4:** Bảng số liệu đo trễ đầy đủ cả đường $C_0$ và đường $A, B$.

---

### Ex9.5: Đối sánh Trực tiếp CLA 4-bit vs RCA 4-bit (LTspice)

1. Trong cùng tệp mô phỏng LTspice, gọi song song 2 mạch:
   - `X_cla`: `cla_adder_4b` (từ Ex9.3).
   - `X_rca`: Chuỗi 4 tế bào `mirror_adder_1b` nối tiếp (từ Bài 6).
2. Đặt **cùng bộ lái đầu vào `inv_x1`** (hoặc cùng nguồn xung $t_r = t_f = 100\,\text{ps}$) và **cùng tụ tải ngõ ra $C_L = 50\,\text{fF}$** cho cả hai bộ cộng.
3. Chạy lại Ca 1 ($C_0$ chuyển) và Ca 2a ($A_0$ chuyển) cho cả `X_cla` và `X_rca`.
4. Điền bảng so sánh 4 cột trễ ($C_0 \to C_4$, $C_0 \to S_3$, $A_0 \to C_4$, $A_0 \to S_3$), tính hệ số cải thiện thực tế và rút ra kết luận có điều kiện.

- **Sản phẩm Ex9.5:** Đồ thị dạng sóng chồng lấn $C_4, S_3$ của CLA vs RCA và bảng tính hệ số cải thiện.

---

## 7. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (POST-LAB)

### 7.1. Phân tích Mở rộng & Nội dung Tùy chọn
1. Phân tích bài toán mở rộng lên 8-bit và 16-bit: giải thích tại sao không thể giữ nguyên CLG phẳng 1 khối như 4-bit và vẽ sơ đồ khối kiến trúc CLA phân cấp 2 tầng (dùng $P_G, G_G$ nhóm 4-bit).
2. *(Tùy chọn nâng cao - Không bắt buộc):* Thiết kế Layout cấp khối cho `pg_cell` hoặc `cla_adder_4b` theo kỹ thuật định tuyến Manhattan 2 tầng kim loại (Metal 1 ngang, Metal 2 dọc) trên khung chiều cao chuẩn $H_{cell}$.

### 7.2. Phiếu báo cáo điền khuyết (Nộp kèm file mô phỏng)

```
========================================================================================
                          BÁO CÁO THỰC HÀNH: BÀI 9
       THIẾT KẾ ĐƯỜNG DỮ LIỆU KHỐI CỘNG NHANH 4-BIT (4-BIT CARRY LOOKAHEAD ADDER)
Họ và Tên: ..................................................... MSSV: .................
Lớp: ....................................... Nhóm/Bàn: ......... Ngày: .................
Chữ ký Giảng viên / Điểm nghiệm thu tại bàn: ............................................
========================================================================================
```

#### a. Phần Chuẩn bị (Pre-lab)
1. **Khai triển $C_3$ (CLA 3-bit):** $C_3 =$ ....................................................................................
2. **Đếm Transistor và $\Sigma W$ theo kiến trúc `XOR2` đã chọn (`XOR = ..... T`):**
   - `pg_cell`: ........ T (4 khối = ........ T); `clg_4b`: ........ T; `sum_cell`: ........ T (4 khối = ........ T).
   - Tổng CLA 4-bit = ........ T (so với 4-bit RCA `112T`: tăng ........ %).
   - $\Sigma W$ của `clg_4b` (cỡ cố định $8\lambda/24\lambda$) = ............ $\lambda$ (so với RCA `2112λ`).
3. **Tải Fan-in lên chân $P_1$:** Số lần xuất hiện trong `clg_4b` = ........ lần $\implies W_{gate} =$ ............ $\lambda$.

#### b. Kết quả Đo đạc Thực hành (In-lab)
1. **Ex9.3 — Kiểm chứng 6 tổ hợp chức năng tĩnh (`cla_adder_4b`):**

| Phép tính ($A + B + C_0$) | Dự đoán Pre-lab ($C_4, S[3:0]$) | Đo LTspice ($C_4, S[3:0]$) | Khớp logic? |
| :--- | :---: | :---: | :---: |
| $5 + 3 + 0$ (`0101 + 0011 + 0`) | ........ , ............ | ........ , ............ | ............ |
| $9 + 6 + 0$ (`1001 + 0110 + 0`) | ........ , ............ | ........ , ............ | ............ |
| $12 + 7 + 0$ (`1100 + 0111 + 0`) | ........ , ............ | ........ , ............ | ............ |
| $7 + 8 + 1$ (`0111 + 1000 + 1`) | ........ , ............ | ........ , ............ | ............ |
| $5 + 10 + 1$ (`0101 + 1010 + 1`) | ........ , ............ | ........ , ............ | ............ |
| $15 + 15 + 1$ (`1111 + 1111 + 1`) | ........ , ............ | ........ , ............ | ............ |

2. **Ex9.4 & Ex9.5 — Đối sánh CLA 4-bit vs RCA 4-bit (cùng bộ lái và $C_L = 50\,\text{fF}$):**

| Chỉ số đo kiểm | 4-bit RCA (Bài 6) | 4-bit CLA (Bài 9) | Chênh lệch / Cải thiện |
| :--- | :---: | :---: | :---: |
| **Tổng số Transistor** | $112\,\text{T}$ | ............ $\text{T}$ | + ............ % |
| **Tổng bề rộng $\Sigma W$** | $2112\,\lambda$ | ............ $\lambda$ | ............ % |
| **Trễ $t_{pd}(C_0 \to C_4)$** | ............ ps | ............ ps | Giảm ............ % |
| **Trễ $t_{pd}(C_0 \to S_3)$** | ............ ps | ............ ps | Giảm ............ % |
| **Trễ $t_{pd}(A_0 \to C_4)$ ($G_0$ chuyển)** | ............ ps | ............ ps | Giảm ............ % |
| **Trễ $t_{pd}(A_0 \to S_3)$ ($G_0$ chuyển)** | ............ ps | ............ ps | Giảm ............ % |

#### c. Câu hỏi Thảo luận Chuyên sâu
1. Giải thích tại sao không thể đánh giá tốc độ thực tế của CLA 4-bit nếu chỉ đo đường $C_0 \to C_4$ (với $A=1111, B=0000$) mà bỏ qua đường $A_0/B_0 \to C_4$ và $A_0/B_0 \to S_3$.
2. Với kích thước cố định $W_n=8\lambda, W_p=24\lambda$ cho cả 4 cổng AOI, tại sao chuỗi 5 transistor của cổng `AOI54321` ($C_4$) lại bị suy giảm sức kéo đáng kể so với `AOI21` ($C_1$)? Nếu đổi sang định cỡ "cùng sức kéo với `inv_x1`" thì tổng $\Sigma W$ của `clg_4b` thay đổi như thế nào?
3. Giải thích giới hạn **Fan-in** khi cố gắng mở rộng khối CLG phẳng này lên $8$-bit hoặc $16$-bit, và trình bày giải pháp CLA phân cấp nhiều tầng (Hierarchical CLA).

---

## 8. BẢNG KIỂM CHỨNG VÀ ĐỐI CHUẨN KỸ THUẬT (BENCHMARK)

| Thông số kiểm chứng | Dải giá trị kỳ vọng (MOSIS C5N) | Điều kiện kiểm tra |
| :--- | :---: | :--- |
| **Số Transistor `clg_4b`** | **$76\text{T}$** (`68T` AOI + `8T` INV) | Đầy đủ 4 cổng AOI và 4 INV |
| **Tổng Transistor `cla_adder_4b`** | $132\text{T}$ (`4T` XOR) / $148\text{T}$ (`6T`) / $164\text{T}$ (`8T`) | Tùy thuộc kiến trúc `xor_tg` |
| **$\Sigma W$ của `clg_4b`** | $1152\lambda$ (cố định $8\lambda/24\lambda$) / $2288\lambda$ (cùng sức kéo) | RCA 4-bit: $2112\lambda$ |
| **Tải lên cờ $P_1, P_2$** | $6$ nhánh AOI ($W_{gate} = 192\lambda \approx 86\,\text{fF}$) | Gấp $\sim 12\times$ `inv_x1` |
| **Ước lượng thô $t_{pd}(C_0 \to C_4)$** | Khoảng $100 - 135\,\text{ps}$ (giảm $\sim 45-55\%$ so với RCA) | Tùy bộ lái và tải $50\,\text{fF}$ |

---

## 9. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP

| Hiện tượng lỗi | Nguyên nhân gốc rễ | Cách khắc phục nhanh |
| :--- | :--- | :--- |
| **Ngõ ra $C_2, C_3, C_4$ chạy sai ở một số tổ hợp** | Nối nhầm thứ tự cờ $P_i, G_i$ trong mạng AOI321/AOI4321/AOI54321, hoặc quên đảo pha qua Inverter ở cuối cổng AOI. | Kiểm tra kỹ từng nhánh PDN/PUN của khối CLG và xác nhận các nút `c1_b..c4_b` đều đi qua `inv_x1`. |
| **Ngõ ra $S_i$ xuất hiện xung nhiễu (glitch) trước khi ổn định** | Do tầng `PG` và `CLG` có thời gian truyền khác nhau (ví dụ $P_3$ đến `sum_cell` trước khi $C_3$ từ `clg_4b` tới nơi). | Đây là glitch tổ hợp tự nhiên; đo giá trị logic sau khi ổn định hoặc đặt mốc đo `.meas` đúng sườn cuối. |
| **Tầng `PG` bị chậm bất thường khi $A_1, B_1$ chuyển trạng thái** | Do $P_1$ phải kéo 6 cặp cổng trong `clg_4b` ($W_{gate}=192\lambda$), nếu `xor_tg` quá yếu sườn xung sẽ bị kéo dài. | Đây là bản chất tải Fan-in cao; quan sát ở Ca 2 để phân tích trong báo cáo. |

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

| Tiêu chí đánh giá | Trọng số | Xuất sắc (8.5 – 10) | Khá (7.0 – 8.4) | Đạt (5.0 – 6.9) | Không đạt (< 5.0) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Chuẩn bị Pre-lab** | **20%** | Khai triển đúng biến thể, vẽ đúng PUN/PDN `AOI321`, đếm đúng T và $\Sigma W$ theo XOR đã chọn, tính đúng tải $P_1$. | Khai triển và đếm đúng T, còn sai sót nhỏ ở $\Sigma W$ hoặc tải $P_1$. | Có bài chuẩn bị nhưng đánh đồng số transistor với diện tích hoặc thiếu câu điều kiện trung lập. | Không làm Pre-lab hoặc sao chép. |
| **2. Schematic `pg_cell`, `clg_4b`, `cla_adder_4b` (Ex9.1–9.3)** | **25%** | Dựng đủ 3 khối chuẩn xác ($76\text{T}$ CLG), 0 lỗi `F5` và kiểm chứng đúng 6/6 tổ hợp bảng chân trị. | Dựng đúng schematic và chạy đúng 4/6 tổ hợp cơ bản. | Dựng mạch còn lỗi đấu nhầm nhánh AOI phải sửa lại. | Mạch sai chức năng. |
| **3. Đo trễ đầy đủ các đường (Ex9.4)** | **25%** | Đo đủ cả đường $C_0$ ($C_0 \to C_4, S_3$) và đường $A, B$ ($G_0$ chuyển, $P_0$ chuyển) với `.tran 0 15n 0 5p`. | Đo đủ đường $C_0$ và 1 ca đường $A, B$. | Chỉ đo được $C_0 \to C_4$, bỏ qua hoàn toàn đường $A, B$. | Không đo được trễ. |
| **4. Đối sánh CLA vs RCA (Ex9.5)** | **20%** | So sánh công bằng cùng bộ lái/tải $50\,\text{fF}$ trên đủ 4 cột trễ và nêu đúng điều kiện cải thiện. | So sánh được đường $C_0$ dưới cùng điều kiện, thiếu cột đường $A, B$. | So sánh khác tải/nguồn lái hoặc thiếu RCA. | Không hoàn thành Ex9.5. |
| **5. Báo cáo & Câu hỏi Fan-in** | **10%** | Báo cáo đầy đủ số liệu khớp `.log`, giải thích thấu đáo giới hạn Fan-in và kiến trúc CLA phân cấp. | Báo cáo đầy đủ, giải thích được Fan-in cơ bản. | Báo cáo thiếu số liệu hoặc thiếu giải thích mở rộng 8/16-bit. | Nộp thiếu báo cáo hoặc số liệu không khớp mô phỏng. |

---

## 11. TÀI LIỆU THAM KHẢO

1. N. H. E. Weste & D. M. Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th Ed., Addison-Wesley (Chương 11: Datapath Subsystems — Carry Lookahead Adders).
2. J. M. Rabaey, A. Chandrakasan & B. Nikolic, *Digital Integrated Circuits: A Design Perspective*, 2nd Ed., Prentice Hall (Chương 11: Designing Arithmetic Building Blocks).
3. R. Jacob Baker, *CMOS: Circuit Design, Layout, and Simulation*, 3rd Ed., Wiley-IEEE Press.
4. Thư viện mô hình SPICE chuẩn phòng thí nghiệm: `04 - Models_and_Libraries/C5_models.txt`.
