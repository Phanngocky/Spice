* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 00 - RC TRANSIENT ANALYSIS & AUTOMATIC MEASUREMENTS
* Circuit: Low-pass RC Filter (R=20k, C=5nF -> Tau = 100us)
* Purpose: Demonstrate .TRAN and .MEASURE commands
* Status: Verified in LTspice
* ==============================================================================

Vin in 0 PULSE(0 5.0 0 10n 10n 500u 1000u)

R1 in out 20k
C1 out 0 5n

.TRAN 0 1m 0 0.1u

.MEASURE TRAN t_pd TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 RISE=1
.MEASURE TRAN trise TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1
.MEASURE TRAN tfall TRIG V(out)=4.5 FALL=1 TARG V(out)=0.5 FALL=1

.END
