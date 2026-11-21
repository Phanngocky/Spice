# HƯỚNG DẪN GIẢNG VIÊN & ĐÁP ÁN MẪU: BÀI LAB 02
## THIẾT KẾ CỔNG LOGIC TĨNH NAND2 VÀ NOR2 CMOS

> [!CAUTION]
> **TÀI LIỆU NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TA)**  
> Tuyệt đối không phân phát tài liệu này cho sinh viên. Tài liệu này cung cấp các giá trị chuẩn, kết quả tính toán giải tích và hướng dẫn chấm thi thực hành tại bàn.

---

### 1. TỔNG QUAN VÀ BẢN ĐỒ MÃ NGUỒN KIỂM CHỨNG

Thư mục này chứa đầy đủ các tệp SPICE Netlist hoàn chỉnh đã được kiểm chứng cú pháp và mô phỏng trên tiến trình MOSIS C5N 0.5µm (`C5_models.txt`):
- `nand2_dc_vtc.sp`: Quét DC phân tích đường cong truyền đạt VTC và ngưỡng chuyển mạch $V_M$.
- `nand2_tran_meas.sp`: Mô phỏng Transient đo trễ tự động bằng câu lệnh `.MEAS` cho 3 kịch bản chuyển mạch và khảo sát hiệu ứng nút nội $C_{int}$.
- `nor2_tran_meas.sp`: Mô phỏng Transient cổng NOR2 đối sánh hiệu năng trường hợp xấu nhất / tốt nhất.
- `nand2_pex_postlayout.sp`: Mô phỏng sau trích xuất ký sinh PEX để đo đạc độ suy giảm tốc độ thực tế.
- `dap_an_chi_tiet_lab02.md`: Đáp án chi tiết từng câu hỏi trong Phiếu báo cáo điền khuyết của sinh viên.

---

### 2. KẾT QUẢ BENCHMARK CHUẨN

| Thông số đo đạc | Giá trị Lý thuyết | Mô phỏng Pre-layout | Mô phỏng Post-layout (PEX) | Ghi chú đánh giá |
| :--- | :---: | :---: | :---: | :--- |
| **Kích thước NAND2** | NMOS: $8\lambda$ / PMOS: $12\lambda$ | Đúng kích thước | Đúng kích thước | $W_n=2.4\mu\text{m}, W_p=3.6\mu\text{m}$ |
| **Kích thước NOR2** | NMOS: $4\lambda$ / PMOS: $24\lambda$ | Đúng kích thước | Đúng kích thước | $W_n=1.2\mu\text{m}, W_p=7.2\mu\text{m}$ |
| **$V_M$ NAND2 (B=5V)** | $2.50\,\text{V}$ | $2.45 - 2.52\,\text{V}$ | $2.45 - 2.52\,\text{V}$ | Quét $V_A$ |
| **Trễ $t_{pHL}$ NAND2 (A switch)**| $33.4\,\text{ps}$ | $48 - 55\,\text{ps}$ | $68 - 78\,\text{ps}$ | Nút nội đã xả điện trước |
| **Trễ $t_{pHL}$ NAND2 (B switch)**| $33.4\,\text{ps}$ | $58 - 68\,\text{ps}$ | $78 - 92\,\text{ps}$ | Chậm hơn $\sim 20\%$ do xả $C_{int}$ |
| **Trễ $t_{pLH}$ NAND2 (1 PMOS)** | $34.2\,\text{ps}$ | $50 - 60\,\text{ps}$ | $68 - 80\,\text{ps}$ | Trường hợp xấu nhất |
| **Trễ $t_{pLH}$ NAND2 (2 PMOS)** | $17.1\,\text{ps}$ | $26 - 32\,\text{ps}$ | $38 - 48\,\text{ps}$ | Nhanh gấp đôi do $R_{eq}$ giảm 1/2 |
| **Trễ $t_{pLH}$ NOR2 (Worst)** | $34.2\,\text{ps}$ | $58 - 70\,\text{ps}$ | $85 - 105\,\text{ps}$ | Chậm hơn NAND2 đáng kể |
| **Diện tích Layout hình học** | N/A | N/A | NAND: $\sim 115\mu\text{m}^2$ / NOR: $\sim 165\mu\text{m}^2$ | NOR lớn hơn $\approx 43\%$ |
| **DRC MOSIS Errors** | 0 | 0 | 0 | Phải đạt 0 lỗi |
| **LVS Comparison** | N/A | N/A | **MATCH** | "Cells are topologically equivalent" |

---

### 3. CÂU HỎI VẤN ĐÁP TẠI BÀN (ORAL EXAM QUESTIONS)

1. *Hỏi:* "Tại sao khi ngõ vào B chuyển mạch sau A, thời gian trễ sườn xuống $t_{pHL}$ của cổng NAND2 lại chậm hơn trường hợp A chuyển mạch sau B?"  
   *Trả lời chuẩn:* Vì giữa 2 NMOS nối tiếp có một nút nội trung gian $X_n$. Khi $A=1$ và $B=0$, ngõ ra đang ở mức $5\,\text{V}$, làm tụ ký sinh tại nút nội nạp lên điện thế xấp xỉ $V_{DD} - V_{thn} \approx 4.3\,\text{V}$. Khi $B$ nhảy lên $1$, dòng xả qua transistor dưới phải gánh xả đồng thời cả điện tích của tụ ngõ ra $C_L$ lẫn tụ nút nội $C_{int}$ xuống đất, làm kéo dài thời gian xả $t_{pHL}$.
2. *Hỏi:* "Đường đi Euler (Eulerian Path) có vai trò gì trong việc vẽ Layout vi mạch CMOS?"  
   *Trả lời chuẩn:* Đường đi Euler trên đồ thị mạch cho phép sắp xếp thứ tự các cổng Polysilicon giống nhau trên cả hai dải Active (P và N). Nhờ đó, các transistor cạnh nhau có thể ghép chung (Abutment) cực má hoặc cực nguồn vào cùng một vùng khuếch tán, loại bỏ các khoảng ngắt khuếch tán, giảm kích thước tế bào và triệt tiêu một nửa tụ ký sinh khuếch tán.
3. *Hỏi:* "Nếu phải chọn giữa cổng NAND và NOR để xây dựng thư viện tế bào chuẩn cho vi mạch số, tại sao các hãng sản xuất bán dẫn luôn chọn NAND làm tế bào ưu tiên?"  
   *Trả lời chuẩn:* Vì trong bán dẫn silicon, độ linh động của điện tử trong NMOS gấp 3 lần lỗ trống trong PMOS. Cổng NAND ghép nối tiếp NMOS chỉ cần tăng $W_n$ lên gấp đôi ($8\lambda$), trong khi cổng NOR ghép nối tiếp PMOS phải tăng $W_p$ lên gấp đôi của kích thước vốn đã lớn ($24\lambda$). Hậu quả là cổng NOR có diện tích silicon lớn hơn $40-50\%$, điện dung ngõ vào lớn hơn $40\%$, và trễ Post-layout chậm hơn NAND từ $25-35\%$.
