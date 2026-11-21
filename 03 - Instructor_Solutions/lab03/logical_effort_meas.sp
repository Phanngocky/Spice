* LOGICAL EFFORT MEASUREMENT OF AOI21 INPUT A
* Slope-Intercept Method: d = g*h + p
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* AOI21 Subcircuit
.subckt aoi21_x1 A B C out vdd gnd
Mpa xp A vdd vdd P W=7.2u L=0.6u
Mpb xp B vdd vdd P W=7.2u L=0.6u
Mpc out C xp vdd P W=7.2u L=0.6u
Mna out A xn 0 N W=2.4u L=0.6u
Mnb xn B 0 0 N W=2.4u L=0.6u
Mnc out C 0 0 N W=1.2u L=0.6u
.ends aoi21_x1

* Subcircuit INV_X1 (Inverter chuan tham chieu)
.subckt inv_x1 in out vdd gnd
Mp out in vdd vdd P W=3.6u L=0.6u
Mn out in 0 0 N W=1.2u L=0.6u
.ends inv_x1

* 4 MACH DO CHO 4 GIA TRI FAN-OUT h = 1, 2, 3, 4
* Cin_inv xap xi 20fF
* Case 1: h = 1 (CL = 20fF)
X1 in_A vdd 0 out_h1 vdd 0 aoi21_x1
C1 out_h1 0 20fF

* Case 2: h = 2 (CL = 40fF)
X2 in_A vdd 0 out_h2 vdd 0 aoi21_x1
C2 out_h2 0 40fF

* Case 3: h = 3 (CL = 60fF)
X3 in_A vdd 0 out_h3 vdd 0 aoi21_x1
C3 out_h3 0 60fF

* Case 4: h = 4 (CL = 80fF)
X4 in_A vdd 0 out_h4 vdd 0 aoi21_x1
C4 out_h4 0 80fF

* Nguon kich xung ngo vao A (chu ky 20ns)
Va in_A 0 PULSE(0 5.0 2n 0.1n 0.1n 8n 20n)

.tran 0.01n 25n

* Do tre tai tung Fan-out
* Fan-out h = 1
.meas tran tphl_1 TRIG v(in_A) VAL=2.5 RISE=1 TARG v(out_h1) VAL=2.5 FALL=1
.meas tran tplh_1 TRIG v(in_A) VAL=2.5 FALL=1 TARG v(out_h1) VAL=2.5 RISE=1
.meas tran tpd_1 PARAM='(tphl_1 + tplh_1)/2'

* Fan-out h = 2
.meas tran tphl_2 TRIG v(in_A) VAL=2.5 RISE=1 TARG v(out_h2) VAL=2.5 FALL=1
.meas tran tplh_2 TRIG v(in_A) VAL=2.5 FALL=1 TARG v(out_h2) VAL=2.5 RISE=1
.meas tran tpd_2 PARAM='(tphl_2 + tplh_2)/2'

* Fan-out h = 3
.meas tran tphl_3 TRIG v(in_A) VAL=2.5 RISE=1 TARG v(out_h3) VAL=2.5 FALL=1
.meas tran tplh_3 TRIG v(in_A) VAL=2.5 FALL=1 TARG v(out_h3) VAL=2.5 RISE=1
.meas tran tpd_3 PARAM='(tphl_3 + tplh_3)/2'

* Fan-out h = 4
.meas tran tphl_4 TRIG v(in_A) VAL=2.5 RISE=1 TARG v(out_h4) VAL=2.5 FALL=1
.meas tran tplh_4 TRIG v(in_A) VAL=2.5 FALL=1 TARG v(out_h4) VAL=2.5 RISE=1
.meas tran tpd_4 PARAM='(tphl_4 + tplh_4)/2'

* Tinh do doc slope = delta_tpd / delta_h
.meas tran delta_tpd PARAM='(tpd_4 - tpd_1)/3'

.end
