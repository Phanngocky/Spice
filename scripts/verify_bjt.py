"""
KIEM CHUNG GIAI TICH: KHAO SAT DAC TUYEN VAO VA RA BJT 2N3904
Hoc phan: Thuc hanh Thiet ke VLSI (5505382) - DH Su pham Ky thuat Da Nang
Tac gia: Phan Ngoc Ky (2026)
"""

import numpy as np

def verify_bjt_characteristics():
    print("=" * 75)
    print("KIỂM CHỨNG GIẢI TÍCH: KHẢO SÁT ĐẶC TUYẾN VÀO - RA BJT NPN (2N3904)")
    print("=" * 75)

    # 1. Thông số mô hình 2N3904 chuẩn SPICE
    Is = 1.0e-14     # Dòng bão hòa ngược (A)
    Bf = 160.0       # Hệ số khuếch đại dòng cực phát chung beta
    VA = 74.0        # Điện áp Early (V)
    Vt = 0.02585     # Thế nhiệt ở 300K (25.85 mV)

    print("\n1. THÔNG SỐ MÔ HÌNH BJT 2N3904:")
    print(f"   - Is (Dòng bão hòa ngược) = {Is:.1e} A")
    print(f"   - Bf (Hệ số khuếch đại beta) = {Bf:.1f}")
    print(f"   - VA (Điện áp Early)       = {VA:.1f} V")
    print(f"   - Vt (Thế nhiệt ở 300K)   = {Vt*1e3:.2f} mV")

    # 2. Đặc tuyến ngõ vào: Ib theo Vbe (cố định Vce = 5.0V)
    print("\n2. KHẢO SÁT ĐẶC TUYẾN NGÕ VÀO Ib(Vbe):")
    print("   Công thức Ebers-Moll: Ib = (Is / beta) * [exp(Vbe / Vt) - 1]")
    vbe_test = [0.40, 0.50, 0.60, 0.65, 0.68, 0.70, 0.72]
    for v in vbe_test:
        ib_val = (Is / Bf) * (np.exp(v / Vt) - 1)
        print(f"   * Vbe = {v:.2f} V -> Ib = {ib_val*1e6:10.4f} uA")

    # Tính ngưỡng mở Vbe tại Ib = 10 uA và 20 uA
    vbe_10u = Vt * np.log((10e-6 * Bf / Is) + 1)
    vbe_20u = Vt * np.log((20e-6 * Bf / Is) + 1)
    print(f"   => Điện áp ngưỡng mở tại Ib = 10 uA: Vbe = {vbe_10u:.4f} V (≈ 0.675 V)")
    print(f"   => Điện áp ngưỡng mở tại Ib = 20 uA: Vbe = {vbe_20u:.4f} V (≈ 0.693 V)")

    # 3. Khảo sát Họ đặc tuyến ngõ ra: Ic(Vce, Ib)
    print("\n3. KHẢO SÁT HỌ ĐẶC TUYẾN NGÕ RA Ic(Vce, Ib):")
    print("   Công thức vùng tích cực: Ic = beta * Ib * (1 + Vce / VA)")
    ib_list = [10e-6, 20e-6, 30e-6, 40e-6, 50e-6]
    vce_points = [1.0, 5.0, 10.0]

    for ib in ib_list:
        print(f"\n   --- Mức dòng Base Ib = {ib*1e6:.0f} uA (Ic lý tưởng chưa tính Early = {Bf*ib*1e3:.2f} mA) ---")
        for vce in vce_points:
            ic_val = Bf * ib * (1.0 + vce / VA) * 1e3
            beta_eff = (ic_val * 1e-3) / ib
            print(f"       Vce = {vce:4.1f} V -> Ic = {ic_val:.4f} mA (beta hiệu dụng = {beta_eff:.1f})")

    # 4. Trích xuất hệ số khuếch đại dòng beta và điện trở ngõ ra ro tại Vce = 5V
    ic_10u_5v = Bf * 10e-6 * (1.0 + 5.0 / VA) * 1e3
    ic_20u_5v = Bf * 20e-6 * (1.0 + 5.0 / VA) * 1e3
    beta_extracted = ((ic_20u_5v - ic_10u_5v) * 1e-3) / (10e-6)
    ro_10u = VA / (Bf * 10e-6)
    ro_20u = VA / (Bf * 20e-6)

    print("\n4. THÔNG SỐ ĐẶC TRƯNG TRÍCH XUẤT:")
    print(f"   - Hệ số khuếch đại dòng vi sai beta tại Vce = 5V: {beta_extracted:.2f}")
    print(f"   - Điện trở ngõ ra ro tại Ib = 10 uA: {ro_10u*1e-3:.2f} kOhm (Độ dốc: {1/ro_10u*1e6:.2f} uS)")
    print(f"   - Điện trở ngõ ra ro tại Ib = 20 uA: {ro_20u*1e-3:.2f} kOhm (Độ dốc: {1/ro_20u*1e6:.2f} uS)")
    print(f"   - Vùng bão hòa (Saturation): Vce < 0.20 - 0.25 V")
    print("=" * 75)

if __name__ == "__main__":
    verify_bjt_characteristics()
