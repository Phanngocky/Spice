# Lab 1 — Gói giảng viên (Đặc tính MOSFET và CMOS Inverter)

Tài liệu chuyên môn nội bộ dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH Sư phạm Kỹ thuật – ĐH Đà Nẵng.  
Đi kèm tài liệu phát cho sinh viên: **"THỰC HÀNH THIẾT KẾ VLSI — BÀI 1: ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER"**.

> **Trạng thái kiểm chứng.**
> - Giá trị giải tích lý thuyết và mô phỏng số: Tính toán và kiểm chứng bằng script `scripts/verify_lab01_new.py` (mô hình giải tích số Level 3 xấp xỉ có xét hệ số điều chế kênh $\lambda = 0,05\,\text{V}^{-1}$).
> - Netlist SPICE tham chiếu: `nmos_iv_curve.sp`, `pmos_iv_curve.sp`, `cmos_inverter_vtc_only.sp`, `cmos_inverter_vtc_tran.sp`, `cmos_inverter_pex_postlayout.sp` đã được rà soát và kiểm chứng tương thích chuẩn LTspice XVII / 2025 và Electric VLSI 9.07+.
> - Cột "Đo": Cung cấp giá trị mốc kiểm chuẩn (Benchmark) từ mô phỏng chuẩn và để trống ô số liệu cho giảng viên ghi nhận kết quả thực tế trên dàn máy phòng lab.

---

## A. KẾ HOẠCH BUỔI VÀ VIỆC CHUẨN BỊ

### A1. Mục đích của buổi học
Buổi học thực hành Lab 1 là bước chuyển bản lề từ mô phỏng linh kiện rời rạc thụ động (Lab 0) sang thiết kế tế bào logic vi mạch tích hợp CMOS cơ sở. Sau buổi học, sinh viên cần mang ra khỏi phòng máy 3 thói quen kỹ thuật cốt lõi:
1. **Thói quen "Tính trước, đo sau, so sánh và giải thích sai lệch":** Tránh chấp nhận thụ động một con số từ phần mềm mà phải luôn có giá trị ước lượng giải tích để đối chứng. Khi số đo trễ thực tế chênh lệch so với mô hình $0,69 \cdot R_{on} \cdot C_L$, sinh viên phải biết giải thích dựa trên cơ chế chuyển tiếp từ vùng bão hòa sang vùng tuyến tính.
2. **Kỹ năng kiểm chứng vật lý đa chiều (Full-Flow IC Design):** Nắm vững chu trình thiết kế vi mạch hoàn chỉnh từ Schematic $\to$ Phân tích VTC $\to$ Đo trễ Transient $\to$ Mask Layout $\to$ Kiểm tra luật DRC $\to$ So khớp sơ đồ LVS $\to$ Trích xuất ký sinh PEX.
3. **Ý thức kỷ luật thiết kế vi mạch chống phá hủy:** Thấu hiểu nguyên lý vật lý của hiện tượng Latch-up và ghi nhớ quy tắc sinh tử: mọi tế bào logic đều phải được bố trí đầy đủ tiếp xúc phân cực Substrate Tap và Well Tap.

### A2. Phân bổ 135 phút thực hành

| Thời lượng | Phân đoạn | Nội dung hoạt động chính | Ghi chú hướng dẫn cho Giảng viên |
| :---: | :--- | :--- | :--- |
| **15 phút** (00–15') | **C0. Cổng kiểm tra Pre-lab** | Kiểm tra bài chuẩn bị ở nhà (P1–P5) tại bàn; ký phiếu kiểm tra đầu giờ. | SV thiếu P2 hoặc P4 chưa được bật máy tính. Nhắc nhở quy ước lưới $\lambda = 0,30\,\mu\text{m}$. |
| **25 phút** (15–40') | **C1. Ex1.1: Đặc tính I-V MOSFET** | Quét DC hai biến trên LTspice; vẽ họ đặc tuyến $I_{DS}-V_{DS}$ và truyền dẫn $I_{DS}-V_{GS}$; đo $V_{th}, \lambda$. | Hướng dẫn dùng cú pháp `.dc VDS 0 5 0.01 VGS 1 5 1`; đo $\lambda$ tại nhánh $V_{GS}=5\,\text{V}$. |
| **25 phút** (40–65') | **C2. Ex1.2: Schematic & VTC** | Dựng Schematic `inv_x1` trong Electric, xuất netlist sang LTspice; quét DC $V_{in}$; đo $V_M, NM_L, NM_H$. | Hướng dẫn thêm pane đồ thị vẽ đạo hàm `d(V(out))/d(V(in))` để tìm chính xác điểm dốc $-1$. |
| **25 phút** (65–90') | **C3. Ex1.3: Đo trễ với `.meas`** | Đặt nguồn PULSE ($50\,\text{MHz}$), tải dung $C_L = 50\,\text{fF}$; chạy `.meas` trích xuất trễ; đóng gói Icon View. | Yêu cầu SV mở SPICE Error Log (`Ctrl+L`) để đọc số; đối chiếu với công thức $0,69 R C$. |
| **25 phút** (90–115')| **C4. Ex1.4: Mask Layout & LVS** | Vẽ Layout trong Electric tuân thủ quy tắc MOSIS; chạy DRC (phím `F5`); chạy đối chiếu NCC (LVS). | Hướng dẫn đặt Taps chống Latch-up; sửa lỗi lệch tên Export làm LVS không match. |
| **10 phút** (115–125')| **C5. Ex1.5: Trích xuất PEX** | Bật trích xuất tụ ký sinh, xuất netlist PEX; mô phỏng lại Transient, đo độ tăng trễ hậu layout. | Cho SV thấy các dòng tham số `AS, AD, PS, PD` và tụ dây kim loại làm trễ tăng thêm $\sim 40-50\%$. |
| **10 phút** (125–135')| **C6. Nghiệm thu & Tổng kết** | Vấn đáp nhanh tại bàn (1 câu hỏi); ký phiếu nghiệm thu kết quả; nhắc thời hạn nộp bài. | Đánh giá thái độ, kiểm tra thư viện `lab_vlsi.jelib` đã lưu đủ các cell hay chưa. |

### A3. Việc Giảng viên cần chuẩn bị trước buổi thực hành
- [ ] Kiểm tra dàn máy tính: Đảm bảo phần mềm Electric VLSI và LTspice đã cài đặt đầy đủ; đường dẫn liên kết công cụ trong Electric (*Preferences $\to$ Tools $\to$ Spice/CDL*) trỏ chính xác đến tệp thực thi của LTspice.
- [ ] Kiểm tra thư viện PDK: Đảm bảo tệp mô hình `C5_models.txt` đã được sao chép sẵn vào thư mục mẫu trên máy chủ phòng lab.
- [ ] Mở và chạy thử trước 5 tệp netlist mẫu trong thư mục `03 - Instructor_Solutions/lab01/` để nắm chắc dạng sóng chuẩn trên màn hình.
- [ ] Chuẩn bị bảng đáp án Pre-lab P1–P5 để đối chiếu nhanh và ký xác nhận đầu buổi cho sinh viên.

---

## B. KIẾN THỨC NỀN DÀNH CHO GIẢNG VIÊN

### B1. Mô hình dòng điện Level 3 so với mô hình bậc hai sách giáo khoa
Trong giảng dạy lý thuyết, mô hình bậc hai (Square-Law Shichman-Hodges) thường được sử dụng vì tính trực quan giải tích:
- Tuyến tính: $I_{DS} = K' \frac{W}{L} [(V_{GS} - V_{th})V_{DS} - \frac{1}{2}V_{DS}^2]$
- Bão hòa: $I_{DS} = \frac{1}{2} K' \frac{W}{L} (V_{GS} - V_{th})^2 (1 + \lambda V_{DS})$

Tuy nhiên, trong mô hình bán dẫn thực tế MOSIS C5N ($L = 0,6\,\mu\text{m}$, thuộc dải dưới micron - Submicron), mô hình Level 3 của SPICE tích hợp thêm các hiệu ứng vật lý phức tạp:

**1. Suy giảm độ linh động (Mobility Degradation):** Dưới tác động của điện trường dọc cực mạnh vuông góc với mặt oxit cổng, độ linh động của hạt dẫn trong kênh bị suy giảm:

$$\mu_{eff} = \frac{\mu_0}{1 + \theta (V_{GS} - V_{th})}$$

**2. Vận tốc bão hòa hạt dẫn (Velocity Saturation):** Khi điện trường ngang má-nguồn vượt quá ngưỡng tới hạn $\mathcal{E}_{sat}$, vận tốc hạt dẫn đạt giới hạn tối đa ($v_{sat} \approx 10^7\,\text{cm/s}$ với electron). Hiện tượng này khiến transistor NMOS đi vào bão hòa sớm hơn so với dự đoán của mô hình bậc hai ($V_{DS,sat} < V_{GS} - V_{th}$), và dòng bão hòa phụ thuộc tuyến tính vào $(V_{GS} - V_{th})$ thay vì bậc hai.

**3. Hiệu ứng thân (Body Effect):** Điện thế phân cực ngược giữa Source và Bulk làm mở rộng vùng nghèo, làm tăng điện áp ngưỡng thực tế:

$$V_{th} = V_{th0} + \gamma \left(\sqrt{2\Phi_F + V_{SB}} - \sqrt{2\Phi_F}\right)$$

Giảng viên cần lưu ý: Dù các hiệu ứng trên làm sai khác dòng điện so với tính tay, nhưng ở nút công nghệ $0,5\,\mu\text{m}$, mô hình bậc hai vẫn là công cụ ước lượng xuất sắc để kiểm tra tính hợp lý của kết quả mô phỏng (trong phạm vi sai lệch chấp nhận được từ 10% đến 20%).

### B2. Dẫn xuất giải tích chi tiết điểm chuyển mạch $V_M$
Điểm chuyển mạch $V_M$ của Inverter là điểm giao giữa đường cong VTC với đường phân giác $V_{out} = V_{in} = V_M$.

Tại $V_{in} = V_{out} = V_M$:
- Transistor NMOS có: $V_{GS,n} = V_M$, $V_{DS,n} = V_M$. Vì $V_{DS,n} \ge V_{GS,n} - V_{thn} \iff V_M \ge V_M - V_{thn}$ (luôn đúng do $V_{thn} > 0$), nên **NMOS hoạt động trong vùng bão hòa**.
- Transistor PMOS có: $|V_{GS,p}| = V_{DD} - V_M$, $|V_{DS,p}| = V_{DD} - V_M$. Tương tự, $|V_{DS,p}| \ge |V_{GS,p}| - |V_{thp}|$ (luôn đúng do $|V_{thp}| > 0$), nên **PMOS cũng hoạt động trong vùng bão hòa**.

Cân bằng dòng điện Kirchhoff tại nút ngõ ra $I_{D,n} = |I_{D,p}|$:

$$\frac{1}{2} k_n (V_M - V_{thn})^2 = \frac{1}{2} k_p (V_{DD} - V_M - |V_{thp}|)^2$$

Lấy căn bậc hai hai vế, đặt $r = \frac{k_p}{k_n} = \frac{K_p' (W/L)_p}{K_n' (W/L)_n} \implies \sqrt{r} = \sqrt{\frac{k_p}{k_n}}$:

$$V_M - V_{thn} = \sqrt{r} (V_{DD} - V_M - |V_{thp}|)$$

$$(1 + \sqrt{r}) V_M = V_{thn} + \sqrt{r} (V_{DD} - |V_{thp}|)$$

$$V_M = \frac{V_{thn} + \sqrt{r} (V_{DD} - |V_{thp}|)}{1 + \sqrt{r}}$$

#### Biện luận sư phạm về tỉ số định kích thước:
- **Trường hợp sách giáo khoa lý tưởng ($V_{thn} = |V_{thp}|$):**
  Nếu $V_{thn} = |V_{thp}|$, ta có $V_M = V_{DD}/2 \iff \sqrt{r} = 1 \iff r = 1$.  
  Điều này dẫn đến tỉ số kích thước: $\frac{(W/L)_p}{(W/L)_n} = \frac{K_n'}{K_p'} = \frac{120}{40} = 3,00$.
- **Trường hợp tiến trình MOSIS C5N thực tế ($V_{thn} = 0,70\,\text{V}, |V_{thp}| = 0,80\,\text{V}$):**
  Nếu chọn $r = 1$ (tỉ số $W_p/W_n = 3,00$):

$$V_M = \frac{0,70 + 1,0 \times (5,0 - 0,80)}{1 + 1,0} = \frac{0,70 + 4,20}{2} = \mathbf{2,450\,\text{V}}$$

  Độ lệch so với $2,50\,\text{V}$ chỉ là $0,05\,\text{V}$ (sai lệch tương đối $2\%$).
- **Để đạt chính xác $V_M = 2,500\,\text{V}$:**

$$2,50 = \frac{0,70 + \sqrt{r}(5,0 - 0,80)}{1 + \sqrt{r}} \implies 2,50 + 2,50\sqrt{r} = 0,70 + 4,20\sqrt{r}$$

$$1,70\sqrt{r} = 1,80 \implies \sqrt{r} = \frac{1,80}{1,70} \approx 1,0588$$

$$r = 1,0588^2 \approx 1,1211 \implies \frac{(W/L)_p}{(W/L)_n} = 1,1211 \times 3,00 = \mathbf{3,363}$$

  Với $W_n = 4\lambda = 1,20\,\mu\text{m}$, ta cần $W_p = 3,363 \times 1,20\,\mu\text{m} = 4,036\,\mu\text{m} \approx 13,45\lambda$.
- **Lý do chọn $W_p = 12\lambda = 3,60\,\mu\text{m}$ trong thực tế:**
  Lưới thiết kế hình học layout của MOSIS C5N có đơn vị $\lambda = 0,30\,\mu\text{m}$. Mọi kích thước hình học bắt buộc phải là số nguyên $\lambda$. Nếu chọn $13\lambda$ ($3,9\,\mu\text{m}$) hoặc $14\lambda$ ($4,2\,\mu\text{m}$) sẽ làm lẻ lưới và phá vỡ cấu trúc đối xứng ô chuẩn. Vì vậy, lựa chọn chuẩn công nghiệp là $W_p = 12\lambda$ và $W_n = 4\lambda$ (tỉ số nguyên $3/1$), chấp nhận dịch chuyển điểm $V_M$ xuống $2,45\,\text{V}$ ($2\%$) nhưng đạt được hiệu quả vượt trội về diện tích và tính mô-đun hóa tế bào chuẩn.

### B3. Điện trở kênh dẫn hiệu dụng $R_{on}$ và giới hạn của mô hình $0,69 \cdot R_{on} \cdot C_L$
Tại chế độ triode sâu ($V_{DS} \to 0$ khi cực cổng phân cực tối đa $V_{GS} = V_{DD}$):
- Transistor NMOS: $R_{on,n} = \frac{1}{K_n' (W/L)_n (V_{DD} - V_{thn})} = \frac{1}{(240 \times 10^{-6}) \times (5,0 - 0,70)} = \mathbf{969\,\Omega}$.
- Transistor PMOS: $R_{on,p} = \frac{1}{K_p' (W/L)_p (V_{DD} - |V_{thp}|)} = \frac{1}{(240 \times 10^{-6}) \times (5,0 - 0,80)} = \mathbf{992\,\Omega}$.

Hai giá trị này gần như cân bằng đối xứng ($\approx 1,0\,\text{k}\Omega$), chứng minh tính đối xứng dẫn nạp của thiết kế.

#### Bản chất sự sai khác giữa mô hình $0,69 R C$ và trễ đo thực tế:
- Khi tính bằng công thức Elmore $t_{pd} \approx 0,69 \cdot R_{on} \cdot C_L$ với tải $C_L = 50\,\text{fF}$:
  $t_{pHL} \approx 0,693 \times 969\,\Omega \times 50\,\text{fF} \approx \mathbf{33,6\,\text{ps}}$.
- Tuy nhiên, khi giải tích phân số quá trình xả điện áp từ $V_{DD} = 5,0\,\text{V}$ xuống $V_{DD}/2 = 2,5\,\text{V}$:
  1. Giai đoạn $5,0\,\text{V} \ge V_{out} \ge 4,3\,\text{V}$ ($V_{DS} \ge V_{GS} - V_{thn}$): NMOS nằm trong vùng **bão hòa**, dòng xả bị chặn ở mức bão hòa $I_{D,sat} \approx 2,22\,\text{mA}$. Điện trở tương đương tức thời tại đầu quá trình là $R_{inst} = 5,0\,\text{V} / 2,22\,\text{mA} \approx 2,25\,\text{k}\Omega$ (cao gấp 2,3 lần so với $R_{on}$).
  2. Giai đoạn $4,3\,\text{V} > V_{out} \ge 2,5\,\text{V}$: NMOS mới chuyển vào vùng **tuyến tính**, dòng xả giảm dần và điện trở kênh dẫn giảm dần về mức $R_{on}$.
- Khi tích phân chính xác dòng điện theo thời gian:

$$t_{pHL} = C_L \int_{2,5\,\text{V}}^{5,0\,\text{V}} \frac{dV_{out}}{I_{DS}(V_{out})} \approx \mathbf{50 - 59\,\text{ps}}$$

- Tỉ số giữa trễ thực tế và mô hình $0,69 R_{on} C_L$ là $\frac{59\,\text{ps}}{33,6\,\text{ps}} \approx \mathbf{1,76}$ lần.
- **Kết luận sư phạm:** Giảng viên cần giải thích rõ cho sinh viên: $R_{on}$ đo tại $V_{DS} \approx 0$ chỉ là điện trở nhỏ nhất của kênh dẫn (ở đáy quá trình). Điện trở hiệu dụng trung bình qua toàn bộ sườn chuyển mạch là $R_{eff} \approx 1,7 \cdot R_{on}$. Do đó, việc trễ mô phỏng SPICE lớn hơn trễ tính tay $0,69 R_{on} C_L$ khoảng 1,5–1,8 lần là phù hợp với bản chất vật lý.

### B4. Cơ chế vật lý hiện tượng Latch-up và vai trò của Guard Rings/Taps
Latch-up là hiện tượng kích hoạt ngoài ý muốn cấu trúc Thyristor bốn lớp $p-n-p-n$ ký sinh sẵn có trong mọi công nghệ CMOS khối (Bulk CMOS):
1. **Transistor BJT ký sinh $Q_1$ ($p-n-p$ thẳng đứng):** Cực phát Emitter là vùng P-Active (Source của PMOS), cực đáy Base là N-Well, cực thu Collector là P-Substrate.
2. **Transistor BJT ký sinh $Q_2$ ($n-p-n$ nằm ngang):** Cực phát Emitter là vùng N-Active (Source của NMOS), cực đáy Base là P-Substrate, cực thu Collector là N-Well.
3. Hai transistor này mắc hồi tiếp dương: Dòng Collector của $Q_1$ đổ vào Base của $Q_2$, và dòng Collector của $Q_2$ rút từ Base của $Q_1$.
4. **Cơ chế kích hoạt:** Điện trở ký sinh của giếng ($R_{well}$) và của chất nền ($R_{sub}$) đóng vai trò then chốt. Nếu điện áp nền bị dao động do nhiễu hoặc do dòng chuyển mạch đột biến, điện áp rơi trên $R_{well}$ hoặc $R_{sub}$ vượt quá $0,7\,\text{V}$, mối nối E-B của một BJT sẽ phân cực thuận và dẫn dòng. Vòng hồi tiếp dương lập tức khóa mạch vào trạng thái ngắn mạch công suất cao giữa $V_{DD}$ và $GND$, dòng điện vọt lên hàng trăm mA gây cháy chip do quá nhiệt.
5. **Biện pháp phòng ngừa trong Layout:**
   - Đặt tiếp xúc $N^+$-tap nối N-Well lên $V_{DD}$ càng gần PMOS càng tốt để ép điện trở $R_{well} \to 0$.
   - Đặt tiếp xúc $P^+$-tap nối P-Substrate xuống $GND$ càng gần NMOS càng tốt để ép điện trở $R_{sub} \to 0$.
   - Khi thiết kế mạch công suất hoặc ngõ ra đệm dòng lớn, bắt buộc phải dùng các dải bảo vệ liên tục (**Guard Rings**) bao bọc toàn bộ chu vi vùng Active.

### B5. Tụ ký sinh khuếch tán má/nguồn và trích xuất PEX
Khi vẽ Layout, mỗi transistor không chỉ có kênh dẫn mà còn có các khối khuếch tán silicon làm cực Source và Drain:
- Diện tích khuếch tán má: $AD = W \times L_{diff}$ (trong đó $L_{diff}$ là khoảng cách từ mép cổng đến mép tiếp xúc contact, thường bằng $5\lambda = 1,5\,\mu\text{m}$).
- Chu vi khuếch tán má: $PD = 2(W + L_{diff})$.
- Tại công nghệ MOSIS C5N:
  * Tụ đáy tiếp giáp: $CJ_n \approx 5,6 \times 10^{-4}\,\text{F/m}^2$, $CJ_p \approx 9,4 \times 10^{-4}\,\text{F/m}^2$.
  * Tụ thành bên tiếp giáp: $CJSW_n \approx 5,0 \times 10^{-10}\,\text{F/m}$, $CJSW_p \approx 2,9 \times 10^{-10}\,\text{F/m}$.
- Tổng tụ ký sinh tại nút ngõ ra $Out$:

$$C_{parasitic} = C_{db,n} + C_{db,p} + C_{wire,metal1} \approx 3,7\,\text{fF} + 8,0\,\text{fF} + 8,5 - 11,8\,\text{fF} \approx \mathbf{20 - 23,5\,\text{fF}}$$

- Khi kéo tải ngoài $C_L = 50\,\text{fF}$, tổng tải hiệu dụng tăng lên:

$$C_{L,eff} = 50\,\text{fF} + 23,5\,\text{fF} = \mathbf{73,5\,\text{fF}} \quad (+47\%)$$

- Do đó, trễ truyền lan sau trích xuất PEX tăng từ $\sim 50\,\text{ps}$ lên $\sim 75\,\text{ps}$ (tăng tương ứng xấp xỉ $47\%$).

### B6. Đường đi Euler (Euler Path) và Sơ đồ que (Stick Diagram) của Inverter
- **Thắc mắc sư phạm thường gặp:** *"Tại sao Đề cương chi tiết (Mục VII Rubric) yêu cầu đường đi Euler, trong khi Inverter chỉ có 1 cổng vào?"*
- **Giải thích của Giảng viên:** 
  1. Trong thiết kế layout CMOS tiêu chuẩn, nguyên tắc cơ bản là tìm đường đi Euler trên đồ thị mạch để xếp các transistor thành một dải khuếch tán liên tục (Diffusion Sharing / Abutment), tránh bị đứt đoạn dải Active gây lãng phí diện tích và tăng tụ ký sinh.
  2. Đối với CMOS Inverter, mạch chỉ gồm 1 transistor PMOS và 1 transistor NMOS điều khiển bởi 1 ngõ vào duy nhất (`In`). Đồ thị mạch chỉ có đúng 1 cạnh đơn lập. Do đó, đường đi Euler ở đây là trường hợp **cơ sở suy biến**:
  
$$\text{Euler Path: } [In]$$
  
  Dải Polysilicon chạy thẳng một đường duy nhất từ trên xuống dưới xuyên qua cả 2 dải khuếch tán.
  3. Đây là bước đệm sư phạm nền tảng bắt buộc để sinh viên làm quen với sơ đồ que (Stick Diagram), nhận biết các lớp vật liệu và tiếp xúc Taps chống Latch-up trước khi bước sang giải bài toán Euler đa biến phức tạp ở Lab 02 ($A - B$) và Lab 03 ($A - B - C$).

---

## C. KỊCH BẢN LÊN LỚP TỪNG PHẦN

### C0. Đầu buổi: Kiểm tra Pre-lab (15 phút)
- **Thao tác giảng viên:** Yêu cầu toàn bộ sinh viên mở sẵn vở hoặc bản in bài tập Pre-lab trên bàn. Đi từng bàn kiểm tra 4 nội dung then chốt:
  1. Bảng trích xuất tham số P1 từ `C5_models.txt`.
  2. Kết quả tính toán giải tích tỉ số kích thước và $V_M$ tại P2.
  3. Bản vẽ sơ đồ que Stick Diagram có đầy đủ các lớp và tiếp xúc Taps tại P4.
  4. Khung netlist điền khuyết tại P5.
- **Dấu hiệu sinh viên đạt:** Tính ra đúng $W_p/W_n = 3,0$ và $V_M = 2,45\,\text{V}$; vẽ sơ đồ que có phân tách rõ thanh nguồn Metal 1 và có dải Poly liên tục cắt qua 2 vùng Active; có vẽ tiếp xúc Well-tap và Substrate-tap.
- **Xử lý:** Ký xác nhận vào góc bài làm. Sinh viên thiếu P2 hoặc P4 bị yêu cầu ngồi tại bàn làm xong trong 15 phút, không được bật máy tính sớm.

### C1. Ex1.1: Khảo sát đặc tính I-V của NMOS và PMOS (25 phút)
- **Thao tác mẫu của GV:** Chiếu màn hình hướng dẫn tạo schematic `nmos_iv.asc`. Nhấn mạnh chân Bulk của NMOS phải nối đất `0`. Hướng dẫn nhập lệnh `.dc VDS 0 5 0.01 VGS 1 5 1`.
- **Lỗi sinh viên hay gặp:** Quên lệnh `.include C5_models.txt` dẫn tới báo lỗi không nhận dạng linh kiện `N`; hoặc nối nhầm chân Bulk của PMOS xuống đất thay vì lên nguồn $5\,\text{V}$.
- **Câu hỏi kiểm tra nhanh:** "Tại sao trong vùng bão hòa, đường cong $I_{DS}$ không nằm ngang phẳng mà lại dốc nhẹ đi lên?"  
  *Dấu hiệu hiểu bài:* Sinh viên trả lời được do hiện tượng điều chế chiều dài kênh dẫn ($\lambda$), khi $V_{DS}$ tăng làm vùng nghèo cực má nở rộng, chiều dài kênh hiệu dụng $L_{eff}$ bị co ngắn lại.

### C2. Ex1.2: Thiết kế Schematic CMOS Inverter và phân tích VTC (25 phút)
- **Thao tác mẫu của GV:** Hướng dẫn vẽ Schematic trong Electric VLSI, đặt tên port viết thường `in`, `out`, `vdd`, `gnd`. Hướng dẫn menu xuất file SPICE. Mở trong LTspice, chạy `.dc Vin 0 5 0.002`.
- **Lỗi sinh viên hay gặp:** Đặt độ phân giải quét $V_{in}$ quá thô (ví dụ bước $0,1\,\text{V}$), khi lấy đạo hàm `d(V(out))/d(V(in))` đồ thị bị gãy khúc, không xác định được điểm dốc $-1$.
- **Câu hỏi kiểm tra nhanh:** "Điểm $V_M$ đo được trên đồ thị của em là bao nhiêu? Tại sao nó không phải là $2,50\,\text{V}$?"  
  *Dấu hiệu hiểu bài:* Sinh viên chỉ ra được $V_M \approx 2,45\,\text{V}$ và giải thích do tỉ số $W_p/W_n = 3,0$ cân bằng dẫn nạp $r=1$, nhưng vì $|V_{thp}| = 0,8\,\text{V} > V_{thn} = 0,7\,\text{V}$ nên $V_M$ bị dịch nhẹ về phía NMOS.

### C3. Ex1.3: Đo trễ Transient bằng lệnh `.meas` (25 phút)
- **Thao tác mẫu của GV:** Hướng dẫn cú pháp nguồn xung `PULSE(0 5.0 0 100p 100p 9.9n 20n)`. Giải thích ý nghĩa từng thông số trong câu lệnh `.meas` đo thời gian giữa hai điểm băng qua mức $2,5\,\text{V}$ (ngưỡng 50%).
- **Lỗi sinh viên hay gặp:** Nhầm lẫn sườn kích hoạt: đo $t_{pHL}$ nhưng gán `TRIG` sườn `FALL` và `TARG` sườn `RISE` khiến lệnh `.meas` báo lỗi `FAIL` trong Error Log.
- **Câu hỏi kiểm tra nhanh:** "So sánh $t_{pd}$ đo được trong bảng với số $33,6\,\text{ps}$ em tính ở Pre-lab, số nào lớn hơn và tại sao?"  
  *Dấu hiệu hiểu bài:* Sinh viên khẳng định số đo SPICE lớn hơn ($\sim 50\,\text{ps}$ so với $\sim 34\,\text{ps}$) và giải thích vì transistor phải xả qua vùng bão hòa trước khi vào vùng tuyến tính.

### C4. Ex1.4: Mask Layout, chạy DRC và đối chiếu LVS (25 phút)
- **Thao tác mẫu của GV:** Mở Electric, chuyển sang view `layout`. Hướng dẫn vẽ thanh ray Metal 1, vùng N-Well, hai vùng Active và dải Poly chung. Nhấn mạnh việc đặt hai tiếp xúc Taps. Bấm phím `F5` chạy DRC. Mở công cụ NCC so sánh Schematic và Layout.
- **Lỗi sinh viên hay gặp:**
  1. Vi phạm khoảng cách vươn Poly qua Active (Gate Overhang $< 2\lambda$).
  2. Đặt tên Export chân hoa/thường không đồng nhất (Schematic là `in`, Layout là `IN`) khiến LVS báo lỗi `Netlists do NOT match`.
- **Câu hỏi kiểm tra nhanh:** "Nếu ta bỏ hai nốt tiếp xúc Taps đi thì LVS có báo lỗi không và chip thật sẽ ra sao?"  
  *Dấu hiệu hiểu bài:* Sinh viên nêu rõ LVS sẽ cảnh báo thiếu chân nguồn/đế hoặc giếng bị hở; trên chip thật sẽ bị cháy do Latch-up.

### C5. Ex1.5: Trích xuất ký sinh PEX và mô phỏng Post-layout (10 phút)
- **Thao tác mẫu của GV:** Hướng dẫn bật tính năng Extract Parasitics trong Electric, xuất file netlist PEX. Mở netlist cho sinh viên thấy các dòng code sinh thêm `AS=... AD=...` và các tụ liên kết.
- **Lỗi sinh viên hay gặp:** Quên gắn thêm nguồn kích thích và tụ tải ngoài $C_L = 50\,\text{fF}$ vào netlist PEX khiến mô phỏng không chạy được hoặc ra kết quả sai lệch.
- **Dấu hiệu hoàn thành:** Sinh viên ghi nhận được $t_{pd,post}$ tăng thêm khoảng 40–50% so với Pre-layout.

### C6. Tổng kết và nghiệm thu (10 phút)
Giảng viên đặt 1 câu hỏi ngẫu nhiên trong Phần E cho từng nhóm, kiểm tra bảng số liệu đã điền đủ, ký xác nhận vào phiếu báo cáo của sinh viên.

---

## D. CÂU HỎI SINH VIÊN THƯỜNG HỎI

1. **"Thưa thầy, tại sao bề rộng PMOS lại phải làm gấp 3 lần NMOS mà không làm bằng nhau để tiết kiệm diện tích?"**  
   *Giải thích:* Do trong tinh thể Silicon, độ linh động của điện tử dẫn ($\mu_n \approx 120\,\text{cm}^2/\text{V}\cdot\text{s}$) cao gấp 3 lần độ linh động của lỗ trống ($\mu_p \approx 40\,\text{cm}^2/\text{V}\cdot\text{s}$) vì hiện tượng tán xạ năng lượng khác nhau. Muốn dòng nạp của PMOS mạnh tương đương dòng xả của NMOS nhằm đạt tốc độ chuyển mạch cân bằng và lề nhiễu đối xứng, ta bắt buộc phải bù đắp độ linh động bằng cách tăng bề rộng kênh dẫn: $W_p \approx 3 \times W_n$. Nếu làm $W_p = W_n$, trễ sườn lên $t_{pLH}$ sẽ chậm gấp 3 lần trễ sườn xuống $t_{pHL}$.

2. **"Tại sao điểm chuyển mạch đo được trong mô phỏng là $2,45\,\text{V}$ chứ không phải đúng $2,50\,\text{V}$?"**  
   *Giải thích:* Vì trong công nghệ C5N, điện áp ngưỡng của hai linh kiện không đối xứng lý tưởng ($V_{thn} = 0,70\,\text{V}$ trong khi $|V_{thp}| = 0,80\,\text{V}$). Khi chọn tỉ số $W_p/W_n = 3,0$, hệ số dẫn nạp hai nhánh bằng nhau ($r = 1$), nhưng ngưỡng PMOS cao hơn khiến PMOS mở khó hơn một chút, làm điểm cân bằng dòng bị kéo nhẹ về phía $0\,\text{V}$. Để đạt chính xác $2,50\,\text{V}$, ta cần tỉ số $W_p/W_n \approx 3,36$ ($W_p = 13,45\lambda$). Tuy nhiên, chuẩn thiết kế công nghiệp ưu tiên số nguyên $\lambda$, nên $12\lambda$ ($3,0$) là lựa chọn tối ưu, chấp nhận độ lệch $2\%$ không đáng kể.

3. **"Tại sao em chạy lệnh `.meas` trong LTspice mà Error Log lại báo `FAIL`?"**  
   *Giải thích:* Lệnh `.meas` báo FAIL do một trong ba nguyên nhân:
   - Ngưỡng đo chưa đạt tới: Ví dụ nguồn xung chỉ đặt biên độ $2,0\,\text{V}$ nhưng câu lệnh lại tìm điểm giao $2,5\,\text{V}$.
   - Khai báo sai sườn chuyển mạch: Tín hiệu đang giảm nhưng lại đặt `TRIG ... RISE=1`.
   - Thời gian mô phỏng kết thúc trước khi có sự kiện chuyển mạch: Kiểm tra lại tham số thời gian trong nguồn PULSE và lệnh `.tran`.

4. **"Tại sao kết quả so sánh NCC (LVS) lại báo `Netlists do NOT match` dù em vẽ sơ đồ và layout rất giống nhau?"**  
   *Giải thích:* Electric phân biệt chính xác chữ hoa và chữ thường trong nhãn chân (Export Ports). Nếu trên Schematic đặt chân là `in` (chữ thường) nhưng trên Layout lại gõ `IN` (chữ hoa), chương trình sẽ coi đây là hai nút mạng khác nhau và báo lỗi không khớp nút. Hãy kiểm tra và đổi lại đồng nhất chữ thường.

---

## E. GỢI Ý CÂU HỎI VẤN ĐÁP TẠI BÀN

| STT | Câu hỏi vấn đáp | Ý chính bắt buộc phải có để đạt điểm tối đa |
| :---: | :--- | :--- |
| **1** | Tại sao thời gian trễ mô phỏng Post-layout lại tăng lên khoảng 40–50% so với Pre-layout? | Trình bày được: Quá trình PEX trích xuất thêm điện dung ký sinh khuếch tán cực má ($C_{db,n}, C_{db,p}$) do diện tích và chu vi vùng khuếch tán ($AD, PD$), cộng với điện dung ký sinh của dây kim loại Metal 1 nối ngõ ra. Tổng điện dung tải tăng từ $50\,\text{fF}$ lên $\approx 73,5\,\text{fF}$ làm trễ tăng tương ứng. |
| **2** | Nếu kỹ sư thiết kế Inverter với $W_p = W_n$, mạch có chạy được không và những chỉ số nào bị ảnh hưởng? | Mạch vẫn hoạt động như một cổng NOT logic. Tuy nhiên: Điểm $V_M$ bị kéo tụt xuống $\approx 1,7\,\text{V}$; lề nhiễu mức thấp $NM_L$ bị thu hẹp nghiêm trọng; trễ sườn lên $t_{pLH}$ chậm gấp 3 lần trễ sườn xuống $t_{pHL}$. Thiết kế này chỉ dùng khi cực kỳ tiết kiệm diện tích và tải ngõ ra chỉ cần xả nhanh. |
| **3** | Vai trò vật lý của tiếp xúc $N^+$-tap và $P^+$-tap trong Layout là gì? Điều gì xảy ra nếu quên đặt? | Trình bày được: Taps dùng để phân cực giếng N-Well lên $5\,\text{V}$ và đế P-Substrate xuống $0\,\text{V}$, triệt tiêu điện trở ký sinh $R_{well}, R_{sub}$. Nếu quên đặt, hiện tượng Latch-up sẽ kích hoạt cấu trúc Thyristor ký sinh $p-n-p-n$ gây ngắn mạch nguồn-đất làm cháy vi mạch thật. |
| **4** | Tại sao công thức trễ $t_{pd} \approx 0,69 \cdot R_{on} \cdot C_L$ lại cho kết quả nhỏ hơn trễ đo SPICE thực tế? | Giải thích được: $R_{on}$ được tính ở vùng triode sâu ($V_{DS} \approx 0$). Trong khi thực tế chuyển mạch từ $5\,\text{V}$ về $2,5\,\text{V}$, transistor bắt đầu từ vùng bão hòa có dòng bị nghẽn và điện trở tức thời lớn gấp hơn 2 lần. Tích phân toàn quá trình cho trễ lớn hơn khoảng 1,5–1,8 lần. |

---

## F. ĐÁP ÁN VÀ SỐ LIỆU THAM CHIẾU

### F1. Đáp án Pre-lab

#### P1. Trích xuất tham số từ `C5_models.txt` [Đo từ PDK]
- **NMOS (Model N):**
  * `VTO` = $0,7000\,\text{V}$
  * `KP` = $120,0\,\mu\text{A/V}^2$
  * `TOX` = $9,5 \times 10^{-9}\,\text{m}$ ($95\,\text{Å}$)
  * `XJ` = $0,20\,\mu\text{m}$ ($2,0 \times 10^{-7}\,\text{m}$)
  * `GAMMA` = $0,50\,\text{V}^{1/2}$
  * `LAMBDA` = $0,050\,\text{V}^{-1}$
- **PMOS (Model P):**
  * `VTO` = $-0,8000\,\text{V}$
  * `KP` = $40,0\,\mu\text{A/V}^2$
  * `TOX` = $9,5 \times 10^{-9}\,\text{m}$
  * `XJ` = $0,20\,\mu\text{m}$
  * `GAMMA` = $0,50\,\text{V}^{1/2}$
  * `LAMBDA` = $0,050\,\text{V}^{-1}$

#### P2. Tính toán giải tích tỉ số $(W_p/W_n)$ và điểm $V_M$ [Suy dẫn]
1. Tỉ số để $V_M = 2,50\,\text{V}$:

$$\sqrt{r} = \frac{V_M - V_{thn}}{V_{DD} - V_M - |V_{thp}|} = \frac{2,50 - 0,70}{5,0 - 2,50 - 0,80} = \frac{1,80}{1,70} \approx 1,0588$$

$$r = 1,0588^2 \approx 1,1211 \implies \left[\frac{(W/L)_p}{(W/L)_n}\right]_{\text{target}} = 1,1211 \times \frac{K_n'}{K_p'} = 1,1211 \times 3,00 = \mathbf{3,363}$$

2. Khi chọn $W_n = 4\lambda = 1,2\,\mu\text{m}$ và $W_p = 12\lambda = 3,6\,\mu\text{m}$ ($W_p/W_n = 3,0$):

$$r = \frac{40 \times (3,6/0,6)}{120 \times (1,2/0,6)} = \frac{240}{240} = \mathbf{1,0000}$$

$$V_M = \frac{0,70 + 1,0 \times (5,0 - 0,80)}{1 + 1,0} = \frac{4,90}{2} = \mathbf{2,450\,\text{V}}$$

   Độ lệch so với $2,50\,\text{V}$ là: $|2,45 - 2,50| = \mathbf{0,05\,\text{V}}$ ($2,0\%$).

#### P3. Ước lượng điện trở dẫn $R_{on}$ và trễ $0,69 R C$ [Suy dẫn]
- $R_{on,n} = \frac{1}{(240 \times 10^{-6}) \times (5,0 - 0,70)} = \mathbf{969\,\Omega}$.
- $R_{on,p} = \frac{1}{(240 \times 10^{-6}) \times (5,0 - 0,80)} = \mathbf{992\,\Omega}$.
- Với $C_L = 50\,\text{fF}$:
  * $t_{pHL} \approx 0,693 \times 969\,\Omega \times 50\,\text{fF} = \mathbf{33,58\,\text{ps}}$.
  * $t_{pLH} \approx 0,693 \times 992\,\Omega \times 50\,\text{fF} = \mathbf{34,37\,\text{ps}}$.
  * $t_{pd} \approx \frac{33,58 + 34,37}{2} = \mathbf{33,98\,\text{ps}} \approx 34\,\text{ps}$.
- **Dự đoán:** Trễ đo thực tế trong LTspice sẽ *lớn hơn* giá trị này (khoảng 1,5 đến 1,8 lần) vì quá trình nạp xả đi qua vùng bão hòa trước khi tới vùng tuyến tính.

#### P4. Thiết kế sơ đồ que (Stick Diagram) [Kiểm tra]
- **Đường đi Euler:** $\text{Euler Path: } [In]$ (đường đơn biến).
- **Tiêu chí chấm sơ đồ que:**
  1. Vẽ đúng 2 thanh nguồn $V_{DD}$ (trên) và $GND$ (dưới) bằng Metal 1.
  2. Dải Polysilicon liên tục chạy dọc từ PMOS xuống NMOS làm ngõ vào `in`.
  3. Dây ngõ ra `out` bằng Metal 1 nối chung 2 cực Drain của PMOS và NMOS.
  4. Có đầy đủ các dấu tiếp xúc Contact (`X`) từ Metal 1 vào Active và Poly.
  5. **Bắt buộc:** Có vẽ tiếp xúc $N^+$-tap nối N-Well lên $V_{DD}$ và $P^+$-tap nối P-Substrate xuống $GND$ để phòng ngừa Latch-up.

```text
       VDD Power Rail (Metal 1)
   ═════════════════════════════════════
      │ [Tap]                 │ [Contact]
   ┌──┴───────┐           ┌───┴───┐
   │  N-Well  │           │   S   │ P-Active (Wp = 12λ)
   └──────────┘           ├───┬───┤
                    In ───┤ G │   │ (Poly)
                          ├───┴───┤
                          │   D   │
                          └───┬───┘
                              │ [Contact]
                              ├────────────── Out (Metal 1)
                              │ [Contact]
   ┌──────────┐           ┌───┴───┐
   │  P-Sub   │           │   D   │ N-Active (Wn = 4λ)
   └──┬───────┘           ├───┬───┤
      │ [Tap]       In ───┤ G │   │ (Poly)
   ═══════════════════════├───┴───┤═════
      GND Power Rail      │   S   │
      (Metal 1)           └───┬───┘
                              │ [Contact]
   ═════════════════════════════════════
```

#### P5. Khung Netlist hoàn chỉnh
```spice
* Netlist CMOS Inverter - MOSIS C5N 0.5um
.include C5_models.txt

* Nguon cap va kich thich
Vdd vdd 0 DC 5.0
Vin in  0 PULSE(0 5.0 0 100p 100p 9.9n 20n)

* Transistor PMOS va NMOS
MP out in vdd vdd P L=0.6U W=3.6U
MN out in 0   0   N L=0.6U W=1.2U

* Tai dung ngo ra
CL out 0 50fF

* Phan tich qua do va cau lenh do tre
.tran 1p 50n
.meas TRAN tpHL TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 FALL=1
.meas TRAN tpLH TRIG V(in)=2.5 FALL=1 TARG V(out)=2.5 RISE=1
.meas TRAN tpd  PARAM (tpHL + tpLH)/2
.end
```

---

### F2. Bảng giá trị kỳ vọng (Benchmark Reference Table)

> Ghi chú nguồn gốc:
> - **[Suy dẫn]:** Tính toán từ công thức giải tích chuẩn.
> - **[Script bậc hai]:** Tính bằng tích phân số mô hình quá độ trong `verify_lab01_new.py`.
> - **[Benchmark SPICE]:** Giá trị chuẩn mô phỏng trong LTspice với Level 3.
> - **[Đo]:** Dành cho giảng viên ghi lại số đo thực tế trên máy tính phòng lab.

| Thông số kỹ thuật | [Suy dẫn] Giải tích | [Script bậc 2] Tích phân | [Benchmark SPICE] Pre-layout | [Benchmark SPICE] Post-layout (PEX) | [Đo] Thực tế phòng lab |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$V_{thn}$** | $0,70\,\text{V}$ | $0,70\,\text{V}$ | $0,69 - 0,71\,\text{V}$ | $0,69 - 0,71\,\text{V}$ | |
| **$V_{thp}$** | $-0,80\,\text{V}$ | $-0,80\,\text{V}$ | $-0,79 - -0,81\,\text{V}$ | $-0,79 - -0,81\,\text{V}$ | |
| **$\lambda_n$** | $0,050\,\text{V}^{-1}$ | $0,050\,\text{V}^{-1}$ | $0,048 - 0,052\,\text{V}^{-1}$ | $0,048 - 0,052\,\text{V}^{-1}$ | |
| **$I_{DS,max(n)}$ ($5\,\text{V}, 5\,\text{V}$)** | $2,22\,\text{mA}$ ($\lambda=0$) | $2,77\,\text{mA}$ ($\lambda=0,05$) | $2,70 - 2,85\,\text{mA}$ | $2,70 - 2,85\,\text{mA}$ | |
| **$I_{DS,max(p)}$ ($5\,\text{V}, 5\,\text{V}$)** | $2,12\,\text{mA}$ ($\lambda=0$) | $2,65\,\text{mA}$ ($\lambda=0,05$) | $2,58 - 2,72\,\text{mA}$ | $2,58 - 2,72\,\text{mA}$ | |
| **Điện áp $V_M$** | $2,450\,\text{V}$ | $2,450\,\text{V}$ | $2,448 - 2,452\,\text{V}$ | $2,445 - 2,450\,\text{V}$ | |
| **$V_{IL}$ (slope = $-1$)** | $1,82\,\text{V}$ | $1,655\,\text{V}$ | $1,65 - 1,82\,\text{V}$ | $1,65 - 1,81\,\text{V}$ | |
| **$V_{IH}$ (slope = $-1$)** | $2,78\,\text{V}$ | $2,825\,\text{V}$ | $2,78 - 2,85\,\text{V}$ | $2,78 - 2,85\,\text{V}$ | |
| **Lề nhiễu $NM_L$** | $1,82\,\text{V}$ | $1,655\,\text{V}$ | $\ge 1,65\,\text{V}$ | $\ge 1,65\,\text{V}$ | |
| **Lề nhiễu $NM_H$** | $2,22\,\text{V}$ | $2,175\,\text{V}$ | $\ge 2,15\,\text{V}$ | $\ge 2,15\,\text{V}$ | |
| **$t_{pHL}$ ($C_L = 50\,\text{fF}$)** | $33,58\,\text{ps}$ ($0,69RC$) | $49,80\,\text{ps}$ | $48 - 55\,\text{ps}$ | $70 - 78\,\text{ps}$ | |
| **$t_{pLH}$ ($C_L = 50\,\text{fF}$)** | $34,37\,\text{ps}$ ($0,69RC$) | $51,91\,\text{ps}$ | $50 - 58\,\text{ps}$ | $73 - 82\,\text{ps}$ | |
| **$t_{pd}$ ($C_L = 50\,\text{fF}$)** | $33,98\,\text{ps}$ ($0,69RC$) | $50,86\,\text{ps}$ | $49 - 56\,\text{ps}$ | $72 - 80\,\text{ps}$ | |
| **Độ tăng trễ PEX vs Pre** | — | $+47,0\%$ | — | $\mathbf{+42 - 48\%}$ | |

---

### F3. Đáp án Post-lab

1. **Thiết kế không đối xứng $W_p = W_n = 4\lambda = 1,2\,\mu\text{m}$:**
   - Hệ số dẫn nạp $r = \frac{40 \times (1,2/0,6)}{120 \times (1,2/0,6)} = \frac{1}{3} \approx 0,3333 \implies \sqrt{r} \approx 0,5774$.
   - Điểm chuyển mạch:

$$V_M = \frac{0,70 + 0,5774 \times (5,0 - 0,80)}{1 + 0,5774} = \frac{0,70 + 2,425}{1,5774} \approx \mathbf{1,98\,\text{V}}$$

     Đường cong VTC bị dịch mạnh sang bên trái (về phía 0 V). Lề nhiễu mức thấp $NM_L$ bị sụt giảm nghiêm trọng từ $\sim 1,7\,\text{V}$ xuống chỉ còn $\sim 1,1\,\text{V}$, làm mạch cực kỳ nhạy cảm với nhiễu đất.
   - Trễ sườn lên $t_{pLH}$ bị kéo dài gấp 3 lần ($R_{on,p} \approx 3 \times 992 \approx 3\,\text{k}\Omega \implies t_{pLH} \approx 150\,\text{ps}$), trong khi $t_{pHL}$ giữ nguyên $\approx 50\,\text{ps}$.
   - Thiết kế này chỉ được chấp nhận trong các mạch có tính bất đối xứng tự nhiên (ví dụ mạch giải mã địa chỉ mảng nhớ chỉ xả tức thời, hoặc tế bào nhớ SRAM nơi kích thước nhỏ là ưu tiên hàng đầu).

2. **Cơ chế vật lý tụ ký sinh khuếch tán và ảnh hưởng của tải dung lớn:**
   - Vùng khuếch tán má tạo nên tiếp giáp $p-n$ với chất nền hoặc giếng. Tiếp giáp này luôn bị phân cực ngược, hình thành một lớp điện tích không gian (vùng nghèo) hoạt động như một tụ điện phẳng với điện môi là silicon.
   - Diện tích đáy $AD$ tạo tụ tiếp giáp phẳng $C_{bottom} = CJ \cdot AD$; chu vi $PD$ tạo tụ thành bên $C_{sidewall} = CJSW \cdot PD$.
   - Khi tải ngoài rất lớn (ví dụ $C_L = 1\,\text{pF} = 1000\,\text{fF}$): Tụ ký sinh nội tại $C_{par} \approx 23,5\,\text{fF}$ chỉ chiếm $\frac{23,5}{1000 + 23,5} \approx 2,3\%$ tổng tải. Lúc này tải ngoài chiếm ưu thế áp đảo, nên sự suy giảm tốc độ giữa Pre-layout và Post-layout trở nên không đáng kể.

3. **Cơ chế chống Latch-up của Guard Rings:**
   - Việc chỉ cắm một vài nốt tiếp xúc Tap rời rạc chỉ dập được điện thế tại cục bộ các điểm đó. Dòng hạt dẫn thiểu số phát xạ từ các tiếp giáp bị phân cực thuận vẫn có thể khuếch tán ngang trong lớp nền và kích hoạt BJT ký sinh ở xa.
   - Dải bảo vệ liên tục (Guard Ring) là một vòng tiếp xúc khép kín bao bọc toàn diện vùng transistor. Vòng này tạo một bức tường chắn điện thế thấp, hấp thụ toàn bộ các hạt dẫn thiểu số trôi dạt và san phẳng điện trở đường dẫn $R_{well}$ và $R_{sub}$ dọc theo toàn bộ chu vi, triệt tiêu khả năng hình thành chênh lệch điện thế $0,7\,\text{V}$ trên tiếp giáp E-B ký sinh.

---

### F4. Barem chấm điểm chi tiết (Thang điểm 10)

| STT | Hạng mục đánh giá | Điểm tối đa | Tiêu chí chấm chi tiết |
| :---: | :--- | :---: | :--- |
| **1** | **Chuẩn bị Pre-lab (Mục 4)** | **2,0 điểm** | - Trích xuất đúng bảng tham số P1: 0,5 đ.<br>- Tính đúng giải tích $W_p/W_n$ và $V_M = 2,45\,\text{V}$ tại P2: 0,5 đ.<br>- Tính đúng $R_{on}$, trễ $0,69 R C$ và có dự đoán đúng tại P3: 0,5 đ.<br>- Vẽ Stick diagram P4 có đủ các lớp và Taps, netlist P5 đúng: 0,5 đ. |
| **2** | **Đo đạc I-V & Phân tích VTC (Ex1.1, Ex1.2)** | **2,5 điểm** | - Chạy đúng họ đặc tuyến $I_{DS}-V_{DS}$ và truyền dẫn $I_{DS}-V_{GS}$: 1,0 đ.<br>- Trích xuất đúng thực nghiệm $V_{th}$ và $\lambda$: 0,5 đ.<br>- Dựng Schematic Inverter và chạy mô phỏng VTC ra dạng sóng chuẩn: 0,5 đ.<br>- Đo chính xác điểm $V_M \approx 2,45\,\text{V}$ và vẽ đạo hàm xác định $NM_L, NM_H$: 0,5 đ. |
| **3** | **Mô phỏng Transient & Lệnh `.meas` (Ex1.3)** | **2,0 điểm** | - Cấu hình nguồn PULSE và tải $50\,\text{fF}$ chính xác: 0,5 đ.<br>- Soạn đúng khối lệnh `.meas` và trích xuất kết quả không báo lỗi FAIL: 1,0 đ.<br>- Lập bảng số liệu theo 3 mức tải dung và tạo Icon View chuẩn IEEE: 0,5 đ. |
| **4** | **Mask Layout, DRC & LVS (Ex1.4)** | **2,5 điểm** | - Vẽ Layout đúng kích thước lưới $\lambda = 0,30\,\mu\text{m}$, gọn gàng: 1,0 đ.<br>- Có đầy đủ tiếp xúc Well Tap và Substrate Tap: 0,5 đ.<br>- Kiểm tra DRC đạt **"0 errors found"**: 0,5 đ.<br>- Đối chiếu NCC (LVS) báo **"Cells are topologically equivalent (MATCH)"**: 0,5 đ. |
| **5** | **Trích xuất PEX & Post-lab (Ex1.5, Mục 7)** | **1,0 điểm** | - Trích xuất netlist PEX và chạy mô phỏng đo độ tăng trễ: 0,5 đ.<br>- Trả lời đúng, lập luận chặt chẽ 3 câu hỏi Post-lab: 0,5 đ. |
| **TỔNG**| **TOÀN BÀI LAB 1** | **10,0 điểm** | **Đạt yêu cầu khi tổng điểm $\ge 5,0$ và LVS đạt MATCH.** |
