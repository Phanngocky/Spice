# -*- coding: utf-8 -*-
"""
Script to build standalone Teacher's Book files for each lab (Lab 00 to Lab 10)
and save them into the dedicated 'Teacher_Book' folder.
"""

import os
import re

os.makedirs('Teacher_Book', exist_ok=True)

# 1. Handout mapping
handouts = {
    0: 'lab-00-nhap-mon-mo-phong-spice-va-ltspice.md',
    1: 'lab-01-dac-tinh-mosfet-va-cmos-inverter.md',
    2: 'lab-02-cong-logic-tinh-nand-nor.md',
    3: 'lab-03-cong-phuc-hop-aoi-oai-logical-effort.md',
    4: 'lab-04-transmission-gate-va-mux.md',
    5: 'lab-05-mach-tuan-tu-latch-va-flipflop.md',
    6: 'lab-06-mach-cong-toan-phan-full-adder.md',
    7: 'lab-07-logic-dong-dynamic-cmos.md',
    8: 'lab-08-o-nho-sram-6t-va-sense-amplifier.md',
    9: 'lab-09-khoi-cong-nhanh-4bit-cla.md',
    10: 'lab-10-capstone-tich-hop-vi-mach-alu-4bit.md'
}

lab_titles = {
    0: 'NHẬP MÔN MÔ PHỎNG SPICE VỚI LTSPICE & MẠCH RC CƠ BẢN',
    1: 'ĐẶC TÍNH I-V CỦA MOSFET VÀ THIẾT KẾ CMOS INVERTER',
    2: 'THIẾT KẾ CỔNG LOGIC TĨNH NAND2 VÀ NOR2 CMOS',
    3: 'CỔNG PHỨC HỢP AOI21 VÀ TỐI ƯU TRỄ THEO PHƯƠNG PHÁP LOGICAL EFFORT',
    4: 'CỔNG TRUYỀN (TRANSMISSION GATE) VÀ BỘ DỒN KÊNH MUX',
    5: 'MẠCH TUẦN TỰ MỨC TRANSISTOR: D-LATCH VÀ D-FLIP-FLOP MASTER-SLAVE',
    6: 'THIẾT KẾ MẠCH CỘNG TOÀN PHẦN 1-BIT (1-BIT FULL ADDER)',
    7: 'KỸ THUẬT LOGIC ĐỘNG VÀ LOGIC DOMINO (DYNAMIC & DOMINO CMOS LOGIC)',
    8: 'THIẾT KẾ Ô NHỚ BÁN DẪN TĨNH (6T SRAM CELL & SENSE AMPLIFIER)',
    9: 'THIẾT KẾ ĐƯỜNG DỮ LIỆU KHỐI CỘNG NHANH 4-BIT (4-BIT CLA)',
    10: 'CAPSTONE: TÍCH HỢP VI MẠCH 4-BIT REGISTERED ALU & XÁC THỰC VẬT LÝ'
}

errata_dict = {
    0: 'Không nên đặt sai số 2% làm yêu cầu tuyệt đối cho mọi chế độ; kiểm tra chiều cực tính của tụ để tránh đo ngược dấu dòng điện; nguồn xung 10ns là xấp xỉ bước lý tưởng.',
    1: 'Handout ghi tỉ số 3/1 cho V_M = 2,50 V; đính chính đúng là 2,45 V, muốn 2,50 V cần W_p/W_n ≈ 3,36. Phân biệt rõ λ_kênh (V^-1) và λ_lưới (0,30 µm) ngay đầu buổi học.',
    2: 'Sơ đồ Stick NAND2 trong handout vẽ thiếu nút Out và lặp nhãn Gate; khẳng định "NAND luôn nhanh hơn NOR" cần bổ sung điều kiện độ linh động electron lớn hơn lỗ trống (μn/μp ≈ 3).',
    3: 'Ghi "AOI21 giảm diện tích 40%" thực ra là giảm 40% số transistor (6T vs 10T), diện tích thực giảm ~18%; ghi "cải thiện tốc độ 363%" thực ra là trễ giảm 72% (tốc độ tăng 3,63 lần); C_in = 20 fF không khớp INV_X1 (~11,4 fF).',
    4: 'R_TG tại 2,5 V ghi 490 Ω là sai (do lấy 969 // 992); đúng phải là ~1,19 kΩ do cả 2 transistor đều bị giảm quá áp cổng; Weak 0 của PMOS ghi 0,8 - 1,05 V bỏ qua hiệu ứng thân (thực tế dâng lên ~1,4 V).',
    5: 'Handout dính ký tự lạ "điện荷"; I3 chưa được nêu rõ; đếm transistor cần chuẩn hóa 18T mỗi bit DFF (2 Latch 8T + 1 Inverter CLK 2T).',
    6: 'Khối Carry ghi nhầm "4 NMOS + 4 PMOS"; công thức Sum bị sai vế trái (đúng là Sum_bar); tổng số transistor chuẩn xác của Mirror Adder là 28T (10T Carry + 14T Sum + 4T Inverters).',
    7: 'Lấy ví dụ OR4 để giải thích chia sẻ điện tích là chưa phù hợp (PDN song song không có nút nội xếp chồng); nên dùng AND3/AND4; inverter 16λ/8λ có V_M = 2,27 V là low-skew, không phải "high-skew".',
    8: 'Công thức V_Q ≈ (V_DD - V_tn)/(2*CR) cho 1,08 V > V_tn = 0,7 V tự mâu thuẫn tiêu chí; giải bậc hai đúng V_Q ≈ 0,79 V; tiêu chí chuẩn là V_Q < V_trip ≈ 1,48 V của nửa ô nhớ đối diện; SNM_read mô hình bậc hai cho ~0,32 V so với 0,62 V của handout.',
    9: 'Cổng AOI54321 tạo C4 chỉ cho W_n = 8λ là vi phạm quy tắc R_on (cần 20λ nếu muốn bằng INV_X1); chấp nhận 8λ là đánh đổi diện tích; câu hỏi Pre-lab lộ đáp án "hoàn toàn xứng đáng" cần đổi thành "dự đoán, đo và so sánh".',
    10: 'Mục tiêu f_max ≥ 1 GHz cần kiểm chứng qua PEX (thực tế f_max,PEX ≈ 1,42 GHz); đếm transistor MUX4 cần thống nhất 64T (16T/bit) thay vì 72T ở Lab 4.'
}

# Read master_tb
with open('03 - Instructor_Solutions/Teacher_Book_VLSI_Lab00_Lab10.md', 'r', encoding='utf-8') as f:
    master_tb = f.read()

def get_master_section(lab_num):
    pat = rf'(# {lab_num}\. LAB {lab_num} [^\n]+[\s\S]*?)(?=\n# \d+\.|\Z)'
    m = re.search(pat, master_tb)
    return m.group(1) if m else ''

def get_solution(lab_num):
    path = f'03 - Instructor_Solutions/lab{lab_num:02d}/dap_an_chi_tiet_lab{lab_num:02d}.md'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# 2. Write Lab 00
with open('03 - Instructor_Solutions/lab00/dap_an_chi_tiet_lab00.md', 'r', encoding='utf-8') as f:
    lab00_text = f.read()

with open('Teacher_Book/Lab00_Teacher_Book.md', 'w', encoding='utf-8') as f:
    f.write(lab00_text)
print('Wrote Teacher_Book/Lab00_Teacher_Book.md')

# 3. Write Lab 01 to Lab 10
for i in range(1, 11):
    ho = handouts[i]
    title = lab_titles[i]
    mst = get_master_section(i)
    sol = get_solution(i)
    err = errata_dict[i]
    
    # Clean up duplicate titles if sol already has them
    file_content = f"""# GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG
# BÀI LAB {i:02d} — TEACHER'S BOOK: {title}
*(Tài liệu chuyên môn lưu hành nội bộ — Tuyệt đối không phát cho sinh viên)*

> **Đi kèm Handout thực hành của sinh viên:** [{ho}](../02%20-%20Student%20Workbook/{ho})  
> **Thư mục giải pháp & Netlist tham chiếu:** [03 - Instructor_Solutions/lab{i:02d}/](../03%20-%20Instructor_Solutions/lab{i:02d}/)  
> **Tiến trình công nghệ áp dụng:** MOSIS SCMOS C5N 0,5 µm ($V_{{DD}} = 5,0\\,\\text{{V}}, \\lambda = 0,30\\,\\mu\\text{{m}}, L_{{min}} = 0,60\\,\\mu\\text{{m}}$).

---

## PHẦN I: KIẾN THỨC NỀN TẢNG, PHÂN TÍCH VẬT LÝ & ĐỊNH CỠ CHUYÊN SÂU

{mst}

---

## PHẦN II: KỊCH BẢN GIẢNG DẠY, ĐÁP ÁN CHI TIẾT & SỐ LIỆU ĐỐI CHUẨN SPICE BENCHMARK

{sol}

---

## PHẦN III: NHỮNG ĐIỂM CẦN CHỈNH SỬA TRONG HANDOUT SINH VIÊN TRƯỚC KHI LÊN LỚP

> [!WARNING]
> **Cảnh báo lỗi kỹ thuật trong Handout gốc cần khắc phục:**  
> {err}
"""
    out_path = f'Teacher_Book/Lab{i:02d}_Teacher_Book.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    print(f'Wrote {out_path} ({len(file_content)} bytes)')

# 4. Write Master Errata & Action Plan
m11 = re.search(r'(# 11\. BẢNG TỔNG HỢP CÁC ĐIỂM CẦN CHỈNH SỬA TRONG HANDOUT GỐC[\s\S]*?)(?=\Z)', master_tb)
errata_plan_content = f"""# TÀI LIỆU QUẢN TRỊ KỸ THUẬT: MASTER ERRATA & KẾ HOẠCH KIỂM CHỨNG
## BỘ GIÁO TRÌNH THỰC HÀNH THIẾT KẾ VI MẠCH VLSI (LAB 00 ĐẾN LAB 10)

> **Tài liệu lưu hành nội bộ dành cho Giảng viên & Trợ giảng**  
> Bản tổng hợp toàn bộ các điểm sai lệch, mâu thuẫn kỹ thuật trong Handout gốc và quy trình 6 bước nghiệm thu thực tế trước ngày khai giảng.

---

{m11.group(1) if m11 else ''}
"""
with open('Teacher_Book/Master_Errata_Va_Ke_Hoach_Kiem_Chung.md', 'w', encoding='utf-8') as f:
    f.write(errata_plan_content)
print('Wrote Teacher_Book/Master_Errata_Va_Ke_Hoach_Kiem_Chung.md')

# 5. Write README.md for Teacher_Book
readme_content = """# BỘ GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TEACHER'S BOOK)
## HỌC PHẦN THỰC HÀNH THIẾT KẾ VI MẠCH VLSI (MÃ HỌC PHẦN: 5505382)
### Tiến trình Công nghệ: MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}$)

> **LƯU HÀNH NỘI BỘ — TUYỆT ĐỐI KHÔNG PHÁT CHO SINH VIÊN**  
> Thư mục này chứa đầy đủ cẩm nang hướng dẫn sư phạm, kiến thức nền tảng vật lý toán, kịch bản giảng dạy, đáp án chi tiết, bảng số liệu đối chuẩn SPICE Benchmark và câu hỏi vấn đáp cho từng bài thực hành từ **Lab 00 đến Lab 10**.

---

## 1. MỤC LỤC ĐIỀU HƯỚNG TỪNG BÀI LAB

| Bài Lab | Tên bài thực hành | Chương đề cương | Vai trò môn học | Tài liệu Teacher's Book | Handout Sinh viên |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **Lab 00** | Nhập môn mô phỏng SPICE & Mạch RC cơ bản | 1, 3 | Bắt buộc (Nhập môn) | [Lab00_Teacher_Book.md](Lab00_Teacher_Book.md) | [lab-00-nhap-mon...md](../02%20-%20Student%20Workbook/lab-00-nhap-mon-mo-phong-spice-va-ltspice.md) |
| **Lab 01** | Đặc tính MOSFET & Thiết kế CMOS Inverter | 2, 3 | Bắt buộc | [Lab01_Teacher_Book.md](Lab01_Teacher_Book.md) | [lab-01-dac-tinh...md](../02%20-%20Student%20Workbook/lab-01-dac-tinh-mosfet-va-cmos-inverter.md) |
| **Lab 02** | Thiết kế Cổng tĩnh NAND2 và NOR2 CMOS | 6 | Bắt buộc | [Lab02_Teacher_Book.md](Lab02_Teacher_Book.md) | [lab-02-cong-logic...md](../02%20-%20Student%20Workbook/lab-02-cong-logic-tinh-nand-nor.md) |
| **Lab 03** | Cổng phức hợp AOI21 & Phương pháp Logical Effort | 3, 6 | Bắt buộc | [Lab03_Teacher_Book.md](Lab03_Teacher_Book.md) | [lab-03-cong-phuc-hop...md](../02%20-%20Student%20Workbook/lab-03-cong-phuc-hop-aoi-oai-logical-effort.md) |
| **Lab 04** | Cổng truyền (Transmission Gate) & MUX 2:1/4:1 | 6 | Tự chọn / Ghép Lab 6 | [Lab04_Teacher_Book.md](Lab04_Teacher_Book.md) | [lab-04-transmission-gate...md](../02%20-%20Student%20Workbook/lab-04-transmission-gate-va-mux.md) |
| **Lab 05** | Mạch tuần tự: D-Latch & D-Flip-Flop Master-Slave | 7 | Bắt buộc | [Lab05_Teacher_Book.md](Lab05_Teacher_Book.md) | [lab-05-mach-tuan-tu...md](../02%20-%20Student%20Workbook/lab-05-mach-tuan-tu-latch-va-flipflop.md) |
| **Lab 06** | Mạch cộng toàn phần 1-bit (1-bit Full Adder) | 6 | Bắt buộc | [Lab06_Teacher_Book.md](Lab06_Teacher_Book.md) | [lab-06-mach-cong...md](../02%20-%20Student%20Workbook/lab-06-mach-cong-toan-phan-full-adder.md) |
| **Lab 07** | Kỹ thuật Logic động (Dynamic CMOS) & Domino | 6 | Nâng cao / Tự chọn | [Lab07_Teacher_Book.md](Lab07_Teacher_Book.md) | [lab-07-logic-dong...md](../02%20-%20Student%20Workbook/lab-07-logic-dong-dynamic-cmos.md) |
| **Lab 08** | Thiết kế Ô nhớ SRAM 6T & Sense Amplifier | Đồ án / Tự chọn | [Lab08_Teacher_Book.md](Lab08_Teacher_Book.md) | [lab-08-o-nho-sram...md](../02%20-%20Student%20Workbook/lab-08-o-nho-sram-6t-va-sense-amplifier.md) |
| **Lab 09** | Khối cộng nhanh 4-bit CLA (Carry Lookahead) | Đồ án / Tự chọn | [Lab09_Teacher_Book.md](Lab09_Teacher_Book.md) | [lab-09-khoi-cong-nhanh...md](../02%20-%20Student%20Workbook/lab-09-khoi-cong-nhanh-4bit-cla.md) |
| **Lab 10** | Capstone: ALU 4-bit tích hợp có thanh ghi | Đồ án (1, 6, 7) | Bắt buộc | [Lab10_Teacher_Book.md](Lab10_Teacher_Book.md) | [lab-10-capstone-alu...md](../02%20-%20Student%20Workbook/lab-10-capstone-tich-hop-vi-mach-alu-4bit.md) |
| **Quản trị** | **Master Errata & Kế hoạch kiểm chứng kỹ thuật** | Toàn khóa | Tài liệu quản trị | [Master_Errata_Va_Ke_Hoach_Kiem_Chung.md](Master_Errata_Va_Ke_Hoach_Kiem_Chung.md) | — |

---

## 2. THAM SỐ CÔNG NGHỆ MOSIS C5N 0,5 µM CHUẨN HÓA

Các tham số chuẩn hóa được trích xuất trực tiếp từ tệp [C5_models.txt](../04%20-%20Models_and_Libraries/C5_models.txt):

| Tham số | Ý nghĩa vật lý | Giá trị chuẩn C5N | Ghi chú giảng dạy |
| :--- | :--- | :---: | :--- |
| $V_{DD}$ | Điện áp nguồn danh định | $5,0\,\text{V}$ | Chuẩn tương thích logic 5V. |
| $\lambda$ | Đơn vị lưới layout mở rộng | $0,30\,\mu\text{m}$ | Chiều dài kênh tối thiểu $L_{min} = 2\lambda = 0,60\,\mu\text{m}$. |
| $\lambda_{kênh}$ | Hệ số điều chế độ dài kênh | $0,05\,\text{V}^{-1}$ | Hệ số LAMBDA trong phương trình dòng điện SPICE. |
| $t_{ox}$ | Độ dày lớp oxit cổng | $9,5\,\text{nm}$ ($95\,\text{Å}$) | Handout cũ giả định $14\,\text{nm}$ là sai lệch! |
| $C_{ox}$ | Điện dung oxit cổng đơn vị | $3,635\,\text{fF/\mu m}^2$ | $3,453 \cdot 10^{-11} / 9,5 \cdot 10^{-9}$. |
| $V_{tn0}, |V_{tp0}|$ | Điện áp ngưỡng không thiên thế thân | $0,70\,\text{V}$ và $0,80\,\text{V}$ | VTO trong model N và P. |
| $K'_n, K'_p$ | Hệ số độ dẫn truyền bản chất | $120\,\mu\text{A/V}^2$ và $40\,\mu\text{A/V}^2$ | Tỉ số độ linh động $\mu_n / \mu_p \approx 3,0$. |
| $\gamma_n, \gamma_p$ | Hệ số hiệu ứng thân (Body factor) | $0,40\,\text{V}^{1/2}$ và $0,50\,\text{V}^{1/2}$ | GAMMA trong model SPICE. |
| $\text{INV\_X1}$ | Kích thước Inverter cơ sở | $W_n = 4\lambda = 1,2\,\mu\text{m}; W_p = 12\lambda = 3,6\,\mu\text{m}$ | Cân bằng trễ $t_{pHL} \approx t_{pLH}$. |
| $R_{on,n}, R_{on,p}$ | Điện trở dẫn tương đương | $969\,\Omega$ và $992\,\Omega$ | Tại $V_{GS} = 5\,\text{V}, V_{DS} \to 0$. |
| $C_{in}(\text{INV\_X1})$ | Điện dung ngõ vào danh định | $11,43\,\text{fF}$ | Gồm $10,47\,\text{fF}$ kênh oxit + $0,96\,\text{fF}$ chồng lấp. |

---

## 3. BA NGUYÊN TẮC SƯ PHẠM CỐT LÕI
1. **"Tính trước — Đo sau — So sánh — Giải thích sai lệch":** Không cho sinh viên chạy mô phỏng khi chưa có con số ước lượng trên giấy.
2. **Minh bạch hóa giới hạn của mô hình:** Công thức $0,69 \cdot R_{on} \cdot C_L$ chỉ là cận dưới giải tích; trễ thực tế SPICE luôn lớn hơn $\sim 1,5 - 1,8$ lần do dòng bão hòa hữu hạn.
3. **Quy tắc định cỡ chuẩn theo Inverter cơ sở:** Mọi cổng logic đa ngõ vào đều định cỡ sao cho đường dẫn xấu nhất có điện trở tương đương $R_{on}$ của $\text{INV\_X1}$.
"""

with open('Teacher_Book/README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)
print('Wrote Teacher_Book/README.md')
