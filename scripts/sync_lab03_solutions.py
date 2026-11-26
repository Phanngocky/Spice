#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to synchronize Lab 03 Instructor Solutions and master compilation
- 03 - Instructor_Solutions/lab03/README.md
- 03 - Instructor_Solutions/lab03/dap_an_chi_tiet_lab03.md
- 03 - Instructor_Solutions/Teacher_Book_VLSI_Lab01_Lab10.md (Lab 3 section)
"""

# 1. Content for 03 - Instructor_Solutions/lab03/README.md
readme_content = """# HƯỚNG DẪN GIẢNG VIÊN & ĐÁP ÁN MẪU: BÀI LAB 03
## CỔNG PHỨC HỢP AOI21 VÀ TỐI ƯU TRỄ THEO PHƯƠNG PHÁP LOGICAL EFFORT

> [!CAUTION]
> **TÀI LIỆU NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TA)**  
> Tuyệt đối không phân phát tài liệu này cho sinh viên. Tài liệu này cung cấp các giá trị chuẩn, kết quả tính toán giải tích và hướng dẫn chấm thi thực hành tại bàn.

---

### 1. TỔNG QUAN VÀ BẢN ĐỒ MÃ NGUỒN KIỂM CHỨNG

Thư mục này chứa đầy đủ các tệp SPICE Netlist hoàn chỉnh đã được kiểm chứng cú pháp và mô phỏng trên tiến trình MOSIS C5N 0.5µm (`C5_models.txt`):
- `aoi21_logic_tran.sp`: Quét xung kiểm chứng toàn bộ 8 tổ hợp bảng chân trị logic ($A, B, C \in \{0, 1\}^3$) trong $80\,\text{ns}$ và đo trễ worst-case.
- `logical_effort_meas.sp`: Mô phỏng Testbench kép đo Logical Effort $g$ và trễ ký sinh $p$ của AOI21 đối chuẩn trực tiếp với `INV_X1` qua quét tải dung.
- `buffer_chain_opt.sp`: Mô phỏng thực nghiệm bài toán chuỗi đệm lái tải cực nặng $C_L = 1,0\,\text{pF}$ ($H = 50$), đối sánh Inverter đơn $1\times$ vs Chuỗi đệm 3 tầng tối ưu ($\hat{f} = 3,68$).
- `aoi21_pex_postlayout.sp`: Netlist trích xuất ký sinh Post-layout (PEX) với đầy đủ điện dung nút nội $X_n, X_p$ và cực má.
- `dap_an_chi_tiet_lab03.md`: Đáp án chi tiết từng câu hỏi trong Phiếu báo cáo và Pre-lab/Post-lab của sinh viên.

---

### 2. KẾT QUẢ BENCHMARK CHUẨN (MOSIS C5N 0.5µm, VDD = 5.0V)

| Thông số đo đạc | Giá trị Lý thuyết Giải tích | Mô phỏng Pre-layout | Mô phỏng Post-layout (PEX) | Ghi chú đánh giá chuyên môn |
| :--- | :---: | :---: | :---: | :--- |
| **Kích thước AOI21** | NMOS: $8\lambda, 8\lambda, 4\lambda$ / PMOS: $24\lambda \times 3$ | Đúng kích thước | Đúng kích thước | $R_{eq,N} \approx 969\,\Omega, R_{eq,P} \approx 992\,\Omega$ |
| **Chức năng logic AOI21** | 8 trạng thái $Y = \overline{(A \cdot B) + C}$ | Đạt $100\%$ | Đạt $100\%$ | Lấy mẫu tại cuối chu kỳ để tránh glitch |
| **Logical Effort ngõ A ($g_A$)** | $2,000$ ($32\lambda / 16\lambda$) | $1,85 - 2,15$ | $1,90 - 2,20$ | Đối chuẩn trực tiếp với `INV_X1` |
| **Logical Effort ngõ C ($g_C$)** | $1,750$ ($28\lambda / 16\lambda$) | $1,62 - 1,88$ | $1,65 - 1,92$ | Nhẹ tải hơn ngõ A $12,5\%$ |
| **Trễ ký sinh ($p_{AOI21}$)** | $2,250$ ($36\lambda / 16\lambda$) | $1,90 - 2,40$ | $2,40 - 2,90$ | Chuẩn hóa theo $p_{inv}$ |
| **Trễ worst-case ngõ C ($50\text{fF}$)** | $34,4\,\text{ps}$ | $52 - 62\,\text{ps}$ | $74 - 88\,\text{ps}$ | $A=1, B=0$ (chỉ 1 PMOS nhánh song song dẫn) |
| **Trễ ngõ C khi $A=B=0$ ($50\text{fF}$)** | $25,7\,\text{ps}$ | $38 - 46\,\text{ps}$ | $55 - 65\,\text{ps}$ | Nhanh hơn do 2 PMOS cùng dẫn song song |
| **Trễ lái trực tiếp 1X ($1\text{pF}$)** | $\approx 0,68\,\text{ns}$ ($51\tau$) | $0,95 - 1,25\,\text{ns}$ | $1,05 - 1,35\,\text{ns}$ | Sườn xung bị kéo dài rất lớn |
| **Trễ chuỗi đệm 3 tầng ($1\text{pF}$)** | $\approx 0,19\,\text{ns}$ ($14,05\tau$) | $0,28 - 0,36\,\text{ns}$ | $0,35 - 0,45\,\text{ns}$ | **Giảm trễ $> 70\%$ (nhanh hơn $> 3$ lần)** |
| **Tổng bề rộng kênh $\sum W$** | $92\lambda_{DR}$ ($27,6\,\mu\text{m}$) | $27,6\,\mu\text{m}$ | $27,6\,\mu\text{m}$ | Nhỏ hơn $17,86\%$ so với cổng rời ($112\lambda$) |
| **Số lượng Transistor** | 6 Transistors | 6 Transistors | 6 Transistors | Giảm $40\%$ so với cổng rời (10T) |
| **Diện tích Layout hình học** | N/A | $\approx 180 - 210\,\mu\text{m}^2$ | $\approx 180 - 210\,\mu\text{m}^2$ | Thứ tự $C-A-B$, $H_{cell} = 60\lambda$ |
| **DRC MOSIS Errors** | 0 | 0 | 0 | Bắt buộc 0 lỗi |
| **LVS Comparison (NCC)** | N/A | N/A | **MATCH** | Trùng khớp sơ đồ $100\%$ |

---

### 3. CÂU HỎI VẤN ĐÁP TẠI BÀN (ORAL EXAM QUESTIONS)

1. *Hỏi:* "Tại sao trong tế bào AOI21, các transistor PMOS lại phải định cỡ lên tới $24\lambda$ ($7,2\,\mu\text{m}$), gấp đôi kích thước của Inverter chuẩn?"  
   *Trả lời chuẩn:* Vì mạng PUN của AOI21 gồm cụm song song $(A \parallel B)$ mắc nối tiếp với $C$. Trong trường hợp xấu nhất khi chỉ có 1 PMOS trong cụm song song dẫn, dòng nạp phải đi qua 2 PMOS mắc nối tiếp. Để tổng điện trở nhánh không vượt quá $R_{on,p0} \approx 992\,\Omega$, mỗi PMOS phải có chiều rộng kênh gấp đôi PMOS chuẩn ($2 \times 12\lambda = 24\lambda$).
2. *Hỏi:* "Nỗ lực logic $g$ phản ánh điều gì về mặt vật lý của cổng logic?"  
   *Trả lời chuẩn:* Nỗ lực logic $g$ biểu thị tỉ số giữa điện dung ngõ vào của cổng đó so với Inverter chuẩn khi cả hai được định cỡ để có cùng khả năng tải dòng ($R_{on}$). Nó cho biết mức độ 'nặng tải' mà cổng logic đó tạo ra cho tầng lái phía trước so với một Inverter cơ sở.
3. *Hỏi:* "Tại sao thứ tự dải Polysilicon $C - A - B$ lại tối ưu hơn thứ tự $A - B - C$ khi vẽ Layout cổng AOI21?"  
   *Trả lời chuẩn:* Vì với thứ tự $C - A - B$, cực má của $M_{NC}$ và $M_{NA}$ trên dải N-Active nằm kề sát nhau, cho phép dùng chung một tiếp xúc Contact ngõ ra `out` (Abutment). Ngược lại với thứ tự $A - B - C$, cực Out bị tách rời ra hai đầu dải khuếch tán, không thể chia sẻ cực má chung.
4. *Hỏi:* "Trong bài toán chuỗi đệm lái tải nặng $1\,\text{pF}$, tại sao chuỗi 3 tầng lại nhanh hơn việc lái trực tiếp bằng Inverter 1X tới hơn 3 lần?"  
   *Trả lời chuẩn:* Vì Inverter 1X có kích thước quá nhỏ, nỗ lực điện $H = 50$ làm thời gian xả dòng bị kéo dài nghiêm trọng ($D = 51\tau$). Khi chèn chuỗi 3 tầng với hệ số phóng đại mỗi tầng $\hat{f} \approx 3,68$, mỗi tầng chỉ phải lái một tải dung vừa phải gấp $\approx 3,7$ lần chính nó, giúp các tầng chuyển mạch rất nhanh và tổng trễ chỉ còn $14,05\tau$ (giảm trễ $72,5\%$).
5. *Hỏi:* "Tính chất 'đáy phẳng' của hàm tối ưu chuỗi đệm có ý nghĩa thực tế gì đối với kỹ sư vi mạch?"  
   *Trả lời chuẩn:* Đường cong trễ theo số tầng $N$ có đáy rất phẳng quanh điểm cực tiểu. Ví dụ với $H=50$, trễ của $N=4$ ($14,64\tau$) chỉ chậm hơn $N=3$ ($14,05\tau$) có $4\%$. Điều này cho phép kỹ sư linh hoạt chọn $N=4$ nếu cần giữ nguyên pha tín hiệu logic mà không sợ làm suy thoái tốc độ của toàn mạch.
"""

with open(r"d:\tam\VLSI_Spice\03 - Instructor_Solutions\lab03\README.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(readme_content)
print("Updated 03 - Instructor_Solutions/lab03/README.md")

# 2. Update 03 - Instructor_Solutions/lab03/dap_an_chi_tiet_lab03.md
with open(r"d:\tam\VLSI_Spice\Teacher_Book\Lab03_Teacher_Book.md", "r", encoding="utf-8") as f:
    tb_content = f.read()

with open(r"d:\tam\VLSI_Spice\03 - Instructor_Solutions\lab03\dap_an_chi_tiet_lab03.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(tb_content)
print("Updated 03 - Instructor_Solutions/lab03/dap_an_chi_tiet_lab03.md")

# 3. Update Lab 3 in 03 - Instructor_Solutions/Teacher_Book_VLSI_Lab01_Lab10.md
master_path = r"d:\tam\VLSI_Spice\03 - Instructor_Solutions\Teacher_Book_VLSI_Lab01_Lab10.md"
with open(master_path, "r", encoding="utf-8") as f:
    master_text = f.read()

start_marker = "# 3. LAB 3 — CỔNG PHỨC HỢP AOI/OAI VÀ LOGICAL EFFORT (CHƯƠNG 3, 6)"
end_marker = "# 4. LAB 4 — CỔNG TRUYỀN (TG) VÀ BỘ DỒN KÊNH MUX (CHƯƠNG 6)"

pos_start = master_text.find(start_marker)
pos_end = master_text.find(end_marker)

if pos_start != -1 and pos_end != -1:
    new_lab03_section = tb_content[tb_content.find(start_marker):]
    replacement = new_lab03_section.strip() + "\n\n---\n\n"
    updated_master = master_text[:pos_start] + replacement + master_text[pos_end:]
    with open(master_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(updated_master)
    print("Updated Lab 3 in 03 - Instructor_Solutions/Teacher_Book_VLSI_Lab01_Lab10.md")
else:
    print(f"Could not find markers: pos_start={pos_start}, pos_end={pos_end}")
