# Lộ trình bộ lab thực hành VLSI (đề xuất, cần giảng viên chốt)

## Ràng buộc từ đề cương
- 3 tín chỉ: LT 24, BT 6, ĐA 15 tiết; 15 tuần, mỗi buổi 3 tiết. Không có tiết thực hành riêng.
- Quỹ giờ khả dụng cho thực hành: ĐA 15 + BT 6 = 21 tiết = **7 buổi**. Bộ lab gốc có 11 bài × 5 tiết = 55 tiết, vượt quỹ giờ khoảng 2,6 lần.
- Chương 4 (công suất) và Chương 5 (liên kết nối) chưa có lab; Lab 8 (SRAM) và Lab 9 (CLA) nằm ngoài danh sách nội dung của đề cương.
- Công cụ: LTspice, Electric VLSI, MOSIS C5 (0,5 µm, 5 V).

## Phương án mặc định
Làm 7 buổi bắt buộc; Pre-lab ở nhà (dùng quỹ 90 giờ tự học); layout/DRC/LVS/PEX chỉ ở ba lab then chốt. Các lab còn lại dừng ở sơ đồ + SPICE, hoặc chuyển thành tự chọn / đề tài đồ án.

| Lab | Tên đề xuất | Chương đề cương | Vai trò | Layout | Trạng thái |
|---|---|---|---|---|---|
| 0 | Làm quen SPICE với LTspice | Ch1, Ch3 | Bắt buộc | Không | **Xong** (student + teacher book) |
| 1 | Đặc tính MOSFET và CMOS inverter | Ch2, Ch3 | Bắt buộc | Layout inverter + DRC | **Xong** (student + teacher book) |
| 2 | Cổng tĩnh NAND/NOR | Ch6 | Bắt buộc | Không | Chưa |
| 3 | Cổng phức hợp AOI/OAI và nỗ lực logic | Ch3, Ch6 | Bắt buộc | Layout AOI21 + DRC + LVS (NCC) | Chưa |
| 4 | Transmission gate và MUX | Ch6 | Gộp vào Lab 6 hoặc tự chọn | Không | Chưa |
| 5 | Mạch tuần tự: latch và flip-flop | Ch7 | Bắt buộc | Không | Chưa |
| 6 | Mạch cộng toàn phần | Ch6 | Bắt buộc | Không | Chưa |
| 7 | Logic động (dynamic CMOS) | Ch6 | Tự chọn | Không | Chưa |
| 8 | Ô nhớ SRAM 6T và sense amplifier | Ngoài đề cương | Tự chọn / đề tài đồ án | Không | Chưa |
| 9 | Khối cộng nhanh CLA 4-bit | Ngoài đề cương | Tự chọn / đề tài đồ án | Không | Chưa |
| 10 | Capstone: ALU 4-bit (bản thu nhỏ) | Đồ án (Ch1, 6, 7) | Bắt buộc | Layout một lát cắt 1 bit + LVS + PEX | Chưa |
| 11 | Công suất động và tĩnh (mới) | Ch4 | Tự chọn / về nhà | Không | Chưa có |
| 12 | Dây liên kết RC, bộ lặp, xuyên âm (mới) | Ch5 | Tự chọn / về nhà | Không | Chưa có |

Bảy buổi bắt buộc: Lab 0, 1, 2, 3, 5, 6, 10.

## Gợi ý nội dung cho hai lab mới
- **Lab 11 (công suất, LTspice thuần):** đo năng lượng mỗi chu kỳ bằng `.meas ... INTEG`, kiểm P = α·C·V²·f khi quét f, α, C_L; đo dòng rò khi ngõ vào tĩnh; quét V_DD; so mất mát trong R với ½CV² (nối từ mục B2 của teacher book Lab 0).
- **Lab 12 (liên kết nối, LTspice thuần):** dây RC dạng thang π nhiều đoạn; so trễ đo với Elmore và với hệ số 0,38·R·C của dây phân bố; chèn bộ lặp và tìm số bộ lặp tối ưu; hai dây kề nhau có tụ ghép để quan sát xuyên âm.

## Hướng mở rộng kỹ năng thực tế (tùy chọn)
- Góc quá trình/điện áp/nhiệt độ (PVT) bằng `.step`; mismatch bằng Monte-Carlo.
- Đặc trưng hóa một tế bào: bảng trễ theo tải và độ dốc xung vào.
- Nhánh mã nguồn mở (ngspice, Magic, Netgen, SKY130, OpenLane) nếu có Linux hoặc WSL. Cần xác minh phiên bản và PDK trước khi đưa vào giáo trình.

## Ghi chú cập nhật trạng thái
Khi hoàn thành một lab, đổi cột Trạng thái và ghi liên kết hai tài liệu (student, teacher). Nếu lộ trình thay đổi sau khi giảng viên chốt quỹ giờ, sửa bảng này trước tiên.
