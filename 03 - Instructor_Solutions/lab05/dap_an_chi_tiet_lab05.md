# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 5 (LAB 05)
# MẠCH TUẦN TỰ MỨC TRANSISTOR: D-LATCH VÀ D-FLIP-FLOP MASTER-SLAVE
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Đồng bộ với Teacher's Book Lab 05)*

> **Script kiểm chứng số liệu:** [verify_lab05_new.py](../../scripts/verify_lab05_new.py)  
> **Teacher's Book đầy đủ:** [Lab05_Teacher_Book.md](../../Teacher_Book/Lab05_Teacher_Book.md)  
> **Tiến trình công nghệ:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## 1. Tóm tắt Đính chính Kỹ thuật (Audit Lab 05)
1. **Vai trò Inverter phản hồi $I_3$:** Với kiến trúc chuẩn có $TG_2$ (Hình 5.1), $TG_1$ và $TG_2$ không dẫn cùng lúc ở trạng thái xác lập nên $I_3$ **không** tranh chấp với $TG_1$ và chỉ cần kích thước tối thiểu ($4\lambda/2\lambda$). Nếu bỏ $TG_2$ (mạch chốt kiểu weak inverter), $W=4\lambda, L=2\lambda$ **không đủ yếu** ($V_X = 2,244\,\text{V} < 2,45\,\text{V}$), phải dùng $L=4\lambda$ ($V_X = 3,098\,\text{V}$).
2. **Race Condition & Nguồn gốc $t_{hold}$:** Cấu trúc Master-Slave chỉ giảm race khi $\overline{CLK}$ bám sát $CLK$; độ trễ qua `X_CLK_INV` ($\approx t_{pd,inv}$) sinh ra khoảng chồng dẫn ngắn và chính là nguyên nhân gây ra $t_{hold} > 0$.
3. **Đường dẫn đầy đủ của $t_{c-q}$:** $CLK \to \overline{CLK} \to TG_{S1} \to I_{S1} \to I_{S2} \to Q$ (3 INV + 1 TG $\approx 144\,\text{ps}$, không phải $110\,\text{ps}$ thiếu $I_2$).
4. **Phương pháp đo SPICE:** Phải dùng `.ic V(q)=0` và `TD=` cho $t_{c-q}$; định nghĩa $\Delta t$ ở mốc $50$–$50$ và dùng quy ước 10% push-out riêng cho $t_{setup}$ (cả sườn lên và xuống của $D$); dùng quét bước $5\,\text{ps}$ (`-50p..+100p`) với `.meas FIND` cho ngưỡng nhị phân $t_{hold}$.
5. **Lộ trình:** Lab 5 tập trung hoàn toàn vào thiết kế mạch tuần tự và đo kiểm định thời trong 135 phút (không bắt buộc Layout/PEX).

---

## 2. Đáp án Chi tiết Pre-lab & Bảng Đối Chuẩn

### 2.1 Bảng chân trị Master-Slave DFF

| $CLK$ | $D$ | Master Latch | Slave Latch | $Q_{next}$ | Chế độ hoạt động |
| :---: | :---: | :---: | :---: | :---: | :--- |
| 0 | 0 | Trong suốt ($Q_M = 0$) | Chốt giữ ($Q = Q_{prev}$) | $Q_{prev}$ | Master nạp '0', Slave giữ |
| 0 | 1 | Trong suốt ($Q_M = 1$) | Chốt giữ ($Q = Q_{prev}$) | $Q_{prev}$ | Master nạp '1', Slave giữ |
| 1 | X | Chốt giữ ($Q_M$ khóa) | Trong suốt ($Q = Q_M$) | $Q_M$ | Master cách ly, Slave xuất |
| $\uparrow$ | 0 | Chuyển sang chốt | Chuyển sang mở | **0** | Lấy mẫu sườn dương ('0') |
| $\uparrow$ | 1 | Chuyển sang chốt | Chuyển sang mở | **1** | Lấy mẫu sườn dương ('1') |

### 2.2 Ước lượng định thời (với giá trị minh họa $t_{pd,inv}=34\,\text{ps}, t_{pd,tg}=42\,\text{ps}$)
- **D-Latch $t_{pd(D\to Q)}$:** $t_{pd,TG1} + t_{pd,I1} + t_{pd,I2} \approx 110\,\text{ps}$.
- **DFF $t_{c-q}$ (đầy đủ):** $t_{pd,INV(CLK)} + t_{pd,TG(S1)} + t_{pd,I(S1)} + t_{pd,I(S2)} \approx \mathbf{144\,\text{ps}}$.
- **DFF $t_{setup}$:** $t_{pd,TG(M1)} + t_{pd,I(M1)} \approx 76\,\text{ps}$.
- **DFF $t_{hold}$:** $\approx t_{pd,INV(CLK)} \approx 34\,\text{ps}$.
- **$T_{min,no-logic}$:** $t_{c-q} + t_{setup} \approx 220\,\text{ps}$ ($\implies 1/T_{min} \approx 4,55\,\text{GHz}$, chưa tính logic tổ hợp $t_{comb,max}$ và $t_{skew}$).

### 2.3 Bài toán chia áp $I_3$ (khi bỏ $TG_2$)
- $W=4\lambda, L=2\lambda$ ($R_n = 969\,\Omega$): $V_X = 5,0 \cdot \frac{969}{969+1190} = \mathbf{2,244\,\text{V}} < V_M \approx 2,45\,\text{V}$ (**Thất bại**).
- $W=4\lambda, L=4\lambda$ ($R_n = 1\,938\,\Omega$): $V_X = 5,0 \cdot \frac{1938}{1938+1190} = \mathbf{3,098\,\text{V}} > 2,45\,\text{V}$ (**Đạt**).

### 2.4 Bảng đối chuẩn thông số In-lab & Post-lab ($C_L = 50\,\text{fF}$)
- **Số transistor:** `dlatch_x1` = $10\text{T}$; `dff_ms_x1` = $22\text{T}$.
- **D-Latch:** $t_{pd(D\to Q)} \approx 100 - 125\,\text{ps}$; mức chốt $5,00\,\text{V} / 0,00\,\text{V}$ ($\pm 20\,\text{mV}$).
- **DFF:** $t_{c-q} \approx 130 - 160\,\text{ps}$; $t_{setup} \approx 70 - 100\,\text{ps}$ (10% push-out); $t_{hold} \approx +15 \text{ đến } +45\,\text{ps}$ (giảm xuống khi thay `X_CLK_INV` bằng `inv_x2`).

---

## 3. Đáp án Câu hỏi Thảo luận Post-lab
1. **Metastability & Synchronizer:** Nút $Q_M$ rơi vào vùng cân bằng không bền $V_M \approx V_{DD}/2$, thời gian giải quyết $t_{resolve} = \tau_{reg} \ln(V_{DD}/\Delta V_0)$. Dùng bộ đồng bộ hóa 2 tầng Flip-Flop (2-FF Synchronizer) để giảm xác suất lỗi (tăng MTBF).
2. **Thay `X_CLK_INV` thành `inv_x2`:** Trễ tạo `clk_n` giảm đi, khóa $TG_{M1}$ nhanh hơn sau sườn lên `clk` $\implies$ $t_{hold}$ giảm.
3. **TSPC DFF vs TG-DFF:** TSPC chỉ dùng 1 pha xung nhịp (nhỏ gọn, nhanh, ít transistor) nhưng là mạch động nhạy nhiễu và không giữ được dữ liệu ở DC; TG-DFF là mạch tĩnh hoàn toàn, tin cậy ở mọi tần số đến DC.
