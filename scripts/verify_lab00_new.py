# -*- coding: utf-8 -*-
"""
Verification script for Lab 0 (Student Workbook & Teacher Book).
Tests all numerical benchmarks, equations, and limits.
"""

import math

def test_example_3_7():
    print("Testing Section 3.7 numerical illustration...")
    R = 10e3
    C = 2e-9
    tau = R * C
    t50 = math.log(2) * tau
    tr = math.log(9) * tau
    fc = 1.0 / (2 * math.pi * tau)
    
    assert abs(tau - 20e-6) < 1e-12, f"Tau mismatch: {tau}"
    assert abs(t50 - 13.8629e-6) < 1e-9, f"t50 mismatch: {t50}"
    assert abs(tr - 43.944e-6) < 1e-8, f"tr mismatch: {tr}"
    assert abs(fc - 7957.747) < 1.0, f"fc mismatch: {fc}"
    print("  [PASS] Section 3.7 values verified!")

def test_pre_lab():
    print("Testing Pre-lab questions...")
    # P2: Vin=10V, R1=15k, R2=10k
    Vin = 10.0
    R1 = 15e3
    R2 = 10e3
    Vout = Vin * R2 / (R1 + R2)
    I = Vin / (R1 + R2)
    slope = R2 / (R1 + R2)
    assert abs(Vout - 4.0) < 1e-9
    assert abs(I - 0.4e-3) < 1e-9
    assert abs(slope - 0.4000) < 1e-9
    
    # P3: R=5k, C=10nF, V0=5V
    R = 5e3
    C = 10e-9
    tau = R * C
    t50 = math.log(2) * tau
    tr = math.log(9) * tau
    fc = 1.0 / (2 * math.pi * tau)
    assert abs(tau - 50e-6) < 1e-12
    assert abs(t50 - 34.657e-6) < 1e-8
    assert abs(tr - 109.86e-6) < 1e-7
    assert abs(fc - 3183.1) < 0.5
    
    # P6: Ton = 3 tau
    Vc_3tau = 5.0 * (1 - math.exp(-3))
    assert abs(Vc_3tau - 4.75106) < 1e-4
    print("  [PASS] Pre-lab questions verified!")

def test_in_lab_rc():
    print("Testing In-lab Ex0.1 - Ex0.4...")
    # Ex0.1: Vin=5V, R1=12k, R2=18k
    Vin = 5.0
    R1 = 12e3
    R2 = 18e3
    Vout = Vin * R2 / (R1 + R2)
    I = Vin / (R1 + R2)
    slope_dc = R2 / (R1 + R2)
    assert abs(Vout - 3.0) < 1e-9
    assert abs(I - 0.166667e-3) < 1e-7
    assert abs(slope_dc - 0.6000) < 1e-9
    
    # Ex0.2: R=20k, C=5nF, V0=5V
    R = 20e3
    C = 5e-9
    tau = R * C
    t50 = math.log(2) * tau
    tr = math.log(9) * tau
    fc = 1.0 / (2 * math.pi * tau)
    
    # Peak currents
    I_peak_chg = 5.0 / R
    Vc_5tau = 5.0 * (1 - math.exp(-5))
    I_peak_dis = -Vc_5tau / R
    diff_percent = abs(abs(I_peak_dis) - I_peak_chg) / I_peak_chg * 100
    
    assert abs(tau - 100e-6) < 1e-12
    assert abs(t50 - 69.3147e-6) < 1e-8
    assert abs(tr - 219.722e-6) < 1e-7
    assert abs(fc - 1591.55) < 0.5
    assert abs(I_peak_chg - 250e-6) < 1e-9
    assert abs(Vc_5tau - 4.9663) < 1e-3
    assert abs(I_peak_dis - (-248.316e-6)) < 1e-7
    assert abs(diff_percent - 0.6738) < 1e-3
    
    # Ex0.3 Cross-check
    cross_check = tr * fc
    assert abs(cross_check - 0.34969) < 1e-4
    
    # Ex0.4 Slope
    # Slope = ln(2) * C in s / Ohm
    slope_s_per_ohm = math.log(2) * C
    slope_us_per_kohm = slope_s_per_ohm * 1e6 * 1e3 # (s/Ohm) * (1e6 us/s) * (1e3 Ohm/kOhm) -> us/kOhm
    assert abs(slope_us_per_kohm - 3.4657) < 1e-3, f"Slope mismatch: {slope_us_per_kohm}"
    
    print("  [PASS] In-lab Ex0.1 - Ex0.4 values verified!")

def test_ex05_mosfet():
    print("Testing Ex0.5 MOSFET square law...")
    Kp_n = 120e-6
    Vtn = 0.70
    W = 1.2e-6
    L = 0.6e-6
    Vgs = 5.0
    Vds = 5.0
    
    Id_sat = 0.5 * Kp_n * (W / L) * (Vgs - Vtn)**2
    assert abs(Id_sat - 2.2188e-3) < 1e-5, f"Id_sat mismatch: {Id_sat}"
    print("  [PASS] Ex0.5 square law verified (Id_sat = 2.219 mA)!")

if __name__ == "__main__":
    print("=== RUNNING FULL LAB 0 VERIFICATION ===")
    test_example_3_7()
    test_pre_lab()
    test_in_lab_rc()
    test_ex05_mosfet()
    print("=== ALL VERIFICATION TESTS PASSED SUCCESSFULLY! ===")
