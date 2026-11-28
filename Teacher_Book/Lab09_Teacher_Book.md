# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 09 — TEACHER'S BOOK: BỘ CỘNG NHANH 4-BIT CARRY LOOKAHEAD (CLA)
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-09-khoi-cong-nhanh-4bit-cla.md](../02%20-%20Student%20Workbook/lab-09-khoi-cong-nhanh-4bit-cla.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab09/](../03%20-%20Instructor_Solutions/lab09/)  
> **Script kiểm chứng số liệu:** [verify_lab09_new.py](../scripts/verify_lab09_new.py)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

### 9.0 Khái niệm chung, Định nghĩa chuẩn & Vai trò các tầng/tham số trong thực tế
*(Phần trình bày nhanh trên bảng 5–7 phút trước khi vào bài)*

1. **Khái niệm chung:**
   - **Ripple Carry Adder (RCA) vs Carry Lookahead Adder (CLA):** Trong RCA, số nhớ phải chờ gợn tuần tự qua từng bit ($O(N)$). CLA khắc phục bằng cách tính trước đồng thời toàn bộ các bit số nhớ $C_1 \dots C_N$ trực tiếp từ $A, B, C_0$ dựa trên hai cờ trung gian $G_i$ và $P_i$.
2. **Định nghĩa chuẩn:**
   - **Cờ Sinh số nhớ (Generate - $G_i = A_i \cdot B_i$):** Bằng $1$ khi cặp bit $(A_i, B_i) = (1,1)$, tự sinh số nhớ mới bất chấp $C_i$.
   - **Cờ Truyền số nhớ (Propagate - $P_i = A_i \oplus B_i$):** Bằng $1$ khi $A_i \neq B_i$, cho phép số nhớ đi vào $C_i$ truyền thẳng sang $C_{i+1}$.
   - **Fan-in (Số ngõ vào của cổng logic):** Số tín hiệu đầu vào quyết định độ sâu transistor mắc nối tiếp trong mạng PUN/PDN của cổng phức hợp AOI.
3. **Vai trò từng tầng mạch & tham số trong thực tế:**

| Tầng / Tham số | Vai trò trong mạch & Ý nghĩa thực tế khi thiết kế chip |
| :--- | :--- |
| **Tầng 1: `pg_cell` ($G_i, P_i$)** | Tính song song $G_i$ (`NAND2+INV`) và $P_i$ (`XOR_TG`) cho mọi bit cùng lúc. Chịu tải đầu ra rất không đều: $P_1, P_2$ lái tới $6$ nhánh trong CLG ($\approx 86\,\text{fF}$) trong khi $G_3$ chỉ lái $1$ nhánh. |
| **Tầng 2: `clg_4b` (AOI + INV, 76T)** | Hiện thực 2 tầng cổng phức hợp (`AOI21..AOI54321` + Inverter) để xuất $C_1 \dots C_4$ song song. Nếu giữ cỡ cố định ($8\lambda/24\lambda$) thì tiết kiệm $\Sigma W$ ($1\,152\lambda$) nhưng nhánh 5 transistor của $C_4$ bị giảm sức kéo còn $\approx 40$% `inv_x1`; nếu tăng cỡ theo độ sâu ($20\lambda/60\lambda$) thì $\Sigma W$ tăng lên $2\,288\lambda$. |
| **Tầng 3: `sum_cell` ($S_i = P_i \oplus C_i$)** | Tái sử dụng cờ $P_i$ có sẵn từ Tầng 1, kết hợp $C_i$ từ `clg_4b` để xuất tổng $S_i$. |
| **Giới hạn mở rộng ($8, 16, 32$ bit)** | Nếu mở rộng CLG phẳng, chuỗi nối tiếp tăng tới $N+1$ transistor (quá chậm) và số transistor tăng $O(N^2)$. Thực tế phải dùng **CLA phân cấp nhiều tầng** (chia nhóm 4-bit dùng $P_G, G_G$). |

---

### 9.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. **Đính chính kiểm kê Transistor và $\Sigma W$:**
   - Khối `clg_4b` chuẩn CMOS đầy đủ gồm `AOI21` ($6\text{T}$) + `AOI321` ($12\text{T}$) + `AOI4321` ($20\text{T}$) + `AOI54321` ($30\text{T}$) = $68\text{T}$ + 4 Inverter ($8\text{T}$) = **$76$ Transistors** (bản cũ ghi nhầm $62\text{T}$ do thiếu nhánh PMOS trong file SPICE rút gọn).
   - Tổng số transistor CLA 4-bit phụ thuộc vào kiến trúc `XOR2`: **$132\text{T}$** (`4T` XOR, +17,9%), **$148\text{T}$** (`6T` XOR, +32,1%), hoặc **$164\text{T}$** (`8T` XOR như `cla_4bit_tran.sp`, +46,4%) so với 4-bit RCA ($112\text{T}$). Con số `134T (+19,6%)` ở bản cũ không tái tạo được.
   - **Số transistor $\neq$ Diện tích:** Theo tổng bề rộng kênh $\Sigma W$, `clg_4b` cỡ cố định ($8\lambda/24\lambda$) có $\Sigma W = 1\,152\lambda$, còn nếu định cỡ **cùng sức kéo với `inv_x1`** ($8,12,16,20\lambda$ N và $24,36,48,60\lambda$ P) thì $\Sigma W = \mathbf{2\,288\lambda}$ (so với $4 \times$ Mirror Adder = $2\,112\lambda$).
2. **Không ấn định trước "nhanh hơn trên 60%":** Ước lượng Elmore thô cho đường $C_0 \to C_4$ (cỡ cố định $8\lambda/24\lambda$) vào khoảng $\approx 117\,\text{ps}$ so với RCA 4 tầng $\approx 240\,\text{ps}$ (giảm $\sim 51$%, chưa chắc vượt 60% ở $4$-bit!). Hơn nữa, đường tới hạn đầy đủ của cả bộ cộng phải xét từ **$A, B \to C_4$ và $A, B \to S_3$** đi qua tầng `PG` đang chịu tải nặng ($P_1, P_2$ xuất hiện $6$ lần trong CLG $\implies W_{gate} = 192\lambda \approx 86\,\text{fF}$!).
3. **Thách thức Fan-in:** Mạng `AOI54321` xếp chồng $5$ transistor nối tiếp làm tăng điện trở và độ phức tạp $O(N^2)$ khi tăng số bit $N$, đòi hỏi phải dùng CLA phân cấp (nhóm 4-bit) cho $8, 16, 32$ bit.

---

### 9.2 Bảng Kiểm kê Chi tiết Khối `clg_4b` và Tải Fan-in (Theo `verify_lab09_new.py`)

| Cổng phức hợp | Các nhánh | Số N = Số P | Độ sâu N / P | Cỡ cùng sức kéo ($W_n, W_p$) | Số T (đủ CMOS) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `AOI21` ($C_1$) | `1, 2` | 3 | 2 / 2 | $8\lambda, 24\lambda$ | 6T |
| `AOI321` ($C_2$) | `1, 2, 3` | 6 | 3 / 3 | $12\lambda, 36\lambda$ | 12T |
| `AOI4321` ($C_3$) | `1, 2, 3, 4` | 10 | 4 / 4 | $16\lambda, 48\lambda$ | 20T |
| `AOI54321` ($C_4$) | `1, 2, 3, 4, 5` | 15 | 5 / 5 | $20\lambda, 60\lambda$ | 30T |
| **Tổng AOI + 4 INV** | — | **$34\text{N}+34\text{P}+4\text{INV}$** | — | **$\Sigma W = 2\,288\lambda$** | **76T** |

**Số lần xuất hiện & Tải cổng trong `clg_4b` (cỡ cố định $8\lambda/24\lambda$):**
- $P_1, P_2$: $6$ lần $\implies W_{gate} = 192\lambda \approx 86,4\,\text{fF}$ ($12\times$ `inv_x1`).
- $P_0, P_3, G_0, C_0$: $4$ lần $\implies W_{gate} = 128\lambda \approx 57,6\,\text{fF}$ ($8\times$ `inv_x1`).
- $G_1$: $3$ lần ($96\lambda$); $G_2$: $2$ lần ($64\lambda$); $G_3$: $1$ lần ($32\lambda$).

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN

### 9.3 Kế hoạch Buổi học 135 Phút & Điều phối Phòng máy
- **00–10':** Cổng kiểm tra Pre-lab. Rà nhanh khai triển $C_3$, sơ đồ PUN/PDN của `AOI321` và phép đếm T theo kiến trúc `XOR` sinh viên chọn.
- **10–30' (Ex9.1):** Dựng `pg_cell{sch}` ($14\text{T}$) và `sum_cell{sch}` ($8\text{T}$).
- **30–65' (Ex9.2):** Dựng `clg_4b{sch}` ($76\text{T}$). Phát khung sẵn `AOI54321` để sinh viên tập trung dựng `AOI21, AOI321, AOI4321` và nối Inverter.
- **65–80' (Ex9.3):** Tích hợp `cla_adder_4b{sch}` và kiểm chứng 6 tổ hợp chức năng tĩnh.
- **80–105' (Ex9.4):** Chạy đo trễ cho cả Ca 1 ($C_0$ chuyển) và Ca 2 ($G_0, P_0$ chuyển từ $A, B$) với `.tran 0 15n 0 5p`.
- **105–125' (Ex9.5):** Đối sánh song song CLA 4-bit vs RCA 4-bit (Bài 6) dưới cùng tải $50\,\text{fF}$ và bộ lái.
- **125–135':** Tổng kết và nghiệm thu tại bàn.

---

### 9.4 Đáp án Chi tiết Pre-lab & Bảng Đối Chuẩn

1. **Khai triển $C_3$ (CLA 3-bit):**
   $$C_3 = G_2 + P_2 G_1 + P_2 P_1 G_0 + P_2 P_1 P_0 C_0$$
2. **Đếm Transistor & $\Sigma W$:**
   - Với `XOR = 8T` (`2 INV + 2 TG` như `cla_4bit_tran.sp`): `PG` $= 14\text{T}$ ($4\times = 56\text{T}$), `CLG` $= 76\text{T}$, `Sum` $= 8\text{T}$ ($4\times = 32\text{T}$) $\implies$ Tổng = **$164\text{T}$** (+46,4% so với RCA $112\text{T}$).
   - $\Sigma W$ của `clg_4b` (cố định $8\lambda/24\lambda$) = **$1\,152\lambda$** (nhỏ hơn $\Sigma W = 2\,112\lambda$ của 4-bit RCA).
   - *Điều kiện có lợi:* CLA có lợi khi số bit $N \ge 4-8$ và độ sâu Fan-in được chia nhóm hợp lý; RCA có lợi khi $N$ nhỏ ($2-4$ bit) cần tối giản diện tích/công suất tĩnh hoặc đường dữ liệu không bị gắt về trễ Carry.
3. **Tải Fan-in lên $P_1$ & Dự đoán $G_0 \to C_4$ vs $C_0 \to C_4$:**
   - $P_1$ xuất hiện $6$ lần $\implies W_{gate} = 192\lambda \approx 86,4\,\text{fF}$.
   - Đường $G_0 \to C_4$ (khi $A_0=B_0$ chuyển) chậm hơn $C_0 \to C_4$ vì phải đi thêm qua tầng `PG` (`NAND2 + INV`) và nút $G_0$ còn gánh thêm tải $4$ nhánh trong CLG ($128\lambda$).

**Bảng Đối chuẩn Kỹ thuật Tham chiếu (MOSIS C5N, $C_L = 50\,\text{fF}$):**

| Hạng mục | Giá trị suy dẫn / Tham chiếu | Ghi chú |
| :--- | :---: | :--- |
| Tổng Transistor CLA 4-bit | $132\text{T}$ (`4T` XOR) / $148\text{T}$ (`6T`) / $164\text{T}$ (`8T`) | Không ra `134T` |
| `clg_4b` Transistor / $\Sigma W$ | $76\text{T}$ / $1\,152\lambda$ (cố định) hoặc $2\,288\lambda$ (cùng sức kéo) | |
| Ước lượng thô $t_{pd}(C_0 \to C_4)$ | $\approx 100 - 135\,\text{ps}$ | Giảm $\sim 45-55$% so với RCA $240\,\text{ps}$ |
| $t_{pd}(A_0 \to C_4)$ ($G_0$ chuyển) | Chậm hơn $C_0 \to C_4$ | Do cộng thêm trễ tầng `PG` và tải $G_0$ |

---

### 9.5 Kịch bản Gỡ lỗi Socratic cho Giảng viên

1. **Sinh viên báo: *"Thầy ơi, em đếm đi đếm lại toàn khối CLA 4-bit theo mạch em dựng ra $164\text{T}$, sao một số tài liệu cũ ghi $134\text{T}$?"***
   - *Gợi ý Socratic:* "Em thử tách riêng từng khối: `clg_4b` đủ PMOS/NMOS của `AOI21..54321` là mấy transistor ($76\text{T}$), và cổng `XOR` trong `pg_cell` em đang dùng có mấy Inverter và mấy TG ($8\text{T}$)? Cộng lại có ra $164\text{T}$ không? Con số $134\text{T}$ trước đây đã bị đếm thiếu PMOS ở `clg_4b`." $\implies$ Sinh viên tin tưởng vào phép đếm chuẩn xác của chính mình.
2. **Sinh viên thắc mắc: *"Khi em đo $C_0 \to C_4$ thì CLA rất nhanh, nhưng khi đo $A_0 \to C_4$ ở Ca 2b ($P_0$ chuyển) thì thấy bị chậm đi rõ rệt!"***
   - *Gợi ý Socratic:* "Ở Ca 1 ($A=1111, B=0000$), các cờ $P, G$ đang đứng yên hay chuyển động? Còn ở Ca 2b, tín hiệu từ $A_0$ phải đi qua cổng nào trước khi vào CLG, và ngõ ra `P` phải kéo bao nhiêu cực cổng trong CLG?" $\implies$ Sinh viên hiểu vai trò tải Fan-in trên tầng `PG`.

---

### 9.6 Đáp án 3 Câu hỏi Thảo luận Post-lab
1. **Tại sao phải đo cả đường $A, B \to C_4, S_3$:** Vì trong Ca 1 ($C_0$ chuyển), tầng `PG` đứng yên nên che mất độ trễ tạo $P, G$ và hiệu ứng tải nặng ($86\,\text{fF}$ trên $P_1, P_2$) mà `pg_cell` phải gánh.
2. **Cố định $8\lambda/24\lambda$ vs Cùng sức kéo:** Ở kích thước cố định $8\lambda/24\lambda$, chuỗi 5 transistor của `AOI54321` có điện trở gấp $5/2$ lần chuỗi 2 transistor, nên sức kéo chỉ còn $\approx 40$% `inv_x1`. Nếu tăng kích thước theo độ sâu ($20\lambda/60\lambda$ cho $C_4$) để giữ cùng sức kéo thì $\Sigma W$ của `clg_4b` tăng gần gấp đôi (từ $1\,152\lambda$ lên $2\,288\lambda$).
3. **Giới hạn Fan-in & CLA phân cấp:** Nếu mở rộng CLG phẳng lên 8 hoặc 16 bit, số transistor nối tiếp lên tới 9–17 (không khả thi về tốc độ lẫn sụt áp). Giải pháp là chia thành các nhóm 4-bit tạo cờ nhóm $P_G, G_G$ đưa vào tầng CLG thứ 2 (Hierarchical CLA), giữ độ sâu tối đa ở mức 4–5 transistor.

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & BỘ CÂU HỎI VẤN ĐÁP TẠI BÀN

### 9.7 Barem chấm điểm nhanh tại bàn (Thang 10)
- **Pre-lab (2,0 điểm):** Khai triển đúng biến thể, vẽ PUN/PDN `AOI321`, đếm đúng T và $\Sigma W$ theo XOR chọn, tính đúng tải $P_1$.
- **Ex9.1–9.3 (2,5 điểm):** Dựng đủ `pg_cell`, `clg_4b` ($76\text{T}$), `cla_adder_4b`, 0 lỗi `F5`, chạy đúng 6/6 tổ hợp tĩnh.
- **Ex9.4 (2,5 điểm):** Đo đủ cả đường $C_0$ ($C_0 \to C_4, S_3$) và đường $A, B$ ($G_0, P_0$ chuyển) với `.tran 0 15n 0 5p`.
- **Ex9.5 (2,0 điểm):** Đối sánh song song CLA vs RCA cùng tải/bộ lái, điền đủ 4 cột và kết luận có điều kiện.
- **Báo cáo & Vấn đáp (1,0 điểm):** Đầy đủ số liệu và trả lời đúng vấn đáp về Fan-in.

### 9.8 Bộ câu hỏi vấn đáp nhanh tại bàn (3 câu chọn lọc)
1. *"Trong khối `clg_4b`, tại sao ngõ ra `P1` và `P2` lại chịu tải điện dung nặng nhất ($6$ nhánh AOI) so với `G3` ($1$ nhánh)?"* (Đáp: Vì $P_1$ xuất hiện trong $C_2$ (1 lần), $C_3$ (2 lần? thực ra $P_1$ xuất hiện 1 lần trong $C_2$, 2 lần trong $C_3$ và 3 lần trong $C_4$ nếu khai triển phẳng — tổng cộng 6 nhánh ở dạng SOP chưa rút gọn)).
2. *"Vì sao trong bảng thông số đối sánh CLA vs RCA ta không được kết luận diện tích CLA chỉ tăng 19,6% dựa trên số transistor?"* (Đáp: Vì kích thước mỗi transistor khác nhau; `clg_4b` cố định $8\lambda/24\lambda$ có $\Sigma W = 1\,152\lambda$ nhưng nếu giữ cùng sức kéo sẽ lên tới $2\,288\lambda$).
3. *"Nếu cần thiết kế bộ cộng 16-bit bằng CLA, anh/chị có vẽ một cổng AOI có 17 transistor nối tiếp để tính $C_{16}$ không? Nếu không thì làm thế nào?"* (Đáp: Không, vì $17$ transistor nối tiếp sẽ cực chậm; phải chia thành 4 khối CLA 4-bit dùng $P_G, G_G$ nối vào một khối CLG cấp 2).
