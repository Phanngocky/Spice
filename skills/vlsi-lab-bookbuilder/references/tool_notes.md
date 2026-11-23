# Ghi chú công cụ

## LTspice (độ tin cậy cao; phím tắt có thể khác nhẹ theo phiên bản)
- `.tran <Tstep> <Tstop> [Tstart [dTmax]]`. Đặt Tstep = 0 để chương trình tự chọn; đặt `dTmax` nhỏ (≤ τ/100 và ≤ một phần mười thời gian sườn) khi cần đo chính xác.
- Đơn vị: không phân biệt hoa/thường. `m` và `M` đều là milli; mega là `Meg`; `1F` là 1 femto; `10nF` hợp lệ vì chữ sau tiền tố bị bỏ qua.
- Một nguồn có thể mang cả `PULSE(...)` và `AC 1`, nhưng mỗi lần chạy chỉ bật một lệnh phân tích.
- Tham số: `.param Rval=20k`, dùng `{Rval}` trong sơ đồ; `.step param Rval list 5k 10k 20k 40k`. Mức đo theo tham số: `.meas ... V(out)={0.5*Vdd}`.
- Kết quả `.meas` nằm trong SPICE Error Log (`Ctrl+L`). Chuột phải vào Error Log có mục vẽ dữ liệu `.meas` theo `.step` (Plot .step'ed .meas data).
- Quy ước dấu: dòng qua linh kiện hai cực dương khi chảy vào cực thứ nhất theo thứ tự nút trong netlist. Với nguồn áp, `I(V1)` âm khi nguồn đang cấp điện cho mạch.
- Mô hình ngoài: `.include C5_models.txt`; nếu đường dẫn có khoảng trắng, đặt trong ngoặc kép. Tên model phải khớp dòng `.MODEL` (có thể là `N`/`P` hoặc `CMOSN`/`CMOSP`): mở tệp trước khi viết handout.
- `nmos4`: thứ tự chân là drain, gate, source, bulk. Log của `.op` có bảng "MOSFET Transistors" (Id, Vgs, Vds, gm).
- Phím tắt thường dùng: F2 chọn linh kiện, F3 vẽ dây, F4 nhãn nút, F5 xóa, F6 sao chép, F7 di chuyển, F8 kéo, F9 hoàn tác, `R/C/L` đặt linh kiện, `G` đất, `S` lệnh SPICE, `Ctrl+R` xoay, `Ctrl+E` lật gương, `Space` thu phóng vừa màn hình.

## Electric VLSI (cần xác minh trên bản đã cài, không tự bịa)
Bộ lab gốc dùng Electric với công nghệ MOSIS C5 (0,5 µm, 5 V); L = 0,6 µm = 2λ và W = 1,2 µm = 4λ, tức λ = 0,3 µm theo văn bản gốc. Luồng làm việc: schematic → layout → DRC → LVS (NCC) → trích ký sinh → mô phỏng hậu layout.
Trước khi viết bất kỳ bước thao tác nào:
- Mở đúng phiên bản đã cài và xác nhận tên menu, tên công nghệ, giá trị quy tắc thiết kế (ví dụ khoảng cách poly–poly, metal1). Lab gốc có số liệu quy tắc cần đối chiếu lại với bảng quy tắc của công nghệ.
- Ghi tên menu theo ảnh chụp thực tế của giảng viên; nếu chưa có, ghi "cần xác nhận" thay vì đoán.
- Không nêu "DRC 0 lỗi, LVS khớp 100%" như kết quả bảo đảm; nêu là tiêu chí đạt.

## Claude Docs (khi có công cụ Docs)
- Tạo mỗi lab hai tài liệu riêng: "Lab N — <tên> (handout sinh viên)" và "Lab N — Gói giảng viên (...)".
- Tài liệu chỉ có chữ: một lệnh `batch` với danh sách rỗng và `container` là đối tượng `{"kind":"project","create":{"name":...,"doc":{"markdown":...}}}`; markdown dưới 32 KB mỗi lần. Ngay sau đó mở bằng Artifact (action `open`) với liên kết trong kết quả. Phần còn lại, nếu có, thêm bằng `update` (insert ở cuối gốc).
- Không tạo tài liệu mới để sửa tài liệu cũ; dùng `update`.
- Chèn trước một khối: `target {"kind":"blocks","ids":["<phiên>.<số>"]}`, `side:"before"`; id phải đầy đủ (phiên + số), không dùng id rút gọn.
- Thay cả khối cần `ifHash` và `ifRev` (lấy từ lần đọc hoặc từ kết quả của chính thao tác tạo khối). Thay chữ: `target {"kind":"find","text":...}`, `with {"from":{"kind":"inline","content":...},"as":"text"}`.
- Ô bảng không được chứa ký tự gạch đứng (ví dụ `|H|`): khối bảng sẽ vỡ thành đoạn văn. Viết "biên độ" thay vì `|H|`.
- Công thức: dùng ký hiệu Unicode (τ, ·, ≈, ≤), mũ viết `10^-6`. Không dùng LaTeX.
- Nếu không có Docs: xuất hai tệp .md.
