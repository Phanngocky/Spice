* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 01 - EX2: CMOS INVERTER VTC & NOISE MARGINS
* Process: MOSIS C5N 0.5um CMOS
* Sizing: NMOS W=1.2u/L=0.6u, PMOS W=3.6u/L=0.6u
* Purpose: DC Sweep from 0V to 5V with 5mV resolution for precise VTC & derivative
* Status: Verified in LTspice
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0
Vin in  0 DC 0

* CMOS Inverter
M_P out in vdd vdd P L=0.6U W=3.6U
M_N out in 0   0   N L=0.6U W=1.2U

* DC Sweep with fine steps for accurate numerical derivative
.DC Vin 0 5.0 0.002

* Measure Switching Threshold VM where V(out) = V(in)
.MEASURE DC VM WHEN V(out)=V(in)

.OPTIONS RELTOL=1E-4 ABSTOL=1E-12 VNTOL=1E-6
.END
