* LAB 07: KHAO SAT HIEN TUONG CHIA SE DIEN TICH (CHARGE SHARING) VA KEEPER
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Mo ta: So sanh mach Dynamic khong co Keeper vs co Keeper khi nut noi Cint bi xa ve 0V

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Inverter chuan dung cho bo dem va Keeper
.subckt inv_std in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in gnd gnd N W=1.2u L=0.6u
.ends inv_std

* ==============================================================
* MACH 1: DYNAMIC GATE KHONG CO KEEPER (NO KEEPER)
* ==============================================================
* Precharge PMOS (W=12lambda = 3.6u)
Mp1 x_nokp clk vdd vdd P W=3.6u L=0.6u

* Series NMOS Network (Top NMOS va Bot NMOS)
Mn_top1 x_nokp in_top n_int1 gnd N W=1.2u L=0.6u
Mn_bot1 n_int1 in_bot n_foot1 gnd N W=1.2u L=0.6u
Mn_foot1 n_foot1 clk gnd gnd N W=2.4u L=0.6u

* Dien dung ky sinh nut noi Cint va nut dong Cx
C_int1 n_int1 0 14fF
C_x1   x_nokp 0 20fF

* Inverter ngo ra
X_inv1 x_nokp y_nokp vdd gnd inv_std

* ==============================================================
* MACH 2: DYNAMIC GATE CO WEAK PMOS KEEPER (WITH KEEPER)
* ==============================================================
* Precharge PMOS (W=12lambda = 3.6u)
Mp2 x_kp clk vdd vdd P W=3.6u L=0.6u

* Keeper PMOS (W=2lambda = 0.6u - Weak Pull-up)
M_kp x_kp y_kp vdd vdd P W=0.6u L=0.6u

* Series NMOS Network (Top NMOS va Bot NMOS)
Mn_top2 x_kp in_top n_int2 gnd N W=1.2u L=0.6u
Mn_bot2 n_int2 in_bot n_foot2 gnd N W=1.2u L=0.6u
Mn_foot2 n_foot2 clk gnd gnd N W=2.4u L=0.6u

* Dien dung ky sinh nut noi Cint va nut dong Cx
C_int2 n_int2 0 14fF
C_x2   x_kp   0 20fF

* Inverter ngo ra (cung cap tin hieu dieu khien Keeper)
X_inv2 x_kp y_kp vdd gnd inv_std

* ==============================================================
* NGUON TIN HIEU KICH THICH
* ==============================================================
* Xung nhip CLK: Chu ky 20ns (Precharge: 0-10ns, Evaluate: 10-20ns)
Vclk clk 0 PULSE(0 5.0 0 0.1n 0.1n 10n 20n)

* Tin hieu ngo vao Top: Bat len 5V trong pha Evaluate tai t=11ns
Vin_top in_top 0 PULSE(0 5.0 11n 0.1n 0.1n 8n 20n)

* Tin hieu ngo vao Bot: Giu nguyen 0V de ngan xa xuong dat (gay Charge Sharing)
Vin_bot in_bot 0 DC 0.0

* ==============================================================
* PHAN TICH TRANSIENT & DO DAC
* ==============================================================
.tran 0.05n 25n

* Dien ap thap nhat tai nut dong khi khong co keeper
.meas tran v_drop_nokp MIN V(x_nokp) FROM=10n TO=20n

* Dien ap thap nhat tai nut dong khi co keeper
.meas tran v_drop_kp MIN V(x_kp) FROM=10n TO=20n

* Dien ap nhieu tren ngo ra Y khi khong co keeper
.meas tran v_glitch_nokp MAX V(y_nokp) FROM=10n TO=20n

* Dien ap nhieu tren ngo ra Y khi co keeper
.meas tran v_glitch_kp MAX V(y_kp) FROM=10n TO=20n

.end
