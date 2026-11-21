* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 01 - EX2 & EX3: CMOS INVERTER VTC & TRANSIENT DELAYS
* Process: MOSIS C5N 0.5um CMOS
* Device Sizing: NMOS W=1.2u/L=0.6u, PMOS W=3.6u/L=0.6u (Beta ratio = 1)
* Status: Synthetic netlist for verification / LTspice compatible
* ==============================================================================

.include "../../04 - Models_and_Libraries/C5_models.txt"

* --- Power Supplies ---
Vdd vdd 0 DC 5.0
Vin in  0 PULSE(0 5.0 0 100p 100p 9.9n 20n)

* --- CMOS Inverter Schematic Netlist ---
* M_PMOS drain gate source bulk model L W
M_P out in vdd vdd P L=0.6U W=3.6U
* M_NMOS drain gate source bulk model L W
M_N out in 0   0   N L=0.6U W=1.2U

* --- Output Load Capacitance ---
CL out 0 50fF

* --- Simulation Analyses ---
* 1. Transient Analysis for delay extraction
.TRAN 1p 50n

* Automatic Delay Measurements (.measure statements)
.MEASURE TRAN tpHL TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 FALL=1
.MEASURE TRAN tpLH TRIG V(in)=2.5 FALL=1 TARG V(out)=2.5 RISE=1
.MEASURE TRAN tpd  PARAM (tpHL + tpLH)/2
.MEASURE TRAN trise TRIG V(out)=0.5 RISE=1 TARG V(out)=4.5 RISE=1
.MEASURE TRAN tfall TRIG V(out)=4.5 FALL=1 TARG V(out)=0.5 FALL=1

* 2. VTC DC Sweep (Comment out .TRAN to run VTC standalone):
* .DC Vin 0 5.0 0.005

.OPTIONS RELTOL=1E-4 ABSTOL=1E-12 VNTOL=1E-6
.END
