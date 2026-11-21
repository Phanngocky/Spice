* BJT BIAS OP - Mach Phan Cuc Phan Ap BJT 2N3904 (Voltage Divider Bias)
* Mon hoc: Thuc hanh Thiet ke VLSI (5505382) - DH Su pham Ky thuat Da Nang
* Tac gia: Phan Ngoc Ky (2026)

.title Voltage Divider Bias Circuit for 2N3904 NPN BJT

* --- NGUON CUNG CAP ---
Vcc 1 0 DC 12.0

* --- PHAN AP CUC BASE ---
R1 1 2 33k
R2 2 0 10k

* --- MACH THU VA PHAT (COLLECTOR - EMITTER) ---
RC 1 3 2.2k
RE 4 0 1.0k

* --- BJT NPN TRANSISTOR ---
* Cu phap BJT: Q<name> <Collector> <Base> <Emitter> [Substrate] <model_name>
Q1 3 2 4 Q2N3904

* --- MODEL 2N3904 CHUAN STANDARD SPICE ---
.model Q2N3904 NPN(Is=1e-14 Bf=160 Vaf=74 Ikf=0.1 Xtb=1.5 Br=1.0 Nc=2
+ Isc=0 Ikr=0 Rc=1 Cjc=4p Mjc=0.333 Vjc=0.75 Fc=0.5 Cje=8p Mje=0.333
+ Vje=0.75 Tr=30.3n Tf=400p Itf=0.6 Vtf=1.7 Xtf=3 Rb=10)

* --- PHAN TICH DC OPERATING POINT ---
.op

* --- TINH TOAN THONG SO THEO GIAI TICH ---
* V_TH = Vcc * R2 / (R1 + R2) = 12 * 10 / 43 = 2.791 V
* R_TH = R1 // R2 = 33k * 10k / 43k = 7.674 kOhm
* I_B = (V_TH - V_BE) / (R_TH + (beta + 1)*RE) approx 12.5 uA
* I_C = beta * I_B approx 2.00 mA
* V_C = Vcc - I_C * RC approx 7.60 V
* V_E = I_E * RE approx 2.02 V
* V_CE = V_C - V_E approx 5.58 V

.meas op v_base FIND V(2)
.meas op v_coll FIND V(3)
.meas op v_emit FIND V(4)
.meas op v_ce   PARAM V(3)-V(4)
.meas op v_be   PARAM V(2)-V(4)
.meas op i_coll PARAM -I(RC)
.meas op i_base PARAM (V(1)-V(2))/33k - V(2)/10k

.end
