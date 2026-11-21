* LAB 07: DOMINO OR4 POST-LAYOUT PEX SIMULATION (PARASITIC EXTRACTED)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Mo ta: Netlist sau layout bao gom dien dung va dien tro ky sinh trich xuat tu Electric VLSI

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* ==============================================================
* POST-LAYOUT NETLIST: domino_or4_x1_pex
* ==============================================================
.subckt domino_or4_x1_pex a b c d clk y vdd gnd

* 1. Precharge PMOS
Mp_pre x_int clk_p vdd vdd P W=3.6u L=0.6u AS=5.4p AD=5.4p PS=10.2u PD=10.2u

* 2. Weak PMOS Keeper
M_kp x_int y_int vdd vdd P W=0.6u L=0.6u AS=1.08p AD=1.08p PS=4.2u PD=4.2u

* 3. Evaluate Foot NMOS
Mn_foot neval_int clk_n gnd gnd N W=2.4u L=0.6u AS=3.6p AD=3.6p PS=7.8u PD=7.8u

* 4. Mang PDN (4 NMOS song song voi khuếch tán chia sẻ)
Mn_a x_int a neval_int gnd N W=1.2u L=0.6u AS=1.8p AD=1.8p PS=5.4u PD=5.4u
Mn_b x_int b neval_int gnd N W=1.2u L=0.6u AS=1.8p AD=1.8p PS=5.4u PD=5.4u
Mn_c x_int c neval_int gnd N W=1.2u L=0.6u AS=1.8p AD=1.8p PS=5.4u PD=5.4u
Mn_d x_int d neval_int gnd N W=1.2u L=0.6u AS=1.8p AD=1.8p PS=5.4u PD=5.4u

* 5. Static Inverter
Mp_inv y_int x_int vdd vdd P W=4.8u L=0.6u AS=7.2p AD=7.2p PS=12.6u PD=12.6u
Mn_inv y_int x_int gnd gnd N W=2.4u L=0.6u AS=3.6p AD=3.6p PS=7.8u PD=7.8u

* 6. Mang dien dung va dien tro ky sinh Metal1/Poly interconnect (PEX)
R_x x_int x 15.0
C_x_pex x 0 28.5fF

R_neval neval_int neval 10.0
C_neval_pex neval 0 16.2fF

R_clk_p clk clk_p 8.0
R_clk_n clk clk_n 6.0
C_clk_pex clk 0 12.0fF

R_y y_int y 12.0
C_y_pex y 0 18.0fF

.ends domino_or4_x1_pex

* ==============================================================
* TESTBENCH PEX
* ==============================================================
X_dut a b c d clk y vdd 0 domino_or4_x1_pex
Cload y 0 30fF

* Nguon tin hieu
Vclk clk 0 PULSE(0 5.0 0 0.1n 0.1n 5n 10n)
Va a 0 PULSE(0 5.0 6n 0.1n 0.1n 4n 20n)
Vb b 0 DC 0.0
Vc c 0 DC 0.0
Vd d 0 DC 0.0

.tran 0.02n 15n

* Do tre Evaluate Post-layout (PEX)
.meas tran tpd_pex_eval TRIG V(a) VAL=2.5 RISE=1 TARG V(y) VAL=2.5 RISE=1

* Dien ap nut dong X trong evaluate
.meas tran vx_min MIN V(X_dut.x) FROM=5n TO=10n

.end
