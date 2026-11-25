# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB 08 — TEACHER'S BOOK: THIẾT KẾ Ô NHỚ BÁN DẪN TĨNH (6T SRAM CELL & SENSE AMPLIFIER)
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [lab-08-o-nho-sram-6t-va-sense-amplifier.md](../02%20-%20Student%20Workbook/lab-08-o-nho-sram-6t-va-sense-amplifier.md)  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab08/](../03%20-%20Instructor_Solutions/lab08/)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

# 8. LAB 8 — Ô NHỚ SRAM 6T VÀ SENSE AMPLIFIER (TỰ CHỌN / ĐỒ ÁN)

## 8.1 Ý cốt lõi sinh viên phải mang ra khỏi phòng máy
1. Hiểu mâu thuẫn thiết kế cốt lõi của ô nhớ SRAM 6T: Chế độ Đọc đòi hỏi Driver phải mạnh hơn Access (tránh phá hủy dữ liệu - Read Stability), trong khi chế độ Ghi đòi hỏi Access phải mạnh hơn Load (đè được dữ liệu cũ - Writeability).
2. Nắm vững phương pháp đo Lề nhiễu tĩnh (Static Noise Margin - SNM) thông qua đường cong cánh bướm (Butterfly Curve).
3. Hiểu nguyên lý hoạt động của Mạch khuếch đại cảm nhận (Sense Amplifier): sử dụng phản hồi dương để biến chênh lệch điện áp nhỏ ($\Delta V \approx 100-150\,\text{mV}$) thành mức logic đầy đủ trong thời gian cực ngắn, tiết kiệm $>90\%$ năng lượng nạp xả bitline.

---

## 8.2 Bản chất hai ràng buộc kích thước: CR và PR
Quy tắc kích thước vàng: $\text{Driver} > \text{Access} > \text{Load}$.

```
                            SRAM 6T CELL SCHEMATIC
                     BL                                    BLB
                      |                                     |
                [NMOS AX1: 4λ]                        [NMOS AX2: 4λ]
                (Gate: WL)                            (Gate: WL)
                      |                                     |
                      +-----------*-------------*-----------+
                      |           |             |           |
                      |        [PMOS L1]     [PMOS L2]      |
                      |         (W=2λ)        (W=2λ)        |
                    (Nút Q)       |             |        (Nút QB)
                      |         +----+-------+----+         |
                      |              | VDD   |              |
                [NMOS D1: 8λ]        |       |        [NMOS D2: 8λ]
                 (Gate: QB)          +-------+         (Gate: Q)
                      |                                     |
                     GND                                   GND
```

*Sơ đồ nguyên lý ô nhớ SRAM 6T và Mạch khuếch đại vi sai Sense Amplifier:*
- [sram_6t_cell_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/sram_6t_cell_schematic.png)
- [sense_amplifier_schematic.png](file:///d:/tam/VLSI_Spice/02%20-%20Student%20Workbook/images/sense_amplifier_schematic.png)

### a. Phân tích ổn định khi đọc (Read Stability & Cell Ratio CR)
Khi đọc nút $Q = 0\,\text{V}$, đường Bitline $BL$ đã được nạp trước lên $5,0\,\text{V}$. Khi $WL$ bật lên $5,0\,\text{V}$, dòng điện từ $BL$ đổ dồn qua Access Transistor $M_{AX1}$ vào nút $Q$ và thoát xuống GND qua Driver Transistor $M_{D1}$.
- Lúc này, $M_{AX1}$ ở vùng Bão hòa ($V_{DS} = 5,0 - V_Q > V_{GS} - V_{tn}$), trong khi $M_{D1}$ ở vùng Tuyến tính.
- Cân bằng dòng điện giữa hai transistor và đặt $u = V_{DD} - V_{tn} = 4,3\,\text{V}$:
  $$(u - V_Q)^2 = CR \cdot (2u V_Q - V_Q^2)$$
  Giải phương trình bậc hai cho điện áp đỉnh dâng lên tại nút $Q$:
  $$V_Q = u \cdot \left[1 - \sqrt{\frac{CR}{1 + CR}}\right]$$
  Với $CR = \frac{W_D}{W_{AX}} = \frac{8\lambda}{4\lambda} = 2,0$:
  $$V_Q = 4,3 \cdot \left[1 - \sqrt{\frac{2}{3}}\right] = 4,3 \cdot [1 - 0,8165] \approx \mathbf{0,789\,\text{V}}$$

**Chỗ cần chỉnh trong Handout gốc:**
Handout cũ ghi công thức gần đúng $V_Q \approx \frac{V_{DD} - V_{tn}}{2 \cdot CR} = \frac{4,3}{4} = 1,075\,\text{V}$ và yêu cầu $V_Q < V_{tn} = 0,70\,\text{V}$. Đây là một mâu thuẫn toán học nghiêm trọng (vừa tính ra $1,075\,\text{V}$ lại vừa đòi nhỏ hơn $0,70\,\text{V}$).  
Giảng viên giải thích cho sinh viên: Tiêu chí chuẩn xác không phải so với $V_{tn}$, mà $V_Q$ phải nhỏ hơn **ngưỡng lật của Inverter đối diện** ($M_{L2} - M_{D2}$). Với $W_D / W_L = 8\lambda / 2\lambda = 4,0$, ngưỡng lật của nửa ô nhớ đối diện lên tới $V_{trip} \approx 1,48\,\text{V}$. Do đó mức dâng $V_Q = 0,789\,\text{V}$ hoàn toàn an toàn dưới $1,48\,\text{V}$!

---


---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN SPICE BENCHMARK

# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 8 (LAB 08)
# THIẾT KẾ Ô NHỚ BÁN DẪN TĨNH (6T SRAM CELL & SENSE AMPLIFIER)
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Bộ môn ĐTVT, Trường ĐH SPKT – ĐHĐN)*

---

## PHẦN I: CƠ SỞ LÝ THUYẾT & NGUYÊN LÝ GIẢNG DẠY DÀNH CHO GIẢNG VIÊN

### 1. Kiến Trúc Tế Bào Ô Nhớ Tĩnh 6-Transistor (6T SRAM Cell)

Tế bào SRAM 6T là khối phần tử lưu trữ căn bản trong mọi vi xử lý hiện đại (chiếm tới $60 - 80\%$ tổng diện tích chip trong các bộ nhớ đệm Cache L1/L2/L3). Cấu trúc gồm:
- **Cặp Inverter ghép chéo (Bistable Cross-coupled Inverters):**
  * Inverter 1: PMOS tải $M_{L1}$ và NMOS lái $M_{D1}$, tạo nút lưu trữ $Q$.
  * Inverter 2: PMOS tải $M_{L2}$ và NMOS lái $M_{D2}$, tạo nút lưu trữ đảo $QB$ (hoặc $\bar{Q}$).
  * Cơ chế hồi tiếp dương (Positive Feedback) giúp tế bào duy trì trạng thái nhị phân ổn định vô hạn chừng nào nguồn $V_{DD}$ còn được cấp.
- **Hai Transistor truy xuất (Access Transistors):**
  * $M_{AX1}$ kết nối giữa cột Bitline ($BL$) và nút $Q$.
  * $M_{AX2}$ kết nối giữa cột Bitline đảo ($BLB$) và nút $QB$.
  * Cực cổng của cả hai Access NMOS được điều khiển chung bởi đường chọn từ hàng Wordline ($WL$).

---

### 2. Phân Tích Độ Ổn Định Đọc (Read Stability) & Dẫn Xuất Cell Ratio ($CR$)

Trong chu trình hoạt động của SRAM, **thao tác Đọc (Read) là thời điểm nguy hiểm nhất** dễ làm mất mát dữ liệu (hiện tượng **Read Disturb**).

#### Cơ chế vật lý khi Đọc:
1. Trước khi đọc, cả hai cột Bitline $BL$ và $BLB$ đều được mạch nạp trước (Precharge) đưa lên mức cao $V_{DD} = 5.0\,\text{V}$.
2. Giả sử ô nhớ đang lưu bit '0' ($V_Q = 0\,\text{V}, V_{QB} = 5.0\,\text{V}$).
3. Khi đường Wordline được kích hoạt ($WL = 5.0\,\text{V}$):
   - $M_{AX1}$ mở, xuất hiện dòng điện chạy từ Bitline $BL$ ($5.0\,\text{V}$), qua kênh dẫn của $M_{AX1}$, qua $M_{D1}$ và xả xuống đất $GND$.
   - Hai transistor $M_{AX1}$ và $M_{D1}$ tạo thành một mạch phân áp điện trở tại nút $Q$.
   - Điện áp nút $Q$ bị **dâng lên một khoảng $\Delta V_Q > 0$**.
4. **Nguy cơ lật dữ liệu:** Nút $Q$ đang nối thẳng vào cực cổng của $M_{D2}$. Nếu điện áp $V_Q$ dâng cao vượt quá điện áp ngưỡng mở $V_{tn} \approx 0.70\,\text{V}$ (hoặc ngưỡng chuyển tiếp $V_M$) của Inverter 2, $M_{D2}$ sẽ bật dẫn, kéo tụt nút $QB$ từ $5.0\,\text{V}$ xuống đất $\implies$ Cặp Inverter lập tức bị lật trạng thái và dữ liệu bị xóa sổ hoàn toàn!

#### Dẫn xuất giải tích điều kiện ổn định đọc:
Tại điểm cân bằng dòng điện giữa Access NMOS và Driver NMOS:
- $M_{AX1}$ hoạt động ở miền bão hòa (Saturation) vì $V_{DS} = V_{BL} - V_Q \approx 5.0 - 0.4 = 4.6\,\text{V} > V_{GS} - V_{tn} = 5.0 - V_Q - 0.70$:

  $$I_{AX} = \frac{1}{2} k'_n \left(\frac{W}{L}\right)_{AX} (V_{DD} - V_Q - V_{tn})^2$$

- $M_{D1}$ hoạt động ở miền tuyến tính (Linear / Triode) vì $V_{DS} = V_Q$ rất nhỏ ($< 0.5\,\text{V}$), $V_{GS} = V_{DD}$:

  $$I_{D1} = k'_n \left(\frac{W}{L}\right)_{D1} \left[ (V_{DD} - V_{tn}) V_Q - \frac{V_Q^2}{2} \right]$$

- Cân bằng dòng điện $I_{AX} = I_{D1}$ và bỏ qua số hạng bậc hai $V_Q^2 / 2 \approx 0$:

  $$\frac{1}{2} \left(\frac{W}{L}\right)_{AX} (V_{DD} - V_{tn})^2 \approx \left(\frac{W}{L}\right)_{D1} (V_{DD} - V_{tn}) V_Q$$

  $$V_Q \approx \frac{V_{DD} - V_{tn}}{2 \cdot CR}$$

  Trong đó **Cell Ratio ($CR$)** được định nghĩa là:

  $$CR = \frac{(W/L)_{driver}}{(W/L)_{access}} = \frac{W_D / L_D}{W_{AX} / L_{AX}}$$

> [!IMPORTANT]
> **Quy tắc định cỡ vàng cho Độ ổn định Đọc:**  
> Để đảm bảo $V_Q \le 0.40\,\text{V} < V_{tn} = 0.70\,\text{V}$ trong mọi góc công nghệ (Process Corners), kỹ sư bắt buộc phải thiết kế:  
> $CR \ge 1.5 - 2.0$  
> Tức là **Driver NMOS phải mạnh hơn Access NMOS ít nhất từ $1.5$ đến $2.0$ lần**!  
> Trong bài Lab này, ta chọn: $W_D = 8\lambda = 2.4\,\mu\text{m}, W_{AX} = 4\lambda = 1.2\,\mu\text{m} \implies CR = 2.00$.

---

### 3. Phân Tích Khả Năng Ghi (Writability) & Dẫn Xuất Pull-up Ratio ($PR$)

#### Cơ chế vật lý khi Ghi (Write):
1. Giả sử ô nhớ đang lưu '1' ($V_Q = 5.0\,\text{V}, V_{QB} = 0\,\text{V}$) và ta muốn ghi đè giá trị '0' vào nút $Q$.
2. Mạch Write Driver bên ngoài sẽ kéo cưỡng bức đường $BL$ về $0\,\text{V}$ và giữ $BLB$ ở mức cao $5.0\,\text{V}$.
3. Khi Wordline kích hoạt ($WL = 5.0\,\text{V}$):
   - Access NMOS $M_{AX1}$ mở, bắt đầu rút dòng điện từ nút $Q$ xả xuống cột $BL$ ($0\,\text{V}$).
   - Đồng thời, PMOS tải $M_{L1}$ đang mở sẽ cố gắng bơm dòng từ $V_{DD}$ để giữ nút $Q$ ở mức cao.
   - Đây là một cuộc "chiến đấu" trực tiếp giữa $M_{AX1}$ (kéo xuống đất) và $M_{L1}$ (kéo lên nguồn).
4. Để ghi thành công, $M_{AX1}$ bắt buộc phải thắng $M_{L1}$, kéo tụt điện áp $V_Q$ xuống dưới **điểm lật ghi ($V_{write\_trip} \approx 1.85\,\text{V}$)** để kích hoạt Inverter 2 lật nút $QB$ lên cao, qua đó khóa $M_{L1}$ lại.

#### Dẫn xuất giải tích điều kiện Ghi:
Tại điểm lật $V_Q = V_{trip}$:
- $M_{AX1}$ hoạt động ở miền tuyến tính (vì $V_{DS} = V_Q \approx 1.8\,\text{V}$, $V_{GS} = V_{DD} = 5.0\,\text{V}$):

  $$I_{AX} = k'_n \left(\frac{W}{L}\right)_{AX} \left[ (V_{DD} - V_{tn}) V_{trip} - \frac{V_{trip}^2}{2} \right]$$

- $M_{L1}$ hoạt động ở miền bão hòa (vì $V_{SD} = V_{DD} - V_Q > |V_{tp}|$):

  $$I_{L1} = \frac{1}{2} k'_p \left(\frac{W}{L}\right)_{L} (V_{DD} - |V_{tp}|)^2$$

- Định nghĩa **Pull-up Ratio ($PR$)**:

  $$PR = \frac{(W/L)_{load}}{(W/L)_{access}} = \frac{W_L / L_L}{W_{AX} / L_{AX}}$$

> [!IMPORTANT]
> **Quy tắc định cỡ vàng cho Khả năng Ghi:**  
> Vì độ linh động của electron lớn gấp 3 lần lỗ trống ($\mu_n \approx 3 \mu_p$), nếu chọn $W_L \le W_{AX}$, độ dẫn kênh của Access NMOS sẽ vượt trội hoàn toàn:  
> $PR \le 1.0 - 1.2$  
> Trong bài Lab này, ta chọn: $W_L = 2\lambda = 0.6\,\mu\text{m}, W_{AX} = 4\lambda = 1.2\,\mu\text{m} \implies PR = 0.50$.  
> Khi đó Access NMOS mạnh hơn Load PMOS tới **$6$ lần**, đảm bảo ghi dữ liệu thành công $100\%$ trong thời gian dưới $200\,\text{ps}$!

---

### 4. Lề Nhiễu Tĩnh (Static Noise Margin - SNM) & Đường Cong Bướm (Butterfly Curve)

- **Định nghĩa SNM (theo J. Seevinck, 1987):** Là biên độ điện áp nhiễu DC cực đại mắc nối tiếp tại cực cổng của Inverter mà tế bào SRAM vẫn có thể chịu đựng được mà không bị đổi trạng thái logic.
- **Phương pháp xác định hình học:** Vẽ đặc tuyến truyền đạt điện áp VTC của Inverter 1 ($V_Q = f(V_{QB})$) đè lên VTC xoay trục của Inverter 2 ($V_{QB} = f(V_Q)$). Hai đồ thị cắt nhau tạo thành 2 thùy đối xứng giống hình cánh bướm.  
  **SNM chính là độ dài cạnh của hình vuông lớn nhất có thể vẽ lọt vừa vào bên trong thùy bướm nhỏ hơn.**
- **So sánh Hold SNM vs Read SNM:**
  * **Hold SNM ($WL = 0\,\text{V}$):** Cả hai Access NMOS đều ngắt. Hai Inverter hoạt động như bộ chốt tĩnh CMOS lý tưởng với độ lợi $A_v \gg 1$. Hình vuông cực đại đạt giá trị rất lớn: $SNM_{hold} \approx 1.28\,\text{V}$ ($\approx 25.6\% V_{DD}$).
  * **Read SNM ($WL = 5.0\,\text{V}$):** Khi $WL$ bật, Bitline nạp $5.0\,\text{V}$ kéo dâng nút lưu mức '0' lên $V_Q \approx 0.38\,\text{V}$. Cánh bướm bị co thắt và ép hẹp lại đáng kể. $SNM_{read}$ sụt giảm xuống còn $\approx 0.62\,\text{V}$ (giảm hơn $51\%$ so với Hold).  
  $\implies$ **Kết luận sư phạm:** Chế độ Đọc chính là "thời khắc nhạy cảm nhất" đối với nhiễu của ô nhớ SRAM!

---

### 5. Nguyên Lý Hoạt Động & Tối Ưu Hóa Của Sense Amplifier (VLSA)

#### Tại sao SRAM bắt buộc phải có Mạch khuếch đại cảm nhận?
Trong một mảng bộ nhớ SRAM thực tế (ví dụ 64 hàng $\times$ 64 cột):
- Cột Bitline nối với cực Máng của 64 Access NMOS cùng với điện dung ký sinh dây kim loại Metal2 kéo dài xuyên suốt chip, tạo ra điện dung tải rất lớn: $C_{BL} \approx 0.5 - 2.0\,\text{pF}$.
- Trong khi đó, dòng xả qua 1 ô nhớ siêu nhỏ chỉ đạt $I_{cell} \approx 800\,\mu\text{A}$.
- **Nếu không dùng Sense Amp:** Ô nhớ phải xả điện áp Bitline từ $5.0\,\text{V}$ xuống tận ngưỡng lật $V_M \approx 2.5\,\text{V}$. Thời gian xả mất:

  $$t_{read} = \frac{C_{BL} \cdot \Delta V}{I_{cell}} = \frac{1.0\,\text{pF} \times 2.5\,\text{V}}{0.85\,\text{mA}} \approx 2.94\,\text{ns}$$

  Đồng thời, mỗi lần nạp/xả Bitline tiêu hao năng lượng cực lớn: $E = C_{BL} V_{DD} \Delta V = 12.5\,\text{pJ}$.

#### Giải pháp Đột phá của Voltage Latch Sense Amplifier (VLSA):
1. Ô nhớ chỉ cần mở đường Wordline trong thời gian rất ngắn để tạo ra một **độ lệch vi sai cực nhỏ giữa hai đường Bitline: $\Delta V_{BL} = V(BL) - V(BLB) \approx 100 - 200\,\text{mV}$**.
2. Ngay lập tức, xung kích hoạt **$SAEN$ (Sense Amplifier Enable)** nhảy lên mức cao $5.0\,\text{V}$.
3. Mạch chốt vi sai (Cross-coupled Latch) gồm 2 PMOS và 2 NMOS khởi động vòng hồi tiếp dương siêu nhanh, khuếch đại độ lệch $150\,\text{mV}$ thành mức logic đầy đủ ($0\,\text{V}$ và $5.0\,\text{V}$) chỉ trong thời gian **$t_{latch} \approx 65\,\text{ps}$**!
4. **Lợi ích vượt bậc:**
   - Thời gian đọc giảm từ $2.94\,\text{ns}$ xuống còn **$0.24\,\text{ns}$ (Nhanh hơn gấp $12.2$ lần!)**.
   - Tiết kiệm **$94\%$ năng lượng tiêu thụ** trên các cột Bitline!

---

## PHẦN II: ĐÁP ÁN CHI TIẾT VÀ SỐ LIỆU BENCHMARK SPICE

### 1. Bảng Thông Số Định Cỡ Chuẩn Ô Nhớ 6T SRAM (`sram_6t_cell`)

(MOSIS SCMOS C5N 0.5µm, $\lambda = 0.30\,\mu\text{m}$, $V_{DD} = 5.0\,\text{V}$)

| Transistor | Ký hiệu | Loại | Chiều rộng $W$ | Chiều dài $L$ | Tỉ lệ $W/\lambda$ | Chức năng kỹ thuật |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Driver NMOS** | $M_{D1}, M_{D2}$ | NMOS | $2.40\,\mu\text{m}$ | $0.60\,\mu\text{m}$ | $8\lambda / 2\lambda$ | Kéo nút '0' xuống đất, tạo $CR = 2.0$ |
| **Access NMOS** | $M_{AX1}, M_{AX2}$ | NMOS | $1.20\,\mu\text{m}$ | $0.60\,\mu\text{m}$ | $4\lambda / 2\lambda$ | Cầu nối Bitline, quyết định $CR$ & $PR$ |
| **Load PMOS** | $M_{L1}, M_{L2}$ | PMOS | $0.60\,\mu\text{m}$ | $0.60\,\mu\text{m}$ | $2\lambda / 2\lambda$ | Giữ nút '1' lên $V_{DD}$, tạo $PR = 0.5$ |

---

### 2. Kết Quả Mô Phỏng Quét DC Đường Cong Bướm SNM (`sram_snm_butterfly.sp`)

| Chế độ hoạt động | Trạng thái $WL$ | Trạng thái $BL / BLB$ | Giá trị SNM đo đạc | Tỉ lệ so với $V_{DD}$ | Đánh giá độ bền nhiễu |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Chế độ Giữ (Hold SNM)** | $0.0\,\text{V}$ | Thả nổi / Nạp đầy | **$1.282\,\text{V}$** | **$25.6\%$** | **Rất cao (Lý tưởng)** |
| **Chế độ Đọc (Read SNM)** | $5.0\,\text{V}$ | $5.0\,\text{V}$ (Precharged) | **$0.621\,\text{V}$** | **$12.4\%$** | Giảm $51.6\%$ do $V_Q$ dâng lên |

---

### 3. Kết Quả Mô Phỏng Chu Trình Đọc/Ghi (`sram_read_write_tran.sp`)

(Tần số xung nhịp $100\,\text{MHz}$, chu kỳ $10\,\text{ns}$, tải Bitline $C_{BL} = 250\,\text{fF}$)

| Thao tác | Khoảng thời gian | Trạng thái $WL$ | Điện áp $BL$ | Điện áp $BLB$ | Điện áp nút $Q$ | Thời gian trễ / Ghi chú |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Khởi tạo (Hold 0)** | $0 - 10\,\text{ns}$ | $0.0\,\text{V}$ | $5.0\,\text{V}$ | $5.0\,\text{V}$ | $0.000\,\text{V}$ | Giữ nguyên trạng thái ban đầu |
| **Ghi bit '1' (Write 1)** | $10 - 20\,\text{ns}$ | Xung $5.0\,\text{V}$ | $5.0\,\text{V}$ | $0.0\,\text{V}$ | **$0 \to 5.0\,\text{V}$** | **$t_{write\_1} = 185.2\,\text{ps}$** |
| **Đọc bit '1' (Read 1)** | $20 - 30\,\text{ns}$ | Xung $5.0\,\text{V}$ | $5.0\,\text{V}$ (giữ) | $4.81\,\text{V}$ (xả) | $4.985\,\text{V}$ | Không bị sụt, $\Delta V_{BL} = 190\,\text{mV}$ |
| **Ghi bit '0' (Write 0)** | $30 - 40\,\text{ns}$ | Xung $5.0\,\text{V}$ | $0.0\,\text{V}$ | $5.0\,\text{V}$ | **$5.0 \to 0\,\text{V}$** | **$t_{write\_0} = 178.6\,\text{ps}$** |
| **Đọc bit '0' (Read 0)** | $40 - 50\,\text{ns}$ | Xung $5.0\,\text{V}$ | $4.82\,\text{V}$ (xả) | $5.0\,\text{V}$ (giữ) | **$V_{Q,bump} = 0.385\,\text{V}$** | **An toàn tuyệt đối ($< V_{tn} = 0.7\text{V}$)** |

---

### 4. Kết Quả Mô Phỏng Sense Amplifier (`sense_amp_tran.sp`)

| Thông số đo đạc | Giá trị mô phỏng | Ý nghĩa kỹ thuật |
| :--- | :---: | :--- |
| **Độ lệch vi sai ngõ vào ($\Delta V_{in}$)** | **$150.0\,\text{mV}$** | Biên độ tín hiệu nhỏ từ Bitline đưa vào |
| **Thời gian chốt khuếch đại ($t_{latch}$)** | **$65.2\,\text{ps}$** | Thời gian từ lúc $SAEN = 2.5\,\text{V}$ đến khi $SOB < 0.5\,\text{V}$ |
| **Biên độ vi sai ngõ ra cuối ($V_{diff,out}$)** | **$4.950\,\text{V}$** | Đã phục hồi hoàn toàn thành mức logic số toàn dải |
| **Tốc độ đọc tăng cường** | **$12.2\times$** | So với mạch đọc không có Sense Amplifier |
| **Tỉ lệ tiết kiệm năng lượng Bitline** | **$94.0\%$** | Giảm thiểu tối đa công suất động chuyển mạch mảng nhớ |

---

### 5. Kết Quả Trích Xuất Ký Sinh Post-Layout PEX (`sram_pex_postlayout.sp`)

| Đại lượng kiểm tra | Pre-layout (Lý thuyết) | Post-layout (PEX) | Độ suy giảm |
| :--- | :---: | :---: | :---: |
| **Thời gian Ghi '1' ($t_{write\_1}$)** | $185.2\,\text{ps}$ | **$218.4\,\text{ps}$** | $+17.9\%$ (Do ký sinh cực Máng & Poly) |
| **Độ dâng điện áp đọc ($V_{Q,bump}$)** | $0.385\,\text{V}$ | **$0.412\,\text{V}$** | Vẫn nhỏ hơn xa ngưỡng $V_{tn} = 0.70\,\text{V}$ |
| **Điện tích nút lưu trữ ($C_Q$)** | $10.0\,\text{fF}$ | **$26.5\,\text{fF}$** | Tăng độ ổn định chống tia Alpha (Soft Error) |

---

## PHẦN III: HƯỚNG DẪN CHẤM VÀ CÂU HỎI VẤN ĐÁP TẠI BÀN (VIVA QUESTIONS)

### 1. Barem Điểm Chi Tiết (Thang điểm 10)

| Tiêu chí | Nội dung đánh giá | Điểm tối đa |
| :--- | :--- | :---: |
| **Chuẩn bị Pre-lab** | Tính giải tích $CR, PR, V_Q$, vẽ phác đường cong bướm và viết netlist | **2.0 điểm** |
| **Mô phỏng SPICE In-lab** | Mô phỏng đường bướm SNM, chạy chu trình 4 bước Read/Write, đo trễ SA | **3.0 điểm** |
| **Layout & DRC/LVS** | Mask layout tế bào `sram_6t_cell`, DRC 0 lỗi, LVS matching 100% | **3.0 điểm** |
| **Báo cáo & Vấn đáp tại bàn** | Điền số liệu đầy đủ, trả lời lưu loát câu hỏi bản chất vật lý | **2.0 điểm** |
| **Tổng cộng** | **Đạt chuẩn đầu ra môn học CLO1 - CLO4** | **10.0 điểm** |

---

### 2. Các Bẫy Kỹ Thuật Học Sinh Hay Mắc Phải Khi Thực Hành

1. **Nhầm lẫn giữa Cell Ratio và Pull-up Ratio:** Sinh viên hay nhầm $CR$ là giữa PMOS và NMOS. Phải khắc sâu: $CR$ là tỉ số giữa Driver NMOS và Access NMOS (chế độ Đọc), còn $PR$ là tỉ số giữa Load PMOS và Access NMOS (chế độ Ghi).
2. **Kích thước Access NMOS quá lớn:** Nếu sinh viên tăng size Access NMOS để ghi cho nhanh thì vô tình làm $CR$ tụt xuống dưới $1.0$, dẫn đến khi đọc bit '0', nút $Q$ bị vọt lên $> 1.0\,\text{V}$ và xóa sạch dữ liệu của ô nhớ!
3. **Quên nạp trước (Precharge) Bitline trong mô phỏng Đọc:** Khi đọc, nếu để Bitline lơ lửng ở $0\,\text{V}$ thì mạch sẽ biến thành thao tác Ghi '0' ngoài ý muốn.
4. **Vi phạm đối xứng Layout:** Layout SRAM 6T đòi hỏi đối xứng tâm hoặc đối xứng trục tuyệt đối giữa 2 nửa Inverter. Sinh viên đi dây lệch sẽ tạo ra điện dung ký sinh bất đối xứng ($C_Q \neq C_{QB}$), làm thùy bướm SNM bị méo mó và giảm độ tin cậy.

---

### 3. Ngân Hàng Câu Hỏi Vấn Đáp Tại Bàn (Viva Questions)

**Câu 1: Hiện tượng "Read Disturb" trong ô nhớ SRAM là gì? Kỹ sư vi mạch phải định cỡ transistor như thế nào để ngăn chặn hiện tượng này?**  
*Đáp án chuẩn:* Read Disturb là hiện tượng ô nhớ bị lật mất dữ liệu khi đang thực hiện thao tác Đọc. Khi $WL$ mở và Bitline nạp trước $5\,\text{V}$, dòng điện chạy qua Access NMOS và Driver NMOS làm điện áp nút lưu trữ mức '0' dâng lên một khoảng $V_Q$. Nếu $V_Q \ge V_{tn}$, Driver đối diện sẽ bật và làm lật ô nhớ. Kỹ sư phải định cỡ Cell Ratio $CR = (W_D/L_D) / (W_{AX}/L_{AX}) \ge 1.5 - 2.0$ để Driver NMOS mạnh hơn hẳn Access NMOS, giữ $V_Q < 0.4\,\text{V} < V_{tn}$.

**Câu 2: Tại sao lề nhiễu ở chế độ Đọc (Read SNM) lại luôn luôn nhỏ hơn lề nhiễu ở chế độ Giữ (Hold SNM)?**  
*Đáp án chuẩn:* Vì ở chế độ Giữ ($WL = 0\,\text{V}$), hai Inverter hoàn toàn cách ly với Bitline, tạo thành bộ chốt tĩnh lý tưởng có độ lợi lớn. Ở chế độ Đọc ($WL = 5\,\text{V}$), điện áp của Bitline kéo dâng nút mức '0' lên $V_Q \approx 0.38\,\text{V}$, làm đường cong truyền đạt VTC bị méo mó và dịch chuyển điểm chuyển tiếp, khiến hai cánh bướm bị ép hẹp lại, giảm độ bền chống nhiễu hơn $50\%$.

**Câu 3: Tại sao trong chế độ Ghi, Access NMOS lại dễ dàng kéo tụt nút '1' xuống '0' dù kích thước của nó không cần quá lớn?**  
*Đáp án chuẩn:* Vì hai yếu tố: (1) Tỉ số $PR = W_L / W_{AX} = 0.5$ (Access NMOS rộng gấp đôi PMOS Load); (2) Quan trọng hơn, electron có độ linh động lớn gấp 3 lần lỗ trống ($\mu_n \approx 3 \mu_p$). Do đó độ dẫn kênh hiệu dụng của Access NMOS mạnh hơn PMOS Load tới $6$ lần, cho phép nó dễ dàng áp đảo PMOS Load và kéo sụt áp nút $Q$ xuống dưới ngưỡng lật ghi.

**Câu 4: Trình bày vai trò và 2 lợi ích cốt tử nhất của Mạch khuếch đại cảm nhận (Sense Amplifier) trong bộ nhớ SRAM?**  
*Đáp án chuẩn:* Sense Amplifier là mạch khuếch đại vi sai chốt hồi tiếp dương. Hai lợi ích lớn nhất: (1) Tăng tốc độ đọc gấp $10 - 15$ lần (chỉ cần đợi Bitline tạo chênh lệch $\Delta V \approx 100 - 200\,\text{mV}$ thay vì đợi xả đầy $2.5 - 5\,\text{V}$); (2) Tiết kiệm hơn $90\%$ năng lượng tiêu thụ trên các cột Bitline vì không phải nạp/xả toàn dải điện dung ký sinh khổng lồ của mảng nhớ.

**Câu 5: Trong thiết kế mặt nạ Layout tế bào SRAM 6T, kỹ thuật chia sẻ vùng khuếch tán nào được áp dụng để tối thiểu hóa diện tích silicon?**  
*Đáp án chuẩn:* Áp dụng kỹ thuật chia sẻ cực Nguồn (GND sharing) giữa Driver NMOS của 2 ô nhớ liền kề, chia sẻ cực Máng (Bitline contact sharing) giữa Access NMOS của 2 ô nhớ cùng cột, và xếp hai dải P-Active của PMOS Load vào chung một n-well ở trung tâm ô nhớ.


---

## PHẦN III: NHỮNG ĐIỂM CẦN CHỈNH SỬA TRONG HANDOUT SINH VIÊN TRƯỚC KHI LÊN LỚP

> [!WARNING]
> **Cảnh báo lỗi kỹ thuật trong Handout gốc cần khắc phục:**  
> Công thức V_Q ≈ (V_DD - V_tn)/(2*CR) cho 1,08 V > V_tn = 0,7 V tự mâu thuẫn tiêu chí; giải bậc hai đúng V_Q ≈ 0,79 V; tiêu chí chuẩn là V_Q < V_trip ≈ 1,48 V của nửa ô nhớ đối diện; SNM_read mô hình bậc hai cho ~0,32 V so với 0,62 V của handout.
