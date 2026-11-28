# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 4 (LAB 04)
# CỔNG TRUYỀN (TRANSMISSION GATE) VÀ BỘ DỒN KÊNH MUX MỨC TRANSISTOR
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Đồng bộ với Teacher's Book Lab 04)*

> **Script kiểm chứng số liệu:** [verify_lab04_new.py](../../scripts/verify_lab04_new.py)  
> **Teacher's Book đầy đủ:** [Lab04_Teacher_Book.md](../../Teacher_Book/Lab04_Teacher_Book.md)  
> **Tiến trình công nghệ:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## 1. Tóm tắt Đính chính Kỹ thuật (Audit Lab 04)
1. **Điện trở $R_{TG}(V_{in})$:** Không phải $490\,\Omega$ ($969 \parallel 992$ là sai vì $V_{GS}$ giảm một nửa ở $V_{in}=2,5\,\text{V}$). Giá trị đúng theo mô hình bậc hai là $\approx \mathbf{1,19\,\text{k}\Omega}$ (không body effect) và vồng lên đỉnh $\approx \mathbf{1,68\,\text{k}\Omega}$ (khi tính body effect).
2. **Weak '0' của PMOS:** Phải tính hiệu ứng thân ($V_{BS} = V_{DD} - V_{out}$). Kết quả điểm cố định là $\mathbf{V_{out,min} \approx 1,42\,\text{V}}$ (C5N) hoặc $1,46\,\text{V}$ ($\gamma=0,53$), không phải $0,80 - 1,05\,\text{V}$.
3. **Cửa sổ đo `.MEAS` cho Weak '0':** Bắt buộc dùng `FROM=35n TO=55n` (sau sườn xuống đầu tiên) để tránh lấy nhầm điểm làm việc DC $V_{out} = 0\,\text{V}$ lúc $t=0$.
4. **Hiện tượng chồng dẫn (Contention):** Tín hiệu $\overline{S}$ trễ hơn $S$ một khoảng $t_{pd,inv} \approx 30-45\,\text{ps}$, làm 2 TG cùng dẫn thoáng qua khi $S$ chuyển trạng thái, sinh ra đỉnh dòng $I(V_{DD})$ và glitch trên $Y$ nếu $D_0 \neq D_1$.

---

## 2. Đáp án Chi tiết Pre-lab & Bảng Đối Chuẩn

### 2.1 Giải bài toán Body Effect (C5N: $\gamma_n=0,40, \gamma_p=0,50, 2\phi_F=0,70$)
- **NMOS Weak '1':** $V_{thn,eff} = 1,213\,\text{V} \implies \mathbf{V_{out,max} = 3,787\,\text{V}}$.
- **PMOS Weak '0':** $|V_{tp,eff}| = 1,417\,\text{V} \implies \mathbf{V_{out,min} = 1,417\,\text{V}}$.
- **Dòng rò tĩnh ở `inv_x1` tầng sau:** $\approx 20,4\,\mu\text{A}$ (C5N) đến $38,9\,\mu\text{A}$ ($\gamma=0,53$).

### 2.2 Định cỡ `TG_FAST` ($R = 0,5 \times R_{inv}$)
- Kích thước nhân đôi: $W_n = 8\lambda = 2,40\,\mu\text{m}, \quad W_p = 24\lambda = 7,20\,\mu\text{m}, \quad L = 2\lambda = 0,60\,\mu\text{m}$.
- Điện trở $R_{TG}$ lý thuyết của TG chuẩn ($4\lambda / 12\lambda$, không body effect):
  * $V_{in} = 0\,\text{V}$: $969\,\Omega$
  * $V_{in} = 2,5\,\text{V}$: $1\,190\,\Omega$
  * $V_{in} = 5,0\,\text{V}$: $992\,\Omega$

### 2.3 Bảng chân trị `mux4_tg`

| $S_1$ | $S_0$ | TG dẫn ở Tầng 1 | TG dẫn ở Tầng 2 | Ngõ ra $Y$ |
| :-: | :-: | :---: | :---: | :---: |
| 0 | 0 | `X_MUX_A.TG0` & `X_MUX_B.TG0` | `X_MUX_C.TG0` | $D_0$ |
| 0 | 1 | `X_MUX_A.TG1` & `X_MUX_B.TG1` | `X_MUX_C.TG0` | $D_1$ |
| 1 | 0 | `X_MUX_A.TG0` & `X_MUX_B.TG0` | `X_MUX_C.TG1` | $D_2$ |
| 1 | 1 | `X_MUX_A.TG1` & `X_MUX_B.TG1` | `X_MUX_C.TG1` | $D_3$ |

### 2.4 Bảng đối chuẩn thông số In-lab & Post-lab ($C_L = 50\,\text{fF}$)
- **Pass Transistor:** NMOS $V_{max} \approx 3,79\,\text{V}$, PMOS $V_{min} \approx 1,42\,\text{V}$, TG Swing $0,00 \to 5,00\,\text{V}$.
- **Trễ `mux2_tg`:** $D \to Y \approx 40-50\,\text{ps}$; $S \to Y \approx 65-80\,\text{ps}$; chồng dẫn $\Delta t \approx 30-45\,\text{ps}$.
- **Trễ `mux4_tg`:** $D_0 \to Y \ge 2 \times t_{pd,MUX2}$ ($\approx 90-115\,\text{ps}$).
- **Chuỗi $N$ TG ($C_{node}=10\,\text{fF}$):** $t_{pd}(N) = 0,69 R_{TG} C_{node} \frac{N(N+1)}{2} \implies$ $N=1\dots6$: $8,2; 24,6; 49,3; 82,1; 123,2; 172,4\,\text{ps}$ ($O(N^2)$).
- **Layout `mux2_tg{lay}`:** 3 cột Poly, $W \approx 29-32\lambda$ ($\approx 9\,\mu\text{m}$), $H_{cell} = 40\lambda$ ($12\,\mu\text{m}$), DRC 0 errors, NCC `topologically equivalent (MATCH)`.

---

## 3. Đáp án 4 Câu hỏi Thảo luận Post-lab
1. **Elmore $O(N^2)$:** Tụ tại nút thứ $k$ nạp/xả qua tổng trở $k$ cổng trước đó $\implies \sum_{k=1}^N k = \frac{N(N+1)}{2}$. Chèn `inv_x1` sau mỗi 3–4 cổng truyền.
2. **Bulk PMOS nối $V_{DD}$:** Tín hiệu tại S/D dao động $0 \leftrightarrow 5\,\text{V}$. Nếu nối Bulk vào S/D, tiếp giáp P-N giữa vùng khuếch tán và N-Well sẽ phân cực thuận khi nút kia ở mức thấp, gây dòng rò và Latch-up.
3. **Đỉnh $R_{TG}$ tại $2,5\,\text{V}$:** Do quá áp cổng giảm còn một nửa và hiệu ứng thân tăng $V_{thn}, |V_{tp}|$ cùng lúc ở giữa dải.
4. **So sánh TG MUX vs Static MUX:** TG MUX không khôi phục mức, phụ thuộc trở kháng nguồn lái $D$ và số tầng mắc nối tiếp; chỉ công bằng khi đo cùng bộ lái `inv_x1` và cùng tải.
