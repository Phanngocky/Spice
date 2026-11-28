#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for VLSI Lab 5: Sequential Circuits (D-Latch & Master-Slave DFF)
MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

def main():
    print("=" * 75)
    print("VLSI LAB 05 - SEQUENTIAL CIRCUITS (D-LATCH & DFF) VERIFICATION")
    print("MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)")
    print("=" * 75)

    # 1. FEEDBACK INVERTER I3 SIZING ANALYSIS (IF TG2 WERE OMITTED)
    print("\n[1] FEEDBACK INVERTER I3 ANALYSIS (TOPOLOGY A vs TOPOLOGY B)")
    vdd = 5.0
    vm_i1 = 2.45  # Switching threshold of I1 (INV_X1, from Lab 1)
    r_tg = 1190.0  # Ohms (from Lab 4)
    
    # R_on for W=4lambda (1.2um), L=2lambda (0.6um)
    # NMOS: Kp=120u, W/L=2, Vov=4.3V -> Ron = 969 Ohm
    # PMOS: Kp=40u, W/L=2, Vov=4.2V -> Ron = 2976 Ohm
    r_n_2l = 1.0 / (120e-6 * 2.0 * 4.3)
    r_p_2l = 1.0 / (40e-6 * 2.0 * 4.2)
    
    # Writing '1' against I3 pulling down; Writing '0' against I3 pulling up
    vx_write1_2l = vdd * r_n_2l / (r_n_2l + r_tg)
    vx_write0_2l = vdd * r_tg / (r_tg + r_p_2l)
    
    # With L = 4lambda (1.2um), W=4lambda (1.2um) -> W/L = 1 -> R doubles
    r_n_4l = 2.0 * r_n_2l
    r_p_4l = 2.0 * r_p_2l
    vx_write1_4l = vdd * r_n_4l / (r_n_4l + r_tg)
    vx_write0_4l = vdd * r_tg / (r_tg + r_p_4l)
    
    print(f"I1 switching threshold V_M ≈ {vm_i1:.2f} V; TG1 resistance R_TG ≈ {r_tg:.0f} Ω")
    print("\nIf TG2 is OMITTED (Ratioed Weak Feedback Topology B):")
    print(f"  Case 1: I3 has W=4λ, L=2λ (R_n={r_n_2l:.0f} Ω, R_p={r_p_2l:.0f} Ω):")
    print(f"    Write '1': V_X = {vx_write1_2l:.3f} V  ({'PASS > V_M' if vx_write1_2l > vm_i1 else 'FAIL < V_M !'})")
    print(f"    Write '0': V_X = {vx_write0_2l:.3f} V  ({'PASS < V_M' if vx_write0_2l < vm_i1 else 'FAIL > V_M !'})")
    print(f"  Case 2: I3 has W=4λ, L=4λ (R_n={r_n_4l:.0f} Ω, R_p={r_p_4l:.0f} Ω):")
    print(f"    Write '1': V_X = {vx_write1_4l:.3f} V  ({'PASS > V_M' if vx_write1_4l > vm_i1 else 'FAIL < V_M !'})")
    print(f"    Write '0': V_X = {vx_write0_4l:.3f} V  ({'PASS < V_M' if vx_write0_4l < vm_i1 else 'FAIL > V_M !'})")
    print("\nConclusion: With TG2 PRESENT (Topology A, standard in Fig 5.1), TG1 and TG2 never")
    print("conduct simultaneously in steady state (except ~t_pd,inv clock skew overlap),")
    print("so I3 does NOT fight TG1 and can be minimum size (4λ/2λ) purely to hold X against leakage.")

    # 2. TIMING PATHS & NOMINAL DELAYS
    print("\n[2] TIMING PATHS (USING LAB 1 & LAB 4 ILLUSTRATIVE DELAYS)")
    t_inv = 34.0  # ps
    t_tg = 42.0   # ps
    
    t_pd_latch = t_tg + 2 * t_inv
    t_cq_full = 3 * t_inv + t_tg  # CLK -> CLK_b -> TG_S1 -> I_S1 -> I_S2 -> Q
    t_cq_direct = 2 * t_inv + t_tg  # Direct NMOS path without CLK_b delay
    t_setup_est = t_tg + t_inv
    t_hold_est = t_inv  # Overlap time due to CLK_b delay
    
    t_min_full = t_cq_full + t_setup_est
    f_max_full = 1000.0 / t_min_full  # GHz
    
    print(f"  Illustrative stage delays: t_pd,INV = {t_inv:.0f} ps, t_pd,TG = {t_tg:.0f} ps")
    print(f"  D-Latch transparent delay t_pd(D->Q) = TG1 + I1 + I2 = {t_pd_latch:.0f} ps")
    print(f"  DFF t_c-q (old buggy formula missing I2) = {t_inv + t_tg + t_inv:.0f} ps")
    print(f"  DFF t_c-q (full path: CLK_inv + TG_S1 + I_S1 + I_S2) = {t_cq_full:.0f} ps")
    print(f"  DFF t_setup (theoretical estimate: TG_M1 + I_M1) = {t_setup_est:.0f} ps")
    print(f"  DFF t_hold (theoretical estimate: CLK_inv skew) ≈ {t_hold_est:.0f} ps")
    print(f"  Register-to-register bare T_min = t_c-q + t_setup = {t_min_full:.0f} ps (1/T_min ≈ {f_max_full:.2f} GHz)")
    print("  Note: Real synchronous clock period T_clk >= t_c-q + t_comb,max + t_setup + t_skew.")

    # 3. TRANSISTOR COUNT
    print("\n[3] TRANSISTOR COUNT")
    print("  D-Latch (dlatch_x1): 2 TG (4T) + 3 INV (6T) = 10 Transistors")
    print("  Master-Slave DFF (dff_ms_x1): 2 x D-Latch (20T) + 1 Clock INV (2T) = 22 Transistors")

if __name__ == '__main__':
    main()
