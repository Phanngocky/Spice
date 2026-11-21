* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 02 - EX3: CMOS NOR2 TRANSIENT DELAY EXTRACTION
* Process: MOSIS C5N 0.5um CMOS
* Sizing: PMOS W=7.2u/L=0.6u (series), NMOS W=1.2u/L=0.6u (parallel), CL=50fF
* Status: Verified in LTspice
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0
Va  a   0 PULSE(0 5.0 10n 100p 100p 9.9n 50n)
Vb  b   0 DC 0

* --- Pull-Up Network (PMOS series) ---
* Internal node xp between MP1 and MP2
MP1 xp  a vdd vdd P L=0.6U W=7.2U
MP2 out b xp  vdd P L=0.6U W=7.2U

* --- Pull-Down Network (NMOS parallel) ---
MN1 out a 0 0 N L=0.6U W=1.2U
MN2 out b 0 0 N L=0.6U W=1.2U

CL out 0 50fF

.TRAN 1p 60n

* Measure Worst-case tpLH and tpHL (only 1 NMOS pulling down)
.MEASURE TRAN tpHL_nor TRIG V(a)=2.5 RISE=1 TARG V(out)=2.5 FALL=1
.MEASURE TRAN tpLH_nor TRIG V(a)=2.5 FALL=1 TARG V(out)=2.5 RISE=1
.MEASURE TRAN tpd_nor  PARAM (tpHL_nor + tpLH_nor)/2

.OPTIONS RELTOL=1E-4 ABSTOL=1E-12 VNTOL=1E-6
.END
