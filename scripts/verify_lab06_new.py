#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for VLSI Lab 6: 1-bit Full Adder (Mirror Adder 28T & TG Adder)
MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

def main():
    print("=" * 75)
    print("VLSI LAB 06 - 1-BIT FULL ADDER VERIFICATION")
    print("MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)")
    print("=" * 75)

    # 1. VERIFY ALL 8 TRUTH TABLE COMBINATIONS & MIRROR ADDER EQUATIONS
    print("\n[1] TRUTH TABLE & MIRROR ADDER EQUATION VERIFICATION (ALL 8 INPUTS)")
    print("| A | B | Cin | Sum (true) | Cout (true) | ~Cout_bar | PDN_Sum = Sum | Match? |")
    print("|---|---|-----|------------|-------------|-----------|---------------|--------|")
    all_ok = True
    for a in (0, 1):
        for b in (0, 1):
            for cin in (0, 1):
                s_true = a ^ b ^ cin
                c_true = (a & b) | (cin & (a | b))
                
                # Mirror Adder Carry PDN: A*B + Cin*(A+B) -> outputs Cout_bar = ~(A*B + Cin*(A+B))
                cout_bar = 1 - ((a & b) | (cin & (a | b)))
                cout_inv = 1 - cout_bar
                
                # Mirror Adder Sum PDN: A*B*Cin + Cout_bar*(A + B + Cin)
                # Note: PDN pulls down when this expression is 1, so output of stage is Sum_bar = ~Sum!
                pdn_sum = (a & b & cin) | (cout_bar & (a | b | cin))
                sum_inv = pdn_sum  # After stage inverter, Sum = PDN_Sum!
                
                ok = (cout_inv == c_true) and (sum_inv == s_true)
                if not ok:
                    all_ok = False
                print(f"| {a} | {b} |  {cin}  |     {s_true}      |      {c_true}      |     {cout_inv}     |       {sum_inv}       |  {'OK' if ok else 'FAIL'}   |")
    assert all_ok, "Boolean verification failed!"
    print("-> Verified: Sum = A*B*Cin + (~Cout)*(A+B+Cin) is the PDN function (stage output is ~Sum).")

    # 2. TRANSISTOR COUNT & TOTAL WIDTH (MIRROR ADDER 28T)
    print("\n[2] MIRROR ADDER TRANSISTOR COUNT & SIZING")
    # Carry block: 5 NMOS (W=8lambda), 5 PMOS (W=24lambda), + INV_X1 (4lambda N + 12lambda P)
    # Sum block: 7 NMOS (W=12lambda), 7 PMOS (W=36lambda), + INV_X1 (4lambda N + 12lambda P)
    n_carry = 5 + 1  # 6 NMOS
    p_carry = 5 + 1  # 6 PMOS
    n_sum = 7 + 1    # 8 NMOS
    p_sum = 7 + 1    # 8 PMOS
    total_t = n_carry + p_carry + n_sum + p_sum
    
    w_carry_n = 5 * 8 + 4    # 44 lambda
    w_carry_p = 5 * 24 + 12  # 132 lambda
    w_sum_n = 7 * 12 + 4     # 88 lambda
    w_sum_p = 7 * 36 + 12    # 264 lambda
    sigma_w = w_carry_n + w_carry_p + w_sum_n + w_sum_p
    
    print(f"  Carry block: 5N + 5P (10T) + INV_Cout (2T) = 12T")
    print(f"  Sum block:   7N + 7P (14T) + INV_Sum (2T)  = 16T")
    print(f"  Total Mirror Adder: {total_t} Transistors (NOT 24 or 24-28!)")
    print(f"  Total Channel Width Sigma_W = {sigma_w} lambda = {sigma_w * 0.30:.1f} um")
    
    # Input gate width on Cin pin:
    # Carry: 1N (8lambda) + 1P (24lambda) = 32lambda
    # Sum: 1N (12lambda, series) + 1P (36lambda, series) + 1N (12lambda, parallel) + 1P (36lambda, parallel) = 96lambda
    w_cin = (8 + 24) + (12 + 36 + 12 + 36)
    c_ox_assumed = 2.5e-15  # 2.5 fF/um^2 (approximate)
    l_eff = 0.60  # um
    c_in_est = w_cin * 0.30 * l_eff * c_ox_assumed * 1e15
    print(f"  Total Gate Width on Cin pin = {w_cin} lambda (8x INV_X1's 16 lambda)")
    print(f"  Estimated Cin capacitance (assuming Cox ≈ 2.5 fF/um^2) ≈ {c_in_est:.1f} fF")

    # 3. EULER PATH FOR CARRY STAGE (5 TRANSISTORS: A, B, Cin, A, B)
    print("\n[3] EULER PATH FOR CARRY STAGE (5 TRANSISTORS)")
    print("  PDN nodes: out (deg 2), n1 (A-B series, deg 2), n2 (Cin-(A||B), deg 3), gnd (deg 3)")
    print("  Odd-degree vertices: gnd (3) and n2 (3). Euler path must start at one and end at the other.")
    print("  Valid 5-transistor Euler path: B - A - Cin - A - B (same for PUN due to self-duality!)")
    print("  Note: A 3-element 'A - B - Cin' order is incomplete because Carry has 5 transistors.")

    # 4. TG ADDER TRANSISTOR COUNT (FROM tg_adder_tran.sp)
    print("\n[4] TG ADDER TRANSISTOR COUNT")
    print("  Architecture in tg_adder_tran.sp:")
    print("    - X_xor1 (2 INV + 2 TG) = 8T")
    print("    - X_inv_p (1 INV for P_n) = 2T")
    print("    - X_xor2 (2 INV + 2 TG) = 8T")
    print("    - MUX2_C (2 TG using P and P_n) = 4T")
    print("    -> Total = 22 Transistors (can be optimized to 16T if sharing internal inverted signals).")

    # 5. 4-BIT RCA CRITICAL PATH WEIGHTS
    print("\n[5] 4-BIT RCA CRITICAL PATH")
    print("  Path to Cout_3: 4 carry stages -> coefficient = 4 for t_pd(Cin -> Cout)")
    print("  Path to Sum_3:  t(A,B -> Cout_0) + 2*t(Cin -> Cout) + t(Cin -> Sum_3) -> 3 carry stages + 1 Sum stage")
    print("  Elmore scaling for N=1..4 unbuffered TG stages: N(N+1)/2 = 1, 3, 6, 10 (at N=4, 10x single stage, not 340ps fixed).")

if __name__ == '__main__':
    main()
