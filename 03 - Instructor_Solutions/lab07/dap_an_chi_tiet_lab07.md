# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 7 (LAB 07)
# KỸ THUẬT LOGIC ĐỘNG VÀ LOGIC DOMINO (DYNAMIC & DOMINO CMOS LOGIC)
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Đồng bộ với Teacher's Book Lab 07)*

> **Script kiểm chứng số liệu:** [verify_lab07_new.py](../../scripts/verify_lab07_new.py)  
> **Teacher's Book đầy đủ:** [Lab07_Teacher_Book.md](../../Teacher_Book/Lab07_Teacher_Book.md)  
> **Tiến trình công nghệ:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## 1. Tóm tắt Đính chính Kỹ thuật (Audit Lab 07)
1. **Điều kiện Charge Sharing:** Cổng Domino OR4 có Foot NMOS không gặp Charge Sharing ở pha Evaluate vì `n_eval` nối đất qua $M_{eval}$. Phải dùng mạch thử **2-NMOS nối tiếp** (`Mn_top`, `Mn_bot`) tạo nút nội cô lập $C_{int}$.
2. **Inverter $16\lambda/8\lambda$ là Low-skew:** Với $W_p/W_n = 2 < 3$, $r = 0,8165 \implies V_M = \mathbf{2,273\,\text{V}} < 2,45\,\text{V}$ (không phải High-skew và không dùng $V_M=2,45\,\text{V}$).
3. **Giới hạn công thức Charge Sharing:** Transistor trên chỉ nạp $C_{int}$ lên tối đa $V_G - V_{thn} \approx 3,79\,\text{V}$ (C5N), nên công thức cân bằng chỉ đúng khi $\frac{C_{int}}{C_X + C_{int}} \ge 0,24 - 0,27$.
4. **Định cỡ Keeper hợp lệ DRC:** $W_{kp} = 2\lambda$ vi phạm bề rộng Active tối thiểu ($3\lambda$); thực tế dùng $W_{kp} = 3\lambda - 4\lambda$ với $L_{kp} = 4\lambda - 8\lambda$. Quét Ex7.3 đo cả $t_{pd,eval}$ và $V_{X,min}$; ở $W_{kp}=8\lambda$ ($L=2\lambda$), dòng Keeper $\approx 69$% dòng PDN đơn nên `.meas` có thể báo `FAILED`.
5. **Ưu thế $\Sigma W$ và $C_{in}$:** Domino OR4 ($9\text{T}$) có $\Sigma W = 62-64\lambda$, $C_{in} = 4\lambda$/chân, nhỏ hơn rất nhiều so với Static OR4 ($10\text{T}, \Sigma W = 224\lambda, C_{in} = 52\lambda$).

---

## 2. Đáp án Chi tiết Pre-lab & Bảng Đối Chuẩn

### 2.1 Ngưỡng $V_M$ và Charge Sharing ($C_X = 20\,\text{fF}, C_{int} = 14\,\text{fF}$)
- $V_M(16\lambda/8\lambda) = \mathbf{2,273\,\text{V}}$ (Low-skew).
- $V_X' = 5,0 \cdot \frac{20}{34} = \mathbf{2,941\,\text{V}}$, $\Delta V_X = \mathbf{2,059\,\text{V}}$, $NM_H = 2,941 - 2,273 = \mathbf{0,668\,\text{V}}$.
- Điều kiện lật giả ($V_X' \le 2,273\,\text{V}$): $C_{int} \ge \mathbf{1,20\,C_X}$.
- Với $C_{int}/C_X = 0,1$: công thức cân bằng cho $\Delta V = 0,455\,\text{V}$, nhưng giới hạn vật lý bởi $V_G - V_{thn} \approx 3,79\,\text{V}$ khống chế $\Delta V \le 0,379\,\text{V}$.

### 2.2 Tỉ số dòng Keeper / PDN đơn ($V_X = 2,5\,\text{V}, L_{kp}=2\lambda$)
- Dòng nhánh PDN đơn ($4\lambda$ nối tiếp foot $8\lambda$, $R_{eq} \approx 1\,454\,\Omega$) $\approx 1,72\,\text{mA}$.
- $W_{kp} = 2\lambda, 4\lambda, 6\lambda, 8\lambda \implies I_{kp} \approx 0,30; 0,59; 0,89; 1,18\,\text{mA} \implies I_{kp}/I_{PDN} \approx \mathbf{0,17;\; 0,34;\; 0,51;\; 0,69}$.

### 2.3 Bảng đối chuẩn thông số
- **Ex7.1:** $V_{X,min} \approx 2,85 - 3,05\,\text{V}$ (không Keeper); tăng rõ rệt khi có Keeper.
- **Ex7.2:** `domino_or4_x1` đúng 6/6 tổ hợp (`0000`, `1000`, `0100`, `0010`, `0001`, `1111`).
- **Ex7.5:** Domino OR4 ($9\text{T}, \Sigma W=62-64\lambda, C_{in}=4\lambda$) vs Static OR4 ($10\text{T}, \Sigma W=224\lambda, C_{in}=52\lambda$).

---

## 3. Đáp án 3 Câu hỏi Thảo luận Post-lab
1. **OR4 không bị Charge Sharing ở Evaluate:** 4 NMOS song song nối chung `n_eval` và nối thẳng đất qua $M_{eval}$ đang bật, không có nút nội cô lập.
2. **Low-skew Inverter ($16\lambda/8\lambda$):** Hạ $V_M$ xuống $2,27\,\text{V}$ giúp mở rộng lề nhiễu mức cao $NM_H = V_X' - V_M$, tăng độ bền trước sụt áp Charge Sharing.
3. **Keeper hợp lệ DRC:** Giữ $W_{kp} = 3\lambda - 4\lambda$ ($\ge 3\lambda$ Active) và tăng chiều dài kênh $L_{kp} = 4\lambda - 8\lambda$.
