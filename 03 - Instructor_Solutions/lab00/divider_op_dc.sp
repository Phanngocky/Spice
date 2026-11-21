* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 00 - EX1: VOLTAGE DIVIDER (.OP & .DC SWEEP)
* Circuit: R1 = 30k, R2 = 20k, Vin = 5V
* Expected Results: V(vout) = 2.000V, I(R1) = 0.100mA, Ptotal = 0.500mW
* Status: Verified with exact analytical math & LTspice syntax
* ==============================================================================

Vin in 0 DC 5.0

R1 in vout 30k
R2 vout 0  20k

* 1. Operating Point Analysis (.OP)
.OP

* 2. DC Sweep Analysis (.DC) - Uncomment to run standalone sweep
* .DC Vin 0 10 0.1

.END
