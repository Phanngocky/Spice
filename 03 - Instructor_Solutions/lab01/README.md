# HƯỚNG DẪN GIẢNG VIÊN & ĐÁP ÁN MẪU: BÀI LAB 01
## ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER

> [!CAUTION]
> **TÀI LIỆU NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TA)**  
> Tuyệt đối không phân phát tài liệu này cho sinh viên. Tài liệu này cung cấp các giá trị chuẩn, kết quả tính toán giải tích và hướng dẫn chấm thi thực hành tại bàn.

---

### 1. ĐÁP ÁN TÍNH TOÁN LÝ THUYẾT (PRE-LAB)

1. **Tỉ số định kích thước $(W_p/W_n)$:**
   - Để điểm chuyển mạch $V_M = V_{DD}/2 = 2.50\,\text{V}$:
     $$\frac{K_n'}{2} \left(\frac{W}{L}\right)_n (V_M - V_{thn})^2 = \frac{K_p'}{2} \left(\frac{W}{L}\right)_p (V_{DD} - V_M - |V_{thp}|)^2$$
   - Với $V_{thn} = 0.70\,\text{V}$ và $|V_{thp}| = 0.80\,\text{V}$:
     $$V_M - V_{thn} = 2.5 - 0.7 = 1.8\,\text{V}$$
     $$V_{DD} - V_M - |V_{thp}| = 5.0 - 2.5 - 0.8 = 1.7\,\text{V}$$
   - Tỉ số dẫn suất $K_n'/K_p' = 120/40 = 3.0$:
     $$\frac{(W/L)_p}{(W/L)_n} = \frac{K_n'}{K_p'} \times \left(\frac{1.8}{1.7}\right)^2 \approx 3.0 \times 1.12 \approx 3.36 \approx 3.0$$
   - Khi chọn $L_n = L_p = 0.60\,\mu\text{m}$, $W_n = 1.20\,\mu\text{m}$ ($4\lambda$):
     $$W_p = 3.0 \times W_n = 3.60\,\mu\text{m} \quad (12\lambda)$$
2. **Điện trở dẫn hiệu dụng $R_{on}$:**
   - $R_{on,n} \approx \frac{1}{120 \times 10^{-6} \times (1.2/0.6) \times (5.0 - 0.7)} = \frac{1}{240 \times 10^{-6} \times 4.3} \approx 969\,\Omega \approx 0.97\,\text{k}\Omega$.
   - $R_{on,p} \approx \frac{1}{40 \times 10^{-6} \times (3.6/0.6) \times (5.0 - 0.8)} = \frac{1}{240 \times 10^{-6} \times 4.2} \approx 992\,\Omega \approx 0.99\,\text{k}\Omega$.
   - Hai điện trở dẫn xấp xỉ bằng nhau ($\approx 1.0\,\text{k}\Omega$), chứng minh tính đối xứng hoàn hảo.
3. **Ước lượng thời gian trễ lý thuyết ($C_L = 50\,\text{fF}$):**
   - $t_{pHL} \approx 0.69 \times R_{on,n} \times C_L = 0.69 \times 969\,\Omega \times 50 \times 10^{-15}\,\text{F} \approx 33.4\,\text{ps}$.
   - $t_{pLH} \approx 0.69 \times R_{on,p} \times C_L = 0.69 \times 992\,\Omega \times 50 \times 10^{-15}\,\text{F} \approx 34.2\,\text{ps}$.
   - Trễ trung bình lý thuyết: $t_{pd} \approx 33.8\,\text{ps}$.

---

### 2. KẾT QUẢ MÔ PHỎNG THAM CHIẾU (BENCHMARK RESULTS)

| Thông số đo đạc | Giá trị Lý thuyết | Giá trị Mô phỏng SPICE Pre-layout | Giá trị Mô phỏng SPICE Post-layout (PEX) | Ghi chú đánh giá |
| :--- | :---: | :---: | :---: | :--- |
| **$V_{thn}$** | $0.70\,\text{V}$ | $0.69 - 0.71\,\text{V}$ | $0.69 - 0.71\,\text{V}$ | Đo qua tiếp tuyến $\sqrt{I_{DS}}$ |
| **$V_{thp}$** | $-0.80\,\text{V}$ | $-0.79 - -0.81\,\text{V}$ | $-0.79 - -0.81\,\text{V}$ | Đo qua tiếp tuyến $\sqrt{\vert I_{DS}\vert}$ |
| **Điện áp chuyển mạch $V_M$** | $2.50\,\text{V}$ | $2.48 - 2.52\,\text{V}$ | $2.47 - 2.52\,\text{V}$ | Giao điểm $V_{out} = V_{in}$ |
| **$V_{IL}$** | $\sim 2.10\,\text{V}$ | $2.05 - 2.15\,\text{V}$ | $2.05 - 2.15\,\text{V}$ | Điểm $dV_{out}/dV_{in} = -1$ |
| **$V_{IH}$** | $\sim 2.85\,\text{V}$ | $2.80 - 2.90\,\text{V}$ | $2.80 - 2.90\,\text{V}$ | Điểm $dV_{out}/dV_{in} = -1$ |
| **Lề nhiễu thấp $NM_L$** | $\sim 2.10\,\text{V}$ | $\ge 2.05\,\text{V}$ | $\ge 2.05\,\text{V}$ | $NM_L = V_{IL} - 0$ |
| **Lề nhiễu cao $NM_H$** | $\sim 2.15\,\text{V}$ | $\ge 2.10\,\text{V}$ | $\ge 2.10\,\text{V}$ | $NM_H = 5.0 - V_{IH}$ |
| **Trễ sườn xuống $t_{pHL}$ ($C_L=50\text{fF}$)** | $33.4\,\text{ps}$ | $45 - 55\,\text{ps}$ | $60 - 75\,\text{ps}$ | Tăng $\sim 25-35\%$ do tụ ký sinh khuếch tán $C_{db}$ |
| **Trễ sườn lên $t_{pLH}$ ($C_L=50\text{fF}$)** | $34.2\,\text{ps}$ | $48 - 58\,\text{ps}$ | $65 - 80\,\text{ps}$ | Tăng $\sim 25-35\%$ do tụ ký sinh khuếch tán $C_{db}$ |
| **DRC MOSIS Errors** | 0 | 0 | 0 | Phải đạt 0 lỗi mới ký nhận |
| **LVS Comparison** | N/A | N/A | **MATCH** | "Cells are topologically equivalent" |

---

### 3. HƯỚNG DẪN CHẤM VÀ PHỎNG VẤN TẠI BÀN (ORAL QUESTIONS)

Giảng viên chọn ngẫu nhiên 1 trong các câu hỏi sau khi nghiệm thu tại bàn:
1. *Hỏi:* "Tại sao trong mô phỏng Post-layout, thời gian trễ $t_{pHL}$ và $t_{pLH}$ lại tăng lên khoảng 20–35% so với mô phỏng Schematic Pre-layout?"  
   *Trả lời chuẩn:* Do trong Layout thực tế, cực Drain có diện tích ($AD$) và chu vi ($PD$) tạo nên điện dung tiếp giáp $p-n$ ($C_{db}$ và $C_{sb}$), cộng thêm điện dung ký sinh của đường dây Metal 1 nối hai cực Drain. Tổng dung ở nút ngõ ra tăng từ $C_L$ thành $C_L + C_{drain,n} + C_{drain,p} + C_{wire}$.
2. *Hỏi:* "Nếu ta đảo ngược vị trí cực Source và Drain của NMOS trong Layout thì mạch có chạy đúng không?"  
   *Trả lời chuẩn:* MOSFET là linh kiện có tính đối xứng cao về mặt cấu trúc (nếu Source và Drain có cùng kích thước và pha tạp). Mạch vẫn hoạt động, tuy nhiên cực Source phải luôn được nối cố định vào mức điện thế thấp nhất ($GND$) để đảm bảo tiếp giáp $p-n$ chất nền luôn phân cực ngược.
3. *Hỏi:* "Nếu bỏ hai tiếp xúc phân cực chất nền (Well/Substrate Taps) thì mạch có mô phỏng được không và trên vi mạch thật sẽ xảy ra hiện tượng gì?"  
   *Trả lời chuẩn:* Trong SPICE nếu gán chân Bulk thì vẫn chạy được; nhưng trên Layout nếu không có Taps thì LVS sẽ báo lỗi thiếu kết nối hoặc nổi điện thế (floating well). Trên chip thật, hiện tượng Latch-up sẽ kích hoạt cấu trúc thyristor ký sinh p-n-p-n, gây dòng ngắn mạch cực lớn làm cháy vi mạch.
