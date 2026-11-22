* ==============================================================================
* INSTRUCTOR SOLUTION: LAB 00 - EX0.4: PARAMETER SWEEP (.PARAM & .STEP)
* Circuit: R1 = {Rval}, C1 = 5nF
* Sweep: Rval list 5k 10k 20k 40k
* Purpose: Extract slope dt_pd/dR and verify t_pd = ln(2)*R*C = 0.69*R*C
* Expected Results:
*   R =  5k -> t_pd = 17.329 us
*   R = 10k -> t_pd = 34.657 us
*   R = 20k -> t_pd = 69.315 us
*   R = 40k -> t_pd = 138.629 us
*   Slope = ln(2)*C = 3.4657 ns/kOhm
* ==============================================================================

.param Rval=20k
.step param Rval list 5k 10k 20k 40k

Vin in 0 PULSE(0 5.0 0 10n 10n 500u 1000u)

R1 in out {Rval}
C1 out 0 5n

.tran 0 1m 0 0.1u

.meas TRAN t_pd TRIG V(in)=2.5 RISE=1 TARG V(out)=2.5 RISE=1

.end
