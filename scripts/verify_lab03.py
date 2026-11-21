"""
Script kiểm chứng tính toán giải tích và số liệu mô phỏng Lab 03:
Cổng phức hợp AOI21 và Phương pháp Logical Effort tối ưu chuỗi đệm Inverter
Công nghệ MOSIS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

import math

def verify_lab03():
    print("=" * 70)
    print("KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 03 - AOI21 & LOGICAL EFFORT")
    print("=" * 70)

    # 1. Kích thước và Ron tương đương
    lambda_val = 0.30  # um
    wn_inv = 4 * lambda_val  # 1.2 um
    wp_inv = 12 * lambda_val # 3.6 um
    L = 2 * lambda_val       # 0.6 um

    print(f"\n1. Inverter tham chiếu (INV_X1):")
    print(f"   Wn = {wn_inv:.2f} um (4 lambda), Wp = {wp_inv:.2f} um (12 lambda), L = {L:.2f} um")
    Cin_inv = 4 + 12 # 16 lambda

    # AOI21: Y = !((A*B) + C)
    # PDN: MN_A & MN_B series (2 NMOS) -> Wn = 2 * 4 = 8 lambda = 2.4 um
    #      MN_C single (1 NMOS) -> Wn = 4 lambda = 1.2 um
    # PUN: (MP_A // MP_B) in series with MP_C
    #      Worst case: 2 PMOS series -> Wp = 2 * 12 = 24 lambda = 7.2 um for all
    wn_A = 8 * lambda_val
    wn_B = 8 * lambda_val
    wn_C = 4 * lambda_val
    wp_A = 24 * lambda_val
    wp_B = 24 * lambda_val
    wp_C = 24 * lambda_val

    print(f"\n2. Kích thước tế bào AOI21_X1:")
    print(f"   MN_A, MN_B (PDN nối tiếp): Wn = {wn_A:.2f} um (8 lambda)")
    print(f"   MN_C       (PDN nhánh đơn): Wn = {wn_C:.2f} um (4 lambda)")
    print(f"   MP_A, MP_B, MP_C (PUN):    Wp = {wp_A:.2f} um (24 lambda)")

    # Logical Effort
    Cin_A = 8 + 24 # 32 lambda
    Cin_B = 8 + 24 # 32 lambda
    Cin_C = 4 + 24 # 28 lambda

    g_A = Cin_A / Cin_inv
    g_B = Cin_B / Cin_inv
    g_C = Cin_C / Cin_inv

    print(f"\n3. Logical Effort (g):")
    print(f"   g_A = Cin_A / Cin_inv = {Cin_A} / {Cin_inv} = {g_A:.3f} (= 6/3 = 2.000)")
    print(f"   g_B = Cin_B / Cin_inv = {Cin_B} / {Cin_inv} = {g_B:.3f} (= 6/3 = 2.000)")
    print(f"   g_C = Cin_C / Cin_inv = {Cin_C} / {Cin_inv} = {g_C:.3f} (= 7/4 = 1.750)")

    # Parasitic delay (p)
    # Drain out: MP_C (24) + MN_A (8) + MN_C (4) = 36 lambda
    # Inverter drain: 12 + 4 = 16 lambda
    p_aoi21 = 36 / 16
    print(f"\n4. Parasitic Delay (p):")
    print(f"   Cout_aoi = 24 + 8 + 4 = 36 lambda")
    print(f"   Cout_inv = 12 + 4 = 16 lambda")
    print(f"   p_aoi21 = 36 / 16 = {p_aoi21:.3f} (= 2.25 tau)")

    # Buffer chain optimization
    print(f"\n5. Tối ưu hóa chuỗi đệm Inverter (Inverter Buffer Chain):")
    Cin = 20e-15 # 20 fF
    CL = 1e-12   # 1 pF
    H = CL / Cin # 50
    print(f"   Cin = {Cin*1e15:.1f} fF, CL = {CL*1e12:.1f} pF -> H = CL/Cin = {H:.1f}")

    delays = {}
    for N in range(1, 6):
        f_hat = H ** (1.0 / N)
        D = N * (f_hat + 1.0)
        delays[N] = (f_hat, D)
        print(f"   N = {N} tầng: f_hat = {f_hat:.3f}, Trễ D = {D:.2f} tau")

    opt_N = min(delays, key=lambda k: delays[k][1])
    opt_f, opt_D = delays[opt_N]
    print(f"   => Số tầng tối ưu: N = {opt_N} (Trễ cực tiểu D = {opt_D:.2f} tau)")
    print(f"   => Cải thiện tốc độ so với N=1 (lái trực tiếp): {delays[1][1] / opt_D:.2f} lần ({delays[1][1] / opt_D * 100:.1f}%)")

    # Sizing for N = 3
    s1 = 1.0
    s2 = opt_f
    s3 = opt_f ** 2
    print(f"\n6. Định kích thước các tầng chuỗi đệm (N = 3, f_hat = {opt_f:.3f}):")
    print(f"   Tầng 1 (1.0X):  Wn = {wn_inv:.2f} um, Wp = {wp_inv:.2f} um")
    print(f"   Tầng 2 ({s2:.2f}X): Wn = {wn_inv * s2:.2f} um, Wp = {wp_inv * s2:.2f} um")
    print(f"   Tầng 3 ({s3:.2f}X): Wn = {wn_inv * s3:.2f} um, Wp = {wp_inv * s3:.2f} um")
    print("=" * 70)

if __name__ == "__main__":
    verify_lab03()
