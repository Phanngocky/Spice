* AOI21 LOGIC VERIFICATION & PROPAGATION DELAY (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Ham logic: Y = !((A * B) + C)

.include "../../04 - Models_and_Libraries/C5_models.txt"

* Nguon cap
Vdd vdd 0 DC 5.0

* Subcircuit AOI21_X1
.subckt aoi21_x1 A B C out vdd gnd
* PMOS PUN: (MP_A // MP_B) in series with MP_C
* MP_A: W=7.2u (24 lambda), L=0.6u (2 lambda)
Mpa xp A vdd vdd P W=7.2u L=0.6u
* MP_B: W=7.2u (24 lambda), L=0.6u (2 lambda)
Mpb xp B vdd vdd P W=7.2u L=0.6u
* MP_C: W=7.2u (24 lambda), L=0.6u (2 lambda)
Mpc out C xp vdd P W=7.2u L=0.6u

* NMOS PDN: (MN_A series MN_B) parallel with MN_C
* MN_A: W=2.4u (8 lambda), L=0.6u (2 lambda)
Mna out A xn 0 N W=2.4u L=0.6u
* MN_B: W=2.4u (8 lambda), L=0.6u (2 lambda)
Mnb xn B 0 0 N W=2.4u L=0.6u
* MN_C: W=1.2u (4 lambda), L=0.6u (2 lambda)
Mnc out C 0 0 N W=1.2u L=0.6u
.ends aoi21_x1

* Goi Instance AOI21
X1 in_A in_B in_C out vdd 0 aoi21_x1
CL out 0 50fF

* Nguon xung kiem chung logic 8 trang thai (000 den 111)
* T_A = 40ns, T_B = 20ns, T_C = 10ns
Va in_A 0 PULSE(0 5.0 0 0.1n 0.1n 20n 40n)
Vb in_B 0 PULSE(0 5.0 0 0.1n 0.1n 10n 20n)
Vc in_C 0 PULSE(0 5.0 0 0.1n 0.1n 5n 10n)

* Mo phong Transient 80ns
.tran 0.05n 80n

* Lenh do tre khi kich ngo vao C (A=0, B=0 tai thoi diem t=5ns)
.meas tran tphl_C TRIG v(in_C) VAL=2.5 RISE=1 TARG v(out) VAL=2.5 FALL=1
.meas tran tplh_C TRIG v(in_C) VAL=2.5 FALL=1 TARG v(out) VAL=2.5 RISE=1
.meas tran tpd_C PARAM='(tphl_C + tplh_C)/2'

.control
run
plot v(in_A)+15 v(in_B)+10 v(in_C)+5 v(out)
.endc

.end
