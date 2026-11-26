# HƯỚNG DẪN GIẢNG VIÊN & ĐÁP ÁN MẪU: BÀI LAB 01
## ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER

> [!CAUTION]
> **TÀI LIỆU NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TA)**  
> Tuyệt đối không phân phát tài liệu này cho sinh viên. Chi tiết lý thuyết chuyên sâu, kịch bản sư phạm 135 phút, phân tích vật lý và giải thích toán học đầy đủ được trình bày trong:  
> 👉 [dap_an_chi_tiet_lab01.md](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/dap_an_chi_tiet_lab01.md) hoặc [Lab01_Teacher_Book.md](file:///d:/tam/VLSI_Spice/Teacher_Book/Lab01_Teacher_Book.md)

---

### 1. ĐÁP ÁN TÍNH TOÁN LÝ THUYẾT (PRE-LAB P1 – P7)

1. **Tham số công nghệ C5N Level 3 (P1):**
   - NMOS: `VTO = 0.70V`, `KP = 120uA/V^2`, `TOX = 9.5nm`, `GAMMA = 0.40`, `VMAX = 1.0E5 m/s`, `THETA = 0.05 V^-1`, `KAPPA = 0.10`.
   - PMOS: `VTO = -0.80V`, `KP = 40uA/V^2`, `TOX = 9.5nm`, `GAMMA = 0.50`, `VMAX = 1.0E5 m/s`, `THETA = 0.10 V^-1`, `KAPPA = 0.20`.
   - Lưu ý: Không có tham số `LAMBDA` trực tiếp trong Level 3. Điều chế kênh được thể hiện qua `KAPPA`, `ETA`, `VMAX`.

2. **Tỉ số định kích thước $(W_p/W_n)$ và điểm $V_M$ (P2):**
   - Để đạt đối xứng $V_M = 2,50\,	ext{V}$: $\sqrt{r} = rac{2,5 - 0,7}{5,0 - 2,5 - 0,8} = rac{1,8}{1,7} pprox 1,0588 \implies r pprox 1,1211 \implies rac{(W/L)_p}{(W/L)_n} = 1,1211 	imes 3,0 = \mathbf{3,363}$.
   - Chuẩn thiết kế lưới nguyên $\lambda_{DR} = 0,30\,\mu	ext{m}$: Chọn $W_p = 12\lambda = 3,60\,\mu	ext{m}$, $W_n = 4\lambda = 1,20\,\mu	ext{m}$ (tỉ số $3,0$).
   - Với tỉ số này ($r=1,0$): $V_M = rac{0,70 + 1,0 	imes (5,0 - 0,80)}{2} = \mathbf{2,450\,	ext{V}}$ (lệch $-50\,	ext{mV}$ hay $2,0\%$ so với $2,50\,	ext{V}$).

3. **Điện trở dẫn hiệu dụng $R_{on}$ tại $V_{DS} 	o 0$ (P3):**
   - $R_{on,n} = rac{1}{240 	imes 10^{-6} 	imes (5,0 - 0,70)} = \mathbf{969\,\Omega}$.
   - $R_{on,p} = rac{1}{240 	imes 10^{-6} 	imes (5,0 - 0,80)} = \mathbf{992\,\Omega}$.
   - Tại $C_L = 50\,	ext{fF}$: $t_{pHL} pprox 33,6\,	ext{ps}, t_{pLH} pprox 34,4\,	ext{ps}, t_{pd} pprox \mathbf{34,0\,	ext{ps}}$.
   - Trễ đo thực tế qua mô phỏng SPICE sẽ lớn hơn ($pprox 48 - 56\,	ext{ps}$, gấp khoảng 1,5–1,8 lần) do transistor phóng nạp qua vùng bão hòa trước khi tới vùng tuyến tính.

4. **Sơ đồ que Stick diagram (P4):**
   - Euler Path: $[In]$. Ray nguồn Metal 1 rộng $6\lambda$. Dải Poly liên tục. Có tiếp xúc $N^+$-tap nối N-Well lên $V_{DD}$ và $P^+$-tap nối P-Substrate xuống $GND$ chống Latch-up.

5. **Lề nhiễu logic bậc hai (P6):**
   - $V_{IL} pprox 2,01\,	ext{V}$, $V_{IH} pprox 2,89\,	ext{V}$, $NM_L pprox 2,01\,	ext{V}$, $NM_H pprox 2,11\,	ext{V}$.

6. **Điện dung ngõ vào $C_{in}$ (P7):**
   - $C_{ox} pprox 3,63\,	ext{fF}/\mu	ext{m}^2$. Kênh dẫn: $2,88\,\mu	ext{m}^2 \implies C_{gate} pprox 10,5\,	ext{fF}$. Tổng $C_{in} pprox 12 - 14\,	ext{fF}$ (kèm chồng lấp).

---

### 2. KẾT QUẢ MÔ PHỎNG THAM CHIẾU (BENCHMARK RESULTS)

| Thông số đo đạc | Giá trị Lý thuyết | Giá trị Mô phỏng SPICE Pre-layout | Giá trị Mô phỏng SPICE Post-layout (PEX) | Ghi chú đánh giá |
| :--- | :---: | :---: | :---: | :--- |
| **$V_{thn}$** | $0,70\,	ext{V}$ | $0,69 - 0,71\,	ext{V}$ | $0,69 - 0,71\,	ext{V}$ | Đo qua tiếp tuyến $\sqrt{I_{DS}}$ |
| **$V_{thp}$** | $-0,80\,	ext{V}$ | $-0,79 - -0,81\,	ext{V}$ | $-0,79 - -0,81\,	ext{V}$ | Đo qua tiếp tuyến $\sqrt{ert I_{DS}ert}$ |
| **$\lambda_{CLM}$ ($V_{GS}=3	ext{V}$)** | — | $0,045 - 0,055\,	ext{V}^{-1}$ | $0,045 - 0,055\,	ext{V}^{-1}$ | Đo giữa $3	ext{V}$ và $5	ext{V}$ vùng bão hòa |
| **Điện áp chuyển mạch $V_M$** | $2,45\,	ext{V}$ | $2,448 - 2,455\,	ext{V}$ | $2,445 - 2,452\,	ext{V}$ | Giao điểm $V_{out} = V_{in}$ |
| **$V_{IL}$ (slope = $-1$)** | $2,01\,	ext{V}$ | $1,65 - 1,82\,	ext{V}$ | $1,65 - 1,81\,	ext{V}$ | Điểm $dV_{out}/dV_{in} = -1$ |
| **$V_{IH}$ (slope = $-1$)** | $2,89\,	ext{V}$ | $2,78 - 2,85\,	ext{V}$ | $2,78 - 2,85\,	ext{V}$ | Điểm $dV_{out}/dV_{in} = -1$ |
| **Lề nhiễu thấp $NM_L$** | $2,01\,	ext{V}$ | $\ge 1,65\,	ext{V}$ | $\ge 1,65\,	ext{V}$ | $NM_L = V_{IL} - 0$ |
| **Lề nhiễu cao $NM_H$** | $2,11\,	ext{V}$ | $\ge 2,15\,	ext{V}$ | $\ge 2,15\,	ext{V}$ | $NM_H = 5,0 - V_{IH}$ |
| **Trễ sườn xuống $t_{pHL}$ ($C_L=50	ext{fF}$)** | $33,6\,	ext{ps}$ ($0,69RC$) | $48 - 55\,	ext{ps}$ | $70 - 78\,	ext{ps}$ | Tăng $+40 - 48\%$ do tụ ký sinh khuếch tán $C_{db}$ và dây dẫn |
| **Trễ sườn lên $t_{pLH}$ ($C_L=50	ext{fF}$)** | $34,4\,	ext{ps}$ ($0,69RC$) | $50 - 58\,	ext{ps}$ | $73 - 82\,	ext{ps}$ | Tăng $+40 - 48\%$ do tụ ký sinh khuếch tán $C_{db}$ và dây dẫn |
| **Trễ trung bình $t_{pd}$ ($C_L=50	ext{fF}$)** | $34,0\,	ext{ps}$ ($0,69RC$) | $49 - 56\,	ext{ps}$ | $72 - 80\,	ext{ps}$ | Tăng $+42 - 48\%$ sau trích xuất PEX |

---

### 3. CÂU HỎI VẤN ĐÁP TẠI BÀN (ORAL QUESTIONS)

1. *Hỏi:* "Tại sao khi đo $\lambda_{CLM}$ trên đường cong $V_{GS} = 5\,	ext{V}$, việc lấy hai điểm $V_{DS} = 3\,	ext{V}$ và $5\,	ext{V}$ là sai về mặt lý thuyết?"  
   *Trả lời chuẩn:* Vì ở $V_{GS} = 5,0\,	ext{V}$, điện áp bão hòa tối thiểu là $V_{DS,sat} = V_{GS} - V_{thn} = 5,0 - 0,7 = 4,3\,	ext{V}$. Điểm $V_{DS} = 3,0\,	ext{V}$ vẫn còn nằm trong vùng tuyến tính (triode), chưa vào bão hòa, do đó không phản ánh đúng hiện tượng điều chế kênh dẫn. Cần đo trên đường cong $V_{GS} = 3,0\,	ext{V}$ nơi $V_{DS,sat} = 2,3\,	ext{V} < 3,0\,	ext{V}$.
2. *Hỏi:* "Tại sao thời gian trễ mô phỏng SPICE lại lớn hơn từ 1,5 đến 1,8 lần so với mô hình Elmore $0,69 \cdot R_{on} \cdot C_L$?"  
   *Trả lời chuẩn:* Vì $R_{on}$ được tính ở vùng triode sâu ($V_{DS} pprox 0$). Trong thực tế chuyển mức từ $5\,	ext{V}$ về $2,5\,	ext{V}$, transistor bắt đầu từ vùng bão hòa có dòng bị chặn và điện trở tức thời cao hơn $2$ lần so với $R_{on}$. Quá trình xả qua vùng bão hòa làm chậm tốc độ phóng nạp so với giả định điện trở hằng số.
3. *Hỏi:* "Tại sao trong tiến trình C5N, chiều cao khung tế bào chuẩn được chốt cố định là $H_{cell} = 40\lambda$?"  
   *Trả lời chuẩn:* Để khi ghép nối các tế bào logic khác nhau (Inverter, NAND, NOR, AOI, Flip-Flop) vào cùng một hàng (standard cell row), hai thanh ray nguồn $V_{DD}$ và $GND$ ở mép trên và mép dưới tự động liền mạch và thẳng hàng nhau, tạo thành lưới phân phối nguồn xuyên suốt cho toàn chip mà không cần đi dây nối thủ công.

---

### 4. DANH MỤC TỆP SPICE NETLIST THAM CHIẾU
- [nmos_iv_curve.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/nmos_iv_curve.sp): Quét đặc tuyến I-V NMOS.
- [pmos_iv_curve.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/pmos_iv_curve.sp): Quét đặc tuyến I-V PMOS.
- [cmos_inverter_vtc_only.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_vtc_only.sp): Quét DC đặc tuyến VTC và tính lề nhiễu.
- [cmos_inverter_vtc_tran.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_vtc_tran.sp): Mô phỏng quá độ Transient và đo trễ tự động.
- [cmos_inverter_pex_postlayout.sp](file:///d:/tam/VLSI_Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_pex_postlayout.sp): Mô phỏng trễ hậu layout sau trích xuất PEX.\n