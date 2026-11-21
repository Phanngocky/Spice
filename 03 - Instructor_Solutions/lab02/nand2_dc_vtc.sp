* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 02 - EX1: CMOS NAND2 VTC & SWITCHING THRESHOLDS
* Process: MOSIS C5N 0.5um CMOS
* Transistors: PMOS W=3.6u/L=0.6u (parallel), NMOS W=2.4u/L=0.6u (series)
* Purpose: DC Sweep of Input A with Input B held at 5V, and Tied Inputs A=B
* Status: Verified in LTspice
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0
Va  a   0 DC 0
Vb  b   0 DC 5.0

* --- Pull-Up Network (PMOS parallel) ---
MP1 out a vdd vdd P L=0.6U W=3.6U
MP2 out b vdd vdd P L=0.6U W=3.6U

* --- Pull-Down Network (NMOS series) ---
* Internal node xn between MN1 and MN2
MN1 out a xn  0   N L=0.6U W=2.4U
MN2 xn  b 0   0   N L=0.6U W=2.4U

* --- DC Sweep: Input A from 0V to 5V ---
.DC Va 0 5.0 0.002

* Switching Threshold Measurement
.MEASURE DC VM_A WHEN V(out)=V(a)

.OPTIONS RELTOL=1E-4 ABSTOL=1E-12 VNTOL=1E-6
.END
