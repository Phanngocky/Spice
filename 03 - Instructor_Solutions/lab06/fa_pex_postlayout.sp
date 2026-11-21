* MIRROR ADDER POST-LAYOUT PARASITIC EXTRACTION (PEX) SIMULATION
* Trich xuat tu Electric Mask Layout: mirror_adder_1b{lay}
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuit Mirror Adder Post-Layout kem tu ky sinh
.subckt mirror_adder_pex a b cin sum cout vdd gnd
* Khối Carry Transistors
Mn_ca1 cout_b a n_ca1 gnd N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u
Mn_cb1 n_ca1  b gnd   gnd N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u
Mn_ccin cout_b cin n_ca2 gnd N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u
Mn_ca2  n_ca2  a   gnd   gnd N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u
Mn_cb2  n_ca2  b   gnd   gnd N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u

Mp_ca1 p_ca1 a vdd vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u
Mp_cb1 p_ca1 b vdd vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u
Mp_ccin cout_b cin p_ca1 vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u
Mp_ca2 p_ca2 a vdd   vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u
Mp_cb2 cout_b b p_ca2 vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u

* Inverter Cout
Mp_cout cout cout_b vdd vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_cout cout cout_b gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* Khối Sum Transistors
Mn_sa1 sum_b a n_sa1 gnd N W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_sb1 n_sa1 b n_sa2 gnd N W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_sc1 n_sa2 cin gnd gnd N W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_scout sum_b cout_b n_sa3 gnd N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u
Mn_sa2   n_sa3 a      gnd   gnd N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u
Mn_sb2   n_sa3 b      gnd   gnd N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u
Mn_sc2   n_sa3 cin    gnd   gnd N W=2.4u L=0.6u AS=5.18p PS=9.12u AD=5.18p PD=9.12u

Mp_sa1 p_sa1 a vdd vdd P W=10.8u L=0.6u AS=23.3p PS=26.0u AD=23.3p PD=26.0u
Mp_sb1 p_sa2 b p_sa1 vdd P W=10.8u L=0.6u AS=23.3p PS=26.0u AD=23.3p PD=26.0u
Mp_sc1 sum_b cin p_sa2 vdd P W=10.8u L=0.6u AS=23.3p PS=26.0u AD=23.3p PD=26.0u
Mp_sa2 p_sa3 a vdd vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u
Mp_sb2 p_sa3 b vdd vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u
Mp_sc2 p_sa3 cin vdd vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u
Mp_scout sum_b cout_b p_sa3 vdd P W=7.2u L=0.6u AS=15.55p PS=18.72u AD=15.55p PD=18.72u

* Inverter Sum
Mp_sum sum sum_b vdd vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_sum sum sum_b gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* Dien dung ky sinh nut noi PEX
Cpar_cb cout_b 0 24.5fF
Cpar_sb sum_b  0 28.6fF
Cpar_co cout   0 16.2fF
Cpar_so sum    0 16.2fF
.ends mirror_adder_pex

* Goi Instance
X_pex a b cin sum cout vdd 0 mirror_adder_pex
CL_sum sum 0 50fF
CL_cout cout 0 50fF

* Nguon kich thich do tre Cin -> Cout
Va a 0 DC 0.0
Vb b 0 DC 5.0
Vcin cin 0 PULSE(0 5.0 2n 0.1n 0.1n 10n 25n)

.tran 0.02n 30n

.meas tran t_cin_cout_pex TRIG v(cin) VAL=2.5 RISE=1 TARG v(cout) VAL=2.5 RISE=1

.end
