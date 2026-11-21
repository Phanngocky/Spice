* SETUP AND HOLD TIME CHARACTERIZATION (.TRAN SWEEP)
* Kich ban quet thoi gian tre delta_t = t_clk - t_data
* Xac dinh diem gay trê 10% (10% Push-out Knee) theo chuan cong nghiep

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

.subckt dff_ms_x1 d clk q vdd gnd
X_clk_inv clk clk_b vdd gnd inv_std
X_master d clk_b clk qm vdd gnd dlatch_x1
X_slave qm clk clk_b q vdd gnd dlatch_x1
.ends dff_ms_x1

* Goi DFF
X_dff d clk q vdd 0 dff_ms_x1
CL q 0 50fF

* Suon len CLK co dinh tai t = 10.0ns
Vclk clk 0 PULSE(0 5.0 10n 0.1n 0.1n 10n 25n)

* Tham so thoi diem du lieu D chuyen 0 -> 1: t_data = 10n - delta_t
* Quet delta_t tu 0.5ns (500ps - rat thoa) xuong 0.04ns (40ps - sap vi pham)
.param delta_t = 0.3n
Vd d 0 PULSE(0 5.0 '10n - delta_t' 0.1n 0.1n 10n 25n)

.step param delta_t LIST 0.5n 0.3n 0.2n 0.15n 0.12n 0.10n 0.08n 0.07n 0.06n

.tran 0.005n 15n

* Do t_cq theo tung gia tri delta_t
.meas tran t_cq TRIG v(clk) VAL=2.5 RISE=1 TARG v(q) VAL=2.5 RISE=1

.end
