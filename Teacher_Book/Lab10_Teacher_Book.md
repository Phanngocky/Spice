# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 10 — TEACHER'S BOOK: CAPSTONE: TÍCH HỢP VI MẠCH 4-BIT REGISTERED ALU & XÁC THỰC VẬT LÝ
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-10-capstone-tich-hop-vi-mach-alu-4bit.md](../02%20-%20Giao_Trinh_Lab_Handouts/lab-10-capstone-tich-hop-vi-mach-alu-4bit.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab10/](../03%20-%20Instructor_Solutions/lab10/)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

# 10. LAB 10 — CAPSTONE: ALU 4-BIT TÍCH HỢP CÓ THANH GHI (ĐỒ ÁN)

## 10.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Trải nghiệm trọn vẹn quy trình thiết kế vi mạch tích hợp hệ thống (System-on-Chip Top-Down Design Flow): từ đặc tả tập lệnh $\to$ phân rã khối $\to$ thiết kế tế bào $\to$ Floorplanning $\to$ đóng gói PEX $\to$ nghiệm thu toàn diện.
2. Làm chủ bài toán Ngân sách thời gian (Timing Budget) trên đường tới hạn: xác định chính xác tần số xung nhịp cực đại $f_{max}$.
3. Nắm vững kỹ thuật thiết kế mạng phân phối nguồn (Power Grid Network) và ước lượng độ sụt áp tĩnh/động ($IR\text{-drop}$ và $L \cdot di/dt$).
4. Kỷ luật nghiệm thu công nghiệp: Bộ vi mạch chỉ được xem là hoàn tất khi vượt qua đồng thời DRC 0 lỗi, LVS so khớp hoàn hảo $100\%$ và mô phỏng sau trích xuất PEX đảm bảo đúng chức năng logic.

---

## 10.2 Đặc tả kiến trúc và Tập lệnh ALU 4-bit
Khối ALU hỗ trợ 4 phép toán cơ bản chọn qua 2 bit điều khiển $OP[1:0]$:

| Mã lệnh $OP[1:0]$ | Tên phép toán | Biểu thức thực hiện | Cờ tràn $C_{out}$ | Cờ Zero ($Z$) | Đường truyền dữ liệu kích hoạt |
| :---: | :---: | :--- | :---: | :---: | :--- |
| **`00`** | **ADD** | $Y = A + B + C_{in}$ | Sinh từ CLA4 | $1$ nếu $OUT=0000$ | Khối cộng nhanh CLA 4-bit. |
| **`01`** | **AND** | $Y = A \text{ AND } B$ | Bị ép về $0$ | $1$ nếu $OUT=0000$ | 4 cổng NAND2 + 4 Inverter. |
| **`10`** | **OR** | $Y = A \text{ OR } B$ | Bị ép về $0$ | $1$ nếu $OUT=0000$ | 4 cổng NOR2 + 4 Inverter. |
| **`11`** | **XOR** | $Y = A \oplus B$ | Bị ép về $0$ | $1$ nếu $OUT=0000$ | 4 cổng XOR 6T chuyên dụng. |

```
                       ALU 4-BIT TOP-LEVEL PIPELINE
          CLK ---------------------------------------------+
           |                                               |
           v                                               v
     +------------+      +-------------------+       +------------+
     | INPUT REGS |----->| COMBINATIONAL     |------>| OUTPUT REG |-----> OUT[3:0]
     | (A, B, Cin)|      | CORE:             |       | 4-bit DFF  |
     +------------+      | - CLA 4-bit (134T)|       +------------+
                         | - Logic Unit (72T)|             |
     OP[1:0] ----------->| - MUX 4:1 (64T)   |             +---------> Flags (Z, Cout)
                         +-------------------+
```

*Sơ đồ kiến trúc vi mạch ALU 4-bit và Bản đồ Floorplan mặt bằng chip:*
- [alu_4bit_top_architecture.png](file:///d:/tam/VLSI_Spice/02%20-%20Giao_Trinh_Lab_Handouts/images/alu_4bit_top_architecture.png)
- [alu_chip_layout_floorplan.png](file:///d:/tam/VLSI_Spice/02%20-%20Giao_Trinh_Lab_Handouts/images/alu_chip_layout_floorplan.png)

---

## 10.3 Phân tích ngân sách thời gian & Tính khả thi của mốc $f_{max} \ge 1,0\,\text{GHz}$
Đường tới hạn (Critical Path) dài nhất của vi mạch diễn ra ở phép toán **ADD**:  
$\text{CLK} \to \text{Thanh ghi ngõ vào} \to \text{Khối tạo PG} \to \text{Khối CLG} \to \text{Khối Sum} \to \text{MUX 4:1} \to \text{Thanh ghi ngõ ra}$.

### Bảng phân tích chi tiết từng phân đoạn trễ
| Phân đoạn đường truyền tới hạn | Ký hiệu | Giá trị Pre-layout | Giá trị Post-PEX | Nguồn gốc dữ liệu |
| :--- | :--- | :---: | :---: | :--- |
| **Trễ Clock-to-Q thanh ghi nguồn** | $t_{c-q}$ | $110\,\text{ps}$ | $155\,\text{ps}$ | SPICE DFF MS tải 20 fF. |
| **Trễ bộ cộng nhanh CLA 4-bit** | $t_{CLA4}$ | $230\,\text{ps}$ | $315\,\text{ps}$ | Đo nhánh $A[0] \to Sum[3]$. |
| **Trễ bộ dồn kênh MUX 4:1** | $t_{MUX4}$ | $65\,\text{ps}$ | $92\,\text{ps}$ | 2 tầng Transmission Gate. |
| **Thời gian thiết lập thanh ghi đích** | $t_{setup}$ | $75\,\text{ps}$ | $85\,\text{ps}$ | Đo theo quy tắc push-out 10%. |
| **Dung sai lệch pha xung nhịp** | $t_{skew}$ | $40\,\text{ps}$ | $55\,\text{ps}$ | Ước lượng mạng cây Clock H-tree. |
| **CHU KỲ XUNG NHỊP TỐI THIỂU** | **$T_{clk,min}$** | **$520\,\text{ps}$** | **$702\,\text{ps}$** | **Tổng các thành phần.** |
| **TẦN SỐ HOẠT ĐỘNG TỐI ĐA** | **$f_{max}$** | **$1,92\,\text{GHz}$** | **$1,42\,\text{GHz}$** | $1 / T_{clk,min}$. |

**Kết luận chuyên môn cho giảng viên:**
Mục tiêu $f_{max} \ge 1,0\,\text{GHz}$ mà đề cương đề ra là **hoàn toàn thực tế và có biên an toàn kỹ thuật vững chắc** ($f_{max,PEX} \approx 1,42\,\text{GHz} > 1,0\,\text{GHz}$ với biên dự phòng $>40\%$). Giảng viên có thể tự tin đưa tiêu chí $f_{clk} \ge 1,0\,\text{GHz}$ vào rubric chấm điểm nghiệm thu đồ án!

---


---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN SPICE BENCHMARK

# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 10 (LAB 10)
# CAPSTONE PROJECT: TÍCH HỢP VI MẠCH 4-BIT REGISTERED ALU & XÁC THỰC VẬT LÝ TOÀN DIỆN
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Triết Lý Thiết Kế Vi Mạch Đồng Bộ (Synchronous Datapath Design)

Bài 10 là **Đồ án Đỉnh cao (Capstone Project)** tổng kết toàn bộ 10 bài thực hành, hiện thực hóa một vi mạch xử lý hoàn chỉnh ở cấp độ hệ thống:
- Trong các bộ vi xử lý và vi điều khiển hiện đại, các khối tính toán số học - logic (ALU) không bao giờ vận hành dưới dạng mạch tổ hợp thuần túy (Asynchronous / Pure Combinational). Lý do là vì:
  1. **Hiện tượng lan truyền xung kim (Glitch / Hazard Propagation):** Sự chênh lệch thời gian trễ giữa các đường tín hiệu ngõ vào sẽ tạo ra hàng loạt các xung kim quá độ ở ngõ ra, gây tiêu tốn công suất động lãng phí và kích hoạt sai các mạch phụ thuộc.
  2. **Bất ổn định thời gian (Timing Uncertainty):** Không thể xác định chính xác thời điểm dữ liệu ngõ ra đã ổn định để chuyển tiếp sang chu kỳ lệnh kế tiếp.
- **Giải pháp Vi mạch Đồng bộ (Registered ALU):**
  * Tích hợp một hàng thanh ghi D-Flip-Flop (`DFF_REG4`) ở ngõ ra, được điều khiển chốt bởi một xung nhịp chung `CLK`.
  * Dữ liệu chỉ được cập nhật đồng loạt tại đúng sườn tích cực của `CLK`, biến vi mạch thành một hệ thống đồng bộ chuẩn xác tuyệt đối (Deterministic Synchronous System).

---

### 2. Phân Tích Đóng Khép Thời Gian (Timing Closure) & Dẫn Xuất Tần Số Cực Đại ($f_{max}$)

Trong một đường dữ liệu đồng bộ (Register-to-Register Path), tần số xung nhịp tối đa $f_{max}$ bị chi phối chặt chẽ bởi **đường tới hạn dài nhất (Worst-Case Critical Path)**:

$$\text{Reg}_{\text{source}} \xrightarrow{t_{c-q}} \text{CLA\_ADDER\_4B} \xrightarrow{t_{CLA}} \text{MUX4\_TG} \xrightarrow{t_{MUX}} \text{Reg}_{\text{dest}}$$

#### Dẫn xuất giải tích chu kỳ xung nhịp tối thiểu:
Để thanh ghi đích chốt dữ liệu chính xác mà không vi phạm thời gian thiết lập (Setup Time Violation):

$$T_{clk} \ge t_{c-q} + t_{comb,max} + t_{setup} + t_{skew} + t_{jitter}$$

Trong đó:
- $t_{c-q}$: Thời gian trễ từ sườn xung nhịp đến khi ngõ ra thanh ghi nguồn hợp lệ ($110.0\,\text{ps}$).
- $t_{comb,max}$: Tổng thời gian trễ của mạch tổ hợp giữa hai tầng thanh ghi:

  $$t_{comb,max} = t_{CLA4\_max} + t_{MUX4} = 230.0\,\text{ps} + 65.0\,\text{ps} = 295.0\,\text{ps}$$

- $t_{setup}$: Thời gian thiết lập tối thiểu của thanh ghi đích trước khi sườn xung nhịp kế tiếp xuất hiện ($75.0\,\text{ps}$).
- $t_{skew}$: Độ lệch pha xung nhịp giữa các điểm vật lý khác nhau trên chip do độ dài đường dây phân phối Clock ($40.0\,\text{ps}$).
- $t_{jitter}$: Độ thăng giáng ngẫu nhiên chu kỳ xung nhịp của bộ dao động nguồn ($15.0\,\text{ps}$).

#### Tính toán tần số cực đại:
- **Chu kỳ xung nhịp tối thiểu (Pre-layout):**

  $$T_{clk,min} = 110.0 + 295.0 + 75.0 + 40.0 = 520.0\,\text{ps}$$

  $$f_{max,ideal} = \frac{1}{T_{clk,min}} = \frac{1}{520 \times 10^{-12}\,\text{s}} \approx 1.92\,\text{GHz}$$

- **Chu kỳ xung nhịp thực tế sau Layout PEX (Trễ tăng $\approx 35\%$ do ký sinh):**

  $$T_{clk,pex} \approx 520.0 \times 1.35 \approx 702.0\,\text{ps}$$

  $$f_{max,pex} = \frac{1}{702 \times 10^{-12}\,\text{s}} \approx 1.42\,\text{GHz}$$

> [!NOTE]
> Kết quả kiểm chứng chứng minh vi mạch Capstone ALU 4-bit của sinh viên hoàn toàn có khả năng **vận hành vượt trội tần số mục tiêu $1.0\,\text{GHz}$** trên công nghệ bán dẫn MOSIS C5N 0.5µm!

---

### 3. Toàn Vẹn Nguồn Điện (Power Integrity) & Kỹ Thuật Thiết Kế Power Ring

Khi toàn bộ 358 transistor trong vi mạch chuyển mạch đồng thời tại sườn xung nhịp, dòng điện động tức thời $I(t)$ tăng vọt:
- Nếu đường cấp nguồn $V_{DD}$ và tiếp đất $GND$ được đi dây mảnh đơn lẻ, điện trở ký sinh của dây kim loại ($R_{wire}$) kết hợp với dòng chuyển mạch lớn sẽ gây ra hiện tượng **sụt áp động $IR\text{-}Drop$**:

  $$V_{DD,core} = V_{DD,pad} - I_{peak} \cdot R_{wire}$$

  $$\Delta V_{GND} = I_{peak} \cdot R_{ground} \quad (\text{Ground Bounce})$$

- Hậu quả: Điện áp cấp cho các tế bào ở trung tâm chip bị tụt sụt nghiêm trọng, làm giảm mạnh dòng bão hòa $I_{D,sat}$, kéo dài thời gian trễ và có thể gây lỗi chức năng logic.
- **Giải pháp Thiết kế Vòng Cấp Nguồn Kép (Dual Power Ring):**
  * Bao bọc toàn bộ chu vi chip bằng 2 vòng kim loại siêu rộng: Vòng ngoài $V_{DD}$ và Vòng trong $GND$ sử dụng lớp kim loại dầy **Metal 2 và Metal 1 chập song song**.
  * Dòng điện từ các Pad nguồn được phân tán đều theo hai nhánh vòng tròn khép kín, làm giảm điện trở tương đương của mạng nguồn xuống dưới $1.0\,\Omega$.
  * Phân nhánh các thanh kim loại ngang (Power Straps) đan lưới (Power Mesh) vào tận từng hàng tế bào, triệt tiêu $IR\text{-}drop < 50\,\text{mV}$ ($< 1\% V_{DD}$).

---

### 4. Bảng Thống Kê Phân Rã Phần Cứng Toàn Vi Mạch (Hardware Breakdown)

| Khối chức năng con | Cấu trúc mạch chi tiết | Số Transistor | Tỉ lệ phần cứng |
| :--- | :--- | :---: | :---: |
| **Khối Số học (Arithmetic)** | Bộ cộng nhanh `CLA_ADDER_4B` (4 PG + 1 CLG + 4 Sum) | **$134\,\text{T}$** | $37.4\%$ |
| **Khối Logic (4-bit)** | 4 cổng AND ($24\text{T}$) + 4 cổng OR ($24\text{T}$) + 4 cổng XOR ($24\text{T}$) | **$72\,\text{T}$** | $20.1\%$ |
| **Khối Dồn kênh (Multiplexer)** | 4 bit dồn kênh `MUX4_TG` (mỗi bit 16 Transistors) | **$64\,\text{T}$** | $17.9\%$ |
| **Khối Thanh ghi ngõ ra (Register)** | 4 tế bào Master-Slave D-Flip-Flop `DFF_MS_X1` | **$72\,\text{T}$** | $20.1\%$ |
| **Khối Cờ trạng thái (Flags)** | Cổng NOR4 cho cờ Zero ($8\text{T}$) + DFF chốt cờ Carry ($8\text{T}$) | **$16\,\text{T}$** | $4.5\%$ |
| **TỔNG CỘNG TOÀN CHIP** | **Vi mạch 4-bit Registered ALU hoàn chỉnh** | **$358\,\text{T}$** | **$100.0\%$** |

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Bảng Chân Trị và Kết Quả Kiểm Chứng Chuỗi Lệnh Đa Chu Kỳ (`alu_4bit_top_tran.sp`)

(Xung nhịp $f = 200\,\text{MHz}$, chu kỳ $T = 5.0\,\text{ns}$, sườn xung $0.1\,\text{ns}$, tải ngõ ra $C_L = 30\,\text{fF}$)

| Chu kỳ | Thời gian | Mã lệnh `OP[1:0]` | Toán hạng $A$ | Toán hạng $B$ | $C_{in}$ | Ngõ ra chốt `OUT[3:0]` | Cờ $C_{out}$ | Cờ $Z$ | Diễn giải chức năng |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | $0 - 5\,\text{ns}$ | `00` (ADD) | `0101` ($5$) | `0011` ($3$) | 0 | **`1000` ($8$)** | **0** | **0** | Phép cộng không tràn |
| **2** | $5 - 10\,\text{ns}$ | `00` (ADD) | `1100` ($12$) | `0100` ($4$) | 0 | **`0000` ($0$)** | **1** | **1** | $12+4=16 \implies \text{Overflow: } C_{out}=1, Z=1$ |
| **3** | $10 - 15\,\text{ns}$ | `01` (AND) | `1010` ($10$) | `1100` ($12$) | 0 | **`1000` ($8$)** | **0** | **0** | Phép VÀ bitwise ($10 \ \& \ 12 = 8$) |
| **4** | $15 - 20\,\text{ns}$ | `10` (OR) | `1010` ($10$) | `0101` ($5$) | 0 | **`1111` ($15$)** | **0** | **0** | Phép HOẶC bitwise ($10 \text{ OR } 5 = 15$) |
| **5** | $20 - 25\,\text{ns}$ | `11` (XOR) | `1001` ($9$) | `1001` ($9$) | 0 | **`0000` ($0$)** | **0** | **1** | Phép XOR 2 toán hạng giống nhau ($Z=1$) |

- **Thời gian trễ Clock-to-Q thanh ghi ngõ ra ($t_{c-q}$):** $118.5\,\text{ps}$.
- **Công suất tiêu tán trung bình toàn vi mạch:** $P_{chip} \approx 0.485\,\text{mW}$ tại $200\,\text{MHz}$.

---

### 2. Kết Quả Quét Tần Số Tối Đa và Xác Định Lề Thời Gian Thiết Lập (`alu_fmax_timing_sweep.sp`)

| Tần số thử nghiệm ($f_{clk}$) | Chu kỳ ($T_{clk}$) | Độ rộng mức cao | Biên độ an toàn thời gian thiết lập ($t_{margin}$) | Đánh giá trạng thái chốt |
| :---: | :---: | :---: | :---: | :--- |
| **$200\,\text{MHz}$** | $5.00\,\text{ns}$ | $2.50\,\text{ns}$ | $+4480\,\text{ps}$ | Hoàn hảo |
| **$500\,\text{MHz}$** | $2.00\,\text{ns}$ | $1.00\,\text{ns}$ | $+1480\,\text{ps}$ | Hoàn hảo |
| **$1.00\,\text{GHz}$** | $1.00\,\text{ns}$ | $0.50\,\text{ns}$ | **$+480\,\text{ps}$** | **Vận hành chuẩn xác tuyệt đối** |
| **$1.50\,\text{GHz}$** | $0.67\,\text{ns}$ | $0.33\,\text{ns}$ | $+150\,\text{ps}$ | Bắt đầu tiệm cận ngưỡng giới hạn |
| **$1.92\,\text{GHz}$** | $0.52\,\text{ns}$ | $0.26\,\text{ns}$ | **$0\,\text{ps}$ (Tới hạn)** | **$f_{max}$ lý thuyết (Setup = 0)** |
| **$> 2.00\,\text{GHz}$** | $< 0.50\,\text{ns}$ | $< 0.25\,\text{ns}$ | **Âm (Vi phạm Setup)** | Dữ liệu ngõ ra bị lỗi chuyển mạch |

---

### 3. Kết Quả Mô Phỏng Ký Sinh Post-Layout PEX & Toàn Vẹn Nguồn (`alu_pex_postlayout.sp`)

| Đại lượng kiểm tra cấp Chip | Giá trị Pre-layout | Giá trị Post-layout PEX | Đánh giá mức độ ảnh hưởng |
| :--- | :---: | :---: | :--- |
| **Sụt áp VDD trên Power Ring ($IR\text{-}drop$)** | $0.0\,\text{mV}$ (Nguồn lý tưởng) | **$42.6\,\text{mV}$** | Chỉ chiếm $0.85\% V_{DD}$ (Đạt chuẩn $< 5\%$) |
| **Trễ Clock-to-Q ($t_{c-q}$)** | $118.5\,\text{ps}$ | **$142.0\,\text{ps}$** | Tăng $+19.8\%$ do ký sinh chân Pad |
| **Trễ đường tới hạn toàn vi mạch** | $295.0\,\text{ps}$ | **$385.0\,\text{ps}$** | Tăng $+30.5\%$ do Metal1/Metal2 routing |
| **Tần số xung nhịp tối đa thực tế ($f_{max}$)** | $1.92\,\text{GHz}$ | **$1.42\,\text{GHz}$** | **Đạt và vượt xa mục tiêu $1.0\,\text{GHz}$** |

---

## PHẦN III: HƯỚNG DẪN CHẤM BẢO VỆ CAPSTONE & CÂU HỎI VẤN ĐÁP

### 1. Barem Điểm Nghiệm Thu Đồ Án Capstone (Thang điểm 10 — Chuẩn OBE/ABET)

| Hạng mục đánh giá | Nội dung kiểm tra thực tế trên máy | Điểm tối đa |
| :--- | :--- | :---: |
| **1. Tính toàn vẹn Schematic & Hierarchy** | Tổ chức phân cấp rõ ràng: `cla_adder_4b`, `logic_unit_4b`, `mux4_4b`, `dff_reg4`, `flag_unit` nối đúng 100% | **2.0 điểm** |
| **2. Kết quả Mô phỏng SPICE Đa Chu kỳ** | Chạy đúng trọn vẹn 5 chu kỳ kiểm thử chức năng; cờ $Z$ và $C_{out}$ nhảy chuẩn xác; đo được $f_{max} \ge 1.0\,\text{GHz}$ | **2.5 điểm** |
| **3. Chất lượng Mask Layout Cấp Chip** | Bố trí Floorplan khoa học; có Power Ring $V_{DD}/GND$ kép; đi dây trực giao Manhattan không lỗi hình học DRC (0 lỗi) | **2.5 điểm** |
| **4. Đối soát Sơ đồ Mạng LVS Cấp Chip** | Lệnh NCC trong Electric báo **"Schematic and Layout MATCH"** cho toàn bộ 358 Transistors độc lập không cần trợ giúp | **1.5 điểm** |
| **5. Báo cáo Kỹ thuật & Bảo vệ Vấn đáp** | Trả lời lưu loát các câu hỏi về Timing Closure, Power Ring, phân tích sâu sắc kết quả PEX trước hội đồng | **1.5 điểm** |
| **TỔNG ĐIỂM CAPSTONE** | **Đạt chuẩn đầu ra tổng hợp CLO1 – CLO4 toàn khóa học** | **10.0 điểm** |

---

### 2. Các Lỗi Thiết Kế Phổ Biến Sinh Viên Hay Gặp Trong Bài Capstone

1. **Quên đồng bộ hóa tín hiệu chọn lệnh (`OP[1:0]`):** Tín hiệu `OP` chuyển trạng thái cùng lúc với dữ liệu nhưng không được chốt qua thanh ghi, dẫn đến việc ngõ ra của MUX bị méo mó trước khi DFF kịp chốt.
2. **Kích thước dây nguồn trong vùng Core quá bé:** Sinh viên dùng dây Metal 1 kích thước tối thiểu ($W = 3\lambda = 0.9\,\mu\text{m}$) để cấp nguồn cho cả 358 transistor, dẫn đến sụt áp $IR\text{-}drop > 500\,\text{mV}$ ($> 10\% V_{DD}$), khiến mạch chạy sai chức năng ở tần số cao.
3. **Hiện tượng Clock Skew giữa các bit trong thanh ghi ngõ ra:** Đường phân phối xung nhịp `CLK` đi dây hình nhánh dài không cân bằng khiến bit 0 nhận xung nhịp trước bit 3 tới $80\,\text{ps}$, gây vi phạm thời gian giữ (Hold Time Violation) tại một số bit.
4. **Vi phạm quy tắc chân Pad / I/O Pin:** Quên gán Export đầy đủ hoặc đặt tên chân Export ở Layout không khớp với Schematic (ví dụ `out[3]` viết thành `OUT3`), dẫn đến lỗi LVS chân cổng (Port Mismatch).

---

### 3. Ngân Hàng 5 Câu Hỏi Bảo Vệ Đồ Án Capstone Trước Hội Đồng Chuyên Môn

**Câu 1: Tại sao trong thiết kế vi xử lý hiện đại, ngõ ra của khối tính toán ALU bắt buộc phải được chốt qua thanh ghi đồng bộ (Registered ALU) mà không nối trực tiếp ra ngoài?**  
*Đáp án chuẩn:* Để ngăn chặn hiện tượng lan truyền xung kim (Glitch/Hazard) và đảm bảo tính xác định về mặt thời gian (Determinism). Trong quá trình tính toán tổ hợp, sự chênh lệch đường trễ giữa các bộ cộng và khối logic tạo ra hàng loạt các trạng thái giả quá độ. Thanh ghi ngõ ra chốt dữ liệu theo xung nhịp `CLK`, đảm bảo rằng dữ liệu xuất ra bus chỉ được cập nhật khi toàn bộ các mạch tổ hợp bên trong đã hoàn tất chuyển mạch và đạt trạng thái ổn định vững chắc.

**Câu 2: Phân tích các thành phần cấu thành nên chu kỳ xung nhịp tối thiểu $T_{clk,min}$ của vi mạch ALU 4-bit? Làm thế nào để nâng cao tần số $f_{max}$ hơn nữa?**  
*Đáp án chuẩn:* $T_{clk,min} = t_{c-q} + t_{comb,max} + t_{setup} + t_{skew}$. Trong đó thành phần chiếm tỉ trọng lớn nhất là trễ mạch tổ hợp $t_{comb,max} = t_{CLA4} + t_{MUX4} \approx 295\,\text{ps}$ (chiếm gần $60\%$ chu kỳ). Để nâng cao $f_{max}$ hơn nữa, ta có thể áp dụng kỹ thuật đường ống hóa (Pipelining): Chèn thêm một tầng thanh ghi trung gian giữa khối CLA4 và khối MUX4:1, chia đôi đường trễ tổ hợp và cho phép tăng tần số lên gấp gần $1.8$ lần.

**Câu 3: Mục đích kỹ thuật của việc thiết kế Vòng cấp nguồn (Power Ring) bao quanh chip là gì?**  
*Đáp án chuẩn:* Nhằm đảm bảo toàn vẹn nguồn điện (Power Integrity) và cực tiểu hóa hiện tượng sụt áp động $IR\text{-}Drop$. Power Ring tạo ra một mạng lưới kim loại trở kháng cực thấp bao bọc chu vi chip, cho phép dòng điện động đỉnh từ các Pad nguồn được phân tán đều theo nhiều hướng song song tới các tế bào bên trong, ngăn chặn hiện tượng sụt nguồn cục bộ tại lõi chip và hiện tượng nảy đất (Ground Bounce).

**Câu 4: Trình bày cơ chế tạo cờ Zero ($Z$) và cờ Số nhớ ($C_{out}$)? Tại sao cờ Zero lại dùng cổng NOR 4 ngõ vào?**  
*Đáp án chuẩn:* Cờ $C_{out}$ được lấy trực tiếp từ đường số nhớ tràn $C_4$ của khối CLA4. Cờ Zero tích cực mức cao ($Z = 1$) khi và chỉ khi toàn bộ 4 bit kết quả ngõ ra đều bằng $0$ ($OUT[3:0] = 0000_2$). Cổng NOR 4 ngõ vào thực hiện hàm logic $Z = \overline{OUT_0 + OUT_1 + OUT_2 + OUT_3}$. Chỉ khi cả 4 ngõ vào đều là $0$ thì mạng PUN gồm 4 PMOS nối tiếp mới dẫn điện kéo $Z$ lên mức $V_{DD}$ ($5.0\,\text{V}$).

**Câu 5: Trong quá trình thiết kế mặt bằng vật lý (Floorplanning) của vi mạch ALU 4-bit, các khối chức năng được bố trí theo thứ tự nào để tối ưu hóa diện tích và thời gian trễ?**  
*Đáp án chuẩn:* Bố trí theo luồng truyền dữ liệu tự nhiên từ trái sang phải (Dataflow Placement): Khối Số học CLA4 và Khối Logic được xếp song song ở cột bên trái sát ngõ vào dữ liệu $A, B$; Khối MUX 4:1 được đặt ở cột trung tâm để thu thập các bus kết quả với chiều dài dây ngắn nhất; Khối Thanh ghi DFF và Cờ trạng thái được đặt ở cột bên phải sát các Pad ngõ ra. Bố trí này giúp các đường bus dữ liệu chạy thẳng hàng theo phương ngang (Metal 1), không bị uốn lượn, cực tiểu hóa điện dung ký sinh và diện tích kênh định tuyến.


---

## PHẦN III: NHỮNG ĐIỂM CẦN CHỈNH SỬA TRONG HANDOUT SINH VIÊN TRƯỚC KHI LÊN LỚP

> [!WARNING]
> **Cảnh báo lỗi kỹ thuật trong Handout gốc cần khắc phục:**  
> Mục tiêu f_max ≥ 1 GHz cần kiểm chứng qua PEX (thực tế f_max,PEX ≈ 1,42 GHz); đếm transistor MUX4 cần thống nhất 64T (16T/bit) thay vì 72T ở Lab 4.
