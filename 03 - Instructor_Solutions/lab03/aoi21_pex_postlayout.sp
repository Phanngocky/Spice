* AOI21 POST-LAYOUT PARASITIC EXTRACTION (PEX) SIMULATION
* Trich xuat tu ky sinh tu Electric Layout: aoi21_x1{lay}
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuit aoi21_pex bao gom dien dung ky sinh cuc ma va nut noi
.subckt aoi21_pex A B C out vdd gnd
* PMOS Transistors
Mpa xp A vdd vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u
Mpb xp B vdd vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u
Mpc out C xp vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u

* NMOS Transistors
Mna out A xn 0 N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u
Mnb xn B 0 0 N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u
Mnc out C 0 0 N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* Dien dung ky sinh nut noi trich xuat (Post-layout Parasitics)
Cpar_xp xp 0 14.8fF
Cpar_xn xn 0 8.2fF
Cpar_out out 0 18.5fF
.ends aoi21_pex

* Mach do voi tai ngo ra CL = 50fF
X1 in_A in_B in_C out vdd 0 aoi21_pex
CL out 0 50fF

* Nguon kich xung do tre ngo vao A (B = 5V, C = 0V)
Va in_A 0 PULSE(0 5.0 2n 0.1n 0.1n 10n 25n)
Vb in_B 0 DC 5.0
Vc in_C 0 DC 0.0

.tran 0.01n 30n

.meas tran tphl_pex TRIG v(in_A) VAL=2.5 RISE=1 TARG v(out) VAL=2.5 FALL=1
.meas tran tplh_pex TRIG v(in_A) VAL=2.5 FALL=1 TARG v(out) VAL=2.5 RISE=1
.meas tran tpd_pex PARAM='(tphl_pex + tplh_pex)/2'

.end
