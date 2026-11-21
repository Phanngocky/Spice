* HIERARCHICAL 4:1 MULTIPLEXER (MUX4_TG) VERIFICATION (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Kien truc: Cay phan cap 3 x MUX2_TG = 18 Transistors

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuits
.subckt tg_gate in out en en_n vdd gnd
Mn in en out gnd N W=1.2u L=0.6u
Mp in en_n out vdd P W=3.6u L=0.6u
.ends tg_gate

.subckt inv_x1 in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_x1

.subckt mux2_tg d0 d1 s y vdd gnd
X_inv s s_n vdd gnd inv_x1
X_tg0 d0 y s_n s vdd gnd tg_gate
X_tg1 d1 y s s_n vdd gnd tg_gate
.ends mux2_tg

* Subcircuit MUX4_TG
.subckt mux4_tg d0 d1 d2 d3 s0 s1 y vdd gnd
* Tang 1: 2 MUX2 dieu khien boi s0
X_m01 d0 d1 s0 y01 vdd gnd mux2_tg
X_m23 d2 d3 s0 y23 vdd gnd mux2_tg
* Tang 2: 1 MUX2 dieu khien boi s1
X_top y01 y23 s1 y vdd gnd mux2_tg
.ends mux4_tg

* Goi Instance MUX4_TG
X4 d0 d1 d2 d3 s0 s1 y vdd 0 mux4_tg
CL y 0 50fF

* Nguon du lieu
Vd0 d0 0 DC 0.0
Vd1 d1 0 DC 5.0
Vd2 d2 0 DC 0.0
Vd3 d3 0 DC 5.0

* Nguon tin hieu chon (s1 s0 quet 00 -> 01 -> 10 -> 11)
* s0: Xung chu ky 20ns
Vs0 s0 0 PULSE(0 5.0 0 0.1n 0.1n 10n 20n)
* s1: Xung chu ky 40ns
Vs1 s1 0 PULSE(0 5.0 0 0.1n 0.1n 20n 40n)

* Mo phong 80ns
.tran 0.05n 80n

* Kiem chung gia tri dien ap ra tai 4 trang thai chon
.meas tran v_s00 AVG v(y) FROM=2n TO=8n
.meas tran v_s01 AVG v(y) FROM=12n TO=18n
.meas tran v_s10 AVG v(y) FROM=22n TO=28n
.meas tran v_s11 AVG v(y) FROM=32n TO=38n

.control
run
plot v(s1)+10 v(s0)+5 v(y)
.endc

.end
