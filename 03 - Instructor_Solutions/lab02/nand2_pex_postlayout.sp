* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 02 - EX5: CMOS NAND2 POST-LAYOUT PEX NETLIST
* Technology: MOSIS C5N 0.5um (mocmos, lambda=0.30um)
* Includes Extracted Diffusion Area/Perimeter (AS, AD, PS, PD) & Wire Caps
* Status: Verified in LTspice
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0
Va  a   0 PULSE(0 5.0 10n 100p 100p 9.9n 50n)
Vb  b   0 DC 5.0

* --- PMOS with Extraction Geometry (W=3.6u, L=0.6u, Shared Drain) ---
* MP1 and MP2 share drain diffusion: AD=3.6u*1.5u = 5.4p shared
MP1 out a vdd vdd P L=0.6U W=3.6U AS=5.4P AD=2.7P PS=10.2U PD=5.1U
MP2 out b vdd vdd P L=0.6U W=3.6U AS=5.4P AD=2.7P PS=10.2U PD=5.1U

* --- NMOS with Extraction Geometry (W=2.4u, L=0.6u, Series) ---
* MN1: Drain connects to out, Source connects to internal node xn
MN1 out a xn  0   N L=0.6U W=2.4U AS=3.6P AD=3.6P PS=7.8U  PD=7.8U
* MN2: Drain connects to internal node xn, Source connects to GND
MN2 xn  b 0   0   N L=0.6U W=2.4U AS=3.6P AD=3.6P PS=7.8U  PD=7.8U

* Parasitic Interconnect Capacitance
C_wire_out out 0 11.2fF
C_wire_xn  xn  0  4.8fF

* External Load
CL out 0 50fF

.TRAN 1p 60n

.MEASURE TRAN tpHL_post TRIG V(a)=2.5 RISE=1 TARG V(out)=2.5 FALL=1
.MEASURE TRAN tpLH_post TRIG V(a)=2.5 FALL=1 TARG V(out)=2.5 RISE=1
.MEASURE TRAN tpd_post  PARAM (tpHL_post + tpLH_post)/2

.OPTIONS RELTOL=1E-4 ABSTOL=1E-12 VNTOL=1E-6
.END
