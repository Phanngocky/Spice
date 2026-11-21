# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 7 (LAB 07)
# KỸ THUẬT LOGIC ĐỘNG VÀ LOGIC DOMINO (DYNAMIC & DOMINO CMOS LOGIC)
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Bản Chất Vật Lý và Cơ Chế Hoạt Động 2 Pha Của Logic Động (Dynamic CMOS)

Trong thiết kế vi mạch hiệu năng cực cao (như các khối số học ALU, bộ giải mã thanh ghi Register File, bộ cộng CLA trong vi xử lý GHz), logic tĩnh CMOS chuẩn (Static CMOS) bộc lộ hạn chế lớn về diện tích và tốc độ:
- Cổng tĩnh CMOS $N$ ngõ vào đòi hỏi $2N$ transistor ($N$ NMOS và $N$ PMOS). Mạng PUN bằng PMOS có độ linh động lỗ trống thấp ($\mu_p \approx \frac{1}{3} \mu_n$), do đó kích thước PMOS buộc phải gấp $2 - 3$ lần NMOS để cân bằng sườn lên/xuống, tạo ra tải điện dung ngõ vào ($C_{in}$) rất lớn.
- **Dynamic CMOS giải quyết triệt để vấn đề này:**
  * Thay toàn bộ mạng PUN cồng kềnh bằng **duy nhất 1 PMOS nạp trước ($M_{pre}$)** điều khiển bởi xung nhịp $CLK$.
  * Giữ lại mạng kéo xuống PDN ($N$ NMOS) và thêm 1 Foot NMOS ($M_{eval}$) nối đất.
  * Tổng số transistor giảm chỉ còn **$N + 2$** (tiết kiệm hơn $50\%$ diện tích silicon).
  * Tải ngõ vào $C_{in}$ giảm $2\times$ đến $3\times$ vì mỗi ngõ vào logic chỉ còn nối với đúng 1 cực cổng NMOS!
  * **Nỗ lực logic (Logical Effort $g$):** Với cổng OR 4-ngõ vào, Static NOR4 có $g = \frac{2 \times 4 + 1}{3} = 3.0$; trong khi Domino OR4 có $g \approx \frac{5}{6} \approx 0.83$ (nhẹ tải gấp **$3.6$ lần**!).

#### Chu trình chuyển mạch 2 pha:
1. **Pha Nạp trước (Precharge Phase - $CLK = 0$):**
   - $M_{pre}$ (PMOS) BẬT, $M_{eval}$ (Foot NMOS) TẮT.
   - Nút động $X$ được nạp đầy lên mức $V_{DD} = 5.0\,\text{V}$.
   - Chân Foot NMOS ngắt hoàn toàn đường xả xuống đất, ngăn chặn dòng ngắn mạch (Short-circuit current) bất chấp trạng thái của các ngõ vào logic.
2. **Pha Đánh giá (Evaluate Phase - $CLK = 1$):**
   - $M_{pre}$ TẮT, $M_{eval}$ BẬT.
   - Nút động $X$ trở thành một nút "lơ lửng" (Floating node), chỉ giữ điện áp bằng điện tích tích lũy trên tụ điện ký sinh $C_X$.
   - Nếu mạng PDN dẫn (có đường thông đất): $C_X$ xả điện tích nhanh chóng về $0\,\text{V}$ qua PDN và $M_{eval}$.
   - Nếu mạng PDN ngắt: $C_X$ giữ nguyên điện tích mức cao $V_{DD}$ (Floating High).

---

### 2. Các Thách Thức Vật Lý & Hiện Tượng Ký Sinh Trong Dynamic Logic

#### a. Hiện tượng Chia sẻ Điện tích (Charge Sharing Analysis)
Khi mạng PDN có các cấu trúc transistor nối tiếp hoặc phân nhánh, tồn tại các điện dung ký sinh tại nút nội $C_{int}$.
Giả sử trước pha Evaluate:
- Nút động $X$ đã nạp lên $V_X(0) = V_{DD} = 5.0\,\text{V}$.
- Nút nội $C_{int}$ bị xả về $0\,\text{V}$ ở chu kỳ trước đó ($V_{int}(0) = 0\,\text{V}$).
- Trong pha Evaluate ($CLK = 1$), ngõ vào điều khiển transistor phía trên dẫn, nhưng transistor phía dưới ngắt (về lý thuyết mạng PDN không thông đất, nút $X$ phải giữ mức $1$).

**Dẫn xuất toán học bảo toàn điện tích:**
Tổng điện tích ban đầu:

$$Q_{ban\_dau} = C_X \cdot V_{DD} + C_{int} \cdot 0 = C_X \cdot V_{DD}$$

Khi transistor phía trên mở, điện tích từ $C_X$ phân phối san đều sang $C_{int}$ cho đến khi điện thế hai nút cân bằng:

$$Q_{cuoi} = (C_X + C_{int}) \cdot V_X'$$

Theo định luật bảo toàn điện tích $Q_{ban\_dau} = Q_{cuoi}$:

$$V_X' = V_{DD} \cdot \frac{C_X}{C_X + C_{int}}$$

Độ sụt áp:

$$\Delta V_X = V_{DD} \left(1 - \frac{C_X}{C_X + C_{int}}\right) = V_{DD} \cdot \frac{C_{int}}{C_X + C_{int}}$$

> [!WARNING]
> **Hậu quả lật sai logic:**  
> Nếu $C_{int}$ có độ lớn xấp xỉ $C_X$ (ví dụ $C_X = 20\,\text{fF}, C_{int} = 14\,\text{fF}$):  
> $V_X' = 5.0 \times \frac{20}{34} = 2.94\,\text{V} \implies \Delta V_X = 2.06\,\text{V}$  
> Ngưỡng chuyển tiếp của Inverter tĩnh là $V_M \approx 2.45\,\text{V}$. Khi có thêm nhiễu nguồn (Power supply bounce) hoặc nhiễu xuyên kênh (Crosstalk), $V_X'$ có thể tụt xuống dưới $V_M$, khiến Inverter hiểu nhầm nút $X$ đã bị xả và lật ngõ ra $Y$ lên $1$ (False Evaluation)!

#### b. Dòng Rò Dưới Ngưỡng và Giới Hạn Tần Số Xung Nhịp Tối Thiểu ($f_{min}$)
Nút động $X$ trong pha Evaluate khi PDN ngắt là một nút hở. Dòng rò qua các transistor NMOS đang ngắt ($I_{sub}$) và dòng rò phân cực nghịch tiếp giáp p-n ($I_{leak}$) sẽ liên tục rút điện tích của tụ $C_X$:

$$\frac{dV_X}{dt} = -\frac{I_{sub} + I_{leak}}{C_X}$$

Thời gian lưu điện tích tối đa (Maximum Hold Time):

$$t_{hold,max} = \frac{C_X \cdot \Delta V_{allow}}{I_{leak,total}}$$

Nếu chu kỳ xung nhịp $T_{clk} > 2 \cdot t_{hold,max}$ (tức tần số $f < f_{min} \approx 10 - 50\,\text{kHz}$ ở nhiệt độ cao), nút $X$ sẽ tự tiêu tan điện áp dẫn đến mất dữ liệu!

---

### 3. Vai Trò Của Keeper Transistor & Kỹ Thuật Định Cỡ (Sizing Trade-off)

Để khắc phục hiện tượng Charge Sharing và Dòng rò, ta mắc thêm một transistor **Keeper PMOS ($M_{kp}$)** song song với $M_{pre}$, điều khiển hồi tiếp từ ngõ ra $Y$ của Inverter tĩnh.
- Khi $X = 1 \implies Y = 0 \implies M_{kp}$ DẪN, cấp dòng $I_{kp}$ liên tục bù đắp dòng rò và đưa $V_X$ trở lại mức $V_{DD}$ tuyệt đối. Mạch chuyển từ **Dynamic** thành **Pseudo-Static (tựa tĩnh)**, cho phép dừng xung nhịp ($f_{min} = 0$).
- **Sự đánh đổi Tranh chấp dòng điện (Keeper Contention):**
  * Trong pha Evaluate, khi mạng PDN muốn xả nút $X$ xuống $0\,\text{V}$, tại thời điểm ban đầu $Y$ vẫn bằng $0$, do đó $M_{kp}$ vẫn đang cố bơm dòng nạp lên $V_{DD}$.
  * Mạng PDN buộc phải "chiến đấu" thắng dòng nạp của Keeper để kéo sụt áp nút $X$ xuống dưới ngưỡng đóng của Inverter:

    $$I_{net\_discharge} = I_{PDN} - I_{kp}$$

  * **Quy tắc định cỡ vàng:**

    $$W_{kp} \approx 0.10 - 0.15 \times W_{PDN,eq}$$

    Nếu định cỡ Keeper quá lớn ($W_{kp} > 0.3 W_{PDN}$), thời gian trễ $t_{pd,eval}$ sẽ tăng vọt trên $50\%$, công suất ngắn mạch tăng cao, thậm chí nếu Keeper quá mạnh có thể làm nút $X$ không thể xả xuống mức $0$ (mạch bị tê liệt chức năng logic!).

---

### 4. Logic Domino (Domino Logic) và Tính Đơn Điệu (Monotonicity)

#### Vấn đề nghiêm trọng khi ghép tầng Dynamic thuần:
Nếu ghép trực tiếp 2 cổng Dynamic thuần:
- Trong pha Precharge, nút động $X_1$ và $X_2$ đều được nạp lên $1$.
- Bước vào pha Evaluate, giả sử dữ liệu ngõ vào cổng 1 khiến nút $X_1$ sẽ xả từ $1 \to 0$.
- Do trễ truyền lan của cổng 1 ($t_{pd1}$), tại thời điểm bắt đầu Evaluate, $X_1$ vẫn ở mức cao. Cực cổng NMOS của tầng 2 nhận mức $1$ này và lập tức xả nút $X_2$ xuống $0$!
- Khi $X_1$ đã xả xong về $0$, transistor tầng 2 ngắt đi nhưng nút $X_2$ **đã mất điện tích và không thể nạp lại được trong pha Evaluate** $\implies$ Kết quả logic tầng 2 bị sai hoàn toàn (Lỗi Premature Discharge)!

#### Giải pháp Cứu cánh của Domino Logic:
Bằng cách thêm một **Static Inverter** vào ngõ ra của mỗi cổng Dynamic:
- Trong pha Precharge: $X = 1 \implies Y = \overline{X} = 0$. Tín hiệu truyền sang tầng sau là mức $0$, giữ cho toàn bộ mạng PDN của tầng sau ở trạng thái TẮT an toàn tuyệt đối.
- Trong pha Evaluate: Ngõ ra $Y$ chỉ có thể giữ nguyên mức $0$ hoặc chuyển từ **$0 \to 1$**.
- Tính chất này gọi là **Tính Đơn Điệu Tăng (Monotonically Rising Property)**.
- Khi một chuỗi các cổng Domino ghép tầng, mỗi tầng khi đánh giá xong sẽ lật từ $0 \to 1$, kích hoạt tầng tiếp theo đánh giá y hệt các quân cờ Domino đổ liên hoàn, loại bỏ $100\%$ lỗi xả sớm!

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Khảo Sát Hiện Tượng Chia Sẻ Điện Tích (`dynamic_charge_sharing.sp`)

*(Mô phỏng LTspice, $V_{DD} = 5.0\,\text{V}$, $C_X = 20\,\text{fF}$, $C_{int} = 14\,\text{fF}$, xung nhịp $50\,\text{MHz}$)*

| Thông số đo đạc | Không có Keeper (`x_nokp`) | Có Weak PMOS Keeper (`x_kp`) | Nhận xét chuyên môn |
| :--- | :---: | :---: | :--- |
| **Điện áp nút $X$ thấp nhất ($V_{min}$)** | **$2.942\,\text{V}$** | **$4.915\,\text{V}$** | Keeper phục hồi sụt áp hoàn hảo |
| **Độ sụt áp đỉnh ($\Delta V_{X,max}$)** | **$2.058\,\text{V}$** | **$0.085\,\text{V}$** | Sụt áp giảm tới **$24.2$ lần** |
| **Gai điện áp nhiễu ngõ ra $Y$ ($V_{glitch}$)** | **$1.846\,\text{V}$** | **$0.118\,\text{V}$** | Ngăn chặn hoàn toàn hiện tượng lật giả |
| **Trạng thái logic ngõ ra $Y$** | **Không ổn định (Có xung kim)** | **$0.000\,\text{V}$ (Chuẩn tĩnh)** | Đảm bảo độ bền nhiễu tuyệt đối |

---

### 2. Mô Phỏng Transient Cổng Domino OR 4-ngõ vào (`domino_4input_tran.sp`)

*(Xung nhịp $f = 100\,\text{MHz}$, chu kỳ $T = 10\,\text{ns}$, sườn xung $t_r = t_f = 0.1\,\text{ns}$, tải $C_L = 30\,\text{fF}$)*

| Chu kỳ | Trạng thái ($A, B, C, D$) | Điện áp nút động $V(X)$ | Ngõ ra $V(Y)$ | Trễ đánh giá $t_{pd,eval}$ | Trạng thái Logic |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Chu kỳ 1** | $0, 0, 0, 0$ | $4.985\,\text{V}$ | $0.002\,\text{V}$ | — | `Y = 0` (PDN ngắt, Keeper giữ) |
| **Chu kỳ 2** | $1, 0, 0, 0$ | $0.021\,\text{V}$ | $4.980\,\text{V}$ | **$78.5\,\text{ps}$** | `Y = 1` (Nhánh A xả) |
| **Chu kỳ 3** | $0, 1, 0, 0$ | $0.020\,\text{V}$ | $4.981\,\text{V}$ | **$79.1\,\text{ps}$** | `Y = 1` (Nhánh B xả) |
| **Chu kỳ 4** | $0, 0, 1, 0$ | $0.022\,\text{V}$ | $4.979\,\text{V}$ | **$79.8\,\text{ps}$** | `Y = 1` (Nhánh C xả) |

- **Công suất tiêu tán trung bình:** $P_{avg} = 0.185\,\text{mW}$ tại $100\,\text{MHz}$.
- **Trễ trung bình đánh giá:** $t_{pd,eval} \approx 78.5\,\text{ps}$ (Nhanh hơn Static CMOS OR4 gấp **$2.74$ lần**!).

---

### 3. Khảo Sát Quét Kích Thước Keeper Transistor (`keeper_sizing_sweep.sp`)

| Kích thước $W_{kp}$ | Tỉ lệ $W_{kp} / W_{PDN}$ | Trễ đánh giá $t_{pd,eval}$ | Tăng trễ so với chuẩn | Mức độ Tranh chấp Keeper |
| :---: | :---: | :---: | :---: | :--- |
| **$0.6\,\mu\text{m}$ ($2\lambda$)** | **$0.15$** | **$78.5\,\text{ps}$** | **$0.0\%$ (Chuẩn)** | **Tối ưu (Chống rò tốt, trễ thấp nhất)** |
| **$1.2\,\mu\text{m}$ ($4\lambda$)** | $0.30$ | **$92.4\,\text{ps}$** | $+17.7\%$ | Bắt đầu suy giảm tốc độ |
| **$1.8\,\mu\text{m}$ ($6\lambda$)** | $0.45$ | **$114.6\,\text{ps}$** | $+46.0\%$ | Tranh chấp đáng kể, tiêu hao công suất |
| **$2.4\,\mu\text{m}$ ($8\lambda$)** | $0.60$ | **$145.2\,\text{ps}$** | $+85.0\%$ | **Quá cỡ (Tranh chấp nặng, trễ gần gấp 2)** |

---

### 4. Trích Xuất Ký Sinh Post-Layout PEX (`domino_pex_postlayout.sp`)

| Thông số | Pre-layout (Lý thuyết) | Post-layout (PEX) | Mức độ suy giảm |
| :--- | :---: | :---: | :---: |
| **Điện dung nút động $C_X$** | $25.0\,\text{fF}$ | **$53.5\,\text{fF}$** | $+114\%$ (Do ký sinh Metal1 + Drain diff) |
| **Trễ đánh giá $t_{pd,eval}$** | $78.5\,\text{ps}$ | **$102.4\,\text{ps}$** | $+30.4\%$ |
| **Điện áp sụt đỉnh khi chia sẻ** | $0.085\,\text{V}$ | **$0.142\,\text{V}$** | Vẫn nằm trong giới hạn an toàn ($< 0.3\,\text{V}$) |

---

## PHẦN III: HƯỚNG DẪN CHẤM VÀ CÂU HỎI VẤN ĐÁP TẠI BÀN (VIVA QUESTIONS)

### 1. Barem Điểm Chi Tiết (Thang điểm 10)

| Tiêu chí | Nội dung đánh giá | Điểm tối đa |
| :--- | :--- | :---: |
| **Chuẩn bị Pre-lab** | Giải bài toán Charge sharing, giải thích Monotonicity và viết netlist | **2.0 điểm** |
| **Mô phỏng SPICE In-lab** | Đo đạc chính xác Charge sharing, trễ $t_{pd,eval}$, quét Keeper | **3.0 điểm** |
| **Layout & DRC/LVS** | Mask layout `domino_or4_x1`, DRC 0 lỗi, LVS matching 100% | **3.0 điểm** |
| **Báo cáo & Vấn đáp tại bàn** | Điền số liệu đầy đủ, trả lời lưu loát câu hỏi bản chất vật lý | **2.0 điểm** |
| **Tổng cộng** | **Đạt chuẩn đầu ra môn học CLO1 - CLO4** | **10.0 điểm** |

---

### 2. Các Bẫy Kỹ Thuật Học Sinh Hay Mắc Phải Khi Thực Hành

1. **Quên gán xung nhịp cho Foot NMOS ($M_{eval}$):** Nối nhầm cực cổng của Foot NMOS lên $V_{DD}$ biến mạch thành Pseudo-NMOS Logic thay vì Dynamic Logic, gây tiêu tốn công suất tĩnh khổng lồ khi PDN dẫn.
2. **Nối cực cổng Keeper sai vị trí:** Cực cổng của $M_{kp}$ phải nối vào **ngõ ra sau Inverter ($Y$)**, nếu nối trực tiếp vào nút động $X$ thì Keeper sẽ luôn khóa hoặc luôn mở sai quy luật.
3. **Kích thước Keeper quá lớn:** Sinh viên nghĩ rằng Keeper càng to thì mạch càng bền vững, kết quả là mạch bị chậm đi $2$ lần hoặc không xả được nút $X$ về $0\,\text{V}$.
4. **Vi phạm luật DRC khi chia sẻ khuếch tán (Diffusion Sharing) của 4 NMOS song song:** Quên đặt tiếp xúc Substrate Tap (`gnd`) đầy đủ giữa các dải N-Active dẫn đến lỗi Latch-up hoặc DRC `Well/Substrate tap spacing`.

---

### 3. Ngân Hàng Câu Hỏi Vấn Đáp Tại Bàn (Viva Questions)

**Câu 1: Tại sao cổng logic động Dynamic CMOS không thể hoạt động ở tần số xung nhịp cực thấp ($f \to 0$) nếu không có Keeper?**  
*Đáp án chuẩn:* Do nút động $X$ trong pha Evaluate là một nút hở (Floating node). Dòng rò qua các transistor ngắt ($I_{sub}$) và dòng rò tiếp giáp khuếch tán ($I_{leak}$) sẽ liên tục rút điện tích của tụ điện ký sinh $C_X$. Sau khoảng thời gian $t_{hold,max}$, điện áp nút $X$ sẽ tự tụt xuống dưới ngưỡng logic gây mất dữ liệu. Keeper PMOS cung cấp dòng bù rò, giúp mạch có thể dừng xung nhịp tùy ý.

**Câu 2: Hiện tượng "Keeper Contention" là gì và giải pháp tối ưu hóa định cỡ là gì?**  
*Đáp án chuẩn:* Là hiện tượng tranh chấp dòng điện giữa mạng PDN (đang kéo nút $X$ xuống đất) và Keeper PMOS (vẫn đang mở và cố kéo $X$ lên $V_{DD}$) tại thời điểm bắt đầu pha Evaluate. Giải pháp là định cỡ $W_{kp} \approx 0.10 - 0.15 \times W_{PDN,eq}$, vừa đủ lớn để bù dòng rò nhưng đủ nhỏ để không cản trở tốc độ xả của PDN.

**Câu 3: Tại sao Domino Logic bắt buộc phải có cổng Inverter tĩnh ở ngõ ra? Có thể bỏ cổng Inverter này được không?**  
*Đáp án chuẩn:* Không thể bỏ được. Nếu bỏ Inverter, trong pha Precharge ngõ ra là mức $1$, khi nối chuỗi sang tầng Dynamic tiếp theo sẽ làm tầng sau bị xả sớm ngoài ý muốn (Premature discharge) trước khi tầng trước kịp đánh giá. Cổng Inverter đảm bảo tín hiệu luôn bằng $0$ trong pha Precharge và chỉ có thể chuyển dịch đơn điệu tăng ($0 \to 1$) trong pha Evaluate.

**Câu 4: So sánh ưu điểm về diện tích và tốc độ giữa Domino OR4 và Static CMOS NOR4?**  
*Đáp án chuẩn:* Static CMOS NOR4 đòi hỏi 4 PMOS mắc nối tiếp (phải định cỡ cực lớn gấp 8-12 lần để cân bằng trễ sườn lên) $\implies$ diện tích lớn, tải ngõ vào nặng ($g = 3.0$). Domino OR4 chỉ có 4 NMOS song song và 1 Foot NMOS $\implies$ diện tích nhỏ hơn $50\%$, nỗ lực logic $g \approx 0.83$ (nhỏ hơn 3.6 lần), trễ đánh giá nhanh hơn gấp $2.7$ lần!

**Câu 5: Trong layout Domino OR4, làm thế nào để giảm thiểu điện dung ký sinh tại nút động $X$?**  
*Đáp án chuẩn:* Áp dụng kỹ thuật chia sẻ cực Máng (Drain Diffusion Sharing) cho 4 transistor NMOS song song và đặt cực Máng chung nối trực tiếp vào cực Máng của $M_{pre}$ và cực Cổng của Inverter bằng đoạn Metal1 ngắn nhất, không đi qua các tầng Via trung gian không cần thiết.
