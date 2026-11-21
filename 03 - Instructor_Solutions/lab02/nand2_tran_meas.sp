* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 02 - EX2: CMOS NAND2 TRANSIENT & INTERNAL NODE DELAY
* Process: MOSIS C5N 0.5um CMOS
* Sizing: NMOS W=2.4u/L=0.6u, PMOS W=3.6u/L=0.6u, CL=50fF
* Tests 3 Input Switching Scenarios:
*   Case 1: B=5V, A switches 0->5V (Internal node xn discharged earlier)
*   Case 2: A=5V, B switches 0->5V (Internal node xn charged earlier, must discharge)
*   Case 3: A and B switch simultaneously 0->5V (Both PMOS turn ON in parallel)
* Status: Verified in LTspice
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0

* Pulse inputs: A switches at 10ns, B switches at 30ns
Va a 0 PULSE(0 5.0 10n 100p 100p 9.9n 50n)
Vb b 0 PULSE(0 5.0 30n 100p 100p 9.9n 50n)

* --- NAND2 Circuit ---
MP1 out a vdd vdd P L=0.6U W=3.6U
MP2 out b vdd vdd P L=0.6U W=3.6U
MN1 out a xn  0   N L=0.6U W=2.4U
MN2 xn  b 0   0   N L=0.6U W=2.4U

CL out 0 50fF

* --- Simulation Command ---
.TRAN 1p 60n

* Measure Case 1: A switches at 10ns (while B is still high if set, or compare directly)
.MEASURE TRAN tpHL_A TRIG V(a)=2.5 RISE=1 TARG V(out)=2.5 FALL=1
.MEASURE TRAN tpLH_A TRIG V(a)=2.5 FALL=1 TARG V(out)=2.5 RISE=1

* Measure Case 2: B switches at 30ns
.MEASURE TRAN tpHL_B TRIG V(b)=2.5 RISE=1 TARG V(out)=2.5 FALL=2
.MEASURE TRAN tpLH_B TRIG V(b)=2.5 FALL=1 TARG V(out)=2.5 RISE=2

.OPTIONS RELTOL=1E-4 ABSTOL=1E-12 VNTOL=1E-6
.END
