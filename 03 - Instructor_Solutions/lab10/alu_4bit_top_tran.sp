* LAB 10: CAPSTONE 4-BIT REGISTERED ALU TRANSIENT SIMULATION (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Kien truc: Top-Level CLA4 + Logic Unit + MUX4:1 4-bit + 4-bit DFF Register + Flag Unit
* Chuc nang OP[1:0]: 00: ADD | 01: AND | 10: OR | 11: XOR
* Tong so Transistor: 358 Transistors

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Inverter chuan (Wp=3.6u, Wn=1.2u)
.subckt inv_std in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_std

* ==============================================================
* 1. KHOI D-FLIP-FLOP MASTER-SLAVE CHUAN (DFF_MS_X1 - Tu Bai 5)
* ==============================================================
.subckt dff_ms_x1 d clk q qb vdd gnd
X_inv_clk clk clk_b vdd gnd inv_std
* TG1 (Master Input, mo khi CLK=0)
Mp_tg1 d_m clk   d vdd P W=2.4u L=0.6u
Mn_tg1 d_m clk_b d gnd N W=1.2u L=0.6u
* Master Inverter 1 & Feedback Inverter 2
X_inv_m1 d_m q_m_b vdd gnd inv_std
X_inv_m2 q_m_b q_m vdd gnd inv_std
Mp_tg2 d_m clk_b q_m vdd P W=2.4u L=0.6u
Mn_tg2 d_m clk   q_m gnd N W=1.2u L=0.6u

* TG3 (Slave Input, mo khi CLK=1)
Mp_tg3 d_s clk_b q_m_b vdd P W=2.4u L=0.6u
Mn_tg3 d_s clk   q_m_b gnd N W=1.2u L=0.6u
* Slave Inverter 1 & Output Inverter
X_inv_s1 d_s q_b vdd gnd inv_std
X_inv_out q_b q vdd gnd inv_std
* Feedback Slave
X_inv_s2 q_b q_s vdd gnd inv_std
Mp_tg4 d_s clk   q_s vdd P W=2.4u L=0.6u
Mn_tg4 d_s clk_b q_s gnd N W=1.2u L=0.6u
.ends dff_ms_x1

* Thanh ghi 4-bit
.subckt dff_reg4 d0 d1 d2 d3 clk q0 q1 q2 q3 vdd gnd
X_ff0 d0 clk q0 q0_b vdd gnd dff_ms_x1
X_ff1 d1 clk q1 q1_b vdd gnd dff_ms_x1
X_ff2 d2 clk q2 q2_b vdd gnd dff_ms_x1
X_ff3 d3 clk q3 q3_b vdd gnd dff_ms_x1
.ends dff_reg4

* ==============================================================
* 2. KHOI LOGIC 4-BIT (AND, OR, XOR)
* ==============================================================
.subckt logic_unit_4b a0 a1 a2 a3 b0 b1 b2 b3
+ and0 and1 and2 and3 or0 or1 or2 or3 xor0 xor1 xor2 xor3 vdd gnd

* 4-bit AND (NAND2 + Inverter)
.param Wn=2.4u Wp=3.6u
Mn_a0 nd0 a0 n1_0 gnd N W=Wn L=0.6u
Mn_b0 n1_0 b0 gnd gnd N W=Wn L=0.6u
Mp_a0 nd0 a0 vdd vdd P W=Wp L=0.6u
Mp_b0 nd0 b0 vdd vdd P W=Wp L=0.6u
X_inv_and0 nd0 and0 vdd gnd inv_std

Mn_a1 nd1 a1 n1_1 gnd N W=Wn L=0.6u
Mn_b1 n1_1 b1 gnd gnd N W=Wn L=0.6u
Mp_a1 nd1 a1 vdd vdd P W=Wp L=0.6u
Mp_b1 nd1 b1 vdd vdd P W=Wp L=0.6u
X_inv_and1 nd1 and1 vdd gnd inv_std

Mn_a2 nd2 a2 n1_2 gnd N W=Wn L=0.6u
Mn_b2 n1_2 b2 gnd gnd N W=Wn L=0.6u
Mp_a2 nd2 a2 vdd vdd P W=Wp L=0.6u
Mp_b2 nd2 b2 vdd vdd P W=Wp L=0.6u
X_inv_and2 nd2 and2 vdd gnd inv_std

Mn_a3 nd3 a3 n1_3 gnd N W=Wn L=0.6u
Mn_b3 n1_3 b3 gnd gnd N W=Wn L=0.6u
Mp_a3 nd3 a3 vdd vdd P W=Wp L=0.6u
Mp_b3 nd3 b3 vdd vdd P W=Wp L=0.6u
X_inv_and3 nd3 and3 vdd gnd inv_std

* 4-bit OR (NOR2 + Inverter)
Mn_or_a0 nr0 a0 gnd gnd N W=Wn L=0.6u
Mn_or_b0 nr0 b0 gnd gnd N W=Wn L=0.6u
Mp_or_a0 pnr0 a0 vdd vdd P W=7.2u L=0.6u
Mp_or_b0 nr0  b0 pnr0 vdd P W=7.2u L=0.6u
X_inv_or0 nr0 or0 vdd gnd inv_std

Mn_or_a1 nr1 a1 gnd gnd N W=Wn L=0.6u
Mn_or_b1 nr1 b1 gnd gnd N W=Wn L=0.6u
Mp_or_a1 pnr1 a1 vdd vdd P W=7.2u L=0.6u
Mp_or_b1 nr1  b1 pnr1 vdd P W=7.2u L=0.6u
X_inv_or1 nr1 or1 vdd gnd inv_std

Mn_or_a2 nr2 a2 gnd gnd N W=Wn L=0.6u
Mn_or_b2 nr2 b2 gnd gnd N W=Wn L=0.6u
Mp_or_a2 pnr2 a2 vdd vdd P W=7.2u L=0.6u
Mp_or_b2 nr2  b2 pnr2 vdd P W=7.2u L=0.6u
X_inv_or2 nr2 or2 vdd gnd inv_std

Mn_or_a3 nr3 a3 gnd gnd N W=Wn L=0.6u
Mn_or_b3 nr3 b3 gnd gnd N W=Wn L=0.6u
Mp_or_a3 pnr3 a3 vdd vdd P W=7.2u L=0.6u
Mp_or_b3 nr3  b3 pnr3 vdd P W=7.2u L=0.6u
X_inv_or3 nr3 or3 vdd gnd inv_std

* 4-bit XOR (TG XOR)
.subckt tg_xor a b y vdd gnd
X_inv_a a a_b vdd gnd inv_std
X_inv_b b b_b vdd gnd inv_std
Mp1 y a_b b vdd P W=2.4u L=0.6u
Mn1 y a   b gnd N W=1.2u L=0.6u
Mp2 y a   b_b vdd P W=2.4u L=0.6u
Mn2 y a_b b_b gnd N W=1.2u L=0.6u
.ends tg_xor

X_xor0 a0 b0 xor0 vdd gnd tg_xor
X_xor1 a1 b1 xor1 vdd gnd tg_xor
X_xor2 a2 b2 xor2 vdd gnd tg_xor
X_xor3 a3 b3 xor3 vdd gnd tg_xor

.ends logic_unit_4b

* ==============================================================
* 3. KHOI BO CHON MUX 4:1 4-BIT (TG MUX4_4B)
* ==============================================================
.subckt mux4_1b in0 in1 in2 in3 op0 op1 y vdd gnd
X_inv_op0 op0 op0_b vdd gnd inv_std
X_inv_op1 op1 op1_b vdd gnd inv_std

* Nhanh in0: op1=0, op0=0
Mp0 y op0 in0_int vdd P W=2.4u L=0.6u
Mn0 y op0_b in0_int gnd N W=1.2u L=0.6u
Mp00 in0_int op1 in0 vdd P W=2.4u L=0.6u
Mn00 in0_int op1_b in0 gnd N W=1.2u L=0.6u

* Nhanh in1: op1=0, op0=1
Mp1 y op0_b in1_int vdd P W=2.4u L=0.6u
Mn1 y op0   in1_int gnd N W=1.2u L=0.6u
Mp11 in1_int op1 in1 vdd P W=2.4u L=0.6u
Mn11 in1_int op1_b in1 gnd N W=1.2u L=0.6u

* Nhanh in2: op1=1, op0=0
Mp2 y op0 in2_int vdd P W=2.4u L=0.6u
Mn2 y op0_b in2_int gnd N W=1.2u L=0.6u
Mp22 in2_int op1_b in2 vdd P W=2.4u L=0.6u
Mn22 in2_int op1   in2 gnd N W=1.2u L=0.6u

* Nhanh in3: op1=1, op0=1
Mp3 y op0_b in3_int vdd P W=2.4u L=0.6u
Mn3 y op0   in3_int gnd N W=1.2u L=0.6u
Mp33 in3_int op1_b in3 vdd P W=2.4u L=0.6u
Mn33 in3_int op1   in3 gnd N W=1.2u L=0.6u

.ends mux4_1b

.subckt mux4_4b add0 add1 add2 add3 and0 and1 and2 and3
+ or0 or1 or2 or3 xor0 xor1 xor2 xor3 op0 op1 y0 y1 y2 y3 vdd gnd
X_m0 add0 and0 or0 xor0 op0 op1 y0 vdd gnd mux4_1b
X_m1 add1 and1 or1 xor1 op0 op1 y1 vdd gnd mux4_1b
X_m2 add2 and2 or2 xor2 op0 op1 y2 vdd gnd mux4_1b
X_m3 add3 and3 or3 xor3 op0 op1 y3 vdd gnd mux4_1b
.ends mux4_4b

* ==============================================================
* 4. KHOI CO TRANG THAI (ZERO FLAG & CARRY LATCH)
* ==============================================================
.subckt flag_unit y0 y1 y2 y3 cout_cla op0 op1 clk z_flag cout_flag vdd gnd
* Zero Flag: Z = !(y0 + y1 + y2 + y3) - Dung NOR4
Mn_z0 nor_out y0 gnd gnd N W=2.4u L=0.6u
Mn_z1 nor_out y1 gnd gnd N W=2.4u L=0.6u
Mn_z2 nor_out y2 gnd gnd N W=2.4u L=0.6u
Mn_z3 nor_out y3 gnd gnd N W=2.4u L=0.6u

Mp_z0 pz1 y0 vdd vdd P W=9.6u L=0.6u
Mp_z1 pz2 y1 pz1 vdd P W=9.6u L=0.6u
Mp_z2 pz3 y2 pz2 vdd P W=9.6u L=0.6u
Mp_z3 nor_out y3 pz3 vdd P W=9.6u L=0.6u

* DFF chot co Zero theo xung nhip
X_ff_z nor_out clk z_flag z_b vdd gnd dff_ms_x1

* DFF chot co Carry
X_ff_c cout_cla clk cout_flag c_b vdd gnd dff_ms_x1
.ends flag_unit

* ==============================================================
* 5. KHOI KHOI CONG NHANH CLA 4-BIT (TU LAB 09)
* ==============================================================
.subckt pg_cell_cla a b p g vdd gnd
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
.ends pg_cell_cla

.subckt clg_4b_core p0 g0 p1 g1 p2 g2 p3 g3 c0 c1 c2 c3 c4 vdd gnd
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
.ends clg_4b_core

.subckt sum_cell_cla p c s vdd gnd
X_inv_c c c_b vdd gnd inv_std
Mp_tg1 s c_b p vdd P W=2.4u L=0.6u
Mn_tg1 s c   p gnd N W=1.2u L=0.6u
X_inv_p p p_b vdd gnd inv_std
Mp_tg2 s c   p_b vdd P W=2.4u L=0.6u
Mn_tg2 s c_b p_b gnd N W=1.2u L=0.6u
.ends sum_cell_cla

.subckt cla_adder_4b a0 a1 a2 a3 b0 b1 b2 b3 c0 s0 s1 s2 s3 c4 vdd gnd
X_pg0 a0 b0 p0 g0 vdd gnd pg_cell_cla
X_pg1 a1 b1 p1 g1 vdd gnd pg_cell_cla
X_pg2 a2 b2 p2 g2 vdd gnd pg_cell_cla
X_pg3 a3 b3 p3 g3 vdd gnd pg_cell_cla
X_clg p0 g0 p1 g1 p2 g2 p3 g3 c0 c1 c2 c3 c4 vdd gnd clg_4b_core
X_sum0 p0 c0 s0 vdd gnd sum_cell_cla
X_sum1 p1 c1 s1 vdd gnd sum_cell_cla
X_sum2 p2 c2 s2 vdd gnd sum_cell_cla
X_sum3 p3 c3 s3 vdd gnd sum_cell_cla
.ends cla_adder_4b

* ==============================================================
* TOP-LEVEL CAPSTONE VI MACH: alu_4b_reg
* ==============================================================
.subckt alu_4b_reg a0 a1 a2 a3 b0 b1 b2 b3 cin op0 op1 clk
+ out0 out1 out2 out3 cout_flag z_flag vdd gnd

* 1. Khối Số học CLA 4-bit
X_cla a0 a1 a2 a3 b0 b1 b2 b3 cin add0 add1 add2 add3 cout_cla vdd gnd cla_adder_4b

* 2. Khối Logic 4-bit
X_logic a0 a1 a2 a3 b0 b1 b2 b3
+ and0 and1 and2 and3 or0 or1 or2 or3 xor0 xor1 xor2 xor3 vdd gnd logic_unit_4b

* 3. Khối Dồn kênh chọn lệnh MUX 4:1 4-bit
X_mux add0 add1 add2 add3 and0 and1 and2 and3
+ or0 or1 or2 or3 xor0 xor1 xor2 xor3 op0 op1
+ res0 res1 res2 res3 vdd gnd mux4_4b

* 4. Khối Thanh ghi chốt ngõ ra 4-bit
X_reg res0 res1 res2 res3 clk out0 out1 out2 out3 vdd gnd dff_reg4

* 5. Khối Cờ trạng thái
X_flags out0 out1 out2 out3 cout_cla op0 op1 clk z_flag cout_flag vdd gnd flag_unit

.ends alu_4b_reg

* ==============================================================
* TESTBENCH KICH HOAT CHUONG TRINH DA CHU KY
* Chu ky T = 5ns (f = 200MHz):
* Chu ky 1 (0-5ns):   OP=00 (ADD) 5 + 3 = 8
* Chu ky 2 (5-10ns):  OP=00 (ADD) 12 + 4 = 16 -> OUT=0, Cout=1, Z=1
* Chu ky 3 (10-15ns): OP=01 (AND) 10 & 12 = 8
* Chu ky 4 (15-20ns): OP=10 (OR)  10 | 5 = 15
* Chu ky 5 (20-25ns): OP=11 (XOR) 9 ^ 9 = 0 -> Z=1
* ==============================================================
Vclk clk 0 PULSE(0 5.0 2.5n 0.1n 0.1n 2.4n 5.0n)
Vcin cin 0 DC 0.0

* OP[1:0] Signals
Vop0 op0 0 PWL(0ns 0V 10ns 0V 10.1ns 5V 15ns 5V 15.1ns 0V 20ns 0V 20.1ns 5V 25ns 5V)
Vop1 op1 0 PWL(0ns 0V 15ns 0V 15.1ns 5V 25ns 5V)

* A[3:0] Data: 5 (0101) -> 12 (1100) -> 10 (1010) -> 10 (1010) -> 9 (1001)
Va0 a0 0 PWL(0ns 5V 5ns 5V 5.1ns 0V 10ns 0V 10.1ns 0V 20ns 0V 20.1ns 5V 25ns 5V)
Va1 a1 0 PWL(0ns 0V 10ns 0V 10.1ns 5V 20ns 5V 20.1ns 0V 25ns 0V)
Va2 a2 0 PWL(0ns 5V 10ns 5V 10.1ns 0V 25ns 0V)
Va3 a3 0 PWL(0ns 0V 5ns 0V 5.1ns 5V 25ns 5V)

* B[3:0] Data: 3 (0011) -> 4 (0100) -> 12 (1100) -> 5 (0101) -> 9 (1001)
Vb0 b0 0 PWL(0ns 5V 5ns 5V 5.1ns 0V 15ns 0V 15.1ns 5V 25ns 5V)
Vb1 b1 0 PWL(0ns 5V 5ns 5V 5.1ns 0V 20ns 0V 20.1ns 0V 25ns 0V)
Vb2 b2 0 PWL(0ns 0V 5ns 0V 5.1ns 5V 20ns 5V 20.1ns 0V 25ns 0V)
Vb3 b3 0 PWL(0ns 0V 10ns 0V 10.1ns 5V 15ns 5V 15.1ns 0V 20ns 0V 20.1ns 5V 25ns 5V)

* Goi Top Level Registered ALU
X_alu a0 a1 a2 a3 b0 b1 b2 b3 cin op0 op1 clk
+ out0 out1 out2 out3 cout_flag z_flag vdd 0 alu_4b_reg

C_out0 out0 0 30fF
C_out1 out1 0 30fF
C_out2 out2 0 30fF
C_out3 out3 0 30fF

.tran 0.05n 25n

* Do tre Clock-to-Out o chu ky 1 (CLK bat tai 2.5ns)
.meas tran t_cq_out3 TRIG V(clk) VAL=2.5 RISE=1 TARG V(out3) VAL=2.5 RISE=1

* Cong suat tieu tan trung binh toan vi mach
.meas tran p_chip_avg AVG I(Vdd)*5.0

.end
