# HƯỚNG DẪN GIẢNG VIÊN & ĐÁP ÁN MẪU: BÀI LAB 00
## NHẬP MÔN MÔ PHỎNG MẠCH VỚI SPICE VÀ LTSPICE

> [!CAUTION]
> **TÀI LIỆU NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TA)**  
> Tuyệt đối không phân phát tài liệu này cho sinh viên. Tài liệu này cung cấp các giá trị chuẩn, kết quả tính toán giải tích và hướng dẫn chấm thi thực hành tại bàn.

---

### 1. ĐÁP ÁN TÍNH TOÁN LÝ THUYẾT (PRE-LAB)

1. **Phân biệt tiền tố đơn vị trong SPICE:**
   - `R = 4.7M` $\to$ SPICE hiểu là $4.7 \times 10^{-3}\,\Omega = 4.7\,\text{m}\Omega = 0.0047\,\Omega$.
   - Để biểu diễn $4.7\,\text{M}\Omega$, cách viết đúng: `4.7Meg` hoặc `4.7MEG`.
   - `C = 100p` $\to$ SPICE hiểu là $100 \times 10^{-12}\,\text{F} = 100\,\text{pF}$.
   - `C = 50f` $\to$ SPICE hiểu là $50 \times 10^{-15}\,\text{F} = 50\,\text{fF}$.

2. **Mạch Cầu Phân áp DC ($V_{in} = 5.0\,\text{V}, R_1 = 30\,\text{k}\Omega, R_2 = 20\,\text{k}\Omega$):**
   - $V_{out} = 5.0 \times \frac{20}{30 + 20} = 2.000\,\text{V}$.
   - Dòng điện qua mạch: $I_{in} = \frac{5.0}{50 \times 10^3} = 0.100\,\text{mA} = 100\,\mu\text{A}$.
   - Tổng công suất tiêu tán: $P_{total} = 5.0 \times 0.1 \times 10^{-3} = 0.500\,\text{mW} = 500\,\mu\text{W}$.

3. **Mạch Lọc Thông Thấp RC ($R = 10\,\text{k}\Omega, C = 10\,\text{nF}$):**
   - Hằng số thời gian: $\tau = R \times C = 10 \times 10^3 \times 10 \times 10^{-9} = 100.0\,\mu\text{s} = 0.100\,\text{ms}$.
   - Điện áp tại $t = \tau$: $V_{out}(\tau) = 5.0 \times (1 - e^{-1}) \approx 5.0 \times 0.63212 = 3.161\,\text{V}$.
   - Điện áp tại $t = 5\tau$: $V_{out}(5\tau) = 5.0 \times (1 - e^{-5}) \approx 5.0 \times 0.99326 = 4.966\,\text{V}$.
   - Tần số cắt lý thuyết:
     $$f_{-3\text{dB}} = \frac{1}{2\pi RC} = \frac{1}{2\pi \times 100 \times 10^{-6}} \approx \frac{1}{6.28318 \times 10^{-4}} \approx 1591.55\,\text{Hz} \approx 1.592\,\text{kHz}$$

---

### 2. KẾT QUẢ MÔ PHỎNG THAM CHIẾU (BENCHMARK RESULTS)

| Phân tích | Đại lượng đo | Giá trị Lý thuyết | Giá trị Mô phỏng SPICE | Ghi chú đánh giá |
| :--- | :--- | :---: | :---: | :--- |
| **`.OP`** | $V(vout)$ | $2.000\,\text{V}$ | $2.00000\,\text{V}$ | Sai số $0\%$ |
| **`.OP`** | $I(R1)$ | $0.100\,\text{mA}$ | $0.10000\,\text{mA}$ | Dòng điện âm nếu đo qua cực âm |
| **`.DC`** | $V_{out}$ tại $V_{in}=10\text{V}$ | $4.000\,\text{V}$ | $4.00000\,\text{V}$ | Tuyến tính hoàn hảo |
| **`.TRAN`** | Hằng số $\tau$ (`tau`) | $100.0\,\mu\text{s}$ | $99.8 - 100.2\,\mu\text{s}$ | Trích xuất từ `.MEAS` |
| **`.TRAN`** | Thời gian tăng $t_{rise}$ | $220.0\,\mu\text{s}$ | $219.5 - 220.5\,\mu\text{s}$ | $t_r \approx 2.2 \tau$ |
| **`.AC`** | Độ lợi dải thông $A_{V,0}$ | $1.000$ ($0\,\text{dB}$) | $0.000\,\text{dB}$ | Tại tần số thấp $10\,\text{Hz}$ |
| **`.AC`** | Tần số cắt $f_{-3\text{dB}}$ (`f_cut`) | $1.592\,\text{kHz}$ | $1.591 - 1.593\,\text{kHz}$ | Sai số $< 0.1\%$ |
| **`.AC`** | Pha tại tần số cắt | $-45.0^\circ$ | $-44.9^\circ - -45.1^\circ$ | Trục pha bên phải |
| **Model** | Dòng $I_D$ NMOS C5N ($5\text{V}/5\text{V}$)| $\sim 1.35\,\text{mA}$ | $1.30 - 1.40\,\text{mA}$ | Mô hình `N` từ `C5_models.txt` |

---

### 3. CÂU HỎI VẤN ĐÁP TẠI BÀN (ORAL QUESTIONS)

1. *Hỏi:* "Tại sao khi viết `R1 in out 10M`, mạch phân áp lại cho ra kết quả gần bằng 0V hoặc sai hoàn toàn?"  
   *Trả lời chuẩn:* Vì trong chuẩn SPICE, ký tự `M` hoặc `m` đại diện cho tiền tố `milli` ($10^{-3}$), tức $0.01\,\Omega$. Để SPICE hiểu là $10\,\text{M}\Omega$ ($10 \times 10^6\,\Omega$), bắt buộc phải viết là `10Meg` hoặc `10MEG`.
2. *Hỏi:* "Nếu trong phân tích `.TRAN`, tín hiệu xung vuông có sườn tăng $1\,\text{ns}$ mà ta đặt `Maximum Timestep` là $10\,\mu\text{s}$ thì điều gì sẽ xảy ra?"  
   *Trả lời chuẩn:* SPICE sẽ nội suy bước quá thô và bỏ qua (miss) hoàn toàn sườn dốc $1\,\text{ns}$, dẫn đến dạng sóng bị méo mó, góc bị gãy, và lệnh `.MEAS` sẽ báo lỗi không tìm thấy điểm chuyển mạch (Trigger not found).
3. *Hỏi:* "Ý nghĩa của việc khai báo nguồn `AC 1 0` trong phân tích đáp ứng tần số là gì?"  
   *Trả lời chuẩn:* Hàm truyền độ lợi được tính là $A_V = \frac{V_{out}}{V_{in}}$. Khi đặt biên độ $V_{in} = 1\,\text{V}$, thì điện áp đo được tại $V_{out}$ chính là độ lợi $A_V$. Khi biểu diễn trên thang decibel: $20 \log_{10}(V_{out}/1) = 20 \log_{10}(V_{out})$, giúp việc quan sát và tính toán độ lợi trực tiếp và thuận tiện nhất.
