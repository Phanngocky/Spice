# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# KIẾN THỨC NỀN & CẨM NANG HƯỚNG DẪN THỰC HÀNH THIẾT KẾ VI MẠCH VLSI
## Toàn tập bộ bài thực hành thiết kế vi mạch CMOS từ Lab 0 đến Lab 10 (Công nghệ MOSIS C5N 0,5 µm)

> **Tài liệu lưu hành nội bộ (Internal Instructor's Guide) — Tuyệt đối không phát cho sinh viên.**  
> **Dùng song song với tài liệu thực hành (Student Handout) từ Lab 0 đến Lab 10.**  
> **Trạng thái kiểm chứng kỹ thuật:** Toàn bộ công thức giải tích, mô hình bậc hai, mô hình SPICE Level 3 chuẩn C5N, số lượng transistor, luật thiết kế hình học SCMOS và ngân sách định thời đã được kiểm chứng chéo và chuẩn hóa đồng bộ với thư viện mô hình `04 - Models_and_Libraries/C5_models.txt` và bộ nghiệm thu mô phỏng `03 - Instructor_Solutions/VERIFICATION_BENCHMARK.md`.

---

# 0. QUY ƯỚC CHUNG & HỆ THỐNG THAM SỐ THIẾT KẾ XUYÊN SUỐT

## 0.1 Bản đồ lộ trình đào tạo và phân bổ thời lượng
Chương trình thực hành được thiết kế tương thích với đề cương chi tiết học phần Thiết kế VLSI (3 tín chỉ: 24 LT + 6 BT + 15 ĐA = 21 tiết thực hành trực tiếp trên lớp tương đương 7 buổi thực hành chuẩn, kết hợp 90 giờ tự học có hướng dẫn).

| Buổi / Lab | Tên bài Lab | Chương đề cương | Vai trò môn học | Công cụ thực hiện | Trọng tâm sư phạm |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **Lab 0** | Nhập môn mô phỏng SPICE & Mạch RC | 1, 3 | Bắt buộc (Nhập môn) | LTspice | Đơn vị SPICE, phân áp, nạp xả RC, định luật $0,69 \cdot RC$. |
| **Lab 1** | Đặc tính MOSFET & CMOS Inverter | 2, 3 | Bắt buộc | LTspice + Electric | Họ $I$-$V$, điểm $V_M$, trễ $t_{pd}$, Layout Inverter, DRC, LVS, PEX. |
| **Lab 2** | Cổng logic tĩnh NAND2 và NOR2 | 6 | Bắt buộc | LTspice | Mạng đối ngẫu, định cỡ $R_{on}$, trễ phụ thuộc vector, đường Euler. |
| **Lab 3** | Cổng phức hợp AOI/OAI & Logical Effort | 3, 6 | Bắt buộc | LTspice + Electric | Tối ưu transistor, mô hình $d = g \cdot h + p$, chuỗi đệm tối ưu, Layout. |
| **Lab 4** | Cổng truyền (Transmission Gate) & MUX | 6 | Tự chọn / Ghép Lab 6 | LTspice | Suy hao mức logic (Weak 0/1), điện trở phẳng $R_{TG}$, chuỗi Elmore. |
| **Lab 5** | Mạch tuần tự: D-Latch & D-Flip-Flop | 7 | Bắt buộc | LTspice | Master-slave, $t_{setup}, t_{hold}, t_{c-q}$, quét dịch pha, metastability. |
| **Lab 6** | Mạch cộng toàn phần (1-bit Full Adder) | 6 | Bắt buộc | LTspice | Mirror Adder 28T, TG Adder, đường tới hạn $C_{in} \to C_{out}$, chuỗi RCA. |
| **Lab 7** | Logic động (Dynamic CMOS) & Domino | 6 | Nâng cao / Tự chọn | LTspice | Hai pha Precharge/Evaluate, chia sẻ điện tích, transistor Keeper. |
| **Lab 8** | Ô nhớ SRAM 6T & Sense Amplifier | Đồ án / Tự chọn | LTspice | Đọc/Ghi ổn định, đường cong bướm SNM, khuếch đại vi sai lẫy. |
| **Lab 9** | Khối cộng nhanh 4-bit CLA | Đồ án / Tự chọn | LTspice | Tách $P/G$, bộ tạo carry song song CLG, đánh đổi diện tích và tốc độ. |
| **Lab 10** | Capstone: ALU 4-bit có thanh ghi | Đồ án (1, 6, 7) | Bắt buộc | LTspice + Electric | Tích hợp Top-down, ngân sách thời gian $f_{max}$, Floorplan, IR-drop. |

---

## 0.2 Tham số tiến trình MOSIS C5N 0,5 µm trích xuất từ tệp PDK thực tế
Các tham số chuẩn hóa được trích xuất trực tiếp từ tệp [C5_models.txt](file:///d:/tam/VLSI_Spice/04%20-%20Models_and_Libraries/C5_models.txt) và dùng xuyên suốt giáo trình:

| Ký hiệu | Ý nghĩa vật lý | Giá trị chuẩn C5N | Nguồn xác thực | Ghi chú hướng dẫn giảng dạy |
| :--- | :--- | :---: | :---: | :--- |
| $V_{DD}$ | Điện áp nguồn danh định | $5,0\,\text{V}$ | Handout / PDK | Chuẩn logic $5\,\text{V}$ TTL/CMOS tương thích. |
| $\lambda$ (lưới) | Đơn vị lưới layout mở rộng | $0,30\,\mu\text{m}$ | MOSIS SCMOS | Chiều dài kênh tối thiểu $L_{min} = 2\lambda = 0,60\,\mu\text{m}$. |
| $\lambda_{kênh}$ | Hệ số điều chế độ dài kênh | $0,05\,\text{V}^{-1}$ | Script / PDK | Cần phân biệt rõ với $\lambda$ lưới layout trên bảng. |
| $t_{ox}$ | Độ dày lớp oxit cổng | $9,5\,\text{nm}$ ($95\,\text{Å}$) | Tệp C5_models.txt | Handout cũ giả định $14\,\text{nm}$ là sai lệch! |
| $C_{ox}$ | Điện dung oxit cổng trên đơn vị diện tích | $3,635\,\text{fF/\mu m}^2$ | $\varepsilon_{ox}/t_{ox}$ | $3,453 \cdot 10^{-11}\,\text{F/m} / 9,5 \cdot 10^{-9}\,\text{m}$. |
| $V_{tn0}, \|V_{tp0}\|$ | Điện áp ngưỡng không thiên thế thân | $0,70\,\text{V}$ và $0,80\,\text{V}$ | Tệp C5_models.txt | VTO trong model N và model P. |
| $K'_n, K'_p$ | Hệ số độ dẫn truyền bản chất | $120\,\mu\text{A/V}^2$ / $40\,\mu\text{A/V}^2$ | Tệp C5_models.txt | Tỉ số độ linh động $\mu_n / \mu_p \approx 3,0$. |
| $\gamma_n, \gamma_p$ | Hệ số hiệu ứng thân (Body factor) | $0,40\,\text{V}^{1/2}$ / $0,50\,\text{V}^{1/2}$ | Tệp C5_models.txt | GAMMA trong model N và model P. |
| $2\Phi_F$ | Thế mặt tiếp xúc vùng nghèo | $0,70\,\text{V}$ | Tệp C5_models.txt | PHI trong model SPICE. |
| $C_{GSO}, C_{GDO}$ | Tụ chồng lấp cực cổng - nguồn/máng | $0,20\,\text{fF/\mu m}$ ($2,0 \cdot 10^{-10}\,\text{F/m}$) | Tệp C5_models.txt | Đóng góp vào tụ Miller khi chuyển mạch. |
| $\text{INV\_X1}$ | Kích thước cổng Inverter chuẩn | $W_n = 4\lambda = 1,2\,\mu\text{m}$; $W_p = 12\lambda = 3,6\,\mu\text{m}$ | Chuẩn quy ước | Tỉ số $W_p / W_n = 3,0$ cân bằng $\beta$. |
| $R_{on,n}, R_{on,p}$ | Điện trở dẫn tương đương ($V_{DS} \to 0$) | $969\,\Omega$ và $992\,\Omega$ | Giải tích số | Tính tại $V_{GS} = 5\,\text{V}$. |
| $C_{in}(\text{INV\_X1})$ | Điện dung ngõ vào tế bào chuẩn | $11,43\,\text{fF}$ | Giải tích chuẩn C5N | $C_{gate} (10,47\,\text{fF}) + C_{overlap} (0,96\,\text{fF})$. |

---

## 0.3 Ba nguyên tắc sư phạm cốt lõi khi đứng lớp
1. **Nguyên tắc "Tính trước — Đo sau — So sánh — Giải thích sai lệch":**
   Không bao giờ cho sinh viên bấm chạy mô phỏng khi chưa có con số ước lượng trên giấy. Sai lệch giữa tính tay bậc hai và mô phỏng SPICE Level 3 là "mảnh đất vàng" để giảng viên giải thích hiện tượng bão hòa vận tốc, hiệu ứng thân và điện dung ký sinh.
2. **Minh bạch hóa giới hạn của mô hình:**
   Mô hình $0,69 \cdot R_{on} \cdot C_L$ chỉ là cận dưới giải tích (giả định điện trở không đổi suốt quá trình phóng nạp). Trễ đo SPICE thực tế luôn lớn hơn từ $1,5$ đến $1,8$ lần do transistor bắt đầu phóng nạp từ vùng bão hòa có dòng điện hữu hạn.
3. **Quy tắc định cỡ chuẩn theo Inverter cơ sở:**
   Mọi cổng logic phức tạp (NAND, NOR, AOI, Mirror Adder) đều được định cỡ sao cho điện trở tương đương của đường dẫn xấu nhất đúng bằng $R_{on}$ của Inverter chuẩn $\text{INV\_X1}$ ($969\,\Omega$ cho kéo xuống và $992\,\Omega$ cho kéo lên).


---

# LAB 0 — NHẬP MÔN MÔ PHỎNG SPICE VỚI LTSPICE & MẠCH RC CƠ BẢN (CHƯƠNG 1, 3)

# TÀI LIỆU GIẢNG DẠY VÀ CẨM NANG SƯ PHẠM: CHƯƠNG 0 (LAB 00)
# NHẬP MÔN MÔ PHỎNG SPICE VỚI LTSPICE & MẠCH RC CƠ BẢN
*(Tài liệu chuyên môn lưu hành nội bộ dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH Sư phạm Kỹ thuật – ĐH Đà Nẵng)*

> **Quy định bảo mật học liệu:** Không phân phát tài liệu này cho sinh viên. Dùng làm cẩm nang hướng dẫn đứng lớp, cung cấp cơ sở vật lý toán, kịch bản hướng dẫn, phương pháp đặt câu hỏi gợi mở (Socratic Questioning), dữ liệu đối chuẩn SPICE Benchmark và các lưu ý kỹ thuật.

---

## 0.1. VAI TRÒ CỦA LAB 0 TRONG HỌC PHẦN THIẾT KẾ VLSI
Trong chương trình đào tạo Thiết kế Vi mạch VLSI, sinh viên thường gặp khó khăn lớn khi phải đối mặt đồng thời với hai thách thức:
1. Độ phức tạp của các công cụ EDA chuyên dụng (như Electric VLSI, Cadence Virtuoso, Synopsys).
2. Sự trừu tượng của các mô hình vật lý bán dẫn phi tuyến tính dưới-micron (Submicron MOSFET).

**Lab 0 đóng vai trò là "vùng đệm an toàn" (Sandbox & Onboarding Lab):**
- Tách biệt kỹ năng sử dụng công cụ mô phỏng SPICE khỏi sự phức tạp của vật lý bán dẫn.
- Sinh viên sử dụng các linh kiện tuyến tính thụ động quen thuộc ($R, C$, nguồn điện) để làm chủ quy trình: *Vẽ sơ đồ $\to$ Xuất Netlist $\to$ Chạy mô phỏng $\to$ Quan sát dạng sóng $\to$ Đo đạc tự động `.meas` $\to$ Kiểm chứng với lý thuyết*.
- Mạch RC bậc nhất trong Lab 0 chính là **mô hình tương đương cơ sở** để giải thích toàn bộ động học nạp xả, độ trễ truyền lan ($t_{pd} \approx 0,69 \cdot R_{on} \cdot C_L$) và nỗ lực logic (Logical Effort) xuyên suốt từ Lab 1 đến Lab 10.

---

## 0.2. MỤC TIÊU VÀ CHUẨN ĐẦU RA (CLO MAPPING)

| Mục tiêu bài Lab 0 | Chuẩn đầu ra học phần (CLO) | Mức độ nhận thức (Bloom) | Tiêu chí đánh giá cụ thể |
| :--- | :---: | :---: | :--- |
| **G0.1:** Hiểu vai trò của SPICE và phương pháp MNA | CLO1 | Mức 2 (Hiểu) | Trình bày được bản chất của Netlist và vai trò của nút đất `0`. |
| **G0.2:** Dựng sơ đồ, xuất và đọc hiểu cú pháp Netlist | CLO1, CLO2 | Mức 3 (Áp dụng) | Viết đúng cú pháp phần tử, nhận diện đúng tiền tố đơn vị (`m` vs `Meg`). |
| **G0.3:** Vận hành 4 chế độ phân tích (.op, .dc, .tran, .ac) | CLO2 | Mức 3 (Áp dụng) | Thiết lập đúng lệnh điều khiển mô phỏng cho từng yêu cầu kỹ thuật. |
| **G0.4:** Trích xuất kết quả bằng câu lệnh đo `.meas` | CLO2 | Mức 3 (Áp dụng) | Viết lệnh `.meas` đo đúng $t_{pd}, t_r, t_f, f_c$ từ nhật ký lỗi `SPICE Error Log`. |
| **G0.5:** Khảo sát độ nhạy tham số với `.param` và `.step` | CLO2 | Mức 4 (Phân tích) | Quét giá trị điện trở, vẽ đồ thị và tính được độ dốc thực nghiệm. |
| **G0.6:** Phân tích bản chất vật lý mạch RC & liên hệ CMOS | CLO1, CLO3 | Mức 4 (Phân tích) | Giải thích quy luật $1\tau - 5\tau$, chứng minh $0,69 \cdot RC$ và liên hệ trễ Inverter. |
| **G0.7:** Tổ chức và đóng gói thư mục dự án chuẩn | CLO4 | Mức 3 (Áp dụng) | Cấu trúc thư mục ngăn nắp, đầy đủ sơ đồ, netlist, log và báo cáo kỹ thuật. |

---

## 0.3. KIẾN THỨC NỀN VỀ SPICE, NETLIST VÀ PHƯƠNG PHÁP MNA

### 1. Bản chất giải thuật MNA (Modified Nodal Analysis)
SPICE không đơn thuần là một phần mềm vẽ mạch; bản chất cốt lõi của SPICE là một **bộ giải hệ phương trình vi phân đại số phi tuyến (Nonlinear Differential-Algebraic Equation Solver)**.

Hệ phương trình trạng thái tổng quát của mạng điện trong SPICE:
$$[\mathbf{G}] \cdot [\mathbf{V}] + [\mathbf{C}] \cdot \left[\frac{d\mathbf{V}}{dt}\right] = [\mathbf{I}]$$

Trong đó:
- $[\mathbf{G}]$: Ma trận dẫn nạp tĩnh (Conductance matrix) đại diện cho các điện trở và nguồn phụ thuộc tuyến tính.
- $[\mathbf{C}]$: Ma trận điện dung và điện cảm (Capacitance/Inductance matrix).
- $[\mathbf{V}]$: Véc-tơ điện thế nút cần tìm tại mọi nút trong mạch.
- $[\mathbf{I}]$: Véc-tơ kích thích từ các nguồn dòng và nguồn áp độc lập.

**Vai trò sinh tử của nút đất `0` (Node 0):**  
Theo định luật Kirchhoff, điện thế chỉ có ý nghĩa tương đối (hiệu điện thế). Để hệ phương trình MNA có nghiệm duy nhất, ma trận dẫn nạp bắt buộc phải chọn một nút làm mốc thế chuẩn ($0\,\text{V}$). Nếu người vẽ quên đặt cọc nối đất, ma trận $[\mathbf{G}]$ sẽ bị suy biến định thức ($\det[\mathbf{G}] = 0$), SPICE lập tức báo lỗi kinh điển: **`Singular Matrix`** hoặc **`Node is floating`**.

### 2. Mối quan hệ giữa 5 thành phần trong hệ sinh thái SPICE
Giảng viên cần vẽ lên bảng lưu đồ phân biệt 5 khái niệm mà sinh viên hay nhầm lẫn:
```
+---------------+     Biên dịch      +---------------+     Tham chiếu     +---------------+
|   SCHEMATIC   | -----------------> |    NETLIST    | <----------------- |     MODEL     |
| (Bản vẽ đồ họa|                    | (Mã văn bản   |                    | (Mô hình toán |
|  trực quan)   |                    |  mô tả kết nối|                    |  vật lý linh  |
+---------------+                    +---------------+                    |  kiện)        |
                                             |                            +---------------+
                                             v Nạp vào
                                     +---------------+
                                     |   SIMULATOR   | (Giải thuật tích phân MNA)
                                     +---------------+
                                             | Xuất dữ liệu
                                             v
                                     +---------------+
                                     | WAVEFORM VIEW | (Hiển thị đồ thị & .meas)
                                     +---------------+
```

---

## 0.4. GIẢI THÍCH BỐN CHẾ ĐỘ PHÂN TÍCH CƠ BẢN

| Chế độ phân tích | Câu hỏi vật lý cần trả lời | Bản chất toán học của thuật toán | Ví dụ ứng dụng trong VLSI |
| :---: | :--- | :--- | :--- |
| **`.OP`** | Mạch đang ở trạng thái phân cực nào khi chưa có tín hiệu biến thiên? | Triệt tiêu đạo hàm $\frac{d\mathbf{V}}{dt} = 0$. Tụ hở mạch, cuộn cảm ngắn mạch. Giải hệ phi tuyến bằng **lặp Newton-Raphson**. | Tìm điểm làm việc tĩnh, kiểm tra phân cực transistor, đo dòng rò tĩnh. |
| **`.DC`** | Ngõ ra biến đổi thế nào khi một nguồn áp vào thay đổi từ từ? | Thực hiện một chuỗi các phân tích `.OP` liên tiếp tại từng bước điện áp ngõ vào được chỉ định. | Khảo sát đường đặc tuyến truyền đạt điện áp $VTC$ ($V_{out} - V_{in}$) của Inverter. |
| **`.TRAN`** | Điện áp và dòng điện thay đổi theo thời gian thực ra sao khi có xung? | Rời rạc hóa thời gian bằng các phương pháp tích phân số: **Trapezoidal Rule** hoặc **Gear Method**. | Đo thời gian trễ truyền lan $t_{pd}$, thời gian sườn tăng $t_r$, sườn giảm $t_f$. |
| **`.AC`** | Mạch khuếch đại hoặc suy giảm tín hiệu ra sao ở các tần số khác nhau? | Tuyến tính hóa mạng phi tuyến quanh điểm tĩnh DC; giải hệ phương trình đại số phức theo tần số góc $\omega$. | Vẽ biểu đồ Bode biên độ và pha; đo tần số cắt $f_{-3\text{dB}}$ và dải thông băng tần. |

---

## 0.5. PHÂN TÍCH VẬT LÝ MẠCH RC & ĐỘNG HỌC PHÓNG NẠP

### 1. Phương trình vi phân nạp và xả
Xét mạch $R$ nối tiếp $C$ kích thích bởi nguồn nhảy bậc $V_0 \cdot u(t)$:
- Theo định luật dòng điện Kirchhoff (KCL) tại nút ngõ ra:
  $$\frac{v_{in}(t) - v_C(t)}{R} - C \frac{dv_C(t)}{dt} = 0 \implies \frac{dv_C(t)}{dt} + \frac{1}{RC} v_C(t) = \frac{v_{in}(t)}{RC}$$

**Nghiệm quá trình nạp ($0 \le t < T_{on}$, điều kiện đầu $v_C(0) = 0$):**
$$v_C(t) = V_0 \left(1 - e^{-t/\tau}\right) \quad \text{với } \tau = R \cdot C$$

**Nghiệm quá trình xả ($t \ge T_{on}$, đặt $t' = t - T_{on}$, điều kiện đầu $v_C(0) = V_0$):**
$$v_C(t') = V_0 e^{-t'/\tau}$$

### 2. Năng lượng và Cân bằng nhiệt động học trong mạch RC
- Điện tích nạp vào tụ: $Q = C \cdot V_0$.
- Năng lượng tổng do nguồn cung cấp trong suốt quá trình nạp:
  $$E_{source} = \int_0^\infty V_0 \cdot i(t) \, dt = V_0 \int_0^\infty dq = C \cdot V_0^2$$
- Năng lượng thực tế tích trữ trong điện trường của tụ điện:
  $$E_C = \int_0^{V_0} v_C \cdot C \, dv_C = \frac{1}{2} C V_0^2$$
- Năng lượng tiêu tán dưới dạng nhiệt trên điện trở $R$:
  $$E_R = E_{source} - E_C = \frac{1}{2} C V_0^2$$

> [!TIP]
> **Điểm sư phạm sâu sắc:** Năng lượng tổn hao trên điện trở nạp **luôn bằng đúng $\frac{1}{2}CV_0^2$, hoàn toàn không phụ thuộc vào giá trị của $R$!** Dù điện trở cực nhỏ hay cực lớn, một nửa năng lượng vẫn bị tiêu tán. Đây chính là gốc rễ của công thức công suất động tiêu tán trong vi mạch số ở Chương 4: $P_{dyn} = \alpha \cdot C_L \cdot V_{DD}^2 \cdot f$.

### 3. Bảng mốc thời gian quy ước nạp điện
| Thời gian | Điện áp nạp đạt được | Phần trăm so với $V_0$ | Ý nghĩa kỹ thuật |
| :---: | :---: | :---: | :--- |
| **$0,693 \tau$** | $0,500 V_0$ | $50,0\%$ | Mốc đo độ trễ truyền lan $t_{50\%}$ danh định. |
| **$1,0 \tau$** | $V_0(1 - e^{-1}) \approx 0,632 V_0$ | **$63,2\%$** | Hằng số thời gian $\tau$ của mạch. |
| **$2,197 \tau$** | Khoảng cách từ $10\%$ đến $90\%$ | $\Delta = 80\%$ | Thời gian sườn xung tăng $t_r \approx 2,2 \tau$. |
| **$3,0 \tau$** | $0,950 V_0$ | $95,0\%$ | Điểm chuyển tiếp gần bão hòa. |
| **$5,0 \tau$** | $V_0(1 - e^{-5}) \approx 0,993 V_0$ | **$99,3\%$** | **Quy ước kỹ thuật xem tụ đã nạp no hoàn toàn.** |

---

## 0.6. LIÊN HỆ GIỮA MẠCH RC VÀ ĐỘ TRỄ CỔNG CMOS

Trong mạch số CMOS, các transistor hoạt động như các công tắc đóng mở điện tử. Khi ngõ vào của một Inverter chuyển trạng thái:
1. **Chuyển từ $0 \to 1$ (Kéo xuống - Pull Down):** NMOS dẫn, PMOS ngắt. Tụ tải ký sinh $C_L$ tại ngõ ra phóng điện tích xuống đất qua kênh dẫn NMOS.
2. **Chuyển từ $1 \to 0$ (Kéo lên - Pull Up):** PMOS dẫn, NMOS ngắt. Nguồn $V_{DD}$ nạp điện cho tụ tải qua kênh dẫn PMOS.

```
       MẠCH RC THỰC HÀNH                  MÔ HÌNH CMOS TƯƠNG ĐƯƠNG               CỔNG INVERTER THỰC TẾ
         R (20k)                                    R_on,p                               VDD (5V)
  Vin --/\/\/\--+-- Vout                    VDD -----/\/\/\---+                         +---+
                |                                             |                         |Mp | (W=12λ)
              +---+                                         +---+                       +---+
              | C | (5nF)                                   |CL | (Tải dung)    Vin ----+---+---- Vout
              +---+                                         +---+                       |Mn | (W=4λ)
                |                                             |                         +---+
               GND                          GND -----/\/\/\---+                           |
                                                    R_on,n                               GND
```

### Giới hạn của mô hình $0,69 \cdot R_{on} \cdot C_L$
- Trong mạch RC thụ động (Lab 0), điện trở $R$ là tuyến tính hằng số $\implies$ Trễ đo được khớp chính xác hoàn toàn với $\ln(2) \cdot RC$.
- Trong cổng CMOS thực tế (Lab 1), kênh dẫn MOSFET là linh kiện phi tuyến. Trong nửa đầu quá trình phóng nạp, transistor hoạt động trong vùng **Bão hòa** (dòng điện gần như không đổi), sau đó mới chuyển sang vùng **Tuyến tính**. Do đó, điện trở kênh dẫn thực tế biến thiên liên tục.
- Giá trị $0,69 \cdot R_{on} \cdot C_L$ chỉ là **cận dưới xấp xỉ**. Trễ mô phỏng thực tế của Inverter luôn lớn hơn từ $1,5$ đến $1,8$ lần con số này. Giảng viên cần nhấn mạnh điều này để chuẩn bị tâm lý cho sinh viên bước vào Lab 1.

---

## 0.7. HƯỚNG DẪN TỔ CHỨC BUỔI THỰC HÀNH (KỊCH BẢN 135' & 225')

Giảng viên chủ động lựa chọn kịch bản thời lượng phù hợp với phòng máy:

### Kịch bản A: Khung chuẩn 135 phút (Ca 3 tiết tiêu chuẩn)
- **00–15' (15 phút):** Điểm danh, phổ biến quy định an toàn, hướng dẫn tạo cấu trúc thư mục `D:\lab_vlsi\lab00\`. Giới thiệu giao diện LTspice, cách chọn linh kiện, ý nghĩa nút đất `0`.
- **15–35' (20 phút):** Giảng viên chiếu máy chiếu làm mẫu **Ex0.1**; giải thích lệnh `.op`, `.dc` và cách đọc dòng điện. Sinh viên làm theo và ghi số liệu.
- **35–75' (40 phút):** **Trọng tâm Ex0.2**: Hướng dẫn cấu hình nguồn PULSE, thiết lập `.tran 0 1m 0 0.1u`. Giải thích cú pháp `.meas`. Sinh viên tự đo và kiểm chứng 5 thông số ($t_{pd}, t_r, t_f, I_{peak,chg}, I_{peak,dis}$).
- **75–100' (25 phút):** Hướng dẫn **Ex0.3**: Cấu hình nguồn AC 1, chạy `.ac dec 20 10 1Meg`. Hướng dẫn sinh viên rê chuột trên biểu đồ Bode tìm điểm $-3\,\text{dB}$ và $-45^\circ$.
- **100–120' (20 phút):** Sinh viên tự lập thực hiện **Ex0.4**: Thay `{Rval}`, chạy `.step`, trích xuất bảng 4 điểm trễ và vẽ đồ thị thực nghiệm.
- **120–135' (15 phút):** Giảng viên demo nhanh **Ex0.5**: Gọi thư viện `C5_models.txt`, giải thích dòng $I_D$ thấp hơn công thức bậc hai. Nghiệm thu sản phẩm tại bàn, hướng dẫn đóng gói dự án nộp về nhà.

### Kịch bản B: Khung mở rộng 225 phút (Ca 5 tiết tích hợp)
- Mở rộng thời gian cho Ex0.2 (60 phút) để sinh viên thử nghiệm thay đổi `dTmax` từ `0.1u` lên `20u` và quan sát sai số trễ tăng vọt.
- Dành 30 phút cho sinh viên tự thực hành Ex0.5 tại lớp, tự tay viết Netlist và tìm hiểu các tham số $VTO, KP$ trong tệp mô hình `C5_models.txt`.
- Dành 25 phút cuối giờ để kiểm tra vấn đáp từng nhóm sinh viên tại bàn máy.

---

## 0.8. HƯỚNG DẪN CHI TIẾT TỪNG BÀI THỰC HÀNH (EX0.1 – EX0.5)

### Ex0.1: Phân tích mạch phân áp DC (.op, .dc)
1. **Kiến thức giảng viên cần giải thích:**
   - Định luật Kirchhoff dòng điện tại nút `out`: $\frac{V_{in} - V_{out}}{R_1} = \frac{V_{out}}{R_2} \implies V_{out} = V_{in} \frac{R_2}{R_1 + R_2}$.
   - Khái niệm điểm làm việc tĩnh DC: mạch không có tín hiệu xoay chiều, tụ điện coi như hở mạch hoàn toàn.
2. **Kịch bản hướng dẫn:**
   - GV chiếu thao tác vẽ schematic, đặt nguồn `voltage`, đặt `GND`.
   - Lưu ý đặc biệt: Chỉ cho sinh viên xem menu **View $\to$ SPICE Netlist** ngay sau khi vẽ xong sơ đồ để sinh viên hiểu bản chất schematic chỉ là giao diện đồ họa sinh ra netlist.
3. **Kết quả tham chiếu:**
   - Với $V_{in} = 5,0\,\text{V}, R_1 = 12\,\text{k}\Omega, R_2 = 18\,\text{k}\Omega$:
     * $V(out) = 3,0000\,\text{V}$ (Sai số $0,00\%$).
     * $I(R1) = 0,1667\,\text{mA} = 166,7\,\mu\text{A}$.
     * Độ dốc đặc tuyến $\frac{\Delta V_{out}}{\Delta V_{in}} = \frac{18}{30} = 0,6000$.
4. **Câu hỏi gợi mở vấn đáp:**
   - *"Nếu thầy thay đổi nguồn vào thành $10\,\text{V}$, điện áp $V_{out}$ sẽ là bao nhiêu? Công suất tiêu tán toàn mạch tăng gấp mấy lần?"* (Đáp: $6\,\text{V}$; công suất tăng 4 lần vì $P \propto V^2$).
5. **Lỗi thường gặp:**
   - Quên đặt nút `GND` $\implies$ Báo lỗi `Singular matrix`.
   - Nhầm nhãn: Đặt tên linh kiện $R_1$ thành giá trị điện trở.

---

### Ex0.2: Mô phỏng quá độ nạp và xả của mạch RC (.tran, .meas)
1. **Kiến thức giảng viên cần giải thích:**
   - Cơ chế nạp xả: Tụ tích trữ điện tích, điện áp trên tụ tỷ lệ với điện tích $q = C \cdot v_C$. Dòng điện qua tụ $i_C = C \frac{dv_C}{dt}$. Vì dòng điện hữu hạn nên $v_C$ không thể biến thiên gián đoạn (nhảy bậc).
   - Bản chất của các câu lệnh `.meas TRIG ... TARG ...`: Bắt thời điểm tín hiệu vượt qua ngưỡng điện áp xác định.
2. **Kịch bản hướng dẫn:**
   - Cho sinh viên tự cấu hình nguồn xung `PULSE(0 5.0 0 10n 10n 500u 1000u)`. Giải thích rõ: $T_{on} = 500\,\mu\text{s} = 5\tau$ để tụ nạp đầy $99,3\%$; $T_{period} = 1000\,\mu\text{s} = 10\tau$ để quan sát đủ cả chu kỳ nạp và xả.
   - Hướng dẫn mở Error Log (`Ctrl + L`) xem kết quả đo tự động.
3. **Kết quả tham chiếu:**
   - $\tau = 20\,\text{k}\Omega \times 5\,\text{nF} = 100,0\,\mu\text{s}$.
   - Trễ 50%: $t_{pd} = \ln(2) \cdot \tau = \mathbf{69,315\,\mu\text{s}}$ (SPICE đo được: $69,31 - 69,33\,\mu\text{s}$, sai lệch $< 0,05\%$).
   - Sườn tăng 10%–90%: $t_r = \ln(9) \cdot \tau = \mathbf{219,72\,\mu\text{s}} \approx 2,2\tau$ (SPICE đo được: $219,5 - 220,0\,\mu\text{s}$).
   - Đỉnh dòng nạp: $I_{peak,chg} = +\frac{5,0\,\text{V}}{20\,\text{k}\Omega} = \mathbf{+0,2500\,\text{mA}}$.
   - Đỉnh dòng xả: $I_{peak,dis} = -\frac{5,0\,\text{V}}{20\,\text{k}\Omega} = \mathbf{-0,2500\,\text{mA}}$.
4. **Câu hỏi gợi mở vấn đáp:**
   - *"Tại sao tại thời điểm $t = 0^+$, dòng nạp lại vọt lên cực đại ngay lập tức trong khi điện áp trên tụ vẫn bằng 0V?"* (Đáp: Tại $t=0^+$, tụ chưa tích điện xem như ngắn mạch, toàn bộ $5\,\text{V}$ đặt lên điện trở $R$).
5. **Lỗi thường gặp:**
   - Quên tham số `0.1u` trong lệnh `.tran 0 1m 0 0.1u` $\implies$ Đồ thị bị gãy khúc, lệnh `.meas` báo lỗi `Measurement FAIL`.
   - Đặt tụ ngược cực $\implies$ Dòng nạp hiển thị dấu âm, dòng xả hiển thị dấu dương.

---

### Ex0.3: Phân tích đáp ứng tần số AC và biểu đồ Bode (.ac)
1. **Kiến thức giảng viên cần giải thích:**
   - Mạch RC là bộ lọc thông thấp bậc một (First-Order Low-Pass Filter).
   - Hàm truyền đạt phức:
     $$H(j\omega) = \frac{1}{1 + j\omega RC} \implies |H(j\omega)| = \frac{1}{\sqrt{1 + (\omega RC)^2}}, \quad \angle H(j\omega) = -\arctan(\omega RC)$$
   - Tại tần số cắt $\omega_c = \frac{1}{RC} \implies f_c = \frac{1}{2\pi RC}$:
     $$|H(j\omega_c)| = \frac{1}{\sqrt{2}} \approx 0,707 \implies 20\log_{10}(0,707) \approx -3,01\,\text{dB}$$
     $$\angle H(j\omega_c) = -\arctan(1) = -45^\circ$$
2. **Kịch bản hướng dẫn:**
   - Nhắc sinh viên: Chế độ `.ac` yêu cầu nguồn phải có thuộc tính `AC 1`.
   - Hướng dẫn đọc biểu đồ Bode: Trục tung bên trái là biên độ ($0\,\text{dB}$ ở tần số thấp, suy giảm $-20\,\text{dB/decade}$ ở tần số cao); trục tung bên phải là góc pha ($0^\circ$ ở tần số thấp, $-45^\circ$ tại $f_c$, tiến về $-90^\circ$ ở tần số cao).
3. **Kết quả tham chiếu:**
   - $f_c = \frac{1}{2\pi \times 100\,\mu\text{s}} \approx \mathbf{1591,55\,\text{Hz}} \approx \mathbf{1,592\,\text{kHz}}$.
   - SPICE đo tự động: $f_c \approx 1591 - 1593\,\text{Hz}$ (Sai lệch $< 0,1\%$).
   - Góc pha đo được tại $f_c$: $-44,9^\circ \text{ đến } -45,1^\circ$.
4. **Câu hỏi gợi mở vấn đáp:**
   - *"Nếu tăng tụ điện $C$ lên 10 lần, tần số cắt của mạch sẽ dịch sang trái hay sang phải trên biểu đồ Bode?"* (Đáp: Tần số cắt giảm 10 lần, đường đặc tuyến dịch sang trái, băng thông mạch bị thu hẹp).

---

### Ex0.4: Khảo sát tham số với `.param` và `.step`
1. **Kiến thức giảng viên cần giải thích:**
   - Trong thiết kế mạch vi mô, các thông số nhiệt độ, điện áp nguồn và kích thước transistor luôn biến động. Lệnh `.step` là công cụ khảo sát độ nhạy (Sensitivity Analysis) và khảo sát góc công nghệ (Process Corners).
   - Quy luật trễ Elmore: $t_{pd} = \ln(2) \cdot C \cdot R$. Vì $C$ không đổi ($5\,\text{nF}$), trễ $t_{pd}$ là hàm bậc nhất của $R$ với hệ số góc $\text{Slope} = \ln(2) \cdot C$.
2. **Kịch bản hướng dẫn:**
   - Nhắc sinh viên kiểm tra cú pháp `{Rval}` trên sơ đồ.
   - Hướng dẫn dùng menu ngữ cảnh trong Error Log để kích hoạt công cụ vẽ đồ thị tự động **Plot .step'ed .meas data**.
3. **Kết quả tham chiếu:**
   - $R = 5\,\text{k}\Omega \implies t_{pd} = 17,33\,\mu\text{s}$
   - $R = 10\,\text{k}\Omega \implies t_{pd} = 34,66\,\mu\text{s}$
   - $R = 20\,\text{k}\Omega \implies t_{pd} = 69,32\,\mu\text{s}$
   - $R = 40\,\text{k}\Omega \implies t_{pd} = 138,63\,\mu\text{s}$
   - Độ dốc thực nghiệm:
     $$\text{Slope} = \frac{138,63 - 17,33}{40 - 5} = \frac{121,30\,\mu\text{s}}{35\,\text{k}\Omega} = \mathbf{3,4657\,\text{ns}/\text{k}\Omega}$$
   - Kiểm chéo với lý thuyết: $\ln(2) \cdot C = 0,69315 \times 5\,\text{nF} = \mathbf{3,4657 \times 10^{-9}\,\text{s}/\Omega} \implies$ Khớp đồng bộ $100\%$.

---

### Ex0.5: Giới thiệu mô hình MOSFET công nghệ C5N
1. **Kiến thức giảng viên cần giải thích:**
   - MOSFET là linh kiện 4 cực: Cực má (Drain), Cực cổng (Gate), Cực nguồn (Source), Cực thân (Bulk/Substrate).
   - Tệp `.model` chứa các tham số vật lý bán dẫn thực tế trích xuất từ xưởng đúc chip (MOSIS).
   - Mô hình Shichman-Hodges bậc hai bỏ qua hiệu ứng hạt dẫn kênh ngắn:
     $$I_{D,sat} = \frac{1}{2} K'_n \left(\frac{W}{L}\right) (V_{GS} - V_{tn})^2 = \frac{1}{2} (120\,\mu\text{A/V}^2) \left(\frac{1,2}{0,6}\right) (5,0 - 0,7)^2 \approx \mathbf{2,219\,\text{mA}}$$
   - Trong công nghệ C5N ($L = 0,6\,\mu\text{m}$), hiệu ứng **bão hòa vận tốc (Velocity Saturation)** làm electron đạt vận tốc giới hạn $v_{sat} \approx 10^7\,\text{cm/s}$, ghìm dòng điện thực tế xuống chỉ còn $\approx \mathbf{1,35 - 1,45\,\text{mA}}$.
2. **Kịch bản hướng dẫn:**
   - GV chiếu cách gõ `.include C5_models.txt`. Lưu ý tệp mô hình phải nằm chung thư mục với tệp mạch vẽ.
   - Yêu cầu sinh viên xem Netlist để thấy rõ cú pháp khai báo transistor:
     `M1 drain gate source bulk N W=1.2u L=0.6u`
3. **Kết quả tham chiếu:**
   - Dòng điện cực má mô phỏng: $I_D \approx 1,40\,\text{mA}$.
   - Sai lệch so với công thức bậc hai: Thấp hơn $\approx 37\%$.

---

## 0.9. BẢNG KẾT QUẢ MÔ PHỎNG THAM CHIẾU (BENCHMARK RESULTS)

Bảng số liệu chuẩn dùng để đối chiếu khi chấm bài thực hành của sinh viên:

| Bài | Thông số đo | Biểu thức lý thuyết | Giá trị Lý thuyết | Kết quả SPICE `.meas` | Sai lệch tương đối | Đánh giá nghiệm thu |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **Ex0.1** | $V(out)$ (.op) | $V_{in} \frac{R_2}{R_1+R_2}$ | $3,0000\,\text{V}$ | **$3,0000\,\text{V}$** | $0,00\%$ | Đạt hoàn toàn |
| **Ex0.1** | $I(R1)$ (.op) | $V_{in} / (R_1+R_2)$ | $0,1667\,\text{mA}$ | **$0,1667\,\text{mA}$** | $0,00\%$ | Dòng từ in sang out |
| **Ex0.1** | Hệ số góc DC | $R_2 / (R_1+R_2)$ | $0,6000$ | **$0,6000$** | $0,00\%$ | Tuyến tính đồng bộ |
| **Ex0.2** | Trễ $t_{pd}$ 50% | $\ln(2) \cdot RC$ | $69,315\,\mu\text{s}$ | **$69,32\,\mu\text{s}$** | $< 0,05\%$ | Chuẩn $\le 2,0\%$ |
| **Ex0.2** | Sườn tăng $t_r$ | $\ln(9) \cdot RC$ | $219,72\,\mu\text{s}$ | **$219,7\,\mu\text{s}$** | $< 0,10\%$ | Chuẩn $\le 2,0\%$ |
| **Ex0.2** | Sườn giảm $t_f$ | $\ln(9) \cdot RC$ | $219,72\,\mu\text{s}$ | **$219,7\,\mu\text{s}$** | $< 0,10\%$ | Chuẩn $\le 2,0\%$ |
| **Ex0.2** | Đỉnh dòng nạp | $+V_0 / R$ | $+0,2500\,\text{mA}$ | **$+0,2500\,\text{mA}$** | $0,00\%$ | Xuất hiện tại $t = 0^+$ |
| **Ex0.2** | Đỉnh dòng xả | $-V_0 / R$ | $-0,2500\,\text{mA}$ | **$-0,2500\,\text{mA}$** | $0,00\%$ | Đảo chiều tại $t = 500\,\mu\text{s}^+$ |
| **Ex0.3** | Độ lợi dải thông | $A_{V,0}$ | $1,000$ ($0\,\text{dB}$) | **$0,000\,\text{dB}$** | $0,00\%$ | Đo tại $10\,\text{Hz}$ |
| **Ex0.3** | Tần số cắt $f_c$ | $\frac{1}{2\pi RC}$ | $1591,55\,\text{Hz}$ | **$1592\,\text{Hz}$** | $< 0,10\%$ | Điểm biên độ $-3\,\text{dB}$ |
| **Ex0.3** | Góc pha tại $f_c$ | $-\arctan(1)$ | $-45,0^\circ$ | **$-45,0^\circ$** | $< 0,10\%$ | Đọc trên trục bên phải |
| **Ex0.4** | $t_{pd}$ ($R=5\text{k}$) | $\ln(2) \cdot 5\text{k} \cdot C$ | $17,329\,\mu\text{s}$ | **$17,33\,\mu\text{s}$** | $0,00\%$ | Bước quét 1 |
| **Ex0.4** | $t_{pd}$ ($R=10\text{k}$) | $\ln(2) \cdot 10\text{k} \cdot C$ | $34,657\,\mu\text{s}$ | **$34,66\,\mu\text{s}$** | $0,00\%$ | Bước quét 2 |
| **Ex0.4** | $t_{pd}$ ($R=20\text{k}$) | $\ln(2) \cdot 20\text{k} \cdot C$ | $69,315\,\mu\text{s}$ | **$69,32\,\mu\text{s}$** | $0,00\%$ | Bước quét 3 |
| **Ex0.4** | $t_{pd}$ ($R=40\text{k}$) | $\ln(2) \cdot 40\text{k} \cdot C$ | $138,629\,\mu\text{s}$ | **$138,63\,\mu\text{s}$** | $0,00\%$ | Bước quét 4 |
| **Ex0.4** | Độ dốc $\Delta t / \Delta R$ | $\ln(2) \cdot C$ | $3,4657\,\text{ns/k}\Omega$ | **$3,466\,\text{ns/k}\Omega$** | $< 0,05\%$ | Trùng khớp hoàn toàn |
| **Ex0.5** | Dòng $I_D$ NMOS | Shichman-Hodges | $\sim 2,22\,\text{mA}$ | **$1,35 - 1,45\,\text{mA}$** | $\sim 37\%$ | Bão hòa vận tốc hạt dẫn |

---

## 0.10. CÂU HỎI MỞ RỘNG VÀ ĐÁP ÁN GỢI Ý

1. **Câu hỏi:** *"Nếu trong phân tích quá độ `.tran`, ta đặt $T_{on} = 2\tau$ thay vì $5\tau$ thì điều gì sẽ xảy ra với các phép đo trễ và thời gian sườn?"*  
   - *Đáp án gợi ý:* Sau $2\tau$, điện áp tụ chỉ nạp được $V_0(1 - e^{-2}) \approx 86,5\% \cdot V_0$ ($4,32\,\text{V}$). Tụ chưa nạp no đã bị xả sớm, làm điện áp đỉnh bị sụt mất $13,5\%$. Hệ quả: phép đo sườn tăng $t_r$ ($10\% \to 90\%$) sẽ bị hỏng hoàn toàn vì điện áp không bao giờ chạm tới mốc $90\%$ ($4,5\,\text{V}$).
2. **Câu hỏi:** *"Tại sao trong mạch RC, tích giữa thời gian sườn tăng $t_r$ và tần số cắt $f_c$ lại là một hằng số không đổi xấp xỉ $0,35$?"*  
   - *Đáp án gợi ý:* Ta có $t_r = \ln(9) \cdot RC \approx 2,1972 \cdot RC$ và $f_c = \frac{1}{2\pi RC}$. Nhân hai vế:
     $$t_r \cdot f_c = (2,1972 \cdot RC) \cdot \left(\frac{1}{2\pi RC}\right) = \frac{2,1972}{2\pi} \approx \mathbf{0,3497} \approx \mathbf{0,35}$$
     Đây là quy tắc kinh điển áp dụng cho mọi hệ thống tuyến tính bậc một để ước lượng băng thông từ thời gian sườn tăng.
3. **Câu hỏi:** *"Trong mạch vi mạch thực tế, tụ điện $C_L$ ở ngõ ra một cổng logic đến từ những nguồn nào?"*  
   - *Đáp án gợi ý:* Đến từ 3 thành phần chính: (1) Tụ cực má khuếch tán ($C_{db}$) của chính cổng đó; (2) Tụ dây nối kim loại (Interconnect capacitance $C_{wire}$); (3) Tụ cực cổng ngõ vào ($C_{gate}$) của các cổng logic tầng kế tiếp mà nó phải lái.

---

## 0.11. BẢNG HƯỚNG DẪN XỬ LÝ LỖI THEO PHƯƠNG PHÁP GỢI MỞ (SOCRATIC DEBUGGING)

Khi sinh viên gặp lỗi, giảng viên **không sửa hộ** mà đặt các câu hỏi dẫn dắt để sinh viên tự tìm ra nguyên nhân:

| Hiện tượng lỗi trên màn hình | Nguyên nhân cốt lõi | Câu hỏi gợi mở giảng viên đặt cho sinh viên |
| :--- | :--- | :--- |
| Báo lỗi **`Singular Matrix`** hoặc **`Node is floating`** | Mạch chưa có nút đất tham chiếu `0`. | *"Em kiểm tra xem mạch điện của em đã có điểm mốc điện thế chuẩn chưa? SPICE tính điện áp so với nút nào?"* |
| Báo lỗi **`Unknown Subcircuit / Model not found`** | Sai tên model trong Netlist hoặc thiếu đường dẫn `.include`. | *"Tên model em gán cho transistor trên sơ đồ có khớp chính xác từng ký tự với tên ghi trong tệp thư viện C5_models.txt không?"* |
| Kết quả phân tích DC ra điện áp xấp xỉ $0\,\text{V}$ | Nhầm lẫn tiền tố `10M` thành $10\,\text{M}\Omega$. | *"Em xem lại bảng đơn vị SPICE: chữ M hoa đứng một mình biểu diễn giá trị gì? Muốn viết Mega em phải viết chữ gì?"* |
| Lệnh `.step` chạy xong nhưng 4 đường đồ thị trùng khít | Quên đặt ngoặc nhọn `{}` quanh tên biến tham số. | *"Linh kiện trên sơ đồ làm sao biết giá trị của nó là một biến số thay đổi chứ không phải là một chuỗi ký tự cố định?"* |
| Dòng điện nạp của tụ hiển thị giá trị âm | Đặt ngược chiều chân cực tính của tụ điện. | *"SPICE quy ước chiều dòng điện chạy qua linh kiện hai cực như thế nào? Cực dương của tụ em đang nối đi đâu?"* |
| Dạng sóng bị gãy góc, lệnh `.meas` báo **`FAIL`** | Bước thời gian cực đại `dTmax` quá lớn so với sườn xung. | *"Thời gian sườn xung của em là bao nhiêu nanosecond? Bước lấy mẫu của máy tính có đủ mịn để bắt được sườn dốc đó không?"* |

---

## 0.12. BỘ HÌNH ẢNH KỸ THUẬT MINH HỌA CHI TIẾT (10 HÌNH KỸ THUẬT)

### Hình 0.1: Lưu đồ quy trình mô phỏng SPICE chuẩn công nghiệp
```mermaid
flowchart TD
    A["Ý tưởng thiết kế mạch"] --> B["Vẽ sơ đồ Schematic\n(LTspice GUI)"]
    B --> C["Trích xuất Netlist\n(Tệp văn bản thuần .cir/.sp)"]
    D["Thư viện mô hình PDK\n(C5_models.txt)"] --> E["Bộ giải thuật toán MNA\n(SPICE Simulator Engine)"]
    C --> E
    F["Thiết lập phân tích:\n.OP, .DC, .TRAN, .AC"] --> E
    E --> G["Cửa sổ hiển thị dạng sóng\n(Waveform Viewer)"]
    E --> H["Trích xuất số đo tự động\n(SPICE Error Log: .meas)"]
    G --> I{"Kiểm chứng lý thuyết\nSai lệch <= 2%?"}
    H --> I
    I -- Đạt --> J["Đóng gói thư mục dự án"]
    I -- Không đạt --> K["Rà soát lỗi: Netlist, Bước thời gian dTmax"]
    K --> B
```
*Mô tả sư phạm:* Hình 0.1 làm rõ vị trí của Netlist và Model trong bộ giải MNA; nhấn mạnh vòng lặp kiểm chứng kỹ thuật trước khi đóng gói sản phẩm.

---

### Hình 0.2: Sơ đồ nguyên lý mạch phân áp DC (Ex0.1)
```
          V1 (5.0V)
             +
           (in)
             |
             +---/\/\/\/\/---+  R1 (12k)
             |
           (out) ------------> Vout = 3.0V (Đo .op)
             |
             +---/\/\/\/\/---+  R2 (18k)
             |
            GND (Nút 0)
```
*Mô tả sư phạm:* Phân tích định luật Ohm và phân chia điện thế; xác định rõ 3 nút điện: `in` (nút 5V), `out` (nút 3V), `0` (nút đất chuẩn).

---

### Hình 0.3: Đối chiếu 1-1 giữa Sơ đồ nguyên lý và Mã Netlist
```
+------------------------------------+----------------------------------------+
|      BẢN VẼ SƠ ĐỒ NGUYÊN LÝ        |          MÃ NGUỒN NETLIST TƯƠNG ỨNG    |
+------------------------------------+----------------------------------------+
|   V1 in 0 DC 5.0                   | * Lab 0 Voltage Divider Netlist        |
|   R1 in out 12k                    | V1 in 0 DC 5.0                         |
|   R2 out 0 18k                     | R1 in out 12k                          |
|   .op                              | R2 out 0 18k                           |
|                                    | .op                                    |
|                                    | .end                                   |
+------------------------------------+----------------------------------------+
```
*Mô tả sư phạm:* Giúp sinh viên xóa bỏ sự mơ hồ giữa giao diện đồ họa và bản chất văn bản thuần của Netlist; hiểu rằng SPICE chỉ đọc các dòng text mô tả kết nối nút.

---

### Hình 0.4: Sơ đồ mạch RC nạp xả quá độ với nguồn xung PULSE (Ex0.2)
```
                   R1 (20k)
   in ------------/\/\/\/\/------------+------------ out
   ^                                   |
   | Nguồn xung PULSE                  |
   | V1=0V, V2=5V, Ton=500u          +---+
   | Tperiod=1000u, Tr=Tf=10n        |   | C1 (5nF)
   |                                 +---+
   |                                   |
  GND (0)                             GND (0)
```
*Mô tả sư phạm:* Xác định các tham số nguồn xung kích thích; giải thích vì sao cần $T_{on} = 5\tau = 500\,\mu\text{s}$ để tụ nạp đầy.

---

### Hình 0.5: Dạng sóng nạp xả quá độ với các mốc thời gian đặc trưng
```
  Điện áp (V)
   5.0V +-----------------------------+ - - - - - - - - - - - - - + V_0
        |         . - - ' '           |                           |
   4.5V | - - - -/- - - - - - - - - - | - - - - - - - - - - - - - | 90%
        |       /                     | \                         |
   3.16V| - - -/- - - - - - - - - - - | - \ - - - - - - - - - - - | 63.2% (1 tau)
   2.5V | - - / - - - - - - - - - - - | - - \ - - - - - - - - - - | 50% (t_50 = 0.69 tau)
        |    /                        |      \                    |
   0.5V | - / - - - - - - - - - - - - | - - - -\- - - - - - - - - | 10%
    0V  +--+----+---------+-----------+---------+-----------------+
        0  t10  t50      1tau        5tau      10tau             Thời gian (t)
           |<-- t_r ----->|                     |<-- t_f ------>|
```
*Mô tả sư phạm:* Đánh dấu trực quan các mốc $1\tau$ ($63,2\%$), $5\tau$ ($99,3\%$), trễ $t_{50\%}$ và thời gian sườn xung $t_r, t_f$.

---

### Hình 0.6: Biểu đồ Bode đáp ứng tần số của mạch lọc RC thông thấp (Ex0.3)
```
  Biên độ (dB)                                          Góc pha (độ)
    0 dB +---------------+                              0 deg +---------------+
         |               \                                    |               \
   -3 dB | - - - - - - - -* (f_c = 1.59 kHz)           -45 deg| - - - - - - - -* (f_c)
         |                 \                                  |                 \
  -20 dB |                  \ Độ dốc -20dB/dec         -90 deg|                  +-----
         +--------------------+---------> Tần số              +--------------------+-----> Tần số
         10 Hz               1.59 kHz   100 kHz               10 Hz               1.59 kHz 100 kHz
```
*Mô tả sư phạm:* Minh họa đặc tính lọc thông thấp; chỉ rõ điểm tần số cắt $f_c$ tương ứng biên độ $-3\,\text{dB}$ và độ dịch pha $-45^\circ$.

---

### Hình 0.7: Đồ thị quét tham số `.step` và Tính tuyến tính của trễ theo điện trở (Ex0.4)
```
  Dạng sóng quá độ V(out) theo 4 bước R         Đồ thị thực nghiệm trễ t_pd theo R
   Vout (V)                                      t_pd (us)
    5V +    R=5k   10k   20k    40k              140 |                           * (40k, 138.6us)
       |     /     /     /      /                    |                          /
       |    /     /     /      /                  70 |              * (20k, 69.3us)
    2.5| - * - - * - - * - - -*                      |             /
       |  /     /     /      /                    35 |      * (10k, 34.7us)
    0V +-+-----+-----+------+-------> t           17 | * (5k, 17.3us)
         |     |     |      |                        +---+------+------+------+-----> R (kOhm)
       tpd1  tpd2   tpd3   tpd4                          5k    10k    20k    40k
                                                     Độ dốc Slope = ln(2)*C = 3.466 ns/kOhm
```
*Mô tả sư phạm:* Thấy rõ họ đường cong nạp xả biến đổi theo $R$; chứng minh bằng thực nghiệm quan hệ tuyến tính đồng bộ giữa độ trễ và giá trị điện trở.

---

### Hình 0.8: Cấu trúc khai báo linh kiện MOSFET trong SPICE Netlist (Ex0.5)
```
       CỰC MÁNG (Drain: Nút 1)
              |
              |     CỰC CỔNG (Gate: Nút 2)
           +--+--+     |
           |     |<----+
           |  N  |
           |     |<----+ CỰC THÂN (Bulk: Nút 4)
           +--+--+
              |
              |
       CỰC NGUỒN (Source: Nút 3)

       CÚ PHÁP NETLIST:
       M1  drain  gate  source  bulk   N   W=1.2u   L=0.6u
       ^     ^      ^      ^      ^    ^     ^        ^
      Tên   Cực D  Cực G  Cực S  Cực B Tên Chiều    Chiều
     Linh                             Model rộng    dài kênh
     kiện                             trong kênh
                                      PDK
```
*Mô tả sư phạm:* Giải phẫu 4 cực của transistor MOSFET và ánh xạ chính xác vào từng trường tham số của dòng lệnh khai báo Netlist.

---

### Hình 0.9: Cầu nối tiến hóa: Từ mạch RC cơ bản đến Cổng Inverter CMOS
```
 GIAI ĐOẠN 1: MẠCH RC THỰC HÀNH       GIAI ĐOẠN 2: CÔNG TẮC ĐIỆN TỬ       GIAI ĐOẠN 3: TẾ BÀO INVERTER CMOS
         R1 (20k)                                    Ron,p                               VDD (5V)
  Vin --/\/\/\--+-- Vout                    VDD -----/\/\/\---+                         +---+
                |                                             |                         |Mp | PMOS (Kéo lên)
              +---+                                         +---+                       +---+
              | C | (5nF)                                   |CL | (Tụ ký sinh)  Vin ----+---+---- Vout
              +---+                                         +---+                       |Mn | NMOS (Kéo xuống)
                |                                             |                         +---+
               GND                          GND -----/\/\/\---+                           |
                                                    Ron,n                                GND
  (Khảo sát mạch tuyến tính)            (Mô hình hóa kênh dẫn)              (Vi mạch tích hợp thực tế)
```
*Mô tả sư phạm:* Hình ảnh mang tính triết lý sư phạm cao nhất bài: Nối liền mạch kiến thức giải tích mạch tuyến tính ở Lab 0 với kiến thức thiết kế vi mạch CMOS ở Lab 1.

---

### Hình 0.10: Cửa sổ nhật ký lỗi SPICE Error Log và Đọc kết quả đo lường `.meas`
```
+-----------------------------------------------------------------------------------------+
|  SPICE Error Log (Phím tắt: Ctrl + L)                                            - X    |
+-----------------------------------------------------------------------------------------+
| Circuit: * Lab0 RC Circuit Transient Benchmark Netlist                                  |
|                                                                                         |
| Direct Newton iteration for .op point succeeded.                                        |
|                                                                                         |
| Measurement: t_pd                                                                       |
|   step  trig_time    targ_time    t_pd                                                  |
|      1  1.00000e-08  6.93248e-05  6.93148e-05  <-- Kết quả đo trễ 50%: 69.315 us       |
|                                                                                         |
| Measurement: t_r                                                                        |
|   step  trig_time    targ_time    t_r                                                   |
|      1  1.05361e-05  2.30258e-04  2.19722e-04  <-- Thời gian tăng: 219.72 us            |
|                                                                                         |
| Measurement: i_peak_chg                                                                 |
|   step  max_val      at_time                                                            |
|      1  0.000250000  1.00000e-08               <-- Đỉnh dòng nạp: +250.0 uA             |
|                                                                                         |
| Total transient steps: 14208, Points: 14208, Iterations: 28416                          |
| Simulation completed successfully in 0.047 seconds.                                     |
+-----------------------------------------------------------------------------------------+
```
*Mô tả sư phạm:* Minh họa thực tế giao diện Error Log trong LTspice; hướng dẫn sinh viên vị trí đọc từng số liệu và cách kiểm tra thông báo hoàn thành của chương trình.

---

## 0.13. RUBRIC ĐÁNH GIÁ KỸ THUẬT VÀ PHÂN QUYỀN ĐIỂM SỐ (THANG 10)

| Tiêu chuẩn đánh giá | Trọng số | Mức Xuất sắc (90% - 100%) | Mức Đạt chuẩn (70% - 85%) | Mức Cần cố gắng (< 70%) |
| :--- | :---: | :--- | :--- | :--- |
| **Kỹ năng thực hành tại lớp (Ex0.1 – Ex0.3)** | **4.0 đ** | Dựng mạch chuẩn xác, vận hành trơn tru cả 3 chế độ `.op`, `.tran`, `.ac`. Trích xuất đầy đủ 5 số đo tự động bằng `.meas` với sai số $\le 2\%$. | Dựng được mạch, chạy được mô phỏng nhưng phải nhờ trợ giúp; số liệu đo đạt sai số $\le 5\%$. | Mạch không chạy, thiếu nút đất, không trích xuất được số liệu bằng `.meas`. |
| **Khảo sát tham số & MOSFET (Ex0.4 – Ex0.5)** | **2.0 đ** | Thiết lập đúng biến `{Rval}`, quét đúng 4 bước, vẽ được đồ thị thực nghiệm và tính đúng độ dốc. Gọi model C5N đo được dòng $I_D$. | Chạy được lệnh `.step` nhưng chưa vẽ được đồ thị độ dốc; gọi được model C5N. | Quên ngoặc nhọn `{}` làm kết quả quét bị sai; không liên kết được thư viện C5N. |
| **Hiểu bản chất qua câu hỏi tư duy** | **2.0 đ** | Trả lời sắc bén, chính xác bản chất vật lý của các câu hỏi tư duy (vai trò nút đất, hằng số $\tau$, ý nghĩa $5\tau$, sụt giảm biên độ AC). | Trả lời được các câu hỏi cơ bản nhưng phần giải thích bản chất vật lý còn mơ hồ. | Không trả lời được câu hỏi hoặc chỉ chép lại công thức mà không hiểu ý nghĩa. |
| **Đóng gói dự án & Báo cáo kỹ thuật (Phần B)** | **2.0 đ** | Thư mục dự án tổ chức đồng bộ đúng cấu trúc; sơ đồ và Netlist đầy đủ; báo cáo trung thực, có ghi nhận lỗi và cách sửa. | Thư mục còn thiếu một số tệp hình ảnh; báo cáo trình bày sơ sài. | Không nộp thư mục dự án hoặc sao chép báo cáo của sinh viên khác. |

---

## 0.14. LIÊN KẾT CHUYỂN TIẾP KIẾN THỨC VỚI BÀI 1 (LAB 1 PREVIEW)

Trước khi kết thúc buổi thực hành Lab 0, giảng viên dành 5 phút chuyển tiếp tư duy cho sinh viên:
1. **Từ mạch RC sang CMOS Inverter:** Nhắc lại công thức trễ $t_{pd} \approx 0,69 \cdot RC$. Trong Lab 1, sinh viên sẽ thay điện trở $R$ bằng kênh dẫn của 2 transistor NMOS và PMOS ghép lại để tạo thành cổng đảo logic đầu tiên.
2. **Từ nguồn xung lý tưởng sang dạng sóng thực tế:** Trong Lab 1, sinh viên sẽ quan sát thấy sườn xung ngõ vào và ngõ ra không còn là các đường thẳng lý tưởng nữa mà bị uốn cong do điện dung cực cổng và cực má của transistor.
3. **Sẵn sàng môi trường làm việc:** Khẳng định với sinh viên rằng thư mục `lab_vlsi/` và tệp `C5_models.txt` mà các em vừa cấu hình thành công hôm nay sẽ là nền tảng dùng chung cho toàn bộ 10 bài Lab thực hành tiếp theo!


---

# 1. LAB 1 — ĐẶC TÍNH I-V CỦA MOSFET VÀ CMOS INVERTER (CHƯƠNG 2, 3)

## 1.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Nhận biết và chỉ rõ 3 vùng hoạt động (Cut-off, Triode, Saturation) trên họ đặc tuyến thực tế; giải thích được vì sao dòng bão hòa bị uốn cong lên (hiệu ứng $\lambda$).
2. Hiểu bản chất điểm điện áp chuyển mạch $V_M$: do tỉ số độ dẫn dòng $r = \beta_p / \beta_n$ quyết định và tính được chính xác trước khi bật máy.
3. Nắm vững bản chất trễ truyền lan $t_{pd}$: công thức $0,69 \cdot R_{on} \cdot C_L$ là cận dưới lý tưởng; trễ đo thực tế phản ánh quá trình xả dòng biến thiên.
4. Nắm chắc quy trình thiết kế vật lý vi mạch: Schematic $\to$ VTC $\to$ Layout $\to$ DRC $\to$ LVS (NCC) $\to$ PEX. Không có LVS và DRC sạch, sơ đồ nguyên lý không có giá trị sản xuất.

---

## 1.2 Bản chất vật lý & Giải thích chuyên sâu cho giảng viên
### a. Phân biệt rõ hai ký hiệu $\lambda$
Ngay đầu buổi học, giảng viên phải viết lên bảng hai định nghĩa tách biệt hoàn toàn để tránh nhầm lẫn:
- $\lambda_{kênh}$ ($\text{V}^{-1}$): Hệ số điều chế chiều dài kênh trong phương trình dòng điện SPICE $I_{DS} = I_{DS0}(1 + \lambda_{kênh} V_{DS})$.
- $\lambda_{lưới}$ ($\mu\text{m}$): Đơn vị chiều dài cơ sở của lưới layout theo luật Mead-Conway SCMOS ($\lambda = 0,30\,\mu\text{m}$ trong tiến trình $0,5\,\mu\text{m}$).

### b. Suy dẫn điểm chuyển mạch $V_M$
Tại điểm chuyển mạch $V_{in} = V_{out} = V_M$, cả hai transistor NMOS và PMOS đều cùng ở trạng thái bão hòa:
$$I_{DS,n} = \frac{1}{2} K'_n \left(\frac{W}{L}\right)_n (V_M - V_{tn})^2$$
$$I_{DS,p} = \frac{1}{2} K'_p \left(\frac{W}{L}\right)_p (V_{DD} - V_M - |V_{tp}|)^2$$
Cân bằng dòng điện $I_{DS,n} = I_{DS,p}$ và đặt tỉ số sức mạnh:
$$r = \frac{\beta_p}{\beta_n} = \frac{K'_p (W/L)_p}{K'_n (W/L)_n}$$
Khai căn hai vế và rút ra biểu thức tổng quát:
$$V_M = \frac{V_{tn} + \sqrt{r} (V_{DD} - |V_{tp}|)}{1 + \sqrt{r}}$$

**Đối chiếu định lượng quan trọng:**
- Khi $r = 1$ (tức chọn $W_p / W_n = K'_n / K'_p = 3,0$):
  $$V_M = \frac{0,70 + 1,0 \cdot (5,0 - 0,80)}{2} = \frac{4,90}{2} = 2,45\,\text{V}$$
- **Lưu ý sửa lỗi Handout:** Handout cũ ghi "tỉ số 3/1 cho $V_M = 2,50\,\text{V}$" là sai lệch $50\,\text{mV}$. Lý do $V_M$ không nằm đúng giữa nguồn ($2,50\,\text{V}$) là do độ lệch điện áp ngưỡng chế tạo bản chất: $V_{tn} = 0,70\,\text{V} \neq |V_{tp}| = 0,80\,\text{V}$.
- Để đạt được $V_M = 2,500\,\text{V}$, cần giải phương trình ngược:
  $$\sqrt{r} = \frac{2,50 - 0,70}{5,0 - 2,50 - 0,80} = \frac{1,80}{1,70} \approx 1,0588 \implies r \approx 1,1211$$
  $$\left(\frac{W}{L}\right)_p = 3 \cdot 1,1211 \cdot \left(\frac{W}{L}\right)_n \approx 3,363 \cdot \left(\frac{W}{L}\right)_n$$
  Với $W_n = 4\lambda = 1,20\,\mu\text{m} \implies W_p = 13,45\lambda \approx 4,04\,\mu\text{m}$. Tuy nhiên, vì quy tắc thiết kế yêu cầu số nguyên $\lambda$, nên việc chọn $W_p = 12\lambda = 3,60\,\mu\text{m}$ ($W_p/W_n = 3,0$) là nghiệm tối ưu thực tế!

### c. Bảng đối chiếu điểm chuyển mạch $V_M$
| $W_p / W_n$ | Tỉ số $r$ | $V_M$ Suy dẫn bậc 2 | $V_M$ SPICE Level 3 | Cột Đo thực nghiệm | Nhận xét sư phạm |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **1,0** | 0,333 | $1,98\,\text{V}$ | $2,05\,\text{V}$ | `[        ]` | Kéo xuống thắng thế; VTC lệch mạnh sang trái. |
| **2,0** | 0,667 | $2,27\,\text{V}$ | $2,31\,\text{V}$ | `[        ]` | Low-skew inverter; dùng trong domino logic. |
| **3,0** | 1,000 | $2,45\,\text{V}$ | $2,47\,\text{V}$ | `[        ]` | Thiết kế chuẩn cân bằng trễ $t_{pHL} \approx t_{pLH}$. |
| **3,36** | 1,121 | $2,50\,\text{V}$ | $2,51\,\text{V}$ | `[        ]` | Cân bằng hoàn toàn điểm đối xứng $V_{DD}/2$. |

---

## 1.3 Hình minh họa chi tiết & Sơ đồ giải phẫu tế bào Inverter

```
                      VDD (5.0V)
                          |
                   +------+------+
                   |    PMOS     |
                   |  W=12λ, L=2λ|
    Vin -----------+--||---------+-------- Vout
                   |  W=4λ,  L=2λ|
                   |    NMOS     |
                   +------+------+
                          |
                         GND
```

*Sơ đồ nguyên lý và mặt cắt vật lý tế bào CMOS Inverter chuẩn (`INV_X1`). Vùng N-well bảo bọc PMOS ngăn đánh thủng ngược; các tiếp xúc Well-Tap ($N^+$ nối $V_{DD}$) và Substrate-Tap ($P^+$ nối GND) triệt tiêu ký sinh SCR chống Latch-up.*

*Mã nguồn SPICE tham chiếu sẵn sàng:*
- Mô phỏng VTC & Đo trễ: [cmos_inverter_vtc_tran.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_vtc_tran.sp)
- Kiểm chứng trích xuất PEX: [cmos_inverter_pex_postlayout.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_pex_postlayout.sp)

---

## 1.4 Giải thích bản chất trễ $t_{pd}$ và sai lệch với mô hình $0,69 \cdot RC$
- **Nguồn gốc công thức $0,69$:** Xuất phát từ phương trình vi phân phóng nạp mạch RC tuyến tính thuần túy: $V(t) = V_{DD} \cdot e^{-t/RC}$. Tại ngưỡng $50\%$ ($V(t) = 0,5 V_{DD}$), ta có $e^{-t/RC} = 0,5 \implies t_{50\%} = RC \ln 2 \approx 0,693 \cdot RC$.
- **Tại sao số đo SPICE luôn lớn hơn $\sim 1,5$ đến $1,8$ lần:**  
  Điện trở $R_{on,n} = 969\,\Omega$ được tính tại điểm cuối của quá trình xả ($V_{DS} \to 0$, vùng tuyến tính sâu). Tuy nhiên, khi ngõ vào chuyển từ $0 \to 5\,\text{V}$, tụ tải $C_L$ đang ở mức $5\,\text{V}$, làm NMOS hoạt động trong vùng **Bão hòa** trong suốt giai đoạn đầu ($V_{out} > 5,0 - 0,7 = 4,3\,\text{V}$) với dòng bão hòa bị chặn ở mức:
  $$I_{sat,n} \approx \frac{1}{2} K'_n \left(\frac{W}{L}\right)_n (V_{DD} - V_{tn})^2 = \frac{1}{2} (120\mu) (2) (4,3)^2 \approx 2,22\,\text{mA}$$
  Để xả điện áp từ $5,0\,\text{V}$ xuống ngưỡng $50\%$ ($2,5\,\text{V}$), thời gian xả dòng xấp xỉ bằng:
  $$t \approx \frac{C_L \cdot \Delta V}{I_{sat,n}} = \frac{50\,\text{fF} \cdot 2,5\,\text{V}}{2,22\,\text{mA}} \approx 56,3\,\text{ps}$$
  Con số $56,3\,\text{ps}$ này khớp chặt chẽ với kết quả tích phân giải tích số ($49,8\,\text{ps}$) và SPICE Level 3 ($59\,\text{ps}$), cao hơn rõ rệt so với con số tính nhanh $0,69 \cdot 969 \cdot 50\,\text{fF} = 33,6\,\text{ps}$.

---

# 2. LAB 2 — CỔNG TĨNH NAND2 VÀ NOR2 (CHƯƠNG 6)

## 2.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Hiểu bản chất mạng đối ngẫu tĩnh: PDN (kéo xuống) dùng NMOS và PUN (kéo lên) dùng PMOS. Nối tiếp trong mạng này tương ứng song song trong mạng kia.
2. Nắm vững nguyên tắc định cỡ theo trường hợp xấu nhất (Worst-Case Sizing): Tại sao cổng NOR2 lại tốn diện tích và có dung dung ngõ vào lớn hơn nhiều so với NAND2 trong công nghệ CMOS có $\mu_n / \mu_p \approx 3$.
3. Giải thích được hiện tượng trễ phụ thuộc vector chuyển mạch (Input-pattern dependency) và vai trò của điện tích tồn dư tại nút nội (Internal node charge).
4. Thực hành phương pháp đường Euler trên đồ thị dải khuếch tán để vẽ layout liền mạch không bị đứt đoạn.

---

## 2.2 Phân tích kỹ thuật & Bảng so sánh PPA
### a. Quy tắc định cỡ tương đương Inverter cơ sở
Để đảm bảo trễ không bị suy giảm so với Inverter chuẩn:
- **Cổng NAND2:**
  - PDN có 2 NMOS nối tiếp: Mỗi transistor phải rộng gấp đôi để tổng trở kéo xuống giữ nguyên $R_{on,n}$: $W_n = 2 \times 4\lambda = 8\lambda = 2,4\,\mu\text{m}$.
  - PUN có 2 PMOS song song: Trường hợp xấu nhất chỉ 1 nhánh dẫn, nên giữ nguyên kích thước $W_p = 12\lambda = 3,6\,\mu\text{m}$.
- **Cổng NOR2:**
  - PDN có 2 NMOS song song: Trường hợp xấu nhất 1 nhánh dẫn: $W_n = 4\lambda = 1,2\,\mu\text{m}$.
  - PUN có 2 PMOS nối tiếp: Vì PMOS đã yếu hơn 3 lần, việc nối tiếp 2 PMOS buộc mỗi transistor phải có chiều rộng kênh gấp đôi: $W_p = 2 \times 12\lambda = 24\lambda = 7,2\,\mu\text{m}$.

```
      NAND2 SCHEMATIC                      NOR2 SCHEMATIC
       VDD (5.0V)                           VDD (5.0V)
     +-----+-----+                               |
     |           |                         [PMOS A: 24λ]
 [PMOS A]    [PMOS B] (Mỗi cái 12λ)              |
     |           |                         [PMOS B: 24λ]
     +-----+-----+                               |
           |-------- Out                         +-------- Out
           |                                     |
     [NMOS A: 8λ]                          +-----+-----+
           |                               |           |
       (X_int)                         [NMOS A]    [NMOS B] (Mỗi cái 4λ)
           |                               |           |
     [NMOS B: 8λ]                          +-----+-----+
           |                                     |
          GND                                   GND
```

*Sơ đồ nguyên lý và định cỡ tế bào NAND2 và NOR2. Xem chi tiết ảnh đồ họa tại:*
- [nand2_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/nand2_schematic.png)
- [nor2_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/nor2_schematic.png)

### b. So sánh định lượng PPA giữa NAND2 và NOR2
| Tiêu chí so sánh | Cổng NAND2 | Cổng NOR2 | Tỉ lệ khác biệt | Ý nghĩa sư phạm |
| :--- | :---: | :---: | :---: | :--- |
| **Tổng chiều rộng kênh $\sum W$** | $2 \times 8\lambda + 2 \times 12\lambda = 40\lambda$ | $2 \times 4\lambda + 2 \times 24\lambda = 56\lambda$ | NOR2 lớn hơn **$+40,0\%$** | NAND2 tiết kiệm diện tích silicon hơn hẳn. |
| **Điện dung ngõ vào Pin A ($C_{in}$)** | $8\lambda + 12\lambda = 20\lambda$ ($14,2\,\text{fF}$) | $4\lambda + 24\lambda = 28\lambda$ ($20,0\,\text{fF}$) | NOR2 nặng hơn **$+40,0\%$** | Lái cổng NOR2 làm tầng trước chậm đi đáng kể. |
| **Logical Effort $g$** | $g = 20\lambda / 16\lambda = 1,25$ ($5/4$) | $g = 28\lambda / 16\lambda = 1,75$ ($7/4$) | NOR2 kém hơn **$+40,0\%$** | Trong thư viện chuẩn, NAND luôn được ưu tiên. |
| **Trễ nội ký sinh $p$** | $p = (24\lambda + 8\lambda) / 16\lambda = 2,0$ | $p = (24\lambda + 8\lambda) / 16\lambda = 2,0$ | Ngang bằng | Cùng có 2 cực má PMOS và 1 cực má NMOS tại Out. |

---

## 2.3 Cơ chế trễ nút nội (Internal Node Delay)
Trong chuỗi NMOS của NAND2, gọi $X_n$ là nút trung gian giữa transistor $M_A$ (gần Out) và $M_B$ (gần GND):
1. **Trường hợp tín hiệu $A$ đến sau ($B=1$ từ trước):** Nút $X_n$ đã được xả sẵn về $0\,\text{V}$ qua $M_B$. Khi $A$ bật lên $1$, dòng điện qua $M_A$ chỉ cần xả một mình tụ tải $C_L$. Trễ là nhỏ nhất.
2. **Trường hợp tín hiệu $B$ đến sau ($A=1$ từ trước):** Trước thời điểm chuyển mạch, nút $X_n$ đã bị nạp lên điện áp cao $V_X \approx V_{DD} - V_{tn}(V_X) \approx 3,6\,\text{V}$ (có xét hiệu ứng thân). Khi $B$ bật lên $1$, transistor $M_B$ phải xả đồng thời cả điện tích của tụ nút nội $C_{int}$ và tụ tải $C_L$.
- **Quy tắc thiết kế vàng cho sinh viên:** Tín hiệu đến muộn nhất trên đường tới hạn (Critical Path) luôn phải được gán vào chân cổng gần ngõ ra nhất ($M_A$) để tận dụng việc nút nội đã được xả trước!

---

# 3. LAB 3 — CỔNG PHỨC HỢP AOI/OAI VÀ LOGICAL EFFORT (CHƯƠNG 3, 6)

## 3.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Cổng logic phức hợp (Complex CMOS Gate AOI/OAI) giúp gom nhiều tầng logic thành một tầng duy nhất, loại bỏ các cổng inverter trung gian nhưng phải trả giá bằng việc xếp chồng transistor.
2. Nắm vững phương pháp Logical Effort (Sutherland-Sproull): mô hình trễ chuẩn hóa $d = g \cdot h + p$ để tính nhẩm kích thước và số tầng tối ưu của đường truyền mà không cần chạy SPICE.
3. Hiểu tính chất "đáy phẳng" của hàm tối ưu chuỗi đệm: số tầng tối ưu $N^*$ cho phép linh hoạt lựa chọn theo diện tích và công suất mà không làm suy giảm trễ quá mức.

---

## 3.2 Phân tích tế bào AOI21 và Định cỡ
Cổng AOI21 thực hiện hàm logic: $Y = \overline{(A \cdot B) + C}$.
- PDN: Nhánh nối tiếp $A-B$ mắc song song với nhánh $C$.
- PUN: Nhánh song song $A \parallel B$ mắc nối tiếp với nhánh $C$.

```
                       VDD (5.0V)
                           |
                     +-----+-----+
                     |           |
                 [PMOS A]    [PMOS B] (Mỗi cái 24λ)
                     |           |
                     +-----+-----+
                           |
                       (Nút nội P)
                           |
                       [PMOS C: 24λ]
                           |
                           +----------------- Out (Y)
                           |
                     +-----+-----+
                     |           |
                 [NMOS A]    [NMOS C: 4λ]
                  (8λ)       |
                     |           |
                 [NMOS B]        |
                  (8λ)           |
                     |           |
                     +-----+-----+
                           |
                          GND
```

*Sơ đồ nguyên lý tế bào AOI21_X1 và Chuỗi đệm Inverter tối ưu:*
- [aoi21_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/aoi21_schematic.png)
- [buffer_chain_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/buffer_chain_schematic.png)

### Bảng phân tích Logical Effort và Ký sinh của AOI21
| Ngõ vào | Cấu trúc dẫn điện tương ứng | Chiều rộng kênh $W_n + W_p$ | Logical Effort $g$ | Parasitic Delay $p$ |
| :---: | :--- | :---: | :---: | :---: |
| **Pin A** | 2 NMOS nối tiếp ($8\lambda$) + 2 PMOS nối tiếp ($24\lambda$) | $8\lambda + 24\lambda = 32\lambda$ | $g_A = 32/16 = \mathbf{2,00}$ | $p = 36/16 = \mathbf{2,25}$ |
| **Pin B** | 2 NMOS nối tiếp ($8\lambda$) + 2 PMOS nối tiếp ($24\lambda$) | $8\lambda + 24\lambda = 32\lambda$ | $g_B = 32/16 = \mathbf{2,00}$ | (Ngõ ra Out nối với cực má |
| **Pin C** | 1 NMOS đơn ($4\lambda$) + 2 PMOS nối tiếp ($24\lambda$) | $4\lambda + 24\lambda = 28\lambda$ | $g_C = 28/16 = \mathbf{1,75}$ | của $M_{PC}, M_{NA}, M_{NC}$) |

---

## 3.3 Tối ưu hóa chuỗi đệm Inverter (Inverter Buffer Chain)
- Cho tải lớn $C_L = 1,0\,\text{pF}$, ngõ vào lái $C_{in} = 20\,\text{fF} \implies$ Hệ số nỗ lực điện dung $H = C_L / C_{in} = 50,0$.
- Trễ tổng chuẩn hóa qua chuỗi $N$ tầng: $D = N \cdot H^{1/N} + N \cdot p_{inv}$. Lấy đạo hàm theo $N$ và giải nghiệm cho thấy nỗ lực tầng tối ưu là $\hat{f} \approx 3,6$ (khi $p_{inv} = 1$).

| Số tầng $N$ | Nỗ lực mỗi tầng $\hat{f} = H^{1/N}$ | Trễ chuẩn hóa $D/\tau$ | Tỉ lệ so với tối ưu | Kích thước các tầng ($W/L$) |
| :---: | :---: | :---: | :---: | :--- |
| **1 tầng** | 50,00 | $51,00\,\tau$ | Chậm gấp **$3,63$ lần** | Tầng 1: $1\text{X}$ ($4\lambda / 12\lambda$) lái thẳng $1\,\text{pF}$. |
| **2 tầng** | 7,07 | $16,14\,\tau$ | Chậm hơn $+14,8\%$ | $1\text{X} \to 7,07\text{X}$. |
| **3 tầng** | **3,68** | **$14,05\,\tau$** | **Tối ưu cực tiểu ($100\%$)** | $1\text{X} \to 3,68\text{X} \to 13,57\text{X}$. |
| **4 tầng** | 2,66 | $14,64\,\tau$ | Chậm hơn $+4,2\%$ | $1\text{X} \to 2,66\text{X} \to 7,07\text{X} \to 18,8\text{X}$. |
| **5 tầng** | 2,19 | $15,93\,\tau$ | Chậm hơn $+13,4\%$ | $1\text{X} \to 2,19\text{X} \to 4,78\text{X} \to 10,4\text{X} \to 22,9\text{X}$. |

**Chỗ cần chỉnh trong Handout gốc:** Handout ghi "tối ưu nhanh hơn $3,63$ lần (cải thiện $363\%$)". Giảng viên cần sửa cách dùng từ: Trễ giảm từ $51\,\tau$ xuống $14,05\,\tau$, tức tốc độ tăng $3,63$ lần, tương ứng thời gian trễ giảm $\frac{51 - 14,05}{51} \approx 72,5\%$. Không được dùng cụm từ "cải thiện $363\%$".

---

# 4. LAB 4 — CỔNG TRUYỀN (TG) VÀ BỘ DỒN KÊNH MUX (CHƯƠNG 6)

## 4.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Hiểu cặn kẽ vì sao một transistor đơn lẻ không thể làm công tắc logic đồng bộ: NMOS truyền mức 1 kém (Weak 1) và PMOS truyền mức 0 kém (Weak 0) do tác động của điện áp ngưỡng và hiệu ứng thân.
2. Hiểu cơ chế bù trừ độ dẫn của Cổng truyền CMOS (Transmission Gate): khi kết hợp song song NMOS và PMOS kích hoạt pha ngược, điện trở tương đương $R_{TG}$ trở nên gần như phẳng trên toàn dải điện áp ngõ vào.
3. Nắm vững mô hình trễ phân tán Elmore trong chuỗi cổng truyền: trễ tăng theo bình phương số tầng $O(N^2)$, từ đó giải thích vì sao cần chèn bộ đệm (Buffer).

---

## 4.2 Bản chất suy hao điện áp và dòng rò tĩnh
### a. NMOS truyền mức '1' và Hiệu ứng thân
Khi cổng của NMOS nối $V_{DD} = 5\,\text{V}$ và cực má nối $5\,\text{V}$, nguồn $V_{out}$ tăng dần. Transistor sẽ ngắt khi điện thế quá cổng $V_{GS}$ tụt xuống bằng điện áp ngưỡng $V_{tn}$:
$$V_{out,max} = V_{DD} - V_{tn}(V_{out,max})$$
Do cực nguồn ở điện thế cao trong khi thân (substrate p) nối đất ($0\,\text{V}$), điện thế thiên thế thân $V_{SB} = V_{out,max} > 0$. Theo phương trình hiệu ứng thân trong `C5_models.txt` ($\gamma = 0,40\,\text{V}^{1/2}, 2\Phi_F = 0,70\,\text{V}$):
$$V_{tn}(V_{SB}) = 0,70 + 0,40 \left(\sqrt{0,70 + V_{out}} - \sqrt{0,70}\right)$$
Giải phương trình tự nhất quán:
$$V_{out} = 5,0 - \left[0,70 + 0,40 \left(\sqrt{0,70 + V_{out}} - \sqrt{0,70}\right)\right] \implies V_{out,max} \approx \mathbf{3,631\,\text{V}}$$

### b. Hậu quả tai hại đối với tầng sau
Khi mức điện áp "Weak 1" ($3,63\,\text{V}$) này được đưa vào ngõ vào của một cổng Inverter tĩnh chuẩn tiếp theo:
- Cực cổng của PMOS ở mức $3,63\,\text{V}$, trong khi cực nguồn PMOS nối $V_{DD} = 5,0\,\text{V}$.
- Điện áp nguồn-cổng: $V_{SG,p} = 5,0 - 3,63 = 1,37\,\text{V}$.
- Vì $V_{SG,p} = 1,37\,\text{V} > |V_{tp}| = 0,80\,\text{V}$, transistor PMOS **không bao giờ ngắt hoàn toàn**!
- Kết quả: Tạo ra một dòng tĩnh xuyên qua Inverter lên tới $\approx 39\,\mu\text{A}$, làm tiêu tốn công suất tĩnh khổng lồ và làm suy giảm nghiêm trọng lề nhiễu mức cao $NM_H$. Đây là lý do sống còn vì sao các mạch logic transistor truyền (Pass-transistor logic) luôn bắt buộc phải có mạch khôi phục mức (Level Restorer).

---

## 4.3 Đặc tính điện trở dẫn tương đương $R_{TG}$
Độ dẫn tổng của cổng truyền khi cả hai transistor cùng dẫn ($1,0\,\text{V} \le V_{in} \le 4,0\,\text{V}$):
$$g_{TG} = g_n + g_p = K'_n \left(\frac{W}{L}\right)_n (V_{DD} - V_{in} - V_{tn}) + K'_p \left(\frac{W}{L}\right)_p (V_{in} - |V_{tp}|)$$
Khi ta chọn tỉ số kích thước cân bằng độ linh động $\beta_n = \beta_p$ (tức $K'_n W_n = K'_p W_p = 240\,\mu\text{A/V}^2$):
$$g_{TG} = \beta [V_{DD} - V_{tn} - |V_{tp}|] = \text{Hằng số không phụ thuộc } V_{in}!$$
$$g_{TG} = 240 \cdot 10^{-6} \cdot [5,0 - 0,70 - 0,80] = 840\,\mu\text{S} \implies R_{TG} = \frac{1}{g_{TG}} \approx \mathbf{1190\,\Omega} \approx 1,19\,\text{k}\Omega$$

**Chỗ cần chỉnh trong Handout gốc:** Handout ghi $R_{TG}$ tại $V_{in} = 2,5\,\text{V}$ là $490\,\Omega$ (do lấy nhầm $969\,\Omega \parallel 992\,\Omega$). Giảng viên chỉ rõ cho sinh viên: tại $2,5\,\text{V}$, độ mở quá cổng của cả hai transistor đều giảm một nửa, nên điện trở của mỗi nhánh tăng gấp đôi ($R_n \approx 2,3\,\text{k}\Omega, R_p \approx 2,45\,\text{k}\Omega$), khi mắc song song sẽ cho ra $\approx 1,19\,\text{k}\Omega$, chứ không phải $490\,\Omega$!

```
       TRANSMISSION GATE (TG)                   MUX 2:1 USING TG
               CLK_B                                   S_B
                 |                                      |
             +---o---+                              +---o---+
             | PMOS  |                              |  TG0  |
   In -------+       +------- Out         IN0 ------+       +-------+
             | NMOS  |                              |       |       |
             +-------+                              +-------+       |
                 |                                      |           |
                CLK                                     S           |
                                                                    +--- Out
                                                        S           |
                                                        |           |
                                                    +-------+       |
                                                    |  TG1  |       |
                                          IN1 ------+       +-------+
                                                    | PMOS  |
                                                    +---o---+
                                                        |
                                                       S_B
```

*Sơ đồ nguyên lý Cổng truyền CMOS (TG) và Bộ dồn kênh MUX 2:1 (`mux2_tg_schematic.png`).*  
*Tham khảo chi tiết ảnh đồ họa tại:* [mux2_tg_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/mux2_tg_schematic.png) và [tg_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/tg_schematic.png).

---

# 5. LAB 5 — MẠCH TUẦN TỰ: D-LATCH VÀ D-FLIP-FLOP (CHƯƠNG 7)

## 5.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Phân biệt rạch ròi giữa Mạch chốt (Latch - nhạy theo mức) và Mạch lật (Flip-Flop - nhạy theo sườn xung nhịp).
2. Nắm vững định nghĩa và phương pháp đo 3 thông số định thời sống còn: Thời gian thiết lập ($t_{setup}$), Thời gian giữ ($t_{hold}$), và Trễ từ xung nhịp đến ngõ ra ($t_{c-q}$).
3. Hiểu hiện tượng bất ổn định (Metastability) khi vi phạm cửa sổ định thời và quy tắc push-out $10\%$.
4. Nắm chắc phương trình ràng buộc chu kỳ xung nhịp hệ thống: $T_{clk} \ge t_{c-q} + t_{comb,max} + t_{setup} + t_{skew}$.

---

## 5.2 Bản chất kiến trúc Master-Slave và Cơ chế hoạt động
Mạch lật D-Flip-Flop kích hoạt sườn dương (Positive Edge-Triggered DFF) được ghép nối từ hai tầng D-Latch mắc nối tiếp điều khiển bởi hai pha xung nhịp ngược nhau:

```
               +----------------- MASTER LATCH ----------------+   +----------------- SLAVE LATCH -----------------+
               |                                               |   |                                               |
               |        TG1 (CLK_B)                 TG2 (CLK)  |   |        TG3 (CLK)                   TG4 (CLK_B)|
               |          +---+                       +---+    |   |          +---+                       +---+    |
      D -------+--------->|   |----+---[INV I1]--*--->|   |--+ |   |     +--->|   |----+---[INV I3]--*--->|   |--+ |
                          +---+    |    (X_M)    |    +---+  | |   |     |    +---+    |    (X_S)    |    +---+  | |
                                   |             |           | +---------+             |             |           | |
                                   +<--[INV I2]--+<----------+     |                   +<--[INV I4]--+<----------+ |
                                                                   |                                               |
                                                                   +-------------------[INV đệm]-----------------> Q
```

*Sơ đồ nguyên lý hoàn chỉnh D-Latch và D-Flip-Flop Master-Slave:*
- [dlatch_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/dlatch_schematic.png)
- [dff_ms_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/dff_ms_schematic.png)

### Bảng trạng thái hoạt động theo pha xung nhịp
| Trạng thái xung nhịp | Tầng Master | Tầng Slave | Toàn mạch DFF | Ý nghĩa chức năng |
| :---: | :---: | :---: | :---: | :--- |
| **$\text{CLK} = 0$** | **Trong suốt (Transparent):** TG1 mở, nhận dữ liệu $D$ vào nút nội $X_M$. | **Giữ (Hold):** TG3 ngắt, TG4 dẫn, vòng lặp phản hồi giữ giá trị $Q$ cũ. | **Chặn ngõ ra:** Mọi thay đổi trên $D$ chưa thể đi tới ngõ ra $Q$. | Chuẩn bị dữ liệu sẵn sàng tại nút $X_M$. |
| **Sườn lên $0 \to 1$** | **Đóng lại (Chuyển sang Giữ):** TG1 ngắt, khóa giá trị $D$ tại nút $X_M$. | **Mở ra (Chuyển sang Trong suốt):** TG3 dẫn, phóng dữ liệu từ $X_M$ ra $Q$. | **Chốt dữ liệu:** Giá trị của $D$ ngay trước sườn lên xuất hiện ở $Q$. | Điểm lấy mẫu sườn dương danh định. |
| **$\text{CLK} = 1$** | **Giữ (Hold):** TG1 ngắt hoàn toàn; cách ly hoàn toàn $D$ với mạch. | **Trong suốt (Transparent):** Nút $X_S$ tiếp tục lái ngõ ra $Q$. | **Khóa an toàn:** Ngăn chặn hiện tượng chạy đua dữ liệu (Race condition). | Dữ liệu ngõ ra $Q$ hoàn toàn ổn định. |

---

## 5.3 Phương pháp đo $t_{setup}, t_{hold}$ và Hiện tượng Metastability
- **Quy tắc đẩy trễ $10\%$ (10% Push-out Rule):**  
  Thời gian thiết lập $t_{setup}$ danh định được xác định là khoảng cách thời gian nhỏ nhất giữa sườn dữ liệu $D$ và sườn xung nhịp $\text{CLK}$ sao cho trễ $t_{c-q}$ chỉ tăng tối đa $10\%$ so với giá trị lý tưởng khi $D$ đến rất sớm.
- **Hiện tượng bất ổn định (Metastability):**  
  Khi $D$ thay đổi quá gần sườn xung nhịp, nút nội $X_M$ không kịp đạt mức logic đầy đủ ($0\,\text{V}$ hoặc $5\,\text{V}$) mà dừng ở vùng lơ lửng quanh ngưỡng $V_M \approx 2,45\,\text{V}$. Vòng phản hồi hai inverter mất thời gian phục hồi tăng theo quy luật hàm mũ:
  $$t_{resolve} = \tau_{reg} \cdot \ln \left(\frac{V_{DD}}{\Delta V_0}\right)$$
  với $\Delta V_0$ là độ lệch ban đầu so với $V_M$.

---

# 6. LAB 6 — MẠCH CỘNG TOÀN PHẦN (1-BIT FULL ADDER) (CHƯƠNG 6)

## 6.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Hiểu sâu kiến trúc vi mạch số: $Sum$ là hàm XOR 3 ngõ vào đối xứng, trong khi $C_{out}$ là hàm đa số (Majority function - bằng 1 khi có từ 2 ngõ vào trở lên bằng 1).
2. Hiểu vì sao kiến trúc Mirror Adder 28T thống trị các thư viện chuẩn ASIC: tính tự đối ngẫu giúp PDN và PUN có cấu trúc topo giống hệt nhau, và việc tái sử dụng $\overline{C_{out}}$ để tạo $Sum$ giúp tiết kiệm tối đa số lượng transistor.
3. Nhận thức rõ ràng: Tốc độ của bộ cộng gợn sóng $N$-bit (Ripple Carry Adder) bị chi phối trực tiếp bởi trễ lan truyền số nhớ $C_{in} \to C_{out}$, không phải trễ $Sum$.

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
- [mirror_adder_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/mirror_adder_schematic.png)
- [tg_adder_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/tg_adder_schematic.png)

### Bảng kiểm kê và sửa lỗi Handout về số lượng Transistor
| Khối chức năng vi mạch | Số Transistor thực tế | Handout cũ ghi nhầm | Phân tích giải phẫu kỹ thuật |
| :--- | :---: | :---: | :--- |
| **Khối tạo số nhớ $\overline{C_{out}}$** | **10T** ($5\text{P} + 5\text{N}$) | "4 NMOS + 4 PMOS" | Nhánh $A \cdot B$ tốn 2T; nhánh $C_{in}(A+B)$ tốn 3T $\implies 5\text{T}$ mỗi mạng. |
| **Bộ đệm Inverter cho $C_{out}$** | **2T** ($1\text{P} + 1\text{N}$) | Bỏ quên | Khôi phục cực tính và tăng cường khả năng lái cho tầng sau. |
| **Khối tạo tổng $\overline{Sum}$** | **14T** ($7\text{P} + 7\text{N}$) | Không tách bạch | Nhánh $A \cdot B \cdot C_{in}$ tốn 3T; nhánh $\overline{C_{out}}(A+B+C_{in})$ tốn 4T $\implies 7\text{T}$ mỗi mạng. |
| **Bộ đệm Inverter cho $Sum$** | **2T** ($1\text{P} + 1\text{N}$) | Bỏ quên | Cần thiết để lật cực tính từ $\overline{Sum} \to Sum$. |
| **TỔNG TOÀN TẾ BÀO FA** | **28T** | "24 đến 28T" | Con số chuẩn xác duy nhất là **28 Transistors**. |

---

# 7. LAB 7 — LOGIC ĐỘNG (DYNAMIC CMOS) VÀ DOMINO (CHƯƠNG 6)

## 7.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Hiểu chu trình hoạt động 2 pha: Pha nạp trước (Precharge - $\text{CLK}=0$) và Pha đánh giá (Evaluate - $\text{CLK}=1$).
2. Nắm vững bản chất hiện tượng chia sẻ điện tích (Charge Sharing) tại các nút nội và điều kiện gây lật giả logic.
3. Hiểu cơ chế hoạt động và kích thước của transistor bù rò (Keeper): cuộc giằng co giữa Keeper và PDN.
4. Nắm chắc tính chất đơn điệu (Monotonicity) của logic động và giải thích được vì sao bắt buộc phải có cổng Inverter tĩnh giữa các tầng Domino.

---

## 7.2 Phân tích hiện tượng chia sẻ điện tích (Charge Sharing)
Xét mạch logic động với nút động $X$ có điện dung $C_X$. Giả sử bên trong mạng PDN có một nút nội trung gian $C_{int}$ ban đầu mang điện tích $0\,\text{V}$.
- Trong pha Evaluate, nếu ngõ vào làm thông các transistor phía trên nút nội nhưng transistor phía dưới ngắt:
- Điện tích ban đầu $Q = C_X \cdot V_{DD}$ sẽ tái phân bố giữa $C_X$ và $C_{int}$.
- Điện áp sụt giảm tức thời trên nút $X$:
  $$V'_X = V_{DD} \cdot \frac{C_X}{C_X + C_{int}}$$
- **Minh họa bằng số:** Với $C_X = 20\,\text{fF}$ và $C_{int} = 14\,\text{fF}$:
  $$V'_X = 5,0 \cdot \frac{20}{20 + 14} \approx \mathbf{2,94\,\text{V}}$$
- **Lề an toàn đối với cổng Inverter tĩnh phía sau:**
  Vì ngưỡng chuyển mạch của Inverter tĩnh là $V_M \approx 2,45\,\text{V}$, điện áp $V'_X = 2,94\,\text{V} > 2,45\,\text{V}$. Do đó lề nhiễu mức cao còn lại:
  $$NM_H = 2,94 - 2,45 = \mathbf{0,49\,\text{V}}$$
  Nếu có thêm nhiễu xuyên âm (Crosstalk) hoặc dòng rò dưới ngưỡng (Subthreshold leakage), $V'_X$ sẽ tụt qua $2,45\,\text{V}$, làm ngõ ra Inverter lật lên $1$ giả tạo!

```
                    DOMINO CMOS LOGIC GATE
                          VDD (5.0V)
                              |
                     +--------+--------+
                     |                 |
                [PMOS Precharge]  [PMOS Keeper] (W=2λ)
                 (Gate: CLK)      (Gate: Y)
                     |                 |
                     +--------+--------+
                              |
                            (Nút X)---------------+
                              |                   |
                        +-----+-----+             |
                        |    PDN    |         +---+---+
                        | Logic NMOS|         |Static |
                        +-----+-----+         |Invert.|---- Out (Y)
                              |               +---+---+
                        [NMOS Foot] (W=8λ)
                         (Gate: CLK)
                              |
                             GND
```

*Sơ đồ nguyên lý Logic động thuần và Cổng Domino hoàn chỉnh:*
- [dynamic_cmos_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/dynamic_cmos_schematic.png)
- [domino_logic_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/domino_logic_schematic.png)

---

# 8. LAB 8 — Ô NHỚ SRAM 6T VÀ SENSE AMPLIFIER (TỰ CHỌN / ĐỒ ÁN)

## 8.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Hiểu mâu thuẫn thiết kế cốt lõi của ô nhớ SRAM 6T: Chế độ Đọc đòi hỏi Driver phải mạnh hơn Access (tránh phá hủy dữ liệu - Read Stability), trong khi chế độ Ghi đòi hỏi Access phải mạnh hơn Load (đè được dữ liệu cũ - Writeability).
2. Nắm vững phương pháp đo Lề nhiễu tĩnh (Static Noise Margin - SNM) thông qua đường cong cánh bướm (Butterfly Curve).
3. Hiểu nguyên lý hoạt động của Mạch khuếch đại cảm nhận (Sense Amplifier): sử dụng phản hồi dương để biến chênh lệch điện áp nhỏ ($\Delta V \approx 100-150\,\text{mV}$) thành mức logic đầy đủ trong thời gian cực ngắn, tiết kiệm $>90\%$ năng lượng nạp xả bitline.

---

## 8.2 Bản chất hai ràng buộc kích thước: CR và PR
Quy tắc kích thước vàng: $\text{Driver} > \text{Access} > \text{Load}$.

```
                            SRAM 6T CELL SCHEMATIC
                     BL                                    BLB
                      |                                     |
                [NMOS AX1: 4λ]                        [NMOS AX2: 4λ]
                (Gate: WL)                            (Gate: WL)
                      |                                     |
                      +-----------*-------------*-----------+
                      |           |             |           |
                      |        [PMOS L1]     [PMOS L2]      |
                      |         (W=2λ)        (W=2λ)        |
                    (Nút Q)       |             |        (Nút QB)
                      |         +----+-------+----+         |
                      |              | VDD   |              |
                [NMOS D1: 8λ]        |       |        [NMOS D2: 8λ]
                 (Gate: QB)          +-------+         (Gate: Q)
                      |                                     |
                     GND                                   GND
```

*Sơ đồ nguyên lý ô nhớ SRAM 6T và Mạch khuếch đại vi sai Sense Amplifier:*
- [sram_6t_cell_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/sram_6t_cell_schematic.png)
- [sense_amplifier_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/sense_amplifier_schematic.png)

### a. Phân tích ổn định khi đọc (Read Stability & Cell Ratio CR)
Khi đọc nút $Q = 0\,\text{V}$, đường Bitline $BL$ đã được nạp trước lên $5,0\,\text{V}$. Khi $WL$ bật lên $5,0\,\text{V}$, dòng điện từ $BL$ đổ dồn qua Access Transistor $M_{AX1}$ vào nút $Q$ và thoát xuống GND qua Driver Transistor $M_{D1}$.
- Lúc này, $M_{AX1}$ ở vùng Bão hòa ($V_{DS} = 5,0 - V_Q > V_{GS} - V_{tn}$), trong khi $M_{D1}$ ở vùng Tuyến tính.
- Cân bằng dòng điện giữa hai transistor và đặt $u = V_{DD} - V_{tn} = 4,3\,\text{V}$:
  $$(u - V_Q)^2 = CR \cdot (2u V_Q - V_Q^2)$$
  Giải phương trình bậc hai cho điện áp đỉnh dâng lên tại nút $Q$:
  $$V_Q = u \cdot \left[1 - \sqrt{\frac{CR}{1 + CR}}\right]$$
  Với $CR = \frac{W_D}{W_{AX}} = \frac{8\lambda}{4\lambda} = 2,0$:
  $$V_Q = 4,3 \cdot \left[1 - \sqrt{\frac{2}{3}}\right] = 4,3 \cdot [1 - 0,8165] \approx \mathbf{0,789\,\text{V}}$$

**Chỗ cần chỉnh trong Handout gốc:**
Handout cũ ghi công thức gần đúng $V_Q \approx \frac{V_{DD} - V_{tn}}{2 \cdot CR} = \frac{4,3}{4} = 1,075\,\text{V}$ và yêu cầu $V_Q < V_{tn} = 0,70\,\text{V}$. Đây là một mâu thuẫn toán học nghiêm trọng (vừa tính ra $1,075\,\text{V}$ lại vừa đòi nhỏ hơn $0,70\,\text{V}$).  
Giảng viên giải thích cho sinh viên: Tiêu chí chuẩn xác không phải so với $V_{tn}$, mà $V_Q$ phải nhỏ hơn **ngưỡng lật của Inverter đối diện** ($M_{L2} - M_{D2}$). Với $W_D / W_L = 8\lambda / 2\lambda = 4,0$, ngưỡng lật của nửa ô nhớ đối diện lên tới $V_{trip} \approx 1,48\,\text{V}$. Do đó mức dâng $V_Q = 0,789\,\text{V}$ hoàn toàn an toàn dưới $1,48\,\text{V}$!

---

# 9. LAB 9 — BỘ CỘNG NHANH 4-BIT CLA (CARRY LOOKAHEAD ADDER) (TỰ CHỌN / ĐỒ ÁN)

## 9.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Hiểu tư duy thiết kế vi mạch bậc cao: Triệt tiêu sự phụ thuộc tuần tự của chuỗi số nhớ bằng cách biểu diễn tín hiệu nhớ dưới dạng biểu thức đại số logic song song.
2. Nắm vững phương trình sinh nhớ ($G_i = A_i \cdot B_i$) và truyền nhớ ($P_i = A_i \oplus B_i$).
3. Nhận thức giới hạn vật lý của Fan-in: Việc khai triển biểu thức $C_4$ dẫn tới cổng AOI có 5 transistor NMOS xếp chồng, làm tăng điện trở kéo xuống và đòi hỏi giải pháp phân cụm (Hierarchical Carry Lookahead).
4. Đánh giá khách quan sự đánh đổi PPA: Tăng $\sim 20\%$ diện tích và số lượng transistor để đổi lấy tốc độ nhanh hơn $>50\%$ so với Ripple Carry Adder.

---

## 9.2 Khai triển biểu thức và Kiểm kê phần cứng vi mạch

```
                     CLA 4-BIT ARCHITECTURE
             A[3:0]                     B[3:0]
               |                          |
               +------------+-------------+
                            |
                     [PG GENERATOR] (48T)
                    Gi = Ai.Bi, Pi = Ai^Bi
                            |
                 +----------+----------+
                 | P[3:0]              | G[3:0]
                 v                     v
              +---------------------------+ <--- Cin
              |   CARRY LOOKAHEAD (CLG)   | (62T)
              | C1, C2, C3, C4 Generation |
              +---------------------------+
                 |       |       |       |
                 C1      C2      C3      C4 (Carry Out)
                 |       |       |       |
                 +-------+-------+-------+
                 |
                 v
           [SUM GENERATOR] (24T: 4 XOR)
             Si = Pi ^ Ci
                 |
                 v
              SUM[3:0]
```

*Sơ đồ khối kiến trúc CLA 4-bit và Sơ đồ nguyên lý khối CLG:*
- [cla_4bit_architecture.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/cla_4bit_architecture.png)
- [clg_carry_logic_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/clg_carry_logic_schematic.png)

### Bảng phân bổ 134 Transistor của tế bào CLA 4-bit chuẩn
| Khối chức năng | Thành phần logic chi tiết | Số Transistor | Tỉ lệ phần cứng |
| :--- | :--- | :---: | :---: |
| **Khối PG Generator** | 4 cổng NAND2 ($4 \times 4\text{T}$) + 4 cổng XOR ($4 \times 6\text{T}$) + 4 INV | **48T** | $35,8\%$ |
| **Khối tạo Carry CLG** | $C_1$ (6T) + $C_2$ (12T) + $C_3$ (20T) + $C_4$ (30T) + 4 INV (8T) | **62T** | $46,3\%$ |
| **Khối tạo Sum** | 4 cổng XOR 2 ngõ vào ($S_i = P_i \oplus C_i$) | **24T** | $17,9\%$ |
| **TỔNG TOÀN KHỐI CLA** | **Kiến trúc CLA 4-bit nguyên khối** | **134T** | **$100\%$** |

---

# 10. LAB 10 — CAPSTONE: ALU 4-BIT TÍCH HỢP CÓ THANH GHI (ĐỒ ÁN)

## 10.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Trải nghiệm trọn vẹn quy trình thiết kế vi mạch tích hợp hệ thống (System-on-Chip Top-Down Design Flow): từ đặc tả tập lệnh $\to$ phân rã khối $\to$ thiết kế tế bào $\to$ Floorplanning $\to$ đóng gói PEX $\to$ nghiệm thu toàn diện.
2. Làm chủ bài toán Ngân sách thời gian (Timing Budget) trên đường tới hạn: xác định chính xác tần số xung nhịp cực đại $f_{max}$.
3. Nắm vững kỹ thuật thiết kế mạng phân phối nguồn (Power Grid Network) và ước lượng độ sụt áp tĩnh/động ($IR\text{-drop}$ và $L \cdot di/dt$).
4. Kỷ luật nghiệm thu công nghiệp: Bộ vi mạch chỉ được xem là hoàn tất khi vượt qua đồng thời DRC 0 lỗi, LVS so khớp đồng bộ $100\%$ và mô phỏng sau trích xuất PEX đảm bảo đúng chức năng logic.

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
- [alu_4bit_top_architecture.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/alu_4bit_top_architecture.png)
- [alu_chip_layout_floorplan.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/alu_chip_layout_floorplan.png)

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

# 11. BẢNG TỔNG HỢP CÁC ĐIỂM CẦN CHỈNH SỬA TRONG HANDOUT GỐC (MASTER ERRATA)

| Bài Lab | Vị trí trong Handout | Lỗi kỹ thuật / Mâu thuẫn phát hiện | Mức độ | Hướng điều chỉnh chính xác trước khi lên lớp |
| :---: | :--- | :--- | :---: | :--- |
| **Chung** | Toàn bộ 10 bài | Tham chiếu ảnh `images/` bị lỗi đường dẫn; lộ thư mục đáp án `03 - Instructor_Solutions/`. | **C** | Thay đường dẫn ảnh chuẩn nội bộ; xóa bỏ toàn bộ dấu vết thư mục đáp án trong bản phát cho SV. |
| **Lab 1** | Mục I & Pre-lab | Ghi $W_p/W_n = 3,0$ cho $V_M = 2,50\,\text{V}$; dùng lẫn lộn $\lambda_{kênh}$ và $\lambda_{lưới}$. | **C** | Đính chính: $3/1$ cho $V_M = 2,45\,\text{V}$; muốn $2,50\,\text{V}$ cần $3,36$. Viết tách biệt $\lambda_{kênh}$ và $\lambda_{lưới}$ trên bảng. |
| **Lab 2** | Mục III.3 & III.4 | Sơ đồ Stick NAND2 vẽ thiếu chân Out; khẳng định hoàn toàn "NAND luôn nhanh hơn NOR". | **C** | Bổ sung nút Out vào sơ đồ Euler; ghi rõ điều kiện "nhanh hơn khi độ linh động electron lớn hơn lỗ trống". |
| **Lab 3** | Mục III.1 & III.4 | Ghi "AOI21 giảm diện tích 40%"; ghi "cải thiện tốc độ 363%"; $C_{in} = 20\,\text{fF}$ không khớp. | **C** | Sửa thành "giảm $40\%$ số transistor, giảm $18\%$ tổng chiều rộng kênh"; sửa thành "nhanh hơn $3,63$ lần (giảm $72\%$ trễ)". |
| **Lab 4** | Mục III.1 & III.2 | $R_{TG}$ tại $2,5\,\text{V}$ ghi $490\,\Omega$; Weak 0 của PMOS ghi $0,8-1,05\,\text{V}$ (quên Body Effect). | **C** | Đính chính: $R_{TG}(2,5\,\text{V}) \approx 1,19\,\text{k}\Omega$. Điện áp Weak 0 thực tế dâng lên $\approx 1,4\,\text{V}$ do hiệu ứng thân PMOS. |
| **Lab 5** | Mục III.3 | Lỗi font ký tự tiếng Hoa ("điện荷"); vẽ thiếu inverter đệm ngõ ra làm sai số transistor. | **C** | Xóa ký tự lạ; chuẩn hóa sơ đồ DFF 18T (gồm 2 Latch 8T + 1 Inverter xung nhịp 2T). |
| **Lab 6** | Mục III.2 & III.3 | Khối Carry ghi nhầm "4 NMOS + 4 PMOS"; công thức Sum bị sai vế trái; đếm transistor mơ hồ. | **C** | Sửa thành 5 NMOS + 5 PMOS ($10\text{T}$); vế trái là $\overline{Sum}$; chốt cứng tổng 28 Transistors. |
| **Lab 7** | Mục III.4 | Lấy ví dụ OR4 để giải thích chia sẻ điện tích; gọi inverter $16\lambda/8\lambda$ là "high-skew". | **C** | Thay ví dụ OR4 bằng AND3/AND4 (có nút nội xếp chồng); đính chính inverter $16\lambda/8\lambda$ là **low-skew** ($V_M \approx 2,27\,\text{V}$). |
| **Lab 8** | Mục III.2a | Công thức $V_Q \approx \frac{V_{DD}-V_{tn}}{2CR}$ cho $1,08\,\text{V} > V_{tn}$, tự mâu thuẫn tiêu chí. | **C** | Thay bằng công thức giải tích đúng $V_Q \approx 0,789\,\text{V}$; tiêu chí an toàn là so với ngưỡng lật $V_{trip} \approx 1,48\,\text{V}$. |
| **Lab 9** | Mục III.3 | Định cỡ chuỗi 5 NMOS chỉ cho $8\lambda$; câu hỏi Pre-lab lộ đáp án "hoàn toàn xứng đáng". | **C** | Giải thích sự đánh đổi diện tích ($8\lambda$ chấp nhận điện trở lớn gấp 2,5 lần); đổi câu hỏi thành "Dự đoán, đo và so sánh". |
| **Lab 10** | Mục I & III | Đếm transistor vênh giữa MUX4 ($64\text{T}$ vs $72\text{T}$); mục tiêu $1\,\text{GHz}$ chưa có cơ sở thực nghiệm. | **C** | Thống nhất cách đếm 358 Transistors toàn chip; khẳng định $f_{max,PEX} \approx 1,42\,\text{GHz}$ đủ sức đạt chuẩn $1,0\,\text{GHz}$. |

*(Quy ước mức độ: **C** = Chắc chắn sai lệch lý thuyết/toán học, bắt buộc phải đính chính trước khi giảng dạy).*

---

# 12. KẾ HOẠCH HÀNH ĐỘNG VÀ GIẢI QUYẾT TRIỆT ĐỂ CÁC ĐIỂM CHƯA KIỂM

Nhằm chuyển đổi toàn bộ các nhãn "Chưa kiểm" thành "Đã kiểm chứng $100\%$", bộ phận giảng viên và trợ giảng thực hiện theo quy trình 6 bước sau trước tuần lễ bắt đầu học kỳ:

1. **Khóa cứng tham số mô hình PDK C5N:**
   Toàn bộ máy tính phòng lab sử dụng duy nhất tệp [C5_models.txt](file:///d:/tam/VLSI_Spice/04%20-%20Models_and_Libraries/C5_models.txt). Tên model trong netlist SPICE là `N` cho NMOS và `P` cho PMOS (cú pháp: `M1 Out In GND GND N W=... L=...`).
2. **Chạy đối chuẩn tự động bằng mã Python:**
   Trước buổi học, trợ giảng chạy toàn bộ chuỗi script kiểm chứng tự động trong thư mục `scripts/`:
   ```powershell
   python scripts/verify_lab01_new.py
   python scripts/verify_lab02.py
   python scripts/verify_lab03.py
   python scripts/verify_lab04.py
   python scripts/verify_lab05.py
   python scripts/verify_lab06.py
   python scripts/verify_lab07.py
   python scripts/verify_lab08.py
   python scripts/verify_lab09.py
   python scripts/verify_lab10.py
   ```
3. **Thực thi mô phỏng SPICE mẫu:**
   Mở LTspice và chạy lần lượt các tệp netlist nghiệm thu chuẩn trong `03 - Instructor_Solutions/` để nắm vững các điểm đo `.meas` và dạng sóng chuẩn:
   - Đo VTC và trễ Inverter: `03 - Instructor_Solutions/lab01/cmos_inverter_vtc_tran.sp`
   - Quét dịch pha $t_{setup}, t_{hold}$: `03 - Instructor_Solutions/lab05/setup_hold_sweep.sp`
   - Đo đường cong bướm SNM: `03 - Instructor_Solutions/lab08/sram_snm_butterfly.sp`
   - Quét tần số tới hạn ALU: `03 - Instructor_Solutions/lab10/alu_fmax_timing_sweep.sp`
4. **Cập nhật số liệu vào cột "Đo thực nghiệm":**
   Điền các giá trị đo thực tế ghi nhận được từ dàn máy phòng lab vào các cột `[ Đo ]` trong các bảng đối chiếu từ Lab 1 đến Lab 10 để làm đáp án chuẩn thống nhất cho toàn bộ cán bộ chấm thi.
5. **Đồng bộ hóa thư viện Layout trong Electric VLSI:**
   Kiểm tra tệp thư viện `lab_vlsi.jelib` trong Electric, xác nhận công nghệ đang chọn là `mocmos` (MOSIS CMOS Submicron, $\lambda = 0,30\,\mu\text{m}$). Kiểm tra luật N-well bao P-active tối thiểu $6\lambda$ và Active bao Contact tối thiểu $1,5\lambda$.
6. **Lưu trữ và phân quyền:**
   Tài liệu Giáo trình nội bộ này được lưu trữ độc quyền trong thư mục quản trị `03 - Instructor_Solutions/Teacher_Book_VLSI_Lab01_Lab10.md`. Khi xuất bản tài liệu cho sinh viên, chỉ trích xuất các phần bài tập thực hành trong `02 - Student Workbook/` và hoàn toàn loại bỏ các gợi ý giải thích cơ chế, đáp án giải tích và các netlist tham chiếu.
