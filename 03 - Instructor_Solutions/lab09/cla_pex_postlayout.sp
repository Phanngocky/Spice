* LAB 09: 4-BIT CARRY LOOKAHEAD ADDER (CLA) POST-LAYOUT PEX SIMULATION
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Mo ta: Netlist sau layout bao gom dien dung va dien tro ky sinh Metal1/Metal2 giua cac khoi PG, CLG va Sum

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Goi netlist cla_adder_4b
.include "cla_4bit_tran.sp"

* Subcircuit PEX bao gom kenh dinh tuyen ky sinh
.subckt cla_adder_4b_pex a0 a1 a2 a3 b0 b1 b2 b3 c0 s0 s1 s2 s3 c4 vdd gnd

* Loi loi CLA
X_core a0 a1 a2 a3 b0 b1 b2 b3 c0_int s0_int s1_int s2_int s3_int c4_int vdd gnd cla_adder_4b

* Dien tro va dien dung ky sinh duong Carry Cin
R_c0 c0 c0_int 15.0
C_c0_pex c0 0 25.0fF

* Dien tro va dien dung ky sinh duong Cout C4
R_c4 c4_int c4 18.0
C_c4_pex c4 0 45.0fF

* Dien tro va dien dung ky sinh cac ngo ra Sum
R_s0 s0_int s0 12.0
C_s0_pex s0 0 20.0fF

R_s1 s1_int s1 12.0
C_s1_pex s1 0 20.0fF

R_s2 s2_int s2 12.0
C_s2_pex s2 0 20.0fF

R_s3 s3_int s3 12.0
C_s3_pex s3 0 22.0fF

.ends cla_adder_4b_pex

* ==============================================================
* TESTBENCH PEX
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

X_dut a0 a1 a2 a3 b0 b1 b2 b3 c0 s0 s1 s2 s3 c4 vdd 0 cla_adder_4b_pex

Cs0 s0 0 30fF
Cs1 s1 0 30fF
Cs2 s2 0 30fF
Cs3 s3 0 30fF
Cc4 c4 0 50fF

.tran 0.02n 15n

* Do tre Carry C0 -> C4 Post-layout PEX
.meas tran tpd_c0_c4_pex TRIG V(c0) VAL=2.5 RISE=1 TARG V(c4) VAL=2.5 RISE=1

* Do tre Sum S3 Post-layout PEX
.meas tran tpd_c0_s3_pex TRIG V(c0) VAL=2.5 RISE=1 TARG V(s3) VAL=2.5 FALL=1

.end
