# Cổng kiểm số liệu

Bộ lab gốc có nhiều lỗi do số liệu mâu thuẫn hoặc tính tay bị coi như số đo. Cổng kiểm này nhằm tránh lặp lại.

## 1. Nhãn nguồn gốc cho mọi con số định lượng
| Nhãn | Nghĩa | Được ghi ở đâu |
|---|---|---|
| Suy dẫn | Có biểu thức và các bước | Teacher book, phần B và F |
| Script | Tính bằng `quick_checks.py` hoặc Python; nêu mô hình | Teacher book |
| Đo | Từ lần chạy thực tế LTspice/Electric | Cột "Đo" của teacher book, sau khi giảng viên chạy |
| Chưa kiểm | Ước lượng hợp lý nhưng chưa có số đo | Phải ghi rõ "chưa kiểm" |

Quy tắc: không viết "mô phỏng cho thấy", "kết quả đo là" nếu chưa chạy. Môi trường soạn thảo thường **không có LTspice hay Electric**; chạy `which ngspice` để biết có công cụ tương đương không. Nếu có ngspice, netlist viết cho LTspice cần chỉnh cú pháp `.tran`/`.meas` trước khi thử, và vẫn phải ghi rõ là chạy bằng ngspice. Nếu không có tệp `C5_models.txt`, không có số đo Level 3 nào là thật.

## 2. Kiểm tính nhất quán nội bộ
- Cộng lại: tổng số transistor, tổng điểm rubric (= 10), tổng phút của buổi (≤ 135), số câu Pre-lab.
- Mỗi tiêu chí đạt/không đạt phải có thể thỏa với số liệu của chính tài liệu. Ví dụ tiêu chí "V_Q < V_tn" mâu thuẫn khi công thức đưa ra cho giá trị lớn hơn V_tn.
- Số ở Teacher book phải khớp số ở Student book (cùng R, C, V_DD, W/L).
- Một con số xuất hiện ở hai lab (ví dụ t_pd inverter) phải lấy từ một nguồn duy nhất và ghi lab nguồn.

## 3. Kiểm đơn vị và cú pháp
- Đơn vị SPICE: `m` là milli, `Meg` là mega, `1F` là 1 femto. Không viết `10M` khi muốn nói mega.
- Mức đo `.meas` nên theo tham số (`{0.5*Vdd}`) thay vì ghi cứng.
- `.tran <Tstep> <Tstop> [Tstart [dTmax]]`; nêu rõ `dTmax` và lý do.

## 4. Kiểm lý thuyết thường sai
- Hiệu ứng thân áp dụng cho cả NMOS và PMOS khi pass transistor (đối xứng).
- R_on phụ thuộc V_in trong transmission gate; không dùng cùng một giá trị ở mọi V_in.
- Tỉ số "x lần nhanh hơn" khác "cải thiện x %"; viết theo tỉ lệ giảm trễ.
- Chồng transistor nối tiếp: định cỡ theo quy tắc R_on bằng inverter chuẩn, hoặc nêu rõ vì sao không.
- Logical effort: ghi rõ tỉ số µn/µp và C_in của inverter chuẩn khi dùng số fF.
- Mô hình bậc hai (square-law) không có bão hòa vận tốc; số trễ và dòng từ mô hình này chỉ là cận để phát hiện mâu thuẫn.

## 5. Kiểm rò đáp án (Student Book)
Không có: đáp án, cột "Đo" điền sẵn, bảng kết quả kỳ vọng, đường dẫn tới thư mục đáp án, "kết quả mong đợi" kèm số. Được phép có: công thức tổng quát và ví dụ minh họa với số khác Pre-lab.

## 6. Kiểm cuối
Chạy `python scripts/lint_lab.py` cho từng sách, không còn lỗi mức ERROR; mọi WARN đã được xem xét. Nêu trong báo cáo cuối những gì chưa kiểm.
