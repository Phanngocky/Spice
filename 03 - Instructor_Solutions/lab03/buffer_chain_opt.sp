* INVERTER BUFFER CHAIN OPTIMIZATION SIMULATION
* Driving Heavy Load: CL = 1.0 pF (H = 50)
* So sanh: Direct Driver (1X) vs 3-Stage Optimal Buffer Chain (f_hat = 3.68)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuit INV_1X: Wn = 1.2u (4L), Wp = 3.6u (12L)
.subckt inv_1x in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in 0 0 N W=1.2u L=0.6u
.ends inv_1x

* Subcircuit INV_3_7X: Wn = 4.42u (~15L), Wp = 13.26u (~44L)
.subckt inv_3_7x in out vdd gnd
Mp out in vdd vdd P W=13.26u L=0.6u
Mn out in 0 0 N W=4.42u L=0.6u
.ends inv_3_7x

* Subcircuit INV_13_6X: Wn = 16.29u (~54L), Wp = 48.86u (~163L)
.subckt inv_13_6x in out vdd gnd
Mp out in vdd vdd P W=48.86u L=0.6u
Mn out in 0 0 N W=16.29u L=0.6u
.ends inv_13_6x

* ==============================================================
* KICH BAN A: LAI TRUC TIEP BANG 1 INVERTER DON (1X)
* ==============================================================
X_dir in out_direct vdd 0 inv_1x
CL_dir out_direct 0 1.0pF

* ==============================================================
* KICH BAN B: CHUOI DEM 3 TANG TOI UU (N = 3, f_hat = 3.68)
* ==============================================================
* Tang 1: 1.0X
X_st1 in net_st1 vdd 0 inv_1x
* Tang 2: 3.68X
X_st2 net_st1 net_st2 vdd 0 inv_3_7x
* Tang 3: 13.57X
X_st3 net_st2 out_chain vdd 0 inv_13_6x
* Tai nang CL = 1.0 pF
CL_chain out_chain 0 1.0pF

* Nguon tin hieu vao: Xung vuong 20MHz (Chu ky 50ns)
Vin in 0 PULSE(0 5.0 5n 0.1n 0.1n 25n 50n)

* Mo phong Transient 80ns
.tran 0.02n 80n

* DO TRE VA THOI GIAN SUON CHO KICH BAN A (LAI TRUC TIEP)
.meas tran tphl_dir TRIG v(in) VAL=2.5 RISE=1 TARG v(out_direct) VAL=2.5 FALL=1
.meas tran tplh_dir TRIG v(in) VAL=2.5 FALL=1 TARG v(out_direct) VAL=2.5 RISE=1
.meas tran tpd_dir PARAM='(tphl_dir + tplh_dir)/2'
.meas tran trise_dir TRIG v(out_direct) VAL=0.5 RISE=1 TARG v(out_direct) VAL=4.5 RISE=1
.meas tran tfall_dir TRIG v(out_direct) VAL=4.5 FALL=1 TARG v(out_direct) VAL=0.5 FALL=1

* DO TRE VA THOI GIAN SUON CHO KICH BAN B (CHUOI DEM 3 TANG)
* Chu y: 3 tang inverter la dao logic (in -> out_chain dao pha)
.meas tran tphl_chain TRIG v(in) VAL=2.5 RISE=1 TARG v(out_chain) VAL=2.5 FALL=1
.meas tran tplh_chain TRIG v(in) VAL=2.5 FALL=1 TARG v(out_chain) VAL=2.5 RISE=1
.meas tran tpd_chain PARAM='(tphl_chain + tplh_chain)/2'
.meas tran trise_chain TRIG v(out_chain) VAL=0.5 RISE=1 TARG v(out_chain) VAL=4.5 RISE=1
.meas tran tfall_chain TRIG v(out_chain) VAL=4.5 FALL=1 TARG v(out_chain) VAL=0.5 FALL=1

* TI SO CAI THIEN TOC DO
.meas tran speedup PARAM='tpd_dir / tpd_chain'

.control
run
plot v(in) v(out_direct) v(out_chain)
.endc

.end
