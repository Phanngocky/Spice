* 28-TRANSISTOR MIRROR ADDER VERIFICATION (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Ham logic: Sum = A xor B xor Cin, Cout = AB + Cin(A + B)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuit inv_std (INV_X1)
.subckt inv_std in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_std

* Subcircuit mirror_adder_1b: a b cin sum cout vdd gnd
.subckt mirror_adder_1b a b cin sum cout vdd gnd

* ==============================================================
* KHOI CARRY: Tao cout_b tu A, B, Cin (8 Transistors)
* cout_b = !(AB + Cin(A + B))
* ==============================================================
* PDN Khối Carry:
* Nhanh 1: A noi tiep B
Mn_ca1 cout_b a n_ca1 gnd N W=2.4u L=0.6u
Mn_cb1 n_ca1  b gnd   gnd N W=2.4u L=0.6u
* Nhanh 2: Cin noi tiep (A // B)
Mn_ccin cout_b cin n_ca2 gnd N W=2.4u L=0.6u
Mn_ca2  n_ca2  a   gnd   gnd N W=2.4u L=0.6u
Mn_cb2  n_ca2  b   gnd   gnd N W=2.4u L=0.6u

* PUN Khối Carry (Doi xung guong):
* Nhanh 1: A // B
Mp_ca1 p_ca1 a vdd vdd P W=7.2u L=0.6u
Mp_cb1 p_ca1 b vdd vdd P W=7.2u L=0.6u
Mp_ccin cout_b cin p_ca1 vdd P W=7.2u L=0.6u
* Nhanh 2: A noi tiep B
Mp_ca2 p_ca2 a vdd   vdd P W=7.2u L=0.6u
Mp_cb2 cout_b b p_ca2 vdd P W=7.2u L=0.6u

* Inverter tao Cout
X_inv_cout cout_b cout vdd gnd inv_std

* ==============================================================
* KHOI SUM: Tao sum_b tu A, B, Cin va cout_b (12 Transistors)
* sum_b = ABCin + cout_b(A + B + Cin)
* ==============================================================
* PDN Khối Sum:
* Nhanh 1: A noi tiep B noi tiep Cin
Mn_sa1 sum_b a n_sa1 gnd N W=3.6u L=0.6u
Mn_sb1 n_sa1 b n_sa2 gnd N W=3.6u L=0.6u
Mn_sc1 n_sa2 cin gnd gnd N W=3.6u L=0.6u
* Nhanh 2: cout_b noi tiep (A // B // Cin)
Mn_scout sum_b cout_b n_sa3 gnd N W=2.4u L=0.6u
Mn_sa2   n_sa3 a      gnd   gnd N W=2.4u L=0.6u
Mn_sb2   n_sa3 b      gnd   gnd N W=2.4u L=0.6u
Mn_sc2   n_sa3 cin    gnd   gnd N W=2.4u L=0.6u

* PUN Khối Sum (Doi xung guong):
* Nhanh 1: A noi tiep B noi tiep Cin
Mp_sa1 p_sa1 a vdd vdd P W=10.8u L=0.6u
Mp_sb1 p_sa2 b p_sa1 vdd P W=10.8u L=0.6u
Mp_sc1 sum_b cin p_sa2 vdd P W=10.8u L=0.6u
* Nhanh 2: cout_b noi tiep (A // B // Cin)
Mp_sa2 p_sa3 a vdd vdd P W=7.2u L=0.6u
Mp_sb2 p_sa3 b vdd vdd P W=7.2u L=0.6u
Mp_sc2 p_sa3 cin vdd vdd P W=7.2u L=0.6u
Mp_scout sum_b cout_b p_sa3 vdd P W=7.2u L=0.6u

* Inverter tao Sum
X_inv_sum sum_b sum vdd gnd inv_std

.ends mirror_adder_1b

* Goi Instance Mirror Adder
X_fa a b cin sum cout vdd 0 mirror_adder_1b
CL_sum sum 0 50fF
CL_cout cout 0 50fF

* Nguon kich thich quet toan bo 8 to hop (000 den 111)
* Va chu ky 80ns, Vb chu ky 40ns, Vcin chu ky 20ns
Va   a   0 PULSE(0 5.0 0 0.1n 0.1n 40n 80n)
Vb   b   0 PULSE(0 5.0 0 0.1n 0.1n 20n 40n)
Vcin cin 0 PULSE(0 5.0 0 0.1n 0.1n 10n 20n)

* Mo phong Transient 80ns
.tran 0.05n 80n

* DO TRE DUONG CARRY TAI THOI DIEM Cin NHAY 0 -> 1 (t = 20ns, A=0, B=1 -> P=1, Cout nhay len 1)
.meas tran t_cin_cout_LH TRIG v(cin) VAL=2.5 RISE=2 TARG v(cout) VAL=2.5 RISE=1
.meas tran t_cin_cout_HL TRIG v(cin) VAL=2.5 FALL=2 TARG v(cout) VAL=2.5 FALL=1
.meas tran t_cin_cout_avg PARAM='(t_cin_cout_LH + t_cin_cout_HL)/2'

* DO TRE DUONG SUM TAI THOI DIEM A NHAY 0 -> 1 (t = 40ns)
.meas tran t_a_sum_LH TRIG v(a) VAL=2.5 RISE=1 TARG v(sum) VAL=2.5 CROSS=1

.control
run
plot v(a)+15 v(b)+10 v(cin)+5 v(sum) v(cout)-5
.endc

.end
