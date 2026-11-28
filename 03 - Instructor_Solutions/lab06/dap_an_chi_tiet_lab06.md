# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 6 (LAB 06)
# THIẾT KẾ MẠCH CỘNG TOÀN PHẦN 1-BIT (MIRROR ADDER 28T VÀ TG ADDER)
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Đồng bộ với Teacher's Book Lab 06)*

> **Script kiểm chứng số liệu:** [verify_lab06_new.py](../../scripts/verify_lab06_new.py)  
> **Teacher's Book đầy đủ:** [Lab06_Teacher_Book.md](../../Teacher_Book/Lab06_Teacher_Book.md)  
> **Tiến trình công nghệ:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## 1. Tóm tắt Đính chính Kỹ thuật (Audit Lab 06)
1. **Biểu thức Sum của Mirror Adder:** Mạng PDN thực hiện $Sum = A B C_{in} + \overline{C_{out}}(A+B+C_{in})$ nên nút ra của tầng là $\overline{Sum}$ (không phải vế trái là $\overline{Sum}$).
2. **Số lượng Transistor Mirror Adder:** Khối Carry = $5\text{N} + 5\text{P} + 2\text{T} = 12\text{T}$; Khối Sum = $7\text{N} + 7\text{P} + 2\text{T} = 16\text{T}$; Tổng chuẩn xác duy nhất là **$28$ Transistors** (không phải $24$ hay $24-28\text{T}$).
3. **Tính chất tự đối ngẫu (Mirror):** PUN và PDN khối Carry dùng **cùng cấu trúc topo**, cho phép dùng chung đường đi Euler 5 transistor `B - A - Cin - A - B`.
4. **TG Adder (`tg_adder_tran.sp`):** Phiên bản ghép module từ `xor_tg` ($8\text{T}$), `inv_p` ($2\text{T}$), `xor_tg` ($8\text{T}$) và `MUX2_C` ($4\text{T}$) gồm **$22$ Transistors** (có thể tối ưu xuống $16\text{T}$ khi chia sẻ nút đảo).
5. **Đường tới hạn & Đảo vị trí $C_{in}$:** Bỏ ngưỡng $C_{in} \to C_{out}$ nhanh hơn $A \to Sum$ gấp $\ge 2$ lần; đường chậm nhất là $C_{in} \to Sum$ (qua `cob` $\to$ `sb` $\to$ `sum`). Đảo vị trí $C_{in}$ được kiểm chứng thực nghiệm thay cho con số 30-40%.

---

## 2. Đáp án Chi tiết Pre-lab & Bảng Đối Chuẩn

### 2.1 Bảng kích thước chuẩn Mirror Adder 28T & Tổng bề rộng $W_{Cin}$
- **Carry Logic ($5\text{N}+5\text{P}$):** NMOS $8\lambda/2\lambda$, PMOS $24\lambda/2\lambda$ ($\Sigma W = 160\lambda$).
- **Sum Logic ($7\text{N}+7\text{P}$):** NMOS $12\lambda/2\lambda$, PMOS $36\lambda/2\lambda$ ($\Sigma W = 336\lambda$).
- **2 Inverter (`INV_Cout`, `INV_Sum`):** NMOS $4\lambda/2\lambda$, PMOS $12\lambda/2\lambda$ ($\Sigma W = 32\lambda$).
- **Tổng toàn mạch:** $28\text{T}$, $\Sigma W = \mathbf{528\lambda}$ ($158,4\,\mu\text{m}$).
- **Tổng bề rộng cổng chân $C_{in}$:** $W_{Cin} = (8+24) + 2 \times (12+36) = \mathbf{128\lambda}$ (gấp $8\times$ `inv_x1`, tương ứng $C_{in} \approx 58\,\text{fF}$ nếu $C_{ox} \approx 2,5\,\text{fF}/\mu\text{m}^2$).

### 2.2 Đường trễ 4-bit RCA & Đường Euler Carry
- $T_{Cout3} = t_{pd(A,B \to Cout,0)} + 3 \cdot t_{pd(Cin \to Cout)}$ (tổng 4 tầng carry từ $C_{in,0}$).
- $T_{Sum3} = t_{pd(A,B \to Cout,0)} + 2 \cdot t_{pd(Cin \to Cout)} + t_{pd(Cin \to Sum,3)}$ (3 tầng carry + 1 tầng sum).
- **Đường Euler 5 transistor khối Carry:** `B - A - Cin - A - B` (bắt đầu/kết thúc tại `gnd`/`vdd` và nút bậc lẻ `n2`).

### 2.3 Bảng đối chuẩn thông số ($C_L = 50\,\text{fF}$)
- **Kiểm chứng 8 tổ hợp:** Đúng 8/8 trạng thái khi lấy mẫu cuối chu kỳ `10n` bằng `.meas FIND` (nhận diện glitch bình thường ở bước `011 -> 100`).
- **Trễ 1 tầng đơn $C_{in} \to C_{out}$ (Mirror Adder):** $\approx 60 - 80\,\text{ps}$.
- **Chuỗi RCA $N=1\dots 4$:** Mirror Adder tăng tuyến tính $O(N)$; TG Adder không đệm tăng bậc hai theo hệ số Elmore $N(N+1)/2 = 1 : 3 : 6 : 10$.

---

## 3. Đáp án 3 Câu hỏi Thảo luận Post-lab
1. **Vị trí $C_{in}$ sát nút `cob`:** Khi $A, B$ đến sớm, các nút nội phía dưới đã được xả/nạp sẵn; đặt $C_{in}$ sát ngõ ra `cob` giúp dòng chuyển mạch chỉ nạp/xả trực tiếp tụ tại `cob`.
2. **Độ dốc $\Delta t / \Delta N$ của RCA vs đo đơn lẻ $50\,\text{fF}$:** Tải thực tế của mỗi tầng trong chuỗi là $C_{in}$ tầng sau ($W_{Cin}=128\lambda \implies C_{in} \approx 58\,\text{fF}$) kèm sườn xung chậm từ tầng trước, làm trễ mỗi tầng thực tế lớn hơn đo đơn lẻ với nguồn xung $0,1\,\text{ns}$.
3. **Mở rộng 32-bit:** RCA chậm đi $\approx 31$ tầng carry ($O(N)$). Khắc phục bằng **Carry-Lookahead Adder (CLA)** ($O(\log N)$) hoặc **Carry-Select Adder**.
