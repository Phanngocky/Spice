* 4-BIT RIPPLE CARRY ADDER CASCADING SIMULATION (.TRAN)
* Kich thich: Truong hop xau nhat Carry lan truyen tu Cin0 -> Cout3
* A = [1 1 1 1], B = [0 0 0 0], Cin0 chuyen 0 -> 1

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuits
.subckt inv_std in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_std

.subckt mirror_adder_1b a b cin sum cout vdd gnd
* PDN Carry
Mn_ca1 cout_b a n_ca1 gnd N W=2.4u L=0.6u
Mn_cb1 n_ca1  b gnd   gnd N W=2.4u L=0.6u
Mn_ccin cout_b cin n_ca2 gnd N W=2.4u L=0.6u
Mn_ca2  n_ca2  a   gnd   gnd N W=2.4u L=0.6u
Mn_cb2  n_ca2  b   gnd   gnd N W=2.4u L=0.6u
* PUN Carry
Mp_ca1 p_ca1 a vdd vdd P W=7.2u L=0.6u
Mp_cb1 p_ca1 b vdd vdd P W=7.2u L=0.6u
Mp_ccin cout_b cin p_ca1 vdd P W=7.2u L=0.6u
Mp_ca2 p_ca2 a vdd   vdd P W=7.2u L=0.6u
Mp_cb2 cout_b b p_ca2 vdd P W=7.2u L=0.6u
X_inv_cout cout_b cout vdd gnd inv_std

* PDN Sum
Mn_sa1 sum_b a n_sa1 gnd N W=3.6u L=0.6u
Mn_sb1 n_sa1 b n_sa2 gnd N W=3.6u L=0.6u
Mn_sc1 n_sa2 cin gnd gnd N W=3.6u L=0.6u
Mn_scout sum_b cout_b n_sa3 gnd N W=2.4u L=0.6u
Mn_sa2   n_sa3 a      gnd   gnd N W=2.4u L=0.6u
Mn_sb2   n_sa3 b      gnd   gnd N W=2.4u L=0.6u
Mn_sc2   n_sa3 cin    gnd   gnd N W=2.4u L=0.6u
* PUN Sum
Mp_sa1 p_sa1 a vdd vdd P W=10.8u L=0.6u
Mp_sb1 p_sa2 b p_sa1 vdd P W=10.8u L=0.6u
Mp_sc1 sum_b cin p_sa2 vdd P W=10.8u L=0.6u
Mp_sa2 p_sa3 a vdd vdd P W=7.2u L=0.6u
Mp_sb2 p_sa3 b vdd vdd P W=7.2u L=0.6u
Mp_sc2 p_sa3 cin vdd vdd P W=7.2u L=0.6u
Mp_scout sum_b cout_b p_sa3 vdd P W=7.2u L=0.6u
X_inv_sum sum_b sum vdd gnd inv_std
.ends mirror_adder_1b

* Chuoi 4-bit Ripple Carry Adder
* Bit 0
X_fa0 a0 b0 cin0 s0 c1 vdd 0 mirror_adder_1b
* Bit 1
X_fa1 a1 b1 c1   s1 c2 vdd 0 mirror_adder_1b
* Bit 2
X_fa2 a2 b2 c2   s2 c3 vdd 0 mirror_adder_1b
* Bit 3
X_fa3 a3 b3 c3   s3 cout3 vdd 0 mirror_adder_1b

* Tai ngo ra
CL0 s0 0 20fF
CL1 s1 0 20fF
CL2 s2 0 20fF
CL3 s3 0 20fF
CL_c3 cout3 0 50fF

* Nguon du lieu: A = 1111, B = 0000
Va0 a0 0 DC 5.0
Va1 a1 0 DC 5.0
Va2 a2 0 DC 5.0
Va3 a3 0 DC 5.0

Vb0 b0 0 DC 0.0
Vb1 b1 0 DC 0.0
Vb2 b2 0 DC 0.0
Vb3 b3 0 DC 0.0

* Nguon xung Carry ngõ vào: Cin0 nhảy 0 -> 1 tại t = 5ns
Vcin0 cin0 0 PULSE(0 5.0 5n 0.1n 0.1n 15n 30n)

.tran 0.01n 30n

* Do tre lan truyen tung tang Carry
.meas tran t_c1 TRIG v(cin0) VAL=2.5 RISE=1 TARG v(c1) VAL=2.5 RISE=1
.meas tran t_c2 TRIG v(cin0) VAL=2.5 RISE=1 TARG v(c2) VAL=2.5 RISE=1
.meas tran t_c3 TRIG v(cin0) VAL=2.5 RISE=1 TARG v(c3) VAL=2.5 RISE=1
.meas tran t_cout3 TRIG v(cin0) VAL=2.5 RISE=1 TARG v(cout3) VAL=2.5 RISE=1

* Do tre trung binh moi tang
.meas tran t_per_stage PARAM='t_cout3 / 4'

.end
