* MUX2_TG POST-LAYOUT PARASITIC EXTRACTION (PEX) SIMULATION
* Trich xuat tu Electric Layout: mux2_tg{lay}
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuit MUX2 Post-Layout kem tu ky sinh
.subckt mux2_tg_pex d0 d1 s y vdd gnd
* Inverter tao s_n
Mp_inv s_n s vdd vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_inv s_n s gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* TG0 (d0 -> y)
Mn_tg0 d0 s_n y gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u
Mp_tg0 d0 s   y vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u

* TG1 (d1 -> y)
Mn_tg1 d1 s   y gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u
Mp_tg1 d1 s_n y vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u

* Dien dung ky sinh nut noi trich xuat tu Mask Layout (PEX)
Cpar_sn s_n 0 11.5fF
Cpar_y  y   0 21.8fF
Cpar_d0 d0  0 8.2fF
Cpar_d1 d1  0 8.2fF
.ends mux2_tg_pex

* Goi Instance
X_pex d0 d1 s y vdd 0 mux2_tg_pex
CL y 0 50fF

* Nguon tin hieu do tre d0 -> y
Vd0 d0 0 PULSE(0 5.0 2n 0.1n 0.1n 10n 25n)
Vd1 d1 0 DC 0.0
Vs  s  0 DC 0.0

.tran 0.01n 30n

.meas tran tphl_pex TRIG v(d0) VAL=2.5 FALL=1 TARG v(y) VAL=2.5 FALL=1
.meas tran tplh_pex TRIG v(d0) VAL=2.5 RISE=1 TARG v(y) VAL=2.5 RISE=1
.meas tran tpd_pex PARAM='(tphl_pex + tplh_pex)/2'

.end
