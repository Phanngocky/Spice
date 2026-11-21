* LAB 07: KEEPER SIZING SWEEP & CONTENTION ANALYSIS
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Muc tieu: Khao sat su danh doi giua Do tre danh gia (tpd_eval) va Su tranh chap Keeper

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Tham so do rong kenh cua Keeper
.param Wkp = 0.6u

* Subcircuit Domino OR4 voi tham so Wkp
.subckt domino_or4_param a b c d clk y vdd gnd PARAMS: W_k=0.6u
Mp_pre x clk vdd vdd P W=3.6u L=0.6u
M_kp   x y   vdd vdd P W={W_k} L=0.6u
Mn_foot n_eval clk gnd gnd N W=2.4u L=0.6u

Mn_a x a n_eval gnd N W=1.2u L=0.6u
Mn_b x b n_eval gnd N W=1.2u L=0.6u
Mn_c x c n_eval gnd N W=1.2u L=0.6u
Mn_d x d n_eval gnd N W=1.2u L=0.6u

C_x x 0 25fF

Mp_inv y x vdd vdd P W=4.8u L=0.6u
Mn_inv y x gnd gnd N W=2.4u L=0.6u
.ends domino_or4_param

* 4 Phien ban voi 4 kich thuoc Keeper khac nhau:
* 1. W = 0.6u (2 lambda - Chuan toi uu)
X1 a 0 0 0 clk y1 vdd 0 domino_or4_param PARAMS: W_k=0.6u
Cload1 y1 0 30fF

* 2. W = 1.2u (4 lambda)
X2 a 0 0 0 clk y2 vdd 0 domino_or4_param PARAMS: W_k=1.2u
Cload2 y2 0 30fF

* 3. W = 1.8u (6 lambda)
X3 a 0 0 0 clk y3 vdd 0 domino_or4_param PARAMS: W_k=1.8u
Cload3 y3 0 30fF

* 4. W = 2.4u (8 lambda - Qua co, gay tranh chap nang)
X4 a 0 0 0 clk y4 vdd 0 domino_or4_param PARAMS: W_k=2.4u
Cload4 y4 0 30fF

* Nguon kich thich
Vclk clk 0 PULSE(0 5.0 0 0.1n 0.1n 5n 10n)
Va a 0 PULSE(0 5.0 6n 0.1n 0.1n 4n 20n)

.tran 0.02n 12n

* Do tre Evaluate cho tung kich thuoc Keeper
.meas tran tpd_w06 TRIG V(a) VAL=2.5 RISE=1 TARG V(y1) VAL=2.5 RISE=1
.meas tran tpd_w12 TRIG V(a) VAL=2.5 RISE=1 TARG V(y2) VAL=2.5 RISE=1
.meas tran tpd_w18 TRIG V(a) VAL=2.5 RISE=1 TARG V(y3) VAL=2.5 RISE=1
.meas tran tpd_w24 TRIG V(a) VAL=2.5 RISE=1 TARG V(y4) VAL=2.5 RISE=1

.end
