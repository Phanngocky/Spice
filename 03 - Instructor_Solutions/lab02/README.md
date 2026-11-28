# HƯỚNG DẪN GIẢNG VIÊN & ĐÁP ÁN MẪU: BÀI LAB 02
## THIẾT KẾ CỔNG LOGIC TĨNH NAND2 VÀ NOR2 CMOS

> [!CAUTION]
> **TÀI LIỆU NỘI BỘ DÀNH CHO GIẢNG VIÊN VÀ TRỢ GIẢNG (TA)**  
> Không phân phát tài liệu này cho sinh viên. Tài liệu này cung cấp các giá trị chuẩn, kết quả tính toán giải tích và hướng dẫn chấm thi thực hành tại bàn.

---

### 1. TỔNG QUAN VÀ BẢN ĐỒ MÃ NGUỒN KIỂM CHỨNG

Thư mục này chứa đầy đủ các tệp SPICE Netlist hoàn chỉnh đã được kiểm chứng cú pháp và mô phỏng trên tiến trình MOSIS C5N 0.5µm (`C5_models.txt`):
- `nand2_dc_vtc.sp`: Quét DC phân tích đường cong truyền đạt VTC và ngưỡng chuyển mạch $V_M$ (1 ngõ vs 2 ngõ nối chung).
- `nand2_tran_meas.sp`: Mô phỏng Transient đo trễ tự động bằng câu lệnh `.MEAS` cho 3 kịch bản chuyển mạch và khảo sát hiệu ứng nút nội $X_n$ ở 2 mức tải ($50\,\text{fF}$ và $10\,\text{fF}$).
- `nor2_tran_meas.sp`: Mô phỏng Transient cổng NOR2 với ngõ vào tĩnh nối đất $0\,\text{V}$, đối sánh hiệu năng trường hợp xấu nhất / tốt nhất.
- `nand2_pex_postlayout.sp`: Mô phỏng sau trích xuất ký sinh PEX để đo đạc độ suy giảm tốc độ thực tế.
- `dap_an_chi_tiet_lab02.md`: Đáp án chi tiết từng câu hỏi trong Phiếu báo cáo và Pre-lab/Post-lab của sinh viên.

---

### 2. KẾT QUẢ BENCHMARK CHUẨN (MOSIS C5N 0.5µm, VDD = 5.0V)

| Thông số đo đạc | Giá trị Lý thuyết Giải tích | Mô phỏng Pre-layout | Mô phỏng Post-layout (PEX) | Ghi chú đánh giá chuyên môn |
| :--- | :---: | :---: | :---: | :--- |
| **Kích thước NAND2** | NMOS: $8\lambda$ / PMOS: $12\lambda$ | $W_n=2,4\,\mu\text{m}, W_p=3,6\,\mu\text{m}$ | $W_n=2,4\,\mu\text{m}, W_p=3,6\,\mu\text{m}$ | Cân bằng $R_{eq,N} \approx 969\,\Omega, R_{eq,P} \approx 992\,\Omega$ |
| **Kích thước NOR2** | NMOS: $4\lambda$ / PMOS: $24\lambda$ | $W_n=1,2\,\mu\text{m}, W_p=7,2\,\mu\text{m}$ | $W_n=1,2\,\mu\text{m}, W_p=7,2\,\mu\text{m}$ | Cân bằng $R_{eq,P} \approx 992\,\Omega, R_{eq,N} \approx 969\,\Omega$ |
| **$V_M$ NAND2 (1 ngõ, $B=5\text{V}$)** | $2,450\,\text{V}$ | $2,44 - 2,50\,\text{V}$ | $2,44 - 2,50\,\text{V}$ | Cân bằng tốt quanh $V_{DD}/2$ |
| **$V_M$ NAND2 (2 ngõ chung $A=B$)** | $2,750\,\text{V}$ | $2,68 - 2,75\,\text{V}$ | $2,68 - 2,75\,\text{V}$ | Dời sang phải $+300\,\text{mV}$ do 2 PMOS dẫn |
| **$V_M$ NOR2 (1 ngõ, $B=0\text{V}$)** | $2,450\,\text{V}$ | $2,43 - 2,49\,\text{V}$ | $2,43 - 2,49\,\text{V}$ | Cân bằng tốt quanh $V_{DD}/2$ |
| **$V_M$ NOR2 (2 ngõ chung $A=B$)** | $2,180\,\text{V}$ | $2,22 - 2,28\,\text{V}$ | $2,22 - 2,28\,\text{V}$ | Dời sang trái $-270\,\text{mV}$ do 2 NMOS dẫn |
| **Trễ $t_{pHL}$ NAND2 ($A$ sw, $50\text{fF}$)** | $33,6\,\text{ps}$ | $48 - 54\,\text{ps}$ | $68 - 76\,\text{ps}$ | Nút nội đã xả điện trước |
| **Trễ $t_{pHL}$ NAND2 ($B$ sw, $50\text{fF}$)** | $35,3\,\text{ps}$ | $51 - 57\,\text{ps}$ | $72 - 82\,\text{ps}$ | Chậm hơn $\sim 5 - 6\%$ |
| **Trễ $t_{pHL}$ NAND2 ($A$ sw, $10\text{fF}$)** | $6,7\,\text{ps}$ | $11 - 14\,\text{ps}$ | $18 - 24\,\text{ps}$ | Tải nhẹ ngoài |
| **Trễ $t_{pHL}$ NAND2 ($B$ sw, $10\text{fF}$)** | $8,4\,\text{ps}$ | $14 - 18\,\text{ps}$ | $24 - 31\,\text{ps}$ | **Chậm hơn $20 - 25\%$ do xả tụ nút nội $C_{int}$** |
| **Trễ $t_{pLH}$ NAND2 (1 PMOS, $50\text{fF}$)** | $34,4\,\text{ps}$ | $50 - 58\,\text{ps}$ | $70 - 80\,\text{ps}$ | Trường hợp xấu nhất |
| **Trễ $t_{pLH}$ NAND2 (2 PMOS, $50\text{fF}$)** | $17,2\,\text{ps}$ | $26 - 32\,\text{ps}$ | $38 - 46\,\text{ps}$ | Nhanh gấp đôi do $R_{eq}$ giảm $1/2$ |
| **Trễ $t_{pLH}$ NOR2 (2 PMOS, $50\text{fF}$)** | $34,4\,\text{ps}$ | $58 - 68\,\text{ps}$ | $88 - 105\,\text{ps}$ | Chậm hơn rõ rệt do Body Effect trên chuỗi PMOS |
| **Trễ $t_{pHL}$ NOR2 (1 NMOS, $50\text{fF}$)** | $33,6\,\text{ps}$ | $46 - 52\,\text{ps}$ | $64 - 72\,\text{ps}$ | Trường hợp xấu nhất |
| **Trễ $t_{pHL}$ NOR2 (2 NMOS, $50\text{fF}$)** | $16,8\,\text{ps}$ | $24 - 28\,\text{ps}$ | $34 - 40\,\text{ps}$ | Nhanh gấp đôi do $R_{eq}$ giảm $1/2$ |
| **Tổng bề rộng kênh $\sum W$** | NAND: $40\lambda$ / NOR: $56\lambda$ | $12,0\,\mu\text{m}$ vs $16,8\,\mu\text{m}$ | $12,0\,\mu\text{m}$ vs $16,8\,\mu\text{m}$ | **NOR2 lớn hơn $+40,0\%$** |
| **Điện dung ngõ vào $C_{in}$** | NAND: $20\lambda$ / NOR: $28\lambda$ | $1,25 \times \text{INV}$ vs $1,75 \times \text{INV}$ | $1,25 \times \text{INV}$ vs $1,75 \times \text{INV}$ | **NOR2 nặng hơn $+40,0\%$ (Logical Effort $g$)** |
| **Diện tích Layout hình học** | N/A | NAND: $\approx 105 - 120\,\mu\text{m}^2$ | NOR: $\approx 160 - 180\,\mu\text{m}^2$ | **NOR2 tốn diện tích hơn $+45 - 50\%$** |
| **DRC MOSIS Errors** | 0 | 0 | 0 | Bắt buộc 0 lỗi |
| **LVS Comparison (NCC)** | N/A | N/A | **MATCH 100%** | "Cells are topologically equivalent" |

---

### 3. CÂU HỎI VẤN ĐÁP TẠI BÀN (ORAL EXAM QUESTIONS)

1. *Hỏi:* "Tại sao khi ngõ vào B chuyển mạch sau A, thời gian trễ sườn xuống $t_{pHL}$ của cổng NAND2 lại chậm hơn trường hợp A chuyển mạch sau B?"  
   *Trả lời chuẩn:* Vì giữa 2 NMOS nối tiếp có một nút nội trung gian $X_n$. Khi $A=1$ và $B=0$, ngõ ra đang ở mức $5\,\text{V}$, transistor trên dẫn làm tụ ký sinh tại nút nội nạp lên điện thế xấp xỉ $V(X_n) \approx V_{DD} - V_{tn}(V_X) \approx 3,7 - 3,9\,\text{V}$ (có xét Body Effect). Khi $B$ nhảy lên $1$, transistor dưới $M_{NB}$ phải xả đồng thời cả điện tích của tụ ngõ ra $C_L$ lẫn tụ nút nội $C_{int}$ xuống đất, làm tăng thời gian xả $t_{pHL}$ từ $20 - 25\%$ ở tải nhẹ.
2. *Hỏi:* "Đường đi Euler (Eulerian Path) có vai trò gì trong việc vẽ Layout vi mạch CMOS?"  
   *Trả lời chuẩn:* Đường đi Euler trên đồ thị mạch cho phép sắp xếp thứ tự các cổng Polysilicon giống nhau trên cả hai dải Active (P và N) theo thứ tự $A-B$. Nhờ đó, các cực má hoặc cực nguồn kề nhau có thể dùng chung một vùng khuếch tán liền mạch (Abutment), loại bỏ các khoảng cách ly $3\lambda$, giảm kích thước tế bào từ $25 - 35\%$ và triệt tiêu một nửa tụ ký sinh cực má $C_{db}$.
3. *Hỏi:* "Nếu cả hai cổng NAND2 và NOR2 cùng được định cỡ để có trễ worst-case bằng nhau ở tải cố định $50\,\text{fF}$, tại sao trong vi mạch số người ta luôn ưu tiên chọn cổng NAND?"  
   *Trả lời chuẩn:* Vì độ linh động electron lớn gấp 3 lần lỗ trống ($\mu_n \approx 3\mu_p$). Cổng NOR2 buộc phải dùng 2 PMOS nối tiếp $W_p = 24\lambda$, dẫn tới:
   - Tổng chiều rộng kênh $\sum W$ lớn hơn $+40\%$ (tốn diện tích silicon).
   - Điện dung ngõ vào $C_{in}$ lớn hơn $+40\%$ ($g=1,75$ so với $1,25$), làm tầng logic lái phía trước bị tải nặng và chậm đi $40\%$.
   - Chuỗi PMOS nối tiếp bị hiệu ứng thân (Body Effect) làm suy giảm dòng kéo lên thực tế.
4. *Hỏi:* "Tại sao khoảng cách giữa hai dải Poly tại cực má chung của NAND2 phải là $6\lambda$ mà không thể là $3\lambda$?"  
   *Trả lời chuẩn:* Vì tại cực má chung có đặt Contact kim loại nối ra chân Out. Chiều rộng Contact là $2\lambda$, khoảng cách cách ly từ Contact tới mỗi dải Poly tối thiểu là $2\lambda$ (Rule 3.2.b). Do đó khoảng cách Poly-to-Poly qua Contact phải là $2 + 2 + 2 = 6\lambda = 1,80\,\mu\text{m}$. Luật $\ge 3\lambda$ chỉ áp dụng cho hai dải Poly không có tiếp xúc ở giữa.
