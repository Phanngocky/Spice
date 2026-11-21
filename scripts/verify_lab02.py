"""
Verification and Numerical Benchmark Generator for Lab 02:
Static CMOS NAND2 and NOR2 Gates
"""
import math

def verify_lab02():
    print("="*60)
    print("VERIFICATION: LAB 02 (CMOS NAND2 & NOR2 GATES)")
    print("="*60)
    
    VDD = 5.0
    Vthn = 0.70
    Vthp = -0.80
    Kn_prime = 120e-6   # A/V^2
    Kp_prime = 40e-6    # A/V^2
    
    # Reference Inverter (INV_X1): Wn=1.2u, Wp=3.6u, L=0.6u
    # Ron_n0 ~ 969 Ohm, Ron_p0 ~ 992 Ohm
    
    # 1. NAND2 Sizing:
    # 2 NMOS in series -> Wn = 2 * 1.2u = 2.4u (8 lambda)
    # 2 PMOS in parallel -> Wp = 3.6u (12 lambda)
    Wn_nand = 2.4e-6
    Wp_nand = 3.6e-6
    L = 0.6e-6
    
    Ron_n_nand = 1.0 / (Kn_prime * (Wn_nand/L) * (VDD - Vthn)) # per transistor
    Req_N_nand = 2 * Ron_n_nand # two in series
    
    Ron_p_nand = 1.0 / (Kp_prime * (Wp_nand/L) * (VDD - abs(Vthp))) # per transistor
    Req_P_worst_nand = Ron_p_nand # 1 PMOS ON
    Req_P_best_nand = Ron_p_nand / 2.0 # 2 PMOS ON
    
    print(f"NAND2 Sizing:")
    print(f"  NMOS: W = {Wn_nand*1e6:.1f}u, L = {L*1e6:.1f}u (Req_N = {Req_N_nand:.1f} Ohm)")
    print(f"  PMOS: W = {Wp_nand*1e6:.1f}u, L = {L*1e6:.1f}u (Req_P_worst = {Req_P_worst_nand:.1f} Ohm, Req_P_best = {Req_P_best_nand:.1f} Ohm)")
    
    CL = 50e-15 # 50 fF
    tpHL_nand = 0.69 * Req_N_nand * CL
    tpLH_worst_nand = 0.69 * Req_P_worst_nand * CL
    tpLH_best_nand = 0.69 * Req_P_best_nand * CL
    tpd_worst_nand = 0.5 * (tpHL_nand + tpLH_worst_nand)
    
    print(f"NAND2 Delay (CL = 50 fF):")
    print(f"  tpHL = {tpHL_nand*1e12:.2f} ps")
    print(f"  tpLH (worst: 1 PMOS) = {tpLH_worst_nand*1e12:.2f} ps")
    print(f"  tpLH (best:  2 PMOS) = {tpLH_best_nand*1e12:.2f} ps")
    print(f"  tpd (worst) = {tpd_worst_nand*1e12:.2f} ps")
    
    # 2. NOR2 Sizing:
    # 2 PMOS in series -> Wp = 2 * 3.6u = 7.2u (24 lambda)
    # 2 NMOS in parallel -> Wn = 1.2u (4 lambda)
    Wp_nor = 7.2e-6
    Wn_nor = 1.2e-6
    
    Ron_p_nor = 1.0 / (Kp_prime * (Wp_nor/L) * (VDD - abs(Vthp))) # per transistor
    Req_P_nor = 2 * Ron_p_nor # two in series
    
    Ron_n_nor = 1.0 / (Kn_prime * (Wn_nor/L) * (VDD - Vthn)) # per transistor
    Req_N_worst_nor = Ron_n_nor # 1 NMOS ON
    Req_N_best_nor = Ron_n_nor / 2.0 # 2 NMOS ON
    
    print(f"\nNOR2 Sizing:")
    print(f"  PMOS: W = {Wp_nor*1e6:.1f}u, L = {L*1e6:.1f}u (Req_P = {Req_P_nor:.1f} Ohm)")
    print(f"  NMOS: W = {Wn_nor*1e6:.1f}u, L = {L*1e6:.1f}u (Req_N_worst = {Req_N_worst_nor:.1f} Ohm, Req_N_best = {Req_N_best_nor:.1f} Ohm)")
    
    tpLH_nor = 0.69 * Req_P_nor * CL
    tpHL_worst_nor = 0.69 * Req_N_worst_nor * CL
    tpHL_best_nor = 0.69 * Req_N_best_nor * CL
    tpd_worst_nor = 0.5 * (tpLH_nor + tpHL_worst_nor)
    
    print(f"NOR2 Delay (CL = 50 fF):")
    print(f"  tpLH = {tpLH_nor*1e12:.2f} ps")
    print(f"  tpHL (worst: 1 NMOS) = {tpHL_worst_nor*1e12:.2f} ps")
    print(f"  tpHL (best:  2 NMOS) = {tpHL_best_nor*1e12:.2f} ps")
    print(f"  tpd (worst) = {tpd_worst_nor*1e12:.2f} ps")
    
    # 3. Comparison PPA:
    # Total Gate Width (Transistor area indicator):
    Area_nand = 2 * Wn_nand + 2 * Wp_nand # 2*2.4 + 2*3.6 = 12.0 um
    Area_nor = 2 * Wp_nor + 2 * Wn_nor   # 2*7.2 + 2*1.2 = 16.8 um
    print(f"\nPPA Comparison:")
    print(f"  Total Transistor Width: NAND2 = {Area_nand*1e6:.1f} um vs NOR2 = {Area_nor*1e6:.1f} um (+{((Area_nor-Area_nand)/Area_nand)*100:.1f}%)")
    print(f"  Input Capacitance (Pin A): NAND2 (Wn+Wp = 6.0u) vs NOR2 (Wn+Wp = 8.4u, +40%)")

if __name__ == "__main__":
    verify_lab02()
