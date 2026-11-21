"""
KIEM CHUNG GIAI TICH: KHAO SAT NAP VA XA TU DIEN (RC CHARGE & DISCHARGE)
Hoc phan: Thuc hanh Thiet ke VLSI (5505382) - DH Su pham Ky thuat Da Nang
Tac gia: Phan Ngoc Ky (2026)
"""

import numpy as np

def verify_rc_charge_discharge():
    print("=" * 75)
    print("KIỂM CHỨNG GIẢI TÍCH: MẠCH NẠP VÀ XẢ TỤ ĐIỆN RC CƠ BẢN")
    print("=" * 75)

    R = 10.0e3   # 10 kOhm
    C = 10.0e-9  # 10 nF
    V0 = 5.0     # 5.0 V
    tau = R * C  # 100 us

    print("\n1. THÔNG SỐ LINH KIỆN:")
    print(f"   - Điện trở R  = {R*1e-3:.1f} kOhm")
    print(f"   - Tụ điện C   = {C*1e9:.1f} nF")
    print(f"   - Điện áp V0  = {V0:.1f} V")
    print(f"   - Hằng số thời gian tau = R * C = {tau*1e6:.2f} us ({tau*1e3:.4f} ms)")

    print("\n2. GIAI ĐOẠN NẠP ĐIỆN TÍCH (0 <= t < Ton):")
    print("   Công thức: Vc(t) = V0 * [1 - exp(-t/tau)], i(t) = (V0/R) * exp(-t/tau)")
    print(f"   - Dòng nạp đỉnh ban đầu tại t = 0: I_peak = +V0/R = {V0/R*1e3:+.3f} mA (+{V0/R*1e6:.1f} uA)")
    
    t_charge_points = [0.5*tau, 1.0*tau, 2.2*tau, 3.0*tau, 5.0*tau]
    for t_val in t_charge_points:
        vc_val = V0 * (1.0 - np.exp(-t_val / tau))
        i_val = (V0 / R) * np.exp(-t_val / tau)
        pct = (vc_val / V0) * 100
        print(f"   * t = {t_val/tau:3.1f} tau ({t_val*1e6:5.1f} us) -> Vc = {vc_val:.4f} V ({pct:5.1f}%), i = {i_val*1e3:.4f} mA")

    print("\n3. GIAI ĐOẠN XẢ ĐIỆN TÍCH (Ton <= t < T, dat t' = t - Ton):")
    print("   Công thức: Vc(t') = V0 * exp(-t'/tau), i(t') = -(V0/R) * exp(-t'/tau)")
    print(f"   - Dòng xả đỉnh ban đầu tại t' = 0: I_peak = -V0/R = {-V0/R*1e3:+.3f} mA ({-V0/R*1e6:.1f} uA)")

    t_discharge_points = [0.5*tau, 1.0*tau, 2.2*tau, 3.0*tau, 5.0*tau]
    for t_val in t_discharge_points:
        vc_val = V0 * np.exp(-t_val / tau)
        i_val = -(V0 / R) * np.exp(-t_val / tau)
        pct = (vc_val / V0) * 100
        print(f"   * t' = {t_val/tau:3.1f} tau ({t_val*1e6:5.1f} us) -> Vc = {vc_val:.4f} V ({pct:5.1f}%), i = {i_val*1e3:.4f} mA")

    print("\n4. CÁC THÔNG SỐ ĐẶC TRƯNG:")
    t_rise = 2.2 * tau
    t_fall = 2.2 * tau
    Q_max = C * V0
    W_max = 0.5 * C * (V0**2)
    print(f"   - Thời gian tăng t_rise (10% -> 90%): 2.2 * tau = {t_rise*1e6:.2f} us")
    print(f"   - Thời gian giảm t_fall (90% -> 10%): 2.2 * tau = {t_fall*1e6:.2f} us")
    print(f"   - Điện tích nạp cực đại Q_max = C * V0 = {Q_max*1e9:.2f} nC")
    print(f"   - Năng lượng tích trữ W_max = 0.5 * C * V0^2 = {W_max*1e6:.4f} uJ ({W_max*1e9:.1f} nJ)")
    print("=" * 75)

if __name__ == "__main__":
    verify_rc_charge_discharge()
