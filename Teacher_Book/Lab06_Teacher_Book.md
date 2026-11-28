# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 06 — TEACHER'S BOOK: MẠCH CỘNG TOÀN PHẦN 1-BIT (MIRROR ADDER 28T VÀ TG ADDER)
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-06-mach-cong-toan-phan-full-adder.md](../02%20-%20Student%20Workbook/lab-06-mach-cong-toan-phan-full-adder.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab06/](../03%20-%20Instructor_Solutions/lab06/)  
> **Script kiểm chứng số liệu:** [verify_lab06_new.py](../scripts/verify_lab06_new.py)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

### 6.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. **Hiểu chính xác giải phẫu Mirror Adder 28T:** Khối Carry có **5 NMOS + 5 PMOS + 2T Inverter = 12T**; khối Sum có **7 NMOS + 7 PMOS + 2T Inverter = 16T**; tổng chuẩn xác là **28 Transistors**. Mạng PDN thực hiện $Sum = A B C_{in} + \overline{C_{out}}(A+B+C_{in})$ nên ngõ ra tầng là $\overline{Sum}$ (bản cũ ghi nhầm vế trái là $\overline{Sum}$).
2. **Hiểu bản chất "Mirror" (tự đối ngẫu):** PUN và PDN của khối Carry dùng **cùng cấu trúc topo** $(A \cdot B) \parallel (C_{in} \cdot (A \parallel B))$, nhờ vậy cân bằng điện dung và dùng chung đường đi Euler 5 transistor (`B - A - Cin - A - B`).
3. **Hiểu thực tế đường tới hạn và đối sánh TG Adder:** Không có chuyện $C_{in} \to C_{out}$ luôn nhanh hơn $A \to Sum$ gấp $\ge 2$ lần (cả hai đều đi qua 2 tầng logic, riêng đường $C_{in} \to Sum$ đi qua $\overline{C_{out}} \to \overline{Sum} \to Sum$ còn chậm hơn $C_{in} \to C_{out}$!). Tầm quan trọng của $C_{in} \to C_{out}$ nằm ở **hệ số nhân $(N-1)$** trong bộ cộng $N$-bit RCA.

---

### 6.2 Phân tích Định cỡ, Điện dung ngõ vào $C_{in}$ và Kiểm chứng Biểu thức

Theo kết quả kiểm chứng từ `verify_lab06_new.py`:

| Khối chức năng | Số NMOS / PMOS | Kích thước $(W/L)_n$ | Kích thước $(W/L)_p$ | Tổng $\Sigma W$ ($\lambda$) | Tổng T |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Carry Logic ($\overline{C_{out}}$)** | $5\text{N} + 5\text{P}$ | $8\lambda / 2\lambda$ (2 nối tiếp) | $24\lambda / 2\lambda$ (2 nối tiếp) | $40 + 120 = 160\lambda$ | 10T |
| **Carry Inverter (`INV_Cout`)** | $1\text{N} + 1\text{P}$ | $4\lambda / 2\lambda$ | $12\lambda / 2\lambda$ | $4 + 12 = 16\lambda$ | 2T |
| **Sum Logic ($\overline{Sum}$)** | $7\text{N} + 7\text{P}$ | $12\lambda / 2\lambda$ (3 nối tiếp) | $36\lambda / 2\lambda$ (3 nối tiếp) | $84 + 252 = 336\lambda$ | 14T |
| **Sum Inverter (`INV_Sum`)** | $1\text{N} + 1\text{P}$ | $4\lambda / 2\lambda$ | $12\lambda / 2\lambda$ | $4 + 12 = 16\lambda$ | 2T |
| **TỔNG TOÀN MẠCH** | **$14\text{N} + 14\text{P}$** | — | — | **$528\lambda$ ($158,4\,\mu\text{m}$)** | **28T** |

**Điểm sư phạm quan trọng cho Ex6.4 (Chuỗi RCA):**
- Tổng bề rộng cổng nối vào chân $C_{in}$ của 1 Mirror Adder là:
  $$W_{Cin} = (8\lambda + 24\lambda)_{\text{Carry}} + (12\lambda + 36\lambda)_{\text{Sum,nối tiếp}} + (12\lambda + 36\lambda)_{\text{Sum,song song}} = \mathbf{128\lambda}$$
- Giá trị này lớn gấp **$8$ lần** bề rộng cổng của một Inverter chuẩn `inv_x1` ($16\lambda$). Với giả định $C_{ox} \approx 2,5\,\text{fF}/\mu\text{m}^2$, $C_{in}$ thực của một tầng Mirror Adder vào khoảng **$\approx 58\,\text{fF}$** (cộng thêm tụ dây nối), tức gần tương đương hoặc lớn hơn tải $C_L = 50\,\text{fF}$ khi đo đơn lẻ!

---

### 6.3 Kiến trúc TG Adder trong `tg_adder_tran.sp` (22T vs 16T)
- **Đính chính lỗi cũ:** Bản cũ liệt kê "XOR 6T/4T + XOR 4T + MUX 4T = 16T" là không cộng ra 16T. Trong tệp Netlist thực tế `03 - Instructor_Solutions/lab06/tg_adder_tran.sp`, `xor_tg` dùng 2 Inverter + 2 TG ($8\text{T}$), nên:
  `X_xor1` ($8\text{T}$) + `X_inv_p` ($2\text{T}$) + `X_xor2` ($8\text{T}$) + `MUX2_C` ($4\text{T}$) = **22 Transistors**.
- Giảng viên giải thích rõ: 22T là dạng lắp ghép trực tiếp theo module chuẩn; nếu tối ưu chia sẻ tín hiệu đảo nội bộ có thể rút gọn xuống 16T.

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN

### 6.4 Kế hoạch Buổi học 135 Phút & Điều phối Phòng máy
- **00–10':** Cổng kiểm tra Pre-lab. Rà nhanh bảng kích thước 28T và công thức $T_{Cout3}, T_{Sum3}$.
- **10–40' (Ex6.1):** Dựng `mirror_adder_1b{sch}`. Phát khung khối Carry dựng sẵn để sinh viên tập trung hoàn thiện khối Sum (7N+7P+2T) và nối đúng dây `cob`.
- **40–55' (Ex6.2):** Mô phỏng 8 tổ hợp bằng `.tran 0 80n 0 1p` và `.meas FIND` tại `5n, 15n, ..., 75n`. Nhắc trước về glitch ở bước `011 -> 100` để sinh viên không hoang mang.
- **55–80' (Ex6.3):** Đo 4 đường trễ và thực hiện thí nghiệm đảo vị trí $C_{in}$ (sát `cob` vs sát rail `vdd`/`gnd`).
- **80–100' (Ex6.4):** Ghép chuỗi $N=1\dots 4$ RCA, đo $t_{chain}(N)$ và so sánh độ dốc với trễ đơn lẻ.
- **100–125' (Ex6.5):** Dựng và đo `tg_adder_1b` (22T) dưới cùng điều kiện lái `inv_x1` và tải $C_L = 50\,\text{fF}$.
- **125–135':** Tổng kết và nghiệm thu tại bàn.

---

### 6.5 Đáp án Chi tiết Pre-lab

1. **Chứng minh biểu thức Sum:** Kiểm tra đủ 8 tổ hợp (xem bảng trong `verify_lab06_new.py`), xác nhận $Sum = A B C_{in} + \overline{C_{out}}(A+B+C_{in})$ trùng khớp hoàn toàn.
2. **Bảng kích thước 28T & $W_{Cin}$:** Như Bảng ở Mục 6.2 ($28\text{T}$, $W_{Cin} = 128\lambda = 8 \times \text{inv\_x1}$).
3. **Biểu thức trễ 4-bit RCA:**
   - Tới $C_{out,3}$: $T_{Cout3} = t_{pd(A,B \to Cout,0)} + 3 \cdot t_{pd(Cin \to Cout)}$ (tổng **4 tầng** carry nếu tính từ $C_{in,0}$).
   - Tới $Sum_3$: $T_{Sum3} = t_{pd(A,B \to Cout,0)} + 2 \cdot t_{pd(Cin \to Cout)} + t_{pd(Cin \to Sum,3)}$ (**3 tầng** carry + **1 tầng** sum).
4. **Đường Euler 5 transistor khối Carry:**
   - Đồ thị PDN Carry có các nút: `out` (bậc 2), `n1` (nối $A\cdot B$, bậc 2), `n2` (nối $C_{in}$ với $A \parallel B$, bậc 3), `gnd` (bậc 3).
   - Vì có 2 đỉnh bậc lẻ (`gnd` và `n2`), đường Euler hợp lệ là dãy **5 cổng**: **`B - A - Cin - A - B`** (dùng chung cho cả PDN và PUN nhờ tính tự đối ngẫu).

---

### 6.6 Bảng Đối Chuẩn Kỹ Thuật Tham Chiếu (MOSIS C5N, $C_L = 50\,\text{fF}$)

| Hạng mục đo kiểm | Giá trị kỳ vọng (Suy dẫn / Tham chiếu) | Ghi chú |
| :--- | :---: | :--- |
| Số lượng Transistor | Mirror Adder: $28\text{T}$; TG Adder: $22\text{T}$ | |
| Ước lượng thô $t_{pd(Cin \to Cout)}$ (Mirror Adder) | $\approx 60 - 80\,\text{ps}$ | Tùy sườn bộ lái và tụ ký sinh nút `cob` |
| Đường chậm nhất của Mirror Adder | $C_{in} \to Sum$ (qua `cob` $\to$ `sb` $\to$ `sum`) | Chậm hơn $C_{in} \to C_{out}$ |
| Đảo vị trí $C_{in}$ (sát `cob` vs sát rail) | Đặt sát `cob` nhanh hơn | Lợi ích phụ thuộc vào tổ hợp $(A,B)$ |
| Chuỗi 4-bit RCA Mirror Adder ($N=1\dots 4$) | Tuyến tính $O(N)$ | Độ dốc phản ánh tải $C_{in} \approx 58\,\text{fF}$ |
| Chuỗi 4-bit TG Adder không đệm ($N=1\dots 4$) | Tỉ lệ Elmore $1 : 3 : 6 : 10$ ($O(N^2)$) | Chậm hơn Mirror Adder khi $N \ge 4$ |

---

### 6.7 Kịch bản Gỡ lỗi Socratic cho Giảng viên (4 tình huống điển hình)

1. **Sinh viên báo: *"Thầy ơi, ở thời điểm $t = 40\,\text{ns}$ (khi $A, B, C_{in}$ chuyển từ `011` sang `100`), ngõ ra `Sum` của em có một gai nhọn vọt lên rồi mới rớt xuống 0!"***
   - *Gợi ý Socratic:* "Em hãy kiểm tra xem tại $40\,\text{ns}$ có mấy ngõ vào đổi trạng thái cùng lúc? Vì khối `Sum` dùng tín hiệu `cob` đi ra từ khối `Carry`, vậy `cob` có kịp ổn định trước khi các transistor $A, B, C_{in}$ trong khối `Sum` chuyển mạch không?" $\implies$ Sinh viên hiểu bản chất tĩnh của glitch tổ hợp và lý do phải lấy mẫu cuối chu kỳ bằng `.meas FIND`.

2. **Sinh viên thắc mắc: *"Tại sao khi em đo $t_{pd(A \to Sum)}$ ở $B=0, C_{in}=0$ thì khá nhanh, nhưng khi đo $C_{in} \to Sum$ ở $A=1, B=0$ lại chậm hơn hẳn?"***
   - *Gợi ý Socratic:* "Ở trường hợp $A=1, B=0$, khi $C_{in}$ đổi từ $0 \to 1$, giá trị $C_{out}$ (và nút `cob`) có đổi theo không? Vậy tín hiệu phải đi qua mấy tầng cổng trước khi tới được `Sum`?" $\implies$ Sinh viên nhận ra đường $C_{in} \to \text{cob} \to \text{sb} \to Sum$ là đường dài nhất.

3. **Sinh viên báo: *"Em đo $t_{pd(Cin \to Cout)}$ mà phần mềm báo `Measurement FAILED`, trong khi 8 tổ hợp vẫn chạy đúng!"***
   - *Gợi ý Socratic:* "Trong phép đo đó em đang đặt hai chân $A$ và $B$ ở mức nào? Nếu $A=B=0$ hoặc $A=B=1$ thì $C_{out}$ có phụ thuộc vào $C_{in}$ nữa không?" $\implies$ Sinh viên nhớ ra điều kiện truyền số nhớ $P = A \oplus B = 1$.

4. **Sinh viên hỏi: *"Tại sao trong chuỗi 4-bit RCA, độ dốc tăng thêm cho mỗi tầng lại lớn hơn một chút so với trễ đo đơn lẻ với $C_L = 50\,\text{fF}$?"***
   - *Gợi ý Socratic:* "Em thử cộng lại tổng bề rộng cổng $W$ nối vào chân $C_{in}$ ở Pre-lab xem nó gấp mấy lần một Inverter chuẩn `inv_x1`? Điện dung thực tế mà `Cout` của tầng trước phải kéo là bao nhiêu?" $\implies$ Sinh viên liên hệ được $W_{Cin} = 128\lambda \implies C_{in} \approx 58\,\text{fF}$.

---

### 6.8 Đáp án Chi tiết Câu hỏi Thảo luận Post-lab

1. **Câu 1 (Vị trí $C_{in}$ sát nút `cob`):** Khi $A$ và $B$ đến trước (ví dụ $A=1, B=0$ hoặc $A=0, B=1$), các nút nội nằm giữa đường nguồn/đất và transistor $C_{in}$ đã được nạp/xả sẵn. Khi đặt $C_{in}$ sát nút `cob`, lúc $C_{in}$ nhảy mức, dòng điện chỉ nạp/xả trực tiếp tụ nút `cob` mà không phải nạp/xả thêm điện dung các nút nội trung gian.
2. **Câu 2 (So sánh độ dốc RCA với đo đơn lẻ $C_L = 50\,\text{fF}$):** Bên trong chuỗi RCA thật, tải của ngõ ra $C_{out}$ là cực cổng $C_{in}$ của tầng tiếp theo ($W_{Cin} = 128\lambda \implies C_{in} \approx 58\,\text{fF}$, lớn hơn tải $50\,\text{fF}$) đồng thời sườn xung kích thích là sườn thực tế từ tầng trước (chậm hơn nguồn xung $0,1\,\text{ns}$ lý tưởng), khiến độ trễ mỗi tầng thực tế lớn hơn so với phép đo đơn lẻ.
3. **Câu 3 (Mở rộng 32-bit & Kiến trúc tốc độ cao):** Với 32-bit RCA, trễ tăng tuyến tính gấp $\approx 31$ tầng carry. Để phá vỡ giới hạn tuyến tính $O(N)$ này, kỹ sư dùng **Carry-Lookahead Adder (CLA)** (tính trước các tín hiệu Generate $G$ và Propagate $P$ để tạo số nhớ song song trong thời gian $O(\log N)$) hoặc **Carry-Select Adder** (tính song song hai trường hợp $C_{in}=0$ và $C_{in}=1$ rồi chọn bằng MUX).

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & BỘ CÂU HỎI VẤN ĐÁP TẠI BÀN

### 6.9 Barem chấm điểm nhanh tại bàn (Thang 10)
- **Pre-lab (2,0 điểm):** Chứng minh đúng hàm Sum, đếm đủ 28T, định cỡ hợp lý $W_n/W_p$, tính đúng $W_{Cin} = 128\lambda$ và công thức 4-bit RCA.
- **Ex6.1–6.2 (2,0 điểm):** Schematic `mirror_adder_1b` đủ 28T, 0 lỗi `F5`, kiểm chứng 8/8 trạng thái bằng `.meas FIND`.
- **Ex6.3 (2,0 điểm):** Đo đủ 4 đường trễ, giải thích đúng đường chậm nhất ($C_{in} \to Sum$), hoàn thành thí nghiệm đảo vị trí $C_{in}$.
- **Ex6.4–6.5 (2,5 điểm):** Đo đủ chuỗi RCA $N=1\dots 4$, vẽ đồ thị $O(N)$, dựng và đo đối sánh công bằng `tg_adder_1b` (22T).
- **Báo cáo & Vấn đáp (1,5 điểm):** Đầy đủ số liệu khớp `.log`, trả lời chính xác câu hỏi thảo luận.

### 6.10 Bộ câu hỏi vấn đáp nhanh tại bàn (3 câu chọn lọc)
1. *"Tại sao hàm của khối Sum trong Mirror Adder lại lấy đầu vào từ nút `cob` ($\overline{C_{out}}$) chứ không lấy từ ngõ ra cuối `cout`?"* (Đáp: Vì sử dụng trực tiếp $\overline{C_{out}}$ giúp tiết kiệm 1 tầng trễ Inverter trên đường Sum và giữ đúng phương trình $Sum = ABC_{in} + \overline{C_{out}}(A+B+C_{in})$).
2. *"Vì sao khi đếm số transistor ở bản cũ ra 24T thì mạch Mirror Adder lại bị sai chức năng?"* (Đáp: Carry có 5 nhánh chứ không phải 4, Sum có 7 nhánh chứ không phải 6; thiếu transistor nghĩa là thiếu đường kéo lên/xuống cho một số tổ hợp logic).
3. *"Nếu thay bộ cộng Mirror Adder trong chuỗi 4-bit RCA bằng TG Full Adder không có bộ đệm ở đường carry, tại sao mạch lại chậm đi nhanh chóng khi tăng số bit?"* (Đáp: Vì chuỗi các TG không đệm tạo thành mạng $RC$ phân bố có trễ tăng theo $O(N^2)$ thay vì tuyến tính $O(N)$).
