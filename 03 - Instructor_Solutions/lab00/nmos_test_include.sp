* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 00 - EX4: THIRD-PARTY MODEL TEST (C5_models.txt)
* Circuit: Single NMOS with Level 3 C5N Model
* Expected Result: ID ~ 1.3 - 2.2 mA at VGS=5V, VDS=5V (No convergence error)
* Status: Verified model compatibility
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

* M1 drain gate source bulk Model L W
M1 vd vg 0 0 N L=0.6U W=1.2U

VDS vd 0 DC 5.0
VGS vg 0 DC 5.0

.OP

.END
