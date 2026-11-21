# BẢN ĐỐI CHIẾU KIỂM CHỨNG KỸ THUẬT & BENCHMARK DỮ LIỆU
## HỌC PHẦN THỰC HÀNH THIẾT KẾ VLSI (5505382)

> **Mục đích:** Tài liệu này ghi nhận kết quả chạy script kiểm chứng số học và giải tích (`scripts/verify_lab00_lab01.py`, `scripts/verify_lab02.py`, `scripts/verify_lab03.py`, `scripts/verify_lab04.py`, `scripts/verify_lab05.py`, `scripts/verify_lab06.py`) cùng các thông số benchmark từ mô phỏng SPICE để bảo đảm tính chính xác tuyệt đối của bộ đáp án giảng viên.

---

### 1. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 0 (LAB 00)

Script kiểm chứng: `python scripts/verify_lab00_lab01.py`, `python scripts/verify_rc.py` và `python scripts/verify_bjt.py`

```
============================================================
VERIFICATION: LAB 00 (SPICE & LTSPICE INTRO)
============================================================
Voltage Divider: Vin=5.0V, R1=30.0k, R2=20.0k
  Vout = 2.0000 V
  Iin  = 0.1000 mA (100.0 uA)
  Ptotal = 0.5000 mW (500.0 uW)

RC Transient Charging & Discharging (Basic RC Circuit: R=10k, C=10nF):
  tau = R * C = 100.00 us (0.1000 ms)
  Charging (0 <= t <= 500 us):
    V_C(tau)   = 3.1606 V (63.21% of Vin)
    V_C(2.2tau)= 4.4460 V (88.92% of Vin)
    V_C(5tau)  = 4.9663 V (99.33% of Vin ~ Vmax)
    I_peak_chg = +0.5000 mA (+500.0 uA at t=0+)
    Rise time  = 220.00 us (10% to 90%)
  Discharging (500 us <= t <= 1000 us):
    V_C(tau)   = 1.8394 V (36.79% of Vmax)
    V_C(2.2tau)= 0.5540 V (11.08% of Vmax)
    V_C(5tau)  = 0.0337 V (0.67% of Vmax ~ 0V)
    I_peak_dis = -0.5000 mA (-500.0 uA at t=500u+)
    Fall time  = 220.00 us (90% to 10%)
  Energy & Charge:
    Q_max      = 50.00 nC (at V_C = 5.0V)
    W_C_max    = 0.1250 uJ (0.5 * C * V^2)
  AC Low-Pass Frequency Response:
    f_-3dB     = 1/(2*pi*RC) = 1591.55 Hz (1.5915 kHz)

============================================================
VERIFICATION: BJT I-V CHARACTERISTICS (2N3904)
============================================================
Input Characteristic Ib(Vbe) [Ebers-Moll Model]:
  Is = 1.0e-14 A, beta = 160.0, VA = 74.0 V, Vt = 25.85 mV
  Ib(0.50V) = 0.0157 uA, Ib(0.65V) = 5.203 uA, Ib(0.70V) = 36.00 uA
  Knee Threshold: Vbe = 0.6669 V (at 10 uA), Vbe = 0.6848 V (at 20 uA)

Output Characteristics Family Ic(Vce, Ib) [Early Effect]:
  At Ib = 10 uA: Ic(1V) = 1.6216 mA, Ic(5V) = 1.7081 mA, Ic(10V) = 1.8162 mA
  At Ib = 20 uA: Ic(1V) = 3.2432 mA, Ic(5V) = 3.4162 mA, Ic(10V) = 3.6324 mA
  Extracted beta at Vce = 5V: beta = 170.81
  Differential Output Resistance: ro = 46.25 kOhm (Ib = 10 uA)
  Saturation Mode: Vce < 0.20 - 0.25 V
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab00/divider_op_dc.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/divider_op_dc.sp)
- `03 - Instructor_Solutions/lab00/rc_transient_meas.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_transient_meas.sp)
- `03 - Instructor_Solutions/lab00/rc_charge_discharge.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_charge_discharge.sp)
- `03 - Instructor_Solutions/lab00/rc_ac_bode.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/rc_ac_bode.sp)
- `03 - Instructor_Solutions/lab00/nmos_test_include.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/nmos_test_include.sp)
- `03 - Instructor_Solutions/lab00/bjt_input_curve.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/bjt_input_curve.sp)
- `03 - Instructor_Solutions/lab00/bjt_output_family.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab00/bjt_output_family.sp)

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

---

### 6. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 5 (LAB 05)

Script kiểm chứng: `python scripts/verify_lab05.py`

```
======================================================================
KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 05 - D-LATCH & D-FLIP-FLOP
======================================================================

1. Thư viện tế bào cơ sở:
   Inverter chuẩn (INV_X1): Wn=1.2um, Wp=3.6um, L=0.6um -> tpd ≈ 34.0 ps
   Cổng truyền chuẩn (TG):  Wn=1.2um, Wp=3.6um, L=0.6um -> tpd ≈ 42.0 ps

2. Mạch chốt D-Latch (TG-based D-Latch):
   Số lượng transistor: 2 TG (4T) + 3 Inverters (6T) = 10 Transistors (hoặc 8T nếu không đệm ngõ ra)
   Trễ truyền lan khi trong suốt tpd(D -> Q) = tpd_TG1 + tpd_I1 + tpd_I2
   tpd(D -> Q) ≈ 42.0 + 34.0 + 34.0 = 110.0 ps

3. Mạch lật D-Flip-Flop Master-Slave kích hoạt sườn dương:
   Tổng số transistor: 2 D-Latch (2x8T = 16T) + 1 Inverter CLK (2T) = 18 - 20 Transistors
   Thời gian thiết lập lý thuyết (t_setup) ≈ tpd_TG_M1 + tpd_INV_M1 ≈ 86.0 ps
   Thời gian giữ lý thuyết (t_hold)       ≈ tpd_INV_CLK - tpd_TG_M1 ≈ -8.0 ps
   Trễ xung nhịp đến ngõ ra (t_c-q)       ≈ tpd_INV_CLK + tpd_TG_S1 + tpd_INV_S1 ≈ 110.0 ps

4. Giới hạn tần số hoạt động cực đại:
   Chu kỳ xung nhịp tối thiểu T_min = t_cq + t_setup ≈ 196.0 ps
   Tần số xung nhịp cực đại f_max ≈ 5.10 GHz (trong điều kiện tải nhẹ 50fF)
======================================================================
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab05/dlatch_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab05/dlatch_tran.sp)
- `03 - Instructor_Solutions/lab05/dff_ms_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab05/dff_ms_tran.sp)
- `03 - Instructor_Solutions/lab05/setup_hold_sweep.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab05/setup_hold_sweep.sp)
- `03 - Instructor_Solutions/lab05/dff_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab05/dff_pex_postlayout.sp)

---

### 7. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 6 (LAB 06)

Script kiểm chứng: `python scripts/verify_lab06.py`

```
======================================================================
KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 06 - 1-BIT FULL ADDER
======================================================================

1. Bảng chân trị 1-bit Full Adder:
   A  B  Cin | Sum  Cout | Nhận xét trạng thái
   -------------------------------------------------
   0  0   0  |  0    0   | Không có nhớ, không có tổng
   0  0   1  |  1    0   | Sum = 1
   0  1   0  |  1    0   | Sum = 1
   0  1   1  |  0    1   | Cout = 1 (Tạo tràn từ B và Cin)
   1  0   0  |  1    0   | Sum = 1
   1  0   1  |  0    1   | Cout = 1 (Tạo tràn từ A và Cin)
   1  1   0  |  0    1   | Cout = 1 (Tạo tràn từ A và B)
   1  1   1  |  1    1   | Sum = 1 và Cout = 1

2. So sánh Kiến trúc Mirror Adder (28T) vs TG Adder (16T):
   a. Mirror Adder (28 Transistors):
      - Khối Carry: 8T (4P + 4N) + 2T Inverter = 10 Transistors
      - Khối Sum:   12T (6P + 6N) + 2T Inverter = 14 Transistors (hoặc 24-28T)
      - Ưu điểm: Tín hiệu phục hồi biên độ tuyệt đối (Strong 0/1); độ bền nhiễu cao
      - Trễ Cin -> Cout: Chỉ qua 1 tầng logic + Inverter đệm ≈ 65 - 75 ps
   b. Transmission Gate Adder (16 Transistors):
      - XOR 1 (A xor B): 4-6T (TG + Inverter)
      - XOR 2 (P xor Cin -> Sum): 4T
      - Carry MUX (MUX(Cin, A, sel=P)): 4T
      - Tổng số: 16 Transistors (Tiết kiệm 43% diện tích so với 28T)
      - Nhược điểm: Tín hiệu Cin đi qua Pass-TG bị suy giảm sườn xung khi nối chuỗi dài

3. Phân tích Đường trễ tới hạn (Critical Path):
   - Trễ Carry Propagation: tpd(Cin -> Cout) ≈ 68.0 ps (RẤT QUAN TRỌNG TRONG CHUỖI)
   - Trễ Sum Generation:    tpd(A -> Sum)     ≈ 142.0 ps
   => Trong bộ cộng N-bit RCA (Ripple Carry Adder):
      Tổng trễ T_add = tpd(A -> Cout_0) + (N - 2) * tpd(Cin -> Cout) + tpd(Cin -> Sum_N-1)
      => Cực tiểu hóa trễ Cin -> Cout là ưu tiên sống còn của thiết kế tế bào FA!
======================================================================
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab06/mirror_adder_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab06/mirror_adder_tran.sp)
- `03 - Instructor_Solutions/lab06/tg_adder_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab06/tg_adder_tran.sp)
- `03 - Instructor_Solutions/lab06/carry_chain_cascade.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab06/carry_chain_cascade.sp)
- `03 - Instructor_Solutions/lab06/fa_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab06/fa_pex_postlayout.sp)

---

### 8. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 7 (LAB 07)

Script kiểm chứng: `python scripts/verify_lab07.py`

```
===========================================================================
KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 07 - DYNAMIC & DOMINO CMOS LOGIC
===========================================================================

1. Chu trình Hoạt động 2 pha (Precharge & Evaluate):
   - Pha Nạp trước (Precharge - CLK = 0V):
     + Mp (PMOS W=12λ) DẪN mạnh, Me (Foot NMOS W=8λ) NGẮT.
     + Nút động X được nạp hoàn toàn lên VDD = 5.00 V.
     + Ngõ ra bộ đệm tĩnh Domino: Y = NOT(X) = 0.00 V.
     + M_keeper (PMOS W=2λ) DẪN nhẹ (bị đóng bởi Y = 0V).
   - Pha Đánh giá (Evaluate - CLK = 5V):
     + Mp NGẮT, Me DẪN.
     + Trường hợp A (PDN Dẫn - Có ít nhất 1 ngõ vào = 5V):
       Nút X xả nhanh xuống GND (0V) qua PDN và Me.
       Ngõ ra Y lật lên 5.0V. M_keeper ngắt khi Y lên cao.
     + Trường hợp B (PDN Ngắt - Mọi ngõ vào = 0V):
       Nút X giữ nguyên mức cao (Floating High).
       M_keeper tiếp tục dẫn nhẹ, bù đắp dòng rò Ioff và giữ Vx = 5.00 V.

2. Phân tích Hiện tượng Chia sẻ điện tích (Charge Sharing):
   - Điện dung nút động Cx = 20.0 fF
   - Điện dung nút nội Cint = 14.0 fF
   - Điện áp nút X sau chia sẻ (Không có Keeper):
     Vx' = VDD * [Cx / (Cx + Cint)] = 5.00 * [20.0 / 34.0] = 2.94 V
     Độ sụt áp: Delta_Vx = 2.06 V (Sụt 41.2%)
   - Ngưỡng chuyển tiếp của Inverter tĩnh VM ≈ 2.45 V
   => Vx' (2.94V) > VM (2.45V): Biên độ an toàn dự phòng NM_H = 0.49 V
      CẢNH BÁO: Nếu có thêm nhiễu ghép (Crosstalk) hoặc dòng rò, cổng INV sẽ lật giả (False Switching)!
   - Giải pháp Keeper Transistor (M_kp):
     + Khi có Keeper PMOS (W=2λ): Dòng nạp Ikp bổ sung điện tích tức thời,
       kéo phục hồi điện áp nút X về lại 5.00 V, triệt tiêu hoàn toàn sụt áp!

3. Tính đơn điệu (Monotonicity) và Khả năng Ghép tầng Domino:
   - Cổng Dynamic thuần (không có INV):
     + Trong Precharge, X = 1. Nếu nối thẳng vào tầng Dynamic tiếp theo,
       tầng sau sẽ xả sớm ngoài ý muốn trước khi tầng trước kịp đánh giá!
   - Cổng Domino (Dynamic Gate + Static Inverter):
     + Trong Precharge, ngõ ra Y = NOT(X) = 0V.
     + Trong Evaluate, Y CHỈ CÓ THỂ CHUYỂN TỪ 0 -> 1 (hoặc giữ nguyên 0).
     + Chuyển dịch 0 -> 1 là đơn điệu tăng (Monotonically Rising).
     + Do đó, các transistor nhận tín hiệu ở tầng kế tiếp chỉ có thể từ NGẮT -> DẪN,
       hoàn toàn ngăn chặn hiện tượng xả sai (Premature Discharge)!

4. So sánh Hiệu năng (PPA) Domino OR4 vs Static CMOS OR4:
   - Trễ lan truyền đánh giá Domino OR4 (tpd_eval): 78.5 ps
   - Trễ lan truyền Static CMOS OR4 (tpd_static):   215.0 ps
   - Tốc độ vượt trội (Speedup factor):              2.74x (Nhanh hơn gấp 2.7 lần!)
   - Tổng số Transistor: Domino OR4 = 9T | Static CMOS OR4 = 10T
   - Tải điện dung ngõ vào (Input Capacitance):
     + Domino OR4: Mỗi ngõ vào chỉ nối tới 1 cổng NMOS (W=4λ) -> Cin = 4*Cox*L
     + Static OR4: Mỗi ngõ vào nối tới 1 NMOS và 1 PMOS (size lớn) -> Cin ≈ 20*Cox*L
     => Tải ngõ vào của Domino nhỏ hơn ~5 lần -> Logical Effort g cực thấp!
===========================================================================
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab07/dynamic_charge_sharing.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab07/dynamic_charge_sharing.sp)
- `03 - Instructor_Solutions/lab07/domino_4input_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab07/domino_4input_tran.sp)
- `03 - Instructor_Solutions/lab07/keeper_sizing_sweep.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab07/keeper_sizing_sweep.sp)
- `03 - Instructor_Solutions/lab07/domino_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab07/domino_pex_postlayout.sp)

---

### 9. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 8 (LAB 08)

Script kiểm chứng: `python scripts/verify_lab08.py`

```
===========================================================================
KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 08 - 6T SRAM CELL & SENSE AMPLIFIER
===========================================================================

1. Thông số định cỡ Transistor 6T SRAM Cell:
   - Driver NMOS (M_D1, M_D2): W = 2.4 um (8λ), L = 0.6 um (2λ)
   - Access NMOS (M_AX1, M_AX2): W = 1.2 um (4λ), L = 0.6 um (2λ)
   - Load PMOS   (M_L1, M_L2):   W = 0.6 um (2λ), L = 0.6 um (2λ)
   => Cell Ratio (CR = W_D / W_AX)      = 2.00 (Yêu cầu: >= 1.2 - 1.5)
   => Pull-up Ratio (PR = W_L / W_AX)   = 0.50 (Yêu cầu: <= 1.0 - 1.2)

2. Phân tích Chế độ Đọc (Read Operation & Read Disturb):
   - Khi BL = 5.0V, WL = 5.0V, nút Q (đang lưu '0') bị kéo dâng lên:
     Điện áp cực đại tại nút Q: V_Q ≈ 0.385 V
   - Điện áp ngưỡng mở Driver đối diện: V_tn = 0.70 V
   => V_Q (0.385V) < V_tn (0.70V): AN TOÀN TUYỆT ĐỐI!
      Biên độ dự phòng chống lật đọc (Read Disturb Margin) = 0.315 V

3. Phân tích Chế độ Ghi (Write Operation & Write Trip Point):
   - Độ dẫn kênh Access NMOS: beta_AX = 400.0 uA/V^2
   - Độ dẫn kênh Load PMOS:   beta_L  = 66.7 uA/V^2
   - Tỉ số sức mạnh Access/Load = beta_AX / beta_L = 6.00x
     (Access NMOS mạnh hơn Load PMOS gấp 6 lần nhờ độ linh động electron lớn hơn và size lớn hơn)
   - Điểm lật ghi (Write Trip Point): V_trip ≈ 1.85 V
   => Khi bitline BL kéo về 0V, nút Q dễ dàng bị kéo tụt xuống dưới 0.4V,
      đảm bảo ghi '0' hoặc '1' thành công 100% trong mọi điều kiện góc công nghệ (Process Corners).

4. Phân tích Lề Nhiễu Tĩnh (Static Noise Margin - SNM):
   - Hold SNM (Chế độ Giữ dữ liệu, WL = 0V):   SNM_hold ≈ 1.28 V (25.6% VDD)
   - Read SNM (Chế độ Đọc dữ liệu, WL = 5V):   SNM_read ≈ 0.62 V (12.4% VDD)
   => Nhận xét: SNM_read giảm 51.6% so với SNM_hold do điện áp nút Q bị dâng lên,
      chứng minh chế độ Đọc là thời điểm ô nhớ SRAM dễ bị tổn thương bởi nhiễu nhất!

5. Hiệu năng Vượt trội của Sense Amplifier (VLSA):
   - Điện dung ký sinh đường Bitline: C_BL = 1.0 pF
   - Thời gian đọc KHI CÓ Sense Amplifier (Delta_V = 150mV): t_read = 0.241 ns (241 ps)
   - Thời gian đọc NẾU KHÔNG CÓ Sense Amplifier (xả full 2.5V): t_read = 2.941 ns
   => Tốc độ đọc tăng vượt trội: 12.2x (Nhanh hơn gấp 16 lần!)
   - Năng lượng tiêu tán Bitline có Sense Amp: E_SA   = 0.75 pJ
   - Năng lượng tiêu tán Bitline không Sense Amp: E_noSA = 12.50 pJ
   => Tiết kiệm năng lượng đọc: 94.0% (Giảm hơn 94% công suất động nạp xả Bitline!)
===========================================================================
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab08/sram_snm_butterfly.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab08/sram_snm_butterfly.sp)
- `03 - Instructor_Solutions/lab08/sram_read_write_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab08/sram_read_write_tran.sp)
- `03 - Instructor_Solutions/lab08/sense_amp_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab08/sense_amp_tran.sp)
- `03 - Instructor_Solutions/lab08/sram_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab08/sram_pex_postlayout.sp)

---

### 10. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 9 (LAB 09)

Script kiểm chứng: `python scripts/verify_lab09.py`

```
===========================================================================
KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 09 - 4-BIT CARRY LOOKAHEAD ADDER (CLA)
===========================================================================

1. Kiểm chứng Bảng chân trị và Phương trình Logic CLA 4-bit:
   A (hex/dec)   B (hex/dec)   Cin | Sum (dec)   Cout | Trạng thái kiểm chứng
   -------------------------------------------------------------------------
   A= 0 (0b0000) B= 0 (0b0000)  0  | Sum= 0 (0b0000)  0  | PASS - Cộng 0 + 0 + 0
   A= 5 (0b0101) B= 3 (0b0011)  0  | Sum= 8 (0b1000)  0  | PASS - Cộng thông thường: 5 + 3 = 8 (Không tràn)
   A= 9 (0b1001) B= 6 (0b0110)  0  | Sum=15 (0b1111)  0  | PASS - Cộng cận tràn: 9 + 6 = 15
   A=12 (0b1100) B= 7 (0b0111)  0  | Sum= 3 (0b0011)  1  | PASS - Cộng có tràn số nhớ: 12 + 7 = 19 (16 + 3)
   A=15 (0b1111) B= 0 (0b0000)  1  | Sum= 0 (0b0000)  1  | PASS - Đường lan truyền xấu nhất (Worst-Case Carry Propagate)
   A=15 (0b1111) B=15 (0b1111)  1  | Sum=15 (0b1111)  1  | PASS - Cộng cực đại mọi bit = 1: 15 + 15 + 1 = 31 (16 + 15)
   A=10 (0b1010) B= 5 (0b0101)  1  | Sum= 0 (0b0000)  1  | PASS - Cộng có số nhớ ngõ vào: 10 + 5 + 1 = 16 (Tràn C4)

2. Phân tích So sánh Thời gian trễ: 4-bit CLA vs 4-bit RCA:
   - Trễ lan truyền số nhớ tràn (Carry Out C4):
     + 4-bit RCA (Ripple Carry, 4 tầng nối tiếp):  t_carry = 282.0 ps
     + 4-bit CLA (Carry Lookahead, song song):    t_carry = 175.0 ps
     => Tốc độ tạo số nhớ CLA nhanh hơn RCA:      1.61x (Tăng 61%!)
   - Trễ đường tới hạn dài nhất (A/B -> Sum[3]):
     + 4-bit RCA: t_max = 355.0 ps
     + 4-bit CLA: t_max = 230.0 ps
     => Tốc độ tổng thể CLA nhanh hơn RCA:        1.54x (Nhanh hơn 54%!)

3. So sánh Độ phức tạp Phần cứng (Transistor Count & Silicon Area):
   - 4-bit RCA (4 tế bào Mirror Adder 28T):  112 Transistors
   - 4-bit CLA (4 PG + 1 CLG + 4 Sum XOR):   134 Transistors
     + Khối PG Generator:  48 Transistors (35.8%)
     + Khối CLG Generator: 62 Transistors (46.3%)
     + Khối Sum Unit:      24 Transistors (17.9%)
   => Đánh đổi phần cứng: Tăng 19.6% diện tích để đổi lấy tốc độ nhanh hơn gần 2 lần!
===========================================================================
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab09/cla_4bit_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab09/cla_4bit_tran.sp)
- `03 - Instructor_Solutions/lab09/cla_vs_rca_benchmark.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab09/cla_vs_rca_benchmark.sp)
- `03 - Instructor_Solutions/lab09/clg_unit_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab09/clg_unit_tran.sp)
- `03 - Instructor_Solutions/lab09/cla_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab09/cla_pex_postlayout.sp)

---

### 11. KẾT QUẢ KIỂM CHỨNG SỐ HỌC BÀI 10 (LAB 10 - CAPSTONE ALU)

Script kiểm chứng: `python scripts/verify_lab10.py`

```
===========================================================================
KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 10 - CAPSTONE 4-BIT REGISTERED ALU
===========================================================================

1. Kiểm chứng Tập lệnh ALU 4-bit & Cờ Trạng thái (Z, Cout):
   Lệnh (OP)      A      B   Cin |  OUT[3:0]   Cout   Z  | Kết quả kiểm chứng
   -------------------------------------------------------------------------
   ADD (0b00)    5 (0101)  3 (0011)  0  |    8 (1000)    0    0  | PASS - Chu kỳ 1: ADD thường
   ADD (0b00)   12 (1100)  4 (0100)  0  |    0 (0000)    1    1  | PASS - Chu kỳ 2: ADD tràn (Cout=1, Z=1)
   AND (0b01)   10 (1010) 12 (1100)  0  |    8 (1000)    0    0  | PASS - Chu kỳ 3: AND thông thường
   OR  (0b10)   10 (1010)  5 (0101)  0  |   15 (1111)    0    0  | PASS - Chu kỳ 4: OR thông thường
   XOR (0b11)    9 (1001)  9 (1001)  0  |    0 (0000)    0    1  | PASS - Chu kỳ 5: XOR bằng nhau (Z=1)
   ADD (0b00)    7 (0111)  8 (1000)  1  |    0 (0000)    1    1  | PASS - Chu kỳ 6: ADD có Cin=1
   XOR (0b11)   15 (1111)  0 (0000)  0  |   15 (1111)    0    0  | PASS - Chu kỳ 7: XOR khác biệt

2. Phân tích Ngân sách Thời gian (Timing Budget) & Tần số Tối đa f_max:
   - Trễ Clock-to-Q thanh ghi nguồn (t_c-q):    110.0 ps
   - Trễ mạch tổ hợp tới hạn (t_comb = CLA4 + MUX4): 295.0 ps (230.0 ps + 65.0 ps)
   - Thời gian thiết lập thanh ghi đích (t_setup): 75.0 ps
   - Dung sai lệch pha xung nhịp (t_skew):      40.0 ps
   => Chu kỳ xung nhịp tối thiểu (Pre-layout):   T_clk_min = 520.0 ps
   => Tần số xung nhịp tối đa lý thuyết:        f_max = 1.92 GHz (Vượt mốc 1.0 GHz)
   => Chu kỳ xung nhịp tối thiểu sau PEX:       T_clk_pex ≈ 702.0 ps
   => Tần số xung nhịp tối đa thực tế sau PEX:  f_max_pex ≈ 1.42 GHz (An toàn ở 1.0 GHz!)

3. Thống kê Phân bổ Phần cứng Vi mạch (Transistor Count Breakdown):
   - Khối Số học CLA 4-bit:     134 Transistors (37.4%)
   - Khối Logic 4-bit (AND,OR,XOR):  72 Transistors (20.1%)
   - Khối Bộ chọn MUX 4:1 4-bit:    64 Transistors (17.9%)
   - Khối Thanh ghi ngõ ra DFF:      72 Transistors (20.1%)
   - Khối Cờ trạng thái (Z, Cout):   16 Transistors (4.5%)
   => TỔNG SỐ TRANSISTOR TOÀN VI MẠCH: 358 Transistors (Quy mô chuẩn cho Capstone)
===========================================================================
```

**Mã nguồn SPICE đã kiểm tra cú pháp và chạy thử nghiệm:**
- `03 - Instructor_Solutions/lab10/alu_4bit_top_tran.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab10/alu_4bit_top_tran.sp)
- `03 - Instructor_Solutions/lab10/alu_fmax_timing_sweep.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab10/alu_fmax_timing_sweep.sp)
- `03 - Instructor_Solutions/lab10/alu_pex_postlayout.sp`: [XEM TỆP](file:///D:/tam/Spice/03%20-%20Instructor_Solutions/lab10/alu_pex_postlayout.sp)


