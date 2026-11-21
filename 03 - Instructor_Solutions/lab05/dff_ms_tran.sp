* MASTER-SLAVE POSITIVE EDGE-TRIGGERED D-FLIP-FLOP (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Kien truc: Master Latch (CLK=0) + Slave Latch (CLK=1)

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

.subckt inv_weak in out vdd gnd
Mp out in vdd vdd P W=1.2u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_weak

.subckt dlatch_x1 d clk clk_n q vdd gnd
X_tg1 d x clk clk_n vdd gnd tg_gate
X_i1 x q_n vdd gnd inv_std
X_i2 q_n q vdd gnd inv_std
X_i3 q_n fb vdd gnd inv_weak
X_tg2 fb x clk_n clk vdd gnd tg_gate
.ends dlatch_x1

* Subcircuit DFF_MS_X1: d clk q vdd gnd
.subckt dff_ms_x1 d clk q vdd gnd
* Inverter tao clk_b
X_clk_inv clk clk_b vdd gnd inv_std

* Master Latch: Tich cuc khi CLK = 0 (clk nhan clk_b, clk_n nhan clk)
X_master d clk_b clk qm vdd gnd dlatch_x1

* Slave Latch: Tich cuc khi CLK = 1 (clk nhan clk, clk_n nhan clk_b)
X_slave qm clk clk_b q vdd gnd dlatch_x1
.ends dff_ms_x1

* Goi Instance DFF
X_dff d clk q vdd 0 dff_ms_x1
CL q 0 50fF

* Nguon xung nhap
* clk: Xung 50MHz (Chu ky 20ns, sườn lên tại 10ns, 30ns, 50ns, 70ns)
Vclk clk 0 PULSE(0 5.0 0 0.1n 0.1n 10n 20n)

* d: Tin hieu du lieu thay doi truoc suon len CLK
* Chuyen 0 -> 1 luc t = 7ns (truoc suon 10ns dung 3ns -> thoa setup time)
* Chuyen 1 -> 0 luc t = 26ns (truoc suon 30ns dung 4ns)
Vd d 0 PULSE(0 5.0 7n 0.1n 0.1n 19n 40n)

* Mo phong Transient 80ns
.tran 0.02n 80n

* DO TRE CLOCK-TO-Q TAI SUON LEN THU 1 (t = 10ns: D=1 -> Q nhay len 1)
.meas tran t_cq_LH TRIG v(clk) VAL=2.5 RISE=1 TARG v(q) VAL=2.5 RISE=1

* DO TRE CLOCK-TO-Q TAI SUON LEN THU 2 (t = 30ns: D=0 -> Q nhay xuong 0)
.meas tran t_cq_HL TRIG v(clk) VAL=2.5 RISE=2 TARG v(q) VAL=2.5 FALL=1

* TRE TRUNG BINH T_CQ
.meas tran t_cq_avg PARAM='(t_cq_LH + t_cq_HL)/2'

.control
run
plot v(clk)+10 v(d)+5 v(q)
.endc

.end
