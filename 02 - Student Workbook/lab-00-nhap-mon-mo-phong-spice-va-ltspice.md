# THỰC HÀNH THIẾT KẾ VLSI — BÀI 0
# LÀM QUEN MÔ PHỎNG SPICE VỚI LTSPICE & MẠCH RC CƠ BẢN

---
**Học phần:** Thực hành Thiết kế VLSI (Mã học phần: `5505382`)  
*(Phần thực hành mô phỏng SPICE phục vụ trực tiếp nội dung đồ án và bài tập lớn môn Thiết kế VLSI)*  
**Bộ môn:** Điện tử - Viễn thông | **Khoa:** Điện - Điện tử | **Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Liên hệ giáo trình:** Chương 1 (Quy trình thiết kế vi mạch Full-Custom), Chương 3 (Mô hình trễ RC và điện trở kênh dẫn)  
**Công cụ sử dụng:** LTspice (phiên bản XVII hoặc LTspice 24/2025 trở lên)  
**Thời lượng đề xuất:** 
- *Khung chuẩn tại lớp (bắt buộc):* 1 buổi thực hành trực tiếp tại phòng máy (135 phút / 3 tiết thực hành).
- *Khung mở rộng (tùy chọn):* 225 phút (5 tiết tích hợp) nếu giảng viên bố trí thêm giờ hướng dẫn chuyên sâu.
- *Phần hoàn thiện tại nhà:* Hoàn thiện và đóng gói thư mục dự án Lab 0 (khoảng 1,5 đến 2 giờ).
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Trích xuất và đọc hiểu cú pháp Netlist SPICE** từ sơ đồ nguyên lý (Schematic), phân biệt rõ vai trò của nút mốc chuẩn `0` và các quy ước tiền tố đơn vị (CLO1, CLO2).
2. **Thiết lập và vận hành 4 chế độ phân tích cơ bản**:
   - Điểm làm việc tĩnh DC: `.op`
   - Quét điện áp DC: `.dc`
   - Đáp ứng miền thời gian (Quá độ): `.tran`
   - Đáp ứng miền tần số: `.ac`
3. **Đo tự động các thông số quá độ và tần số bằng câu lệnh `.meas`**: Đo chính xác độ trễ lan truyền ($t_{pd}$), thời gian sườn tăng/giảm ($t_r, t_f$), đỉnh dòng điện nạp/xả và tần số cắt $-3\,\text{dB}$ ($f_c$) với sai lệch tương đối $\le 2,0\%$ so với lý thuyết giải tích (CLO2).
4. **Khảo sát độ nhạy tham số linh kiện** bằng chỉ thị `.param` và lệnh quét `.step`, trích xuất dữ liệu đo từ SPICE Error Log và vẽ đồ thị thực nghiệm để xác định độ dốc (CLO2).
5. **Thực hiện kiểm chéo giữa hai phép đo độc lập** (miền thời gian và miền tần số) để khẳng định tính nhất quán vật lý của hệ thống tuyến tính bậc một ($t_r \cdot f_c \approx 0,35$) (CLO2).
6. **Liên kết mô hình công nghệ MOSFET C5N Level 3** bằng lệnh `.include`, đo dòng cực má $I_D$ bằng `.op`, so sánh với mô hình bậc hai Shichman-Hodges và giải thích các nguyên nhân vật lý gây chênh lệch (CLO1, CLO2).
7. **Tổ chức, đóng gói và bàn giao thư mục dự án mô phỏng** `lab00_MSSV_HoTen/` theo đúng quy chuẩn kỹ thuật (CLO4).

> [!NOTE]
> **Định hướng sư phạm:** Mục tiêu cốt lõi của Lab 0 là làm quen công cụ, rèn luyện kỹ năng mô phỏng và hình thành thói quen kiểm chứng kết quả ("tính trước, đo sau, so sánh và giải thích sai lệch"). Sinh viên **chưa bắt buộc phải tự thiết kế các tế bào logic CMOS phức tạp** trong bài này; phần mô hình transistor MOSFET được tiếp cận ở mức độ làm quen liên kết mô hình để chuẩn bị cho Lab 1.

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

| Thành phần | Chi tiết chuyển giao kỹ thuật |
| :--- | :--- |
| **Dùng lại từ lab trước** | Không có (đây là bài Lab nền tảng đầu tiên của học phần). |
| **Sinh ra cho lab sau** | - **Thư mục dự án mẫu `lab00_MSSV_HoTen/`** được chuẩn hóa cấu trúc để tái sử dụng từ Lab 1 đến Lab 10.<br>- **Tệp mô hình công nghệ `C5_models.txt`**: Sao chép từ thư mục `04 - Models_and_Libraries/C5_models.txt` của kho học liệu vào thư mục làm việc.<br>- **Khung netlist mẫu và cú pháp đo `.meas` tham số hóa** dùng lại cho toàn bộ các bài đo cổng logic CMOS.<br>- **Bảng đối chuẩn trễ RC cơ sở** làm mốc so sánh với độ trễ truyền lan của Inverter tại Lab 1. |

---

## 3. CƠ SỞ LÝ THUYẾT NGẮN GỌN

### 3.1. SPICE và Cấu trúc Netlist
SPICE (*Simulation Program with Integrated Circuit Emphasis*) là chương trình mô phỏng mạch điện tử chuẩn công nghiệp, giải hệ phương trình vi phân đại số phi tuyến thông qua **Phương pháp Điện áp Nút Cải biên (Modified Nodal Analysis - MNA)**.

Dữ liệu đầu vào của SPICE là một tệp văn bản thuần gọi là **Netlist**. Mỗi dòng mô tả một phần tử theo cú pháp:
```
<Tên linh kiện> <Nút +> <Nút -> [Nút điều khiển...] <Giá trị hoặc Tên Model>
```
- **Dòng đầu tiên** của tệp Netlist luôn là tiêu đề (Title) và không được tính là linh kiện của mạch.
- Dòng bắt đầu bằng dấu hoa thị `*` là chú thích (Comment); dòng bắt đầu bằng dấu cộng `+` là dòng nối tiếp của câu lệnh trước.
- **Nút đất bắt buộc phải có tên là `0` (hoặc `GND`)**: SPICE dùng nút `0` làm mốc thế chuẩn $0\,\text{V}$. Nếu thiếu nút `0`, ma trận dẫn nạp MNA sẽ bị suy biến và trình mô phỏng thường báo lỗi như `Singular matrix` hoặc `no DC path to ground`.
- Trong LTspice, sinh viên có thể xem trực tiếp Netlist được sinh ra từ sơ đồ bằng cách chọn menu **View $\to$ SPICE Netlist**.

### 3.2. Tiền tố đơn vị: Bẫy `m` và `Meg`
Trình biên dịch SPICE **không phân biệt chữ hoa và chữ thường**. Do đó, cả `m` và `M` đều được quy ước là **milli** ($10^{-3}$).

| Ký hiệu trong SPICE | Hệ số toán học | Ví dụ nhập liệu | Giá trị thực tế hiểu bởi SPICE |
| :---: | :---: | :--- | :--- |
| **`T`**, **`G`** | $10^{12}$, $10^9$ | `2.4G` | $2,4 \times 10^9\,\text{Hz}$ ($2,4\,\text{GHz}$) |
| **`Meg`** | $10^6$ | `1Meg` | $1\,000\,000\,\Omega$ ($1\,\text{M}\Omega$) |
| **`k`** | $10^3$ | `10k` | $10\,000\,\Omega$ ($10\,\text{k}\Omega$) |
| **`m`** (hoặc **`M`**) | $10^{-3}$ | `10m` | $0,01$ ($10\,\text{m}\Omega$ hoặc $10\,\text{ms}$) |
| **`u`** | $10^{-6}$ | `10u` | $10\,\mu\text{F}$ hoặc $10\,\mu\text{s}$ |
| **`n`**, **`p`**, **`f`** | $10^{-9}, 10^{-12}, 10^{-15}$ | `50f` | $50\,\text{fF} = 50 \times 10^{-15}\,\text{F}$ |

> [!CAUTION]
> **Cảnh báo lỗi kinh điển:** `10M` là $10\,\text{milli}$, **không phải** $10\,\text{Mega}$. Nếu muốn nhập điện trở $1\,\text{M}\Omega$, bắt buộc phải gõ `1Meg`. Chữ cái đứng ngay sau tiền tố bị bỏ qua (ví dụ `10nF` vẫn là $10\,\text{nF}$), nhưng nếu gõ `1F` thì SPICE sẽ hiểu là $1\,\text{femto}$ ($10^{-15}$), không phải $1\,\text{Farad}$!

### 3.3. Cú pháp Nguồn kích thích
Các cú pháp nguồn điện áp thường gặp:
```spice
V1 vdd 0 DC 5.0                             ; Nguồn điện áp DC 5 V không đổi
V2 in  0 SINE(0 1.0 1k)                     ; Nguồn hình sin: Offset 0V, Biên độ đỉnh 1V, 1 kHz
V3 clk 0 PULSE(0 5.0 0 10n 10n 500u 1000u)  ; Nguồn xung: V1 V2 Tdelay Trise Tfall Ton Tperiod
V4 in  0 AC 1.0 0                           ; Nguồn AC tín hiệu nhỏ: Biên độ 1V, Pha 0 độ
```

> [!TIP]
> **Nguồn xung tích hợp kích thích AC:** Có thể khai báo một nguồn duy nhất vừa phát xung PULSE vừa có biên độ AC:
> ```spice
> Vin in 0 PULSE(0 5.0 0 10n 10n 500u 1000u) AC 1
> ```
> Cấu hình này cho phép chạy cả phân tích quá độ `.tran` lẫn phân tích tần số `.ac` mà không cần thay đổi nguồn!

### 3.4. Bốn chế độ phân tích cơ bản

| Chế độ phân tích | Câu hỏi vật lý cần trả lời | Bản chất tính toán | Ví dụ cú pháp |
| :--- | :--- | :--- | :--- |
| **`.op`** (Operating Point) | Mạch đang ở trạng thái phân cực nào? | Triệt tiêu đạo hàm theo thời gian ($d/dt = 0$); tụ điện hở mạch, cuộn cảm ngắn mạch. | `.op` |
| **`.dc`** (DC Sweep) | Đại lượng ngõ ra biến thiên ra sao khi quét nguồn vào? | Thực hiện chuỗi các phân tích `.op` liên tiếp khi thay đổi điện áp nguồn. | `.dc V1 0 10 0.1` |
| **`.tran`** (Transient) | Dạng sóng điện áp và dòng điện thay đổi theo thời gian như thế nào? | Tích phân số giải hệ phương trình vi phân theo miền thời gian. | `.tran 0 1m 0 0.1u` |
| **`.ac`** (AC Analysis) | Mạch phản ứng thế nào ở các dải tần số khác nhau? | Tuyến tính hóa mạch quanh điểm tĩnh DC và quét đáp ứng tần số góc. | `.ac dec 20 10 1Meg` |

*Lưu ý khi thiết lập `.tran`:* Cú pháp đầy đủ là `.tran <Tstep> <Tstop> [Tstart [dTmax]]`. Trong đó, `dTmax` là bước thời gian cực đại. Nên đặt `dTmax` nhỏ hơn hằng số thời gian $\tau$ nhiều lần (ví dụ $\le \tau/1000$, như `0.1u` đối với mạch có $\tau = 100\,\mu\text{s}$) để dạng sóng trơn tru và câu lệnh `.meas` bắt chính xác sườn xung dốc.

### 3.5. Đo lường tự động bằng câu lệnh `.meas` tham số hóa
Thay vì đặt con trỏ chuột đo thủ công dễ sai lệch, lệnh `.meas` giúp SPICE tự động trích xuất các thông số kỹ thuật và ghi vào tệp **SPICE Error Log** (phím tắt `Ctrl + L`). Để tái sử dụng cho các bài vi mạch với điện áp nguồn bất kỳ, nên tham số hóa ngưỡng đo:
```spice
.param Vdd=5.0
.meas TRAN t_pd TRIG V(in)={0.5*Vdd} RISE=1 TARG V(out)={0.5*Vdd} RISE=1  ; Trễ 50%
.meas TRAN t_r  TRIG V(out)={0.1*Vdd} RISE=1 TARG V(out)={0.9*Vdd} RISE=1 ; Sườn tăng 10%-90%
.meas TRAN t_f  TRIG V(out)={0.9*Vdd} FALL=1 TARG V(out)={0.1*Vdd} FALL=1 ; Sườn giảm 90%-10%
.meas TRAN I_peak_chg MAX I(C1)                                           ; Đỉnh dòng nạp
.meas TRAN I_peak_dis MIN I(C1)                                           ; Đỉnh dòng xả
.meas AC   Av_max MAX mag(V(out))                                         ; Độ lợi cực đại
.meas AC   f_c WHEN mag(V(out))=Av_max/sqrt(2) FALL=1                     ; Tần số cắt -3dB
```

### 3.6. Khảo sát tham số với `.param` và `.step`
Cho phép quét một tập hợp các giá trị linh kiện để đánh giá độ nhạy của mạch:
```spice
.param Rval=20k
R1 in out {Rval}
.step param Rval list 5k 10k 20k 40k
```
*Lưu ý:* Giá trị linh kiện trên bản vẽ sơ đồ phải đặt trong dấu ngoặc nhọn `{Rval}` để LTspice hiểu đó là biến số.

### 3.7. Mạch RC và Mô hình trễ cổng logic CMOS
Mạch RC nối tiếp là mô hình vật lý cơ sở của mọi cổng vi mạch CMOS:
```
           R1 (10k)
   in -----/\/\/\/\/-----+------- out (Điện áp trên tụ)
                         |
                       +---+
                       |   | C1 (2nF)
                       +---+
                         |
                        GND (Nút 0)
```
- **Hằng số thời gian:** $\tau = R \cdot C$.  
  *(Ví dụ minh họa lý thuyết: Với $R = 10\,\text{k}\Omega, C = 2\,\text{nF} \implies \tau = 10\,\text{k}\Omega \times 2\,\text{nF} = 20\,\mu\text{s}$).*
- **Nạp điện ($0 \le t < T_{on}$):** $v_C(t) = V_0 (1 - e^{-t/\tau})$.
- **Xả điện ($T_{on} \le t < T_{period}$, $t' = t - T_{on}$):** $v_C(t') = v_C(T_{on}) \cdot e^{-t'/\tau}$.
- **Trễ 50%:** $t_{50\%} = \tau \ln(2) \approx 0,693 \cdot RC$.  
  *(Với ví dụ trên: $t_{50\%} \approx 0,693 \times 20\,\mu\text{s} \approx 13,86\,\mu\text{s}$).*
- **Thời gian sườn tăng (10%–90%):** $t_r = \tau \ln(9) \approx 2,197 \cdot RC \approx 2,2 \cdot RC$.  
  *(Với ví dụ trên: $t_r \approx 2,197 \times 20\,\mu\text{s} \approx 43,94\,\mu\text{s} \approx 44\,\mu\text{s}$).*
- **Tần số cắt $-3\,\text{dB}$:** $f_c = \frac{1}{2\pi RC}$; tại $f_c$, góc pha bằng $-45^\circ$, biên độ suy giảm $-3,01\,\text{dB}$.  
  *(Với ví dụ trên: $f_c = \frac{1}{2\pi \times 20\,\mu\text{s}} \approx 7,958\,\text{kHz} \approx 7,96\,\text{kHz}$).*

> [!IMPORTANT]
> **Cầu nối sang Thiết kế VLSI (Lab 1):**  
> Khi cổng Inverter CMOS chuyển trạng thái logic, tụ tải ngõ ra $C_L$ phóng/nạp qua kênh dẫn của MOSFET. Kênh dẫn này được mô hình hóa xấp xỉ bằng một điện trở hiệu dụng $R_{on}$. Do đó, thời gian trễ truyền lan của cổng đảo được ước lượng trực tiếp bằng công thức:
> $$t_{pd} \approx 0,69 \cdot R_{on} \cdot C_L$$

### 3.8. Quy ước chiều dòng điện và Cực tính linh kiện trong SPICE
Trong SPICE, dòng điện qua một linh kiện hai cực được quy ước **chảy từ cực dương (Node +) sang cực âm (Node -)** theo thứ tự khai báo trong Netlist.
- Với khai báo `C1 out 0 5n`, cực dương là nút `out`, cực âm là nút `0`.
- **Khi nạp:** Dòng điện đi từ ngoài vào nút `out` rồi xuống đất qua $C_1 \implies I(C1) > 0$.
- **Khi xả:** Tụ điện phóng điện ngược từ `out` về nguồn $\implies$ Dòng đi từ nút `0` ngược lên `out` $\implies I(C1) < 0$.
- *Lưu ý:* Chiều dòng điện trên đồ thị phụ thuộc vào thứ tự nút trong Netlist và hướng đặt linh kiện trên sơ đồ. Nếu xoay tụ $180^\circ$, cực dương nối xuống đất thì đồ thị dòng điện sẽ bị đảo dấu âm/dương.

### 3.9. Phím tắt thao tác nhanh trong LTspice
- `F2`: Chọn linh kiện (Component) | `R`, `C`, `L`: Đặt nhanh điện trở, tụ điện, cuộn cảm
- `F3`: Vẽ dây nối (Wire) | `G`: Đặt cọc nối đất (Ground - Node 0)
- `F4`: Đặt nhãn tên nút (Net Label) | `S`: Nhập câu lệnh SPICE Directive
- `F5`: Xóa linh kiện (Delete) | `Ctrl + R`: Xoay linh kiện 90° | `Space`: Thu phóng vừa màn hình

---

## 4. CÂU HỎI CHUẨN BỊ TRƯỚC KHI ĐẾN LỚP (PRE-LAB)
*(Sinh viên hoàn thành ra giấy hoặc soạn tệp văn bản và nộp cho Giảng viên/Trợ giảng trước khi bắt đầu buổi thực hành)*

1. **Câu P1 (Tiền tố đơn vị SPICE):**  
   Một sinh viên nhập giá trị điện trở là `4.7M` và tụ điện là `22uF`. SPICE sẽ hiểu giá trị của hai linh kiện này lần lượt là bao nhiêu? Muốn khai báo điện trở $4,7\,\text{M}\Omega$ và tụ điện $22\,\text{pF}$, cú pháp đúng trong SPICE là gì?
2. **Câu P2 (Tính toán mạch phân áp DC):**  
   Cho mạch phân áp gồm nguồn $V_{in} = 10,0\,\text{V}$, $R_1 = 15\,\text{k}\Omega$, $R_2 = 10\,\text{k}\Omega$ (nối xuống đất).  
   a) Tính điện áp tĩnh ngõ ra $V_{out}$ và dòng điện tĩnh $I$ chạy qua mạch.  
   b) Dự đoán độ dốc $\frac{dV_{out}}{dV_{in}}$ khi quét điện áp ngõ vào từ $0\,\text{V}$ đến $10\,\text{V}$.
3. **Câu P3 (Tính toán thông số quá độ mạch RC):**  
   Cho mạch RC nối tiếp gồm $R = 5\,\text{k}\Omega$ và $C = 10\,\text{nF}$, kích thích bởi bước nhảy điện áp từ $0\,\text{V} \to 5,0\,\text{V}$.  
   Tính: Hằng số thời gian $\tau$, thời gian trễ 50% ($t_{50\%}$), thời gian sườn tăng 10%–90% ($t_r$), và tần số cắt $-3\,\text{dB}$ ($f_c$).
4. **Câu P4 (Thiết lập nguồn xung PULSE):**  
   Để tụ điện trong mạch ở Câu P3 có đủ thời gian nạp đạt trên $99\%$ điện áp nguồn và sau đó xả về dưới $1\%$, hãy xác định giá trị tối thiểu của độ rộng xung $T_{on}$ và chu kỳ xung $T_{period}$.
5. **Câu P5 (Độ nhạy tham số):**  
   Nếu ta giữ nguyên điện trở $R$ và tăng điện dung tụ điện lên gấp đôi ($C' = 2C$), thời gian trễ $t_{pd}$ và tần số cắt $f_c$ của mạch sẽ thay đổi như thế nào?
6. **Câu P6 (Phác thảo dạng sóng nạp không đầy):**  
   Giả sử cấp vào mạch RC một xung điện áp có độ rộng chỉ bằng $T_{on} = 3\tau$. Hãy tính điện áp đỉnh mà tụ đạt được (theo Volt và theo phần trăm $V_0$). Tụ đã nạp đầy chưa? Vẽ phác thảo dạng sóng $v_C(t)$ trong trường hợp này.

---

## 5. KẾ HOẠCH VÀ PHÂN BỔ THỜI LƯỢNG THỰC HÀNH

Quá trình thực hành Lab 0 được tổ chức trực tiếp tại phòng máy theo khung giờ chuẩn:

| Phân đoạn nội dung | Khung chuẩn 135 phút (3 tiết) | Khung mở rộng 225 phút (5 tiết - Tùy chọn) | Vai trò tổ chức lớp |
| :--- | :---: | :---: | :--- |
| **1. Giới thiệu công cụ & Thư mục dự án** | 15 phút | 20 phút | Giảng viên hướng dẫn quy trình, tạo folder. |
| **2. Ex0.1: Phân tích mạch phân áp DC** | 20 phút | 35 phút | Giảng viên làm mẫu, sinh viên thao tác theo. |
| **3. Ex0.2: Mạch RC Transient (Trọng tâm)** | 40 phút | 60 phút | Giảng viên hướng dẫn từng bước, SV thực hành đo `.meas`. |
| **4. Ex0.3: Phân tích AC & Biểu đồ Bode** | 25 phút | 40 phút | Giảng viên giải thích tần số cắt, SV đo đáp ứng. |
| **5. Ex0.4: Quét tham số `.step`** | 20 phút | 30 phút | Sinh viên tự thực hiện dưới sự hỗ trợ của GV. |
| **6. Ex0.5: Giới thiệu mô hình MOSFET C5N** | 10 phút | 15 phút | Giảng viên demo nhanh, định hướng sang Lab 1. |
| **7. Tổng kết & Giao nhiệm vụ đóng gói** | 05 phút | 25 phút | Kiểm tra kết quả tại chỗ, hướng dẫn nộp bài. |

---

## 6. NỘI DUNG THỰC HÀNH TẠI LỚP (PHẦN A)

> [!TIP]
> **Tổ chức thư mục làm việc chuẩn:**  
> Tạo thư mục làm việc theo cấu trúc `lab00_MSSV_HoTen/` trên máy tính. Toàn bộ các tệp vẽ sơ đồ `.asc`, tệp netlist `.sp` và tệp mô hình `C5_models.txt` (lấy từ `04 - Models_and_Libraries/C5_models.txt`) phải được lưu trữ khoa học trong thư mục này.

---

### Ex0.1 — Phân tích điểm làm việc DC và đặc tuyến truyền đạt của mạch phân áp
*(Thời lượng: 20–35 phút | Hình thức: Giảng viên làm mẫu, sinh viên thực hành theo)*

**1. Mục đích:** Làm quen với việc nhập sơ đồ nguyên lý, khai báo nguồn DC, chạy phân tích điểm tĩnh `.op` và quét DC `.dc`.

**2. Các bước thực hiện:**
1. Tạo sơ đồ mới (**File $\to$ New Schematic**), lưu tệp với tên `ex01_divider.asc`.
2. Đặt nguồn điện áp $V_1 = 5.0\,\text{V}$, điện trở $R_1 = 12\,\text{k}\Omega$, $R_2 = 18\,\text{k}\Omega$, đặt cọc đất `GND` tại chân dưới của $R_2$.
3. Đặt nhãn tên nút ngõ vào là `in` và nút giữa hai điện trở là `out`.
4. Nhấn phím `S`, nhập lệnh `.op`, nhấn biểu tượng **Run (hình người chạy)**. Đọc kết quả điện áp tĩnh tại nút `out` và dòng điện qua $R_1$ trong cửa sổ Operating Point.
5. Chuyển sang quét DC: Nhấp chuột phải vào dòng lệnh mô phỏng đổi thành `.dc V1 0 10 0.1`. Nhấn **Run**. Đưa que đo nhấp vào nút `out` để quan sát đặc tuyến truyền đạt $V_{out} = f(V_{in})$.

**3. Câu hỏi tư duy:**
- *Câu hỏi 1:* Tại sao bắt buộc phải có nút đất `0` trong Netlist SPICE? Nếu xóa cọc đất đi, LTspice sẽ xuất hiện thông báo lỗi gì?
- *Câu hỏi 2:* Dự đoán độ dốc của đường đặc tuyến $V_{out}$ theo $V_{in}$ trước khi chạy mô phỏng, sau đó đối chiếu với đồ thị quét DC thực tế thu được.

**4. Sản phẩm nghiệm thu Ex0.1:**
- Sơ đồ mạch phân áp `ex01_divider.asc`.
- Tệp Netlist `ex01_divider.sp` trích xuất từ menu **View $\to$ SPICE Netlist**.
- Bảng so sánh điện áp $V_{out}$ và dòng điện $I(R_1)$ giữa lý thuyết tính tay và kết quả mô phỏng `.op`.

---

### Ex0.2 — Mô phỏng quá độ nạp và xả của mạch RC (Bài thực hành trọng tâm)
*(Thời lượng: 40–60 phút | Hình thức: Giảng viên hướng dẫn từng bước, sinh viên thực hành độc lập)*

**1. Mục đích:** Làm chủ phân tích miền thời gian `.tran`, quan sát quá trình nạp/xả tụ điện, khai thác câu lệnh `.meas` tham số hóa để đo tự động $t_{pd}, t_r, t_f$ và đỉnh dòng điện.

**2. Các bước thực hiện:**
1. Tạo sơ đồ mới lưu tên `ex02_rc_tran.asc`. Dựng mạch RC nối tiếp gồm $R_1 = 20\,\text{k}\Omega$ và $C_1 = 5\,\text{nF}$ nối xuống đất.
2. Cấu hình nguồn xung tại ngõ vào `in`: Nhấp chuột phải vào nguồn, chọn **Advanced $\to$ PULSE**:
   - $V_1 = 0$, $V_2 = 5.0$, $T_{delay} = 0$, $T_{rise} = 10\text{n}$, $T_{fall} = 10\text{n}$, $T_{on} = 500\mu$, $T_{period} = 1000\mu$.  
   *(Nhận xét: Thời gian sườn $10\,\text{ns}$ rất nhỏ so với $\tau = 100\,\mu\text{s}$, xấp xỉ nguồn xung lý tưởng khi $t_r, t_f \ll \tau$).*
3. Nhập lệnh phân tích quá độ: `.tran 0 1m 0 0.1u`.  
   *(Lưu ý: `dTmax = 0.1u` nhỏ hơn $\tau = 100\,\mu\text{s}$ tới 1000 lần, đảm bảo độ chính xác cao).*
4. Nhấn phím `S`, nhập khối câu lệnh đo lường tự động `.meas` tham số hóa:
   ```spice
   .param Vdd=5.0
   .meas TRAN t_pd TRIG V(in)={0.5*Vdd} RISE=1 TARG V(out)={0.5*Vdd} RISE=1
   .meas TRAN t_r  TRIG V(out)={0.1*Vdd} RISE=1 TARG V(out)={0.9*Vdd} RISE=1
   .meas TRAN t_f  TRIG V(out)={0.9*Vdd} FALL=1 TARG V(out)={0.1*Vdd} FALL=1
   .meas TRAN I_peak_chg MAX I(C1)
   .meas TRAN I_peak_dis MIN I(C1)
   ```
5. Nhấn **Run (hình người chạy)**. Đưa que đo xem điện áp `V(in)` và `V(out)`. Mở **View $\to$ SPICE Error Log** (`Ctrl + L`) để đọc các số đo tự động.
6. Thêm một khung đồ thị (**Add Plot Pane**), đưa que đo vào thân tụ $C_1$ để quan sát dạng sóng dòng điện nạp/xả.

**3. Câu hỏi tư duy:**
- *Câu hỏi 1:* Tại sao điện áp trên tụ điện $v_C(t)$ không thể thay đổi tức thời khi có xung điện áp nhảy bậc ở ngõ vào?
- *Câu hỏi 2:* Dùng con trỏ chuột (Cursor) đo điện áp $V(out)$ tại thời điểm $t = \tau = 100\,\mu\text{s}$. Giá trị này đạt bao nhiêu phần trăm so với $5,0\,\text{V}$ và có khớp với lý thuyết $63,2\%$ không?
- *Câu hỏi 3:* Nếu tăng giá trị điện dung lên gấp đôi ($C = 10\,\text{nF}$), thời gian trễ $t_{pd}$ và sườn tăng $t_r$ thay đổi như thế nào?
- *Câu hỏi 4:* Tính điện áp trên tụ $v_C$ tại thời điểm $t = T_{on} = 500\,\mu\text{s}$ trước, từ đó suy ra dòng điện đỉnh xả lý thuyết $I_{peak,dis}$. So sánh độ lớn của $|I_{peak,dis}|$ với đỉnh dòng nạp $I_{peak,chg}$ và giải thích vì sao có sự chênh lệch nhỏ ($\,\sim 0,67\%$) giữa hai giá trị này.

**4. Sản phẩm nghiệm thu Ex0.2:**
- Sơ đồ mạch `ex02_rc_tran.asc`.
- Tệp Netlist `ex02_rc_tran.sp`.
- Dạng sóng chụp màn hình gồm 2 đồ thị: Điện áp $V(in), V(out)$ và Dòng điện $I(C1)$.
- Bảng đối chiếu số liệu đo SPICE `.meas` so với công thức giải tích ($\tau = RC$, $t_{50\%} = \ln(2) RC$, $t_r = \ln(9) RC$, $I_{peak,chg}$, $I_{peak,dis}$).

---

### Ex0.3 — Phân tích đáp ứng tần số AC và Biểu đồ Bode
*(Thời lượng: 25–40 phút | Hình thức: Giảng viên hướng dẫn, sinh viên thực hành)*

**1. Mục đích:** Khảo sát đặc tính lọc thông thấp của mạch RC trong miền tần số; xác định tần số cắt $-3\,\text{dB}$, độ dịch pha và thực hiện phép kiểm chéo độc lập với phép đo miền thời gian.

**2. Các bước thực hiện:**
1. Lưu sơ đồ mới thành `ex03_rc_ac.asc` (dựa trên mạch RC của Ex0.2). Nhấp chuột phải vào nguồn điện áp, trong ô **Small Signal AC Analysis (AC)**, nhập biên độ `1`.
2. Nhấn phím `S`, đổi lệnh mô phỏng thành: `.ac dec 20 10 1Meg` (quét từ $10\,\text{Hz}$ đến $1\,\text{MHz}$, mỗi thập kỷ tần số lấy 20 điểm).
3. Nhập câu lệnh `.meas` tìm tần số cắt:
   ```spice
   .meas AC Av_max MAX mag(V(out))
   .meas AC f_c WHEN mag(V(out))=Av_max/sqrt(2) FALL=1
   ```
4. Nhấn **Run**, que đo nhấp vào nút `out` để hiển thị biểu đồ Bode (trục trái biểu thị biên độ theo dB, trục phải biểu thị góc pha theo độ).

**3. Câu hỏi tư duy:**
- *Câu hỏi 1:* Vì sao mạch RC lại cho tín hiệu tần số thấp đi qua và làm suy giảm mạnh tín hiệu ở tần số cao?
- *Câu hỏi 2:* Tại tần số cắt $f_c$, biên độ suy giảm bao nhiêu dB so với vùng tần số thấp và góc pha giữa điện áp ra và vào bằng bao nhiêu độ?
- *Câu hỏi 3:* Bản chất khác biệt giữa chế độ mô phỏng miền thời gian `.tran` và miền tần số `.ac` là gì?

**4. Sản phẩm nghiệm thu Ex0.3:**
- Đồ thị biểu đồ Bode có gắn con trỏ chuột (Cursor) tại điểm $-3\,\text{dB}$ và $-45^\circ$.
- Tệp Netlist `ex03_rc_ac.sp`.
- Bảng so sánh tần số cắt đo được từ SPICE `.meas` với công thức giải tích $f_c = \frac{1}{2\pi R C}$.
- **Phép kiểm chéo hai miền độc lập:** Tính tích số $t_r \cdot f_c$ từ kết quả đo của Ex0.2 ($t_r$) và Ex0.3 ($f_c$), so sánh với giá trị giải tích lý thuyết:
  $$t_r \cdot f_c = (\ln(9) \cdot RC) \cdot \left(\frac{1}{2\pi RC}\right) = \frac{\ln(9)}{2\pi} \approx 0,35$$

---

### Ex0.4 — Khảo sát độ nhạy tham số với `.param` và `.step`
*(Thời lượng: 20–30 phút | Hình thức: Sinh viên thực hiện dưới sự hướng dẫn)*

**1. Mục đích:** Làm chủ kỹ thuật quét tham số linh kiện tự động; chứng minh bằng thực nghiệm quy luật biến thiên tuyến tính của độ trễ theo điện trở.

**2. Các bước thực hiện:**
1. Lưu sơ đồ mới thành `ex04_rc_step.asc`. Trên sơ đồ mạch RC quá độ, thay đổi giá trị của điện trở $R_1$ thành biến `{Rval}`.
2. Thêm các dòng lệnh định nghĩa và quét tham số:
   ```spice
   .param Rval=20k
   .step param Rval list 5k 10k 20k 40k
   ```
3. Chạy lại mô phỏng `.tran 0 1m 0 0.1u` với lệnh đo trễ `t_pd`.
4. Mở **SPICE Error Log** (`Ctrl + L`) để quan sát 4 giá trị trễ $t_{pd}$ tương ứng với 4 bước quét.
5. Nhấp chuột phải vào cửa sổ Error Log, chọn **Plot .step'ed .meas data** để vẽ đồ thị hàm số $t_{pd} = f(R)$.

**3. Câu hỏi tư duy:**
- *Câu hỏi 1:* Tại sao thời gian trễ truyền lan $t_{pd}$ lại tăng tuyến tính theo giá trị điện trở? Giải thích bản chất đối với mạch RC tuyến tính.
- *Câu hỏi 2:* Tính độ dốc lý thuyết của đồ thị $\text{Slope} = \ln(2) \cdot C$. So sánh với độ dốc thực nghiệm trích xuất từ đồ thị $\frac{\Delta t_{pd}}{\Delta R}$.
- *Câu hỏi 3:* Nếu ta giữ nguyên điện trở $R$ và quét giá trị tụ điện $C$ thì đồ thị trễ sẽ có dạng như thế nào?

**4. Sản phẩm nghiệm thu Ex0.4:**
- Bảng số liệu trễ $t_{pd}$ qua 4 giá trị điện trở ($5\,\text{k}\Omega, 10\,\text{k}\Omega, 20\,\text{k}\Omega, 40\,\text{k}\Omega$).
- Tệp Netlist `ex04_rc_step.sp`.
- Đồ thị thực nghiệm $t_{pd} - R$ trích xuất từ LTspice.
- Tính toán và xác nhận độ dốc lý thuyết so với độ dốc đo đạc thực nghiệm.

---

### Ex0.5 — Giới thiệu liên kết mô hình MOSFET công nghệ C5N
*(Thời lượng: 10–15 phút | Hình thức: Giảng viên demo nhanh, sinh viên hoàn thiện)*

**1. Mục đích:** Tạo bước đệm chuyển tiếp từ linh kiện thụ động sang linh kiện tích cực; làm quen với lệnh gọi tệp mô hình thư viện công nghệ ngoài `.include`.

**2. Các bước thực hiện:**
1. Sao chép tệp `C5_models.txt` từ thư mục `04 - Models_and_Libraries/C5_models.txt` vào thư mục làm việc `lab00_MSSV_HoTen/`.
2. Mở sơ đồ mới lưu tên `ex05_nmos_test.asc`, lấy linh kiện transistor NMOS 4 cực (`nmos4`).
3. Nhấp chuột phải vào transistor: Đặt tên Model là **`N`**, chiều rộng kênh $W = 1.2\,\mu\text{m}$ (`1.2u`), chiều dài kênh $L = 0.6\,\mu\text{m}$ (`0.6u`).
4. Đặt nguồn $V_{DS} = 5.0\,\text{V}$ vào cực má (Drain), nguồn $V_{GS} = 5.0\,\text{V}$ vào cực cổng (Gate); cực nguồn (Source) và cực thân (Bulk) nối chung xuống đất.
5. Nhấn phím `S`, chèn lệnh liên kết tệp mô hình: `.include C5_models.txt`.
6. Đặt lệnh `.op` và nhấn **Run (hình người chạy)**. Đọc dòng điện cực má $I_D$ trong kết quả Operating Point.

**3. Câu hỏi định hướng cho Lab 1:**
- *Câu hỏi 1:* Tại sao SPICE cần tệp mô hình riêng biệt (`.model`) mà không thể khai báo MOSFET đơn giản như một điện trở?
- *Câu hỏi 2:* Sử dụng các tham số công nghệ danh định ($K'_n = 120\,\mu\text{A/V}^2$, $V_{tn} = 0,70\,\text{V}$), hãy tính dòng điện cực má bão hòa $I_{D,sat}$ theo công thức bậc hai Shichman-Hodges. So sánh với dòng điện $I_D$ đo được từ kết quả mô phỏng `.op` và nêu ít nhất hai hiện tượng vật lý trong transistor dưới-micron (submicron) gây ra sự chênh lệch này.

**4. Sản phẩm nghiệm thu Ex0.5:**
- Sơ đồ mạch phân cực `ex05_nmos_test.asc` và Netlist `ex05_nmos_test.sp`.
- Giá trị dòng điện $I_D$ ghi nhận từ kết quả `.op`.
- Bảng so sánh dòng điện lý thuyết bậc hai và mô phỏng SPICE Level 3 kèm nhận xét định tính.

---

## 7. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (PHẦN B)

Sau khi hoàn thành buổi thực hành tại lớp, sinh viên tiến hành **hoàn thiện và đóng gói thư mục dự án Lab 0** với các yêu cầu sau:

### 1. Cấu trúc thư mục dự án nộp bài (`lab00_MSSV_HoTen/`)
```
lab00_MSSV_HoTen/
│
├── schematics/             # Chứa toàn bộ 5 tệp sơ đồ nguyên lý
│   ├── ex01_divider.asc
│   ├── ex02_rc_tran.asc
│   ├── ex03_rc_ac.asc
│   ├── ex04_rc_step.asc
│   └── ex05_nmos_test.asc
│
├── netlists/               # Chứa toàn bộ 5 tệp Netlist trích xuất
│   ├── ex01_divider.sp
│   ├── ex02_rc_tran.sp
│   ├── ex03_rc_ac.sp
│   ├── ex04_rc_step.sp
│   └── ex05_nmos_test.sp
│
├── waveforms/              # Chứa ảnh chụp dạng sóng và kết quả đo rõ nét
│   ├── ex01_dc_sweep.png
│   ├── ex02_transient_v_i.png
│   ├── ex03_bode_plot.png
│   ├── ex04_step_plot.png
│   └── ex05_op_point.png   # Ảnh chụp cửa sổ .op hoặc bảng thông số ID
│
├── C5_models.txt           # Tệp thư viện mô hình C5N chuẩn (Level 3)
└── Bao_Cao_Lab00_MSSV.pdf  # Báo cáo kỹ thuật tổng kết (từ 3 đến 4 trang)
```

### 2. Nội dung báo cáo kỹ thuật tổng kết (3–4 trang)
Báo cáo trình bày khoa học, súc tích gồm 4 phần:
1. **Đáp án phần Pre-lab:** Trình bày lời giải 6 câu hỏi chuẩn bị trước khi đến lớp.
2. **Bảng tổng hợp kết quả Benchmark:** Bảng so sánh đầy đủ giữa Lý thuyết giải tích và Đo đạc SPICE cho cả 5 bài Ex0.1 – Ex0.5, kèm cột tính sai lệch tương đối $\text{Error (\%)}$ và kết quả kiểm chéo $t_r \cdot f_c$.
3. **Trả lời các câu hỏi tư duy trọng tâm:** Trình bày ngắn gọn câu trả lời cho các câu hỏi tư duy đã nêu trong từng bài Ex.
4. **Thử nghiệm lỗi có chủ đích (Deliberate Fault Injection):** Để rèn luyện kỹ năng chẩn đoán, sinh viên bắt buộc chủ động tạo ra **ít nhất 01 lỗi kỹ thuật có chủ đích** (ví dụ: xóa cọc đất ở Ex0.1, hoặc bỏ dấu ngoặc nhọn `{}` ở Ex0.4, hoặc gõ nhầm tiền tố `10M`), chụp ảnh thông báo lỗi của LTspice, giải thích cơ chế phát sinh lỗi và cách khắc phục.

---

## 8. TIÊU CHÍ KIỂM CHỨNG KỸ THUẬT & SAI LỆCH CHẤP NHẬN

Mỗi kết quả đo tự động bằng `.meas` được đánh giá độ chính xác bằng công thức:
$$\text{Sai lệch tương đối (\%)} = \frac{|\text{Giá trị SPICE} - \text{Giá trị Lý thuyết}|}{\text{Giá trị Lý thuyết}} \times 100\%$$

- **Chỉ tiêu đối với mạch RC (Ex0.1 – Ex0.4):** Sai lệch tương đối $\le 2,0\%$. Mạch RC là mạng tuyến tính lý tưởng nên khi thiết lập đúng bước thời gian $dT_{max} \le \tau/1000$ (`0.1u`), sai số mô phỏng thông thường sẽ rất nhỏ ($< 0,1\%$).
- **Đối với bài MOSFET (Ex0.5):** Không áp dụng chỉ tiêu sai số $\le 2\%$. Sinh viên được yêu cầu **nêu và giải thích sự chênh lệch** giữa mô hình giải tích bậc hai thô và mô hình SPICE Level 3 (dòng thực tế thường thấp hơn từ $30\%$ đến $40\%$ do bão hòa vận tốc hạt dẫn và suy giảm độ linh động).

---

## 9. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP (SELF-DEBUGGING)

| Hiện tượng lỗi | Nguyên nhân cốt lõi | Hướng tự kiểm tra và xử lý |
| :--- | :--- | :--- |
| **Không chạy được, báo *Singular Matrix* hoặc *no DC path*** | Thiếu nút đất tham chiếu `0`. | Kiểm tra xem mạch đã đặt cọc đất `GND` chưa. |
| **Báo lỗi *Node is floating*** | Có chân linh kiện bị hở hoặc chưa nối dây. | Dùng phím `F3` kiểm tra các mối nối có xuất hiện chấm vuông không. |
| **Lệnh `.step` ra các đường trùng khít nhau** | Quên đặt dấu ngoặc nhọn `{}` quanh tên biến. | Kiểm tra giá trị điện trở trên sơ đồ: phải là `{Rval}`, không phải `Rval`. |
| **Dòng điện nạp của tụ bị âm** | Tụ điện bị đặt ngược cực tính (+/-) trong netlist. | Chọn tụ điện, nhấn `Ctrl + R` xoay 2 lần để đảo lại chiều cực. |
| **Báo lỗi *Unknown Model / Subcircuit*** | Sai tên model trong Netlist hoặc thiếu `.include`. | Mở tệp model kiểm tra chính xác tên (`N` chứ không phải `NMOS`). |
| **Đồ thị trễ `.meas` bị răng cưa, sai lệch lớn** | Bước thời gian mô phỏng `dTmax` bị quá thô. | Sửa lệnh `.tran`: thêm `0.1u` vào tham số cuối cùng: `.tran 0 1m 0 0.1u`. |

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

| Hạng mục đánh giá | Chuẩn CLO | Điểm | Tiêu chí đạt điểm tối đa |
| :--- | :---: | :---: | :--- |
| **Chuẩn bị Pre-lab (Nộp đầu buổi)** | **CLO1** | **1.5 điểm** | Trả lời đầy đủ, chính xác 6 câu hỏi Pre-lab; hiểu đúng đơn vị, quy tắc mạch phân áp và động học nạp xả RC. |
| **Kỹ năng thao tác tại lớp (Ex0.1 – Ex0.3)** | **CLO2** | **3.5 điểm** | Dựng sơ đồ đúng chuẩn, vận hành đủ các chế độ `.op`, `.tran`, `.ac`; trích xuất đúng số đo tự động bằng `.meas` với sai số $\le 2\%$; thực hiện đúng kiểm chéo $t_r \cdot f_c$. |
| **Khảo sát tham số & MOSFET (Ex0.4 – Ex0.5)** | **CLO2** | **2.0 điểm** | Quét đúng 4 bước giá trị $R$, vẽ được đồ thị thực nghiệm và xác nhận độ dốc; liên kết đúng thư viện C5N và đo được dòng $I_D$. |
| **Dự đoán – Đo đạc – Giải thích sai lệch** | **CLO1, CLO2** | **1.5 điểm** | Thể hiện rõ quy trình khoa học: dự đoán trước, đo bằng SPICE, đối chiếu và giải thích sắc bén các chênh lệch vật lý (đặc biệt là dòng xả Ex0.2 và dòng MOSFET Ex0.5). |
| **Đóng gói dự án & Báo cáo kỹ thuật (Phần B)** | **CLO4** | **1.5 điểm** | Thư mục dự án đầy đủ 5 schematic, 5 netlist, waveforms và C5_models.txt; báo cáo 3–4 trang trình bày trung thực, có thử nghiệm lỗi có chủ đích. |\n