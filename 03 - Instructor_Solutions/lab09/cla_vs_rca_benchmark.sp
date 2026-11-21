* LAB 09: BENCHMARK DOI SANH 4-BIT CLA VS 4-BIT RCA (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Muc tieu: Do dac va so sanh truc tiep thoi gian tre lan truyen so nho C0 -> C4
*          giua Bo cong nhanh CLA va Bo cong gon song RCA (Mirror Adder)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Inverter chuan
.subckt inv_std in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_std

* --------------------------------------------------------------
* SUB-CIRCUITS CHO CLA 4-BIT
* --------------------------------------------------------------
.subckt pg_cell a b p g vdd gnd
Mp_na1 g_b a vdd vdd P W=3.6u L=0.6u
Mp_na2 g_b b vdd vdd P W=3.6u L=0.6u
Mn_na1 g_b a n_na1 gnd N W=2.4u L=0.6u
Mn_na2 n_na1 b gnd gnd N W=2.4u L=0.6u
X_inv_g g_b g vdd gnd inv_std
X_inv_a a a_b vdd gnd inv_std
Mp_tg1 p a_b b vdd P W=2.4u L=0.6u
Mn_tg1 p a   b gnd N W=1.2u L=0.6u
X_inv_b b b_b vdd gnd inv_std
Mp_tg2 p a   b_b vdd P W=2.4u L=0.6u
Mn_tg2 p a_b b_b gnd N W=1.2u L=0.6u
.ends pg_cell

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

.subckt sum_cell p c s vdd gnd
X_inv_c c c_b vdd gnd inv_std
Mp_tg1 s c_b p vdd P W=2.4u L=0.6u
Mn_tg1 s c   p gnd N W=1.2u L=0.6u
X_inv_p p p_b vdd gnd inv_std
Mp_tg2 s c   p_b vdd P W=2.4u L=0.6u
Mn_tg2 s c_b p_b gnd N W=1.2u L=0.6u
.ends sum_cell

.subckt cla_adder_4b a0 a1 a2 a3 b0 b1 b2 b3 c0 s0 s1 s2 s3 c4 vdd gnd
X_pg0 a0 b0 p0 g0 vdd gnd pg_cell
X_pg1 a1 b1 p1 g1 vdd gnd pg_cell
X_pg2 a2 b2 p2 g2 vdd gnd pg_cell
X_pg3 a3 b3 p3 g3 vdd gnd pg_cell
X_clg p0 g0 p1 g1 p2 g2 p3 g3 c0 c1 c2 c3 c4 vdd gnd clg_4b
X_sum0 p0 c0 s0 vdd gnd sum_cell
X_sum1 p1 c1 s1 vdd gnd sum_cell
X_sum2 p2 c2 s2 vdd gnd sum_cell
X_sum3 p3 c3 s3 vdd gnd sum_cell
.ends cla_adder_4b

* --------------------------------------------------------------
* SUB-CIRCUITS CHO RCA 4-BIT (MIRROR ADDER 28T)
* --------------------------------------------------------------
.subckt mirror_adder_1b a b cin sum cout vdd gnd
Mn_ca1 cout_b a n_ca1 gnd N W=2.4u L=0.6u
Mn_cb1 n_ca1  b gnd   gnd N W=2.4u L=0.6u
Mn_ccin cout_b cin n_ca2 gnd N W=2.4u L=0.6u
Mn_ca2  n_ca2  a   gnd   gnd N W=2.4u L=0.6u
Mn_cb2  n_ca2  b   gnd   gnd N W=2.4u L=0.6u

Mp_ca1 p_ca1 a vdd vdd P W=7.2u L=0.6u
Mp_cb1 p_ca1 b vdd vdd P W=7.2u L=0.6u
Mp_ccin cout_b cin p_ca1 vdd P W=7.2u L=0.6u
Mp_ca2 p_ca2 a vdd   vdd P W=7.2u L=0.6u
Mp_cb2 cout_b b p_ca2 vdd P W=7.2u L=0.6u
X_inv_cout cout_b cout vdd gnd inv_std

Mn_sa1 sum_b a n_sa1 gnd N W=3.6u L=0.6u
Mn_sb1 n_sa1 b n_sa2 gnd N W=3.6u L=0.6u
Mn_sc1 n_sa2 cin gnd gnd N W=3.6u L=0.6u
Mn_scout sum_b cout_b n_sa3 gnd N W=3.6u L=0.6u
Mn_sa2 n_sa3 a gnd gnd N W=3.6u L=0.6u
Mn_sb2 n_sa3 b gnd gnd N W=3.6u L=0.6u
Mn_sc2 n_sa3 cin gnd gnd N W=3.6u L=0.6u

Mp_sa1 p_sa1 a vdd vdd P W=7.2u L=0.6u
Mp_sb1 p_sa2 b p_sa1 vdd P W=7.2u L=0.6u
Mp_sc1 sum_b cin p_sa2 vdd P W=7.2u L=0.6u
Mp_scout p_sa3 cout_b vdd vdd P W=7.2u L=0.6u
Mp_sa2 sum_b a p_sa3 vdd P W=7.2u L=0.6u
Mp_sb2 sum_b b p_sa3 vdd P W=7.2u L=0.6u
Mp_sc2 sum_b cin p_sa3 vdd P W=7.2u L=0.6u
X_inv_sum sum_b sum vdd gnd inv_std
.ends mirror_adder_1b

.subckt rca_adder_4b a0 a1 a2 a3 b0 b1 b2 b3 c0 s0 s1 s2 s3 c4 vdd gnd
X_fa0 a0 b0 c0 s0 c1 vdd gnd mirror_adder_1b
X_fa1 a1 b1 c1 s1 c2 vdd gnd mirror_adder_1b
X_fa2 a2 b2 c2 s2 c3 vdd gnd mirror_adder_1b
X_fa3 a3 b3 c3 s3 c4 vdd gnd mirror_adder_1b
.ends rca_adder_4b

* ==============================================================
* TESTBENCH KICH HOAT SONG SONG CA 2 MACH
* ==============================================================
Va0 a0 0 DC 5.0
Va1 a1 0 DC 5.0
Va2 a2 0 DC 5.0
Va3 a3 0 DC 5.0

Vb0 b0 0 DC 0.0
Vb1 b1 0 DC 0.0
Vb2 b2 0 DC 0.0
Vb3 b3 0 DC 0.0

Vc0 c0 0 PULSE(0 5.0 5.0n 0.1n 0.1n 10n 20n)

* Mach 1: 4-bit CLA
X_cla a0 a1 a2 a3 b0 b1 b2 b3 c0 s0_cla s1_cla s2_cla s3_cla c4_cla vdd 0 cla_adder_4b
Cc4_cla c4_cla 0 50fF

* Mach 2: 4-bit RCA
X_rca a0 a1 a2 a3 b0 b1 b2 b3 c0 s0_rca s1_rca s2_rca s3_rca c4_rca vdd 0 rca_adder_4b
Cc4_rca c4_rca 0 50fF

.tran 0.02n 15n

* Do tre Carry C0 -> C4 cho ca 2 mach
.meas tran tpd_carry_cla TRIG V(c0) VAL=2.5 RISE=1 TARG V(c4_cla) VAL=2.5 RISE=1
.meas tran tpd_carry_rca TRIG V(c0) VAL=2.5 RISE=1 TARG V(c4_rca) VAL=2.5 RISE=1

* Do tre Sum S3 cho ca 2 mach
.meas tran tpd_sum_cla TRIG V(c0) VAL=2.5 RISE=1 TARG V(s3_cla) VAL=2.5 FALL=1
.meas tran tpd_sum_rca TRIG V(c0) VAL=2.5 RISE=1 TARG V(s3_rca) VAL=2.5 FALL=1

.end
