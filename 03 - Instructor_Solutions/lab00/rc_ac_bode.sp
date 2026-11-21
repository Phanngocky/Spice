* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 00 - RC AC ANALYSIS & CUT-OFF FREQUENCY MEASUREMENT
* Circuit: Low-pass RC Filter (R=10k, C=10nF -> f_3dB = 1/(2*pi*10k*10n) = 1.5915 kHz)
* Purpose: Demonstrate .AC and .MEASURE AC commands
* Status: Verified in LTspice
* ==============================================================================

Vin in 0 AC 1.0 0

R1 in out 10k
C1 out 0 10nF

* AC Analysis from 10Hz to 1MHz, 20 points per decade
.AC dec 20 10 1Meg

* Automatic measurement of maximum passband gain and 3dB cut-off frequency
.MEASURE AC Av_max MAX mag(V(out)/V(in))
.MEASURE AC f_cut WHEN mag(V(out)/V(in))=(Av_max/sqrt(2)) FALL=1

.END
