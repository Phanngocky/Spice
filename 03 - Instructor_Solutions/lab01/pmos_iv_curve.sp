* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 01 - EX1: PMOS I-V CHARACTERIZATION
* Process: MOSIS C5N 0.5um CMOS (Level 3 Model P)
* Sizing: W = 3.6u, L = 0.6u
* Status: Verified in LTspice
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

* M1 drain gate source bulk Model L W
* For PMOS, source is connected to VDD (5V), bulk to VDD (5V)
M1 vd vg vdd vdd P L=0.6U W=3.6U

Vdd vdd 0 DC 5.0
* Sweep VDS from 0V to -5V relative to source (so Vd from 5V down to 0V)
Vd  vdd vd DC 0
* Sweep VGS from -1V to -5V relative to source (so Vg from 4V down to 0V)
Vg  vdd vg DC 5.0

* Nested DC Sweep for output characteristics |IDS| - |VDS|
.DC Vd 0 5 0.01 Vg 1 5 1

.OPTIONS RELTOL=1E-4 ABSTOL=1E-12 VNTOL=1E-6
.END
