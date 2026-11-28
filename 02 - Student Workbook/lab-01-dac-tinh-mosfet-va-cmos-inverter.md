# THỰC HÀNH THIẾT KẾ VLSI — BÀI 1
# ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER

---
**Học phần:** Thực hành Thiết kế VLSI (Mã học phần: `5505382`)  
*(Phần thực hành mô phỏng SPICE và thiết kế Layout phục vụ trực tiếp nội dung đồ án môn học)*  
**Bộ môn:** Điện tử - Viễn thông | **Khoa:** Điện - Điện tử | **Trường:** Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng  
**Liên hệ giáo trình:** Chương 2 (Đặc tính linh kiện MOSFET), Chương 4 (Mô hình trễ RC và cổng Inverter)  
**Công cụ sử dụng:** Electric VLSI Design System (v9.07 trở lên), LTspice (XVII hoặc LTspice 24/2025)  
**Công nghệ tham chiếu:** MOSIS SCMOS SUBMICRON C5N 0.5 µm (Lưới thiết kế $\lambda_{DR} = 0,30\,\mu\text{m}$, 3 lớp kim loại, $V_{DD} = 5,0\,\text{V}$)  
**Thời lượng:** Pre-lab khoảng 1,5 giờ ở nhà; In-lab 1 buổi (3 tiết = 135 phút tại phòng máy); Post-lab khoảng 1 giờ  
---

## 1. MỤC TIÊU BÀI THỰC HÀNH

Sau khi hoàn thành bài thực hành này, sinh viên có khả năng:
1. **Trích xuất thực nghiệm đặc tính I-V của MOSFET:** Sử dụng LTspice quét DC hai biến để vẽ họ đặc tuyến ra $I_{DS}-V_{DS}$ và đặc tuyến truyền dẫn $I_{DS}-V_{GS}$ của NMOS và PMOS; xác định điện áp ngưỡng ($V_{thn}, V_{thp}$) và hệ số điều chế chiều dài kênh $\lambda_{CLM}$ trong vùng bão hòa (CLO1, CLO2).
2. **Thiết kế sơ đồ nguyên lý & Phân tích VTC:** Dựng sơ đồ nguyên lý (Schematic) trên Electric VLSI với kích thước kênh cân bằng dẫn nạp ($W_p/W_n = 3/1$); mô phỏng đường đặc tuyến truyền đạt điện áp (VTC), xác định điện áp chuyển mạch $V_M$ và các mức lề nhiễu logic $NM_L, NM_H$, so sánh và đối chiếu với dự đoán giải tích ở phần Pre-lab (CLO2).
3. **Đo đạc động học trễ bằng câu lệnh SPICE:** Cấu hình nguồn xung và chèn các câu lệnh `.meas` tham số hóa để trích xuất tự động trễ sườn xuống $t_{pHL}$, trễ sườn lên $t_{pLH}$, trễ truyền lan trung bình $t_{pd}$, thời gian tăng $t_r$ và giảm $t_f$ ở ba mức tải dung $C_L = 10\,\text{fF}, 50\,\text{fF}, 100\,\text{fF}$; so sánh với giá trị chuẩn Benchmark và giải thích cơ chế vật lý của sai lệch so với mô hình Elmore $0,69 \cdot R_{on} \cdot C_L$ (CLO2).
4. **Thiết kế Layout và kiểm chứng vật lý:** Thiết kế mặt nạ vật lý (Mask Layout) cho Inverter tuân thủ quy tắc hình học MOSIS SCMOS Submicron (lưới $\lambda_{DR} = 0,30\,\mu\text{m}$); thực hiện kiểm tra luật hình học DRC đạt 0 lỗi (*0 errors found*) và đối chiếu sơ đồ nguyên lý LVS (công cụ NCC) đạt trạng thái trùng khớp topo (*MATCH*) (CLO2, CLO4).
5. **Đánh giá ảnh hưởng ký sinh hậu thiết kế (PEX):** Trích xuất tụ ký sinh khuếch tán ($C_{db}, C_{sb}$) và tụ liên kết kim loại; chạy mô phỏng Post-layout để định lượng mức suy giảm tốc độ truyền lan so với Pre-layout; hoàn thiện tế bào chuẩn `INV_X1` sẵn sàng tái sử dụng cho các bài lab sau (CLO2, CLO4).

---

## 2. KẾ THỪA VÀ SẢN PHẨM BÀN GIAO

| Thành phần | Chi tiết chuyển giao kỹ thuật |
| :--- | :--- |
| **Dùng lại từ lab trước** | - Thư mục dự án chuẩn hóa `lab01_MSSV_HoTen/` kế thừa quy tắc tổ chức từ Lab 0.<br>- Tệp mô hình công nghệ `C5_models.txt` (Level 3) sao chép từ thư mục `04 - Models_and_Libraries/`.<br>- Kỹ năng viết netlist SPICE, cấu hình phân tích `.dc`, `.tran` và khối câu lệnh `.meas` tham số hóa `{0.5*Vdd}` đo thời gian trễ tự động.<br>- Mô hình trễ $RC$ cơ bản $t_{50} = \ln(2) \cdot R \cdot C \approx 0,69 \cdot R \cdot C$ đã kiểm chứng ở Lab 0. |
| **Sinh ra cho lab sau** | - Tế bào chuẩn `INV_X1` hoàn chỉnh (Schematic, Layout, Icon View) trong thư viện `lab_vlsi.jelib` làm tế bào gốc cho Lab 2 (NAND/NOR), Lab 3 (AOI/OAI), Lab 5 (Flip-Flop) và Lab 10 (ALU 4-bit).<br>- Chiều cao khung tế bào chuẩn thống nhất $H_{cell} = 40\lambda_{DR} = 12,0\,\mu\text{m}$ dùng đồng mức cho toàn bộ các bài lab tiếp theo.<br>- Giá trị chuẩn thực nghiệm của $R_{on,n}, R_{on,p}, t_{pd0}$ và điện dung ngõ vào $C_{in}$ làm đơn vị chuẩn hóa (Inverter chuẩn) cho phương pháp Nỗ lực Logic (Logical Effort) tại Lab 3. |

---

## 3. CƠ SỞ LÝ THUYẾT NGẮN GỌN

### 3.1. Phân biệt hai ký hiệu $\lambda$ và Mô hình dòng điện MOSFET
Trong tài liệu vi mạch, ký hiệu $\lambda$ được sử dụng cho hai đại lượng vật lý hoàn toàn độc lập:
- **$\lambda_{CLM}$ (Channel Length Modulation, đơn vị $\text{V}^{-1}$):** Hệ số điều chế chiều dài kênh dẫn trong phương trình dòng điện SPICE.
- **$\lambda_{DR}$ (Design Rule Grid, đơn vị $\mu\text{m}$):** Đơn vị chiều dài cơ sở của lưới layout theo luật Mead-Conway SCMOS ($\\lambda_{DR} = 0,30\,\mu\text{m}$ trong tiến trình MOSIS C5N $0,5\,\mu\text{m}$).

Trong tiến trình CMOS n-well trên đế p, dòng điện $I_{DS}$ của transistor NMOS được mô hình hóa theo ba vùng hoạt động:

**1. Vùng ngưng dẫn (Cut-off):** Khi $V_{GS} < V_{thn} \implies I_{DS} \approx 0$  
*(Mô hình Level 3 thực tế có dòng rò dưới ngưỡng $I_{sub}$ biến thiên theo hàm mũ của $V_{GS}$)*.

**2. Vùng tuyến tính (Linear / Triode):** Khi $V_{GS} \ge V_{thn}$ và $V_{DS} < V_{DS,sat}$  
Theo mô hình bậc hai cổ điển ($V_{DS,sat} = V_{GS} - V_{thn}$):
$$I_{DS} = K_n' \left(\frac{W}{L}\right)_n \left[ (V_{GS} - V_{thn}) V_{DS} - \frac{V_{DS}^2}{2} \right] (1 + \lambda_{CLM} V_{DS})$$

**3. Vùng bão hòa (Saturation):** Khi $V_{GS} \ge V_{thn}$ và $V_{DS} \ge V_{DS,sat}$
$$I_{DS} = \frac{K_n'}{2} \left(\frac{W}{L}\right)_n (V_{GS} - V_{thn})^2 (1 + \lambda_{CLM} V_{DS})$$

Trong đó:
- $K_n' = \mu_n C_{ox}$ là hệ số truyền dẫn của NMOS (tại công nghệ C5N: $K_n' \approx 120\,\mu\text{A/V}^2$).
- $V_{thn}$ là điện áp ngưỡng không phân cực đế ($V_{thn} \approx 0,70\,\text{V}$).
- Đối với PMOS, cực tính điện áp đảo dấu ($V_{GS}, V_{DS}, V_{thp}$ mang dấu âm) và thay $K_n'$ bằng $K_p' = \mu_p C_{ox}$ (tại công nghệ C5N: $K_p' \approx 40\,\mu\text{A/V}^2$). Do độ linh động electron cao gấp khoảng 3 lần lỗ trống ($\mu_n \approx 3 \mu_p$), nên $K_n' \approx 3 K_p'$.
- **Lưu ý về mô hình Level 3:** Ở kênh dẫn ngắn ($L = 0,6\,\mu\text{m}$), hiệu ứng **bão hòa vận tốc hạt dẫn (Velocity Saturation)** làm electron đạt vận tốc tới hạn sớm hơn, khiến điện thế bão hòa thực tế $V_{DS,sat} < V_{GS} - V_{thn}$.

### 3.2. Đường cong truyền đạt VTC và điện áp chuyển mạch $V_M$
Sơ đồ nguyên lý CMOS Inverter gồm một transistor PMOS kéo lên nguồn $V_{DD}$ và một transistor NMOS kéo xuống đất $GND$:

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

Đặc tuyến truyền đạt $V_{out} = f(V_{in})$ chia thành 5 vùng:
- **Vùng A:** $0 \le V_{in} < V_{thn} \implies$ NMOS tắt, PMOS tuyến tính $\implies V_{out} = V_{OH} = V_{DD}$.
- **Vùng B:** $V_{thn} \le V_{in} < V_M \implies$ NMOS bão hòa, PMOS tuyến tính $\implies V_{out}$ giảm dần.
- **Vùng C:** $V_{in} \approx V_M \implies$ Cả hai transistor đều hoạt động trong vùng bão hòa $\implies$ Độ lợi khuếch đại điện áp đạt cực đại ($-\infty$ trong mô hình lý tưởng).
- **Vùng D:** $V_M < V_{in} \le V_{DD} - |V_{thp}| \implies$ NMOS tuyến tính, PMOS bão hòa $\implies V_{out}$ giảm nhanh về 0 V.
- **Vùng E:** $V_{in} > V_{DD} - |V_{thp}| \implies$ NMOS tuyến tính, PMOS tắt $\implies V_{out} = V_{OL} = 0\,\text{V}$.

Tại điểm chuyển mạch $V_{in} = V_{out} = V_M$, cân bằng dòng bão hòa $I_{D,n} = |I_{D,p}|$:
$$\frac{1}{2} k_n (V_M - V_{thn})^2 = \frac{1}{2} k_p (V_{DD} - V_M - |V_{thp}|)^2$$

Đặt $r = \frac{k_p}{k_n} = \frac{K_p'(W/L)_p}{K_n'(W/L)_n}$, ta thu được công thức giải tích tổng quát:
$$V_M = \frac{V_{thn} + \sqrt{r}(V_{DD} - |V_{thp}|)}{1 + \sqrt{r}}$$

> [!NOTE]
> **Ví dụ minh họa tính $V_M$ trên tiến trình giả định ($V_{DD} = 3,3\,\text{V}$):**  
> Xét tiến trình có $V_{DD} = 3,3\,\text{V}$, $V_{thn} = 0,50\,\text{V}$, $|V_{thp}| = 0,60\,\text{V}$, và $K_n'/K_p' = 2,5$.
> - Nếu chọn $r = 1 \implies (W/L)_p / (W/L)_n = 2,5$:  
>   $$V_M = \frac{0,50 + 1,0 \times (3,3 - 0,60)}{1 + 1,0} = \frac{0,50 + 2,70}{2} = 1,60\,\text{V} \quad (\text{lệch } 0,05\,\text{V so với } V_{DD}/2 = 1,65\,\text{V})$$
> - Muốn đạt chính xác $V_M = 1,65\,\text{V}$:  
>   $$\sqrt{r} = \frac{1,65 - 0,50}{3,3 - 1,65 - 0,60} = \frac{1,15}{1,05} \approx 1,095 \implies r = 1,20 \implies \frac{(W/L)_p}{(W/L)_n} = 1,20 \times 2,5 = 3,00$$

> [!TIP]
> **Quy ước thiết kế tế bào chuẩn:** Trong thực tế thiết kế layout, tỉ số kích thước nguyên theo lưới $\lambda_{DR}$ luôn được ưu tiên để đảm bảo tính đối xứng và mô-đun hóa tế bào chuẩn, dù có thể tạo ra độ dịch chuyển nhỏ của $V_M$ so với mốc đối xứng $V_{DD}/2$.

### 3.3. Điện trở kênh dẫn hiệu dụng $R_{on}$ và mô hình trễ Elmore $RC$
Khi ngõ ra chuyển mức logic, transistor nạp hoặc xả điện dung tải tổng $C_L$. Mạch tương đương quá độ phóng nạp được mô hình hóa bằng mạch Elmore $RC$ bậc một:
- Tại vùng triode sâu ($V_{DS} \to 0$ khi cổng mở sâu $V_{GS} = V_{DD}$):
  $$R_{on,n} = \frac{1}{K_n' \left(\frac{W}{L}\right)_n (V_{DD} - V_{thn})}, \quad R_{on,p} = \frac{1}{K_p' \left(\frac{W}{L}\right)_p (V_{DD} - |V_{thp}|)}$$
- Ước lượng trễ bậc một Elmore:
  $$t_{pHL} \approx 0,69 \cdot R_{on,n} \cdot C_L, \quad t_{pLH} \approx 0,69 \cdot R_{on,p} \cdot C_L, \quad t_{pd} = \frac{t_{pHL} + t_{pLH}}{2}$$

> [!CAUTION]
> **Giới hạn của mô hình $0,69 \cdot R_{on} \cdot C_L$:** Mô hình bậc một giả định điện trở kênh dẫn là hằng số suốt quá trình chuyển mức. Trong thực tế phóng nạp từ $V_{DD}$ về $V_{DD}/2$, transistor bắt đầu từ vùng bão hòa (dòng bị giới hạn bởi điện áp pinch-off, điện trở tức thời $V_{DS}/I_{DS}$ cao hơn nhiều so với vùng triode) rồi mới chuyển dần sang vùng tuyến tính. Do đó, thời gian trễ mô phỏng SPICE thực tế sẽ có sự chênh lệch đáng kể so với ước lượng đơn giản $0,69 \cdot R_{on} \cdot C_L$. Sinh viên cần đo đạc, so sánh và giải thích cơ chế vật lý này trong báo cáo.

### 3.4. Phương pháp đường đi Euler (Euler Path) và Sơ đồ que (Stick Diagram)
Trong thiết kế Layout vi mạch CMOS, mục tiêu hàng đầu là **tối thiểu hóa diện tích silicon** và **giảm thiểu điện dung ký sinh khuếch tán ($C_{db}, C_{sb}$)** bằng hai kỹ thuật:
1. **Chia sẻ vùng khuếch tán (Diffusion Sharing / Abutment):** Ghép các cực Source hoặc cực Drain của các transistor lân cận vào chung một dải khuếch tán.
2. **Đường đi Euler (Eulerian Path):** Tìm thứ tự duyệt các biến cổng chung cho cả mạng kéo lên PUN và mạng kéo xuống PDN để đặt các dải Polysilicon thẳng hàng xuyên suốt mà không làm đứt đoạn dải khuếch tán.

**Trường hợp cơ sở của CMOS Inverter:**  
Do Inverter chỉ có **duy nhất 1 ngõ vào $In$**, đồ thị mạch chỉ có 1 cạnh đơn lập. Thứ tự đường Euler ở đây là trường hợp suy biến:
$$\text{Euler Path: } [In]$$
Dải Polysilicon ngõ vào chạy thẳng đứng từ trên xuống dưới, cắt ngang qua dải P-Active (tạo PMOS) và cắt tiếp qua dải N-Active (tạo NMOS).

```text
======================= Thanh nguồn VDD (Metal 1, 6λ) =======================
       │ [Tap N-Well]                                 │ [Contact Source]
   ┌───┴──────────────────────────────────────────────┴───┐
   │ N-Well (Bao quanh toàn bộ PMOS và Tap)               │
   │                                                      │
   │       ┌───────────────┐                          ┌───┴───┐
   │       │ N-Well Tap    │                          │       │ (P-Active)
   │       │               │                          │   S   │ (Wp = 12λ)
   │       └───────────────┘                      ┌───┴───┐   │
   │                                              │ PMOS  │   │
   │                                              └───┬───┘   │
   │                                                  │   D   │
   │                                                  └───┬───┘
   └──────────────────────────────────────────────────────┼───┘
                                                          │ [Contact Drain]
                        Polysilicon (Cực cổng In)         │
         In ──────────────────────────────────────────────┼───────────── Out (Metal 1, 3λ)
                        (Euler Path: 1 cổng duy nhất)     │
                                                          │ [Contact Drain]
   ┌──────────────────────────────────────────────────────┴───┐
   │ P-Substrate                                              │
   │       ┌───────────────┐                          ┌───┴───┐
   │       │ P-Sub Tap     │                          │       │ (N-Active)
   │       │               │                          │   D   │ (Wn = 4λ)
   │       └───────────────┘                      ┌───┴───┐   │
   │                                              │ NMOS  │   │
   │                                              └───┬───┘   │
   │                                                  │   S   │
   │                                                  └───┬───┘
   └───┬──────────────────────────────────────────────────┴───┐
       │ [Tap P-Sub]                                  │ [Contact Source]
======================= Thanh đất GND (Metal 1, 6λ) =========================
```
*Hình 1.1: Sơ đồ que (Stick Diagram) chuẩn của tế bào CMOS Inverter `INV_X1` (N-Well bao bọc PMOS).*

### 3.5. Quy tắc hình học MOSIS SCMOS và Phòng ngừa Latch-up
Khi chuyển sang Mask Layout chi tiết trong Electric VLSI, thiết kế tuân thủ quy tắc hình học MOSIS SCMOS Submicron với tham số lưới $\lambda_{DR} = 0,30\,\mu\text{m}$:
- **Lưới thiết kế:** $1\lambda_{DR} = 0,30\,\mu\text{m}$. Chiều dài kênh tối thiểu: $L_{min} = 2\lambda_{DR} = 0,60\,\mu\text{m}$.
- **Kích thước transistor chuẩn tế bào `INV_X1`:**
  * Transistor NMOS: $W_n = 4\lambda_{DR} = 1,20\,\mu\text{m}, L_n = 2\lambda_{DR} = 0,60\,\mu\text{m}$.
  * Transistor PMOS: $W_p = 12\lambda_{DR} = 3,60\,\mu\text{m}, L_p = 2\lambda_{DR} = 0,60\,\mu\text{m}$ (tỉ số $W_p/W_n = 3/1$).
- **Độ rộng dây kim loại và thanh ray nguồn:**
  * Dải Polysilicon: tối thiểu $2\lambda_{DR} = 0,60\,\mu\text{m}$.
  * Thanh ray nguồn Metal 1 ($V_{DD}, GND$): chuẩn thiết kế **$6\lambda_{DR} = 1,80\,\mu\text{m}$** (đảm bảo mật độ dòng electromigration khi ghép chuỗi tế bào).
  * Dây Metal 1 nội bộ: tối thiểu $3\lambda_{DR} = 0,90\,\mu\text{m}$.
  * Chiều cao khung tế bào chuẩn thống nhất: **$H_{cell} = 40\lambda_{DR} = 12,0\,\mu\text{m}$**.
- **Quy tắc biên tiếp giáp và phần vươn (Overhang / Enclosure):**
  * Phần Poly vươn qua mép khuếch tán (Gate Overhang) $\ge 2\lambda_{DR} = 0,60\,\mu\text{m}$.
  * Lỗ tiếp xúc Contact: kích thước cố định $2\lambda_{DR} \times 2\lambda_{DR} = 0,60\,\mu\text{m} \times 0,60\,\mu\text{m}$.
  * Lớp bao quanh tiếp xúc (Contact Enclosure) của Active hoặc Metal 1 $\ge 1\lambda_{DR} = 0,30\,\mu\text{m}$.
  * Ranh giới giếng N-Well bao quanh vùng P-Active tối thiểu $6\lambda_{DR} = 1,80\,\mu\text{m}$.

```text
     ┌──────────────────────────────────────────────────────────────┐
     │                VDD Power Rail (Metal 1, 6λ)                  │
     └───────┬──────────────────────────────────────────────┬───────┘
             │                                              │
       [N-Well Tap]                                 [Source Contact]
  ┌──────────┴──────────────────────────────────────────────┴───────────┐
  │ N-Well Boundary (≥ 6λ enclosure around P-Active)                    │
  │   ┌───────────────┐                          ┌──────────────────┐   │
  │   │  N-Well Tap   │                          │ P-Active         │   │
  │   │  (2λ x 2λ)    │         Polysilicon      │ (Wp = 12λ)       │   │
  │   └───────────────┘         (2λ = 0.6µm)     │                  │   │
  │                                  │           │                  │   │
  │                            In ───┼───────────┤ Gate Channel     │   │
  │                                  │           │ (L = 2λ = 0.6µm) │   │
  │                                  │           │                  │   │
  │                                  │           │ P-Active         │   │
  │                                  │           └────────┬─────────┘   │
  └──────────────────────────────────┼────────────────────┼─────────────┘
                                     │                    │ [Drain Contact]
                                     │                    │
                                     │           Out ─────┴───── (Metal 1, 3λ)
                                     │                    │
                                     │                    │ [Drain Contact]
  ┌──────────────────────────────────┼────────────────────┼─────────────┐
  │ P-Substrate                      │           ┌────────┴─────────┐   │
  │   ┌───────────────┐              │           │ N-Active         │   │
  │   │  P-Sub Tap    │              │           │ (Wn = 4λ)        │   │
  │   │  (2λ x 2λ)    │        In ───┼───────────┤ Gate Channel     │   │
  │   └───────────────┘              │           │ (L = 2λ = 0.6µm) │   │
  │                                  │           │                  │   │
  │                             (Gate Overhang   │ N-Active         │   │
  │                              ≥ 2λ = 0.6µm)   └────────┬─────────┘   │
  └──────────┬────────────────────────────────────────────┴─────────────┘
             │                                              │
       [P-Sub Tap]                                  [Source Contact]
     ┌───────┴──────────────────────────────────────────────┴───────┐
     │                GND Power Rail (Metal 1, 6λ)                  │
     └──────────────────────────────────────────────────────────────┘
```
*Hình 1.2: Phân bố mặt nạ Mask Layout chuẩn SCMOS của tế bào `INV_X1` ($H_{cell} = 40\lambda$).*

- **Phòng ngừa hiện tượng Latch-up:**  
  Trong cấu trúc CMOS n-well, hai transistor BJT ký sinh ($p-n-p$ thẳng đứng và $n-p-n$ nằm ngang) ghép hồi tiếp dương tạo thành cấu trúc Thyristor bốn lớp $p-n-p-n$. Khi có xung đột điện áp hoặc nhiễu làm sụt áp trên điện trở nền/giếng ($R_{sub}, R_{well}$) vượt quá $0,7\,\text{V}$, cấu trúc này dẫn thông tạo đường đoản mạch giữa $V_{DD}$ và $GND$ với dòng lớn có thể làm hỏng chip.  
  *Biện pháp bắt buộc:* Bố trí tiếp xúc $N^+$-tap nối N-Well lên $V_{DD}$ và tiếp xúc $P^+$-tap nối P-Substrate xuống $GND$ ngay sát các transistor để dập tắt điện áp phân cực kích hoạt Latch-up.

---

## 4. CÂU HỎI CHUẨN BỊ TRƯỚC KHI ĐẾN LỚP (PRE-LAB)
*(Sinh viên hoàn thành ra giấy hoặc soạn tệp và nộp đầu buổi thực hành)*

### P1. Trích xuất tham số công nghệ từ `C5_models.txt`
Mở tệp `C5_models.txt` (Level 3) trong thư mục dự án `lab01_MSSV_HoTen/`. Tìm hai khối `.MODEL N NMOS` và `.MODEL P PMOS`, đọc và điền các tham số vào bảng sau:

| Tham số SPICE | Ý nghĩa vật lý | Đơn vị | Giá trị NMOS (Model N) | Giá trị PMOS (Model P) |
| :--- | :--- | :---: | :---: | :---: |
| `LEVEL` | Cấp độ mô hình toán học SPICE | — | .................... | .................... |
| `VTO` | Điện áp ngưỡng không phân cực đế ($V_{GS0}$) | V | .................... | .................... |
| `KP` | Hệ số dẫn suất truyền dẫn ($K' = \mu C_{ox}$) | $\mu\text{A/V}^2$ | .................... | .................... |
| `TOX` | Độ dày lớp oxit điện môi cổng ($t_{ox}$) | m (hoặc nm) | .................... | .................... |
| `GAMMA` | Hệ số hiệu ứng thân (Body effect) | $\text{V}^{1/2}$ | .................... | .................... |
| `VMAX` | Vận tốc bão hòa cực đại của hạt dẫn ($v_{sat}$) | m/s | .................... | .................... |
| `THETA` | Hệ số suy giảm độ linh động theo điện trường dọc | $\text{V}^{-1}$ | .................... | .................... |
| `KAPPA` | Hệ số điều chế chiều dài kênh vùng bão hòa | — | .................... | .................... |

*Câu hỏi phụ:* Trong danh sách tham số của mô hình Level 3 trên, có xuất hiện trực tiếp tham số `LAMBDA` hay không? Tham số nào mô tả hiện tượng điều chế kênh dẫn trong vùng bão hòa?

### P2. Tính toán giải tích tỉ số $(W_p/W_n)$ và điểm chuyển mạch $V_M$
Cho các tham số danh định công nghệ C5N: $V_{DD} = 5,0\,\text{V}$, $V_{thn} = 0,70\,\text{V}$, $|V_{thp}| = 0,80\,\text{V}$, $K_n' = 120\,\mu\text{A/V}^2$, $K_p' = 40\,\mu\text{A/V}^2$.
1. Tính tỉ số định kích thước chính xác $\left[\frac{(W/L)_p}{(W/L)_n}\right]_{\text{target}}$ để điện áp chuyển mạch đối xứng đồng bộ $V_M = V_{DD}/2 = 2,50\,\text{V}$.
2. Với chiều dài kênh chuẩn $L_n = L_p = 2\lambda_{DR} = 0,60\,\mu\text{m}$, chọn $W_n = 4\lambda_{DR} = 1,20\,\mu\text{m}$ và $W_p = 12\lambda_{DR} = 3,60\,\mu\text{m}$ (tỉ số nguyên $W_p/W_n = 3,0$ theo chuẩn lưới):
   - Tính hệ số sức mạnh độ dẫn $r = \frac{k_p}{k_n}$.
   - Tính điện áp chuyển mạch lý thuyết $V_M$ tương ứng và xác định độ lệch (theo mV và theo phần trăm) so với mốc $2,50\,\text{V}$.

### P3. Ước lượng điện trở dẫn $R_{on}$ và thời gian trễ
1. Tính điện trở dẫn hiệu dụng ở vùng triode sâu ($V_{DS} \to 0$ khi mở sâu) của NMOS ($W_n = 1,2\,\mu\text{m}$) và PMOS ($W_p = 3,6\,\mu\text{m}$) theo công thức ở Mục 3.3.
2. Với tải dung chuẩn $C_L = 50\,\text{fF}$, ước lượng trễ lý thuyết $t_{pHL}, t_{pLH}$ và $t_{pd}$ theo mô hình Elmore $0,69 \cdot R_{on} \cdot C_L$.
3. **Dự đoán:** Khi đo đạc thực tế trên LTspice, thời gian trễ thu được sẽ *lớn hơn* hay *nhỏ hơn* giá trị ước lượng $0,69 \cdot R_{on} \cdot C_L$ này? Giải thích lý do vật lý ngắn gọn trong 1–2 câu.

### P4. Thiết kế sơ đồ que (Stick Diagram)
Vẽ sơ đồ que của tế bào CMOS Inverter lên giấy kẻ ô ly (dựa trên cấu trúc đường Euler tại Hình 1.1 và các quy tắc SCMOS tại Mục 3.5). Yêu cầu bổ sung ràng buộc thiết kế:
- Thanh nguồn $V_{DD}$ và $GND$ chạy ngang bằng Metal 1 (độ rộng $6\lambda_{DR}$).
- Dải Poly ngõ vào `in` chạy dọc cắt qua P-Active và N-Active.
- Dây ngõ ra `out` bằng Metal 1 dẫn sang phía bên phải của tế bào.
- Thể hiện đầy đủ vị trí các tiếp xúc Contact và tiếp xúc bảo vệ Taps ($N^+$-tap nối $V_{DD}$, $P^+$-tap nối $GND$).

### P5. Chuẩn bị khung Netlist SPICE
Điền các giá trị thích hợp vào chỗ trống `____` trong đoạn netlist SPICE dưới đây để sẵn sàng mô phỏng quá độ:

```spice
* Netlist CMOS Inverter - MOSIS C5N 0.5um
.include C5_models.txt
.param Vdd=5.0
.param CL_val=50f

* Nguon cap va kich thich xung
Vdd vdd 0 DC {Vdd}
Vin in  0 PULSE(0 {Vdd} 0 100p 100p 9.9n 20n)

* Transistor PMOS va NMOS
MP out in vdd vdd P L=0.6u W=____
MN out in 0   0   N L=0.6u W=____

* Tai dung ngo ra
CL out 0 {CL_val}

* Phan tich qua do va cau lenh do tre tu dong
.tran 0 50n 0 1p
.meas TRAN tpHL TRIG V(in)={0.5*Vdd} RISE=1 TARG V(out)={0.5*Vdd} FALL=1
.meas TRAN tpLH TRIG V(in)={0.5*Vdd} FALL=1 TARG V(out)={0.5*Vdd} RISE=1
.meas TRAN tpd  PARAM (tpHL + tpLH)/2
.meas TRAN trise TRIG V(out)={0.1*Vdd} RISE=1 TARG V(out)={0.9*Vdd} RISE=1
.meas TRAN tfall TRIG V(out)={0.9*Vdd} FALL=1 TARG V(out)={0.1*Vdd} FALL=1
.end
```

### P6. Dự đoán lề nhiễu logic (Noise Margins)
Bằng mô hình giải tích bậc hai, hãy dự đoán các giá trị điện áp $V_{IL}, V_{IH}$ (tại điểm có đạo hàm $\frac{dV_{out}}{dV_{in}} = -1$) và tính các lề nhiễu logic $NM_L = V_{IL} - V_{OL}$, $NM_H = V_{OH} - V_{IH}$ (với $V_{OL} = 0\,\text{V}, V_{OH} = 5,0\,\text{V}$). Dự đoán $NM_L$ và $NM_H$ giá trị nào lớn hơn?

### P7. Ước lượng điện dung ngõ vào $C_{in}$
Dựa vào chiều dày oxit cổng $T_{ox}$ tra được ở P1 ($T_{ox} = 9,5\,\text{nm}$), hãy tính điện dung đơn vị $C_{ox} = \frac{\varepsilon_{ox}}{T_{ox}}$ (với $\varepsilon_{ox} \approx 3,45 \times 10^{-11}\,\text{F/m}$). Ước lượng tổng điện dung cổng ngõ vào của Inverter:
$$C_{in} \approx C_{ox} \cdot (W_n L_n + W_p L_p)$$

---

## 5. KẾ HOẠCH PHÂN BỔ THỜI LƯỢNG IN-LAB (135 PHÚT)

| Phân đoạn | Thời lượng | Nội dung hoạt động chính | Sản phẩm nghiệm thu tại chỗ |
| :--- | :---: | :--- | :--- |
| **1. Cổng kiểm tra Pre-lab** | 10 phút | Kiểm tra bài chuẩn bị P1–P7 tại bàn; khởi tạo thư mục `lab01_MSSV_HoTen/`. | Ký xác nhận bài Pre-lab. |
| **2. Ex1.1: Đặc tính I-V MOSFET** | 25 phút | Quét DC hai biến trên LTspice; trích xuất đặc tuyến ra, $V_{th}$ và $\lambda_{CLM}$. | Đồ thị họ đặc tuyến NMOS/PMOS. |
| **3. Ex1.2: Schematic & VTC** | 25 phút | Dựng Schematic trên Electric, xuất netlist sang LTspice; đo $V_M, NM_L, NM_H$. | Đồ thị VTC kèm đường đạo hàm. |
| **4. Ex1.3: Đo trễ với `.meas`** | 20 phút | Quét trễ ở 3 mức tải dung ($10\,\text{fF}, 50\,\text{fF}, 100\,\text{fF}$); đọc SPICE Error Log. | Bảng số liệu trễ 3 mức tải. |
| **5. Ex1.4: Mask Layout & LVS** | 45 phút | Vẽ Layout trong Electric; chạy DRC (`F5`) đạt 0 lỗi; chạy LVS (NCC) đạt MATCH. | Ảnh DRC 0 lỗi, NCC MATCH. |
| **6. Tổng kết & Nghiệm thu** | 10 phút | Kiểm tra chéo số liệu, vấn đáp nhanh tại bàn; hướng dẫn nộp bài. | Phiếu nghiệm thu thực hành. |

*(Lưu ý: Thao tác đóng gói Icon View và bài tập Ex1.5 PEX được chuyển sang phần bài tập hoàn thiện Post-lab để đảm bảo quỹ thời gian 135 phút tại lớp).*

---

## 6. NỘI DUNG THỰC HÀNH TẠI LỚP (PHẦN A)

### Ex1.1 — Khảo sát đặc tính I-V của NMOS và PMOS trên LTspice
*(Thời lượng: 25 phút | Hình thức: Sinh viên thực hành độc lập dưới sự hướng dẫn)*

**1. Mục đích:** Trích xuất họ đặc tuyến $I_{DS}-V_{DS}$, đặc tuyến truyền dẫn $I_{DS}-V_{GS}$, đo điện áp ngưỡng $V_{th}$ và hệ số điều chế kênh $\lambda_{CLM}$.

**2. Các bước thực hiện:**
1. Tạo schematic mới trong LTspice lưu tên `ex01_nmos_iv.asc`. Đặt linh kiện `nmos4`, đặt tên Model là **`N`**, $L = 0.6\,\mu\text{m}$ (`0.6u`), $W = 1.2\,\mu\text{m}$ (`1.2u`). Nối cực Source (S) và Bulk (B) xuống đất `0`.
2. Đặt nguồn $V_{DS}$ nối vào Drain, nguồn $V_{GS}$ nối vào Gate. Chèn câu lệnh `.include C5_models.txt`.
3. **Khảo sát đặc tuyến ra $I_{DS}-V_{DS}$:**
   - Lệnh mô phỏng: `.dc VDS 0 5 0.01 VGS 1 5 1`.
   - Nhấn **Run**, đưa que đo vào cực Drain `Id(M1)` để hiển thị họ 5 đường đặc tuyến.
   - **Đo hệ số $\lambda_{CLM}$ trong vùng bão hòa:** Chọn đường cong $V_{GS} = 3,0\,\text{V}$ (tại đây điện áp bão hòa $V_{DS,sat} \approx 2,3\,\text{V}$). Dùng con trỏ chuột chọn 2 điểm trong vùng bão hòa sâu: điểm 1 tại $V_{DS1} = 3,0\,\text{V}$ (đọc $I_1$) và điểm 2 tại $V_{DS2} = 5,0\,\text{V}$ (đọc $I_2$).
   - Tính hệ số điều chế kênh chính xác theo công thức:
     $$\lambda_{CLM} = \frac{I_2 - I_1}{I_1 V_{DS2} - I_2 V_{DS1}}$$
4. **Khảo sát đặc tuyến truyền dẫn $I_{DS}-V_{GS}$ và đo $V_{thn}$:**
   - Cố định $V_{DS} = 5,0\,\text{V}$, đổi lệnh mô phỏng: `.dc VGS 0 5 0.01`.
   - Thêm đường cong căn bậc hai dòng điện: gõ biểu thức `sqrt(Id(M1))`.
   - Tìm giao điểm của tiếp tuyến đoạn dốc với trục hoành để trích xuất $V_{thn}$.
   - *(Mở rộng)* Đổi $V_{DS} = 0,1\,\text{V}$ (vùng tuyến tính) để trích xuất $V_{thn}$ bằng ngoại suy tuyến tính, so sánh với phương pháp $\sqrt{I_D}$.
5. **Khảo sát đặc tuyến PMOS (`ex01_pmos_iv.asc`):**
   - Dùng linh kiện `pmos4`, Model = **`P`**, $L = 0.6\,\mu\text{m}$, $W = 3.6\,\mu\text{m}$.
   - Nối cực Source và Bulk lên nguồn $V_{DD} = 5,0\,\text{V}$. Cực Gate nối nguồn $V_G$, cực Drain nối nguồn $V_D$.
   - Quét điện áp để quan sát đặc tuyến $|I_D| - |V_{DS}|$, trích xuất $V_{thp}$ và dòng bão hòa cực đại.

**3. Sản phẩm nghiệm thu Ex1.1:**
- Sơ đồ mạch `ex01_nmos_iv.asc` và `ex01_pmos_iv.asc`.
- Dạng sóng họ đặc tuyến $I_{DS}-V_{DS}$ và đặc tuyến $\sqrt{I_{DS}}-V_{GS}$.
- Bảng tổng hợp số đo thực nghiệm: $V_{thn}, V_{thp}, \lambda_{CLM}, I_{DS,sat(n)}, I_{DS,sat(p)}$.
- **Câu hỏi kiểm tra:** So sánh giá trị dòng bão hòa $I_{DS,sat}$ đo được của NMOS ($W=1,2\,\mu\text{m}$) và PMOS ($W=3,6\,\mu\text{m}$) ở $5\,\text{V}$. Đối chiếu với dự đoán bậc hai và giải thích nguyên nhân chênh lệch?

---

### Ex1.2 — Thiết kế Schematic CMOS Inverter và phân tích đặc tuyến VTC
*(Thời lượng: 25 phút | Hình thức: Giảng viên hướng dẫn, sinh viên thực hành)*

**1. Mục đích:** Xây dựng sơ đồ nguyên lý tế bào `inv_x1` trên Electric VLSI, xuất netlist sang LTspice để quét DC, xác định điểm chuyển mạch $V_M$ và các mức lề nhiễu logic.

**2. Các bước thực hiện:**
1. Khởi động Electric VLSI, mở thư viện `lab_vlsi.jelib` (hoặc tạo mới trong thư mục `lab01_MSSV_HoTen/`).
2. Tạo cell mới: Cell Name: `inv_x1`, View: `schematic`.
3. Đặt linh kiện và cấu hình kích thước:
   - 1 PMOS: $W = 12\lambda_{DR}$ ($3,6\,\mu\text{m}$), $L = 2\lambda_{DR}$ ($0,6\,\mu\text{m}$).
   - 1 NMOS: $W = 4\lambda_{DR}$ ($1,2\,\mu\text{m}$), $L = 2\lambda_{DR}$ ($0,6\,\mu\text{m}$).
4. Đi dây nối cực Cổng chung làm ngõ vào `in`, cực Máng chung làm ngõ ra `out`. Nối cực Nguồn PMOS lên `vdd`, cực Nguồn NMOS xuống `gnd`.
5. Tạo các chân giao tiếp (Export Ports): `in` (Input), `out` (Output), `vdd` (Power), `gnd` (Ground). Lưu ý gõ chính xác chữ thường.
6. Kiểm tra quy tắc điện tử: chọn menu **Tools $\to$ ERC $\to$ Check Electrical Rules** (đảm bảo không có lỗi hở dây hoặc ngắn mạch).
7. Xuất netlist SPICE: chọn menu **Tools $\to$ Simulation (Spice) $\to$ Write Spice Deck**, lưu tệp `inv_vtc.sp`.
8. Mở netlist trong trình soạn thảo hoặc LTspice. Bổ sung các lệnh nguồn kích thích và lệnh phân tích:
   ```spice
   * Khung lenh dieu khien mo phong VTC
   .include C5_models.txt
   Vdd vdd 0 DC 5.0
   Vin in  0 DC 2.5
   .dc Vin 0 5 0.002
   ```
9. Chạy mô phỏng trong LTspice, vẽ đồ thị $V_{out} = f(V_{in})$. Dùng con trỏ xác định giao điểm $V_{out} = V_{in}$ để đọc điện áp chuyển mạch $V_M$.
10. Thêm một khung đồ thị mới (**Add Plot Pane**), gõ biểu thức đạo hàm `d(V(out))/d(V(in))`. Dùng con trỏ tìm hai điểm có độ dốc bằng đúng $-1,00$:
    - Điểm thứ nhất ($V_{in} < V_M$): đọc điện áp $V_{IL}$.
    - Điểm thứ hai ($V_{in} > V_M$): đọc điện áp $V_{IH}$.
    - Đọc $V_{OL}$ (tại $V_{in} = 5\,\text{V}$) và $V_{OH}$ (tại $V_{in} = 0\,\text{V}$).
    - Tính lề nhiễu logic: $NM_L = V_{IL} - V_{OL}$ và $NM_H = V_{OH} - V_{IH}$.

**3. Sản phẩm nghiệm thu Ex1.2:**
- Sơ đồ nguyên lý `inv_x1{sch}` trong Electric VLSI.
- Tệp Netlist `inv_vtc.sp`.
- Đồ thị đặc tuyến VTC kèm đường đạo hàm dốc $-1$.
- Bảng thông số: $V_M, V_{IL}, V_{IH}, V_{OL}, V_{OH}, NM_L, NM_H$.
- **Câu hỏi kiểm tra:** Điện áp chuyển mạch $V_M$ đo được lệch bao nhiêu mV so với mốc $2,50\,\text{V}$ và so với dự đoán Pre-lab? Nguyên nhân vật lý của sự sai khác này là gì?

---

### Ex1.3 — Mô phỏng quá độ Transient & trích xuất trễ bằng lệnh `.meas`
*(Thời lượng: 20 phút | Hình thức: Sinh viên thực hành độc lập)*

**1. Mục đích:** Đo chính xác các thông số động học trễ ($t_{pHL}, t_{pLH}, t_{pd}, t_r, t_f$) bằng lệnh `.meas` tự động ở các mức tải dung khác nhau.

**2. Các bước thực hiện:**
1. Tạo tệp mô phỏng mới `inv_tran.asc` (hoặc sửa trên netlist từ Ex1.2).
2. Cấu hình nguồn xung tại ngõ vào `in`:
   ```spice
   Vin in 0 PULSE(0 5.0 0 100p 100p 9.9n 20n)
   ```
3. Đặt tải dung ngõ ra: ban đầu đặt $C_L = 50\,\text{fF}$ (`50f`).
4. Thiết lập lệnh phân tích và khối đo tự động tham số hóa:
   ```spice
   .param Vdd=5.0
   .tran 0 50n 0 1p
   .meas TRAN tpHL TRIG V(in)={0.5*Vdd} RISE=1 TARG V(out)={0.5*Vdd} FALL=1
   .meas TRAN tpLH TRIG V(in)={0.5*Vdd} FALL=1 TARG V(out)={0.5*Vdd} RISE=1
   .meas TRAN tpd  PARAM (tpHL + tpLH)/2
   .meas TRAN trise TRIG V(out)={0.1*Vdd} RISE=1 TARG V(out)={0.9*Vdd} RISE=1
   .meas TRAN tfall TRIG V(out)={0.9*Vdd} FALL=1 TARG V(out)={0.1*Vdd} FALL=1
   ```
5. Nhấn **Run**. Mở **View $\to$ SPICE Error Log** (`Ctrl + L`) để đọc các kết quả đo tự động.
6. **Khảo sát quét tải dung:** Thêm lệnh quét tham số tải:
   ```spice
   .step param CL list 10f 50f 100f
   ```
   Chạy lại mô phỏng và lập bảng ghi nhận các giá trị trễ tại 3 mức tải.

**3. Sản phẩm nghiệm thu Ex1.3:**
- Dạng sóng chuyển mạch $V_{in}(t)$ và $V_{out}(t)$ tại $C_L = 50\,\text{fF}$.
- Bảng trích xuất số liệu trễ ở 3 mức tải dung ($10\,\text{fF}, 50\,\text{fF}, 100\,\text{fF}$).
- **Câu hỏi kiểm tra:** Lấy số đo $t_{pd}$ tại $C_L = 50\,\text{fF}$ chia cho giá trị giải tích $0,69 \cdot R_{on} \cdot C_L$ tính ở Pre-lab. Tỉ số này bằng bao nhiêu và hãy giải thích bản chất vật lý vì sao có sự chênh lệch đó?

---

### Ex1.4 — Thiết kế Mask Layout, kiểm tra DRC & đối chiếu LVS (NCC)
*(Thời lượng: 45 phút | Hình thức: Sinh viên thực hiện, Giảng viên hỗ trợ)*

**1. Mục đích:** Vẽ mặt nạ vật lý hoàn chỉnh cho tế bào `INV_X1`, kiểm tra luật hình học DRC đạt 0 lỗi và đối chiếu sơ đồ logic LVS đạt trạng thái MATCH.

**2. Các bước thực hiện:**
1. Trong Electric VLSI, mở cell `inv_x1`, tạo view mới: View: `layout`.
2. Vẽ hai thanh ray nguồn nằm ngang bằng lớp Metal 1, độ rộng chuẩn **$6\lambda_{DR} = 1,80\,\mu\text{m}$**:
   - Thanh trên tạo Export port tên `vdd` (loại Power).
   - Thanh dưới tạo Export port tên `gnd` (loại Ground).
   - Khoảng cách giữa hai ray xác lập chiều cao khung tế bào chuẩn **$H_{cell} = 40\lambda_{DR} = 12,0\,\mu\text{m}$**.
3. **Bố trí vùng n-well và transistor PMOS (nửa trên):**
   - Đặt vùng N-Well bao bọc nửa trên tế bào.
   - Đặt linh kiện transistor PMOS (hoặc dải P-Active) kích thước $W = 12\lambda_{DR} = 3,60\,\mu\text{m}$, $L = 2\lambda_{DR} = 0,60\,\mu\text{m}$.
   - Đặt tiếp xúc $N^+$-tap trong N-Well và nối lên thanh ray `vdd`.
   - Nối cực Source của PMOS lên thanh ray `vdd`.
4. **Bố trí transistor NMOS (nửa dưới):**
   - Đặt linh kiện transistor NMOS (hoặc dải N-Active) kích thước $W = 4\lambda_{DR} = 1,20\,\mu\text{m}$, $L = 2\lambda_{DR} = 0,60\,\mu\text{m}$.
   - Đặt tiếp xúc $P^+$-tap trên chất nền P-Substrate và nối xuống thanh ray `gnd`.
   - Nối cực Source của NMOS xuống thanh ray `gnd`.
5. **Đấu nối cực cổng và cực má:**
   - Dùng dải Polysilicon ($2\lambda_{DR}$) nối thẳng hàng từ PMOS xuống NMOS làm cổng chung. Phần vươn Poly qua mép Active (Gate Overhang) phải $\ge 2\lambda_{DR} = 0,60\,\mu\text{m}$. Gán Export port tên `in` (loại Input).
   - Nối chung cực Drain của PMOS và NMOS bằng đường Metal 1 ($3\lambda_{DR}$), tạo Export port tên `out` (loại Output).
6. **Kiểm tra luật hình học DRC:**
   - Nhấn phím **`F5`** (hoặc menu **Tools $\to$ DRC $\to$ Check Hierarchical**).
   - Quan sát thanh thông báo ở đáy màn hình. Nếu có vệt kẻ báo lỗi, phóng to kiểm tra khoảng cách và sửa cho đến khi thông báo: **`0 errors found`** (hoặc `No errors found`).
7. **Đối chiếu sơ đồ nguyên lý và layout LVS (NCC):**
   - Chọn menu **Tools $\to$ NCC $\to$ Schematic and Layout Comparison**.
   - Kiểm tra cửa sổ thông báo của Electric. Kết quả đạt chuẩn khi xuất hiện dòng chữ:  
     **`Cells are topologically equivalent (MATCH)`**.

**3. Sản phẩm nghiệm thu Ex1.4:**
- Bản vẽ Mask Layout hoàn chỉnh của cell `inv_x1{lay}` trong Electric.
- Ảnh chụp thông báo kiểm tra DRC đạt 0 lỗi.
- Ảnh chụp cửa sổ thông báo NCC so sánh LVS đạt trạng thái MATCH.
- **Câu hỏi kiểm tra:** Nếu ta bỏ quên tiếp xúc $N^+$-tap hoặc $P^+$-tap, công cụ DRC và LVS sẽ thông báo ra sao? Hậu quả nghiêm trọng nhất trên chip chế tạo thực tế là gì?

---

## 7. HƯỚNG DẪN HOÀN THIỆN SAU BUỔI HỌC (POST-LAB)

### 1. Đóng gói Icon View & Phân tích trích xuất ký sinh PEX
1. **Tạo Icon View (`inv_x1{ic}`):** Trong Electric, mở cell `inv_x1`, chọn menu **View $\to$ Make Icon View**. Chỉnh sửa biểu tượng cổng đảo chuẩn với đủ 4 chân giao tiếp (`in`, `out`, `vdd`, `gnd`).
2. **Trích xuất ký sinh PEX (Ex1.5 nâng cao):**
   - Trong cửa sổ layout của `inv_x1`, chọn **Tools $\to$ Simulation (Spice) $\to$ Write Spice Deck**, lưu netlist dạng PEX `inv_x1_pex.sp` (chọn trích xuất điện dung và điện trở ký sinh).
   - Mở tệp netlist PEX, quan sát các tham số hình học khuếch tán (`AS, AD, PS, PD`) và các phần tử tụ ký sinh dây nối.
   - Thêm nguồn kích thích và tụ tải $C_L = 50\,\text{fF}$ giống Ex1.3, chạy mô phỏng quá độ để đo các thông số trễ Post-layout: $t_{pHL,post}, t_{pLH,post}, t_{pd,post}$.
   - Tính toán phần trăm suy giảm tốc độ hậu thiết kế:
     $$\Delta t_{pd} (\text{pct}) = \frac{t_{pd,post} - t_{pd,pre}}{t_{pd,pre}} \times 100\text{ pct}$$

### 2. Trả lời các câu hỏi phân tích Post-lab
1. **Thiết kế kích thước đối xứng $W_p = W_n = 4\lambda_{DR}$:**  
   Nếu nhà thiết kế chọn $W_p = W_n = 1,2\,\mu\text{m}$ để tiết kiệm diện tích:  
   - Hãy tính điểm $V_M$ lý thuyết mới và nhận xét sự dịch chuyển của đặc tuyến VTC? Lề nhiễu nào bị suy giảm mạnh?  
   - Tỉ số trễ $t_{pLH} / t_{pHL}$ thay đổi ra sao? Trong ứng dụng nào thì thiết kế này có thể chấp nhận được?
2. **Cơ chế vật lý của tụ ký sinh khuếch tán:**  
   Dựa vào các tham số trích xuất (`AS, AD, PS, PD`), giải thích nguồn gốc vật lý của tụ cực má $C_{db}$. Tại sao khi kéo tải ngoài rất lớn ($C_L = 1\,\text{pF}$), sự chênh lệch trễ giữa Pre-layout và Post-layout lại trở nên không đáng kể?
3. **Cơ chế bảo vệ của Guard Rings:**  
   Giải thích vì sao việc bao bọc các transistor bằng dải bảo vệ liên tục (Guard Rings) lại ngăn chặn hiện tượng Latch-up hiệu quả hơn việc chỉ đặt một vài nốt tiếp xúc Tap rời rạc?

### 3. Cấu trúc thư mục nộp bài (`lab01_MSSV_HoTen/`)
```
lab01_MSSV_HoTen/
│
├── schematics/             # Các tệp mô phỏng schematic (.asc)
│   ├── ex01_nmos_iv.asc
│   ├── ex01_pmos_iv.asc
│   ├── inv_vtc.asc
│   └── inv_tran.asc
│
├── netlists/               # Các tệp Netlist SPICE trích xuất (.sp)
│   ├── inv_vtc.sp
│   ├── inv_tran.sp
│   └── inv_x1_pex.sp
│
├── waveforms/              # Ảnh chụp dạng sóng và kết quả đo
│   ├── ex01_iv_curves.png
│   ├── ex02_vtc_plot.png
│   ├── ex03_tran_plot.png
│   ├── ex04_drc_clean.png
│   └── ex04_ncc_match.png
│
├── lab_vlsi.jelib          # Thư viện Electric VLSI chứa cell inv_x1 (sch, ic, lay)
├── C5_models.txt           # Thư viện mô hình công nghệ
└── Bao_Cao_Lab01_MSSV.pdf  # Báo cáo kỹ thuật tổng kết (từ 3 đến 4 trang)
```

---

## 8. BẢNG KIỂM CHỨNG VÀ ĐỐI CHUẨN KỸ THUẬT

Sinh viên tổng hợp toàn bộ kết quả đo đạc và kiểm chứng vào bảng đối chuẩn sau (tại mức tải chuẩn $C_L = 50\,\text{fF}$):

| Đại lượng kỹ thuật | [1] Dự đoán Pre-lab | [2] Đo đạc Pre-layout | [3] Đo đạc Post-layout | So với Benchmark GV ([2] vs Benchmark) | So với Lý thuyết 0,69RC ([2] vs [1]) | Ngưỡng nghiệm thu |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Điện áp chuyển mạch $V_M$** | ................. V | ................. V | ................. V | — | Sai lệch: ........... % | $\le 3$% so với Pre-lab |
| **Lề nhiễu mức thấp $NM_L$** | ................. V | ................. V | ................. V | — | — | Đạt tiêu chuẩn thiết kế |
| **Lề nhiễu mức cao $NM_H$** | ................. V | ................. V | ................. V | — | — | Đạt tiêu chuẩn thiết kế |
| **Trễ sườn xuống $t_{pHL}$** | ................. ps | ................. ps | ................. ps | Sai lệch: ........... % | Tỉ số đo / 0,69RC: ....... | $\le 20$% so với Benchmark GV |
| **Trễ sườn lên $t_{pLH}$** | ................. ps | ................. ps | ................. ps | Sai lệch: ........... % | Tỉ số đo / 0,69RC: ....... | $\le 20$% so với Benchmark GV |
| **Trễ trung bình $t_{pd}$** | ................. ps | ................. ps | ................. ps | Sai lệch: ........... % | Tỉ số đo / 0,69RC: ....... | $\le 20$% so với Benchmark GV |

*Lưu ý:* Giá trị Benchmark của Giảng viên được công bố trong cẩm nang hướng dẫn Teacher's Book. Phép so sánh với mô hình $0,69 \cdot R_{on} \cdot C_L$ dùng để đánh giá năng lực phân tích bản chất vật lý (quá trình xả qua vùng bão hòa), không dùng làm tiêu chí đạt/trượt kỹ thuật.

---

## 9. HƯỚNG DẪN TỰ CHẨN ĐOÁN LỖI THƯỜNG GẶP

| Hiện tượng lỗi | Nguyên nhân cốt lõi | Hướng tự kiểm tra và xử lý |
| :--- | :--- | :--- |
| **NCC báo "Netlists do NOT match"** | Sai lệch tên chân Export giữa Schematic và Layout (do Electric phân biệt hoa/thường). | Kiểm tra và chuẩn hóa tên chân trên cả 2 view: `in`, `out`, `vdd`, `gnd` đồng nhất chữ thường. |
| **DRC báo lỗi khoảng cách Poly hoặc N-Well** | Vẽ dải Poly quá sát Contact ($< 2\lambda$) hoặc N-Well không bao trọn P-Active ($< 6\lambda$). | Bật hiển thị Grid, căn chỉnh các dải theo bội số của $\lambda_{DR} = 0,30\,\mu\text{m}$. |
| **Đồ thị VTC dốc ngược hoặc không đổi mức** | Nhầm lẫn chân Source/Drain PMOS hoặc Bulk PMOS nối nhầm xuống `gnd`. | Kiểm tra sơ đồ: Bulk PMOS luôn lên `vdd`, Bulk NMOS luôn xuống `gnd`. |
| **Lệnh `.meas` báo lỗi FAIL trong Error Log** | Mức điện áp đo đặt sai ngưỡng hoặc chu kỳ xung quá ngắn mạch chưa chuyển xong. | Kiểm tra cú pháp: `.meas TRAN tpHL TRIG V(in)={0.5*Vdd} ...`; xung chu kỳ $20\,\text{ns}$ đủ dài cho $50\,\text{fF}$. |
| **SPICE báo lỗi trùng lặp model khi chạy deck** | Deck của Electric đã tự chèn model PDK và trong tệp lại có thêm `.include C5_models.txt`. | Mở netlist, kiểm tra và xóa một trong hai định nghĩa model bị trùng lặp. |

---

## 10. RUBRIC ĐÁNH GIÁ (THANG ĐIỂM 10)

| Hạng mục đánh giá | Chuẩn CLO | Điểm | Tiêu chí đạt điểm tối đa |
| :--- | :---: | :---: | :--- |
| **Chuẩn bị Pre-lab (Mục 4)** | **CLO1** | **2.0 điểm** | Điền đủ tham số P1; giải đúng P2 ($W_p/W_n$ và $V_M$); tính đúng $R_{on}$, trễ P3; vẽ Stick diagram P4 có đủ Taps và dải Poly liên tục; netlist P5 hoàn chỉnh; dự đoán P6, P7 hợp lý. |
| **Khảo sát I-V & Phân tích VTC (Ex1.1, Ex1.2)** | **CLO2** | **2.5 điểm** | Quét đúng họ đặc tuyến ra và truyền dẫn; trích xuất chuẩn xác $V_{th}$ và $\lambda_{CLM}$; Schematic đúng quy chuẩn; đo chính xác $V_M$ (sai số $\le 3$% so với Pre-lab), xác định đúng lề nhiễu $NM_L, NM_H$. |
| **Mô phỏng quá độ Transient & Đo trễ (Ex1.3)** | **CLO2** | **2.0 điểm** | Thiết lập nguồn xung đúng chuẩn; dùng thành thạo khối lệnh `.meas` đo đủ 5 thông số ở 3 mức tải dung; sai lệch trễ $\le 20$% so với Benchmark GV; giải thích sắc bén cơ chế sai lệch so với $0,69RC$. |
| **Mask Layout, kiểm tra DRC & LVS (Ex1.4)** | **CLO2, CLO4** | **2.5 điểm** | Vẽ Layout chuẩn theo quy tắc SCMOS Submicron ($H_{cell} = 40\lambda$, ray nguồn $6\lambda$); có đủ tiếp xúc Well Tap và Substrate Tap chống Latch-up; kiểm tra DRC đạt 0 lỗi; NCC đối chiếu LVS đạt **MATCH**. |
| **Đánh giá PEX & Báo cáo Post-lab (Ex1.5, Mục 7)** | **CLO4** | **1.0 điểm** | Trích xuất netlist PEX và đo được độ suy giảm tốc độ; nộp đủ tệp thư viện `lab_vlsi.jelib`; báo cáo kỹ thuật 3–4 trang trình bày mạch lạc, trả lời xuất sắc 3 câu hỏi bản chất vật lý Post-lab. |

---

## 11. TÀI LIỆU THAM KHẢO

1. Neil H. E. Weste, David Money Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th Edition, Addison-Wesley, 2011 (Chương 2: MOS Transistor Theory; Chương 4: Delay).
2. Jan M. Rabaey, Anantha Chandrakasan, Borivoje Nikolic, *Digital Integrated Circuits: A Design Perspective*, 2nd Edition, Prentice Hall, 2003 (Chương 3: The Devices; Chương 5: The Inverter).
3. Steven M. Rubin, *Electric VLSI Design System User's Manual*, Static Free Software, 2017.
4. MOSIS Service, *SCMOS Layout Design Rules (Submicron 0.5 micron C5N Process)*, Information Sciences Institute, University of Southern California.\n