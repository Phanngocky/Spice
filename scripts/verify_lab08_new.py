#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for VLSI Lab 8: 6T SRAM Cell & Voltage Latch Sense Amplifier
MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

import math

def solve_vq_read(cr, vdd=5.0, vtn0=0.70, gamma=0.53, phi2=0.65, use_body=False):
    """
    Exact quadratic current balance for Read '0':
    Access (sat) = Driver (triode)
    0.5 * (u_ax - Vq)^2 = CR * ((u_d)*Vq - 0.5*Vq^2)
    """
    u_d = vdd - vtn0
    vq = 0.7
    for _ in range(100):
        if use_body:
            vtn_ax = vtn0 + gamma * (math.sqrt(phi2 + vq) - math.sqrt(phi2))
        else:
            vtn_ax = vtn0
        u_ax = vdd - vtn_ax
        # Solve 0.5*(u_ax - vq)^2 = cr * (u_d*vq - 0.5*vq^2)
        # (0.5 + 0.5*cr)*vq^2 - (u_ax + cr*u_d)*vq + 0.5*u_ax^2 = 0
        a = 0.5 * (1.0 + cr)
        b = -(u_ax + cr * u_d)
        c = 0.5 * (u_ax ** 2)
        disc = b**2 - 4*a*c
        vq_next = (-b - math.sqrt(disc)) / (2*a)
        if abs(vq_next - vq) < 1e-6:
            break
        vq = vq_next
    return vq

def solve_vq_write0(vdd=5.0, vtn0=0.70, vtp0=0.80, kp_n=120e-6, kp_p=40e-6, w_ax=2.0, w_l=1.0):
    """
    Write '0' equilibrium: Access NMOS (4lambda -> W/L=2) pulling down against Load PMOS (2lambda -> W/L=1)
    At Q low, Access is in triode (V_DS = Vq, V_GS = Vdd), Load PMOS is in sat (V_SD = Vdd - Vq, V_SG = Vdd).
    """
    bn = kp_n * w_ax
    bp = kp_p * w_l
    u_n = vdd - vtn0
    u_p = vdd - vtp0
    # bn*(u_n*vq - 0.5*vq^2) = 0.5*bp*(u_p)^2
    rhs = 0.5 * (bp / bn) * (u_p ** 2)
    # 0.5*vq^2 - u_n*vq + rhs = 0
    vq = u_n - math.sqrt(u_n**2 - 2*rhs)
    return vq

def inv_vtc_hold(vin, vdd=5.0, vtn0=0.70, vtp0=0.80, kp_n=120e-6, kp_p=40e-6, wd=4.0, wl=1.0):
    """
    Solves Vout for a given Vin of the SRAM inverter (Driver W/L=4, Load W/L=1) in Hold mode.
    """
    bn = kp_n * wd
    bp = kp_p * wl
    if vin <= vtn0:
        return vdd
    if vin >= vdd - vtp0:
        return 0.0
    
    # Bisection for Vout in [0, vdd] where Id_n(vin, vout) = Id_p(vin, vout)
    lo, hi = 0.0, vdd
    for _ in range(60):
        vout = 0.5 * (lo + hi)
        # NMOS current
        vov_n = vin - vtn0
        if vout < vov_n:
            id_n = bn * (vov_n * vout - 0.5 * vout**2)
        else:
            id_n = 0.5 * bn * (vov_n ** 2)
        # PMOS current
        vov_p = vdd - vin - vtp0
        vsd_p = vdd - vout
        if vsd_p < vov_p:
            id_p = bp * (vov_p * vsd_p - 0.5 * vsd_p**2)
        else:
            id_p = 0.5 * bp * (vov_p ** 2)
        if id_n > id_p:
            hi = vout  # Vout needs to go lower to reduce id_n / increase id_p
        else:
            lo = vout
    return 0.5 * (lo + hi)

def inv_vtc_read(vin, vdd=5.0, vtn0=0.70, vtp0=0.80, kp_n=120e-6, kp_p=40e-6, wd=4.0, wl=1.0, wax=2.0, gamma=0.53, phi2=0.65):
    """
    Solves Vout for a given Vin of the SRAM inverter in Read mode (BL = 5V, WL = 5V).
    Access NMOS pulls Vout UP toward Vdd - Vtn(Vout).
    """
    bn = kp_n * wd
    bp = kp_p * wl
    bax = kp_n * wax
    
    lo, hi = 0.0, vdd
    for _ in range(60):
        vout = 0.5 * (lo + hi)
        # Driver NMOS pulls DOWN
        vov_n = max(0.0, vin - vtn0)
        if vout < vov_n:
            id_n = bn * (vov_n * vout - 0.5 * vout**2)
        else:
            id_n = 0.5 * bn * (vov_n ** 2)
            
        # Load PMOS pulls UP
        vov_p = max(0.0, vdd - vin - vtp0)
        vsd_p = vdd - vout
        if vsd_p < vov_p:
            id_p = bp * (vov_p * vsd_p - 0.5 * vsd_p**2)
        else:
            id_p = 0.5 * bp * (vov_p ** 2)
            
        # Access NMOS pulls UP (Gate=Vdd, Drain=Vdd, Source=Vout)
        vtn_ax = vtn0 + gamma * (math.sqrt(phi2 + vout) - math.sqrt(phi2))
        vov_ax = max(0.0, vdd - vout - vtn_ax)
        id_ax = 0.5 * bax * (vov_ax ** 2)  # Always in sat when Vds = Vdd - Vout > Vov_ax
        
        if id_n > (id_p + id_ax):
            hi = vout
        else:
            lo = vout
    return 0.5 * (lo + hi)

def calc_snm(vtc_func):
    """
    Computes SNM via 45-degree coordinate rotation for symmetric inverters.
    u = (x_plot - y_plot)/sqrt(2), v = (x_plot + y_plot)/sqrt(2)
    In the upper-left lobe (x_plot < y_plot):
      Curve 1: (x, f(x)) for x in [0, V_M]  (top-right boundary)
      Curve 2: (f(x), x) for x in [V_M, Vdd] (bottom-left boundary)
    At the same u, the inscribed square side is (v1(u) - v2(u)) / sqrt(2).
    """
    s2 = math.sqrt(2.0)
    xs = [i * 0.005 for i in range(1001)]
    ys = [vtc_func(x) for x in xs]

    # Find V_M where x == y
    vm = 0.0
    for x, y in zip(xs, ys):
        if x >= y:
            vm = x
            break

    # Store (u, v) for both curves in upper-left lobe
    pts1 = [((x - y)/s2, (x + y)/s2) for x, y in zip(xs, ys) if x <= vm]
    pts2 = [((y - x)/s2, (y + x)/s2) for x, y in zip(xs, ys) if x >= vm]
    pts1.sort(key=lambda t: t[0])
    pts2.sort(key=lambda t: t[0])

    def interp_v(pts, u_target):
        for i in range(len(pts) - 1):
            if pts[i][0] <= u_target <= pts[i+1][0]:
                du = pts[i+1][0] - pts[i][0]
                if du < 1e-12:
                    return pts[i][1]
                t = (u_target - pts[i][0]) / du
                return pts[i][1] + t * (pts[i+1][1] - pts[i][1])
        return None

    u_min = max(pts1[0][0], pts2[0][0])
    u_max = min(pts1[-1][0], pts2[-1][0])
    max_s = 0.0
    for i in range(1, 500):
        u_t = u_min + i * (u_max - u_min) / 500.0
        v1 = interp_v(pts1, u_t)
        v2 = interp_v(pts2, u_t)
        if v1 is not None and v2 is not None:
            s = abs(v1 - v2) / s2
            if s > max_s:
                max_s = s
    return max_s, vm

def main():
    print("=" * 75)
    print("VLSI LAB 08 - 6T SRAM CELL & SENSE AMPLIFIER VERIFICATION")
    print("MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)")
    print("=" * 75)

    # 1. READ '0' V_Q TABLE ACROSS CR
    print("\n[1] READ '0' VOLTAGE BUMP V_Q vs CELL RATIO (CR)")
    print("|  CR  | V_Q (no body) | V_Q (with body) | Old Approx 4.3/(2*CR) |")
    print("|:----:|:-------------:|:---------------:|:---------------------:|")
    for cr in (1.0, 1.5, 2.0, 2.5, 3.0, 3.07, 4.0):
        vq0 = solve_vq_read(cr, use_body=False)
        vqb = solve_vq_read(cr, use_body=True)
        approx = 4.3 / (2.0 * cr)
        print(f"| {cr:4.2f} |    {vq0:6.3f} V   |     {vqb:6.3f} V    |        {approx:6.3f} V       |")

    # 2. WRITE '0' & TRIP VOLTAGES
    print("\n[2] WRITE '0' EQUILIBRIUM & INVERTER TRIP VOLTAGES (Driver 8λ, Access 4λ, Load 2λ)")
    vq_wr = solve_vq_write0()
    snm_hold, vm_hold = calc_snm(inv_vtc_hold)
    snm_read, vm_read = calc_snm(inv_vtc_read)
    print(f"  Pull ratio with mobility (Access/Load) = (120*2)/(40*1) = 6.0x (W/L PR = 0.5)")
    print(f"  Write '0' equilibrium Q voltage = {vq_wr:.3f} V (well below V_M = {vm_hold:.3f} V)")
    print(f"  Inverter V_M (Hold mode) = {vm_hold:.3f} V  -> SNM_hold = {snm_hold:.3f} V ({snm_hold/5.0*100:.1f}% VDD)")
    print(f"  Inverter V_M (Read mode) = {vm_read:.3f} V  -> SNM_read = {snm_read:.3f} V ({snm_read/5.0*100:.1f}% VDD)")
    print(f"  Ratio SNM_read / SNM_hold = {snm_read/snm_hold:.3f}")

    # 3. SENSE AMPLIFIER ROUGH LATCH TIME
    print("\n[3] VLSA ROUGH LATCH TIME ESTIMATION")
    print("  Topology (from sense_amp_tran.sp): Cross-coupled INV (12λ P / 8λ N) + Tail NMOS (12λ) + Pass NMOS (4λ)")
    print("  With C_so = C_sob = 20 fF, Delta_V_in = +/- 150 mV -> Delta_V_out ≈ 4.5 V (ln 30 ≈ 3.4)")
    print("  Rough analytical t_latch ≈ (C/gm)*ln(30) ≈ 70 - 200 ps (must be measured in SPICE).")

if __name__ == '__main__':
    main()
