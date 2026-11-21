* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 01 - EX1: NMOS I-V CHARACTERIZATION
* Process: MOSIS C5N 0.5um CMOS (Level 3 Models)
* Purpose: DC Sweeps for IDS-VDS and IDS-VGS Curve Extraction
* Status: Synthetic netlist for verification / LTspice compatible
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

* --- Circuit Topology ---
* M1 drain gate source bulk model L=0.6u W=1.2u
M1 vd vg 0 0 N L=0.6U W=1.2U

* DC Voltage Supplies
VDS vd 0 DC 5.0
VGS vg 0 DC 5.0

* --- Simulation Commands ---
* 1. Nested DC Sweep for output characteristics IDS - VDS
* Sweeps VDS from 0V to 5V (step 10mV) for VGS = 1V, 2V, 3V, 4V, 5V
.DC VDS 0 5 0.01 VGS 1 5 1

* 2. Alternative Sweep for transfer characteristic IDS - VGS (uncomment to run):
* .DC VGS 0 5 0.01

.OPTIONS RELTOL=1E-4 ABSTOL=1E-12 VNTOL=1E-6
.END
