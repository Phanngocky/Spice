* TRANSMISSION GATE VS PASS TRANSISTOR VERIFICATION (.TRAN)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* So sanh: NMOS Pass Transistor (Weak 1) vs PMOS Pass Transistor (Weak 0) vs CMOS TG (Rail-to-Rail)

.include "../../04 - Models_and_Libraries/C5_models.txt"

* Nguon cap VDD
Vdd vdd 0 DC 5.0

* ==============================================================
* NHANH 1: NMOS PASS TRANSISTOR
* Gate noi len VDD (5V), Substrate noi GND (0V)
* ==============================================================
Mn1 in vdd out_nmos 0 N W=1.2u L=0.6u
CL_n out_nmos 0 50fF

* ==============================================================
* NHANH 2: PMOS PASS TRANSISTOR
* Gate noi xuong GND (0V), Substrate noi VDD (5V)
* ==============================================================
Mp1 in 0 out_pmos vdd P W=3.6u L=0.6u
CL_p out_pmos 0 50fF

* ==============================================================
* NHANH 3: CMOS TRANSMISSION GATE (TG)
* NMOS Gate = VDD (5V), PMOS Gate = GND (0V)
* ==============================================================
Mn_tg in vdd out_tg 0 N W=1.2u L=0.6u
Mp_tg in 0 out_tg vdd P W=3.6u L=0.6u
CL_tg out_tg 0 50fF

* Nguon tin hieu vao: Xung vuong 0V - 5V, tan so 20MHz (T = 50ns)
Vin in 0 PULSE(0 5.0 5n 0.1n 0.1n 25n 50n)

* Mo phong Transient 80ns
.tran 0.05n 80n

* DO BIEN DO DIEN AP DINH - DAY (V_MAX & V_MIN)
.meas tran vmax_nmos MAX v(out_nmos) FROM=10n TO=30n
.meas tran vmin_nmos MIN v(out_nmos) FROM=35n TO=55n

.meas tran vmax_pmos MAX v(out_pmos) FROM=10n TO=30n
.meas tran vmin_pmos MIN v(out_pmos) FROM=35n TO=55n

.meas tran vmax_tg MAX v(out_tg) FROM=10n TO=30n
.meas tran vmin_tg MIN v(out_tg) FROM=35n TO=55n

* DO TRE TRUYEN LAN CUA CONG TRUYEN TG
.meas tran tphl_tg TRIG v(in) VAL=2.5 FALL=1 TARG v(out_tg) VAL=2.5 FALL=1
.meas tran tplh_tg TRIG v(in) VAL=2.5 RISE=1 TARG v(out_tg) VAL=2.5 RISE=1
.meas tran tpd_tg PARAM='(tphl_tg + tplh_tg)/2'

.control
run
plot v(in) v(out_nmos) v(out_pmos) v(out_tg)
.endc

.end
