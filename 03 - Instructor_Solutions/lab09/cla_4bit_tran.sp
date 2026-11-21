* LAB 09: 4-BIT CARRY LOOKAHEAD ADDER (CLA) TRANSIENT SIMULATION
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Kien truc: 3 tang phan cap (PG Cell -> CLG Unit -> Sum Cell)
* Ngo vao: A[3:0], B[3:0], C0 | Ngo ra: S[3:0], C4

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Inverter chuan (Wp=3.6u, Wn=1.2u)
.subckt inv_std in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_std

* ==============================================================
* KHOI 1: TE BAO SINH CO PG (PG_CELL)
* P = A xor B, G = A and B (12 Transistors)
* ==============================================================
.subckt pg_cell a b p g vdd gnd
* Cổng NAND2 tao g_b, qua Inverter thanh g (G = AB)
Mp_na1 g_b a vdd vdd P W=3.6u L=0.6u
Mp_na2 g_b b vdd vdd P W=3.6u L=0.6u
Mn_na1 g_b a n_na1 gnd N W=2.4u L=0.6u
Mn_na2 n_na1 b gnd gnd N W=2.4u L=0.6u
X_inv_g g_b g vdd gnd inv_std

* Cong XOR2 dung Transmission Gate tao p (P = A xor B)
X_inv_a a a_b vdd gnd inv_std
* TG 1 truyen B khi A=0 (a_b=1)
Mp_tg1 p a_b b vdd P W=2.4u L=0.6u
Mn_tg1 p a   b gnd N W=1.2u L=0.6u
* TG 2 truyen B_b khi A=1
X_inv_b b b_b vdd gnd inv_std
Mp_tg2 p a   b_b vdd P W=2.4u L=0.6u
Mn_tg2 p a_b b_b gnd N W=1.2u L=0.6u
.ends pg_cell

* ==============================================================
* KHOI 2: KHỐI TẠO SỐ NHỚ SỚM 4-BIT (CLG_4B)
* C1 = G0 + P0*C0
* C2 = G1 + P1*G0 + P1*P0*C0
* C3 = G2 + P2*G1 + P2*P1*G0 + P2*P1*P0*C0
* C4 = G3 + P3*G2 + P3*P2*G1 + P3*P2*P1*G0 + P3*P2*P1*P0*C0
* ==============================================================
.subckt clg_4b p0 g0 p1 g1 p2 g2 p3 g3 c0 c1 c2 c3 c4 vdd gnd

* --- Mach tao C1 (AOI21 + Inv) ---
* c1_b = !(G0 + P0*C0)
Mp_c1_1 n_pc1 g0 vdd vdd P W=4.8u L=0.6u
Mp_c1_2 c1_b  p0 n_pc1 vdd P W=4.8u L=0.6u
Mp_c1_3 c1_b  c0 n_pc1 vdd P W=4.8u L=0.6u

Mn_c1_g0 c1_b g0 gnd gnd N W=2.4u L=0.6u
Mn_c1_p0 c1_b p0 n_nc1 gnd N W=2.4u L=0.6u
Mn_c1_c0 n_nc1 c0 gnd gnd N W=2.4u L=0.6u
X_inv_c1 c1_b c1 vdd gnd inv_std

* --- Mach tao C2 (AOI321 + Inv) ---
* c2_b = !(G1 + P1*G0 + P1*P0*C0)
Mn_c2_g1 c2_b g1 gnd gnd N W=2.4u L=0.6u
Mn_c2_p1_1 c2_b p1 n_nc2_1 gnd N W=2.4u L=0.6u
Mn_c2_g0 n_nc2_1 g0 gnd gnd N W=2.4u L=0.6u

Mn_c2_p1_2 c2_b p1 n_nc2_2 gnd N W=2.4u L=0.6u
Mn_c2_p0 n_nc2_2 p0 n_nc2_3 gnd N W=2.4u L=0.6u
Mn_c2_c0 n_nc2_3 c0 gnd gnd N W=2.4u L=0.6u

Mp_c2_g1 c2_b g1 vdd vdd P W=7.2u L=0.6u
X_inv_c2 c2_b c2 vdd gnd inv_std

* --- Mach tao C3 (AOI4321 + Inv) ---
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

* --- Mach tao C4 (AOI54321 + Inv) ---
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

* ==============================================================
* KHOI 3: TE BAO TAO TONG SUM (SUM_CELL)
* S = P xor C (6 Transistors)
* ==============================================================
.subckt sum_cell p c s vdd gnd
X_inv_c c c_b vdd gnd inv_std
* TG truyen P khi C=0
Mp_tg1 s c_b p vdd P W=2.4u L=0.6u
Mn_tg1 s c   p gnd N W=1.2u L=0.6u
* TG truyen P_b khi C=1
X_inv_p p p_b vdd gnd inv_std
Mp_tg2 s c   p_b vdd P W=2.4u L=0.6u
Mn_tg2 s c_b p_b gnd N W=1.2u L=0.6u
.ends sum_cell

* ==============================================================
* TOP-LEVEL SUBCIRCUIT: cla_adder_4b
* ==============================================================
.subckt cla_adder_4b a0 a1 a2 a3 b0 b1 b2 b3 c0 s0 s1 s2 s3 c4 vdd gnd

* 1. Khối 4 PG Cells
X_pg0 a0 b0 p0 g0 vdd gnd pg_cell
X_pg1 a1 b1 p1 g1 vdd gnd pg_cell
X_pg2 a2 b2 p2 g2 vdd gnd pg_cell
X_pg3 a3 b3 p3 g3 vdd gnd pg_cell

* 2. Khối Carry Lookahead Generator
X_clg p0 g0 p1 g1 p2 g2 p3 g3 c0 c1 c2 c3 c4 vdd gnd clg_4b

* 3. Khối 4 Sum Cells
X_sum0 p0 c0 s0 vdd gnd sum_cell
X_sum1 p1 c1 s1 vdd gnd sum_cell
X_sum2 p2 c2 s2 vdd gnd sum_cell
X_sum3 p3 c3 s3 vdd gnd sum_cell

.ends cla_adder_4b

* ==============================================================
* TESTBENCH WORST-CASE CARRY PROPAGATION
* A = 1111 (15), B = 0000 (0), C0: 0 -> 1 tai t = 5ns
* Sum truoc 5ns: 1111 (15), C4 = 0
* Sum sau 5ns:   0000 (0),  C4 = 1 (15 + 1 = 16)
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

* Goi Top Level CLA
X_dut a0 a1 a2 a3 b0 b1 b2 b3 c0 s0 s1 s2 s3 c4 vdd 0 cla_adder_4b

* Tai ngo ra
Cs0 s0 0 30fF
Cs1 s1 0 30fF
Cs2 s2 0 30fF
Cs3 s3 0 30fF
Cc4 c4 0 50fF

* ==============================================================
* MO PHONG TRANSIENT & DO TRE
* ==============================================================
.tran 0.02n 15n

* Do tre Carry Propagation: C0 -> C4
.meas tran tpd_c0_c4 TRIG V(c0) VAL=2.5 RISE=1 TARG V(c4) VAL=2.5 RISE=1

* Do tre Sum S3: C0 -> S3 (chuyen tu 1 -> 0)
.meas tran tpd_c0_s3 TRIG V(c0) VAL=2.5 RISE=1 TARG V(s3) VAL=2.5 FALL=1

* Cong suat tieu tan trung binh
.meas tran p_avg AVG I(Vdd)*5.0

.end
