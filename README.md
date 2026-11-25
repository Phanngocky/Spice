# THỰC HÀNH THIẾT KẾ VLSI (VLSI DESIGN LABORATORY)
### Chương trình Đào tạo Kỹ sư Thiết kế Vi mạch Bán dẫn (2026)
**Trường Đại học Sư phạm Kỹ thuật – Đại học Đà Nẵng (UTE - ĐHĐN)**  
**Bộ môn:** Điện tử - Viễn thông | **Khoa:** Điện - Điện tử  
**Mã học phần:** `5505382` | **Số tín chỉ:** 2 tín chỉ thực hành (60 tiết tại phòng Lab máy tính)

---

## 1. TỔNG QUAN VÀ ĐỊNH VỊ HỌC PHẦN

Học phần **Thực hành Thiết kế VLSI** là học phần chuyên ngành bắt buộc, định hình năng lực thiết kế vi mạch tích hợp cỡ lớn (VLSI) ở **mức Transistor và mức Vật lý (Full-Custom CMOS IC Design Flow)**.

> [!IMPORTANT]
> **Phân định rõ ràng giữa hai trục thực hành trong CTĐT Vi mạch 2026:**
> - **Trục Front-End & RTL (Mã HP: 5505221 / TH FPGA):** Thực hành thiết kế hệ thống số với ngôn ngữ Verilog HDL trên kit FPGA Intel DE25-Standard (Agilex 5 / Cyclone V), kiểm chứng mô phỏng trên ModelSim/QuestaSim (đã hoàn thiện tài liệu tại thư mục `D:\tam\fpga`).
> - **Trục Transistor & Physical Verification (Học phần này - Mã HP: 5505382):** Thực hành thiết kế vi mạch tùy biến hoàn toàn (Full-Custom CMOS), từ sơ đồ nguyên lý Schematic, mô phỏng SPICE DC/AC/Transient, vẽ sơ đồ que Stick Diagram, thiết kế mặt nạ vật lý Mask Layout, kiểm tra luật hình học DRC, đối chiếu sơ đồ LVS, đến trích xuất ký sinh PEX và mô phỏng Post-layout trên nền tảng **Electric VLSI Design System + LTspice / ngspice** với công nghệ chuẩn **MOSIS SCMOS C5N 0.5µm**.

---

## 2. CẤU TRÚC HỆ THỐNG TÀI LIỆU VÀ MÃ NGUỒN

```
D:\tam\Spice\
├── 01 - De_Cuong_Hoc_Phan/
│   └── De_Cuong_Chi_Tiet_TH_Thiet_Ke_VLSI.md  # Đề cương chi tiết học phần, CLO-PLO, Rubric OBE
├── 02 - Student Workbook/             # Tài liệu phát cho sinh viên (Handouts 3 pha & Mẫu báo cáo)
│   ├── lab-00-nhap-mon-mo-phong-spice-va-ltspice.md # Lab 00: Nhập môn Mô phỏng Mạch với SPICE và LTspice
│   ├── lab-01-dac-tinh-mosfet-va-cmos-inverter.md   # Lab 01: MOSFET I-V & Inverter VTC/Delay/Layout/PEX
│   ├── lab-02-cong-logic-tinh-nand-nor.md     # Lab 02: Cổng NAND2/NOR2, Sizing (W/L), Euler Path
│   ├── lab-03-cong-phuc-hop-aoi-oai-logical-effort.md # Lab 03: AOI/OAI & Logical Effort
│   ├── lab-04-transmission-gate-va-mux.md     # Lab 04: Cổng truyền TG, MUX 2:1 & MUX 4:1
│   ├── lab-05-mach-tuan-tu-latch-va-flipflop.md # Lab 05: D-Latch & D-FF Master-Slave C2MOS/TSPC
│   ├── lab-06-mach-cong-toan-phan-full-adder.md # Lab 06: 1-bit Full Adder (Mirror vs TG Adder)
│   ├── lab-07-logic-dong-dynamic-cmos.md      # Lab 07: Domino Logic & Hiện tượng Charge Sharing
│   ├── lab-08-o-nho-sram-6t-va-sense-amp.md   # Lab 08: 6T SRAM Cell, SNM, Precharge & Sense Amp
│   ├── lab-09-duong-du-lieu-cong-nhanh-cla.md # Lab 09: 4-bit Carry-Lookahead Adder (CLA)
│   └── lab-10-capstone-4bit-registered-alu.md # Lab 10: Capstone Tích hợp Vi mạch 4-bit Registered ALU
├── 03 - Instructor_Solutions/                 # Gói đáp án của giảng viên & barem chấm điểm
│   └── lab01/
│       ├── nmos_iv_curve.sp                  # Netlist SPICE đo đặc tính I-V
│       ├── cmos_inverter_vtc_tran.sp         # Netlist SPICE mô phỏng VTC & Trễ quá độ Pre-layout
│       ├── cmos_inverter_pex_postlayout.sp   # Netlist SPICE mô phỏng sau trích xuất ký sinh PEX
│       └── README.md                         # Đáp án tính tay, bảng benchmark & câu hỏi vấn đáp
├── 04 - Models_and_Libraries/
│   └── C5_models.txt                         # Thư viện mô hình SPICE MOSIS C5N 0.5um (Level 3/BSIM3)
└── Hướng dẫn cài đặt Electric&LTSpice.pdf     # Tài liệu hướng dẫn cài đặt từ Veron Labs
```

---

## 3. LỘ TRÌNH 12 BUỔI THỰC HÀNH VÀ SẢN PHẨM CAPSTONE XUYÊN SUỐT

Sản phẩm xuyên suốt của toàn bộ học phần là: **Xây dựng Thư viện Tế bào Chuẩn (Standard Cell Library) và Tích hợp Vi mạch Đường Dữ liệu 4-bit Registered ALU hoàn chỉnh** qua 12 buổi học:

| Buổi | Tên bài Lab | Trọng tâm Mức Transistor & Vật lý | IP Tế bào bàn giao |
| :---: | :--- | :--- | :--- |
| **01** | **Lab 00** | Nhập môn Mô phỏng Mạch với SPICE & LTspice: Netlist, bảng đơn vị, phân tích .OP, .DC, .TRAN, .AC, câu lệnh đo tự động .MEAS, gọi mô hình ngoài C5_models.txt. | Kỹ năng SPICE & Đo lường tự động. |
| **02** | **Lab 01** | MOSFET I-V ($V_{th}, K', \lambda$), CMOS Inverter VTC, Lề nhiễu, Trễ $t_{pd}$, Layout Inverter, DRC & LVS. | IP `INV_X1` |
| **03** | **Lab 02** | Cổng logic tĩnh NAND2 & NOR2, Sizing cân bằng điện trở $R_{on}$, Đường Euler tối ưu chia sẻ Diffusion. | IP `NAND2_X1`, `NOR2_X1` |
| **04** | **Lab 03** | Cổng phức hợp AOI21/OAI21, Phương pháp Logical Effort tối ưu chuỗi đệm Inverter (Buffer Chain). | IP `AOI21_X1`, `BUF_CHAIN` |
| **05** | **Lab 04** | Cổng truyền Transmission Gate (TG), MUX 2:1 và MUX 4:1 mức transistor, so sánh với MUX cổng tĩnh. | IP `TG_GATE`, `MUX2_TG`, `MUX4_TG` |
| **06** | **Lab 05** | Mạch tuần tự mức transistor: D-Latch và D-Flip-Flop Master-Slave C²MOS, đo $t_{setup}, t_{hold}, t_{c-q}$. | IP `DLATCH_X1`, `DFF_MS_X1` |
| **07** | **Lab 06** | Mạch cộng 1-bit Full Adder (Mirror Adder vs TG Adder), tối ưu đường trễ Carry Propagation. | IP `FULL_ADDER_1B` |
| **08** | **Lab 07** | Logic động (Dynamic CMOS Logic): Domino Logic, hiện tượng phân chia điện tích và Keeper Transistor. | Khối Domino OR4/AND4 |
| **09** | **Lab 08** | Ô nhớ SRAM 6T, tỉ lệ Cell Ratio / Pull-up Ratio, Static Noise Margin (SNM), Precharge & Sense Amp. | Khối SRAM 1-bit Cell |
| **10** | **Lab 09** | Đường dữ liệu Bộ cộng nhanh 4-bit CLA (Carry-Lookahead Adder), định tuyến 2 lớp kim loại Metal 1/2. | IP `CLA_ADDER_4B` |
| **11** | **Lab 10** | **Capstone Project:** Tích hợp Vi mạch 4-bit Registered ALU hoàn chỉnh (CLA4 + MUX4 + DFF + Power Ring). | Top-Level Registered ALU |
| **12** | **Buổi 12** | Báo cáo nghiệm thu Capstone, Bảo vệ phương án Layout/Sizing và Thi vấn đáp thực hành tại bàn. | Báo cáo & Điểm tổng kết |

---

## 4. QUY TRÌNH THỰC HIỆN BÀI LAB (CHUẨN 3 PHA)

1. **Pre-lab (Ở nhà):**
   - Tính toán thông số kích thước $(W/L)$, điện áp chuyển mạch $V_M$, điện trở dẫn $R_{on}$ và ước lượng trễ lý thuyết.
   - Vẽ sơ đồ que (Stick Diagram) chuẩn Euler Path lên giấy kẻ ô ly.
   - *Yêu cầu: Giảng viên kiểm tra và ký xác nhận đầu giờ; không đạt không được vào máy tính.*
2. **In-lab (Trên lớp):**
   - **Ex1 – Ex3 (Cốt lõi, bắt buộc):** Dựng Schematic, quét DC/Transient trên SPICE, đo lề nhiễu và trễ truyền lan.
   - **Ex4 (Tiêu chuẩn):** Thiết kế Layout vật lý, chạy DRC đạt **0 Errors**, đối chiếu LVS đạt **MATCH** hoàn hảo.
   - **Ex5 (Thử thách nâng cao):** Trích xuất ký sinh PEX, mô phỏng Post-layout, đối chiếu độ suy giảm hiệu năng.
3. **Post-lab (Báo cáo):**
   - Lập bảng đối chiếu 3 chiều: **[Lý thuyết tính tay] vs [SPICE Pre-layout] vs [Đo đạc Post-layout]**.
   - Phân tích nguyên nhân vật lý gây sai lệch (hiệu ứng kênh ngắn, điện dung khuếch tán, ký sinh kim loại).
