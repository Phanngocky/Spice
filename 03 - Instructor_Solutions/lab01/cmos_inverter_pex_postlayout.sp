* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 01 - EX5: POST-LAYOUT PEX NETLIST FOR CMOS INVERTER
* Technology: MOSIS C5N 0.5um (SCMOS mocmos, lambda=0.30um)
* Includes Area and Perimeter of Source/Drain Diffusion + Metal Parasitics
* Status: Synthetic netlist for verification / LTspice compatible
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

* --- Supplies ---
Vdd vdd 0 DC 5.0
Vin in_pad 0 PULSE(0 5.0 0 100p 100p 9.9n 20n)

* --- Input Pin / Wiring Parasitics ---
R_in in_pad in 5.0
C_in_poly in 0 3.2fF

* --- PMOS with Extraction Geometry ---
* W = 3.6u, L = 0.6u, Ldiff = 1.5u
* AD = AS = 3.6u * 1.5u = 5.4p
* PD = PS = 2 * (3.6u + 1.5u) = 10.2u
M_P out in vdd vdd P L=0.6U W=3.6U AS=5.4P AD=5.4P PS=10.2U PD=10.2U

* --- NMOS with Extraction Geometry ---
* W = 1.2u, L = 0.6u, Ldiff = 1.5u
* AD = AS = 1.2u * 1.5u = 1.8p
* PD = PS = 2 * (1.2u + 1.5u) = 5.4u
M_N out in 0 0 N L=0.6U W=1.2U AS=1.8P AD=1.8P PS=5.4U PD=5.4U

* --- Extracted Parasitic Interconnect Capacitance at Output Node ---
C_par_metal1 out 0 8.5fF

* --- External Load ---
CL out 0 50fF

* --- Transient Analysis ---
.TRAN 1p 50n

.MEASURE TRAN tpHL_post TRIG V(in_pad)=2.5 RISE=1 TARG V(out)=2.5 FALL=1
.MEASURE TRAN tpLH_post TRIG V(in_pad)=2.5 FALL=1 TARG V(out)=2.5 RISE=1
.MEASURE TRAN tpd_post  PARAM (tpHL_post + tpLH_post)/2

.OPTIONS RELTOL=1E-4 ABSTOL=1E-12 VNTOL=1E-6
.END
