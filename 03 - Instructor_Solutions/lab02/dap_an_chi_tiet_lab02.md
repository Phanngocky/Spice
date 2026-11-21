# ĐÁP ÁN CHI TIẾT PHIẾU BÁO CÁO: BÀI 2 (LAB 02)
## THIẾT KẾ CỔNG LOGIC TĨNH NAND2 VÀ NOR2 CMOS
*(Tài liệu chuẩn dành riêng cho Giảng viên và Trợ giảng)*

---

### a. Phần Chuẩn bị (Pre-lab)

1. **Bảng kích thước transistor định cỡ lý thuyết:**

   | Cổng logic | Transistor | Vai trò | Kích thước $(W/L)$ theo $\lambda$ | Kích thước $(W/L)$ theo $\mu\text{m}$ | Điện trở dẫn hiệu dụng $R_{on}$ |
   | :--- | :---: | :---: | :---: | :---: | :---: |
   | **NAND2** | $M_{N1}, M_{N2}$ | PDN (nối tiếp) | **$8\lambda / 2\lambda$** | **$2.40\,\mu\text{m} / 0.60\,\mu\text{m}$** | $R_{on,N1} = R_{on,N2} =$ **$484.5\,\Omega$** ($R_{eq,N} = 969.0\,\Omega$) |
   | **NAND2** | $M_{P1}, M_{P2}$ | PUN (song song) | **$12\lambda / 2\lambda$** | **$3.60\,\mu\text{m} / 0.60\,\mu\text{m}$** | $R_{on,P1} = R_{on,P2} =$ **$992.1\,\Omega$** ($R_{eq,P,worst} = 992.1\,\Omega$) |
   | **NOR2** | $M_{N1}, M_{N2}$ | PDN (song song) | **$4\lambda / 2\lambda$** | **$1.20\,\mu\text{m} / 0.60\,\mu\text{m}$** | $R_{on,N1} = R_{on,N2} =$ **$969.0\,\Omega$** ($R_{eq,N,worst} = 969.0\,\Omega$) |
   | **NOR2** | $M_{P1}, M_{P2}$ | PUN (nối tiếp) | **$24\lambda / 2\lambda$** | **$7.20\,\mu\text{m} / 0.60\,\mu\text{m}$** | $R_{on,P1} = R_{on,P2} =$ **$496.0\,\Omega$** ($R_{eq,P} = 992.1\,\Omega$) |

2. **Dự đoán thời gian trễ lý thuyết ($C_L = 50\,\text{fF}$):**
   - **Cổng NAND2:**
     * $t_{pHL} = 0.69 \times 969.0 \times 50\text{f} =$ **$33.43\,\text{ps}$**.
     * $t_{pLH,worst} = 0.69 \times 992.1 \times 50\text{f} =$ **$34.23\,\text{ps}$** (khi chỉ 1 PMOS dẫn).
     * $t_{pLH,best} = 0.69 \times 496.0 \times 50\text{f} =$ **$17.11\,\text{ps}$** (khi 2 PMOS cùng dẫn).
   - **Cổng NOR2:**
     * $t_{pLH} = 0.69 \times 992.1 \times 50\text{f} =$ **$34.23\,\text{ps}$**.
     * $t_{pHL,worst} = 0.69 \times 969.0 \times 50\text{f} =$ **$33.43\,\text{ps}$** (khi chỉ 1 NMOS dẫn).
     * $t_{pHL,best} = 0.69 \times 484.5 \times 50\text{f} =$ **$16.72\,\text{ps}$** (khi 2 NMOS cùng dẫn).

3. **Sơ đồ que Stick Diagram của cổng `NAND2_X1`:**
   - Tiêu chí chấm:
     * Dải P-Active liên tục trong N-Well; dải N-Active liên tục trên P-Substrate.
     * 2 dải Polysilicon song song $A$ và $B$ thẳng đứng (chu trình Euler $A-B$).
     * PMOS: Cực Drain của $M_{P1}$ và $M_{P2}$ nối chung bằng tiếp xúc Metal 1 ra `out` (chia sẻ vùng khuếch tán giữa 2 transistor). Hai cực Source nằm ở hai phía ngoài nối lên $V_{DD}$.
     * NMOS: $M_{N1}$ (cổng A) nối ra `out`, $M_{N2}$ (cổng B) nối xuống $GND$, nút giữa là nút nội khuếch tán tự nhiên (không cần contact).

---

### b. Phần Thực hành (In-lab)

1. **Khảo sát đặc tuyến VTC của cổng NAND2:**
   - Khi ngõ vào $B = 5\,\text{V}$ cố định, quét $V_A$: $V_M =$ **$2.45 - 2.52\,\text{V}$**.
   - Khi nối chung hai ngõ vào $A = B = V_{in}$: $V_M =$ **$2.30 - 2.38\,\text{V}$** (dịch nhẹ về bên trái).
   - *Giải thích:* Khi $A=B$, cả 2 PMOS cùng dẫn song song làm tăng gấp đôi độ dẫn kéo lên ($2\beta_p$), trong khi PDN vẫn là chuỗi nối tiếp giữ nguyên độ dẫn $\beta_n$, kéo điện thế chuyển mạch dịch nhẹ về phía có dòng dẫn mạnh hơn.

2. **Bảng đo trễ quá độ (Transient) Pre-layout của cổng NAND2 ($C_L = 50\,\text{fF}$):**

   | Kịch bản kích thích | Ngõ vào $A$ | Ngõ vào $B$ | $t_{pHL}$ (ps) | $t_{pLH}$ (ps) | $t_{pd}$ trung bình (ps) |
   | :--- | :---: | :---: | :---: | :---: | :---: |
   | **Ca 1 ($A$ chuyển mạch trễ)** | Xung $0 \to 5\text{V}$ | $5.0\,\text{V}$ tĩnh | **$48 - 55$** | **$50 - 60$** | **$49 - 57$** |
   | **Ca 2 ($B$ chuyển mạch trễ)** | $5.0\,\text{V}$ tĩnh | Xung $0 \to 5\text{V}$ | **$58 - 68$** | **$50 - 60$** | **$54 - 64$** |
   | **Ca 3 ($A, B$ cùng chuyển mạch)**| Xung $0 \to 5\text{V}$ | Xung $0 \to 5\text{V}$ | **$50 - 58$** | **$26 - 32$** | **$38 - 45$** |

   *Nhận xét:* $t_{pHL}$ của Ca 2 chậm hơn Ca 1 từ **$15\% - 25\%$** vì khi $B$ chuyển đổi sau, nút nội $X_n$ đã bị nạp điện tích từ trước và phải xả đồng thời cả điện tích nút nội lẫn tải dung $C_L$. Trong Ca 3, khi cả 2 PMOS cùng dẫn, $t_{pLH}$ giảm gần một nửa (từ $\approx 55\,\text{ps}$ xuống $\approx 29\,\text{ps}$).

3. **Bảng đo trễ quá độ (Transient) Pre-layout của cổng NOR2 ($C_L = 50\,\text{fF}$):**

   | Kịch bản kích thích | Ngõ vào $A$ | Ngõ vào $B$ | $t_{pLH}$ (ps) | $t_{pHL}$ (ps) | $t_{pd}$ trung bình (ps) |
   | :--- | :---: | :---: | :---: | :---: | :---: |
   | **Ca 1 ($A$ chuyển mạch trễ)** | Xung $0 \to 5\text{V}$ | $0.0\,\text{V}$ tĩnh | **$58 - 70$** | **$46 - 55$** | **$52 - 62$** |
   | **Ca 2 ($B$ chuyển mạch trễ)** | $0.0\,\text{V}$ tĩnh | Xung $0 \to 5\text{V}$ | **$52 - 62$** | **$46 - 55$** | **$49 - 58$** |
   | **Ca 3 ($A, B$ cùng chuyển mạch)**| Xung $0 \to 5\text{V}$ | Xung $0 \to 5\text{V}$ | **$55 - 65$** | **$24 - 30$** | **$39 - 47$** |

4. **Kết quả Layout và Kiểm chứng Vật lý:**
   - Kích thước tế bào NAND2: Chiều rộng $W \approx 28 - 32\lambda$ ($8.4 - 9.6\,\mu\text{m}$); Chiều cao $H \approx 40 - 48\lambda$ ($12.0 - 14.4\,\mu\text{m}$).
   - Diện tích NAND2: $\approx 100 - 138\,\mu\text{m}^2$.
   - Số lỗi DRC: **0 errors**.
   - Kết quả LVS: **"Cells are topologically equivalent (MATCH)"**.

5. **Bảng So sánh PPA giữa NAND2 và NOR2:**

   | Tiêu chí so sánh | Cổng NAND2_X1 | Cổng NOR2_X1 | Tỉ số ($\frac{\text{NOR2}}{\text{NAND2}}$) | Đánh giá ưu thế |
   | :--- | :---: | :---: | :---: | :---: |
   | **Tổng bề rộng kênh $\sum W$** | $12.0\,\mu\text{m}$ | $16.8\,\mu\text{m}$ | **$+40.0\%$** | NAND2 nhỏ hơn vượt trội |
   | **Điện dung ngõ vào Pin A ($C_{in}$)** | $6.0\,\mu\text{m} \times C_{ox}$ | $8.4\,\mu\text{m} \times C_{ox}$ | **$+40.0\%$** | NAND2 ít tải cho tầng lái |
   | **Diện tích Layout hình học** | $\sim 115\,\mu\text{m}^2$ | $\sim 165\,\mu\text{m}^2$ | **$+43.5\%$** | NAND2 tiết kiệm silicon |
   | **Trễ sườn lên Post-layout ($t_{pLH}$)** | $\sim 70\,\text{ps}$ | $\sim 95\,\text{ps}$ | **$+35.7\%$** | NAND2 chuyển mạch nhanh hơn |

6. **Đáp án Câu hỏi Phân tích:**
   - *Câu 1:* Cổng NAND luôn chiếm ưu thế tuyệt đối vì hạt tải điện tử trong NMOS có độ linh động cao gấp 3 lần lỗ trống trong PMOS ($\mu_n \approx 3\mu_p$). Để cân bằng trễ, chuỗi nối tiếp trong NAND là NMOS ($W_n = 8\lambda$), trong khi chuỗi nối tiếp trong NOR là PMOS ($W_p = 24\lambda$). Do đó, cổng NOR2 tốn thêm $40\%$ tổng bề rộng transistor, diện tích layout phình to $\approx 43\%$, và điện dung ngõ vào tăng $40\%$ làm toàn bộ chuỗi mạch logic bị chậm lại.
   - *Câu 2:* Kỹ thuật chia sẻ vùng khuếch tán (Abutment) giúp gộp chung hai cực má (Drain) của transistor nằm cạnh nhau vào cùng một vùng bán dẫn, loại bỏ khoảng cách cách ly Active-Active ($3\lambda$) và giảm một nửa diện tích khuếch tán cực má ($AD, PD$). Điều này giúp thu hẹp đáng kể chiều rộng tế bào và giảm một nửa điện dung ký sinh nút ngõ ra, trực tiếp nâng cao tốc độ chuyển mạch của cổng.
   - *Câu 3:* Trong cổng NAND 4 ngõ vào (NAND4), để giữ điện trở kéo xuống bằng Inverter, kích thước 4 NMOS nối tiếp phải là $W_n = 4 \times 4\lambda = 16\lambda = 4.8\,\mu\text{m}$. Việc mắc nối tiếp từ 4 transistor trở lên sẽ khiến diện tích khuếch tán nút nội tăng theo hàm số bậc hai ($O(N^2)$), tổng điện dung ký sinh nút nội tích lũy rất lớn làm trễ truyền lan tăng vọt và suy giảm lề nhiễu động học. Trong công nghiệp vi mạch, chuẩn tế bào thường cấm mắc chuỗi nối tiếp quá 3–4 transistor.
