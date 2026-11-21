# ĐÁP ÁN CHI TIẾT PHIẾU BÁO CÁO: BÀI 1 (LAB 01)
## ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER
*(Tài liệu chuẩn dành riêng cho Giảng viên và Trợ giảng)*

---

### a. Phần Chuẩn bị (Pre-lab)

1. **Trích xuất tham số từ `C5_models.txt`:**
   - NMOS: `VTO` = **$0.7000\,\text{V}$** ; `KP` = **$120.0\,\mu\text{A/V}^2$** ; `TOX` = **$9.5 \times 10^{-9}\,\text{m}$** ($9.5\,\text{nm}$).
   - PMOS: `VTO` = **$-0.8000\,\text{V}$** ; `KP` = **$40.0\,\mu\text{A/V}^2$** ; `TOX` = **$9.5 \times 10^{-9}\,\text{m}$** ($9.5\,\text{nm}$).

2. **Tính toán kích thước và trễ lý thuyết ($V_{DD} = 5.0\,\text{V}$):**
   - Tỉ số kích thước lý thuyết: $\frac{(W/L)_p}{(W/L)_n} = \frac{\mu_n}{\mu_p} = \frac{120}{40} =$ **$3.00$** (hoặc $3.36$ nếu giải tích chính xác theo ngưỡng $V_{th}$).
   - Kích thước lựa chọn: NMOS ($W_n/L_n$) = **$1.20\,\mu\text{m} / 0.60\,\mu\text{m}$ ($4\lambda / 2\lambda$)** ; PMOS ($W_p/L_p$) = **$3.60\,\mu\text{m} / 0.60\,\mu\text{m}$ ($12\lambda / 2\lambda$)**.
   - Điện trở dẫn hiệu dụng: $R_{on,n} =$ **$969\,\Omega$ ($0.97\,\text{k}\Omega$)** ; $R_{on,p} =$ **$992\,\Omega$ ($0.99\,\text{k}\Omega$)**.
   - Dự đoán trễ với $C_L = 50\,\text{fF}$:
     * $t_{pHL} = 0.69 \times 969 \times 50\text{f} =$ **$33.4\,\text{ps}$**.
     * $t_{pLH} = 0.69 \times 992 \times 50\text{f} =$ **$34.2\,\text{ps}$**.
     * $t_{pd} =$ **$33.8\,\text{ps}$**.

3. **Sơ đồ que (Stick Diagram):**
   - Tiêu chí chấm:
     * Hai thanh ray Metal 1 song song ($V_{DD}$ trên, $GND$ dưới).
     * Dải Poly liên tục chạy dọc cắt qua P-Active (nằm trong N-Well) và N-Active.
     * Cực Drain nối chung bằng Metal 1 ra ngõ xuất `out`.
     * Đầy đủ 2 tiếp xúc Taps: N-Well tap nối $V_{DD}$, Substrate tap nối $GND$.

4. **Câu lệnh SPICE đo trễ (.MEAS) chuẩn:**
   ```spice
   .MEASURE TRAN tpHL TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 FALL=1
   .MEASURE TRAN tpLH TRIG V(in)=2.5 FALL=1 TARG V(out)=2.5 RISE=1
   .MEASURE TRAN tpd PARAM (tpHL + tpLH)/2
   .MEASURE TRAN trise TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1
   .MEASURE TRAN tfall TRIG V(out)=4.5 FALL=1 TARG V(out)=0.5 FALL=1
   ```

---

### b. Phần Thực hành (In-lab)

1. **Kết quả đo đặc tính I-V của MOSFET:**

   | Tham số trích xuất | NMOS ($W=1.2\mu\text{m}, L=0.6\mu\text{m}$) | PMOS ($W=3.6\mu\text{m}, L=0.6\mu\text{m}$) |
   | :--- | :---: | :---: |
   | **Điện áp ngưỡng thực nghiệm ($V_{th}$)** | **$0.69 - 0.71\,\text{V}$** | **$-0.79 - -0.81\,\text{V}$** |
   | **Dòng bão hòa cực đại $I_{DS,max}$** | **$1.8 - 2.2\,\text{mA}$** | **$1.7 - 2.1\,\text{mA}$** |
   | **Hệ số điều chế kênh $\lambda$** | **$0.02 - 0.05\,\text{V}^{-1}$** | **$0.03 - 0.06\,\text{V}^{-1}$** |

2. **Kết quả phân tích đường cong truyền đạt VTC:**
   - Điện áp chuyển mạch đo được: $V_M =$ **$2.45 - 2.52\,\text{V}$** (Độ lệch so với $2.5\,\text{V}$: $\le 2\%$).
   - Điện áp vào mức thấp: $V_{IL} =$ **$1.80 - 2.10\,\text{V}$**.
   - Điện áp vào mức cao: $V_{IH} =$ **$2.75 - 2.90\,\text{V}$**.
   - Lề nhiễu logic mức thấp: $NM_L =$ **$1.80 - 2.10\,\text{V}$** ($NM_L = V_{IL} - 0$).
   - Lề nhiễu logic mức cao: $NM_H =$ **$2.10 - 2.25\,\text{V}$** ($NM_H = 5.0 - V_{IH}$).

3. **Kết quả đo trễ quá độ (Transient) Pre-layout:**

   | Tải dung $C_L$ | $t_{pHL}$ (ps) | $t_{pLH}$ (ps) | $t_{pd}$ trung bình (ps) | Thời gian tăng $t_r$ (ps) | Thời gian giảm $t_f$ (ps) |
   | :---: | :---: | :---: | :---: | :---: | :---: |
   | **$10\,\text{fF}$** | **$15 - 22$** | **$16 - 24$** | **$16 - 23$** | **$30 - 45$** | **$28 - 40$** |
   | **$50\,\text{fF}$** | **$45 - 55$** | **$48 - 58$** | **$47 - 56$** | **$110 - 130$** | **$100 - 120$** |
   | **$100\,\text{fF}$** | **$85 - 100$** | **$90 - 105$** | **$88 - 102$** | **$210 - 240$** | **$190 - 220$** |

   *Nhận xét:* Trễ truyền lan $t_{pd}$ phụ thuộc tuyến tính chặt chẽ vào tải dung $C_L$ theo hàm $t_{pd} = p + g \times h$ (phù hợp hoàn hảo với lý thuyết Logical Effort).

4. **Kết quả Thiết kế Mask Layout và Kiểm chứng Vật lý:**
   - Kích thước tế bào chuẩn: Chiều rộng $W \approx 20 - 24\lambda$ ($6.0 - 7.2\,\mu\text{m}$); Chiều cao $H \approx 40 - 48\lambda$ ($12.0 - 14.4\,\mu\text{m}$).
   - Diện tích tế bào: $\approx 70 - 105\,\mu\text{m}^2$.
   - Số lỗi DRC: **0 errors**.
   - Kết quả LVS: **"Cells are topologically equivalent (MATCH)"**.

5. **Bảng Đối chiếu Tổng hợp 3 Chiều ($C_L = 50\,\text{fF}$):**

   | Đại lượng kỹ thuật | [1] Lý thuyết tính tay | [2] SPICE Pre-layout | [3] SPICE Post-layout (PEX) | Sai số PEX vs Pre-layout |
   | :--- | :---: | :---: | :---: | :---: |
   | **Điện áp $V_M$ (V)** | $2.50\,\text{V}$ | $2.48\,\text{V}$ | $2.48\,\text{V}$ | $\approx 0\%$ |
   | **Lề nhiễu $NM_L$ (V)** | $2.00\,\text{V}$ | $1.95\,\text{V}$ | $1.95\,\text{V}$ | $\approx 0\%$ |
   | **Lề nhiễu $NM_H$ (V)** | $2.15\,\text{V}$ | $2.18\,\text{V}$ | $2.18\,\text{V}$ | $\approx 0\%$ |
   | **Trễ sườn xuống $t_{pHL}$ (ps)** | $33.4\,\text{ps}$ | $50.2\,\text{ps}$ | $68.5\,\text{ps}$ | **$+36.5\%$** |
   | **Trễ sườn lên $t_{pLH}$ (ps)** | $34.2\,\text{ps}$ | $53.1\,\text{ps}$ | $72.0\,\text{ps}$ | **$+35.6\%$** |
   | **Trễ trung bình $t_{pd}$ (ps)** | $33.8\,\text{ps}$ | $51.6\,\text{ps}$ | $70.2\,\text{ps}$ | **$+36.0\%$** |

6. **Đáp án Câu hỏi Phân tích:**
   - *Câu 1:* Trễ Post-layout tăng thêm $\sim 30-40\%$ do trong Layout thực tế, các tiếp giáp P-N cực Drain của NMOS và PMOS đóng góp thêm điện dung khuếch tán đáy ($C_{j} \times AD$) và chu vi thành bên ($C_{jsw} \times PD$). Ngoài ra, đường dây Metal 1 nối hai cực Drain và chân pad ngõ ra cũng có điện dung ký sinh dây dẫn nối đất. Tổng tải dung thực tế tại nút `out` tăng từ $50\,\text{fF}$ lên $\sim 70-75\,\text{fF}$.
   - *Câu 2:* Nếu thiếu tiếp xúc phân cực Substrate/Well Taps, chất nền và giếng N sẽ ở trạng thái nổi (floating). Khi có đột biến điện áp hoặc nhiễu xung, cấu trúc thyristor ký sinh p-n-p-n (tạo bởi PMOS, N-Well, P-Substrate và NMOS) sẽ bị kích hoạt dẫn bão hòa, tạo nên hiện tượng **Latch-up** làm ngắn mạch trực tiếp nguồn $V_{DD}$ xuống $GND$, dòng điện tăng vọt không kiểm soát gây cháy và phá hủy vi mạch.
   - *Câu 3:* Nếu chọn $W_p = W_n$, do độ linh động $\mu_p \approx \mu_n / 3$, dòng dẫn PMOS sẽ yếu hơn NMOS gấp 3 lần. Đường cong VTC sẽ bị lệch sang trái ($V_M$ tụt xuống $\sim 1.8\,\text{V}$), làm suy giảm nghiêm trọng lề nhiễu mức thấp $NM_L$, đồng thời trễ sườn lên $t_{pLH}$ sẽ lớn gấp 3 lần trễ sườn xuống $t_{pHL}$ (mất đối xứng động học). Thiết kế $W_p = W_n$ chỉ được chấp nhận trong các mạch yêu cầu tiết kiệm diện tích tối đa hoặc mạch NOR nhiều ngõ vào mắc song song.
