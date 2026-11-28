# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 02 — TEACHER'S BOOK: THIẾT KẾ CỔNG LOGIC TĨNH NAND2 VÀ NOR2 CMOS
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-02-cong-logic-tinh-nand-nor.md](../02%20-%20Student%20Workbook/lab-02-cong-logic-tinh-nand-nor.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab02/](../03%20-%20Instructor_Solutions/lab02/)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda_{DR} = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

# 2. LAB 2 — CỔNG TĨNH NAND2 VÀ NOR2 (CHƯƠNG 6)

## 2.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. **Hiểu bản chất topo mạng đối ngẫu tĩnh:** Mạng kéo xuống (PDN) dùng NMOS thực hiện hàm bù $\bar{Y}$, mạng kéo lên (PUN) dùng PMOS thực hiện hàm $Y$. Phép nối tiếp trong mạng này tương ứng với song song trong mạng kia theo định lý De Morgan.
2. **Nắm vững nguyên tắc định cỡ theo trường hợp xấu nhất (Worst-Case Sizing):** Định cỡ để điện trở kéo tương đương bằng Inverter chuẩn `INV_X1` ($R_{eq,N} \approx 969\,\Omega, R_{eq,P} \approx 992\,\Omega$).
3. **Hiểu rõ bản chất so sánh NAND vs NOR (Bác bỏ hiểu lầm):** Ở cùng tải dung ngoài $C_L = 50\,\text{fF}$, trễ lý thuyết worst-case của NAND2 và NOR2 **bằng nhau** ($\approx 33,8\,\text{ps}$). Ưu thế đáng kể thực sự của NAND nằm ở:
   - Tiết kiệm **+40% tổng diện tích kênh** ($\sum W$: $40\lambda$ vs $56\lambda$).
   - Nhẹ tải hơn **+40% điện dung ngõ vào** ($C_{in}$: $20\lambda$ vs $28\lambda$), không làm chậm tầng lái phía trước.
   - Tránh được hiệu ứng thân (Body Effect) trên chuỗi PMOS nối tiếp vốn làm suy giảm mạnh dòng kéo lên của NOR2.
4. **Giải thích được hiện tượng trễ phụ thuộc vector chuyển mạch (Input-pattern dependency):** Phân tích cơ chế tích lũy điện tích tại nút nội $X_n$. Hiểu vì sao ở tải lớn ($50\,\text{fF}$) độ lệch chỉ $\sim 5$%, nhưng ở tải nhỏ ($10\,\text{fF}$) độ lệch vọt lên tới $\sim 20 - 25$%.
5. **Thành thạo phương pháp đường Euler trên đồ thị dải khuếch tán:** Tìm thứ tự dải Poly chung $A - B$ để thực hiện chia sẻ vùng khuếch tán (Abutment), triệt tiêu các khoảng cắt dải khuếch tán và giảm điện dung ký sinh nút ngõ ra.
6. **Nắm chắc luật hình học DRC:** Khoảng cách giữa 2 dải Poly tại nơi có đặt Contact chia sẻ cực má bắt buộc phải $\ge 6\lambda_{DR} = 1,80\,\mu\text{m}$ (không được nhầm lẫn với khoảng cách ly $3\lambda_{DR}$ ở nơi không có contact).

---

## 2.2 Phân tích Kỹ thuật & Bảng So sánh PPA Chuyên sâu

### a. Suy dẫn Toán học Định cỡ Tương đương Inverter Cơ sở
Cho Inverter chuẩn `INV_X1`:
- $W_{n,inv} = 4\lambda_{DR} = 1,20\,\mu\text{m}$, $W_{p,inv} = 12\lambda_{DR} = 3,60\,\mu\text{m}$, $L = 2\lambda_{DR} = 0,60\,\mu\text{m}$.
- Điện trở dẫn kênh tuyến tính:
  $$R_{on,n0} = \frac{1}{K'_n (W_n/L)_{inv} (V_{DD} - V_{tn0})} = \frac{1}{120\mu \times (1,2/0,6) \times (5,0 - 0,70)} \approx 968,99\,\Omega$$
  $$R_{on,p0} = \frac{1}{K'_p (W_p/L)_{inv} (V_{DD} - |V_{tp0}|)} = \frac{1}{40\mu \times (3,6/0,6) \times (5,0 - 0,80)} \approx 992,06\,\Omega$$

#### 1. Định cỡ Cổng NAND2 ($Y = \overline{A \cdot B}$):
- **Mạng kéo xuống (PDN):** 2 NMOS mắc nối tiếp. Khi cả hai cùng dẫn:
  $$R_{eq,N} = R_{on,NA} + R_{on,NB} = 2 \times \left(\frac{R_{\Box,n}}{W_n / L}
ight) = \frac{R_{\Box,n}}{W_{n,inv} / L}$$
  $$\implies W_n = 2 \times W_{n,inv} = 2 \times 4\lambda_{DR} = \mathbf{8\lambda_{DR} = 2,40\,\mu\text{m}}$$
  *(Mỗi NMOS có điện trở $R_{on,N1} = R_{on,N2} \approx 484,5\,\Omega \implies R_{eq,N} \approx 969,0\,\Omega = R_{on,n0}$)*.
- **Mạng kéo lên (PUN):** 2 PMOS mắc song song. Tình huống bất lợi nhất là chỉ có **1 PMOS dẫn**:
  $$W_p = W_{p,inv} = \mathbf{12\lambda_{DR} = 3,60\,\mu\text{m}} \implies R_{eq,P,worst} = R_{on,p0} \approx 992,1\,\Omega$$
  *(Khi cả 2 PMOS cùng dẫn $A=0, B=0$: $R_{eq,P,best} = R_{on,p0}/2 \approx 496,0\,\Omega$, trễ sườn lên nhanh gấp đôi)*.

#### 2. Định cỡ Cổng NOR2 ($Y = \overline{A + B}$):
- **Mạng kéo xuống (PDN):** 2 NMOS mắc song song. Tình huống bất lợi nhất là chỉ có **1 NMOS dẫn**:
  $$W_n = W_{n,inv} = \mathbf{4\lambda_{DR} = 1,20\,\mu\text{m}} \implies R_{eq,N,worst} = R_{on,n0} \approx 969,0\,\Omega$$
  *(Khi cả 2 NMOS cùng dẫn: $R_{eq,N,best} = R_{on,n0}/2 \approx 484,5\,\Omega$, trễ sườn xuống nhanh gấp đôi)*.
- **Mạng kéo lên (PUN):** 2 PMOS mắc nối tiếp. Bắt buộc cả 2 PMOS phải cùng dẫn:
  $$R_{eq,P} = R_{on,PA} + R_{on,PB} = 2 \times \left(\frac{R_{\Box,p}}{W_p / L}
ight) = R_{on,p0}$$
  $$\implies W_p = 2 \times W_{p,inv} = 2 \times 12\lambda_{DR} = \mathbf{24\lambda_{DR} = 7,20\,\mu\text{m}}$$
  *(Mỗi PMOS có điện trở $R_{on,P1} = R_{on,P2} \approx 496,0\,\Omega \implies R_{eq,P} \approx 992,1\,\Omega = R_{on,p0}$)*.

```
       NAND2 SCHEMATIC                      NOR2 SCHEMATIC
        VDD (5.0V)                           VDD (5.0V)
      +-----+-----+                               |
      |           |                         [PMOS A: 24λ]
  [PMOS A]    [PMOS B] (Mỗi cái 12λ)              |
      |           |                             (Xp)
      +-----+-----+                               |
            |-------- Out                   [PMOS B: 24λ]
            |                                     |
      [NMOS A: 8λ]                                +-------- Out
            |                                     |
           (Xn)                             +-----+-----+
            |                               |           |
      [NMOS B: 8λ]                      [NMOS A]    [NMOS B] (Mỗi cái 4λ)
            |                               |           |
           GND                              +-----+-----+
                                                  |
                                                 GND
```

---

### b. Đối sánh Định lượng PPA: Bản chất Ưu thế Đáng kể của NAND
Bảng tổng hợp đối sánh chuyên sâu dành cho giảng viên phản biện:

| Chỉ số PPA | Cổng Inverter `INV_X1` | Cổng NAND2 (`nand2_x1`) | Cổng NOR2 (`nor2_x1`) | So sánh NOR2 với NAND2 |
| :--- | :---: | :---: | :---: | :---: |
| **Tổng chiều rộng kênh $\sum W$** | $16\lambda_{DR}$ ($4,8\,\mu\text{m}$) | $40\lambda_{DR}$ ($12,0\,\mu\text{m}$) | $56\lambda_{DR}$ ($16,8\,\mu\text{m}$) | NOR2 lớn hơn **+40,0%** |
| **Điện dung ngõ vào Pin A ($C_{in}$)** | $16\lambda_{DR} \cdot C'$ ($1,00\times$) | $20\lambda_{DR} \cdot C'$ ($1,25\times$) | $28\lambda_{DR} \cdot C'$ ($1,75\times$) | NOR2 nặng hơn **+40,0%** |
| **Hệ số Logical Effort ($g$)** | $1,000$ | $1,250$ ($5/4$) | $1,750$ ($7/4$) | NOR2 kém hơn **+40,0%** |
| **Trễ $t_{pd,worst}$ lý thuyết ($C_L = 50\,\text{fF}$)** | $33,8\,\text{ps}$ | $33,8\,\text{ps}$ | $33,8\,\text{ps}$ | **Bằng nhau đồng bộ** |
| **Ảnh hưởng Body Effect** | Không | Không đáng kể ($X_n$ xả) | **Rất nặng** ($V_{SB} > 0$ trên PMOS) | NOR2 bị suy thoái dòng nạp |
| **Tụ ký sinh cực má nút Out ($C_{db}$)** | Nhỏ | $C_{db,N1} + 2C_{db,P}$ | $2C_{db,N} + C_{db,P2} (24\lambda)$ | NOR2 có diện tích khuếch tán lớn hơn |

> [!IMPORTANT]
> **Kết luận sư phạm then chốt:**  
> Đừng bao giờ nói với sinh viên một cách chung chung là *"cổng NAND nhanh hơn cổng NOR"*. Hãy giải thích chính xác:  
> 1. Khi xét riêng một cổng kéo một tải thuần $C_L$ cố định, nếu định cỡ đúng thì tốc độ worst-case của chúng ngang nhau.  
> 2. Nhưng trong một chuỗi logic (Logic Path), cổng NOR2 làm tầng đứng trước nó phải kéo một tụ ngõ vào lớn hơn 40%, khiến tầng trước bị chậm đi 40%. Đồng thời nó chiếm diện tích silicon lớn hơn 40%. Do đó, xét trên toàn hệ thống vi mạch, **mạng dùng cổng NAND luôn nhanh hơn, nhỏ hơn và tiêu thụ năng lượng thấp hơn mạng dùng cổng NOR**.

---

## 2.3 Cơ chế Trễ Nút nội ($X_n$) & Phân tích Giải tích Elmore

### 1. Phân tích Điện áp Tích lũy tại Nút nội
Trong chuỗi 2 NMOS của NAND2, nút nội $X_n$ nằm giữa $M_{NA}$ (gần Out) và $M_{NB}$ (gần GND).
- **Trước khi chuyển mạch (Trạng thái tĩnh $A=1, B=0$):**  
  Ngõ ra $Out$ ở mức cao $V_{DD} = 5,0\,\text{V}$. Transistor $M_{NA}$ dẫn điện, nạp điện tích từ $Out$ vào nút $X_n$.
  Tuy nhiên, điện thế nút $X_n$ không thể đạt tới $5,0\,\text{V}$ vì khi $V(X_n)$ tăng, $V_{GS,NA} = V_A - V(X_n) = 5,0 - V(X_n)$ sẽ giảm dần. Transistor $M_{NA}$ ngắt khi $V_{GS,NA} = V_{tn}(V_X)$:
  $$V(X_n) = V_{DD} - V_{tn}(V(X_n))$$
- **Ảnh hưởng của Hiệu ứng Thân (Body Effect):**
  Cực thân của $M_{NA}$ nối đất $GND = 0\,\text{V}$, cực nguồn là nút $X_n \implies V_{SB} = V(X_n) > 0$.
  $$V_{tn}(V_{SB}) = V_{tn0} + \gamma \left(\sqrt{2\phi_F + V_{SB}} - \sqrt{2\phi_F}
ight)$$
  Với $V_{tn0} = 0,70\,\text{V}, \gamma \approx 0,50\,\text{V}^{1/2}, 2\phi_F \approx 0,60\,\text{V}$:  
  Điện áp ngưỡng tăng lên $V_{tn} \approx 1,1 - 1,3\,\text{V}$.  
  Do đó, điện áp nạp cực đại của nút nội đạt:  
  $$V(X_n) \approx 5,0 - 1,2 \approx \mathbf{3,7 - 3,9\,\text{V}} \quad (\text{không phải } 4,3\,\text{V})$$

### 2. Mô hình Trễ Elmore và Độ Lệch theo Tải Dung
- **Ca 1 (Ngõ vào $A$ kích $0 \to 1$, ngõ $B = 5,0\,\text{V}$ static):**
  $M_{NB}$ đã dẫn từ trước $\implies$ nút $X_n$ đã xả hết điện tích về $0\,\text{V}$. Khi $A$ bật, dòng qua chuỗi chỉ cần rút điện tích từ $C_L$:
  $$t_{pHL(Ca1)} = \ln(2) \cdot (R_{on,NA} + R_{on,NB}) \cdot C_L$$
- **Ca 2 (Ngõ vào $B$ kích $0 \to 1$, ngõ $A = 5,0\,\text{V}$ static):**
  Nút $X_n$ đã tích sẵn điện tích ở điện áp $\approx 3,8\,\text{V}$. Khi $B$ bật, $M_{NB}$ phải xả đồng thời cả $C_L$ và $C_{int}$:
  $$t_{pHL(Ca2)} = \ln(2) \cdot \left[ (R_{on,NA} + R_{on,NB}) C_L + R_{on,NB} C_{int} 
ight]$$
  $$\Delta t_{pHL} = t_{pHL(Ca2)} - t_{pHL(Ca1)} = \ln(2) \cdot R_{on,NB} \cdot C_{int}$$

**Tính toán định lượng:**
Với $R_{on,NB} \approx 484,5\,\Omega$ và tụ nút nội $C_{int} \approx 5,0\,\text{fF}$:
$$\Delta t_{pHL} \approx 0,69315 \times 484,5\,\Omega \times 5,0\,\text{fF} \approx \mathbf{1,68\,\text{ps}}$$

**So sánh phần trăm tăng trễ ở 2 mức tải:**
- **Tại $C_L = 50\,\text{fF}$:**
  $$t_{pHL(Ca1)} \approx 0,69315 \times 969\,\Omega \times 50\,\text{fF} \approx 33,6\,\text{ps}$$
  $$\frac{\Delta t_{pHL}}{t_{pHL(Ca1)}} = \frac{1,68\,\text{ps}}{33,6\,\text{ps}} \times 100\text{ pct} \approx \mathbf{5,0\text{ pct}}$$
  *(Độ lệch 5% rất khó quan sát rõ trên đồ thị mô phỏng do sai số số trị)*.
- **Tại $C_L = 10\,\text{fF}$:**
  $$t_{pHL(Ca1)} \approx 0,69315 \times 969\,\Omega \times 10\,\text{fF} \approx 6,72\,\text{ps}$$
  $$\frac{\Delta t_{pHL}}{t_{pHL(Ca1)}} = \frac{1,68\,\text{ps}}{6,72\,\text{ps}} \times 100\text{ pct} \approx \mathbf{25,0\text{ pct}}$$
  *(Độ lệch 25% hiển thị vô cùng rõ nét! Đây là lý do vì sao bài thực hành yêu cầu đo ở cả hai mức tải $50\,\text{fF}$ và $10\,\text{fF}$)*.

---

## 2.4 Phương pháp Đường đi Euler & Luật Hình học Layout

### a. Đồ thị Euler & Thứ tự Cổng $A - B$
1. **Đồ thị PUN:** 2 PMOS mắc song song giữa $V_{DD}$ và $Out$. Hai cạnh $A$ và $B$ nối chung giữa 2 nút $V_{DD}$ và $Out$.
2. **Đồ thị PDN:** 2 NMOS mắc nối tiếp giữa $Out$ và $GND$ qua nút trung gian $X_n$. Cạnh $A$ nối giữa $Out - X_n$; cạnh $B$ nối giữa $X_n - GND$.
3. **Chu trình Euler chung:** Đi theo thứ tự biến cổng **$A - B$** (hoặc $B - A$).

```
                  SƠ ĐỒ BỐ TRÍ DẢI KHUẾCH TÁN LIỀN MẠCH (ABUTMENT)
        VDD (Metal 1) ──────────────────────────────────────────────────
                       │ (Contact)                   │ (Contact)
                  ┌────┴─────────────────────────────┴────┐
                  │          P-Active (12λ)               │ (N-Well)
                  └────┬──────────────┬──────────────┬────┘
                       │              │              │
                       │ (Gate A)     │ (Out Contact)│ (Gate B)
                       │              │              │
        Ngõ vào A ─────┼──────────────┼──────────────┼──────────────
                       │              │              │
        Ngõ vào B ─────┼──────────────┼──────────────┼──────────────
                       │              │              │
                       │ (Gate A)     │              │ (Gate B)
                  ┌────┴──────────────┴──────────────┴────┐
                  │ (Out)            (Xn: Abutted)   (GND)│ N-Active (8λ)
                  └────┬─────────────────────────────┬────┘
                       │ (Contact)                   │ (Contact)
                      Out (Metal 1)                 GND (Metal 1)
```

### b. Giải thích Luật Khoảng cách Poly-to-Poly $\ge 6\lambda_{DR}$
Giảng viên cần chỉ rõ trên bảng:
- Khi có một tiếp xúc Contact nằm giữa hai dải Polysilicon (chân ngõ ra `out`):
  * Bề rộng tiếp xúc Contact kim loại: $2\lambda_{DR} = 0,60\,\mu\text{m}$.
  * Khoảng cách tối thiểu từ mép Contact tới mép Poly (Rule 3.2.b): $\ge 2\lambda_{DR} = 0,60\,\mu\text{m}$.
  * Do đó, khoảng cách tâm-tâm giữa hai mép Poly là:
    $$S_{poly-poly} = 2\lambda_{DR} \text{ (Poly-Contact)} + 2\lambda_{DR} \text{ (Contact)} + 2\lambda_{DR} \text{ (Contact-Poly)} = \mathbf{6\lambda_{DR} = 1,80\,\mu\text{m}}$$
- Sinh viên thường mắc lỗi lấy luật cách ly Poly tối thiểu $3\lambda_{DR} = 0,90\,\mu\text{m}$ (Rule 3.2.a áp dụng cho 2 dải Poly chạy song song không có gì ở giữa) đặt vào vị trí có Contact $\implies$ Gây lỗi chạm DRC nghiêm trọng!

---

## 2.5 Suy dẫn Giải tích Ngưỡng Chuyển mạch $V_M$

Tại ngưỡng chuyển mạch $V_{in} = V_{out} = V_M$, các transistor đều hoạt động ở vùng bão hòa.

### 1. Trường hợp 1 ngõ vào quét ($B = 5,0\,\text{V}$ static, quét ngõ $A$):
- Cực cổng $M_{PB}$ nối $5\,\text{V} \implies M_{PB}$ ngắt hoàn toàn ($V_{GS,PB} = 0$). Chỉ có $M_{PA}$ tham gia kéo lên với $W_p = 12\lambda$.
- Cực cổng $M_{NB}$ nối $5\,\text{V} \implies M_{NB}$ dẫn mạnh ở vùng tuyến tính sâu như một điện trở nhỏ. Transistor $M_{NA}$ dẫn bão hòa với kích thước tương đương chuỗi là $W_{n,eq} = 4\lambda$.
- Tỉ số độ dẫn dòng:
  $$r = \frac{\beta_p}{\beta_n} = \frac{K'_p (W_p/L)}{K'_n (W_n/L)_{eq}} = \frac{40\mu \times (12/2)}{120\mu \times (4/2)} = \frac{240\mu}{240\mu} = \mathbf{1,00}$$
- Áp dụng công thức ngưỡng:
  $$V_M = \frac{V_{tn} + \sqrt{r}(V_{DD} - |V_{tp}|)}{1 + \sqrt{r}} = \frac{0,70 + 1,0 \times (5,0 - 0,80)}{2} = \mathbf{2,450\,\text{V}}$$

### 2. Trường hợp 2 ngõ vào nối chung quét đồng thời ($A = B = V_{in}$):
- Cả hai PMOS cùng dẫn song song kéo lên: $\beta_p$ tăng gấp đôi:
  $$\beta_p = 2 \times [K'_p (12/2)] = 2 \times 240\mu = 480\,\mu\text{A/V}^2$$
- Hai NMOS nối tiếp cùng có điện áp cổng $V_{in}$: dòng bão hòa chuỗi tương đương với NMOS có độ rộng $W \approx 4\lambda \implies \beta_n \approx 240\,\mu\text{A/V}^2$.
- Tỉ số độ dẫn dòng mới:
  $$r_{tied} \approx \frac{480\mu}{240\mu} = \mathbf{2,00} \implies \sqrt{r_{tied}} = \sqrt{2} \approx 1,4142$$
- Ngưỡng chuyển mạch mới:
  $$V_{M,tied} = \frac{0,70 + 1,4142 \times (5,0 - 0,80)}{1 + 1,4142} = \frac{0,70 + 5,9397}{2,4142} = \frac{6,6397}{2,4142} \approx \mathbf{2,750\,\text{V}}$$
- **Nhận xét vật lý:** Ngưỡng $V_M$ dời sang phải một khoảng $\Delta V_M \approx +300\,\text{mV}$ vì khả năng kéo lên của PUN tăng gấp đôi khi 2 PMOS cùng dẫn.

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN SPICE BENCHMARK

## 2.6 Kế hoạch Buổi học 135 Phút & Kịch bản Can thiệp Sư phạm

### Khung giờ chi tiết:
- **00 – 15' (15 phút):** Điểm danh. Kiểm tra tại bàn bài làm Pre-lab (kích thước $W/L$, Stick diagram, kịch bản SPICE). Ký xác nhận vào báo cáo.
- **15 – 45' (30 phút):** **Ex2.1:** Dựng Schematic `nand2_x1{sch}`. Lưu ý sinh viên gán đúng Export (`Ctrl + E`), nhấn `F5` kiểm tra. Chạy quét DC VTC 1 ngõ và 2 ngõ chung. Xác nhận điểm $V_M$.
- **45 – 75' (30 phút):** **Ex2.2:** Mô phỏng quá độ Transient cổng NAND2. Hướng dẫn sinh viên viết lệnh `.meas`. Đo trễ ở 2 mức tải $C_L = 50\,\text{fF}$ và $C_L = 10\,\text{fF}$ để làm nổi bật hiệu ứng nút nội $X_n$.
- **75 – 100' (25 phút):** **Ex2.3:** Dựng Schematic `nor2_x1{sch}` với $W_p = 24\lambda$. Nhắc nhở sinh viên: ngõ vào tĩnh phải nối đất $0\,\text{V}$ (bẫy phổ biến). Đo trễ và ghi số liệu.
- **100 – 125' (25 phút):** **Ex2.4:** Thiết kế Mask Layout `nand2_x1{lay}`. Nhấn mạnh khoảng cách Poly $\ge 6\lambda_{DR}$ qua Contact chia sẻ cực má. Chạy DRC (0 lỗi) và chạy NCC LVS ("MATCH 100%").
- **125 – 135' (10 phút):** Nghiệm thu tại bàn, kiểm tra file `.jelib`, ký xác nhận hoàn thành In-lab.

---

## 2.7 Bảng Đáp án Chi tiết Pre-lab

### 1. Kích thước & Điện trở Tương đương:
| Cổng logic | Transistor | Vai trò | $(W/L)$ theo $\lambda_{DR}$ | $(W/L)$ theo $\mu\text{m}$ | Điện trở hiệu dụng |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **NAND2** | $M_{N1}, M_{N2}$ | PDN (nối tiếp) | $8\lambda / 2\lambda$ | $2,40\,\mu\text{m} / 0,60\,\mu\text{m}$ | $R_{on,N1} = R_{on,N2} = 484,5\,\Omega \implies R_{eq,N} = \mathbf{969,0\,\Omega}$ |
| **NAND2** | $M_{P1}, M_{P2}$ | PUN (song song) | $12\lambda / 2\lambda$ | $3,60\,\mu\text{m} / 0,60\,\mu\text{m}$ | $R_{eq,P,worst} = \mathbf{992,1\,\Omega}, R_{eq,P,best} = \mathbf{496,0\,\Omega}$ |
| **NOR2** | $M_{N1}, M_{N2}$ | PDN (song song) | $4\lambda / 2\lambda$ | $1,20\,\mu\text{m} / 0,60\,\mu\text{m}$ | $R_{eq,N,worst} = \mathbf{969,0\,\Omega}, R_{eq,N,best} = \mathbf{484,5\,\Omega}$ |
| **NOR2** | $M_{P1}, M_{P2}$ | PUN (nối tiếp) | $24\lambda / 2\lambda$ | $7,20\,\mu\text{m} / 0,60\,\mu\text{m}$ | $R_{on,P1} = R_{on,P2} = 496,0\,\Omega \implies R_{eq,P} = \mathbf{992,1\,\Omega}$ |

- **Tổng bề rộng kênh:** $\sum W_{NAND2} = 40\lambda_{DR} = 12,0\,\mu\text{m}$; $\sum W_{NOR2} = 56\lambda_{DR} = 16,8\,\mu\text{m}$ (NOR2 lớn hơn +40,0%).
- **Điện dung ngõ vào tương đối:**
  - $C_{in,inv} \propto 16\lambda_{DR}$.
  - $C_{in,NAND2} \propto 20\lambda_{DR} = 1,25 \times C_{in,inv} \implies g_{NAND2} = 1,250$ ($5/4$).
  - $C_{in,NOR2} \propto 28\lambda_{DR} = 1,75 \times C_{in,inv} \implies g_{NOR2} = 1,750$ ($7/4$).

### 2. Trễ Lý thuyết Giải tích:
- **Tại $C_L = 50\,\text{fF}$:**
  - NAND2: $t_{pHL} = 33,6\,\text{ps}$; $t_{pLH,worst} = 34,4\,\text{ps}$; $t_{pLH,best} = 17,2\,\text{ps}$; $t_{pd,worst} = \mathbf{34,0\,\text{ps}}$.
  - NOR2: $t_{pLH} = 34,4\,\text{ps}$; $t_{pHL,worst} = 33,6\,\text{ps}$; $t_{pHL,best} = 16,8\,\text{ps}$; $t_{pd,worst} = \mathbf{34,0\,\text{ps}}$.
- **Tại $C_L = 10\,\text{fF}$:**
  - NAND2: $t_{pHL(Ca1)} = 6,7\,\text{ps}$; $t_{pHL(Ca2)} = 6,7 + 1,7 = 8,4\,\text{ps}$ (tăng +25,0%).

---

## 2.8 Bảng Đối Chuẩn Kỹ Thuật Toàn Diện (SPICE Benchmark MOSIS C5N Level 3)

| STT | Thông số đo đạc kỹ thuật | Giá trị Giải tích Bậc 2 | Đo SPICE Pre-layout | Đo SPICE Post-layout (PEX) | Ghi chú & Nhận xét |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | **$V_M$ NAND2 (1 ngõ quét, $B=5\text{V}$)** | $2,450\,\text{V}$ | $2,44 - 2,50\,\text{V}$ | $2,44 - 2,50\,\text{V}$ | Cân bằng lý tưởng |
| 2 | **$V_M$ NAND2 (2 ngõ quét chung)** | $2,750\,\text{V}$ | $2,68 - 2,75\,\text{V}$ | $2,68 - 2,75\,\text{V}$ | Dời sang phải do 2 PMOS dẫn |
| 3 | **$V_M$ NOR2 (1 ngõ quét, $B=0\text{V}$)** | $2,450\,\text{V}$ | $2,43 - 2,49\,\text{V}$ | $2,43 - 2,49\,\text{V}$ | Cân bằng lý tưởng |
| 4 | **$V_M$ NOR2 (2 ngõ quét chung)** | $2,180\,\text{V}$ | $2,22 - 2,28\,\text{V}$ | $2,22 - 2,28\,\text{V}$ | Dời sang trái do 2 NMOS dẫn |
| 5 | **NAND2 $t_{pHL(Ca1)}$ ($A$ switch, $50\text{fF}$)** | $33,6\,\text{ps}$ | $48 - 54\,\text{ps}$ | $68 - 76\,\text{ps}$ | Nút nội đã xả điện |
| 6 | **NAND2 $t_{pHL(Ca2)}$ ($B$ switch, $50\text{fF}$)** | $35,3\,\text{ps}$ | $51 - 57\,\text{ps}$ | $72 - 82\,\text{ps}$ | Chậm hơn $\sim 5 - 6$% |
| 7 | **NAND2 $t_{pHL(Ca1)}$ ($A$ switch, $10\text{fF}$)** | $6,7\,\text{ps}$ | $11 - 14\,\text{ps}$ | $18 - 24\,\text{ps}$ | Tải nhẹ |
| 8 | **NAND2 $t_{pHL(Ca2)}$ ($B$ switch, $10\text{fF}$)** | $8,4\,\text{ps}$ | $14 - 18\,\text{ps}$ | $24 - 31\,\text{ps}$ | **Chậm hơn 20 - 25% do xả $C_{int}$** |
| 9 | **NAND2 $t_{pLH(worst)}$ (1 PMOS, $50\text{fF}$)** | $34,4\,\text{ps}$ | $50 - 58\,\text{ps}$ | $70 - 80\,\text{ps}$ | Trường hợp xấu nhất |
| 10 | **NAND2 $t_{pLH(best)}$ (2 PMOS, $50\text{fF}$)** | $17,2\,\text{ps}$ | $26 - 32\,\text{ps}$ | $38 - 46\,\text{ps}$ | Nhanh gấp đôi khi 2 PMOS cùng dẫn |
| 11 | **NOR2 $t_{pLH(worst)}$ (2 PMOS, $50\text{fF}$)** | $34,4\,\text{ps}$ | $58 - 68\,\text{ps}$ | $88 - 105\,\text{ps}$ | Chậm hơn rõ rệt do Body Effect |
| 12 | **NOR2 $t_{pHL(worst)}$ (1 NMOS, $50\text{fF}$)** | $33,6\,\text{ps}$ | $46 - 52\,\text{ps}$ | $64 - 72\,\text{ps}$ | 1 NMOS kéo xuống |
| 13 | **NOR2 $t_{pHL(best)}$ (2 NMOS, $50\text{fF}$)** | $16,8\,\text{ps}$ | $24 - 28\,\text{ps}$ | $34 - 40\,\text{ps}$ | Nhanh gấp đôi khi 2 NMOS cùng dẫn |
| 14 | **Diện tích Layout hình học ($W \times H$)** | N/A | NAND2: $\approx 105 - 120\,\mu\text{m}^2$ | NOR2: $\approx 160 - 180\,\mu\text{m}^2$ | **NOR2 lớn hơn $+45 - 50$** |
| 15 | **DRC MOSIS Errors** | 0 | 0 lỗi | 0 lỗi | Bắt buộc 0 lỗi |
| 16 | **LVS Comparison (NCC)** | N/A | **MATCH 100%** | **MATCH 100%** | So khớp topo đồng bộ |

---

## 2.9 Kịch bản Gỡ lỗi Socratic Dialogues cho Giảng viên

### Tình huống 1: Sinh viên thắc mắc "Tại sao khoảng cách 2 dải Poly là 3λ mà Electric lại báo lỗi DRC?"
- **Giảng viên:** *"Em hãy mở luật DRC Mead-Conway xem Rule 3.2.a và Rule 3.2.b khác nhau chỗ nào?"*
- **Sinh viên:** *"Rule 3.2.a ghi Poly-to-Poly spacing $\ge 3\lambda$. Em đặt đúng $3\lambda$ rồi mà thầy?"*
- **Giảng viên:** *"Giữa 2 dải Poly của em có cái gì ở giữa không?"*
- **Sinh viên:** *"Dạ có cái Contact nối cực má PMOS ra chân Out."*
- **Giảng viên:** *"Bề rộng Contact là bao nhiêu $\lambda$? Và khoảng cách từ Contact đến mỗi dải Poly tối thiểu là bao nhiêu?"*
- **Sinh viên:** *"Dạ Contact rộng $2\lambda$, khoảng cách mỗi bên là $2\lambda$ nữa. Tổng cộng là $2 + 2 + 2 = 6\lambda$ ạ! Em hiểu rồi, em phải dãn 2 dải Poly ra tối thiểu $6\lambda$ ($1,8\,\mu\text{m}$) thì mới đủ chỗ đặt Contact!"*

### Tình huống 2: Sinh viên thắc mắc "Em mô phỏng NOR2 mà ngõ ra cứ nằm bẹp ở mức 0V không nhúc nhích?"
- **Giảng viên:** *"Em cấp tín hiệu cho ngõ A và ngõ B như thế nào?"*
- **Sinh viên:** *"Dạ ngõ A em cấp xung $0 \to 5\text{V}$, còn ngõ B em nối nguồn DC tĩnh $5,0\,\text{V}$ như bài NAND2."*
- **Giảng viên:** *"Cổng NOR có bảng chân lý thế nào? Khi ngõ B bằng 1 thì ngõ ra bằng mấy dù ngõ A có nhảy thế nào chăng nữa?"*
- **Sinh viên:** *"Dạ $1 + A = 1$, phủ định là 0 ạ... Ôi ngõ ra luôn bằng 0! Vì NMOS B luôn mở dẫn xuống đất!"*
- **Giảng viên:** *"Chính xác. Vậy với cổng NOR, muốn khảo sát ngõ A chuyển mạch thì ngõ B phải giữ ở mức logic nào để không cản trở?"*
- **Sinh viên:** *"Dạ phải giữ mức 0, tức là nối đất $0\,\text{V}$ ạ!"*

### Tình huống 3: Sinh viên thắc mắc "Em đo trễ nút nội ở NAND2 giữa kích ngõ A và ngõ B thấy lệch có 1 ps, không đáng kể?"
- **Giảng viên:** *"Tải dung $C_L$ em đang đặt là bao nhiêu?"*
- **Sinh viên:** *"Dạ $50\,\text{fF}$ ạ."*
- **Giảng viên:** *"Theo công thức Elmore, độ lệch trễ $\Delta t_{pHL} \approx \ln(2) R_{on} C_{int}$. Nó phụ thuộc vào $C_{int}$ chứ có phụ thuộc vào $C_L$ không?"*
- **Sinh viên:** *"Dạ không, nó phụ thuộc vào tụ nút nội khoảng $5\,\text{fF}$."*
- **Giảng viên:** *"Đúng. Khi tải ngoài $C_L = 50\,\text{fF}$ rất lớn, thời gian xả tải ngoài mất hơn $30\,\text{ps}$, nên $1,6\,\text{ps}$ của nút nội chỉ chiếm 5%. Bây giờ em giảm tụ tải xuống $C_L = 10\,\text{fF}$ xem tỷ lệ chênh lệch sẽ là bao nhiêu?"*
- **Sinh viên (sau khi chạy):** *"Thưa thầy, trễ tăng từ $12\,\text{ps}$ lên $15\,\text{ps}$, lệch hơn 25% rõ rệt luôn ạ!"*

---

## 2.10 Đáp án Chi tiết Câu hỏi Post-lab

1. **Ưu thế của cổng NAND trong thiết kế ASIC:**  
   - Cổng NAND2 có tổng bề rộng kênh $\sum W = 40\lambda$ nhỏ hơn 40% so với NOR2 ($56\lambda$), giúp tiết kiệm diện tích silicon trên chip.
   - Điện dung ngõ vào của NAND2 ($20\lambda \cdot C'$) nhẹ hơn 40% so với NOR2 ($28\lambda \cdot C'$), tương ứng Logical Effort $g_{NAND2} = 1,25 < g_{NOR2} = 1,75$. Khi một cổng logic lái cổng NAND, trễ của cổng lái nhỏ hơn nhiều so với lái cổng NOR.
   - Tránh được hiệu ứng thân làm tăng $|V_{thp}|$ của PMOS nối tiếp trong NOR2.
2. **Vai trò của Kỹ thuật Abutment:**  
   - Chia sẻ vùng khuếch tán giúp loại bỏ khoảng cách ly cách điện ($3\lambda_{DR}$) giữa các transistor, giảm chiều dài tế bào từ 25 - 35%.
   - Giảm một nửa diện tích khuếch tán tại nút ngõ ra, triệt tiêu $50$ điện dung ký sinh cực má $C_{db}$, giúp tăng tốc độ chuyển mạch thực tế và giảm tiêu thụ công suất động $P_{dyn} = \alpha C f V_{DD}^2$.
3. **Thách thức khi thiết kế NAND4:**  
   - Để giữ nguyên khả năng kéo dòng tương đương Inverter chuẩn, 4 NMOS nối tiếp phải có chiều rộng kênh:
     $$W_n = 4 \times W_{n,inv} = 4 \times 4\lambda_{DR} = \mathbf{16\lambda_{DR} = 4,80\,\mu\text{m}}$$
   - Trong mạch logic CMOS tĩnh, trễ của chuỗi transistor mắc nối tiếp tăng theo **hàm bậc hai của số transistor $N$ ($t_{pd} \propto N^2$)** theo mô hình Elmore vì mỗi transistor vừa đóng góp thêm điện trở vừa đóng góp thêm điện dung ký sinh nút nội. Đồng thời các transistor phía trên bị hiệu ứng thân nặng nề. Do đó, quy tắc thiết kế vi mạch luôn giới hạn số ngõ vào mắc nối tiếp không quá 4 (thường dùng cây cổng NAND2/NAND3 kết hợp thay vì dùng một cổng đơn có $N \ge 4$).

---

## PHẦN III: TIÊU CHÍ NGHIỆM THU & BỘ CÂU HỎI VẤN ĐÁP TẠI BÀN

### 1. Barem Nghiệm thu Tại bàn (Thang 10):
- **1. Chuẩn bị Pre-lab (2.0 điểm):** Tính đúng kích thước $W/L$, điện trở $R_{on}$, trễ lý thuyết; vẽ đúng đồ thị Euler và sơ đồ que Stick Diagram có đầy đủ chú thích lớp và Tap.
- **2. Schematic & VTC NAND2 (2.0 điểm):** Dựng đúng sơ đồ, 0 warning F5; đo chính xác điểm $V_M$ trường hợp 1 ngõ ($2,45\,\text{V}$) và 2 ngõ ($2,75\,\text{V}$); giải thích đúng bản chất dời ngưỡng.
- **3. Đo trễ & Hiệu ứng nút nội (2.0 điểm):** Viết đúng câu lệnh `.meas`; đo đủ 3 kịch bản; chứng minh được trễ tăng 20 - 25% ở tải $10\,\text{fF}$.
- **4. Schematic & Đo trễ NOR2 (1.5 điểm):** Dựng đúng NOR2 ($W_p = 24\lambda$); đấu ngõ tĩnh xuống đất $0\,\text{V}$; đo đủ trễ worst-case và best-case.
- **5. Physical Layout, DRC & LVS (1.5 điểm):** Bố trí dải khuếch tán liền mạch Abutment; khoảng cách Poly $\ge 6\lambda$ qua contact; DRC 0 errors; NCC LVS báo **"MATCH 100%"**.
- **6. Báo cáo, Đối sánh PPA & Tác phong (1.0 điểm):** Lập bảng đối sánh PPA đầy đủ; thái độ nghiêm túc; trả lời trôi chảy câu hỏi vấn đáp.

### 2. Bộ Câu hỏi Vấn đáp Nhanh tại Bàn Máy:
1. *Hỏi:* "Tại sao khi đo trễ sườn xuống $t_{pHL}$ của cổng NAND2, việc kích ngõ B lại chậm hơn kích ngõ A?"  
   *Đáp chuẩn:* Vì giữa 2 NMOS có nút nội $X_n$. Khi kích ngõ B (ngõ A đã ở mức 1), nút $X_n$ đã bị nạp điện tích lên $\approx 3,8\,\text{V}$. Khi ngõ B chuyển trạng thái, transistor dưới phải đồng thời xả cả tụ tải ngõ ra $C_L$ lẫn tụ nút nội $C_{int}$ xuống đất.
2. *Hỏi:* "Đường đi Euler có vai trò gì trong việc vẽ Layout vi mạch CMOS?"  
   *Đáp chuẩn:* Giúp tìm thứ tự các cổng Polysilicon đồng nhất trên cả 2 mạng PUN và PDN ($A-B$). Nhờ đó các transistor kề nhau có thể dùng chung vùng khuếch tán (Abutment), loại bỏ các khoảng cách ly $3\lambda$, thu nhỏ diện tích và triệt tiêu điện dung ký sinh cực má.
3. *Hỏi:* "Nếu hai cổng NAND2 và NOR2 cùng được định cỡ để có điện trở kéo xấu nhất bằng nhau, trễ tại tải cố định bằng nhau, thì tại sao người ta vẫn ưu tiên dùng NAND2?"  
   *Đáp chuẩn:* Vì NOR2 có tổng chiều rộng kênh $\sum W$ lớn hơn 40% (tốn diện tích) và điện dung ngõ vào $C_{in}$ lớn hơn 40% ($g=1,75$ so với $1,25$). Cổng NOR2 làm tầng logic phía trước bị chậm đi 40% do phải kéo tải nặng hơn.
4. *Hỏi:* "Tại sao khoảng cách giữa hai dải Poly tại cực má chung của NAND2 phải là $6\lambda$ mà không thể là $3\lambda$?"  
   *Đáp chuẩn:* Vì ở giữa 2 dải Poly đó có đặt Contact kim loại nối ra chân Out. Chiều rộng Contact là $2\lambda$, khoảng cách cách ly từ Contact tới mỗi mép Poly tối thiểu là $2\lambda$. Do đó khoảng cách Poly-to-Poly tối thiểu phải là $2 + 2 + 2 = 6\lambda$ ($1,8\,\mu\text{m}$).
5. *Hỏi:* "Khi đo VTC của NAND2, tại sao khi nối chung cả 2 ngõ vào $A=B$ thì ngưỡng $V_M$ lại dịch chuyển sang phải?"  
   *Đáp chuẩn:* Vì khi nối chung $A=B$, cả hai PMOS cùng dẫn song song kéo lên nguồn, làm độ dẫn kéo lên $\beta_p$ tăng gấp đôi, trong khi mạng kéo xuống vẫn là chuỗi 2 NMOS. Mạng kéo lên mạnh hơn sẽ kéo điểm cân bằng điện áp $V_M$ tăng lên (dời sang phải $\approx +300\,\text{mV}$).
