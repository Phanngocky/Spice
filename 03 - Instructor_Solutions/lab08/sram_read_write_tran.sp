* LAB 08: 6T SRAM CELL TRANSIENT READ & WRITE SIMULATION (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Chu trinh: Write '1' -> Read '1' -> Write '0' -> Read '0'
* Sizing: Driver W=2.4u (8lambda), Access W=1.2u (4lambda), Load W=0.6u (2lambda)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* ==============================================================
* SUBCIRCUIT: sram_6t_cell
* wl bl blb q qb vdd gnd
* ==============================================================
.subckt sram_6t_cell wl bl blb q qb vdd gnd

* Inverter 1: Load M_L1 va Driver M_D1 tao nut Q
Mp_l1 q qb vdd vdd P W=0.6u L=0.6u
Mn_d1 q qb gnd gnd N W=2.4u L=0.6u

* Inverter 2: Load M_L2 va Driver M_D2 tao nut QB
Mp_l2 qb q vdd vdd P W=0.6u L=0.6u
Mn_d2 qb q gnd gnd N W=2.4u L=0.6u

* Access NMOS M_AX1 (BL <-> Q) va M_AX2 (BLB <-> QB)
Mn_ax1 bl  wl q  gnd N W=1.2u L=0.6u
Mn_ax2 blb wl qb gnd N W=1.2u L=0.6u

* Dien dung ky sinh nut luu tru noi bo Q va QB
C_q  q  0 10fF
C_qb qb 0 10fF

.ends sram_6t_cell

* ==============================================================
* TESTBENCH & TAI BITLINE
* ==============================================================
X_cell wl bl blb q qb vdd 0 sram_6t_cell

* Dien dung ky sinh cot Bitline (dai dien cho mang 64 hang)
C_bl  bl  0 250fF
C_blb blb 0 250fF

* ==============================================================
* NGUON KICH THICH CHO CHU TRINH WRITE VA READ
* ==============================================================
* Xung chon tu Wordline WL: Kich hoat moi chu ky 10ns
* - t = 12ns - 16ns: Write 1 (Chu ky 2)
* - t = 22ns - 26ns: Read 1  (Chu ky 3)
* - t = 32ns - 36ns: Write 0 (Chu ky 4)
* - t = 42ns - 46ns: Read 0  (Chu ky 5)
Vwl wl 0 PWL(
+ 0ns 0V   11.9ns 0V  12.0ns 5V  16.0ns 5V  16.1ns 0V
+ 21.9ns 0V 22.0ns 5V  26.0ns 5V  26.1ns 0V
+ 31.9ns 0V 32.0ns 5V  36.0ns 5V  36.1ns 0V
+ 41.9ns 0V 42.0ns 5V  46.0ns 5V  46.1ns 0V 50ns 0V)

* Bitline BL Driver:
* - Write 1: BL = 5V
* - Read 1:  BL precharge 5V (tha noi)
* - Write 0: BL = 0V
* - Read 0:  BL precharge 5V (tha noi va bi xa boi Driver)
Vbl_drv bl_in 0 PWL(
+ 0ns 5V   10ns 5V    16.5ns 5V
+ 20ns 5V  26.5ns 5V
+ 30ns 0V  31.9ns 0V  32.0ns 0V  36.5ns 0V
+ 40ns 5V  41.9ns 5V  42.0ns 5V  50ns 5V)

* Bitline Bar BLB Driver:
* - Write 1: BLB = 0V
* - Read 1:  BLB precharge 5V
* - Write 0: BLB = 5V
* - Read 0:  BLB precharge 5V
Vblb_drv blb_in 0 PWL(
+ 0ns 5V   10ns 5V    11.9ns 5V  12.0ns 0V  16.5ns 0V
+ 20ns 5V  26.5ns 5V
+ 30ns 5V  36.5ns 5V
+ 40ns 5V  50ns 5V)

* Switch cach ly cho phep Precharge va Float Bitline trong pha Read:
R_bl  bl_in  bl  100
R_blb blb_in blb 100

* ==============================================================
* MO PHONG TRANSIENT & DO LUONG
* ==============================================================
* Dat dieu kien ban dau (Initial Condition: Q = 0V, QB = 5V)
.ic V(q)=0.0 V(qb)=5.0 V(bl)=5.0 V(blb)=5.0

.tran 0.05n 50n

* 1. Thoi gian Ghi '1' (tu 12ns: thoi gian Q vuot 2.5V)
.meas tran t_write_1 TRIG V(wl) VAL=2.5 RISE=1 TARG V(q) VAL=2.5 RISE=1

* 2. Thoi gian Ghi '0' (tu 32ns: thoi gian Q tut xuong 2.5V)
.meas tran t_write_0 TRIG V(wl) VAL=2.5 RISE=3 TARG V(q) VAL=2.5 FALL=1

* 3. Do dâng dien ap nhieu khi Doc '0' (Read Disturb Bump tai t = 42ns - 46ns)
.meas tran vq_read_bump MAX V(q) FROM=42n TO=46n

* 4. Do chenh lech dien ap Bitline khi doc '0' (Delta V_BL tai t = 45ns)
.meas tran v_bl_at_45n  FIND V(bl)  AT=45n
.meas tran v_blb_at_45n FIND V(blb) AT=45n

.end
