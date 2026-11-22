import math

def verify_lab00():
    print("=" * 60)
    print("VERIFICATION: LAB 00 (REVISED & ALIGNED)")
    print("=" * 60)

    # P1: Units
    print("P1. Units:")
    print("  2.2M   = 2.2 * 10^-3 = 0.0022 (milli)")
    print("  2.2Meg = 2.2 * 10^6  = 2,200,000 (mega)")
    print("  47n    = 47 * 10^-9  = 47 nF / ns / nH")
    print("  30f    = 30 * 10^-15 = 30 fF")

    # P2: Voltage Divider
    Vin = 5.0
    R1 = 12.0e3
    R2 = 18.0e3
    R_total = R1 + R2
    Vout = Vin * (R2 / R_total)
    I_in = Vin / R_total
    P_total = Vin * I_in
    print("\nP2. Voltage Divider (Vin=5V, R1=12k, R2=18k):")
    print(f"  Vout    = {Vout:.4f} V (exactly 3.0 V)")
    print(f"  I       = {I_in * 1e3:.4f} mA ({I_in * 1e6:.1f} uA)")
    print(f"  P_total = {P_total * 1e3:.4f} mW ({P_total * 1e6:.1f} uW)")

    # P3: RC Circuit (R=20k, C=5nF)
    R = 20.0e3
    C = 5.0e-9
    tau = R * C
    Vc_tau = Vin * (1 - math.exp(-1))
    t_50 = math.log(2) * tau
    t_r = math.log(9) * tau  # 10% to 90%
    f_3db = 1.0 / (2 * math.pi * tau)
    I_peak_charge = Vin / R
    print("\nP3. RC Circuit (R=20k, C=5nF, Vin=0->5V):")
    print(f"  tau     = {tau * 1e6:.2f} us ({tau * 1e3:.4f} ms)")
    print(f"  Vc(tau) = {Vc_tau:.4f} V ({Vc_tau / Vin * 100:.2f}%)")
    print(f"  t_50    = {t_50 * 1e6:.4f} us (ln(2)*tau = {math.log(2):.5f} * tau)")
    print(f"  t_r     = {t_r * 1e6:.4f} us (ln(9)*tau = {math.log(9):.5f} * tau ~ 2.2*tau)")
    print(f"  f_-3dB  = {f_3db:.2f} Hz ({f_3db / 1e3:.4f} kHz)")
    print(f"  I_peak  = {I_peak_charge * 1e3:.4f} mA ({I_peak_charge * 1e6:.1f} uA)")

    # P5: VLSI Link (Inverter R=1k, CL=50fF)
    R_inv = 1.0e3
    CL = 50.0e-15
    t_50_vlsi = 0.69315 * R_inv * CL
    print("\nP5. VLSI Link (R=1k, CL=50fF):")
    print(f"  t_50    = {t_50_vlsi * 1e12:.3f} ps")

    # Ex0.4: Parameter Sweep (.step param Rval list 5k 10k 20k 40k)
    print("\nEx0.4: Param Sweep Rval (C=5nF):")
    R_list = [5e3, 10e3, 20e3, 40e3]
    for r_val in R_list:
        t_pd_val = math.log(2) * r_val * C
        print(f"  R = {r_val / 1e3:4.1f} kOhm -> t_pd = {t_pd_val * 1e6:7.3f} us")
    slope = math.log(2) * C
    print(f"  Slope dt_pd/dR = ln(2)*C = {slope * 1e9:.4f} ns/kOhm ({slope:.4e} s/Ohm)")

    # Ex0.5: MOSFET C5N NMOS test (W=1.2u, L=0.6u, VGS=5V, VDS=5V)
    # Using typical Level 3 / BSIM params for C5N:
    # Vth0 ~ 0.70V, KP ~ 120 uA/V^2
    # ID_sat_approx = 0.5 * KP * (W/L) * (VGS - VTH)^2
    kp_n = 120.0e-6
    vth_n = 0.70
    w_n = 1.2e-6
    l_n = 0.6e-6
    id_approx = 0.5 * kp_n * (w_n / l_n) * ((Vin - vth_n) ** 2)
    print("\nEx0.5: NMOS C5N Test (W=1.2u, L=0.6u, VGS=5V, VDS=5V):")
    print(f"  ID (approx square law) = {id_approx * 1e3:.3f} mA (Vth={vth_n}V, KP={kp_n*1e6} uA/V^2)")
    print("=" * 60)

if __name__ == "__main__":
    verify_lab00()
