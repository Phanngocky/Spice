* LAB 08: VOLTAGE LATCH SENSE AMPLIFIER (VLSA) TRANSIENT SIMULATION
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Mo ta: Khuếch đại tín hiệu vi sai biên độ nhỏ Delta_V = 150mV thành mức logic 0V - 5V

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* ==============================================================
* SUBCIRCUIT: sense_amp_vlsa
* bl blb saen so sob vdd gnd
* ==============================================================
.subckt sense_amp_vlsa bl blb saen so sob vdd gnd

* 1. Cross-coupled Inverter Pair
Mp1 so  sob vdd vdd P W=3.6u L=0.6u
Mp2 sob so  vdd vdd P W=3.6u L=0.6u

Mn1 so  sob n_tail gnd N W=2.4u L=0.6u
Mn2 sob so  n_tail gnd N W=2.4u L=0.6u

* 2. Tail NMOS duoc kich hoat boi SAEN
Mn_tail n_tail saen gnd gnd N W=3.6u L=0.6u

* 3. Pass gates ket noi tu BL/BLB vao nut SO/SOB
Mn_pass1 so  bl  vdd gnd N W=1.2u L=0.6u
Mn_pass2 sob blb vdd gnd N W=1.2u L=0.6u

* 4. Dien dung ky sinh tai nut Sense Output
C_so  so  0 20fF
C_sob sob 0 20fF

.ends sense_amp_vlsa

* ==============================================================
* TESTBENCH & TIN HIEU VAO VI SAI
* ==============================================================
* Tin hieu Bitline voi do lech Delta_V = 150mV:
* BL = 5.00V (Bit '1')
* BLB = 4.85V (Bitline bi xa nhe do o nho luu '0')
Vbl  bl  0 DC 5.00
Vblb blb 0 DC 4.85

* Xung kich hoat Sense Amplifier Enable (SAEN):
* Truoc 2.0ns: SAEN = 0V (Sense Amp tat)
* Tai 2.0ns:   SAEN bat len 5.0V voi suon len 0.1ns
Vsaen saen 0 PULSE(0 5.0 2.0n 0.1n 0.1n 3.0n 10n)

* Goi subcircuit Sense Amp
X_sa bl blb saen so sob vdd 0 sense_amp_vlsa

* Dat dien ap ban dau cho nut SO va SOB bang VDD (Precharged)
.ic V(so)=5.00 V(sob)=4.85

* ==============================================================
* MO PHONG TRANSIENT & DO TRE KHUECH DAI
* ==============================================================
.tran 0.01n 5.0n

* Thoi gian chot khuếch dai: tu luc SAEN dat 2.5V den khi SOB tut xuong 0.5V
.meas tran t_latch TRIG V(saen) VAL=2.5 RISE=1 TARG V(sob) VAL=0.5 FALL=1

* Do lech vi sai tai thoi diem t = 2.5ns
.meas tran v_diff FIND (V(so) - V(sob)) AT=2.5n

.end
