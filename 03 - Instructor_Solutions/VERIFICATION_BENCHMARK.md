# BẢN ĐỐI CHIẾU KIỂM CHỨNG KỸ THUẬT & BENCHMARK DỮ LIỆU
## HỌC PHẦN THỰC HÀNH THIẾT KẾ VLSI (5505382)

> **Mục đích:** Tài liệu này ghi nhận kết quả chạy script kiểm chứng số học và giải tích (`scripts/verify_lab00_lab01.py`, `scripts/verify_lab02.py`, `scripts/verify_lab03.py`, `scripts/verify_lab04.py`) cùng các thông số benchmark từ mô phỏng SPICE để bảo đảm tính chính xác tuyệt đối của bộ đáp án giảng viên.

---

### 1. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 0 (LAB 00)

Script kiểm chứng: `python scripts/verify_lab00_lab01.py`

```
============================================================
VERIFICATION: LAB 00 (SPICE & LTSPICE INTRO)
============================================================
Voltage Divider: Vin=5.0V, R1=30.0k, R2=20.0k
  Vout = 2.0000 V
  Iin  = 0.1000 mA (100.0 uA)
  Ptotal = 0.5000 mW (500.0 uW)

RC Low-Pass Filter: R=10.0k, C=10.0nF
  tau = R * C = 100.00 us (0.1000 ms)
  V(tau) = 3.1606 V (63.21%)
  V(2.2tau) = 4.4460 V (88.92%)
  V(5tau) = 4.9663 V (99.33%)
  f_-3dB = 1/(2*pi*RC) = 1591.55 Hz (1.5915 kHz)
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab00/divider_op_dc.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/divider_op_dc.sp)
- `03 - Instructor_Solutions/lab00/rc_transient_meas.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_transient_meas.sp)
- `03 - Instructor_Solutions/lab00/rc_ac_bode.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_ac_bode.sp)
- `03 - Instructor_Solutions/lab00/nmos_test_include.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/nmos_test_include.sp)

---

### 2. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 1 (LAB 01)

```
============================================================
VERIFICATION: LAB 01 (MOSFET I-V & CMOS INVERTER)
============================================================
MOSFET Parameters (C5N 0.5um):
  NMOS: W=1.2u, L=0.6u -> beta_n = 240.0 uA/V^2
  PMOS: W=3.6u, L=0.6u -> beta_p = 240.0 uA/V^2
  Sizing ratio (Wp/Wn) = 3.00
  Idsat_n (VGS=5V, VDS=5V) = 2.219 mA
  Idsat_p (|VGS|=5V, |VDS|=5V) = 2.117 mA

CMOS Inverter VTC Characteristics:
  r = sqrt(beta_p/beta_n) = 1.0000
  Switching Threshold VM = 2.4500 V
  Numerical VIL = 1.820 V
  Numerical VIH = 2.780 V
  Noise Margin Low  NML = 1.820 V
  Noise Margin High NMH = 2.220 V

Equivalent On-Resistance:
  Ron_n = 969.0 Ohm (0.969 kOhm)
  Ron_p = 992.1 Ohm (0.992 kOhm)

Delay Estimation (CL = 50 fF):
  tpHL (theoretical) = 33.43 ps
  tpLH (theoretical) = 34.23 ps
  tpd  (theoretical) = 33.83 ps
  tpd (post-layout PEX approx, CL_eff=73.5fF) = 49.73 ps (+47.0%)
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab01/nmos_iv_curve.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab01/nmos_iv_curve.sp)
- `03 - Instructor_Solutions/lab01/pmos_iv_curve.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab01/pmos_iv_curve.sp)
- `03 - Instructor_Solutions/lab01/cmos_inverter_vtc_only.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_vtc_only.sp)
- `03 - Instructor_Solutions/lab01/cmos_inverter_vtc_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_vtc_tran.sp)
- `03 - Instructor_Solutions/lab01/cmos_inverter_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab01/cmos_inverter_pex_postlayout.sp)

---

### 3. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 2 (LAB 02)

Script kiểm chứng: `python scripts/verify_lab02.py`

```
============================================================
VERIFICATION: LAB 02 (CMOS NAND2 & NOR2 GATES)
============================================================
NAND2 Sizing:
  NMOS: W = 2.4u, L = 0.6u (Req_N = 969.0 Ohm)
  PMOS: W = 3.6u, L = 0.6u (Req_P_worst = 992.1 Ohm, Req_P_best = 496.0 Ohm)
NAND2 Delay (CL = 50 fF):
  tpHL = 33.43 ps
  tpLH (worst: 1 PMOS) = 34.23 ps
  tpLH (best:  2 PMOS) = 17.11 ps
  tpd (worst) = 33.83 ps

NOR2 Sizing:
  PMOS: W = 7.2u, L = 0.6u (Req_P = 992.1 Ohm)
  NMOS: W = 1.2u, L = 0.6u (Req_N_worst = 969.0 Ohm, Req_N_best = 484.5 Ohm)
NOR2 Delay (CL = 50 fF):
  tpLH = 34.23 ps
  tpHL (worst: 1 NMOS) = 33.43 ps
  tpHL (best:  2 NMOS) = 16.72 ps
  tpd (worst) = 33.83 ps

PPA Comparison:
  Total Transistor Width: NAND2 = 12.0 um vs NOR2 = 16.8 um (+40.0%)
  Input Capacitance (Pin A): NAND2 (Wn+Wp = 6.0u) vs NOR2 (Wn+Wp = 8.4u, +40%)
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab02/nand2_dc_vtc.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab02/nand2_dc_vtc.sp)
- `03 - Instructor_Solutions/lab02/nand2_tran_meas.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab02/nand2_tran_meas.sp)
- `03 - Instructor_Solutions/lab02/nor2_tran_meas.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab02/nor2_tran_meas.sp)
- `03 - Instructor_Solutions/lab02/nand2_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab02/nand2_pex_postlayout.sp)

---

### 4. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 3 (LAB 03)

Script kiểm chứng: `python scripts/verify_lab03.py`

```
======================================================================
KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 03 - AOI21 & LOGICAL EFFORT
======================================================================

1. Inverter tham chiếu (INV_X1):
   Wn = 1.20 um (4 lambda), Wp = 3.60 um (12 lambda), L = 0.60 um

2. Kích thước tế bào AOI21_X1:
   MN_A, MN_B (PDN nối tiếp): Wn = 2.40 um (8 lambda)
   MN_C       (PDN nhánh đơn): Wn = 1.20 um (4 lambda)
   MP_A, MP_B, MP_C (PUN):    Wp = 7.20 um (24 lambda)

3. Logical Effort (g):
   g_A = Cin_A / Cin_inv = 32 / 16 = 2.000 (= 6/3 = 2.000)
   g_B = Cin_B / Cin_inv = 32 / 16 = 2.000 (= 6/3 = 2.000)
   g_C = Cin_C / Cin_inv = 28 / 16 = 1.750 (= 7/4 = 1.750)

4. Parasitic Delay (p):
   Cout_aoi = 24 + 8 + 4 = 36 lambda
   Cout_inv = 12 + 4 = 16 lambda
   p_aoi21 = 36 / 16 = 2.250 (= 2.25 tau)

5. Tối ưu hóa chuỗi đệm Inverter (Inverter Buffer Chain):
   Cin = 20.0 fF, CL = 1.0 pF -> H = CL/Cin = 50.0
   N = 1 tầng: f_hat = 50.000, Trễ D = 51.00 tau
   N = 2 tầng: f_hat = 7.071, Trễ D = 16.14 tau
   N = 3 tầng: f_hat = 3.684, Trễ D = 14.05 tau
   N = 4 tầng: f_hat = 2.659, Trễ D = 14.64 tau
   N = 5 tầng: f_hat = 2.187, Trễ D = 15.93 tau
   => Số tầng tối ưu: N = 3 (Trễ cực tiểu D = 14.05 tau)
   => Cải thiện tốc độ so với N=1 (lái trực tiếp): 3.63 lần (362.9%)

6. Định kích thước các tầng chuỗi đệm (N = 3, f_hat = 3.684):
   Tầng 1 (1.0X):  Wn = 1.20 um, Wp = 3.60 um
   Tầng 2 (3.68X): Wn = 4.42 um, Wp = 13.26 um
   Tầng 3 (13.57X): Wn = 16.29 um, Wp = 48.86 um
======================================================================
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab03/aoi21_logic_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab03/aoi21_logic_tran.sp)
- `03 - Instructor_Solutions/lab03/logical_effort_meas.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab03/logical_effort_meas.sp)
- `03 - Instructor_Solutions/lab03/buffer_chain_opt.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab03/buffer_chain_opt.sp)
- `03 - Instructor_Solutions/lab03/aoi21_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab03/aoi21_pex_postlayout.sp)

---

### 5. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 4 (LAB 04)

Script kiểm chứng: `python scripts/verify_lab04.py`

```
======================================================================
KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 04 - TRANSMISSION GATE & MUX
======================================================================

1. Khảo sát Pass Transistor truyền đơn lẻ:
   a. NMOS truyền mức '1' (Gate=5V, Drain=5V, V_SB = Vout):
      Vthn_eff (do Body Effect) = 1.369 V (tăng từ 0.70 V)
      Vout_max (Weak '1') = 3.631 V (suy giảm 1.369 V so với VDD)
   b. PMOS truyền mức '0' (Gate=0V, Drain=0V, V_BS = Vout):
      Vout_min (Weak '0') ≈ |Vthp| ≈ 0.80 V - 1.05 V
   c. Cổng truyền CMOS (TG) kết hợp NMOS // PMOS:
      Truyền mức '0' qua NMOS (Strong '0'): Vout_min = 0.000 V
      Truyền mức '1' qua PMOS (Strong '1'): Vout_max = 5.000 V
      => Đạt biên độ logic toàn dải Rail-to-Rail: 0.0V đến 5.0V

2. Điện trở dẫn tương đương của Cổng truyền (TG):
   Khi Vin gần 0V:   NMOS dẫn mạnh (Triode), R_TG ≈ 969.0 Ohm
   Khi Vin gần 5V:   PMOS dẫn mạnh (Triode), R_TG ≈ 992.0 Ohm
   Khi Vin = 2.5V:   Cả NMOS và PMOS cùng dẫn, R_TG ≈ 490.2 Ohm
   Điện trở trung bình R_TG,avg ≈ 1000 - 1200 Ohm (tương đối phẳng trên toàn dải)

3. Thời gian trễ quá độ qua Cổng truyền (CL = 50 fF):
   tpd_TG ≈ 0.69 * R_TG,avg * CL ≈ 39.67 ps

4. So sánh PPA Bộ dồn kênh MUX 2:1:
   a. TG-based MUX 2:1 (2 TG + 1 Inverter):
      Số transistor: 2 * 2T + 2T = 6 Transistors
      Số tầng trễ: 1 TG (tpd ≈ 40 - 55 ps)
   b. Static CMOS Gate MUX (2 AND + 1 OR = AOI22 + INV):
      Số transistor: 8T (AOI22) + 2T (INV) = 10 Transistors (hoặc 12T nếu dùng NAND)
      Số tầng trễ: 2 tầng cổng logic (tpd ≈ 120 - 150 ps)
   => TG MUX tiết kiệm 40% transistor, giảm diện tích ~38%, nhanh gấp ~2.5 - 3 lần
======================================================================
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab04/tg_transmission_dc_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab04/tg_transmission_dc_tran.sp)
- `03 - Instructor_Solutions/lab04/mux2_tg_logic_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab04/mux2_tg_logic_tran.sp)
- `03 - Instructor_Solutions/lab04/mux4_tg_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab04/mux4_tg_tran.sp)
- `03 - Instructor_Solutions/lab04/mux2_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab04/mux2_pex_postlayout.sp)
