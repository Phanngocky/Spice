* D-LATCH LEVEL-SENSITIVE VERIFICATION (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Kien truc: TG-based D-Latch (Active High CLK = 1)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuit tg_gate: in out en en_n vdd gnd
.subckt tg_gate in out en en_n vdd gnd
Mn in en out gnd N W=1.2u L=0.6u
Mp in en_n out vdd P W=3.6u L=0.6u
.ends tg_gate

* Subcircuit inv_std: in out vdd gnd (INV_X1)
.subckt inv_std in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_std

* Subcircuit inv_weak: in out vdd gnd (Weak Inverter for Feedback)
.subckt inv_weak in out vdd gnd
Mp out in vdd vdd P W=1.2u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_weak

* Subcircuit dlatch_x1: d clk clk_n q vdd gnd
.subckt dlatch_x1 d clk clk_n q vdd gnd
* Cong truyen ngo vao TG1 (dan khi clk=1)
X_tg1 d x clk clk_n vdd gnd tg_gate
* Inverter I1 tao q_n tu nut x
X_i1 x q_n vdd gnd inv_std
* Inverter I2 dem ngo ra q
X_i2 q_n q vdd gnd inv_std
* Inverter phan hoi I3
X_i3 q_n fb vdd gnd inv_weak
* Cong truyen phan hoi TG2 (dan khi clk=0)
X_tg2 fb x clk_n clk vdd gnd tg_gate
.ends dlatch_x1

* Goi Instance D-Latch
X_latch d clk clk_n q vdd 0 dlatch_x1
CL q 0 50fF

* Nguon xung nhap
* clk: Xung 25MHz (T = 40ns: 20ns cao, 20ns thap)
Vclk clk 0 PULSE(0 5.0 0 0.1n 0.1n 20n 40n)
* clk_n: Dao pha cua clk
Vclk_n clk_n 0 PULSE(5.0 0 0 0.1n 0.1n 20n 40n)

* d: Tin hieu du lieu thay doi luc CLK=1 (kiem tra trong suot) va luc CLK=0 (kiem tra chot)
Vd d 0 PULSE(0 5.0 5n 0.1n 0.1n 30n 60n)

* Mo phong Transient 120ns
.tran 0.05n 120n

* DO TRE TRUYEN LAN KHI TRONG SUOT (CLK = 1, t = 5ns -> 15ns)
.meas tran tphl_dq TRIG v(d) VAL=2.5 FALL=1 TARG v(q) VAL=2.5 FALL=1
.meas tran tplh_dq TRIG v(d) VAL=2.5 RISE=1 TARG v(q) VAL=2.5 RISE=1
.meas tran tpd_dq PARAM='(tphl_dq + tplh_dq)/2'

.control
run
plot v(clk)+10 v(d)+5 v(q)
.endc

.end
