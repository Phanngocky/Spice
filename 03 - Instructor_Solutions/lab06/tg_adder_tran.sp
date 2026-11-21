* 16-TRANSISTOR TRANSMISSION GATE FULL ADDER VERIFICATION (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* P = A xor B, Sum = P xor Cin, Cout = MUX(Cin, A, sel=P)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuits
.subckt tg_gate in out en en_n vdd gnd
Mn in en out gnd N W=1.2u L=0.6u
Mp in en_n out vdd P W=3.6u L=0.6u
.ends tg_gate

.subckt inv_std in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_std

* Cổng XOR Cổng truyền: in1 in2 out
.subckt xor_tg a b out vdd gnd
X_inv_b b b_n vdd gnd inv_std
* Khi B=0: out = A (qua TG1)
X_tg1 a out b_n b vdd gnd tg_gate
* Khi B=1: out = !A
X_inv_a a a_n vdd gnd inv_std
X_tg2 a_n out b b_n vdd gnd tg_gate
.ends xor_tg

* Subcircuit 16T TG Full Adder
.subckt tg_adder_1b a b cin sum cout vdd gnd
* Khoi 1: P = A xor B
X_xor1 a b p vdd gnd xor_tg
X_inv_p p p_n vdd gnd inv_std

* Khoi 2: Sum = P xor Cin
X_xor2 p cin sum vdd gnd xor_tg

* Khoi 3: Cout = MUX(Cin, A, sel=P)
* Khi P=1: Cout = Cin (qua TG_C1)
X_tg_c1 cin cout p p_n vdd gnd tg_gate
* Khi P=0: Cout = A (qua TG_C2)
X_tg_c2 a cout p_n p vdd gnd tg_gate
.ends tg_adder_1b

* Goi Instance TG Adder
X_tg_fa a b cin sum cout vdd 0 tg_adder_1b
CL_sum sum 0 50fF
CL_cout cout 0 50fF

* Nguon kich thich 8 to hop
Va   a   0 PULSE(0 5.0 0 0.1n 0.1n 40n 80n)
Vb   b   0 PULSE(0 5.0 0 0.1n 0.1n 20n 40n)
Vcin cin 0 PULSE(0 5.0 0 0.1n 0.1n 10n 20n)

.tran 0.05n 80n

* Do tre Cin -> Cout qua TG MUX
.meas tran t_cin_cout_tg TRIG v(cin) VAL=2.5 RISE=2 TARG v(cout) VAL=2.5 RISE=1

.end
