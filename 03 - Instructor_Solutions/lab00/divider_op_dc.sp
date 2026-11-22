* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 00 - EX0.1: VOLTAGE DIVIDER (.OP & .DC SWEEP)
* Circuit: R1 = 12k, R2 = 18k, Vin = 5.0V
* Expected Results:
*   V(vout) = 5.0 * 18k / (12k + 18k) = 3.000V
*   I(R1) = 5.0V / 30k = 0.1667mA (166.7 uA)
*   Ptotal = 5.0V * 0.1667mA = 0.8333mW (833.3 uW)
*   DC Sweep Slope: dVout/dVin = R2/(R1 + R2) = 18k/30k = 0.600
* ==============================================================================

Vin in 0 DC 5.0

R1 in vout 12k
R2 vout 0  18k

* 1. Operating Point Analysis (.OP)
.OP

* 2. DC Sweep Analysis (.DC) - Uncomment to run standalone sweep
* .DC Vin 0 10 0.1

.END
