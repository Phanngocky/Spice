# THỰC HÀNH THIẾT KẾ VLSI — BÀI 0
# LÀM QUEN MÔ PHỎNG SPICE VỚI LTSPICE & MẠCH RC CƠ BẢN

---
**Học phần:** Thực hành Thiết kế VLSI (Mã học phần: `5505382`)  
**Bộ môn:** Điện tử - Viễn thông | **Khoa:** Điện - Điện tử | **Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Liên hệ giáo trình:** Chương 1 (Quy trình thiết kế vi mạch Full-Custom), Chương 3 (Mô hình trễ RC và điện trở kênh dẫn)  
**Công cụ sử dụng:** LTspice (phiên bản XVII hoặc LTspice 2025 trở lên)  
**Thời lượng đề xuất:** 
- *Phần A (Tại lớp):* 1 buổi thực hành trực tiếp tại phòng máy (135 phút chuẩn hoặc 225 phút mở rộng).
- *Phần B (Tại nhà):* Hoàn thiện và đóng gói thư mục dự án Lab 0 (khoảng 1,5 đến 2 giờ).
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Hiểu được vai trò của SPICE** trong quy trình thiết kế, mô phỏng và kiểm chứng vi mạch điện tử.
2. **Xây dựng được sơ đồ nguyên lý (Schematic)**, tạo, trích xuất và đọc hiểu cú pháp tệp văn bản **Netlist**.
3. **Sử dụng thành thạo 4 chế độ phân tích cơ bản**:
   - Điểm làm việc tĩnh DC: `.op`
   - Quét điện áp DC: `.dc`
   - Đáp ứng miền thời gian (Quá độ): `.tran`
   - Đáp ứng miền tần số: `.ac`
4. **Khai thác cửa sổ đồ thị (Waveform Viewer)**, đọc chính xác kết quả mô phỏng và sử dụng câu lệnh đo tự động **`.meas`** để trích xuất các thông số quá độ ($t_{pd}, t_r, t_f$) và tần số cắt ($f_{-3\text{dB}}$).
5. **Khảo sát tham số linh kiện** bằng chỉ thị `.param` và lệnh quét `.step` để đánh giá ảnh hưởng của tham số đến đặc tính mạch.
6. **Nắm vững bản chất vật lý của mạch RC**: hiểu mối liên hệ mật thiết giữa mạch RC, hằng số thời gian $\tau$ và mô hình độ trễ của cổng logic CMOS ($t_{pd} \approx 0,69 \cdot R_{on} \cdot C_L$).
7. **Biết cách tổ chức, lưu trữ và trình bày** một thư mục dự án mô phỏng kỹ thuật hoàn chỉnh theo chuẩn mực thiết kế.

> [!NOTE]
> **Định hướng sư phạm:** Mục tiêu cốt lõi của Lab 0 là làm quen công cụ, rèn luyện kỹ năng mô phỏng và hình thành thói quen kiểm chứng kết quả. Sinh viên **chưa bắt buộc phải tự thiết kế hay phân tích sâu các tế bào CMOS** trong bài này; phần mô hình transistor MOSFET được tiếp cận ở mức độ giới thiệu để chuẩn bị cho Lab 1.

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

| Thành phần | Chi tiết chuyển giao kỹ thuật |
| :--- | :--- |
| **Dùng lại từ lab trước** | Không có (đây là bài Lab nền tảng đầu tiên của học phần). |
| **Sinh ra cho lab sau** | - **Thư mục dự án mẫu `lab00_project/`** được chuẩn hóa cấu trúc để tái sử dụng từ Lab 1 đến Lab 10.<br>- **Tệp mô hình công nghệ `C5_models.txt`** được cấu hình sẵn trong thư mục làm việc.<br>- **Khung netlist mẫu và cú pháp đo `.meas`** đo trễ tự động dùng lại cho toàn bộ các bài đo cổng logic CMOS.<br>- **Bảng đối chuẩn trễ RC cơ sở** làm mốc so sánh với độ trễ truyền lan của Inverter tại Lab 1. |

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
- **Nút đất bắt buộc phải có tên là `0` (hoặc `GND`)**: SPICE dùng nút `0` làm mốc thế chuẩn $0\,\text{V}$. Thiếu nút `0`, mạch sẽ báo lỗi ma trận suy biến (*Singular Matrix*) hoặc nút lơ lửng (*Node is floating*).
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
> **Cảnh báo lỗi kinh điển:** `10M` là $10\,\text{milli}$, **tuyệt đối không phải** $10\,\text{Mega}$. Nếu muốn nhập điện trở $1\,\text{M}\Omega$, bắt buộc phải gõ `1Meg`. Chữ cái đứng ngay sau tiền tố bị bỏ qua (ví dụ `10nF` vẫn là $10\,\text{nF}$), nhưng nếu gõ `1F` thì SPICE sẽ hiểu là $1\,\text{femto}$ ($10^{-15}$), không phải $1\,\text{Farad}$!

### 3.3. Cú pháp Nguồn kích thích
Các cú pháp nguồn điện áp thường gặp:
```spice
V1 vdd 0 DC 5.0                             ; Nguồn điện áp DC 5 V không đổi
V2 in  0 SINE(0 1.0 1k)                     ; Nguồn hình sin: Offset 0V, Biên độ đỉnh 1V, 1 kHz
V3 clk 0 PULSE(0 5.0 0 10n 10n 500u 1000u)  ; Nguồn xung: V1 V2 Tdelay Trise Tfall Ton Tperiod
V4 in  0 AC 1.0 0                           ; Nguồn AC tín hiệu nhỏ: Biên độ 1V, Pha 0 độ
```

> [!TIP]
> **Nguồn xung tích hợp kích thích AC:** Bạn có thể khai báo một nguồn duy nhất vừa phát xung PULSE vừa có biên độ AC:
> ```spice
> Vin in 0 PULSE(0 5.0 0 10n 10n 500u 1000u) AC 1
> ```
> Nguồn này cho phép chạy cả phân tích quá độ `.tran` lẫn phân tích tần số `.ac` mà không cần đổi nguồn!

### 3.4. Bốn chế độ phân tích cơ bản

| Chế độ phân tích | Câu hỏi vật lý cần trả lời | Bản chất tính toán | Ví dụ cú pháp |
| :--- | :--- | :--- | :--- |
| **`.op`** (Operating Point) | Mạch đang ở trạng thái phân cực nào? | Triệt tiêu đạo hàm theo thời gian ($d/dt = 0$); tụ điện hở mạch, cuộn cảm ngắn mạch. | `.op` |
| **`.dc`** (DC Sweep) | Đại lượng ngõ ra biến thiên ra sao khi quét nguồn vào? | Thực hiện chuỗi các phân tích `.op` liên tiếp khi thay đổi điện áp nguồn. | `.dc V1 0 10 0.1` |
| **`.tran`** (Transient) | Dạng sóng điện áp và dòng điện thay đổi theo thời gian như thế nào? | Tích phân số giải hệ phương trình vi phân theo miền thời gian. | `.tran 0 1m 0 0.1u` |
| **`.ac`** (AC Analysis) | Mạch phản ứng thế nào ở các dải tần số khác nhau? | Tuyến tính hóa mạch quanh điểm tĩnh DC và quét đáp ứng tần số góc. | `.ac dec 20 10 1Meg` |

*Lưu ý khi thiết lập `.tran`:* Cú pháp đầy đủ là `.tran <Tstep> <Tstop> [Tstart [dTmax]]`. Trong đó, `dTmax` là bước thời gian cực đại. Luôn đặt `dTmax` đủ nhỏ (ví dụ `0.1u` với mạch RC có $\tau = 100\,\mu\text{s}$) để dạng sóng trơn tru và câu lệnh `.meas` bắt chính xác sườn xung dốc.

### 3.5. Đo lường tự động bằng câu lệnh `.meas`
Thay vì đặt con trỏ chuột đo thủ công dễ sai lệch, lệnh `.meas` giúp SPICE tự động trích xuất các thông số kỹ thuật và ghi vào tệp **SPICE Error Log** (phím tắt `Ctrl + L`):
```spice
.meas TRAN t_pd TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 RISE=1  ; Đo trễ 50%
.meas TRAN t_r  TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1 ; Đo thời gian tăng 10%-90%
.meas TRAN t_f  TRIG V(out)=4.5 FALL=1 TARG V(out)=0.5 FALL=1 ; Đo thời gian giảm 90%-10%
.meas AC   Av_max MAX mag(V(out)/V(in))                       ; Tìm độ lợi cực đại
.meas AC   f_c WHEN mag(V(out)/V(in))=Av_max/sqrt(2) FALL=1   ; Đo tần số cắt -3dB
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
           R1 (20k)
   in -----/\/\/\/\/-----+------- out (Điện áp trên tụ)
                         |
                       +---+
                       |   | C1 (5nF)
                       +---+
                         |
                        GND (Nút 0)
```
- **Hằng số thời gian:** $\tau = R \cdot C$.
- **Nạp điện ($0 \le t < T_{on}$):** $v_C(t) = V_0 (1 - e^{-t/\tau})$.
- **Xả điện ($T_{on} \le t < T_{period}$, $t' = t - T_{on}$):** $v_C(t') = V_0 e^{-t'/\tau}$.
- **Trễ 50%:** $t_{50\%} = \tau \ln(2) \approx 0,693 \cdot RC$.
- **Thời gian sườn tăng (10%–90%):** $t_r = \tau \ln(9) \approx 2,197 \cdot RC \approx 2,2 \cdot RC$.
- **Tần số cắt $-3\,\text{dB}$:** $f_c = \frac{1}{2\pi RC}$; tại $f_c$, góc pha bằng $-45^\circ$, biên độ giảm còn $1/\sqrt{2}$ ($\approx -3,01\,\text{dB}$).

> [!IMPORTANT]
> **Cầu nối sang Thiết kế VLSI (Lab 1):**  
> Khi cổng Inverter CMOS chuyển từ $1 \to 0$, tụ tải ngõ ra $C_L$ xả điện xuống đất qua kênh dẫn của NMOS. Kênh dẫn này đóng vai trò như một điện trở hiệu dụng $R_{on,n}$. Do đó, thời gian trễ truyền lan của cổng đảo được ước lượng trực tiếp bằng công thức:
> $$t_{pd} \approx 0,69 \cdot R_{on} \cdot C_L$$

### 3.8. Quy ước chiều dòng điện và Cực tính linh kiện trong SPICE
Trong SPICE, dòng điện qua một linh kiện hai cực được quy ước **chảy từ cực dương (Node +) sang cực âm (Node -)**.
- Với khai báo `C1 out 0 5n`, cực dương là nút `out`, cực âm là nút `0`.
- **Khi nạp:** Dòng điện đi từ ngoài vào nút `out` rồi xuống đất qua $C_1 \implies I(C1) > 0$.
- **Khi xả:** Tụ điện phóng điện ngược từ `out` về nguồn $\implies$ Dòng đi từ nút `0` ngược lên `out` $\implies I(C1) < 0$.
- *Cảnh báo:* Nếu bạn vẽ sơ đồ mà xoay tụ làm cực âm nối lên nút `out`, chiều dòng điện hiển thị trên đồ thị sẽ bị đảo ngược dấu!

### 3.9. Phím tắt thao tác nhanh trong LTspice
- `F2`: Chọn linh kiện (Component) | `R`, `C`, `L`: Đặt nhanh điện trở, tụ điện, cuộn cảm
- `F3`: Vẽ dây nối (Wire) | `G`: Đặt cọc nối đất (Ground - Node 0)
- `F4`: Đặt nhãn tên nút (Net Label) | `S`: Nhập câu lệnh SPICE Directive
- `F5`: Xóa linh kiện (Delete) | `Ctrl + R`: Xoay linh kiện 90° | `Space`: Thu phóng vừa màn hình

---

## 4. KẾ HOẠCH VÀ PHÂN BỔ THỜI LƯỢNG THỰC HÀNH

Quá trình thực hành Lab 0 được tổ chức thành 2 phần nối tiếp:

### Khung thời gian thực hành tại lớp (Phần A)
Tùy theo thời khóa biểu thực tế của Nhà trường, giảng viên áp dụng một trong hai khung phân bổ:

| Phân đoạn nội dung | Khung chuẩn 135 phút (3 tiết) | Khung mở rộng 225 phút (5 tiết) | Vai trò tổ chức lớp |
| :--- | :---: | :---: | :--- |
| **1. Giới thiệu công cụ & Thư mục dự án** | 15 phút | 20 phút | Giảng viên hướng dẫn quy trình, tạo folder. |
| **2. Ex0.1: Phân tích mạch phân áp DC** | 20 phút | 35 phút | Giảng viên làm mẫu, sinh viên thao tác theo. |
| **3. Ex0.2: Mạch RC Transient (Trọng tâm)** | 40 phút | 60 phút | Giảng viên hướng dẫn từng bước, SV thực hành đo `.meas`. |
| **4. Ex0.3: Phân tích AC & Biểu đồ Bode** | 25 phút | 40 phút | Giảng viên giải thích tần số cắt, SV đo đáp ứng. |
| **5. Ex0.4: Quét tham số `.step`** | 20 phút | 30 phút | Sinh viên tự thực hiện dưới sự hỗ trợ của GV. |
| **6. Ex0.5: Giới thiệu mô hình MOSFET C5N** | 10 phút | 15 phút | Giảng viên demo nhanh, định hướng sang Lab 1. |
| **7. Tổng kết & Giao nhiệm vụ đóng gói** | 05 phút | 25 phút | Kiểm tra kết quả tại chỗ, hướng dẫn nộp bài. |

---

## 5. NỘI DUNG THỰC HÀNH TẠI LỚP (PHẦN A)

> [!TIP]
> **Tổ chức thư mục làm việc:**  
> Tạo thư mục `D:\lab_vlsi\lab00\` trên máy tính. Toàn bộ các tệp vẽ sơ đồ `.asc`, tệp netlist `.sp` và tệp mô hình `C5_models.txt` phải được lưu chung trong thư mục này.

---

### Ex0.1 — Phân tích điểm làm việc DC và đặc tuyến truyền đạt của mạch phân áp
*(Thời lượng: 20–35 phút | Hình thức: Giảng viên làm mẫu, sinh viên thực hành theo)*

**1. Mục đích:** Làm quen với việc nhập sơ đồ nguyên lý, khai báo nguồn DC, chạy phân tích `.op` và quét `.dc`.

**2. Các bước thực hiện:**
1. Tạo sơ đồ mới (**File $\to$ New Schematic**).
2. Đặt nguồn điện áp $V_1 = 5.0\,\text{V}$, điện trở $R_1 = 12\,\text{k}\Omega$, $R_2 = 18\,\text{k}\Omega$, đặt cọc đất `GND` tại chân dưới của $R_2$.
3. Đặt nhãn cho nút ngõ vào là `in` và nút giữa hai điện trở là `out`.
4. Nhấn phím `S`, nhập lệnh `.op`, nhấn biểu tượng **Run** (người chạy). Đọc kết quả điện áp tĩnh tại nút `out` và dòng điện qua $R_1$.
5. Đổi lệnh mô phỏng sang quét DC: nhấp chuột phải vào dòng lệnh đổi thành `.dc V1 0 10 0.1`. Nhấn **Run**. Đưa que đo nhấp vào nút `out` để quan sát đặc tuyến truyền đạt $V_{out} = f(V_{in})$.

**3. Câu hỏi tư duy:**
- *Câu hỏi 1:* Tại sao bắt buộc phải có nút đất `0` trong Netlist SPICE? Nếu xóa cọc đất đi mạch có chạy được không?
- *Câu hỏi 2:* Khi thay đổi điện áp đầu vào $V_{in}$, điện áp ngõ ra $V_{out}$ thay đổi theo quy luật nào? Độ dốc của đường đặc tuyến bằng bao nhiêu và liên hệ thế nào với tỉ số $\frac{R_2}{R_1 + R_2}$?

**4. Sản phẩm nghiệm thu Ex0.1:**
- Sơ đồ mạch phân áp `divider.asc`.
- Tệp Netlist `divider.sp` trích xuất từ menu **View $\to$ SPICE Netlist**.
- Bảng so sánh điện áp $V_{out}$ và dòng $I$ giữa lý thuyết phân áp với kết quả `.op`.

---

### Ex0.2 — Mô phỏng quá độ nạp và xả của mạch RC (Bài thực hành trọng tâm)
*(Thời lượng: 40–60 phút | Hình thức: Giảng viên hướng dẫn từng bước, sinh viên thực hành độc lập)*

**1. Mục đích:** Làm chủ phân tích miền thời gian `.tran`, quan sát quá trình nạp/xả tụ điện, khai thác câu lệnh `.meas` để đo tự động $t_{pd}, t_r, t_f$ và đỉnh dòng điện.

**2. Các bước thực hiện:**
1. Dựng mạch RC nối tiếp gồm $R_1 = 20\,\text{k}\Omega$ và $C_1 = 5\,\text{nF}$ nối xuống đất.
2. Cấu hình nguồn xung tại ngõ vào `in`: Nhấp chuột phải vào nguồn, chọn **Advanced $\to$ PULSE**:
   - $V_1 = 0$, $V_2 = 5.0$, $T_{delay} = 0$, $T_{rise} = 10\text{n}$, $T_{fall} = 10\text{n}$, $T_{on} = 500\mu$, $T_{period} = 1000\mu$.
   *(Nhận xét: Thời gian sườn $10\,\text{ns}$ rất nhỏ so với $\tau = 100\,\mu\text{s}$, xấp xỉ hoàn hảo một nguồn xung lý tưởng).*
3. Nhập lệnh phân tích quá độ: `.tran 0 1m 0 0.1u`.
4. Nhấn phím `S`, nhập khối câu lệnh đo lường tự động `.meas`:
   ```spice
   .meas TRAN t_pd TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 RISE=1
   .meas TRAN t_r  TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1
   .meas TRAN t_f  TRIG V(out)=4.5 FALL=1 TARG V(out)=0.5 FALL=1
   .meas TRAN I_peak_chg MAX I(C1)
   .meas TRAN I_peak_dis MIN I(C1)
   ```
5. Nhấn **Run**. Đưa que đo xem điện áp `V(in)` và `V(out)`. Mở **View $\to$ SPICE Error Log** (`Ctrl + L`) để đọc các số đo tự động.
6. Thêm một khung đồ thị (**Add Plot Pane**), đưa que đo vào thân tụ $C_1$ để quan sát dạng sóng dòng điện nạp/xả.

**3. Câu hỏi tư duy:**
- *Câu hỏi 1:* Tại sao điện áp trên tụ điện $v_C(t)$ không thể thay đổi tức thời khi có xung điện áp nhảy bậc ở ngõ vào?
- *Câu hỏi 2:* Sau đúng một hằng số thời gian $\tau$, điện áp nạp trên tụ đạt bao nhiêu phần trăm điện áp cực đại? Sau bao nhiêu $\tau$ thì mạch được xem là nạp đầy?
- *Câu hỏi 3:* Nếu tăng giá trị điện dung lên gấp đôi ($C = 10\,\text{nF}$), thời gian trễ $t_{pd}$ và sườn tăng $t_r$ thay đổi như thế nào?
- *Câu hỏi 4:* Dòng điện đỉnh nạp $I_{peak,chg}$ và dòng điện đỉnh xả $I_{peak,dis}$ có độ lớn bằng bao nhiêu và xảy ra tại thời điểm nào?

**4. Sản phẩm nghiệm thu Ex0.2:**
- Sơ đồ mạch `rc_transient.asc`.
- Dạng sóng chụp màn hình gồm 2 đồ thị: Điện áp $V(in), V(out)$ và Dòng điện $I(C1)$.
- Bảng đối chiếu số liệu đo SPICE `.meas` so với công thức giải tích ($\tau = RC$, $t_{50\%} = 0,693 RC$, $t_r \approx 2,2 RC$).

---

### Ex0.3 — Phân tích đáp ứng tần số AC và Biểu đồ Bode
*(Thời lượng: 25–40 phút | Hình thức: Giảng viên hướng dẫn, sinh viên thực hành)*

**1. Mục đích:** Hiểu đặc tính lọc thông thấp của mạch RC trong miền tần số; xác định tần số cắt $-3\,\text{dB}$ và độ dịch pha.

**2. Các bước thực hiện:**
1. Dùng lại sơ đồ mạch RC của Ex0.2. Nhấp chuột phải vào nguồn điện áp, trong ô **Small Signal AC Analysis (AC)**, nhập biên độ `1`.
2. Nhấn phím `S`, đổi lệnh mô phỏng thành: `.ac dec 20 10 1Meg` (quét từ $10\,\text{Hz}$ đến $1\,\text{MHz}$, mỗi thập kỷ tần số lấy 20 điểm).
3. Nhập câu lệnh `.meas` tìm tần số cắt:
   ```spice
   .meas AC Av_max MAX mag(V(out)/V(in))
   .meas AC f_c WHEN mag(V(out)/V(in))=Av_max/sqrt(2) FALL=1
   ```
4. Nhấn **Run**, que đo nhấp vào nút `out` để hiển thị biểu đồ Bode (trục trái biểu thị biên độ theo dB, trục phải biểu thị góc pha theo độ).

**3. Câu hỏi tư duy:**
- *Câu hỏi 1:* Vì sao mạch RC lại có khả năng cho tín hiệu tần số thấp đi qua và làm suy giảm mạnh tín hiệu ở tần số cao?
- *Câu hỏi 2:* Tại tần số cắt $f_c$, biên độ suy giảm bao nhiêu dB so với vùng tần số thấp và góc pha giữa điện áp ra và vào bằng bao nhiêu độ?
- *Câu hỏi 3:* Sự khác biệt bản chất giữa chế độ mô phỏng miền thời gian `.tran` và miền tần số `.ac` là gì?

**4. Sản phẩm nghiệm thu Ex0.3:**
- Đồ thị biểu đồ Bode có gắn con trỏ chuột (Cursor) tại điểm $-3\,\text{dB}$ và $-45^\circ$.
- Bảng so sánh tần số cắt đo được với công thức giải tích: $f_c = \frac{1}{2\pi R C} = \frac{1}{2\pi \times 100\,\mu\text{s}} \approx 1,592\,\text{kHz}$.

---

### Ex0.4 — Khảo sát độ nhạy tham số với `.param` và `.step`
*(Thời lượng: 20–30 phút | Hình thức: Sinh viên thực hiện dưới sự hướng dẫn)*

**1. Mục đích:** Làm chủ kỹ thuật quét tham số linh kiện tự động; chứng minh bằng thực nghiệm quy luật trễ tuyến tính theo điện trở.

**2. Các bước thực hiện:**
1. Trên sơ đồ mạch RC quá độ, thay đổi giá trị của điện trở $R_1$ thành biến `{Rval}`.
2. Thêm các dòng lệnh định nghĩa và quét tham số:
   ```spice
   .param Rval=20k
   .step param Rval list 5k 10k 20k 40k
   ```
3. Chạy lại mô phỏng `.tran 0 1m 0 0.1u` với lệnh đo trễ `t_pd`.
4. Mở **SPICE Error Log** (`Ctrl + L`) để quan sát 4 giá trị trễ $t_{pd}$ tương ứng với 4 bước quét.
5. Nhấp chuột phải vào cửa sổ Error Log, chọn **Plot .step'ed .meas data** để vẽ đồ thị hàm số $t_{pd} = f(R)$.

**3. Câu hỏi tư duy:**
- *Câu hỏi 1:* Tại sao thời gian trễ truyền lan $t_{pd}$ lại tăng gần như tuyến tính tuyệt đối theo giá trị điện trở?
- *Câu hỏi 2:* Độ dốc của đường đồ thị $\frac{\Delta t_{pd}}{\Delta R}$ bằng bao nhiêu và có đúng bằng $\ln(2) \cdot C \approx 0,693 \cdot C$ không?
- *Câu hỏi 3:* Nếu ta giữ nguyên điện trở $R$ và quét giá trị tụ điện $C$ thì đồ thị trễ sẽ có dạng như thế nào?

**4. Sản phẩm nghiệm thu Ex0.4:**
- Bảng số liệu trễ $t_{pd}$ qua 4 giá trị điện trở ($5\,\text{k}\Omega, 10\,\text{k}\Omega, 20\,\text{k}\Omega, 40\,\text{k}\Omega$).
- Đồ thị thực nghiệm $t_{pd} - R$ trích xuất từ LTspice.
- Tính toán và xác nhận độ dốc: $\text{Slope} \approx 3,466\,\text{ns}/\text{k}\Omega$.

---

### Ex0.5 — Giới thiệu liên kết mô hình MOSFET công nghệ C5N
*(Thời lượng: 10–15 phút | Hình thức: Giảng viên demo nhanh, sinh viên hoàn thiện)*

**1. Mục đích:** Tạo bước đệm chuyển tiếp từ linh kiện thụ động sang linh kiện tích cực; làm quen với lệnh gọi tệp mô hình thư viện ngoài `.include`.

**2. Các bước thực hiện:**
1. Mở một sơ đồ mới, lấy linh kiện transistor NMOS 4 cực (`nmos4`).
2. Nhấp chuột phải vào transistor: đặt tên Model là **`N`**, chiều rộng kênh $W = 1.2\,\mu\text{m}$ (`1.2u`), chiều dài kênh $L = 0.6\,\mu\text{m}$ (`0.6u`).
3. Đặt nguồn $V_{DS} = 5.0\,\text{V}$ vào cực má (Drain), nguồn $V_{GS} = 5.0\,\text{V}$ vào cực cổng (Gate); cực nguồn (Source) và cực thân (Bulk) nối chung xuống đất.
4. Nhấn phím `S`, chèn lệnh liên kết tệp mô hình: `.include C5_models.txt`.
5. Đặt lệnh `.op` và chạy mô phỏng. Đọc dòng điện cực má $I_D$.

**3. Câu hỏi định hướng cho Lab 1:**
- *Câu hỏi 1:* Tại sao SPICE cần tệp mô hình riêng biệt (`.model`) mà không thể khai báo MOSFET đơn giản như một điện trở?
- *Câu hỏi 2:* Dòng điện $I_D$ mô phỏng được trong SPICE khoảng $1,4\,\text{mA}$, trong khi công thức bậc hai sách giáo khoa tính ra $\approx 2,2\,\text{mA}$. Nguyên nhân vật lý nào trong transistor dưới-micron (submicron) gây ra sự chênh lệch này?

**4. Sản phẩm nghiệm thu Ex0.5:**
- Sơ đồ mạch phân cực `nmos_test.asc` và Netlist tương ứng.
- Giá trị dòng điện $I_D$ ghi nhận từ kết quả `.op`.

---

## 6. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (PHẦN B)

Sau khi hoàn thành buổi thực hành tại lớp, sinh viên không cần làm thêm bài tập mới mà tiến hành **hoàn thiện và đóng gói thư mục dự án Lab 0** với các yêu cầu sau:

### 1. Cấu trúc thư mục dự án nộp bài (`lab00_MSSV_HoTen/`)
```
lab00_MSSV_HoTen/
│
├── schematics/             # Chứa toàn bộ các tệp sơ đồ nguyên lý
│   ├── ex01_divider.asc
│   ├── ex02_rc_tran.asc
│   ├── ex03_rc_ac.asc
│   ├── ex04_rc_step.asc
│   └── ex05_nmos_test.asc
│
├── netlists/               # Chứa các tệp Netlist trích xuất
│   ├── ex01_divider.sp
│   ├── ex02_rc_tran.sp
│   └── ex05_nmos_test.sp
│
├── waveforms/              # Chứa ảnh chụp dạng sóng rõ nét
│   ├── ex01_dc_sweep.png
│   ├── ex02_transient_v_i.png
│   ├── ex03_bode_plot.png
│   └── ex04_step_plot.png
│
├── C5_models.txt           # Tệp thư viện mô hình C5N chuẩn
└── Bao_Cao_Lab00_MSSV.pdf  # Báo cáo kỹ thuật tổng kết (từ 2 đến 3 trang)
```

### 2. Nội dung báo cáo kỹ thuật tổng kết
Báo cáo ngắn gọn, súc tích gồm 3 phần:
1. **Bảng tổng hợp kết quả Benchmark:** Bảng so sánh đầy đủ giữa Lý thuyết giải tích và Đo đạc SPICE cho cả 5 bài Ex0.1 – Ex0.5, kèm cột tính sai lệch tương đối $\text{Error (\%)}$.
2. **Trả lời ngắn gọn các câu hỏi tư duy:** Trình bày câu trả lời cho các câu hỏi tư duy đã nêu trong từng bài Ex.
3. **Nhật ký xử lý lỗi kỹ thuật (Debug Log):** Ghi chép trung thực 1–2 lỗi hoặc cảnh báo mà em đã gặp phải trong quá trình làm bài và giải thích cách em đã khắc phục thành công.

---

## 7. TIÊU CHÍ KIỂM CHỨNG KỸ THUẬT & SAI LỆCH CHẤP NHẬN

Mỗi kết quả đo tự động bằng `.meas` được đánh giá độ chính xác bằng công thức:
$$\text{Sai lệch tương đối (\%)} = \frac{|\text{Giá trị SPICE} - \text{Giá trị Lý thuyết}|}{\text{Giá trị Lý thuyết}} \times 100\%$$

- **Chỉ tiêu đối với mạch RC (Ex0.1 – Ex0.4):** Sai lệch tương đối $\le 2,0\%$. Mạch RC là mạng tuyến tính lý tưởng nên nếu thiết lập đúng `dTmax = 0.1u`, sai số thông thường sẽ $< 0,1\%$.
- **Đối với bài MOSFET (Ex0.5):** Chấp nhận sai lệch giữa tính tay bậc hai và mô phỏng SPICE Level 3 lên tới $30\% - 40\%$. Sinh viên chỉ cần nêu đúng nguyên nhân do hiện tượng **bão hòa vận tốc hạt dẫn (Velocity Saturation)** và **suy giảm độ linh động (Mobility Degradation)**.

---

## 8. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP (SELF-DEBUGGING)

| Hiện tượng lỗi | Nguyên nhân cốt lõi | Hướng tự kiểm tra và xử lý |
| :--- | :--- | :--- |
| **Không chạy được, báo *Singular Matrix*** | Thiếu nút đất tham chiếu `0`. | Kiểm tra xem mạch đã đặt cọc đất `GND` chưa. |
| **Báo lỗi *Node is floating*** | Có chân linh kiện bị hở hoặc chưa nối dây. | Dùng phím `F3` kiểm tra các mối nối có xuất hiện chấm vuông không. |
| **Lệnh `.step` ra các đường trùng khít nhau** | Quên đặt dấu ngoặc nhọn `{}` quanh tên biến. | Kiểm tra giá trị điện trở trên sơ đồ: phải là `{Rval}`, không phải `Rval`. |
| **Dòng điện nạp của tụ bị âm** | Tụ điện bị đặt ngược cực tính (+/-). | Chọn tụ điện, nhấn `Ctrl + R` xoay 2 lần để đảo lại chiều cực. |
| **Báo lỗi *Unknown Model / Subcircuit*** | Sai tên model trong Netlist hoặc thiếu `.include`. | Mở tệp model kiểm tra chính xác tên (`N` chứ không phải `NMOS`). |
| **Đồ thị trễ `.meas` bị răng cưa, sai lệch lớn** | Bước thời gian mô phỏng `dTmax` bị quá thô. | Sửa lệnh `.tran`: thêm `0.1u` vào tham số cuối cùng: `.tran 0 1m 0 0.1u`. |

---

## 9. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

| Hạng mục đánh giá | Điểm | Tiêu chí đạt điểm tối đa |
| :--- | :---: | :--- |
| **Kỹ năng thao tác tại lớp (Ex0.1 – Ex0.3)** | **4.0 điểm** | Dựng mạch đúng, chạy đủ 3 chế độ `.op`, `.tran`, `.ac`; trích xuất số liệu chuẩn xác bằng `.meas` với sai số $\le 2\%$. |
| **Khảo sát tham số & MOSFET (Ex0.4 – Ex0.5)** | **2.0 điểm** | Quét đúng 4 bước giá trị $R$, vẽ được đồ thị thực nghiệm; liên kết thành công tệp model C5N và đo được dòng $I_D$. |
| **Hiểu bản chất qua câu hỏi tư duy** | **2.0 điểm** | Trả lời đúng, rõ ràng bản chất vật lý của các câu hỏi tư duy trong từng bài (vai trò nút đất, cơ chế nạp xả tụ, hằng số thời gian). |
| **Đóng gói dự án & Báo cáo kỹ thuật (Phần B)** | **2.0 điểm** | Thư mục dự án đầy đủ cấu trúc chuẩn; sơ đồ và Netlist sạch sẽ; báo cáo trình bày số liệu trung thực, ghi nhận lỗi rõ ràng. |
