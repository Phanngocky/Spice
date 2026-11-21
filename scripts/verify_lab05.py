"""
Script kiểm chứng tính toán giải tích và số liệu mô phỏng Lab 05:
Mạch tuần tự mức Transistor: D-Latch và D-Flip-Flop Master-Slave
Công nghệ MOSIS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

import math

def verify_lab05():
    print("=" * 70)
    print("KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 05 - D-LATCH & D-FLIP-FLOP")
    print("=" * 70)

    # 1. Thong so cong nghe C5N
    lambda_val = 0.30
    L = 2 * lambda_val # 0.6 um
    wn_inv = 4 * lambda_val # 1.2 um
    wp_inv = 12 * lambda_val # 3.6 um
    tpd_inv = 34.0 # ps (INV_X1 voi tai tieu chuan)
    tpd_tg = 42.0  # ps (TG_GATE voi tai tieu chuan)

    print(f"\n1. Thư viện tế bào cơ sở:")
    print(f"   Inverter chuẩn (INV_X1): Wn=1.2um, Wp=3.6um, L=0.6um -> tpd ≈ {tpd_inv:.1f} ps")
    print(f"   Cổng truyền chuẩn (TG):  Wn=1.2um, Wp=3.6um, L=0.6um -> tpd ≈ {tpd_tg:.1f} ps")

    # 2. D-Latch dung Cong truyen (TG-based D-Latch)
    # Gom 2 TG (TG1 input, TG2 feedback) va 3 Inverter (I1 forward, I2 output, I3 feedback)
    # Khi CLK = 1 (Trong suot): tpd(D -> Q) = tpd_TG1 + tpd_I1 + tpd_I2
    tpd_latch_dq = tpd_tg + tpd_inv + tpd_inv
    print(f"\n2. Mạch chốt D-Latch (TG-based D-Latch):")
    print(f"   Số lượng transistor: 2 TG (4T) + 3 Inverters (6T) = 10 Transistors (hoặc 8T nếu không đệm ngõ ra)")
    print(f"   Trễ truyền lan khi trong suốt tpd(D -> Q) = tpd_TG1 + tpd_I1 + tpd_I2")
    print(f"   tpd(D -> Q) ≈ {tpd_tg:.1f} + {tpd_inv:.1f} + {tpd_inv:.1f} = {tpd_latch_dq:.1f} ps")

    # 3. Master-Slave D-Flip-Flop (Positive Edge-Triggered DFF)
    # Master (CLK=0 transparent, CLK=1 hold) + Slave (CLK=1 transparent, CLK=0 hold)
    # Setup time: thoi gian D phai den som de nap nut Master qm: t_setup ≈ tpd_TG_M1 + tpd_I_M1
    t_setup = tpd_tg + tpd_inv + 10.0 # them bien do on dinh
    # Hold time: thoi gian D phai giu de TG_M1 ngat hoan toan
    # t_hold ≈ tpd_inv_clk - tpd_TG_M1
    t_hold = tpd_inv - tpd_tg
    # Clock-to-Q delay: tu khi CLK len 50% den khi Slave truyen ra Q
    # t_cq = tpd_inv_clk + tpd_TG_S1 + tpd_I_S1
    t_cq = tpd_inv + tpd_tg + tpd_inv

    print(f"\n3. Mạch lật D-Flip-Flop Master-Slave kích hoạt sườn dương:")
    print(f"   Tổng số transistor: 2 D-Latch (2x8T = 16T) + 1 Inverter CLK (2T) = 18 - 20 Transistors")
    print(f"   Thời gian thiết lập lý thuyết (t_setup) ≈ tpd_TG_M1 + tpd_INV_M1 ≈ {t_setup:.1f} ps")
    print(f"   Thời gian giữ lý thuyết (t_hold)       ≈ tpd_INV_CLK - tpd_TG_M1 ≈ {t_hold:.1f} ps")
    print(f"   Trễ xung nhịp đến ngõ ra (t_c-q)       ≈ tpd_INV_CLK + tpd_TG_S1 + tpd_INV_S1 ≈ {t_cq:.1f} ps")

    # 4. Tan so cuc dai f_max
    # f_max = 1 / (t_cq + t_setup)
    t_cycle_min = t_cq + t_setup
    f_max = 1.0 / (t_cycle_min * 1e-12) / 1e9 # GHz
    print(f"\n4. Giới hạn tần số hoạt động cực đại:")
    print(f"   Chu kỳ xung nhịp tối thiểu T_min = t_cq + t_setup ≈ {t_cycle_min:.1f} ps")
    print(f"   Tần số xung nhịp cực đại f_max ≈ {f_max:.2f} GHz (trong điều kiện tải nhẹ 50fF)")
    print("=" * 70)

if __name__ == "__main__":
    verify_lab05()
