# BỘ GIÁO TRÌNH NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TEACHER'S BOOK)
## HỌC PHẦN THỰC HÀNH THIẾT KẾ VI MẠCH VLSI (MÃ HỌC PHẦN: 5505382)
### Tiến trình Công nghệ: MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,	ext{V}, \lambda = 0,30\,\mu	ext{m}$)

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
| $V_{DD}$ | Điện áp nguồn danh định | $5,0\,	ext{V}$ | Chuẩn tương thích logic 5V. |
| $\lambda$ | Đơn vị lưới layout mở rộng | $0,30\,\mu	ext{m}$ | Chiều dài kênh tối thiểu $L_{min} = 2\lambda = 0,60\,\mu	ext{m}$. |
| $\lambda_{kênh}$ | Hệ số điều chế độ dài kênh | $0,05\,	ext{V}^{-1}$ | Hệ số LAMBDA trong phương trình dòng điện SPICE. |
| $t_{ox}$ | Độ dày lớp oxit cổng | $9,5\,	ext{nm}$ ($95\,	ext{Å}$) | Handout cũ giả định $14\,	ext{nm}$ là sai lệch! |
| $C_{ox}$ | Điện dung oxit cổng đơn vị | $3,635\,	ext{fF/\mu m}^2$ | $3,453 \cdot 10^{-11} / 9,5 \cdot 10^{-9}$. |
| $V_{tn0}, |V_{tp0}|$ | Điện áp ngưỡng không thiên thế thân | $0,70\,	ext{V}$ và $0,80\,	ext{V}$ | VTO trong model N và P. |
| $K'_n, K'_p$ | Hệ số độ dẫn truyền bản chất | $120\,\mu	ext{A/V}^2$ và $40\,\mu	ext{A/V}^2$ | Tỉ số độ linh động $\mu_n / \mu_p pprox 3,0$. |
| $\gamma_n, \gamma_p$ | Hệ số hiệu ứng thân (Body factor) | $0,40\,	ext{V}^{1/2}$ và $0,50\,	ext{V}^{1/2}$ | GAMMA trong model SPICE. |
| $	ext{INV\_X1}$ | Kích thước Inverter cơ sở | $W_n = 4\lambda = 1,2\,\mu	ext{m}; W_p = 12\lambda = 3,6\,\mu	ext{m}$ | Cân bằng trễ $t_{pHL} pprox t_{pLH}$. |
| $R_{on,n}, R_{on,p}$ | Điện trở dẫn tương đương | $969\,\Omega$ và $992\,\Omega$ | Tại $V_{GS} = 5\,	ext{V}, V_{DS} 	o 0$. |
| $C_{in}(	ext{INV\_X1})$ | Điện dung ngõ vào danh định | $11,43\,	ext{fF}$ | Gồm $10,47\,	ext{fF}$ kênh oxit + $0,96\,	ext{fF}$ chồng lấp. |

---

## 3. BA NGUYÊN TẮC SƯ PHẠM CỐT LÕI
1. **"Tính trước — Đo sau — So sánh — Giải thích sai lệch":** Không cho sinh viên chạy mô phỏng khi chưa có con số ước lượng trên giấy.
2. **Minh bạch hóa giới hạn của mô hình:** Công thức $0,69 \cdot R_{on} \cdot C_L$ chỉ là cận dưới giải tích; trễ thực tế SPICE luôn lớn hơn $\sim 1,5 - 1,8$ lần do dòng bão hòa hữu hạn.
3. **Quy tắc định cỡ chuẩn theo Inverter cơ sở:** Mọi cổng logic đa ngõ vào đều định cỡ sao cho đường dẫn xấu nhất có điện trở tương đương $R_{on}$ của $	ext{INV\_X1}$.
