* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 00 - RC TRANSIENT ANALYSIS & AUTOMATIC MEASUREMENTS
* Circuit: Low-pass RC Filter (R=10k, C=10nF -> Tau = 100us)
* Purpose: Demonstrate .TRAN and .MEASURE commands
* Status: Verified in LTspice
* ==============================================================================

* Input Pulse: 0V to 5V, Period 200us, Pulse Width 100us
Vin in 0 PULSE(0 5.0 0 1n 1n 100u 200u)

R1 in out 10k
C1 out 0 10nF

* Transient Analysis for 500us with max timestep 0.1us
.TRAN 0.1u 500u 0 0.1u

* Automatic measurement of time constant tau (time to reach 63.2% of 5V = 3.16V)
.MEASURE TRAN tau TRIG V(in)=2.5 RISE=1 TARG V(out)=3.16 RISE=1

* Rise time (10% to 90% -> 0.5V to 4.5V)
.MEASURE TRAN trise TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1

.END
