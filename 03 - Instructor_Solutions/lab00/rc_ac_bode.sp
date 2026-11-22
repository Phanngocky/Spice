* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 00 - EX0.3: RC AC ANALYSIS & BODE PLOT
* Circuit: R1 = 20k, C1 = 5nF -> f_-3dB = 1/(2*pi*20k*5n) = 1591.55 Hz (1.592 kHz)
* Expected Results:
*   Av_max = 1.000 (0.00 dB) at low frequency
*   f_c (-3dB cutoff frequency) = 1.592 kHz
*   Phase at f_c = -45.0 degrees
* ==============================================================================

Vin in 0 AC 1.0 0

R1 in out 20k
C1 out 0 5n

.ac dec 20 10 1Meg

.meas AC Av_max MAX mag(V(out)/V(in))
.meas AC f_c WHEN mag(V(out)/V(in))=Av_max/sqrt(2) FALL=1

.end
