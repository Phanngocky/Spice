* LAB 10: 4-BIT REGISTERED ALU CHIP-LEVEL POST-LAYOUT PEX SIMULATION
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Mo ta: Mo phong cap chip voi Vong cap nguon (Power Ring VDD/GND), sut ap IR-Drop
*       va mang ky sinh Metal1/Metal2 giua cac khoi CLA4, Logic, MUX4 va DFF

.include "../../04 - Models_and_Libraries/C5_models.txt"

* Nguon cap cap chip
Vdd_pad vdd_pad 0 DC 5.0
Vgnd_pad gnd_pad 0 DC 0.0

* ==============================================================
* MO HINH VONG CAP NGUON POWER RING & IR-DROP
* ==============================================================
* Dien tro vong nguon VDD (Metal 2/Metal 1 kep xung quanh chip)
R_ring_vdd1 vdd_pad vdd_core 0.8
C_ring_vdd  vdd_core 0 150fF

* Dien tro vong dat GND
R_ring_gnd1 gnd_pad gnd_core 0.6
C_ring_gnd  gnd_core 0 120fF

* Goi Subcircuit alu_4b_reg tu alu_4bit_top_tran.sp
.include "alu_4bit_top_tran.sp"

* Subcircuit Cap Chip voi kenh dinh tuyen PEX
.subckt alu_4b_reg_pex a0 a1 a2 a3 b0 b1 b2 b3 cin op0 op1 clk
+ out0 out1 out2 out3 cout_flag z_flag vdd gnd

* Loi vi mach Core
X_core a0_i a1_i a2_i a3_i b0_i b1_i b2_i b3_i cin_i op0_i op1_i clk_i
+ out0_i out1_i out2_i out3_i cout_i z_i vdd gnd alu_4b_reg

* Ky sinh duong vao A, B, OP, CLK
R_a0 a0 a0_i 10.0
C_a0 a0 0 25fF
R_b0 b0 b0_i 10.0
C_b0 b0 0 25fF
R_clk clk clk_i 8.0
C_clk clk 0 35fF

R_op0 op0 op0_i 12.0
R_op1 op1 op1_i 12.0
R_cin cin cin_i 10.0

* Nối thẳng các ngõ vào còn lại
R_a1 a1 a1_i 10.0
R_a2 a2 a2_i 10.0
R_a3 a3 a3_i 10.0
R_b1 b1 b1_i 10.0
R_b2 b2 b2_i 10.0
R_b3 b3 b3_i 10.0

* Ky sinh ngo ra
R_o0 out0_i out0 15.0
C_o0 out0 0 30fF
R_o1 out1_i out1 15.0
C_o1 out1 0 30fF
R_o2 out2_i out2 15.0
C_o2 out2 0 30fF
R_o3 out3_i out3 15.0
C_o3 out3 0 30fF
R_zf z_i z_flag 12.0
R_cf cout_i cout_flag 12.0

.ends alu_4b_reg_pex

* ==============================================================
* TESTBENCH PEX CHIP LEVEL (Xung nhip 500 MHz, T = 2.0ns)
* ==============================================================
Vclk clk 0 PULSE(0 5.0 1.0n 0.1n 0.1n 0.9n 2.0n)
Vcin cin 0 DC 0.0

* ADD: 5 + 3 = 8
Va0 a0 0 DC 5.0
Va1 a1 0 DC 0.0
Va2 a2 0 DC 5.0
Va3 a3 0 DC 0.0

Vb0 b0 0 DC 5.0
Vb1 b1 0 DC 5.0
Vb2 b2 0 DC 0.0
Vb3 b3 0 DC 0.0

Vop0 op0 0 DC 0.0
Vop1 op1 0 DC 0.0

X_chip a0 a1 a2 a3 b0 b1 b2 b3 cin op0 op1 clk
+ out0 out1 out2 out3 cout_flag z_flag vdd_core gnd_core alu_4b_reg_pex

.tran 0.02n 6.0n

* Do tre Clock-to-Q sau Layout PEX
.meas tran t_cq_pex TRIG V(clk) VAL=2.5 RISE=1 TARG V(out3) VAL=2.5 RISE=1

* Do sut ap cuc dai tren Vong cap nguon VDD (IR Drop)
.meas tran ir_drop_max MAX (V(vdd_pad) - V(vdd_core))

.end
