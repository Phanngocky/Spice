#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for VLSI Lab 7: Dynamic CMOS & Domino Logic
MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

import math

def main():
    print("=" * 75)
    print("VLSI LAB 07 - DYNAMIC CMOS & DOMINO LOGIC VERIFICATION")
    print("MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)")
    print("=" * 75)

    vdd = 5.0
    vtn0 = 0.70
    vtp0 = 0.80
    kp_n = 120e-6
    kp_p = 40e-6

    # 1. LOW-SKEW INVERTER (16lambda / 8lambda) SWITCHING THRESHOLD V_M
    print("\n[1] INVERTER SWITCHING THRESHOLD V_M (Wp=16lambda, Wn=8lambda, L=2lambda)")
    r_inv = math.sqrt((kp_p * (16.0 / 2.0)) / (kp_n * (8.0 / 2.0)))
    vm_domino = (vtn0 + r_inv * (vdd - vtp0)) / (1.0 + r_inv)
    
    # Compare with INV_X1 (12lambda / 4lambda)
    r_x1 = math.sqrt((kp_p * (12.0 / 2.0)) / (kp_n * (4.0 / 2.0)))
    vm_x1 = (vtn0 + r_x1 * (vdd - vtp0)) / (1.0 + r_x1)
    
    print(f"  INV_X1 (12λ/4λ): r = {r_x1:.4f} -> V_M = {vm_x1:.3f} V")
    print(f"  Domino INV (16λ/8λ): r = {r_inv:.4f} -> V_M = {vm_domino:.3f} V")
    print("  -> Since V_M = 2.273 V < 2.45 V (INV_X1), 16λ/8λ is LOW-SKEW (not High-skew!).")

    # 2. CHARGE SHARING ANALYSIS
    print("\n[2] CHARGE SHARING ANALYSIS")
    cx = 20.0e-15
    cint = 14.0e-15
    vx_prime = vdd * (cx / (cx + cint))
    dv_x = vdd - vx_prime
    nm_h_domino = vx_prime - vm_domino
    nm_h_x1 = vx_prime - vm_x1
    cint_crit_ratio = (vdd / vm_domino) - 1.0
    
    print(f"  Pre-lab case (Cx = 20 fF, Cint = 14 fF):")
    print(f"    V_X' = {vx_prime:.3f} V, Delta V_X = {dv_x:.3f} V")
    print(f"    NM_H (vs V_M = {vm_domino:.3f} V) = {nm_h_domino:.3f} V  (vs 2.45 V: {nm_h_x1:.3f} V)")
    print(f"    False switching condition (V_X' <= V_M): Cint >= {cint_crit_ratio:.2f} * Cx")

    # Check upper NMOS charging limit V_G - V_thn(V_SB)
    # Using C5N gamma=0.40, 2phi=0.70 -> V_int_max ≈ 3.787V (or 3.631V for gamma=0.53)
    v_int_max_c5n = 3.787
    ratio_thresh = (vdd - v_int_max_c5n) / vdd
    print(f"\n  Physical limit on upper NMOS charging Cint: V_max ≈ {v_int_max_c5n:.2f} V (C5N)")
    print(f"    Equalization formula holds only when Cint/(Cx+Cint) >= {ratio_thresh:.2f} (about 0.24 - 0.27).")
    # Small Cint case: Cint/Cx = 0.1
    dv_naive = vdd * (0.1 / 1.1)
    dv_phys = v_int_max_c5n * 0.1
    print(f"    For Cint/Cx = 0.1: Naive formula gives dV = {dv_naive:.3f} V, Physical limit dV <= {dv_phys:.3f} V")

    # 3. KEEPER CONTENTION CURRENT RATIOS (ROUGH LINEAR MODEL AT V_X = 2.5V)
    print("\n[3] KEEPER CONTENTION RATIOS (V_X = 2.5 V, L_kp = 2lambda)")
    v_sd = 2.5
    r_pdn_single = 969.0 + 485.0  # 4lambda branch + 8lambda foot
    i_pdn = v_sd / r_pdn_single * 1e3  # mA
    print(f"  Single PDN branch current (approx, R_eq ≈ {r_pdn_single:.0f} Ω) ≈ {i_pdn:.2f} mA")
    for w_kp in (2, 4, 6, 8):
        i_kp = kp_p * (w_kp / 2.0) * ((vdd - vtp0) * v_sd - 0.5 * v_sd**2) * 1e3
        ratio = i_kp / i_pdn
        print(f"    W_kp = {w_kp}λ (L=2λ): I_kp ≈ {i_kp:.2f} mA -> I_kp/I_PDN ≈ {ratio:.2f}")

    # 4. DOMINO OR4 vs STATIC OR4 AREA & INPUT CAPACITANCE
    print("\n[4] DOMINO OR4 vs STATIC OR4 (TOTAL WIDTH & C_in)")
    sw_domino = 12 + 8 + 4 * 4 + 2 + 16 + 8  # 62 lambda (or 64 with W_kp=4lambda)
    sw_static = (4 * 4 + 4 * 48) + (12 + 4)  # NOR4 (4N 4λ, 4P 48λ) + INV_X1 (16λ) = 224 lambda
    cin_domino = 4
    cin_static = 4 + 48
    print(f"  Domino OR4: 9T, Sigma_W = {sw_domino}λ (or {sw_domino+2}λ with W_kp=4λ), C_in/pin = {cin_domino}λ")
    print(f"  Static OR4: 10T, Sigma_W = {sw_static}λ, C_in/pin = {cin_static}λ ({cin_static/cin_domino:.0f}x larger!)")

if __name__ == '__main__':
    main()
