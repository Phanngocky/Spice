# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 8 (LAB 08)
# Ô NHỚ SRAM 6T VÀ MẠCH KHUẾCH ĐẠI CẢM NHẬN (VLSA)
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Đồng bộ với Teacher's Book Lab 08)*

> **Script kiểm chứng số liệu:** [verify_lab08_new.py](../../scripts/verify_lab08_new.py)  
> **Teacher's Book đầy đủ:** [Lab08_Teacher_Book.md](../../Teacher_Book/Lab08_Teacher_Book.md)  
> **Tiến trình công nghệ:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## 1. Tóm tắt Đính chính Kỹ thuật (Audit Lab 08)
1. **Giải quyết mâu thuẫn $V_Q$ khi đọc `'0'`:** Công thức bậc nhất cho $1,075\,\text{V} > V_{tn} = 0,70\,\text{V}$ ở $CR=2$. Nghiệm bậc hai chính xác cho $V_Q = \mathbf{0,789\,\text{V}}$ (không body effect) và $\mathbf{0,725\,\text{V}}$ (có body effect trên Access NMOS). Tiêu chí vật lý đúng là $V_Q < V_M$ của Inverter đối diện ($\mathbf{1,485\,\text{V}}$).
2. **Sức kéo khi ghi `'0'` (`PR`):** Với $K'_n / K'_p = 3$, tỉ số sức kéo Access ($4\lambda$) so với Load ($2\lambda$) là **$6\times$**, kéo nút $Q$ cân bằng ở $\mathbf{0,357\,\text{V}} \ll 1,485\,\text{V}$.
3. **Giá trị $SNM$ & Phương pháp đo:** $SNM_{hold} \approx \mathbf{1,303\,\text{V}}$ ($26,1\% V_{DD}$), $SNM_{read} \approx \mathbf{0,359\,\text{V}}$ ($7,2\% V_{DD}$, do $V_M$ dịch lên $2,090\,\text{V}$), không phải $0,62\,\text{V}$. Đo bằng phương pháp xoay trục $45^\circ$ tại **thùy nhỏ hơn**.
4. **Tách Đọc tĩnh vs Đọc động & Tường minh VLSA:** Dùng nguồn cố định $5\,\text{V}$ cho Đọc tĩnh ($V_Q$); dùng tụ $C_{BL}=1\,\text{pF}$ thả nổi cho Đọc động ($\Delta V_{BL}(t)$). Bổ sung sơ đồ `sense_amp_vlsa` (`Mp` $12\lambda$, `Mn` $8\lambda$, `Mn_tail` $12\lambda$, `Mn_pass` $4\lambda$), đo $t_{latch}$ cả hai chiều $\pm 150\,\text{mV}$ và đối sánh trực tiếp với đường đọc không VLSA.

---

## 2. Đáp án Chi tiết Pre-lab & Bảng Đối Chuẩn

### 2.1 Bảng $V_Q$ theo $CR$ (Nghiệm bậc hai)
- $CR = 1,0$: $1,259\,\text{V}$ (không body) / $1,123\,\text{V}$ (có body)
- $CR = 1,5$: $0,969\,\text{V}$ / $0,880\,\text{V}$
- **$CR = 2,0$: $\mathbf{0,789\,\text{V}}$ / $\mathbf{0,725\,\text{V}}$** (so với bậc nhất $1,075\,\text{V}$)
- $CR = 3,0$: $0,576\,\text{V}$ / $0,539\,\text{V}$ (đạt cả tiêu chí khắt khe $< 0,70\,\text{V}$)

### 2.2 Đáp án các thông số còn lại
- **Ngưỡng $V_M$ Inverter ($8\lambda/2\lambda$):** $1,485\,\text{V}$ (Hold) $\to$ dịch lên $2,090\,\text{V}$ (Read).
- **Mức $Q$ khi ghi `'0'`:** $0,357\,\text{V}$ (tỉ số sức kéo Access/Load = $6\times$).
- **$SNM_{hold}$ / $SNM_{read}$:** $1,303\,\text{V}$ / $0,359\,\text{V}$ (tỉ số $0,276$).
- **VLSA $t_{latch}$ ($\pm 150\,\text{mV}$):** Khoảng $70 - 200\,\text{ps}$ ($C_{so}=C_{sob}=20\,\text{fF}$).

---

## 3. Đáp án 3 Câu hỏi Thảo luận Post-lab
1. **Tiêu chí Read Disturb:** Công thức bậc nhất ước lượng quá cao ($1,075\,\text{V}$ vs $0,73-0,79\,\text{V}$); tiêu chí đúng là $V_Q < V_M$ của Inverter đối diện ($1,485\,\text{V}$), không phải $V_{tn}=0,70\,\text{V}$.
2. **Sức kéo ghi `'0'`:** Do $K'_n = 3 K'_p$, nên $PR = 0,5$ thực chất cho Access mạnh gấp $6\times$ Load, dễ dàng kéo $Q$ về $0,357\,\text{V}$.
3. **Input Offset VLSA:** Nếu $\Delta V_{os} = 100\,\text{mV} > \Delta V_{BL} = 80\,\text{mV}$ ngược dấu, VLSA sẽ chốt sai hướng và xuất bit logic sai.
