# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 06 — TEACHER'S BOOK: THIẾT KẾ MẠCH CỘNG TOÀN PHẦN 1-BIT (1-BIT FULL ADDER)
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-06-mach-cong-toan-phan-full-adder.md](../02%20-%20Giao_Trinh_Lab_Handouts/lab-06-mach-cong-toan-phan-full-adder.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab06/](../03%20-%20Instructor_Solutions/lab06/)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

# 6. LAB 6 — MẠCH CỘNG TOÀN PHẦN (1-BIT FULL ADDER) (CHƯƠNG 6)

## 6.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Hiểu sâu kiến trúc vi mạch số: $Sum$ là hàm XOR 3 ngõ vào đối xứng, trong khi $C_{out}$ là hàm đa số (Majority function - bằng 1 khi có từ 2 ngõ vào trở lên bằng 1).
2. Hiểu vì sao kiến trúc Mirror Adder 28T thống trị các thư viện chuẩn ASIC: tính tự đối ngẫu giúp PDN và PUN có cấu trúc topo giống hệt nhau, và việc tái sử dụng $\overline{C_{out}}$ để tạo $Sum$ giúp tiết kiệm tối đa số lượng transistor.
3. Nhận thức rõ ràng: Tốc độ của bộ cộng gợn sóng $N$-bit (Ripple Carry Adder) bị khống chế tuyệt đối bởi trễ lan truyền số nhớ $C_{in} \to C_{out}$, không phải trễ $Sum$.

---

## 6.2 Phân tích giải phẫu Mirror Adder 28T
Phương trình chuẩn hóa:
$$C_{out} = A \cdot B + C_{in} \cdot (A + B)$$
$$\overline{C_{out}} = \overline{A \cdot B + C_{in} \cdot (A + B)}$$
$$Sum = A \cdot B \cdot C_{in} + \overline{C_{out}} \cdot (A + B + C_{in})$$

```
                   MIRROR ADDER 28T TOPOLOGY
      [CARRY BLOCK: 10T]                  [SUM BLOCK: 14T]
          VDD (5.0V)                          VDD (5.0V)
              |                                   |
      +-------+-------+                   +-------+-------+
      | PUN: 5 PMOS   |                   | PUN: 7 PMOS   |
      | Đối ngẫu Carry|                   | 3 PMOS // C_B |
      +-------+-------+                   +-------+-------+
              |                                   |
              +--------- C_out_B                  +--------- Sum_B
              |                                   |
      +-------+-------+                   +-------+-------+
      | PDN: 5 NMOS   |                   | PDN: 7 NMOS   |
      | A.B + Cin(A+B)|                   | 3 NMOS // C_B |
      +-------+-------+                   +-------+-------+
              |                                   |
             GND                                 GND
              |                                   |
        [INV C: 2T]                         [INV S: 2T]
              |                                   |
            C_out                                Sum
```

*Sơ đồ mạch chi tiết Mirror Adder và Transmission Gate Adder:*
- [mirror_adder_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Giao_Trinh_Lab_Handouts/images/mirror_adder_schematic.png)
- [tg_adder_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Giao_Trinh_Lab_Handouts/images/tg_adder_schematic.png)

### Bảng kiểm kê và sửa lỗi Handout về số lượng Transistor
| Khối chức năng vi mạch | Số Transistor thực tế | Handout cũ ghi nhầm | Phân tích giải phẫu kỹ thuật |
| :--- | :---: | :---: | :--- |
| **Khối tạo số nhớ $\overline{C_{out}}$** | **10T** ($5\text{P} + 5\text{N}$) | "4 NMOS + 4 PMOS" | Nhánh $A \cdot B$ tốn 2T; nhánh $C_{in}(A+B)$ tốn 3T $\implies 5\text{T}$ mỗi mạng. |
| **Bộ đệm Inverter cho $C_{out}$** | **2T** ($1\text{P} + 1\text{N}$) | Bỏ quên | Khôi phục cực tính và tăng cường khả năng lái cho tầng sau. |
| **Khối tạo tổng $\overline{Sum}$** | **14T** ($7\text{P} + 7\text{N}$) | Không tách bạch | Nhánh $A \cdot B \cdot C_{in}$ tốn 3T; nhánh $\overline{C_{out}}(A+B+C_{in})$ tốn 4T $\implies 7\text{T}$ mỗi mạng. |
| **Bộ đệm Inverter cho $Sum$** | **2T** ($1\text{P} + 1\text{N}$) | Bỏ quên | Cần thiết để lật cực tính từ $\overline{Sum} \to Sum$. |
| **TỔNG TOÀN TẾ BÀO FA** | **28T** | "24 đến 28T" | Con số chuẩn xác duy nhất là **28 Transistors**. |

---


---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN SPICE BENCHMARK

# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 6 (LAB 06)
# THIẾT KẾ MẠCH CỘNG TOÀN PHẦN 1-BIT (1-BIT FULL ADDER)
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Phân Tích Đường Trễ Tới Hạn (Critical Path) Trong Bộ Cộng Số Học

Trong một bộ xử lý số (ALU / DSP Processor), phép cộng là phép tính nền tảng nhất (chiếm trên $70\%$ khối lượng tính toán).  
Khi xây dựng bộ cộng $N$-bit dạng gợn sóng (Ripple Carry Adder - RCA) ghép từ $N$ tế bào Full Adder:
- Dữ liệu hai toán hạng $A[N-1:0]$ và $B[N-1:0]$ có sẵn tại cùng một thời điểm đầu chu kỳ ($t = 0$).
- Tuy nhiên, bit số nhớ $C_{in,i}$ của tầng thứ $i$ bắt buộc phải chờ số nhớ $C_{out,i-1}$ của tầng $i-1$ hoàn thành chuyển mạch thì mới bắt đầu tính toán được.
- Tổng thời gian trễ thực thi của bộ cộng $N$-bit:

  $$T_{add} = t_{pd(A,B \to C_{out,0})} + (N - 2) \cdot t_{pd(C_{in} \to C_{out})} + t_{pd(C_{in} \to Sum_{N-1})}$$

  Trong đó:
  * $t_{pd(A,B \to C_{out,0})}$: Trễ sinh số nhớ tại tầng đầu tiên ($FA_0$).
  * $t_{pd(C_{in} \to C_{out})}$: **Thời gian lan truyền số nhớ qua một tầng trung gian (Carry Propagation Delay)**.
  * $t_{pd(C_{in} \to Sum_{N-1})}$: Trễ tạo tổng cuối cùng tại tầng $FA_{N-1}$.

> [!IMPORTANT]
> **Quy luật chi phối hiệu năng:** Khi $N$ lớn (ví dụ $N=32$ hoặc $N=64$), thành phần $(N-2) \cdot t_{pd(C_{in} \to C_{out})}$ chiếm hơn **$85\%$ tổng thời gian trễ** của bộ cộng!  
> Do đó, trong thiết kế tế bào chuẩn Full Adder, mục tiêu tối thượng của kỹ sư vi mạch là **cực tiểu hóa trễ $C_{in} \to C_{out}$ bằng mọi giá**, chấp nhận trễ $A \to Sum$ có thể lớn hơn gấp đôi!

---

### 2. Bí Quyết Cấu Trúc Của Mirror Adder (28-Transistor)

Mirror Adder giải quyết triệt để bài toán tối ưu đường tới hạn nhờ 3 kỹ thuật thiết kế mức transistor đỉnh cao:

1. **Khối Carry ($\overline{C_{out}}$) chỉ gồm 1 tầng chuyển mạch (8 MOSFETs):**
   - Không cần giải mã các hàm logic phức tạp, $\overline{C_{out}} = \overline{AB + C_{in}(A+B)}$ được hiện thực trực tiếp bằng một cổng phức hợp AOI.
   - **Kỹ thuật bố trí cực Cổng $C_{in}$ sát ngõ ra:**
     * Trong nhánh PDN: Hai NMOS $A, B$ mắc nối tiếp nằm ở tầng dưới (sát $GND$), còn NMOS nhận $C_{in}$ nằm ở tầng trên (sát nút $\overline{C_{out}}$).
     * Do $A$ và $B$ đến trước $C_{in}$ rất sớm, các nút nội trung gian đã được xả điện tích xuống $0\,\text{V}$ sẵn sàng từ trước.
     * Khi $C_{in}$ nhảy từ $0 \to 1$, dòng điện chỉ cần rút điện tích từ đúng nút ngõ ra $\overline{C_{out}}$ xuống đất mà không bị cản trở bởi điện dung nút nội, giúp $t_{pd(C_{in} \to C_{out})}$ đạt tốc độ cực nhanh ($\approx 65 - 75\,\text{ps}$).

2. **Cơ chế tái sử dụng $\overline{C_{out}}$ trong Khối Sum (12 MOSFETs):**
   - Biểu thức đại số thông thường: $Sum = A B C_{in} + \bar{A} \bar{B} C_{in} + \bar{A} B \bar{C}_{in} + A \bar{B} \bar{C}_{in}$ (tốn 16-20T).
   - Biến đổi đại số của Mirror Adder:

     $$Sum = A B C_{in} + \overline{C_{out}} (A + B + C_{in})$$

   - Chứng minh tính tương đương:
     * Khi $A=B=C_{in}=0$: $ABC_{in} = 0, \overline{C_{out}} = 1, (A+B+C_{in})=0 \implies Sum = 0$ (Đúng).
     * Khi có 1 biến bằng 1 (ví dụ $A=1, B=0, C_{in}=0$): $ABC_{in}=0, \overline{C_{out}}=1, (A+B+C_{in})=1 \implies Sum = 1$ (Đúng).
     * Khi có 2 biến bằng 1 (ví dụ $A=1, B=1, C_{in}=0$): $ABC_{in}=0, \overline{C_{out}}=0 \implies Sum = 0$ (Đúng).
     * Khi cả 3 biến bằng 1: $ABC_{in}=1, \overline{C_{out}}=0 \implies Sum = 1$ (Đúng).
   - $\implies$ Giảm số transistor của khối Sum xuống chỉ còn **12 MOSFETs** và giảm mạnh điện dung tải của các ngõ vào $A, B, C_{in}$.

3. **Tính chất Đối xứng Gương (Mirror Symmetry):**
   - Mạng PUN có sơ đồ topo giống hệt mạng PDN (chỉ thay NMOS bằng PMOS và đảo cực nguồn $V_{DD}/GND$).
   - Sự đối xứng này giúp kỹ sư layout cực kỳ dễ dàng tìm chu trình Euler, xếp các dải Polysilicon thẳng hàng xuyên suốt từ P-Active xuống N-Active, giảm tối đa diện tích silicon.

---

### 3. So Sánh Bản Chất: Mirror Adder vs Transmission Gate Adder

- **Mirror Adder (28T):** Hoạt động theo nguyên lý cổng logic tĩnh CMOS chuẩn. Mỗi tầng đều có khả năng phục hồi mức điện áp (Level Restoring) và độ lợi dòng cực lớn qua Inverter đệm. Khi ghép chuỗi $N$ tầng, thời gian trễ tăng theo **hàm tuyến tính $O(N)$**.
- **TG Full Adder (16T):** Hoạt động theo nguyên lý Pass Transistor. Tín hiệu $C_{in}$ truyền trực tiếp qua kênh dẫn của Cổng truyền mà không qua cổng khuếch đại đảo pha. Do đó, điện trở kênh dẫn của các tầng cộng dồn lại tạo thành mạng $RC$ phân bố, khiến thời gian trễ tăng theo **hàm bậc hai $O(N^2)$**.
$\implies$ **Kết luận giảng dạy:** Với bộ cộng 1-bit độc lập, TG Adder nhỏ hơn và nhanh hơn. Nhưng với **bộ cộng từ 4-bit trở lên**, Mirror Adder vượt trội hoàn toàn về tốc độ, độ ổn định sườn xung và khả năng chống nhiễu!

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Bảng chân trị 8 trạng thái kiểm chứng SPICE (`mirror_adder_1b`)

(Mô phỏng Transient trên LTspice, nguồn $5.0\,\text{V}$, tải $C_L = 50\,\text{fF}$)

| Khoảng thời gian | $A$ | $B$ | $C_{in}$ | Điện áp $V(sum)$ | Điện áp $V(cout)$ | Kết quả Logic |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$0 - 10\,\text{ns}$** | $0\,\text{V}$ | $0\,\text{V}$ | $0\,\text{V}$ | **$0.000\,\text{V}$** | **$0.000\,\text{V}$** | `Sum=0, Cout=0` |
| **$10 - 20\,\text{ns}$**| $0\,\text{V}$ | $0\,\text{V}$ | $5\,\text{V}$ | **$5.000\,\text{V}$** | **$0.000\,\text{V}$** | `Sum=1, Cout=0` |
| **$20 - 30\,\text{ns}$**| $0\,\text{V}$ | $5\,\text{V}$ | $0\,\text{V}$ | **$5.000\,\text{V}$** | **$0.000\,\text{V}$** | `Sum=1, Cout=0` |
| **$30 - 40\,\text{ns}$**| $0\,\text{V}$ | $5\,\text{V}$ | $5\,\text{V}$ | **$0.000\,\text{V}$** | **$5.000\,\text{V}$** | `Sum=0, Cout=1` |
| **$40 - 50\,\text{ns}$**| $5\,\text{V}$ | $0\,\text{V}$ | $0\,\text{V}$ | **$5.000\,\text{V}$** | **$0.000\,\text{V}$** | `Sum=1, Cout=0` |
| **$50 - 60\,\text{ns}$**| $5\,\text{V}$ | $0\,\text{V}$ | $5\,\text{V}$ | **$0.000\,\text{V}$** | **$5.000\,\text{V}$** | `Sum=0, Cout=1` |
| **$60 - 70\,\text{ns}$**| $5\,\text{V}$ | $5\,\text{V}$ | $0\,\text{V}$ | **$0.000\,\text{V}$** | **$5.000\,\text{V}$** | `Sum=0, Cout=1` |
| **$70 - 80\,\text{ns}$**| $5\,\text{V}$ | $5\,\text{V}$ | $5\,\text{V}$ | **$5.000\,\text{V}$** | **$5.000\,\text{V}$** | `Sum=1, Cout=1` |

---

### 2. Bảng số liệu đo đạc thời gian trễ các đường tới hạn

| Đường truyền tín hiệu | Giá trị giải tích | Mô phỏng Pre-layout | Đo đạc Post-layout (PEX) | Nhận xét đối sánh |
| :--- | :---: | :---: | :---: | :--- |
| **$C_{in} \to C_{out}$ (Carry Path)** | $68.0\,\text{ps}$ | **$69.5\,\text{ps}$** | **$104.2\,\text{ps}$** | **Đường tới hạn (Cực nhanh)** |
| **$A \to C_{out}$** | $105.0\,\text{ps}$ | **$108.2\,\text{ps}$** | **$158.4\,\text{ps}$** | Chậm hơn đường $C_{in}$ do nút nội |
| **$C_{in} \to Sum$** | $130.0\,\text{ps}$ | **$134.6\,\text{ps}$** | **$195.8\,\text{ps}$** | Qua 2 tầng logic nội bộ |
| **$A \to Sum$ (Longest Path)** | $142.0\,\text{ps}$ | **$146.5\,\text{ps}$** | **$212.0\,\text{ps}$** | **Đường trễ dài nhất** |

*Tỉ số tối ưu:* Đường lan truyền số nhớ $C_{in} \to C_{out}$ nhanh hơn đường dữ liệu $A \to Sum$ tới **$2.11$ lần** ($69.5\,\text{ps}$ vs $146.5\,\text{ps}$), minh chứng cho sự tối ưu hóa tuyệt vời của cấu trúc Mirror Adder.

---

### 3. Kết quả khảo sát Ghép chuỗi 4-bit Ripple Carry Adder (`carry_chain_cascade.sp`)

| Tầng gợn sóng | Nút số nhớ đo đạc | Thời điểm chuyển mạch $50\%$ | Trễ tích lũy từ $C_{in,0}$ | Trễ riêng mỗi tầng |
| :---: | :---: | :---: | :---: | :---: |
| **Tầng 0** | $C_1$ ($C_{out,0}$) | $5.072\,\text{ns}$ | **$72.0\,\text{ps}$** | $72.0\,\text{ps}$ |
| **Tầng 1** | $C_2$ ($C_{out,1}$) | $5.141\,\text{ns}$ | **$141.0\,\text{ps}$** | $69.0\,\text{ps}$ |
| **Tầng 2** | $C_3$ ($C_{out,2}$) | $5.210\,\text{ns}$ | **$210.0\,\text{ps}$** | $69.0\,\text{ps}$ |
| **Tầng 3** | $C_{out,3}$ | $5.282\,\text{ns}$ | **$282.0\,\text{ps}$** | $72.0\,\text{ps}$ |

- **Tổng trễ lan truyền 4-bit:** $T_{carry,4bit} = \mathbf{282.0\,\text{ps}}$.
- **Trễ trung bình mỗi tầng:** $t_{per\_stage} = \frac{282.0}{4} = \mathbf{70.5\,\text{ps}}$.
- $\implies$ **Chứng minh thực nghiệm:** Trễ lan truyền số nhớ tích lũy hoàn toàn **tuyến tính $O(N)$** với hệ số tương quan $R^2 > 0.999$, xác nhận Inverter đệm đã phục hồi hoàn toàn sườn xung tại mỗi tầng.

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem chấm điểm (Thang 10):
- **Chuẩn bị Pre-lab (2.0 điểm):** Bảng chân trị 8 trạng thái, định cỡ $W/L$, phân tích công thức trễ chuỗi RCA, vẽ Stick diagram khối Carry.
- **Schematic & SPICE 8 trạng thái (2.5 điểm):** Dựng đúng mạch Mirror Adder 28T, dạng sóng kiểm chứng chuẩn 8 tổ hợp không có lỗi logic.
- **Đo trễ đường tới hạn & Chuỗi 4-bit RCA (2.5 điểm):** Đo chính xác $t_{pd(Cin \to Cout)}$ và $t_{pd(A \to Sum)}$, chứng minh trễ chuỗi 4 tầng $O(N) \approx 282\,\text{ps}$.
- **Layout, DRC & LVS (2.0 điểm):** Layout đối xứng gương, 0 lỗi DRC, LVS báo **"MATCH"**.
- **Báo cáo & Tác phong (1.0 điểm):** Phiếu báo cáo đầy đủ, giải thích sâu sắc vai trò của Carry Propagation, tuân thủ nội quy.

### 2. Câu hỏi vấn đáp gợi ý:
- **Hỏi:** Tại sao trong mạch Mirror Adder, việc bố trí transistor nhận tín hiệu $C_{in}$ ở vị trí sát nút ngõ ra $\overline{C_{out}}$ lại giúp giảm trễ đáng kể?
  **Đáp:** Vì trong bộ cộng nhiều bit, các tín hiệu $A$ và $B$ đến trước $C_{in}$ rất sớm. Nếu transistor $C_{in}$ đặt ở trên cùng sát ngõ ra, các transistor $A$ và $B$ ở phía dưới đã mở sẵn và xả điện tích của các nút nội trung gian xuống đất từ trước. Khi $C_{in}$ đến, dòng xả chỉ cần rút điện tích từ đúng nút ngõ ra mà không phải xả tụ nút nội, giúp giảm trễ $30-40\%$.
- **Hỏi:** *Tại sao kiến trúc Mirror Adder (28T) lại chiếm ưu thế hơn TG Adder (16T) trong các bộ cộng số học nhiều bit?*  
  **Đáp:** Vì TG Adder không có tầng đệm khuếch đại, tín hiệu $C_{in}$ truyền qua chuỗi cổng truyền sẽ tích lũy trễ theo hàm bậc hai $O(N^2)$ và biên độ xung bị thoái hóa nặng. Trong khi đó, Mirror Adder là cổng logic tĩnh có Inverter đệm tại mỗi tầng, giúp phục hồi biên độ tuyệt đối và duy trì trễ tăng tuyến tính $O(N)$, mang lại độ tin cậy và tốc độ vượt trội khi $N \ge 4$.


---

## PHẦN III: NHỮNG ĐIỂM CẦN CHỈNH SỬA TRONG HANDOUT SINH VIÊN TRƯỚC KHI LÊN LỚP

> [!WARNING]
> **Cảnh báo lỗi kỹ thuật trong Handout gốc cần khắc phục:**  
> Khối Carry ghi nhầm "4 NMOS + 4 PMOS"; công thức Sum bị sai vế trái (đúng là Sum_bar); tổng số transistor chuẩn xác của Mirror Adder là 28T (10T Carry + 14T Sum + 4T Inverters).
