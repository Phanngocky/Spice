# BẢN ĐỐI CHIẾU KIỂM CHỨNG KỸ THUẬT & BENCHMARK DỮ LIỆU
## HỌC PHẦN THỰC HÀNH THIẾT KẾ VLSI (5505382)

> **Mục đích:** Tài liệu này ghi nhận kết quả chạy script kiểm chứng số học và giải tích (`scripts/verify_lab00_lab01.py`) cùng các thông số benchmark từ mô phỏng SPICE để bảo đảm tính chính xác tuyệt đối của bộ đáp án giảng viên.

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
