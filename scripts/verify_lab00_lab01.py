"""
Verification and Numerical Benchmark Generator for VLSI Labs (Lab 00 & Lab 01)
Calculates exact theoretical values and generates SPICE benchmark verification data.
"""
import math
import numpy as np

def verify_lab00():
    print("="*60)
    print("VERIFICATION: LAB 00 (SPICE & LTSPICE INTRO)")
    print("="*60)
    
    # 1. Voltage Divider
    Vin = 5.0
    R1 = 30e3
    R2 = 20e3
    Vout = Vin * (R2 / (R1 + R2))
    Iin = Vin / (R1 + R2)
    Ptotal = Vin * Iin
    print(f"Voltage Divider: Vin={Vin}V, R1={R1/1e3}k, R2={R2/1e3}k")
    print(f"  Vout = {Vout:.4f} V")
    print(f"  Iin  = {Iin*1e3:.4f} mA ({Iin*1e6:.1f} uA)")
    print(f"  Ptotal = {Ptotal*1e3:.4f} mW ({Ptotal*1e6:.1f} uW)")
    
    # 2. RC Filter
    R = 10e3
    C = 10e-9
    tau = R * C
    V_tau = Vin * (1.0 - math.exp(-1.0))
    V_2_2tau = Vin * (1.0 - math.exp(-2.2))
    V_5tau = Vin * (1.0 - math.exp(-5.0))
    f_cut = 1.0 / (2.0 * math.pi * R * C)
    print(f"\nRC Low-Pass Filter: R={R/1e3}k, C={C*1e9}nF")
    print(f"  tau = R * C = {tau*1e6:.2f} us ({tau*1e3:.4f} ms)")
    print(f"  V(tau) = {V_tau:.4f} V (63.21%)")
    print(f"  V(2.2tau) = {V_2_2tau:.4f} V (88.92%)")
    print(f"  V(5tau) = {V_5tau:.4f} V (99.33%)")
    print(f"  f_-3dB = 1/(2*pi*RC) = {f_cut:.2f} Hz ({f_cut/1e3:.4f} kHz)")
    return {
        "Vout_div": Vout, "Iin_div": Iin, "P_div": Ptotal,
        "tau": tau, "V_tau": V_tau, "f_cut": f_cut
    }

def verify_lab01():
    print("\n" + "="*60)
    print("VERIFICATION: LAB 01 (MOSFET I-V & CMOS INVERTER)")
    print("="*60)
    
    VDD = 5.0
    Vthn = 0.70
    Vthp = -0.80
    Kn_prime = 120e-6   # A/V^2
    Kp_prime = 40e-6    # A/V^2
    
    Ln = 0.60e-6
    Wn = 1.20e-6
    Lp = 0.60e-6
    Wp = 3.60e-6
    
    beta_n = Kn_prime * (Wn / Ln)  # 240 uA/V^2
    beta_p = Kp_prime * (Wp / Lp)  # 240 uA/V^2
    
    print(f"MOSFET Parameters (C5N 0.5um):")
    print(f"  NMOS: W={Wn*1e6}u, L={Ln*1e6}u -> beta_n = {beta_n*1e6:.1f} uA/V^2")
    print(f"  PMOS: W={Wp*1e6}u, L={Lp*1e6}u -> beta_p = {beta_p*1e6:.1f} uA/V^2")
    print(f"  Sizing ratio (Wp/Wn) = {Wp/Wn:.2f}")
    
    # Saturation current at VGS = VDS = 5V
    Idsat_n = 0.5 * beta_n * (VDD - Vthn)**2
    Idsat_p = 0.5 * beta_p * (VDD - abs(Vthp))**2
    print(f"  Idsat_n (VGS=5V, VDS=5V) = {Idsat_n*1e3:.3f} mA")
    print(f"  Idsat_p (|VGS|=5V, |VDS|=5V) = {Idsat_p*1e3:.3f} mA")
    
    # Switching Threshold VM:
    # 0.5 * beta_n * (VM - Vthn)^2 = 0.5 * beta_p * (VDD - VM - |Vthp|)^2
    # sqrt(beta_p / beta_n) = r
    r = math.sqrt(beta_p / beta_n)
    VM = (Vthn + r * (VDD - abs(Vthp))) / (1.0 + r)
    print(f"\nCMOS Inverter VTC Characteristics:")
    print(f"  r = sqrt(beta_p/beta_n) = {r:.4f}")
    print(f"  Switching Threshold VM = {VM:.4f} V")
    
    # Noise Margins Calculation (Analytical Approximation for matched inverter)
    # VIL = (2*VM + VDD - |Vthp|) / (1 + r) ... approx:
    # dVout/dVin = -1
    # When NMOS is saturated and PMOS is linear:
    # In = beta_n/2 * (Vin - Vthn)^2
    # Ip = beta_p * ((VDD - Vin - |Vthp|)*(VDD - Vout) - (VDD - Vout)^2 / 2)
    # Equating and taking derivative dVout/dVin = -1 yields:
    VIL = (2.0 * VM + Vthn - VDD) / 2.0  # standard textbook approximation
    # Let's do numerical solve for VTC curve
    Vin_vals = np.linspace(0, 5, 501)
    Vout_vals = []
    for vin in Vin_vals:
        # solve for vout where In = Ip
        best_vout = 0.0
        min_err = 1e9
        for vout in np.linspace(0, 5, 501):
            # NMOS current
            if vin < Vthn:
                in_curr = 0.0
            elif vout >= vin - Vthn: # sat
                in_curr = 0.5 * beta_n * (vin - Vthn)**2
            else: # linear
                in_curr = beta_n * ((vin - Vthn)*vout - 0.5*vout**2)
                
            # PMOS current (vsp = VDD, vsg = VDD - vin, vsd = VDD - vout)
            vsg = VDD - vin
            vsd = VDD - vout
            vth_p = abs(Vthp)
            if vsg < vth_p:
                ip_curr = 0.0
            elif vsd >= vsg - vth_p: # sat
                ip_curr = 0.5 * beta_p * (vsg - vth_p)**2
            else: # linear
                ip_curr = beta_p * ((vsg - vth_p)*vsd - 0.5*vsd**2)
                
            err = abs(in_curr - ip_curr)
            if err < min_err:
                min_err = err
                best_vout = vout
        Vout_vals.append(best_vout)
    
    Vout_vals = np.array(Vout_vals)
    dvdv = np.gradient(Vout_vals, Vin_vals)
    
    # Points where dvdv = -1
    # VIL: before VM
    idx_before_vm = np.where((Vin_vals < 2.5) & (dvdv <= -1.0))[0]
    vil_idx = idx_before_vm[0] if len(idx_before_vm) > 0 else 200
    VIL_num = Vin_vals[vil_idx]
    
    # VIH: after VM
    idx_after_vm = np.where((Vin_vals > 2.5) & (dvdv >= -1.0))[0]
    vih_idx = idx_after_vm[0] if len(idx_after_vm) > 0 else 300
    VIH_num = Vin_vals[vih_idx]
    
    NML = VIL_num - 0.0
    NMH = VDD - VIH_num
    print(f"  Numerical VIL = {VIL_num:.3f} V")
    print(f"  Numerical VIH = {VIH_num:.3f} V")
    print(f"  Noise Margin Low  NML = {NML:.3f} V")
    print(f"  Noise Margin High NMH = {NMH:.3f} V")
    
    # Ron calculation
    Ron_n = 1.0 / (Kn_prime * (Wn/Ln) * (VDD - Vthn))
    Ron_p = 1.0 / (Kp_prime * (Wp/Lp) * (VDD - abs(Vthp)))
    print(f"\nEquivalent On-Resistance:")
    print(f"  Ron_n = {Ron_n:.1f} Ohm ({Ron_n/1e3:.3f} kOhm)")
    print(f"  Ron_p = {Ron_p:.1f} Ohm ({Ron_p/1e3:.3f} kOhm)")
    
    CL = 50e-15 # 50 fF
    tpHL = 0.69 * Ron_n * CL
    tpLH = 0.69 * Ron_p * CL
    tpd = 0.5 * (tpHL + tpLH)
    print(f"\nDelay Estimation (CL = 50 fF):")
    print(f"  tpHL (theoretical) = {tpHL*1e12:.2f} ps")
    print(f"  tpLH (theoretical) = {tpLH*1e12:.2f} ps")
    print(f"  tpd  (theoretical) = {tpd*1e12:.2f} ps")
    
    # Post-layout Parasitic addition:
    # Diffusion cap approx 15 fF, wire cap 8.5 fF -> total CL_eff = 50 + 23.5 = 73.5 fF
    CL_post = CL + 23.5e-15
    tpd_post = 0.69 * 0.5 * (Ron_n + Ron_p) * CL_post
    print(f"  tpd (post-layout PEX approx, CL_eff=73.5fF) = {tpd_post*1e12:.2f} ps (+{((tpd_post-tpd)/tpd)*100:.1f}%)")

if __name__ == "__main__":
    verify_lab00()
    verify_lab01()
