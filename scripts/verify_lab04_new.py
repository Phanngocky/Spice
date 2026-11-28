#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for VLSI Lab 4: Transmission Gate and MUX
MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

import math

def solve_nmos_weak1(vdd, vth0, gamma, phi2):
    """
    Fixed-point solver for NMOS Weak '1':
    Vout = VDD - Vtn(Vout)
    Vtn(Vout) = Vth0 + gamma * (sqrt(phi2 + Vout) - sqrt(phi2))
    """
    vout = 3.5  # initial guess
    for _ in range(100):
        vtn = vth0 + gamma * (math.sqrt(phi2 + vout) - math.sqrt(phi2))
        vout_next = vdd - vtn
        if abs(vout_next - vout) < 1e-6:
            break
        vout = vout_next
    return vout, vtn

def solve_pmos_weak0(vdd, vth0_p, gamma_p, phi2_p):
    """
    Fixed-point solver for PMOS Weak '0':
    Bulk is at VDD, Source is at Vout -> V_BS = VDD - Vout
    PMOS cuts off when Vout <= |Vtp(V_BS)|
    |Vtp(V_BS)| = |Vth0_p| + gamma_p * (sqrt(phi2_p + (VDD - Vout)) - sqrt(phi2_p))
    """
    vout = 1.0  # initial guess
    for _ in range(100):
        vbs = vdd - vout
        vtp = vth0_p + gamma_p * (math.sqrt(phi2_p + vbs) - math.sqrt(phi2_p))
        vout_next = vtp
        if abs(vout_next - vout) < 1e-6:
            break
        vout = vout_next
    return vout, vtp

def calc_tg_resistance(vdd, vth0_n, gamma_n, phi2_n, kp_n, wn, ln,
                       vth0_p, gamma_p, phi2_p, kp_p, wp, lp,
                       use_body_effect=False):
    """
    Calculates Ron_n, Ron_p, and R_TG across Vin = 0.0 to 5.0V
    """
    beta_n = kp_n * (wn / ln)
    beta_p = kp_p * (wp / lp)
    
    results = []
    vin_steps = [round(x * 0.5, 1) for x in range(11)]
    
    for vin in vin_steps:
        # NMOS: Gate = VDD = 5V, Source = Vin, Bulk = 0V
        # VSB_n = Vin
        if use_body_effect:
            vtn = vth0_n + gamma_n * (math.sqrt(phi2_n + vin) - math.sqrt(phi2_n))
        else:
            vtn = vth0_n
            
        vov_n = vdd - vin - vtn
        if vov_n > 0:
            ron_n = 1.0 / (beta_n * vov_n)
        else:
            ron_n = float('inf')
            
        # PMOS: Gate = 0V, Source = Vin (for Vin near VDD) or Source is Vout.
        # When Vin is high, VSB_p = VDD - Vin
        if use_body_effect:
            vsb_p = max(0.0, vdd - vin)
            vtp = vth0_p + gamma_p * (math.sqrt(phi2_p + vsb_p) - math.sqrt(phi2_p))
        else:
            vtp = vth0_p
            
        vov_p = vin - vtp
        if vov_p > 0:
            ron_p = 1.0 / (beta_p * vov_p)
        else:
            ron_p = float('inf')
            
        # Parallel combination
        if ron_n == float('inf') and ron_p == float('inf'):
            r_tg = float('inf')
        elif ron_n == float('inf'):
            r_tg = ron_p
        elif ron_p == float('inf'):
            r_tg = ron_n
        else:
            r_tg = (ron_n * ron_p) / (ron_n + ron_p)
            
        results.append({
            'vin': vin,
            'vtn': vtn,
            'vtp': vtp,
            'ron_n': ron_n,
            'ron_p': ron_p,
            'r_tg': r_tg
        })
    return results

def main():
    print("=" * 75)
    print("VLSI LAB 04 - TRANSMISSION GATE & MUX VERIFICATION")
    print("MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)")
    print("=" * 75)
    
    # 1. BODY EFFECT & VOLTAGE LOSS
    print("\n[1] BODY EFFECT & VOLTAGE LOSS (WEAK '1' & WEAK '0')")
    
    # Case A: Generic textbook parameters (Audit reference)
    v_nmos_a, vtn_a = solve_nmos_weak1(vdd=5.0, vth0=0.70, gamma=0.53, phi2=0.65)
    v_pmos_a, vtp_a = solve_pmos_weak0(vdd=5.0, vth0_p=0.80, gamma_p=0.53, phi2_p=0.65)
    
    # Case B: Exact C5_models.txt parameters
    v_nmos_b, vtn_b = solve_nmos_weak1(vdd=5.0, vth0=0.70, gamma=0.40, phi2=0.70)
    v_pmos_b, vtp_b = solve_pmos_weak0(vdd=5.0, vth0_p=0.80, gamma_p=0.50, phi2_p=0.70)
    
    print("--- Case A: Textbook Parameters (gamma=0.53, 2phi_F=0.65) ---")
    print(f"  NMOS Weak '1': Vout,max = {v_nmos_a:.4f} V  (Vthn,eff = {vtn_a:.4f} V, Drop = {5.0 - v_nmos_a:.4f} V)")
    print(f"  PMOS Weak '0': Vout,min = {v_pmos_a:.4f} V  (|Vtp,eff| = {vtp_a:.4f} V, Rise = {v_pmos_a:.4f} V)")
    
    print("\n--- Case B: Exact C5N Parameters (gamma_n=0.40, gamma_p=0.50, 2phi_F=0.70) ---")
    print(f"  NMOS Weak '1': Vout,max = {v_nmos_b:.4f} V  (Vthn,eff = {vtn_b:.4f} V, Drop = {5.0 - v_nmos_b:.4f} V)")
    print(f"  PMOS Weak '0': Vout,min = {v_pmos_b:.4f} V  (|Vtp,eff| = {vtp_b:.4f} V, Rise = {v_pmos_b:.4f} V)")
    
    # Static leakage current through downstream inverter:
    # If downstream INV has Wp=12lambda=3.6u, Lp=2lambda=0.6u, Vin = Vout,max
    kp_p = 40.0e-6
    wp_lp = 3.6 / 0.6
    vsg_p_a = 5.0 - v_nmos_a
    vsg_p_b = 5.0 - v_nmos_b
    i_stat_a = 0.5 * kp_p * wp_lp * ((vsg_p_a - 0.80)**2) * 1e6
    i_stat_b = 0.5 * kp_p * wp_lp * ((vsg_p_b - 0.80)**2) * 1e6
    print(f"\nDownstream Inverter PMOS static leakage current:")
    print(f"  With Case A Weak '1' ({v_nmos_a:.3f}V): I_static ≈ {i_stat_a:.2f} uA")
    print(f"  With Case B Weak '1' ({v_nmos_b:.3f}V): I_static ≈ {i_stat_b:.2f} uA")
    
    # 2. TRANSMISSION GATE ON-RESISTANCE
    print("\n[2] TRANSMISSION GATE ON-RESISTANCE R_TG(Vin)")
    print("Sizing: NMOS 4lambda (1.2um), PMOS 12lambda (3.6um), L = 2lambda (0.6um)")
    print("beta_n = 120u * 2 = 240 uA/V^2; beta_p = 40u * 6 = 240 uA/V^2")
    
    res_no_body = calc_tg_resistance(vdd=5.0, vth0_n=0.70, gamma_n=0.53, phi2_n=0.65, kp_n=120e-6, wn=1.2, ln=0.6,
                                      vth0_p=0.80, gamma_p=0.53, phi2_p=0.65, kp_p=40e-6, wp=3.6, lp=0.6,
                                      use_body_effect=False)
                                      
    res_with_body = calc_tg_resistance(vdd=5.0, vth0_n=0.70, gamma_n=0.53, phi2_n=0.65, kp_n=120e-6, wn=1.2, ln=0.6,
                                        vth0_p=0.80, gamma_p=0.53, phi2_p=0.65, kp_p=40e-6, wp=3.6, lp=0.6,
                                        use_body_effect=True)
                                        
    print("\n| Vin (V) | Ron,n w/o Body (Ω) | Ron,p w/o Body (Ω) | R_TG w/o Body (Ω) | R_TG w/ Body (Ω) |")
    print("|:-------:|:-------------------:|:-------------------:|:-----------------:|:----------------:|")
    for r0, rb in zip(res_no_body, res_with_body):
        rn_str = f"{r0['ron_n']:.0f}" if r0['ron_n'] != float('inf') else "OFF"
        rp_str = f"{r0['ron_p']:.0f}" if r0['ron_p'] != float('inf') else "OFF"
        rtg0_str = f"{r0['r_tg']:.0f}" if r0['r_tg'] != float('inf') else "OFF"
        rtgb_str = f"{rb['r_tg']:.0f}" if rb['r_tg'] != float('inf') else "OFF"
        print(f"|  {r0['vin']:4.1f}   |        {rn_str:>6}       |        {rp_str:>6}       |      {rtg0_str:>6}       |      {rtgb_str:>6}      |")
        
    print("\nKey Takeaway on R_TG:")
    print("  - At full overdrive (V_GS = 5V): R_on,n(0V) = 1/(240u*4.3V) = 969 Ω; R_on,p(5V) = 1/(240u*4.2V) = 992 Ω.")
    print("  - At mid-rail (Vin = 2.5V): V_ov,n = 2.5 - 0.7 = 1.8V -> Ron,n = 2,315 Ω.")
    print("                              V_ov,p = 2.5 - 0.8 = 1.7V -> Ron,p = 2,451 Ω.")
    print("                              R_TG = 2315 || 2451 = 1,190.5 Ω ≈ 1.19 kΩ (FLAT across 1.0V - 4.0V)!")
    print("  - The old claim of '490 Ω' was completely wrong due to erroneously taking 969 || 992 without accounting for reduced gate overdrive!")
    
    # 3. ELMORE DELAY FOR CASCADED TG CHAINS
    print("\n[3] ELMORE DELAY FOR CASCADED TG CHAINS O(N^2)")
    r_tg = 1190.0  # Ohms
    c_node = 10.0e-15  # 10 fF per TG stage (diffusion parasitics)
    print(f"Assuming R_TG = {r_tg:.0f} Ω, C_node = {c_node*1e15:.1f} fF per stage:")
    print("| N stages | Sum i=1..N (i) | Elmore Delay t_pd (ps) | Ratio to N=1 |")
    print("|:--------:|:--------------:|:----------------------:|:------------:|")
    for n in range(1, 7):
        factor = n * (n + 1) / 2
        t_elmore = 0.69 * r_tg * c_node * factor * 1e12
        ratio = factor
        print(f"|    {n}     |       {factor:4.1f}     |        {t_elmore:6.2f} ps       |    {ratio:5.1f}x    |")
        
    print("This clearly demonstrates quadratic delay growth O(N^2).")
    print("Design Rule: Insert an inverting buffer every 3 to 4 transmission gates!")
    
    # 4. CONTENTION / OVERLAP TIME
    print("\n[4] MUX SELECT SWITCHING & CONTENTION OVERLAP")
    print("Select signal S is inverted to S_b by internal INV_X1.")
    print("INV_X1 delay: t_pd,inv ≈ 30 - 45 ps.")
    print("During S transition 0 -> 1:")
    print("  - TG1 (driven by S) begins turning ON immediately.")
    print("  - TG0 (driven by S_b) remains conductive for delta_t ≈ t_pd,inv.")
    print("  - If D0 != D1, a temporary short circuit path exists between D0 and D1 via node Y,")
    print("    generating an supply current spike I(Vdd) and output glitch.")
    
    # 5. TRANSISTOR COUNT & PPA COMPARISON
    print("\n[5] MUX2:1 & MUX4:1 TRANSISTOR COUNT & COMPLEXITY")
    print("| Circuit | Architecture | Transistor Count | Critical Path Gates | Level Restoration |")
    print("|:-------:|:------------:|:----------------:|:-------------------:|:-----------------:|")
    print("| MUX 2:1 | TG-based     | 6 T (2 TG + 1 INV) | 1 TG (passive)    | Non-restoring     |")
    print("| MUX 2:1 | Static CMOS  | 10 - 12 T (AOI22) | 2 Gates (active)    | Restoring         |")
    print("| MUX 4:1 | TG Tree (3x) | 18 T (6 TG + 3 INV)| 2 TG (passive)    | Non-restoring     |")
    print("| MUX 4:1 | Static CMOS  | 30 - 36 T        | 4 Gates (active)    | Restoring         |")
    
    print("\nLayout Dimensions:")
    print("  Cell Height H_cell = 40 lambda = 12.0 um")
    print("  MUX2_TG Width: 3 Poly columns (S, S_b, INV gate) + 4 diffusion contacts + taps ≈ 30 lambda = 9.0 um")
    print("  Cell Area ≈ 30 lambda x 40 lambda = 1200 lambda^2 = 108.0 um^2")

if __name__ == '__main__':
    main()
