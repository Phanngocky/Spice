* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 00 - EX0.2: RC CHARGE & DISCHARGE
* Circuit: R1 = 20k, C1 = 5nF -> tau = R*C = 100us
* ==============================================================================

Vin in 0 PULSE(0 5.0 0 10n 10n 500u 1000u) AC 1

R1 in out 20k
C1 out 0 5n

.tran 0 1m 0 0.1u

.meas TRAN t_pd TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 RISE=1
.meas TRAN t_r TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1
.meas TRAN t_f TRIG V(out)=4.5 FALL=1 TARG V(out)=0.5 FALL=1
.meas TRAN I_peak_chg MAX I(C1)
.meas TRAN I_peak_dis MIN I(C1)
.meas TRAN tau_chg TRIG V(in)=2.5 RISE=1 TARG V(out)=3.1606 RISE=1
.meas TRAN tau_dis TRIG V(in)=2.5 FALL=1 TARG V(out)=1.8394 FALL=1

.end
