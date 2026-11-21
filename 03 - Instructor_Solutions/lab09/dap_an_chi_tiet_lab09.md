# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 9 (LAB 09)
# THIẾT KẾ ĐƯỜNG DỮ LIỆU KHỐI CỘNG NHANH 4-BIT (4-BIT CARRY LOOKAHEAD ADDER - CLA)
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Hạn Chế Nút Thắt Cổ Chai Của RCA và Triết Lý Thiết Kế CLA

Trong Bài 6, chúng ta đã nghiên cứu Mạch cộng toàn phần (Full Adder) và bộ cộng gợn sóng (Ripple Carry Adder - RCA):
- **Nút thắt cổ chai của RCA:** Số nhớ $C_{out,i}$ của tầng thứ $i$ phụ thuộc trực tiếp vào số nhớ $C_{in,i}$ từ tầng $i-1$. Tín hiệu số nhớ phải gợn từng bước tuần tự qua chuỗi $N$ tế bào, dẫn đến thời gian trễ tăng tuyến tính theo kích thước từ dữ liệu:
  $$T_{RCA} = O(N)$$
  Khi mở rộng lên $32$-bit hay $64$-bit, trễ lan truyền số nhớ chiếm hơn **$85\%$ tổng thời gian trễ** của toàn bộ khối tính toán ALU.
- **Triết lý đột phá của Carry Lookahead Adder (CLA):**
  * Thay vì đợi số nhớ lan truyền tuần tự qua từng bit, CLA **tính toán trước đồng thời toàn bộ các bit số nhớ ($C_1, C_2, C_3, C_4$)** trực tiếp từ hai toán hạng đầu vào $A[3:0], B[3:0]$ và số nhớ đầu tiên $C_0$.
  * Toàn bộ các bit số nhớ được tạo ra song song chỉ sau **$2$ tầng trễ cổng logic**, biến độ phức tạp thời gian từ $O(N)$ trở thành xấp xỉ hằng số $O(1)$!

---

### 2. Dẫn Xuất Đại Số & Hệ Phương Trình Số Nhớ Đệ Quy

Xét một bit cộng thứ $i$ bất kỳ với hai ngõ vào $A_i$ và $B_i$:
1. **Cờ Sinh số nhớ (Generate - $G_i$):**
   $$G_i = A_i \cdot B_i$$
   Khi cả hai bit $A_i = B_i = 1$, một số nhớ chắc chắn được sinh ra tại tầng $i$ bất chấp số nhớ ngõ vào $C_i$ bằng $0$ hay $1$.
2. **Cờ Truyền số nhớ (Propagate - $P_i$):**
   $$P_i = A_i \oplus B_i \quad (\text{hoặc } P_i = A_i + B_i)$$
   Khi có đúng một bit bằng $1$, nếu có số nhớ $C_i = 1$ đi vào thì số nhớ này sẽ được truyền xuyên qua tầng $i$ để đi tiếp tới tầng $i+1$.  
   *(Trong thiết kế này, ta chọn $P_i = A_i \oplus B_i$ để tái sử dụng ngay tín hiệu $P_i$ cho việc tạo tổng $S_i = P_i \oplus C_i$, tiết kiệm diện tích silicon).*

#### Khai triển đệ quy hệ phương trình Carry Lookahead:
- Bit số nhớ thứ nhất:
  $$C_1 = G_0 + P_0 C_0$$
- Bit số nhớ thứ hai (thế $C_1$ vào):
  $$C_2 = G_1 + P_1 C_1 = G_1 + P_1 (G_0 + P_0 C_0) = G_1 + P_1 G_0 + P_1 P_0 C_0$$
- Bit số nhớ thứ ba (thế $C_2$ vào):
  $$C_3 = G_2 + P_2 C_2 = G_2 + P_2 G_1 + P_2 P_1 G_0 + P_2 P_1 P_0 C_0$$
- Bit số nhớ thứ tư (thế $C_3$ vào):
  $$C_4 = G_3 + P_3 G_2 + P_3 P_2 G_1 + P_3 P_2 P_1 G_0 + P_3 P_2 P_1 P_0 C_0$$

#### Tính toán Tổng Sum:
$$S_i = P_i \oplus C_i = A_i \oplus B_i \oplus C_i \quad (i = 0, 1, 2, 3)$$

---

### 3. Hiện Thực Mức Transistor: Cổng Phức Hợp AOI và Thách Thức Fan-in

Mỗi phương trình số nhớ $C_i$ có dạng tổng của các tích (Sum of Products), được hiện thực cực kỳ nhỏ gọn bằng cổng phức hợp **AOI (AND-OR-Invert)** kết hợp với một Inverter đệm:
- $C_1$: Cổng AOI21 + Inverter.
- $C_2$: Cổng AOI321 + Inverter.
- $C_3$: Cổng AOI4321 + Inverter.
- $C_4$: Cổng AOI54321 + Inverter.

#### Thách thức Vật lý về Giới hạn Fan-in (Fan-in Limitation):
- Nhánh dài nhất của phương trình $C_4$ ($P_3 P_2 P_1 P_0 C_0$) yêu cầu **$5$ transistor NMOS mắc nối tiếp** trong mạng kéo xuống PDN.
- Khi số lượng transistor nối tiếp tăng lên:
  * Điện trở kênh dẫn cộng dồn: $R_{eq} \approx 5 \cdot R_n$.
  * Điện dung ký sinh tại các nút nội trung gian tăng tuyến tính: $C_{int} \approx 4 \cdot C_{diff}$.
  * Trễ chuyển mạch Elmore tăng theo hàm bậc hai: $\tau \approx R C + 2 R C + \dots + 5 R C = 15 R C$.
- $\implies$ **Quy tắc thiết kế công nghiệp:** Trong công nghệ CMOS tiêu chuẩn, kích thước tối đa của một khối CLA đơn tầng thường **không vượt quá 4-bit** ($Fan\text{-}in \le 5$). Để xây dựng các bộ cộng $16$-bit hay $64$-bit, kỹ sư bắt buộc phải ghép phân tầng (Hierarchical Block CLA hoặc dùng cấu trúc cây song song Kogge-Stone / Brent-Kung).

---

### 4. Phân Tích Đánh Đổi Phần Cứng (PPA Trade-off)

| Tiêu chí | 4-bit Ripple Carry Adder (RCA) | 4-bit Carry Lookahead Adder (CLA) | Đánh giá so sánh |
| :--- | :---: | :---: | :--- |
| **Tổng số Transistor** | $112\,\text{T}$ ($4 \times 28\,\text{T}$) | **$134\,\text{T}$** ($48\,\text{T}_{PG} + 62\,\text{T}_{CLG} + 24\,\text{T}_{Sum}$) | CLA tốn thêm **$+19.6\%$** diện tích |
| **Trễ lan truyền Carry ($C_0 \to C_4$)** | $282.0\,\text{ps}$ (4 tầng nối tiếp) | **$175.0\,\text{ps}$** (Tính song song 2 tầng) | **CLA nhanh hơn $1.61\times$ ($+61\%$)** |
| **Trễ đường tới hạn ($A/B \to S_3$)** | $355.0\,\text{ps}$ | **$230.0\,\text{ps}$** | **CLA nhanh hơn $1.54\times$ ($+54\%$)** |
| **Độ phức tạp trễ lý thuyết** | $O(N)$ (Tuyến tính) | **$O(1)$** (Hằng số ở cấp khối 4-bit) | Vượt trội hoàn toàn khi mở rộng bit |

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Bảng Chân Trị và Kiểm Chứng Số Học 4-bit CLA (`cla_4bit_tran.sp`)

*(MOSIS C5N 0.5µm, $V_{DD} = 5.0\,\text{V}$, tải ngõ ra $C_L = 30\,\text{fF}$ cho Sum, $C_{L,C4} = 50\,\text{fF}$)*

| Trường hợp | Toán hạng $A[3:0]$ | Toán hạng $B[3:0]$ | $C_0$ | Tổng $Sum[3:0]$ | $C_4$ | Phép tính thực thi | Đánh giá |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **1** | `0000` ($0$) | `0000` ($0$) | 0 | **`0000` ($0$)** | **0** | $0 + 0 + 0 = 0$ | PASS |
| **2** | `0101` ($5$) | `0011` ($3$) | 0 | **`1000` ($8$)** | **0** | $5 + 3 + 0 = 8$ (Không tràn) | PASS |
| **3** | `1001` ($9$) | `0110` ($6$) | 0 | **`1111` ($15$)** | **0** | $9 + 6 + 0 = 15$ (Cận tràn) | PASS |
| **4** | `1100` ($12$) | `0111` ($7$) | 0 | **`0011` ($3$)** | **1** | $12 + 7 + 0 = 19 = 16 + 3$ | PASS |
| **5** | **`1111` ($15$)** | **`0000` ($0$)** | **$0 \to 1$** | **`0000` ($0$)** | **1** | **$15 + 0 + 1 = 16$ (Worst Case)**| **PASS** |
| **6** | `1111` ($15$) | `1111` ($15$) | 1 | **`1111` ($15$)** | **1** | $15 + 15 + 1 = 31 = 16 + 15$ | PASS |

---

### 2. Kết Quả Đối Sánh Trực Tiếp 4-bit CLA vs 4-bit RCA (`cla_vs_rca_benchmark.sp`)

*(Đo đạc trong trường hợp xấu nhất: $A = 1111_2, B = 0000_2, C_0$ nhảy từ $0 \to 1$)*

| Thông số đo đạc | 4-bit RCA (Mirror Adder) | 4-bit CLA (Carry Lookahead) | Tỉ số cải thiện (Speedup) |
| :--- | :---: | :---: | :---: |
| **Trễ lan truyền số nhớ $t_{pd(C0 \to C4)}$** | **$282.0\,\text{ps}$** | **$175.0\,\text{ps}$** | **$1.61\times$ (Nhanh hơn $61\%$)** |
| **Trễ đường tới hạn $t_{pd(C0 \to S3)}$** | **$355.0\,\text{ps}$** | **$230.0\,\text{ps}$** | **$1.54\times$ (Nhanh hơn $54\%$)** |
| **Công suất tiêu tán trung bình ($100\,\text{MHz}$)** | $0.215\,\text{mW}$ | $0.258\,\text{mW}$ | Tăng $+20\%$ do thêm logic CLG |

---

### 3. Kết Quả Đo Đạc Độc Lập Khối CLG (`clg_unit_tran.sp`)

| Đường tín hiệu số nhớ | Biểu thức logic | Số transistor nối tiếp max | Thời gian trễ $t_{pd}$ từ $C_0$ |
| :---: | :--- | :---: | :---: |
| **$C_1$** | $G_0 + P_0 C_0$ | 2 NMOS | **$72.4\,\text{ps}$** |
| **$C_2$** | $G_1 + P_1 G_0 + P_1 P_0 C_0$ | 3 NMOS | **$88.5\,\text{ps}$** |
| **$C_3$** | $G_2 + P_2 G_1 + P_2 P_1 G_0 + P_2 P_1 P_0 C_0$ | 4 NMOS | **$102.1\,\text{ps}$** |
| **$C_4$** | $G_3 + P_3 G_2 + \dots + P_3 P_2 P_1 P_0 C_0$ | 5 NMOS | **$110.0\,\text{ps}$** |

*Nhận xét:* Dù $C_4$ có tới 5 transistor nối tiếp nhưng nhờ định cỡ $W_{PMOS} = 7.2\,\mu\text{m}$ và $W_{NMOS} = 2.4\,\mu\text{m}$, trễ của $C_4$ chỉ chênh lệch rất nhỏ so với $C_3$ ($110\,\text{ps}$ vs $102\,\text{ps}$), bảo đảm tính đồng bộ cao.

---

### 4. Kết Quả Trích Xuất Ký Sinh Post-Layout PEX (`cla_pex_postlayout.sp`)

| Thông số kiểm tra | Pre-layout (Lý thuyết) | Post-layout (PEX) | Tỉ lệ suy giảm |
| :--- | :---: | :---: | :---: |
| **Trễ số nhớ $t_{pd(C0 \to C4)}$** | $175.0\,\text{ps}$ | **$208.5\,\text{ps}$** | $+19.1\%$ (Do ký sinh Metal1/Metal2 nối dài) |
| **Trễ đường tới hạn $t_{pd(C0 \to S3)}$** | $230.0\,\text{ps}$ | **$268.0\,\text{ps}$** | $+16.5\%$ |
| **Tốc độ so với RCA Post-layout** | $1.61\times$ | **$1.58\times$** | **Vẫn vượt trội gần $60\%$ sau khi layout** |

---

## PHẦN III: HƯỚNG DẪN CHẤM VÀ CÂU HỎI VẤN ĐÁP TẠI BÀN (VIVA QUESTIONS)

### 1. Barem Điểm Chi Tiết (Thang điểm 10)

| Tiêu chí | Nội dung đánh giá | Điểm tối đa |
| :--- | :--- | :---: |
| **Chuẩn bị Pre-lab** | Khai triển phương trình $C_1 - C_4$, tính toán bảng chân trị và viết netlist | **2.0 điểm** |
| **Mô phỏng SPICE In-lab** | Chạy mô phỏng CLA, đo trễ so sánh trực tiếp với RCA, đo độc lập CLG | **3.0 điểm** |
| **Layout & DRC/LVS** | Mask layout phân cấp khối `cla_adder_4b`, đi dây 2 tầng kim loại, DRC 0 lỗi, LVS matching 100% | **3.0 điểm** |
| **Báo cáo & Vấn đáp tại bàn** | Điền số liệu đầy đủ, giải thích sâu sắc sự đánh đổi diện tích và tốc độ | **2.0 điểm** |
| **Tổng cộng** | **Đạt chuẩn đầu ra môn học CLO2 - CLO4** | **10.0 điểm** |

---

### 2. Các Bẫy Kỹ Thuật Học Sinh Hay Mắc Phải Khi Thực Hành

1. **Nhầm lẫn cờ $P_i$ giữa phép OR và phép XOR:** Nếu dùng $P_i = A_i + B_i$ thì đúng cho khối số nhớ nhưng không dùng trực tiếp để tính $S_i$ được. Sinh viên phải phân biệt rõ: chọn $P_i = A_i \oplus B_i$ cho phép dùng chung $P_i$ cho cả CLG và Sum unit.
2. **Quên đảo pha ngõ ra của cổng AOI:** Cổng AOI tự nhiên có chức năng đảo (Invert: $\overline{C_i}$). Sinh viên thường quên mắc thêm Inverter đệm để tạo ra tín hiệu $C_i$ tích cực mức cao, dẫn đến số nhớ bị đảo bit sai toàn bộ.
3. **Hiện tượng suy giảm sườn xung ở nhánh $C_4$:** Do nhánh $C_4$ có 5 NMOS nối tiếp, nếu sinh viên giữ nguyên kích thước tối thiểu ($W = 1.2\,\mu\text{m}$) thì sườn xả bị kéo dài nghiêm trọng ($t_{fall} > 400\,\text{ps}$). Phải tăng kích thước NMOS trong chuỗi lên ít nhất $W = 2.4\,\mu\text{m}$.
4. **Xung đột lớp kim loại trong Layout:** Khối CLA có mật độ dây nối giữa PG, CLG và Sum rất dày đặc. Sinh viên đi dây tùy tiện trên cùng một lớp Metal1 sẽ bị chạm chập hoặc vi phạm luật DRC `Metal spacing`. Phải tuân thủ quy tắc: **Metal 1 đi ngang, Metal 2 đi dọc** (Manhattan Routing).

---

### 3. Ngân Hàng Câu Hỏi Vấn Đáp Tại Bàn (Viva Questions)

**Câu 1: Phân tích sự khác biệt bản chất giữa Bộ cộng gợn sóng (RCA) và Bộ cộng nhanh (CLA) về mặt độ phức tạp thời gian trễ?**  
*Đáp án chuẩn:* Trong RCA, bit số nhớ lan truyền tuần tự qua từng tế bào Full Adder nên thời gian trễ tăng tuyến tính theo số bit $T_{RCA} = O(N)$. Trong CLA, các bit số nhớ được tính toán song song trực tiếp từ các toán hạng đầu vào qua các phương trình đại số của khối CLG, do đó thời gian sinh số nhớ chỉ qua 2 tầng cổng logic, đạt độ phức tạp hằng số $T_{CLA} = O(1)$ ở cấp độ khối 4-bit, giúp tăng tốc độ xử lý lên gần gấp đôi.

**Câu 2: Tại sao trong công nghiệp người ta không thiết kế một khối CLA 16-bit hay 32-bit nguyên khối mà chỉ dừng lại ở khối 4-bit?**  
*Đáp án chuẩn:* Vì giới hạn Fan-in trong công nghệ CMOS. Phương trình số nhớ của bit thứ $N$ đòi hỏi nhánh dài nhất phải có $N+1$ transistor mắc nối tiếp. Khi $N > 4$, điện trở kênh dẫn tăng tỉ lệ thuận và điện dung nút nội tăng khiến trễ Elmore tăng theo hàm bậc hai ($O(N^2)$), làm triệt tiêu hoàn toàn ưu thế tốc độ của CLA. Do đó người ta chỉ làm khối CLA 4-bit, sau đó ghép nối phân tầng (Hierarchical CLA).

**Câu 3: Ý nghĩa vật lý của hai tín hiệu cờ $G_i$ (Generate) và $P_i$ (Propagate) là gì?**  
*Đáp án chuẩn:* $G_i = A_i \cdot B_i$ (Cờ sinh) biểu thị tầng thứ $i$ tự sản sinh ra một số nhớ mang đi bất chấp số nhớ đầu vào $C_i$. $P_i = A_i \oplus B_i$ (Cờ truyền) biểu thị tầng thứ $i$ không tự sinh ra số nhớ nhưng sẽ truyền nguyên vẹn số nhớ đầu vào $C_i$ xuyên qua nó để chuyển tiếp lên tầng $i+1$.

**Câu 4: Trình bày sự đánh đổi phần cứng (Hardware Trade-off) giữa 4-bit CLA và 4-bit RCA?**  
*Đáp án chuẩn:* 4-bit CLA tốn $134$ transistor so với $112$ transistor của 4-bit RCA (tăng $19.6\%$ diện tích silicon và tăng nhẹ công suất tiêu tán) để đổi lấy thời gian lan truyền số nhớ nhanh hơn $61\%$ ($175\,\text{ps}$ so với $282\,\text{ps}$) và trễ tổng thể nhanh hơn $54\%$. Đây là sự đánh đổi cực kỳ kinh tế và bắt buộc trong các vi xử lý hiệu năng cao.

**Câu 5: Trong thiết kế Mask Layout của khối CLA 4-bit, phương pháp định tuyến nào được áp dụng để tránh chạm chập giữa các khối PG, CLG và Sum?**  
*Đáp án chuẩn:* Áp dụng phương pháp định tuyến trực giao Manhattan (Orthogonal Routing): Toàn bộ các đường tín hiệu dữ liệu và bus số nhớ chạy theo phương ngang được định tuyến bằng lớp Metal 1, trong khi các đường phân phối xung nhịp, nguồn và tín hiệu điều khiển chạy theo phương dọc được định tuyến bằng lớp Metal 2, kết nối xuyên tầng bằng Via1.
