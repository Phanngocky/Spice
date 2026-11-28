#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for VLSI Lab 9: 4-bit Carry Lookahead Adder (CLA)
MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

def main():
    print("=" * 75)
    print("VLSI LAB 09 - 4-BIT CARRY LOOKAHEAD ADDER (CLA) VERIFICATION")
    print("MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)")
    print("=" * 75)

    # 1. CLG TRANSISTOR COUNT & EQUAL-DRIVE SIZING
    print("\n[1] CLG_4B TRANSISTOR COUNT & EQUAL-DRIVE SIZING (INV_X1 = 4λ N, 12λ P)")
    clg_gates = [
        ("AOI21 (C1)",  [1, 2],          3, 2, 2),
        ("AOI321 (C2)", [1, 2, 3],       6, 3, 3),
        ("AOI4321 (C3)",[1, 2, 3, 4],   10, 4, 4),
        ("AOI54321(C4)",[1, 2, 3, 4, 5],15, 5, 5),
    ]
    total_aoi_t = 0
    sigma_w_fixed = 0
    sigma_w_equal = 0
    print("| Gate         | Branches | N=P | Depth N/P | Equal-Drive (Wn, Wp) | Fixed (8λ/24λ) T |")
    print("|:-------------|:--------:|:---:|:---------:|:--------------------:|:----------------:|")
    for name, branches, n_t, dn, dp in clg_gates:
        total_t_gate = 2 * n_t
        total_aoi_t += total_t_gate
        wn_eq = 4 * dn
        wp_eq = 12 * dp
        sigma_w_fixed += n_t * (8 + 24)
        sigma_w_equal += n_t * (wn_eq + wp_eq)
        print(f"| {name:12} | {str(branches):8} |  {n_t:2} |   {dn} / {dp}   |     {wn_eq:2}λ , {wp_eq:2}λ       |        {total_t_gate:2} T      |")
    
    # Add 4 output inverters (INV_X1: 4λ + 12λ = 16λ)
    total_clg_t = total_aoi_t + 4 * 2
    sigma_w_fixed += 4 * 16
    sigma_w_equal += 4 * 16
    print(f"  Total AOI transistors = {total_aoi_t} T + 4 INV (8 T) = {total_clg_t} T")
    print(f"  CLG Sigma_W (fixed 8λ/24λ) = {sigma_w_fixed} λ  ({sigma_w_fixed*0.3:.1f} um)")
    print(f"  CLG Sigma_W (equal-drive)  = {sigma_w_equal} λ  ({sigma_w_equal*0.3:.1f} um)")
    
    # Compare with 4x Mirror Adder RCA (Lab 6)
    rca_sigma_w = 4 * 528
    print(f"  4-bit RCA Sigma_W (4 x 528λ from Lab 6) = {rca_sigma_w} λ  ({rca_sigma_w*0.3:.1f} um)")

    # 2. TOTAL CLA TRANSISTOR COUNT vs XOR ARCHITECTURE
    print("\n[2] TOTAL CLA TRANSISTOR COUNT (vs 4-bit RCA = 112 T)")
    rca_t = 4 * 28
    for xor_t in (4, 6, 8):
        pg_t = 4 + 2 + xor_t  # NAND2 (4T) + INV (2T) + XOR
        sum_t = xor_t
        cla_t = total_clg_t + 4 * pg_t + 4 * sum_t
        pct = (cla_t - rca_t) / rca_t * 100.0
        print(f"  XOR = {xor_t} T -> PG = {pg_t:2} T, Sum = {sum_t} T -> Total CLA = {cla_t} T (+{pct:.1f}% vs RCA 112 T)")
    print("  Note: '134 T (+19.6%)' in the old handout cannot be reproduced from any XOR architecture!")

    # 3. SIGNAL FAN-IN & GATE LOAD IN CLG
    print("\n[3] SIGNAL FAN-IN & GATE LOAD IN CLG (FIXED 8λ/24λ)")
    # Count appearances across C1..C4:
    # C1: G0, P0, C0
    # C2: G1, P1*2, G0, P0, C0
    # C3: G2, P2*3, G1, P1*2, G0, P0, C0
    # C4: G3, P3*4, G2, P2*3, G1, P1*2, G0, P0, C0
    loads = {
        'P0': 4, 'P1': 6, 'P2': 6, 'P3': 4,
        'G0': 4, 'G1': 3, 'G2': 2, 'G3': 1, 'C0': 4
    }
    c_ox = 2.5e-15  # assumed 2.5 fF/um^2
    l_eff = 0.60
    for sig, cnt in loads.items():
        w_tot = cnt * (8 + 24)
        c_est = w_tot * 0.30 * l_eff * c_ox * 1e15
        print(f"  {sig:2}: appears {cnt} times -> W_gate = {w_tot:3} λ -> C_in ≈ {c_est:5.1f} fF ({w_tot/16:.1f}x INV_X1)")

    # 4. ROUGH ELMORE DELAY ESTIMATE (C0 -> C4)
    print("\n[4] ROUGH ELMORE DELAY ESTIMATE (C0 -> C4, FIXED 8λ/24λ)")
    r_n8 = 485.0  # Ohms for 8lambda NMOS
    c_out = 40.0e-15
    c_int = 4.5e-15
    # 5 series NMOS in AOI54321: C_out sees 5*R, plus 4 internal nodes (4+3+2+1 = 10)*R
    t_aoi5 = 0.69 * (c_out * 5 * r_n8 + c_int * 10 * r_n8) * 1e12
    t_inv = 35.0
    t_cla_c0_c4 = t_aoi5 + t_inv
    t_rca_4 = 4 * 60.0  # rough 60ps/stage from Lab 6
    improv = (t_rca_4 - t_cla_c0_c4) / t_rca_4 * 100.0
    print(f"  AOI54321 (5 series NMOS) ≈ {t_aoi5:.1f} ps + INV ≈ {t_inv:.0f} ps -> C0->C4 ≈ {t_cla_c0_c4:.1f} ps")
    print(f"  Rough RCA (4 x 60 ps) ≈ {t_rca_4:.0f} ps -> ~{improv:.1f}% reduction (NOT guaranteed > 60%!).")

if __name__ == '__main__':
    main()
