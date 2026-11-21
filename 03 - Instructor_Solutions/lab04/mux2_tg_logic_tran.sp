* TG-BASED 2:1 MULTIPLEXER (MUX2_TG) VERIFICATION (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Kien truc: 2 Transmission Gates + 1 Inverter = 6 Transistors

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuit tg_gate: in out en en_n vdd gnd
.subckt tg_gate in out en en_n vdd gnd
Mn in en out gnd N W=1.2u L=0.6u
Mp in en_n out vdd P W=3.6u L=0.6u
.ends tg_gate

* Subcircuit inv_x1: in out vdd gnd
.subckt inv_x1 in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_x1

* Subcircuit mux2_tg: d0 d1 s y vdd gnd
.subckt mux2_tg d0 d1 s y vdd gnd
* Inverter tao tin hieu dao s_n
X_inv s s_n vdd gnd inv_x1
* TG0 truyen d0 khi s=0 (en=s_n, en_n=s)
X_tg0 d0 y s_n s vdd gnd tg_gate
* TG1 truyen d1 khi s=1 (en=s, en_n=s_n)
X_tg1 d1 y s s_n vdd gnd tg_gate
.ends mux2_tg

* Goi Instance MUX2_TG
X_mux d0 d1 s y vdd 0 mux2_tg
CL y 0 50fF

* Nguon kich thich:
* d0: Xung 25MHz (T = 40ns, ton = 20ns)
Vd0 d0 0 PULSE(0 5.0 0 0.1n 0.1n 20n 40n)
* d1: Xung 50MHz (T = 20ns, ton = 10ns)
Vd1 d1 0 PULSE(0 5.0 0 0.1n 0.1n 10n 20n)
* s: Xung chon kenh 12.5MHz (T = 80ns: 40ns dau s=0 -> chon d0; 40ns sau s=1 -> chon d1)
Vs s 0 PULSE(0 5.0 0 0.1n 0.1n 40n 80n)

* Mo phong Transient 160ns (2 chu ky chon)
.tran 0.05n 160n

* DO TRE D0 -> Y (khi s = 0, do tai thoi diem t = 20ns)
.meas tran tphl_d0 TRIG v(d0) VAL=2.5 FALL=1 TARG v(y) VAL=2.5 FALL=1
.meas tran tplh_d0 TRIG v(d0) VAL=2.5 RISE=1 TARG v(y) VAL=2.5 RISE=1
.meas tran tpd_d0 PARAM='(tphl_d0 + tplh_d0)/2'

* DO TRE D1 -> Y (khi s = 1, do tai thoi diem t = 60ns)
.meas tran tphl_d1 TRIG v(d1) VAL=2.5 FALL=2 TARG v(y) VAL=2.5 FALL=3
.meas tran tplh_d1 TRIG v(d1) VAL=2.5 RISE=2 TARG v(y) VAL=2.5 RISE=3
.meas tran tpd_d1 PARAM='(tphl_d1 + tplh_d1)/2'

* DO TRE SELECT S -> Y (thoi diem s chuyen tu 0 -> 1 tai t = 40ns)
.meas tran tpd_s_to_y TRIG v(s) VAL=2.5 RISE=1 TARG v(y) VAL=2.5 CROSS=1

.control
run
plot v(d0)+10 v(d1)+5 v(s)-5 v(y)
.endc

.end
