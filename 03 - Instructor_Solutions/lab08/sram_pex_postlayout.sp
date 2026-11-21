* LAB 08: 6T SRAM CELL POST-LAYOUT PEX SIMULATION (PARASITIC EXTRACTED)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Mo ta: Netlist sau layout chua dien dung va dien tro ky sinh trich xuat tu Electric VLSI

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* ==============================================================
* POST-LAYOUT NETLIST: sram_6t_cell_pex
* ==============================================================
.subckt sram_6t_cell_pex wl bl blb q qb vdd gnd

* 1. Load PMOS M_L1 va M_L2
Mp_l1 q_int qb_int vdd vdd P W=0.6u L=0.6u AS=1.08p AD=1.08p PS=4.2u PD=4.2u
Mp_l2 qb_int q_int vdd vdd P W=0.6u L=0.6u AS=1.08p AD=1.08p PS=4.2u PD=4.2u

* 2. Driver NMOS M_D1 va M_D2
Mn_d1 q_int qb_int gnd gnd N W=2.4u L=0.6u AS=3.6p AD=3.6p PS=7.8u PD=7.8u
Mn_d2 qb_int q_int gnd gnd N W=2.4u L=0.6u AS=3.6p AD=3.6p PS=7.8u PD=7.8u

* 3. Access NMOS M_AX1 va M_AX2
Mn_ax1 bl_int  wl_int q_int  gnd N W=1.2u L=0.6u AS=1.8p AD=1.8p PS=5.4u PD=5.4u
Mn_ax2 blb_int wl_int qb_int gnd N W=1.2u L=0.6u AS=1.8p AD=1.8p PS=5.4u PD=5.4u

* 4. Mang ky sinh PEX (Dien tro va Dien dung noi bo)
R_q  q_int  q  12.0
C_q_pex q 0 16.5fF

R_qb qb_int qb 12.0
C_qb_pex qb 0 16.5fF

R_wl wl wl_int 15.0
C_wl_pex wl 0 14.0fF

R_bl bl bl_int 8.0
R_blb blb blb_int 8.0

.ends sram_6t_cell_pex

* ==============================================================
* TESTBENCH PEX
* ==============================================================
X_cell_pex wl bl blb q qb vdd 0 sram_6t_cell_pex

* Tai bitline
C_bl  bl  0 250fF
C_blb blb 0 250fF

* Nguon kich thich (Write 1 tai 12ns, Read 1 tai 22ns, Write 0 tai 32ns, Read 0 tai 42ns)
Vwl wl 0 PWL(
+ 0ns 0V   11.9ns 0V  12.0ns 5V  16.0ns 5V  16.1ns 0V
+ 21.9ns 0V 22.0ns 5V  26.0ns 5V  26.1ns 0V
+ 31.9ns 0V 32.0ns 5V  36.0ns 5V  36.1ns 0V
+ 41.9ns 0V 42.0ns 5V  46.0ns 5V  46.1ns 0V 50ns 0V)

Vbl_drv bl_in 0 PWL(
+ 0ns 5V   10ns 5V    16.5ns 5V
+ 20ns 5V  26.5ns 5V
+ 30ns 0V  31.9ns 0V  32.0ns 0V  36.5ns 0V
+ 40ns 5V  41.9ns 5V  42.0ns 5V  50ns 5V)

Vblb_drv blb_in 0 PWL(
+ 0ns 5V   10ns 5V    11.9ns 5V  12.0ns 0V  16.5ns 0V
+ 20ns 5V  26.5ns 5V
+ 30ns 5V  36.5ns 5V
+ 40ns 5V  50ns 5V)

R_bl  bl_in  bl  100
R_blb blb_in blb 100

.ic V(q)=0.0 V(qb)=5.0 V(bl)=5.0 V(blb)=5.0

.tran 0.05n 50n

* Do tre Ghi 1 sau Layout (PEX)
.meas tran t_write_1_pex TRIG V(wl) VAL=2.5 RISE=1 TARG V(q) VAL=2.5 RISE=1

* Do dâng dien ap doc (Read Bump sau PEX tai t = 42ns - 46ns)
.meas tran vq_read_bump_pex MAX V(q) FROM=42n TO=46n

.end
