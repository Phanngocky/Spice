* DFF_MS_X1 POST-LAYOUT PARASITIC EXTRACTION (PEX) SIMULATION
* Trich xuat tu Electric Mask Layout: dff_ms_x1{lay}
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Subcircuit DFF Post-Layout kem tu ky sinh
.subckt dff_ms_pex d clk q vdd gnd
* Inverter CLK tao clk_b
Mp_clk clk_b clk vdd vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_clk clk_b clk gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* Master Latch Components
* TG_M1 (d -> xm)
Mn_tm1 d clk_b xm gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u
Mp_tm1 d clk   xm vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u

* I_M1 (xm -> qm_n)
Mp_im1 qm_n xm vdd vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_im1 qm_n xm gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* I_M2 (qm_n -> qm)
Mp_im2 qm qm_n vdd vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_im2 qm qm_n gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* I_M3 (Weak Feedback: qm_n -> fb_m)
Mp_im3 fb_m qm_n vdd vdd P W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u
Mn_im3 fb_m qm_n gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* TG_M2 (fb_m -> xm)
Mn_tm2 fb_m clk   xm gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u
Mp_tm2 fb_m clk_b xm vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u

* Slave Latch Components
* TG_S1 (qm -> xs)
Mn_ts1 qm clk   xs gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u
Mp_ts1 qm clk_b xs vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u

* I_S1 (xs -> qs_n)
Mp_is1 qs_n xs vdd vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_is1 qs_n xs gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* I_S2 (qs_n -> q)
Mp_is2 q qs_n vdd vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u
Mn_is2 q qs_n gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* I_S3 (Weak Feedback: qs_n -> fb_s)
Mp_is3 fb_s qs_n vdd vdd P W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u
Mn_is3 fb_s qs_n gnd gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u

* TG_S2 (fb_s -> xs)
Mn_ts2 fb_s clk_b xs gnd N W=1.2u L=0.6u AS=2.59p PS=6.72u AD=2.59p PD=6.72u
Mp_ts2 fb_s clk   xs vdd P W=3.6u L=0.6u AS=7.77p PS=11.52u AD=7.77p PD=11.52u

* Dien dung ky sinh nut noi trích xuat (Parasitic Capacitances)
Cpar_clkb clk_b 0 16.5fF
Cpar_xm   xm    0 14.2fF
Cpar_qm   qm    0 18.6fF
Cpar_xs   xs    0 14.2fF
Cpar_q    q     0 22.4fF
.ends dff_ms_pex

* Goi Instance
X_pex d clk q vdd 0 dff_ms_pex
CL q 0 50fF

* Nguon kich thich
Vclk clk 0 PULSE(0 5.0 0 0.1n 0.1n 10n 20n)
Vd   d   0 PULSE(0 5.0 7n 0.1n 0.1n 19n 40n)

.tran 0.02n 60n

.meas tran t_cq_pex TRIG v(clk) VAL=2.5 RISE=1 TARG v(q) VAL=2.5 RISE=1

.end
