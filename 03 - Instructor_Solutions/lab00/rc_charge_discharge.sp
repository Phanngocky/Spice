* RC CHARGE AND DISCHARGE - Mo Phong Qua Trinh Nap va Xa Tu Dien Co Ban
* Mon hoc: Thuc hanh Thiet ke VLSI (5505382) - DH Su pham Ky thuat Da Nang
* Tac gia: Phan Ngoc Ky (2026)

.title RC Circuit Charge and Discharge Transient Simulation

* --- NGUON XUNG VUONG PULSE KICH THICH NAP - XA ---
* Cu phap: PULSE(Vinitial Von Tdelay Trise Tfall Ton Tperiod)
* Vo = 5V, Ton = 500us (5*tau), Tperiod = 1000us (10*tau de nap day va xa het)
Vin in 0 PULSE(0 5.0 0 10n 10n 500u 1000u)

* --- PHAN TU MACH RC ---
R1 in out 10k
C1 out 0 10n

* --- MO PHONG QUA DO (TRANSIENT ANALYSIS) ---
* Thoi gian mo phong: 1000us (1 chu ky tron ven nap va xa), buoc cuc dai 0.1us
.tran 0.1u 1000u 0 0.1u

* --- CAC CAU LENH DO LUONG TU DONG (.MEASURE) ---
* 1. DO GIAI DOAN NAP (0 -> 500us):
* Hang so thoi gian nap tau_charge (thoi diem V(out) dat 63.2% cua 5V = 3.1606V)
.meas TRAN tau_charge TRIG V(in)=2.5 RISE=1 TARG V(out)=3.1606 RISE=1
* Thoi gian tang t_rise tu 10% (0.5V) len 90% (4.5V)
.meas TRAN t_rise TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1
* Dien ap sau 5*tau nap (tai 499us)
.meas TRAN Vc_charged FIND V(out) AT=499u
* Dong dien nap cuc dai
.meas TRAN I_peak_charge MAX I(C1)

* 2. DO GIAI DOAN XA (500us -> 1000us):
* Hang so thoi gian xa tau_discharge (thoi diem V(out) sut con 36.8% cua 5V = 1.8394V)
.meas TRAN tau_discharge TRIG V(in)=2.5 FALL=1 TARG V(out)=1.8394 FALL=1
* Thoi gian giam t_fall tu 90% (4.5V) xuong 10% (0.5V)
.meas TRAN t_fall TRIG V(out)=4.5 FALL=1 TARG V(out)=0.5 FALL=1
* Dien ap sau 5*tau xa (tai 999us)
.meas TRAN Vc_discharged FIND V(out) AT=999u
* Dong dien xa cuc dai (dong am doi chieu)
.meas TRAN I_peak_discharge MIN I(C1)

.end
