* LAB 10: ALUFMAX TIMING SWEEP & SETUP TIME MARGIN VERIFICATION
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Muc tieu: Xac dinh tan so xung nhip toi da f_max cua Registered ALU 4-bit

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Include toàn bộ netlist alu_4b_reg từ alu_4bit_top_tran.sp
.include "alu_4bit_top_tran.sp"

* Testbench kiểm tra đường tới hạn dài nhất (A -> CLA -> MUX -> DFF)
* ADD: A = 1111 (15), B = 0000 (0), Cin = 1 -> Sum = 0000, Cout = 1
Va0 a0 0 DC 5.0
Va1 a1 0 DC 5.0
Va2 a2 0 DC 5.0
Va3 a3 0 DC 5.0

Vb0 b0 0 DC 0.0
Vb1 b1 0 DC 0.0
Vb2 b2 0 DC 0.0
Vb3 b3 0 DC 0.0

Vcin cin 0 DC 5.0
Vop0 op0 0 DC 0.0
Vop1 op1 0 DC 0.0

* Xung nhịp quét ở tần số cao f = 1.0 GHz (T = 1.0ns)
Vclk clk 0 PULSE(0 5.0 0.5n 0.05n 0.05n 0.45n 1.0n)

X_dut a0 a1 a2 a3 b0 b1 b2 b3 cin op0 op1 clk
+ out0 out1 out2 out3 cout_flag z_flag vdd 0 alu_4b_reg

C_out0 out0 0 30fF
C_out1 out1 0 30fF
C_out2 out2 0 30fF
C_out3 out3 0 30fF

.tran 0.01n 4.0n

* Đo thời gian trễ chốt ngõ ra ở xung nhịp 1.0 GHz
.meas tran t_cq_f1ghz TRIG V(clk) VAL=2.5 RISE=2 TARG V(out3) VAL=2.5 FALL=1

* Kiểm chứng cờ Zero đã chốt mức cao (Z = 1)
.meas tran z_level FIND V(z_flag) AT=2.8n

.end
