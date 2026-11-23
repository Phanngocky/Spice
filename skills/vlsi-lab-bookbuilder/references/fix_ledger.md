# Sổ lỗi đã biết của bộ lab gốc (rà soát lần 1)

Mức độ: **C** = chắc chắn (tính tay hoặc đọc là thấy); **K** = nên kiểm bằng LTspice hoặc tính lại; **G** = góp ý. Các số mô hình do mô hình bậc hai tính, không phải Level 3 của C5.

## Lỗi chung toàn bộ
- 31 tham chiếu ảnh `images/...` nhưng gói gửi không có thư mục ảnh (C, với gói đã nhận).
- Từ tuyệt đối dày: "hoàn toàn", "100%", "hoàn hảo", "tuyệt đối", "luôn" (G).
- Rubric hai kiểu khác nhau (Lab 1–6 theo trọng số %, Lab 7–10 theo mức) (G).
- Đường dẫn cứng như `04 - Models_and_Libraries/` và `03 - Instructor_Solutions/` trong handout (C).
- Nhiều số "ps" trong Lab 5, 6, 9, 10 là giá trị ước lượng bằng tay: t_pd inverter 34 ps trùng 0,69 × 969 Ω × 50 fF ≈ 34 ps. Mô hình bậc hai cho khoảng 59 ps ở 50 fF (gấp ~1,8) (K).

## Theo lab
| Lab | Vị trí | Vấn đề | Mức |
|---|---|---|---|
| 0 | Toàn bài | Lệch trọng tâm: BJT 2N3904 và phân áp; Pre-lab trùng số ví dụ lý thuyết (lộ đáp án) | C |
| 1 | Mục I | Ghi tỉ số ≈ 3/1 cho V_M = 2,50 V; với V_tn ≠ \|V_tp\| thì r = 1 cho 2,45 V, muốn 2,50 V cần tỉ số ≈ 3,36 | G |
| 1 | Pre-lab | 0,69·R_on·C_L với R_on tại V_DS ≈ 0 thấp hơn trễ đo của mạch thật (~1,8 lần theo mô hình bậc hai); nên để sinh viên tự phát hiện | K |
| 2 | §III.4 | Trễ nút nội "tăng 10–25%" chưa kiểm; "NAND luôn nhỏ hơn NOR" nên viết có điều kiện; sơ đồ ASCII stick NAND2 thiếu nút Out và lặp nhãn Gate | G |
| 3 | §III.4 | "Nhanh hơn 3,63 lần (cải thiện 363%)": 51/14,05 = 3,63 lần, tức giảm trễ ~72%, không phải cải thiện 363% | C |
| 3 | §III.4 | C_in = 20 fF không khớp INV_X1 (~7–10 fF theo W·L·C_ox với t_ox ≈ 14 nm, là giả định); nếu dùng C_in thật thì H ≈ 110–140 và N tối ưu = 4 | K |
| 3 | Mẹo | "Luôn gán tín hiệu tới hạn vào ngõ C" nên viết có điều kiện | G |
| 4 | §III.2 | R_TG tại V_in = 2,5 V tính 969∥992 ≈ 490 Ω là sai; R_on,n ≈ 2,3 kΩ và R_on,p ≈ 2,45 kΩ tại đó, R_TG ≈ 1,2 kΩ, cao hơn hai đầu dải (~1 kΩ) | C |
| 4 | §III.1b | Weak '0' của PMOS ghi 0,8–1,05 V bỏ qua hiệu ứng thân (NMOS thì có tính); tính đối xứng ≈ 1,4 V | K |
| 5 | §III.3 | Ký tự Trung Quốc lạc: "điện荷" | C |
| 6 | §III.2 | Carry mirror: PDN có 5 NMOS + 5 PMOS = 10T, không có inverter; văn bản ghi "4 NMOS + 4 PMOS + inverter"; tổng đúng là 28T (10 + 14 + 2×2), không phải "24–28T" | C |
| 6 | §III.3 | TG adder "16T" nhưng cộng các khối (XOR 4–6T + XOR 4T + MUX 4T) ra 12–14T; MUX cần inverter cho tín hiệu chọn | K |
| 7 | §III.4 | Domino OR4 là ví dụ yếu cho charge sharing (PDN song song); nên dùng AND3/AND4 | G |
| 7 | Pre-lab | Inverter đệm 16λ/8λ có V_M ≈ 2,27 V theo công thức Lab 1, không phải 2,45 V; gọi "high-skew" mâu thuẫn (tỉ số 2 < 3,36 nên là low-skew) | C |
| 8 | §III.2a | V_Q ≈ (V_DD − V_tn)/(2·CR) với CR = 2 ra 1,08 V > V_tn = 0,7 V, mâu thuẫn tiêu chí "V_Q < V_tn"; giải bậc hai đúng ≈ 0,79 V (cũng > 0,7 V); tiêu chí đúng so với ngưỡng lật của inverter đối diện | C |
| 8 | §III.3 | SNM_read = 0,62 V; mô hình bậc hai cho ~0,3 V; SNM_hold 1,28 V khớp (mô hình cho 1,30 V) | K |
| 9 | §III.3 | AOI54321 xếp chồng 5 NMOS chỉ cho W = 8λ, trái quy tắc R_on bằng inverter (đúng 20λ); Pre-lab gợi sẵn kết luận "hoàn toàn xứng đáng" | K |
| 9, 10 | Đếm T | CLA4 = 134T khó tái hiện: CLG = 76T, tổng 124–140T tùy XOR 4T/6T; Lab 10 ghi MUX4 4-bit = 64T trong khi Lab 4 cho 18T × 4 = 72T | C |
| 10 | Mục tiêu | f_max ≥ 1 GHz cho 0,5 µm/5 V và bảng điền sẵn 1,92 GHz (tính tay); chưa nên đưa vào rubric trước khi chạy thử; handout trỏ tới `03 - Instructor_Solutions/` | K |

## Lab 0 (đã xử lý)
Đã viết lại theo hướng: bỏ BJT, thêm `.param/.step` kiểm ln2·R·C, thêm liên kết mô hình MOSFET, Pre-lab dùng số khác, kiểm chéo t_r · f_c ≈ 0,35, sửa câu hỏi `dTmax` (20 µs lệch ~0,7%, 100 µs lệch ~18%, chưa kiểm bằng LTspice). Còn mở: tên model trong `C5_models.txt` (N/P hay CMOSN/CMOSP) cần giảng viên xác nhận.
