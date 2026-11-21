* LAB 09: CARRY LOOKAHEAD GENERATOR (CLG_4B) STANDALONE TEST (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Muc tieu: Kiem tra doc lap toc do sinh so nho C1, C2, C3, C4 cua khoi CLG

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

.subckt inv_std in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_std

* Subcircuit CLG_4B
.subckt clg_4b p0 g0 p1 g1 p2 g2 p3 g3 c0 c1 c2 c3 c4 vdd gnd
Mp_c1_1 n_pc1 g0 vdd vdd P W=4.8u L=0.6u
Mp_c1_2 c1_b  p0 n_pc1 vdd P W=4.8u L=0.6u
Mp_c1_3 c1_b  c0 n_pc1 vdd P W=4.8u L=0.6u
Mn_c1_g0 c1_b g0 gnd gnd N W=2.4u L=0.6u
Mn_c1_p0 c1_b p0 n_nc1 gnd N W=2.4u L=0.6u
Mn_c1_c0 n_nc1 c0 gnd gnd N W=2.4u L=0.6u
X_inv_c1 c1_b c1 vdd gnd inv_std

Mn_c2_g1 c2_b g1 gnd gnd N W=2.4u L=0.6u
Mn_c2_p1_1 c2_b p1 n_nc2_1 gnd N W=2.4u L=0.6u
Mn_c2_g0 n_nc2_1 g0 gnd gnd N W=2.4u L=0.6u
Mn_c2_p1_2 c2_b p1 n_nc2_2 gnd N W=2.4u L=0.6u
Mn_c2_p0 n_nc2_2 p0 n_nc2_3 gnd N W=2.4u L=0.6u
Mn_c2_c0 n_nc2_3 c0 gnd gnd N W=2.4u L=0.6u
Mp_c2_g1 c2_b g1 vdd vdd P W=7.2u L=0.6u
X_inv_c2 c2_b c2 vdd gnd inv_std

Mn_c3_g2 c3_b g2 gnd gnd N W=2.4u L=0.6u
Mn_c3_p2_1 c3_b p2 n_nc3_1 gnd N W=2.4u L=0.6u
Mn_c3_g1 n_nc3_1 g1 gnd gnd N W=2.4u L=0.6u
Mn_c3_p2_2 c3_b p2 n_nc3_2 gnd N W=2.4u L=0.6u
Mn_c3_p1_1 n_nc3_2 p1 n_nc3_3 gnd N W=2.4u L=0.6u
Mn_c3_g0 n_nc3_3 g0 gnd gnd N W=2.4u L=0.6u
Mn_c3_p2_3 c3_b p2 n_nc3_4 gnd N W=2.4u L=0.6u
Mn_c3_p1_2 n_nc3_4 p1 n_nc3_5 gnd N W=2.4u L=0.6u
Mn_c3_p0 n_nc3_5 p0 n_nc3_6 gnd N W=2.4u L=0.6u
Mn_c3_c0 n_nc3_6 c0 gnd gnd N W=2.4u L=0.6u
Mp_c3_g2 c3_b g2 vdd vdd P W=7.2u L=0.6u
X_inv_c3 c3_b c3 vdd gnd inv_std

Mn_c4_g3 c4_b g3 gnd gnd N W=2.4u L=0.6u
Mn_c4_p3_1 c4_b p3 n_nc4_1 gnd N W=2.4u L=0.6u
Mn_c4_g2 n_nc4_1 g2 gnd gnd N W=2.4u L=0.6u
Mn_c4_p3_2 c4_b p3 n_nc4_2 gnd N W=2.4u L=0.6u
Mn_c4_p2_1 n_nc4_2 p2 n_nc4_3 gnd N W=2.4u L=0.6u
Mn_c4_g1 n_nc4_3 g1 gnd gnd N W=2.4u L=0.6u
Mn_c4_p3_3 c4_b p3 n_nc4_4 gnd N W=2.4u L=0.6u
Mn_c4_p2_2 n_nc4_4 p2 n_nc4_5 gnd N W=2.4u L=0.6u
Mn_c4_p1_1 n_nc4_5 p1 n_nc4_6 gnd N W=2.4u L=0.6u
Mn_c4_g0 n_nc4_6 g0 gnd gnd N W=2.4u L=0.6u
Mn_c4_p3_4 c4_b p3 n_nc4_7 gnd N W=2.4u L=0.6u
Mn_c4_p2_3 n_nc4_7 p2 n_nc4_8 gnd N W=2.4u L=0.6u
Mn_c4_p1_2 n_nc4_8 p1 n_nc4_9 gnd N W=2.4u L=0.6u
Mn_c4_p0 n_nc4_9 p0 n_nc4_10 gnd N W=2.4u L=0.6u
Mn_c4_c0 n_nc4_10 c0 gnd gnd N W=2.4u L=0.6u
Mp_c4_g3 c4_b g3 vdd vdd P W=7.2u L=0.6u
X_inv_c4 c4_b c4 vdd gnd inv_std
.ends clg_4b

* Testbench: P0=P1=P2=P3 = 1, G0=G1=G2=G3 = 0, C0: 0 -> 1
Vp0 p0 0 DC 5.0
Vp1 p1 0 DC 5.0
Vp2 p2 0 DC 5.0
Vp3 p3 0 DC 5.0

Vg0 g0 0 DC 0.0
Vg1 g1 0 DC 0.0
Vg2 g2 0 DC 0.0
Vg3 g3 0 DC 0.0

Vc0 c0 0 PULSE(0 5.0 2.0n 0.1n 0.1n 5n 10n)

X_dut p0 g0 p1 g1 p2 g2 p3 g3 c0 c1 c2 c3 c4 vdd 0 clg_4b

Cc1 c1 0 30fF
Cc2 c2 0 30fF
Cc3 c3 0 30fF
Cc4 c4 0 50fF

.tran 0.02n 6n

* Do tre truyen so nho tu C0 den tung ngo ra
.meas tran tpd_c0_c1 TRIG V(c0) VAL=2.5 RISE=1 TARG V(c1) VAL=2.5 RISE=1
.meas tran tpd_c0_c2 TRIG V(c0) VAL=2.5 RISE=1 TARG V(c2) VAL=2.5 RISE=1
.meas tran tpd_c0_c3 TRIG V(c0) VAL=2.5 RISE=1 TARG V(c3) VAL=2.5 RISE=1
.meas tran tpd_c0_c4 TRIG V(c0) VAL=2.5 RISE=1 TARG V(c4) VAL=2.5 RISE=1

.end
