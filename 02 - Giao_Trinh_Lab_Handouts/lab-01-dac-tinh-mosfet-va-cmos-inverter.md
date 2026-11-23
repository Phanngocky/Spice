# THỰC HÀNH THIẾT KẾ VLSI — BÀI 1
# ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER

---
**Học phần:** Thực hành Thiết kế VLSI (Mã học phần: `5505382`)  
**Bộ môn:** Điện tử - Viễn thông | **Khoa:** Điện - Điện tử | **Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Liên hệ giáo trình:** Chương 2 (Đặc tính linh kiện MOSFET), Chương 3 (Mô hình trễ RC và cổng Inverter)  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07 trở lên), LTspice (XVII hoặc LTspice 2025)  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5 µm ($\lambda = 0,30\,\mu\text{m}$, 3 lớp kim loại, $V_{DD} = 5,0\,\text{V}$)  
**Thời lượng:** Pre-lab khoảng 1,5 giờ ở nhà; In-lab 1 buổi (3 tiết = 135 phút tại phòng máy); Post-lab khoảng 1 giờ  
---

## 1. MỤC TIÊU (ĐO ĐƯỢC)

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Trích xuất thực nghiệm tham số I-V:** Sử dụng LTspice quét DC hai biến để vẽ họ đặc tuyến $I_{DS}-V_{DS}$ và $I_{DS}-V_{GS}$ của NMOS và PMOS; xác định điện áp ngưỡng thực nghiệm ($V_{thn}, V_{thp}$) và hệ số điều chế chiều dài kênh ($\lambda$) với sai lệch dưới 5% so với mô hình Level 3.
2. **Thiết kế & Tối ưu hóa CMOS Inverter:** Dựng sơ đồ nguyên lý (Schematic) trên Electric VLSI với kích thước kênh cân bằng $\beta$ ($W_p/W_n = 3/1$); phân tích đường cong truyền đạt điện áp (VTC), xác định điện áp chuyển mạch $V_M \approx 2,45\,\text{V}$ và các mức lề nhiễu logic $NM_L, NM_H \ge 1,5\,\text{V}$.
3. **Đo đạc động học trễ bằng câu lệnh SPICE:** Cấu hình nguồn xung và chèn các câu lệnh `.meas` để trích xuất tự động trễ sườn xuống $t_{pHL}$, trễ sườn lên $t_{pLH}$, trễ truyền lan trung bình $t_{pd}$, thời gian tăng $t_r$ và giảm $t_f$ ở ba mức tải dung $C_L = 10\,\text{fF}, 50\,\text{fF}, 100\,\text{fF}$; đối chiếu với mô hình $0,69 \cdot R_{on} \cdot C_L$ và lý giải nguyên nhân sai lệch.
4. **Thiết kế Layout và kiểm chứng vật lý:** Thiết kế mặt nạ vật lý (Mask Layout) cho Inverter tuân thủ quy tắc thiết kế MOSIS SCMOS ($\lambda = 0,30\,\mu\text{m}$); thực hiện kiểm tra luật hình học DRC đạt 0 lỗi và đối chiếu sơ đồ nguyên lý LVS (NCC) đạt trạng thái trùng khớp topo (MATCH).
5. **Trích xuất ký sinh (PEX) và đánh giá hậu thiết kế:** Trích xuất tụ ký sinh khuếch tán ($C_{db}, C_{sb}$) và tụ liên kết kim loại; chạy mô phỏng Post-layout để định lượng mức suy giảm tốc độ truyền lan so với Pre-layout; đóng gói tế bào chuẩn `INV_X1` kèm biểu tượng (Icon View) sẵn sàng tái sử dụng cho các bài lab sau.

---

## 2. KẾ THỪA VÀ SẢN PHẨM

| Thành phần | Chi tiết chuyển giao |
| :--- | :--- |
| **Dùng lại từ lab trước** | - Thư mục dự án `lab_vlsi/` và tệp thư viện mô hình `C5_models.txt` từ Lab 0.<br>- Kỹ năng viết netlist SPICE, cấu hình phân tích `.dc`, `.tran` và khối câu lệnh `.meas` đo thời gian trễ tự động.<br>- Mô hình trễ $RC$ cơ bản $t_{50} = \ln(2) \cdot R \cdot C \approx 0,69 \cdot R \cdot C$ đã được kiểm chứng bằng thực nghiệm quét tham số ở Lab 0. |
| **Sinh ra cho lab sau** | - Tế bào chuẩn `INV_X1` hoàn chỉnh (Schematic, Layout, Icon View) trong Electric VLSI làm tế bào gốc cho Lab 2 (NAND/NOR), Lab 3 (AOI/OAI), Lab 5 (Latch/Flip-flop) và Lab 10 (ALU 4-bit).<br>- Giá trị chuẩn thực nghiệm của $R_{on,n}, R_{on,p}, t_{pd0}$ và điện dung ngõ vào $C_{in}$ làm đơn vị chuẩn hóa (Inverter chuẩn) cho phương pháp nỗ lực logic (Logical Effort) tại Lab 3. |

---

## 3. CƠ SỞ NGẮN GỌN

### 3.1. Mô hình dòng điện của MOSFET
Trong tiến trình CMOS n-well trên đế p, dòng điện má-nguồn $I_{DS}$ của transistor NMOS được mô hình hóa theo ba vùng hoạt động chính:

1. **Vùng ngưng dẫn (Cut-off):** Khi $V_{GS} < V_{thn}$

   $$I_{DS} \approx 0$$

   (Trong mô hình Level 3 thực tế tồn tại dòng rò dưới ngưỡng $I_{sub}$ phụ thuộc hàm mũ vào $V_{GS}$).

2. **Vùng tuyến tính (Linear / Triode):** Khi $V_{GS} \ge V_{thn}$ và $V_{DS} < V_{GS} - V_{thn}$

   $$I_{DS} = K_n' \left(\frac{W}{L}\right)_n \left[ (V_{GS} - V_{thn}) V_{DS} - \frac{V_{DS}^2}{2} \right] (1 + \lambda V_{DS})$$

3. **Vùng bão hòa (Saturation):** Khi $V_{GS} \ge V_{thn}$ và $V_{DS} \ge V_{GS} - V_{thn}$

   $$I_{DS} = \frac{K_n'}{2} \left(\frac{W}{L}\right)_n (V_{GS} - V_{thn})^2 (1 + \lambda V_{DS})$$

Trong đó:
- $K_n' = \mu_n C_{ox}$ là hệ số dẫn suất truyền dẫn của NMOS (tại công nghệ C5N: $K_n' \approx 120\,\mu\text{A/V}^2$).
- $V_{thn}$ là điện áp ngưỡng không phân cực đế ($V_{thn} \approx 0,70\,\text{V}$).
- $\lambda$ là hệ số điều chế chiều dài kênh dẫn (đặc trưng cho độ dốc của dòng $I_{DS}$ theo $V_{DS}$ trong vùng bão hòa).
- Đối với PMOS, các phương trình có dạng tương tự nhưng đảo dấu cực tính ($V_{GS}, V_{DS}, V_{thp}$ mang dấu âm) và thay $K_n'$ bằng $K_p' = \mu_p C_{ox}$ (tại công nghệ C5N: $K_p' \approx 40\,\mu\text{A/V}^2$). Do độ linh động electron cao gấp khoảng 3 lần lỗ trống ($\mu_n \approx 3 \mu_p$), nên $K_n' \approx 3 K_p'$.

### 3.2. Đường cong truyền đạt VTC và điện áp chuyển mạch $V_M$
Sơ đồ nguyên lý CMOS Inverter gồm một transistor PMOS kéo lên nguồn $V_{DD}$ và một transistor NMOS kéo xuống đất $GND$.

```text
             VDD (5,0 V)
                 │
             ┌───┴───┐
             │  PMOS │ (Wp, Lp)
      In ────┤       ├─────┬───── Out
             └───┬───┘     │
                 │         │
             ┌───┴───┐     │
             │  NMOS │     │
      In ────┤       ├─────┘   (Wn, Ln)
             └───┬───┘
                 │
             GND (0 V)
```

Đường cong truyền đạt điện áp $V_{out} = f(V_{in})$ chia thành 5 vùng:
- **Vùng A:** $0 \le V_{in} < V_{thn} \implies$ NMOS tắt, PMOS tuyến tính $\implies V_{out} = V_{OH} = V_{DD}$.
- **Vùng B:** $V_{thn} \le V_{in} < V_M \implies$ NMOS bão hòa, PMOS tuyến tính $\implies V_{out}$ giảm dần.
- **Vùng C:** $V_{in} = V_M \approx V_{DD}/2 \implies$ Cả hai transistor đều ở vùng bão hòa $\implies$ Độ lợi khuếch đại cực đại.
- **Vùng D:** $V_M < V_{in} \le V_{DD} - |V_{thp}| \implies$ NMOS tuyến tính, PMOS bão hòa $\implies V_{out}$ giảm về gần 0 V.
- **Vùng E:** $V_{in} > V_{DD} - |V_{thp}| \implies$ NMOS tuyến tính, PMOS tắt $\implies V_{out} = V_{OL} = 0\,\text{V}$.

Tại điểm chuyển mạch $V_{in} = V_{out} = V_M$, cân bằng dòng bão hòa $I_{D,n} = |I_{D,p}|$:

$$\frac{1}{2} k_n (V_M - V_{thn})^2 = \frac{1}{2} k_p (V_{DD} - V_M - |V_{thp}|)^2$$

Đặt $r = \frac{k_p}{k_n} = \frac{K_p'(W/L)_p}{K_n'(W/L)_n}$, ta thu được công thức tổng quát:

$$V_M = \frac{V_{thn} + \sqrt{r}(V_{DD} - |V_{thp}|)}{1 + \sqrt{r}}$$

> [!NOTE]
> **Ví dụ minh họa tính $V_M$ trên tiến trình giả định (không trùng thông số C5N):**
> Xét một tiến trình CMOS có $V_{DD} = 3,3\,\text{V}$, $V_{thn} = 0,50\,\text{V}$, $|V_{thp}| = 0,60\,\text{V}$, và $K_n'/K_p' = 2,5$.
> - Nếu chọn thiết kế cân bằng dẫn nạp $r = 1 \implies (W/L)_p / (W/L)_n = 2,5$:
>   $V_M = \frac{0,50 + 1,0 \times (3,3 - 0,60)}{1 + 1,0} = \frac{0,50 + 2,70}{2} = 1,60\,\text{V}$ (lệch $0,05\,\text{V}$ so với mốc đối xứng $V_{DD}/2 = 1,65\,\text{V}$).
> - Muốn đạt chính xác $V_M = 1,65\,\text{V}$:
>   $\sqrt{r} = \frac{1,65 - 0,50}{3,3 - 1,65 - 0,60} = \frac{1,15}{1,05} \approx 1,095 \implies r = 1,20 \implies \frac{(W/L)_p}{(W/L)_n} = 1,20 \times 2,5 = 3,00$.

> [!TIP]
> **Mẹo IC (Tỉ số lưới $\lambda$):** Trong công nghệ MOSIS C5N ($V_{DD} = 5,0\,\text{V}$, $V_{thn} = 0,70\,\text{V}$, $|V_{thp}| = 0,80\,\text{V}$), tỉ số cân bằng $r = 1$ cho điểm chuyển mạch $V_M = 2,45\,\text{V}$. Muốn đạt mốc $2,50\,\text{V}$ cần tỉ số khoảng $3,36$. Tuy nhiên, để tuân thủ bước lưới số nguyên $\lambda$, ta chọn chuẩn công nghiệp $W_p = 12\lambda = 3,6\,\mu\text{m}$ và $W_n = 4\lambda = 1,2\,\mu\text{m}$ (tỉ số $3/1$), chấp nhận độ lệch $V_M$ chỉ $2\%$ để đổi lại diện tích và tính mô-đun hóa tối ưu.

### 3.3. Điện trở kênh dẫn hiệu dụng $R_{on}$ và mô hình trễ $RC$
Khi ngõ ra chuyển mức, transistor nạp hoặc xả tụ tải $C_L$.
- Tại vùng triode sâu ($V_{DS} \to 0$ khi cổng mở sâu):

  $$R_{on,n} = \frac{1}{K_n' \left(\frac{W}{L}\right)_n (V_{DD} - V_{thn})}, \quad R_{on,p} = \frac{1}{K_p' \left(\frac{W}{L}\right)_p (V_{DD} - |V_{thp}|)}$$

- Ước lượng trễ bậc một Elmore:

  $$t_{pHL} \approx 0,69 \cdot R_{on,n} \cdot C_L, \quad t_{pLH} \approx 0,69 \cdot R_{on,p} \cdot C_L, \quad t_{pd} = \frac{t_{pHL} + t_{pLH}}{2}$$

> [!CAUTION]
> **Giới hạn của mô hình $0,69 \cdot R_{on} \cdot C_L$:** Trong thực tế chuyển mạch từ $V_{DD}$ xuống $V_{DD}/2$, transistor bắt đầu từ vùng bão hòa (dòng dẫn bị giới hạn bởi điện áp pinch-off, điện trở tức thời $V_{DS}/I_{DS}$ cao hơn nhiều so với vùng triode) rồi mới chuyển dần sang vùng tuyến tính. Do đó, thời gian trễ đo thực tế từ mô phỏng SPICE thường cao hơn giá trị ước lượng $0,69 \cdot R_{on} \cdot C_L$ khoảng 1,5 đến 1,8 lần. Đây là đặc tính vật lý tự nhiên của quá trình phóng nạp qua vùng bão hòa; sinh viên cần ghi nhận và phân tích sự khác biệt này.

### 3.4. Quy tắc hình học MOSIS SCMOS và Latch-up
- Đơn vị chia lưới: $\lambda = 0,30\,\mu\text{m}$. Chiều dài kênh tối thiểu: $L_{min} = 2\lambda = 0,60\,\mu\text{m}$.
- Độ rộng tối thiểu: Poly $= 2\lambda$ ($0,60\,\mu\text{m}$), Active $= 3\lambda$ ($0,90\,\mu\text{m}$), Metal 1 $= 3\lambda$ ($0,90\,\mu\text{m}$).
- Poly vươn qua mép Active (Gate Overhang) $\ge 2\lambda$ ($0,60\,\mu\text{m}$).
- Kích thước lỗ tiếp xúc (Contact) cố định $2\lambda \times 2\lambda$ ($0,6\,\mu\text{m} \times 0,6\,\mu\text{m}$), lớp bao bọc (Enclosure) $\ge 1\lambda$.
- **Phân cực đế và giếng (Taps):** Bắt buộc phải có $N^+$-tap nối N-Well lên $V_{DD}$ và $P^+$-tap nối P-Substrate xuống $GND$. Nếu thiếu các tiếp xúc này, điện thế nền bị thả nổi làm phân cực thuận các tiếp giáp p-n ký sinh, kích hoạt cặp transistor lưỡng cực ký sinh ($pnp-npn$) tạo thành hiện tượng ngắn mạch **Latch-up** làm cháy vi mạch thật.

---

## 4. PRE-LAB (LÀM Ở NHÀ, NỘP TRƯỚC GIỜ LAB)

Sinh viên hoàn thành các câu hỏi sau vào vở bài tập hoặc mẫu báo cáo trước khi đến lớp.

### P1. Trích xuất tham số công nghệ
Mở tệp `C5_models.txt` trong thư mục dự án `lab_vlsi/` (hoặc thư viện đã cấp ở Lab 0). Tìm khối `.MODEL N NMOS` và `.MODEL P PMOS` (mô hình Level 3), trích xuất và điền các tham số vào bảng sau:

| Tham số SPICE | Ý nghĩa vật lý | Đơn vị | Giá trị NMOS (Model N) | Giá trị PMOS (Model P) |
| :--- | :--- | :---: | :---: | :---: |
| `VTO` | Điện áp ngưỡng không phân cực đế ($V_{GS0}$) | V | .................... | .................... |
| `KP` | Hệ số dẫn suất truyền dẫn ($K' = \mu C_{ox}$) | $\mu\text{A/V}^2$ | .................... | .................... |
| `TOX` | Độ dày lớp oxit cổng ($t_{ox}$) | m | .................... | .................... |
| `XJ` | Độ sâu tiếp giáp khuếch tán má/nguồn | m | .................... | .................... |
| `GAMMA` | Hệ số hiệu ứng thân ($\gamma$) | $\text{V}^{1/2}$ | .................... | .................... |
| `LAMBDA` | Hệ số điều chế chiều dài kênh ($\lambda$) | $\text{V}^{-1}$ | .................... | .................... |

### P2. Tính toán giải tích tỉ số $(W_p/W_n)$ và điểm chuyển mạch $V_M$
Cho các tham số công nghệ C5N: $V_{DD} = 5,0\,\text{V}$, $V_{thn} = 0,70\,\text{V}$, $|V_{thp}| = 0,80\,\text{V}$, $K_n' = 120\,\mu\text{A/V}^2$, $K_p' = 40\,\mu\text{A/V}^2$.
1. Tính tỉ số định kích thước chính xác $\left[\frac{(W/L)_p}{(W/L)_n}\right]_{\text{target}}$ để điện áp chuyển mạch đối xứng $V_M = V_{DD}/2 = 2,50\,\text{V}$.
2. Với chiều dài kênh chuẩn $L_n = L_p = 2\lambda = 0,60\,\mu\text{m}$, chọn $W_n = 4\lambda = 1,20\,\mu\text{m}$. Nếu chọn $W_p = 12\lambda = 3,60\,\mu\text{m}$ (tỉ số nguyên $W_p/W_n = 3,0$ theo chuẩn lưới):
   - Tính hệ số $r = \frac{k_p}{k_n}$.
   - Tính điện áp chuyển mạch lý thuyết $V_M$ tương ứng và xác định sai lệch so với mốc $2,50\,\text{V}$.

### P3. Ước lượng điện trở dẫn $R_{on}$ và thời gian trễ
1. Tính điện trở dẫn hiệu dụng ở vùng triode sâu ($V_{DS} \to 0$ khi mở sâu) của NMOS ($W_n = 1,2\,\mu\text{m}$) và PMOS ($W_p = 3,6\,\mu\text{m}$) theo công thức ở mục 3.3.
2. Với tải dung chuẩn $C_L = 50\,\text{fF}$, ước lượng trễ lý thuyết $t_{pHL}, t_{pLH}$ và $t_{pd}$ theo mô hình $0,69 \cdot R_{on} \cdot C_L$.
3. **Dự đoán:** Khi đo đạc thực tế trên LTspice, thời gian trễ thu được sẽ *lớn hơn* hay *nhỏ hơn* giá trị ước lượng $0,69 \cdot R_{on} \cdot C_L$ này? Nêu lý do ngắn gọn trong 1 câu.

### P4. Thiết kế sơ đồ que (Stick Diagram)
Vẽ sơ đồ que của tế bào CMOS Inverter lên giấy kẻ ô ly. Yêu cầu thể hiện rõ:
- Thanh nguồn $V_{DD}$ và thanh đất $GND$ bằng lớp Metal 1.
- Vùng P-Active trong N-Well (nửa trên) và N-Active trên đế P (nửa dưới).
- Dải Polysilicon liên tục chạy dọc tạo cực cổng cho cả hai transistor, nối ra cổng `in`.
- Dây nối Metal 1 giữa hai cực Drain ra cổng `out`.
- Các vị trí tiếp xúc Contact (Active-to-Metal 1, Poly-to-Metal 1).
- Tiếp xúc phân cực $N^+$-tap (nối N-Well lên $V_{DD}$) và $P^+$-tap (nối P-Substrate xuống $GND$).

### P5. Chuẩn bị khung Netlist SPICE
Điền các giá trị thích hợp vào chỗ trống `____` trong đoạn netlist SPICE dưới đây để mô phỏng VTC và trễ quá độ của Inverter:

```spice
* Netlist CMOS Inverter - MOSIS C5N 0.5um
.include C5_models.txt

* Nguon cap va kich thich
Vdd vdd 0 DC ____
Vin in  0 PULSE(0 ____ 0 100p 100p 9.9n 20n)

* Transistor PMOS va NMOS
MP out in vdd vdd P L=____ W=____
MN out in 0   0   N L=____ W=____

* Tai dung ngo ra
CL out 0 ____

* Phan tich qua do va cau lenh do tre
.tran 1p 50n
.meas TRAN tpHL TRIG V(in)=____ RISE=1 TARG V(out)=____ FALL=1
.meas TRAN tpLH TRIG V(in)=____ FALL=1 TARG V(out)=____ RISE=1
.meas TRAN tpd  PARAM (tpHL + tpLH)/2
.end
```

### Cổng kiểm tra đầu buổi
Giảng viên kiểm tra trực tiếp P1, P2, P4 và P5 tại bàn thực hành. Sinh viên chưa hoàn thành P2 hoặc P4 sẽ không được phép khởi động máy tính thực hành.

---

## 5. IN-LAB (THỰC HÀNH TẠI PHÒNG MÁY — 135 PHÚT)

> [!IMPORTANT]
> **Thử ngay:** Mở thư mục làm việc `lab_vlsi/`. Đảm bảo tệp `C5_models.txt` đã có sẵn trong thư mục. Mọi tệp sơ đồ (`.asc`), netlist (`.sp`) và thư viện Electric (`.jelib`) đều lưu trong thư mục này.

### Ex1.1 (bắt buộc): Khảo sát đặc tính I-V của NMOS và PMOS trên LTspice
1. Mở LTspice, tạo schematic mới đặt tên `nmos_iv.asc`.
2. Đặt transistor `nmos4` (phím `F2`). Nhấn chuột phải vào linh kiện, đặt Model = `N`, `L = 0.6u`, `W = 1.2u`. Nối cực Source (S) và Bulk (B) xuống đất `0`.
3. Đặt nguồn $V_{DS}$ nối vào cực Drain, nguồn $V_{GS}$ nối vào cực Gate. Thêm lệnh `.include C5_models.txt` (phím `S`).
4. **Khảo sát họ đặc tuyến ra $I_{DS}-V_{DS}$:**
   - Cấu hình quét DC lồng nhau: `.dc VDS 0 5 0.01 VGS 1 5 1`.
   - Chạy mô phỏng (`Run`), chọn đo dòng cực Drain `I(M1)`.
   - Quan sát 5 đường đặc tuyến tương ứng $V_{GS} = 1\,\text{V}, 2\,\text{V}, 3\,\text{V}, 4\,\text{V}, 5\,\text{V}$.
   - Dùng con trỏ (Cursor) trên đường cong $V_{GS} = 5\,\text{V}$, chọn 2 điểm trong vùng bão hòa ($V_{DS1} = 3,0\,\text{V}$ và $V_{DS2} = 5,0\,\text{V}$) để tính hệ số điều chế kênh $\lambda_n$:

     $$\lambda \approx \frac{\Delta I_{DS}}{I_{DS1} \cdot \Delta V_{DS}}$$

5. **Khảo sát đặc tuyến truyền dẫn $I_{DS}-V_{GS}$ và đo $V_{thn}$:**
   - Cố định $V_{DS} = 5,0\,\text{V}$. Đổi lệnh mô phỏng thành quét đơn: `.dc VGS 0 5 0.01`.
   - Thêm đường cong căn bậc hai của dòng: biểu thức `sqrt(I(M1))`.
   - Tìm giao điểm của tiếp tuyến đoạn tuyến tính với trục hoành để trích xuất $V_{thn}$.
6. **Lặp lại cho PMOS (`pmos_iv.asc`):** Dùng `pmos4`, Model = `P`, `L = 0.6u`, `W = 3.6u`. Cực Source và Bulk nối lên nguồn $V_{DD} = 5,0\,\text{V}$. Quét điện áp $|V_{DS}|$ và $|V_{GS}|$ từ $0 \to 5\,\text{V}$, trích xuất $V_{thp}$ và dòng bão hòa cực đại.

**Sản phẩm:** Ảnh chụp dạng sóng $I_{DS}-V_{DS}$ (5 nhánh) của NMOS; bảng ghi giá trị trích xuất thực nghiệm ($V_{thn}, V_{thp}, \lambda_n, I_{DS,sat}$).  
**Câu hỏi kiểm tra:** Độ dốc của đường đặc tuyến trong vùng bão hòa phản ánh thông số vật lý nào? Vì sao dòng bão hòa của NMOS ($W=1,2\,\mu\text{m}$) và PMOS ($W=3,6\,\mu\text{m}$) ở $5\,\text{V}$ lại xấp xỉ bằng nhau?

---

### Ex1.2 (bắt buộc): Thiết kế Schematic CMOS Inverter và phân tích VTC
1. Mở Electric VLSI, tạo cell mới: Cell Name: `inv_x1`, View: `schematic`.
2. Đặt linh kiện:
   - 1 PMOS: $W = 12\lambda$ ($3,6\,\mu\text{m}$), $L = 2\lambda$ ($0,6\,\mu\text{m}$).
   - 1 NMOS: $W = 4\lambda$ ($1,2\,\mu\text{m}$), $L = 2\lambda$ ($0,6\,\mu\text{m}$).
3. Đi dây nối cực Cổng chung làm ngõ vào `in`, cực Máng chung làm ngõ ra `out`. Nối cực Nguồn PMOS lên `vdd`, cực Nguồn NMOS xuống `gnd`.
4. Tạo chân giao tiếp (Export Ports): `in` (Input), `out` (Output), `vdd` (Power), `gnd` (Ground). Nhấn `F5` kiểm tra kết nối logic (không có lỗi dây hở).
5. Xuất netlist SPICE sang LTspice (*Tools $\to$ Simulation (Spice) $\to$ Write Spice Deck*).
6. Trong LTspice, cấu hình phân tích quét DC ngõ vào:
   ```spice
   .dc Vin 0 5 0.002
   ```
7. Chạy mô phỏng, vẽ đồ thị $V_{out} = f(V_{in})$.
8. Dùng con trỏ xác định giao điểm $V_{out} = V_{in}$ để đọc điện áp chuyển mạch $V_M$.
9. Thêm một pane đồ thị mới, vẽ đạo hàm điện áp `d(V(out))/d(V(in))`. Xác định hai điểm có độ dốc bằng $-1,00$:
   - Điểm thứ nhất (khi $V_{in} < V_M$): đọc điện áp $V_{IL}$.
   - Điểm thứ hai (khi $V_{in} > V_M$): đọc điện áp $V_{IH}$.
   - Tính lề nhiễu logic: $NM_L = V_{IL} - V_{OL} = V_{IL}$ và $NM_H = V_{OH} - V_{IH} = 5,0 - V_{IH}$.

**Sản phẩm:** Ảnh chụp sơ đồ Schematic trong Electric; ảnh đồ thị hàm truyền VTC kèm đường dốc đạo hàm; bảng thông số $V_M, V_{IL}, V_{IH}, NM_L, NM_H$.  
**Câu hỏi kiểm tra:** Điện áp chuyển mạch đo được lệch bao nhiêu mV so với $2,50\,\text{V}$? Sự sai khác này xuất phát từ nguyên nhân nào trong việc chọn kích thước?

---

### Ex1.3 (bắt buộc): Mô phỏng quá độ Transient & trích xuất trễ bằng lệnh `.meas`
1. Chuyển mạch sang phân tích quá độ miền thời gian:
   - Cấu hình nguồn xung tại ngõ vào:
     ```spice
     Vin in 0 PULSE(0 5.0 0 100p 100p 9.9n 20n)
     ```
   - Đặt tải dung $C_L = 50\,\text{fF}$ tại ngõ ra `out`.
   - Cấu hình phân tích `.tran 1p 50n`.
2. Chèn khối lệnh `.meas` tự động (nhấn phím `S`):
   ```spice
   .meas TRAN tpHL TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 FALL=1
   .meas TRAN tpLH TRIG V(in)=2.5 FALL=1 TARG V(out)=2.5 RISE=1
   .meas TRAN tpd  PARAM (tpHL + tpLH)/2
   .meas TRAN trise TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1
   .meas TRAN tfall TRIG V(out)=4.5 FALL=1 TARG V(out)=0.5 FALL=1
   ```
3. Chạy mô phỏng. Mở **SPICE Error Log** (`Ctrl + L`) để đọc trực tiếp các thông số trễ.
4. Quét ảnh hưởng của tải dung: Thay đổi $C_L$ lần lượt thành $10\,\text{fF}$ và $100\,\text{fF}$ (hoặc dùng `.step param CL list 10f 50f 100f`). Ghi lại các giá trị trễ vào bảng số liệu.
5. **Đóng gói Icon trong Electric:** Trở lại Electric, mở menu **View $\to$ Make Icon View**. Chỉnh sửa biểu tượng cổng NOT chuẩn IEEE với đủ 4 chân `in`, `out`, `vdd`, `gnd`.

**Sản phẩm:** Ảnh dạng sóng chuyển mạch $V_{in}(t)$ và $V_{out}(t)$; nội dung trích xuất từ SPICE Error Log; bảng số liệu trễ ở 3 mức tải dung; ảnh biểu tượng Icon View hoàn thiện.  
**Câu hỏi kiểm tra:** So sánh giá trị $t_{pd}$ đo được tại $C_L = 50\,\text{fF}$ với giá trị ước lượng $0,69 \cdot R_{on} \cdot C_L$ ở Pre-lab. Tỉ số giữa hai giá trị này bằng bao nhiêu và giải thích bản chất vật lý?

---

### Ex1.4 (tiêu chuẩn): Thiết kế Mask Layout, chạy DRC & đối chiếu LVS
1. Trong Electric, tạo cell mới: Cell Name: `inv_x1`, View: `layout`.
2. Tạo hai thanh ray nguồn nằm ngang bằng lớp Metal 1, độ rộng tối thiểu $6\lambda$ ($1,8\,\mu\text{m}$): thanh trên gán export `vdd`, thanh dưới gán export `gnd`.
3. Nửa trên: Vẽ vùng N-Well; đặt vùng P-Active kích thước $W = 12\lambda$ ($3,6\,\mu\text{m}$), $L = 2\lambda$ ($0,6\,\mu\text{m}$).
4. Nửa dưới: Đặt vùng N-Active kích thước $W = 4\lambda$ ($1,2\,\mu\text{m}$), $L = 2\lambda$ ($0,6\,\mu\text{m}$).
5. Vẽ dải Polysilicon liên tục cắt dọc qua cả hai vùng Active làm cổng chung. Dải Poly phải vươn thừa ra ngoài mép Active tối thiểu $2\lambda$ ($0,6\,\mu\text{m}$). Gán Export port tên `in` tại đầu dải Poly.
6. Đặt các tiếp xúc Contact:
   - Nối cực Source PMOS lên thanh `vdd`.
   - Nối cực Source NMOS xuống thanh `gnd`.
   - Nối chung cực Drain của PMOS và NMOS bằng Metal 1, tạo Export port tên `out`.
7. **Đặt tiếp xúc chống Latch-up:**
   - Đặt tiếp xúc $N^+$-tap trong N-Well nối lên thanh `vdd`.
   - Đặt tiếp xúc $P^+$-tap trên nền P nối xuống thanh `gnd`.
8. **Kiểm tra luật hình học DRC:** Nhấn phím `F5`. Hiệu chỉnh khoảng cách và độ rộng các lớp cho đến khi thanh trạng thái báo: **"0 errors found"**.
9. **Đối chiếu sơ đồ logic LVS (NCC):** Chọn menu **Tools $\to$ NCC $\to$ Schematic and Layout Comparison**. Kiểm tra kết quả trong cửa sổ thông báo đạt: **"Cells are topologically equivalent (MATCH)"**.

**Sản phẩm:** Ảnh chụp màn hình Layout hoàn chỉnh có đầy đủ nhãn cổng và Taps; ảnh thông báo DRC đạt 0 lỗi; ảnh thông báo NCC so sánh LVS đạt trạng thái MATCH.  
**Câu hỏi kiểm tra:** Nếu bỏ quên tiếp xúc $N^+$-tap hoặc $P^+$-tap, công cụ DRC và NCC sẽ phản ứng như thế nào? Trong thực tế chế tạo, hậu quả nghiêm trọng nhất là gì?

---

### Ex1.5 (thử thách): Trích xuất ký sinh (PEX) & Phân tích Post-layout
1. Trong cửa sổ Layout của `inv_x1`, chọn menu **Tools $\to$ Simulation (Spice) $\to$ Options**, đánh dấu chọn mục **"Extract Parasitic Capacitances"** và **"Extract Parasitic Resistances"**.
2. Xuất netlist sau trích xuất: **Tools $\to$ Simulation (Spice) $\to$ Write Spice Deck**, lưu tệp dạng `inv_x1_pex.sp`.
3. Mở tệp netlist vừa sinh ra bằng trình soạn thảo văn bản, quan sát các tham số hình học khuếch tán (`AS, AD, PS, PD`) được gán thêm vào transistor và các phần tử tụ ký sinh dây dẫn (`C...`).
4. Mở netlist này trong LTspice, bổ sung nguồn kích thích và tải dung ngoài $C_L = 50\,\text{fF}$ giống hệt điều kiện đo ở Ex1.3.
5. Chạy mô phỏng quá độ Transient, dùng `.meas` đọc các thông số trễ Post-layout: $t_{pHL,post}, t_{pLH,post}, t_{pd,post}$.
6. Tính toán phần trăm suy giảm tốc độ:

   $$\Delta t_{pd} (\%) = \frac{t_{pd,post} - t_{pd,pre}}{t_{pd,pre}} \times 100\%$$

**Sản phẩm:** Bảng so sánh 3 chiều: Lý thuyết giải tích | Mô phỏng Pre-layout | Mô phỏng Post-layout (PEX); số phần trăm tăng trễ.  
**Câu hỏi kiểm tra:** Tụ ký sinh khuếch tán cực má ($C_{db}$) và tụ ký sinh dây kim loại đóng góp xấp xỉ bao nhiêu phần trăm vào sự gia tăng độ trễ ngõ ra?

---

## 6. KIỂM CHỨNG VÀ SO SÁNH KẾT QUẢ

Sinh viên tổng hợp số liệu đo đạc và kiểm chứng vào bảng đối chuẩn dưới đây (tại tải chuẩn $C_L = 50\,\text{fF}$):

| Đại lượng kỹ thuật | [1] Lý thuyết Pre-lab | [2] Mô phỏng Pre-layout | [3] Mô phỏng Post-layout | Sai lệch Pre vs LT ($\frac{[2]-[1]}{[1]}$) | Tăng trễ PEX ($\frac{[3]-[2]}{[2]}$) | Ngưỡng chấp nhận |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Điện áp chuyển mạch $V_M$** | $2,45\,\text{V}$ | .................... V | .................... V | .................... % | — | $\le 3\%$ |
| **Lề nhiễu mức thấp $NM_L$** | $\ge 1,5\,\text{V}$ | .................... V | .................... V | — | — | $\ge 1,5\,\text{V}$ |
| **Lề nhiễu mức cao $NM_H$** | $\ge 1,5\,\text{V}$ | .................... V | .................... V | — | — | $\ge 1,5\,\text{V}$ |
| **Trễ sườn xuống $t_{pHL}$** | .................... ps | .................... ps | .................... ps | .................... % | .................... % | $\le 20\%$ so với benchmark |
| **Trễ sườn lên $t_{pLH}$** | .................... ps | .................... ps | .................... ps | .................... % | .................... % | $\le 20\%$ so với benchmark |
| **Trễ trung bình $t_{pd}$** | .................... ps | .................... ps | .................... ps | .................... % | .................... % | $\le 20\%$ so với benchmark |

### Thứ tự chẩn đoán nguyên nhân khi số đo vượt ngưỡng sai lệch:
1. **Kiểm tra mức điện áp đo trong `.meas`:** Điểm đo trễ 50% phải đặt tại $2,5\,\text{V}$ (`TRIG V(in)=2.5 TARG V(out)=2.5`). Nếu nhập sai thành $0,5\,\text{V}$ hoặc nhầm lẫn sườn `RISE`/`FALL`, số đo sẽ sai lệch.
2. **Kiểm tra bước thời gian mô phỏng:** Đảm bảo lệnh `.tran` có bước tích phân đủ mịn (ví dụ `.tran 1p 50n`). Nếu bước thời gian quá thô, SPICE nội suy tuyến tính giữa các điểm rời rạc sẽ gây sai số trễ vài chục picosecond.
3. **Kiểm tra đơn vị linh kiện:** Trong netlist, kiểm tra đơn vị $W$ và $L$. Viết `1.2u` chứ không viết `1.2` (SPICE sẽ hiểu là 1,2 mét). Kiểm tra tụ tải `50f` (femto) chứ không viết `50p` hay `50m`.
4. **Kiểm tra phân cực Bulk:** Đảm bảo chân Bulk của PMOS nối chắc chắn lên `vdd` và chân Bulk của NMOS nối xuống `gnd`. Nếu nối hở hoặc nối nhầm chân, hiệu ứng thân sẽ làm điện áp ngưỡng dịch chuyển mạnh.

---

## 7. POST-LAB (BÁO CÁO VÀ ĐÁNH GIÁ MỞ RỘNG)

Sinh viên trả lời 3 câu hỏi sau vào phần cuối của báo cáo thực hành:

1. **Phân tích kích thước không đối xứng:** Nếu một nhà thiết kế quyết định định kích thước $W_p = W_n = 4\lambda = 1,2\,\mu\text{m}$ nhằm tiết kiệm diện tích silicon:
   - Hãy dự đoán dạng biến đổi của đường cong VTC (điểm $V_M$ sẽ dịch sang trái hay sang phải, lề nhiễu nào bị thu hẹp)?
   - Tỉ số trễ $t_{pLH}/t_{pHL}$ sẽ thay đổi như thế nào? Trong các ứng dụng thực tế nào thì thiết kế $W_p = W_n$ được ưu tiên chấp nhận?
2. **Bản chất vật lý của sự tăng trễ hậu trích xuất:** Dựa vào các tham số trích xuất (`AS, AD, PS, PD`) trong netlist Post-layout, hãy phân tích cơ chế vật lý tạo nên các tụ ký sinh khuếch tán má $C_{db}$. Tại sao khi kéo tải ngoài $C_L$ rất lớn (ví dụ $1\,\text{pF}$) thì ảnh hưởng phần trăm của tụ ký sinh hậu layout lại trở nên không đáng kể?
3. **Cơ chế chống Latch-up của Guard Rings:** Giải thích cơ chế vì sao việc đặt các dải phân cực liên tục (Guard Rings) bao quanh transistor lại có khả năng triệt tiêu nguy cơ kích hoạt dòng ngắn mạch Latch-up tốt hơn so với việc chỉ đặt một vài nốt tiếp xúc Tap rời rạc.

### Danh mục tệp nộp bài
Sinh viên nén các tệp sau vào tệp lưu trữ `MSSV_Lab01.zip`:
- `nmos_iv.asc`, `pmos_iv.asc`: Sơ đồ mô phỏng I-V trên LTspice.
- `inv_schematic.asc` (hoặc thư viện `lab1.jelib` của Electric): Chứa cell `inv_x1` với Schematic, Icon View và Layout.
- `inv_x1_pex.sp`: Netlist SPICE hậu trích xuất ký sinh PEX.
- Tệp báo cáo PDF hoàn chỉnh (ảnh chụp sơ đồ, đồ thị VTC, log đo `.meas`, bảng kiểm chứng và giải thích câu hỏi Post-lab).

---

## 8. LỖI THƯỜNG GẶP VÀ CÁCH KHẮC PHỤC

| Hiện tượng lỗi | Nguyên nhân gốc rễ | Giải pháp xử lý |
| :--- | :--- | :--- |
| **NCC báo "Netlists do NOT match"** | Sai lệch tên chân Export giữa Schematic và Layout (ví dụ một bên đặt `IN`, bên kia đặt `in`, do Electric phân biệt hoa/thường). | Kiểm tra và chuẩn hóa tên chân Export trên cả hai view: `in`, `out`, `vdd`, `gnd` đồng nhất chữ thường. |
| **DRC báo lỗi "N-Well overlap" hoặc khoảng cách Poly** | Vẽ dải Poly quá sát mép tiếp xúc Contact hoặc vùng Active không đủ khoảng vươn ($< 2\lambda$). | Bật hiển thị lưới (*Grid*), căn chỉnh các lớp theo bội số của $\lambda = 0,30\,\mu\text{m}$; giữ khoảng cách Poly – Contact $\ge 2\lambda$. |
| **Đồ thị VTC dốc ngược hoặc không chuyển mức** | Nhầm lẫn cực Source và Drain của PMOS, hoặc Bulk của PMOS bị nối nhầm xuống `gnd` thay vì `vdd`. | Kiểm tra lại sơ đồ: Bulk PMOS luôn lên $V_{DD}$, Bulk NMOS luôn xuống $GND$. |
| **Lệnh `.meas` báo lỗi "FAIL" trong Error Log** | Mức điện áp kích thích trong nguồn PULSE không vượt qua ngưỡng $2,5\,\text{V}$, hoặc chu kỳ xung quá ngắn khiến mạch chưa kịp chuyển trạng thái. | Kiểm tra cú pháp nguồn: `PULSE(0 5.0 0 100p 100p 9.9n 20n)`; chu kỳ $20\,\text{ns}$ ($50\,\text{MHz}$) đủ lớn cho $C_L = 50\,\text{fF}$. |
| **LTspice báo lỗi không tìm thấy mô hình linh kiện** | Tệp `C5_models.txt` không nằm cùng thư mục với sơ đồ `.asc`, hoặc đường dẫn chứa ký tự tiếng Việt có dấu. | Đặt tệp `.asc` và `C5_models.txt` trong cùng thư mục đường dẫn ngắn (ví dụ `D:\tam\Spice\lab_vlsi\`). |

---

## 9. TÁI SỬ DỤNG CHO CÁC BÀI LAB TIẾP THEO

Tế bào chuẩn `INV_X1` xây dựng trong bài này là khối nền tảng xuyên suốt toàn bộ học phần:
- [ ] Thư viện `lab_vlsi.jelib` chứa cell `inv_x1` với 3 view hoàn chỉnh: `schematic`, `icon`, `layout`.
- [ ] Icon View của `inv_x1` được dùng trực tiếp để ghép nối cổng NAND/NOR tĩnh ở Lab 2 và xây dựng chuỗi đệm Inverter tối ưu trễ ở Lab 3.
- [ ] Layout của `inv_x1` với chiều cao khung tế bào chuẩn ($H_{cell} = 36\lambda$ hoặc $40\lambda$) sẽ dùng làm chiều cao chuẩn đồng mức cho tất cả các cổng logic tiếp theo để tạo kênh chạy nguồn `vdd`/`gnd` liền mạch.

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

Đánh giá theo chuẩn đầu ra học phần (áp dụng Tiêu chí 1: Kỹ năng mô phỏng và thiết kế vi mạch):

| Tiêu chí | Trọng số | Mức Xuất sắc (8,5 – 10) | Mức Khá (7,0 – 8,4) | Mức Đạt (5,0 – 6,9) | Mức Không đạt (< 5,0) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Chuẩn bị Pre-lab (Mục 4)** | **20%** | Điền đủ tham số P1; tính đúng giải tích P2, P3; vẽ Stick diagram P4 chuẩn xác có Taps; khung netlist P5 hoàn chỉnh. | Điền đủ P1, P2; Stick diagram đúng cấu trúc cơ bản nhưng thiếu chú thích chi tiết; netlist đúng. | Tính toán P2 còn nhầm lẫn số học; Stick diagram thiếu tiếp xúc Taps; chuẩn bị netlist chưa xong. | Không làm bài chuẩn bị Pre-lab ở nhà hoặc sao chép bài của người khác. |
| **2. Đo đạc I-V & Phân tích VTC (Ex1.1, Ex1.2)** | **25%** | Trích xuất chính xác đặc tuyến $I_{DS}-V_{DS}$ và $V_{th}, \lambda$; Schematic chuẩn; đo chuẩn xác $V_M$, tiếp tuyến dốc $-1$ cho $NM_L, NM_H$. | Trích xuất đúng đặc tuyến; Schematic đúng; đo được $V_M$ và lề nhiễu nhưng thao tác còn chậm. | Dựng được Schematic; chạy được VTC nhưng xác định $V_M$ hoặc lề nhiễu còn sai sót. | Mạch báo lỗi không mô phỏng được hoặc không trích xuất được tham số. |
| **3. Mô phỏng Transient & Lệnh `.meas` (Ex1.3)** | **20%** | Cấu hình nguồn xung đúng chuẩn; dùng thành thạo khối lệnh `.meas` đo đủ 5 tham số ở 3 mức tải; tạo Icon View chuẩn IEEE. | Đo được thông số trễ với `.meas`; lập đủ bảng số liệu; tạo được Icon nhưng vị trí chân chưa chuẩn. | Đo trễ bằng con trỏ thủ công do chưa chạy được lệnh `.meas`; Icon vẽ sơ sài. | Không đo được thông số trễ hoặc không tạo được Icon View. |
| **4. Mask Layout, DRC & LVS (Ex1.4)** | **25%** | Layout chuẩn đẹp, tối ưu diện tích; kiểm tra DRC đạt 0 lỗi; NCC đối chiếu LVS báo MATCH độc lập tại bàn. | Layout đúng chuẩn; DRC đạt 0 lỗi; LVS báo MATCH sau khi được giảng viên hướng dẫn sửa tên port. | Layout còn cồng kềnh; còn vi phạm một vài lỗi DRC nhưng tự sửa được; LVS match. | Vi phạm nhiều lỗi DRC nghiêm trọng; LVS báo lỗi không tương đương topo; bỏ dở layout. |
| **5. Trích xuất PEX & Báo cáo Post-lab (Ex1.5, Mục 7)** | **10%** | Xuất netlist PEX thành công; đo và lập bảng đối chuẩn 3 chiều; trả lời xuất sắc 3 câu hỏi bản chất vật lý. | Trích xuất được PEX; điền đủ bảng đối chuẩn; trả lời đúng các câu hỏi lý thuyết chính. | Trích xuất được PEX nhưng phần phân tích nguyên nhân sai lệch còn mơ hồ, chưa sâu. | Không thực hiện được bước PEX hoặc nộp báo cáo để trống nhiều phần. |

---

## 11. TÀI LIỆU THAM KHẢO

1. Neil H. E. Weste, David Money Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th Edition, Addison-Wesley, 2011 (Chương 2: MOS Transistor Theory; Chương 3: Delay).
2. Jan M. Rabaey, Anantha Chandrakasan, Borivoje Nikolic, *Digital Integrated Circuits: A Design Perspective*, 2nd Edition, Prentice Hall, 2003 (Chương 3: The Devices; Chương 5: The Inverter).
3. Steven M. Rubin, *Electric VLSI Design System User's Manual*, Static Free Software, 2017.
4. Analog Devices, *LTspice Information & Help Guide*, Analog Devices Inc., 2024.
5. MOSIS Service, *SCMOS Layout Design Rules (Submicron 0.5 micron C5N Process)*, Information Sciences Institute, University of Southern California.
