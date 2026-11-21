* LAB 07: DOMINO 4-INPUT OR GATE TRANSIENT SIMULATION
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Kien truc: Dynamic OR4 + Weak PMOS Keeper + High-skew Static Inverter
* Ham logic: Y = A + B + C + D

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* ==============================================================
* SUBCIRCUIT: domino_or4_x1
* a b c d clk y vdd gnd
* ==============================================================
.subckt domino_or4_x1 a b c d clk y vdd gnd

* 1. Precharge PMOS (W=12lambda = 3.6u, L=2lambda = 0.6u)
Mp_pre x clk vdd vdd P W=3.6u L=0.6u

* 2. Weak PMOS Keeper (W=2lambda = 0.6u, L=2lambda = 0.6u)
M_kp x y vdd vdd P W=0.6u L=0.6u

* 3. Evaluate Foot NMOS (W=8lambda = 2.4u, L=2lambda = 0.6u)
Mn_foot n_eval clk gnd gnd N W=2.4u L=0.6u

* 4. Mạng PDN: 4 NMOS song song A, B, C, D (Moi NMOS: W=4lambda = 1.2u)
Mn_a x a n_eval gnd N W=1.2u L=0.6u
Mn_b x b n_eval gnd N W=1.2u L=0.6u
Mn_c x c n_eval gnd N W=1.2u L=0.6u
Mn_d x d n_eval gnd N W=1.2u L=0.6u

* 5. Dien dung ky sinh nut dong X
C_x x 0 25fF

* 6. Static Inverter bo dem ngo ra (PMOS W=16lambda=4.8u, NMOS W=8lambda=2.4u)
Mp_inv y x vdd vdd P W=4.8u L=0.6u
Mn_inv y x gnd gnd N W=2.4u L=0.6u

.ends domino_or4_x1

* ==============================================================
* MACH THU (TESTBENCH)
* ==============================================================
X_dut a b c d clk y vdd 0 domino_or4_x1

* Tai ngo ra CL = 30fF
Cload y 0 30fF

* Xung nhip CLK: f = 100MHz (T = 10ns, Do rong 5ns)
Vclk clk 0 PULSE(0 5.0 0 0.1n 0.1n 5n 10n)

* Ngo vao A: Kich hoat o chu ky 2 (Evaluate 2: t = 10ns - 20ns)
Va a 0 PULSE(0 5.0 12n 0.1n 0.1n 6n 50n)

* Ngo vao B: Kich hoat o chu ky 3 (Evaluate 3: t = 20ns - 30ns)
Vb b 0 PULSE(0 5.0 22n 0.1n 0.1n 6n 50n)

* Ngo vao C: Kich hoat o chu ky 4 (Evaluate 4: t = 30ns - 40ns)
Vc c 0 PULSE(0 5.0 32n 0.1n 0.1n 6n 50n)

* Ngo vao D: Giu 0V de kiem chung khi ca 4 ngo vao = 0 (Evaluate 1: t = 0 - 10ns)
Vd d 0 DC 0.0

* ==============================================================
* MO PHONG TRANSIENT & DO TRE
* ==============================================================
.tran 0.02n 45n

* Do tre Evaluate khi A bat len 5V (Chu ky 2 tai t ≈ 12ns)
.meas tran tpd_eval TRIG V(a) VAL=2.5 RISE=1 TARG V(y) VAL=2.5 RISE=1

* Cong suat tieu tan trung binh toan mach
.meas tran p_avg AVG I(Vdd)*5.0

* Dien ap nut dong X trong chu ky 1 (Evaluate 1, moi ngo vao = 0: X phai giu ~5V)
.meas tran vx_eval1_min MIN V(X_dut.x) FROM=5n TO=10n

* Dien ap ngo ra Y trong chu ky 1 (Y phai giu 0V)
.meas tran vy_eval1_max MAX V(y) FROM=5n TO=10n

.end
