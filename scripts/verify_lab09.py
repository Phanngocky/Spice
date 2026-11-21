"""
Script kiểm chứng tính toán giải tích và số liệu mô phỏng Lab 09:
Thiết kế Đường dữ liệu Khối cộng nhanh 4-bit (4-bit Carry Lookahead Adder - CLA)
Công nghệ MOSIS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

def cla_4bit_compute(a_bits, b_bits, c0):
    """Tính toán logic giải tích của 4-bit CLA"""
    g = [a_bits[i] & b_bits[i] for i in range(4)]
    p = [a_bits[i] ^ b_bits[i] for i in range(4)]

    c = [0] * 5
    c[0] = c0
    c[1] = g[0] | (p[0] & c[0])
    c[2] = g[1] | (p[1] & g[0]) | (p[1] & p[0] & c[0])
    c[3] = g[2] | (p[2] & g[1]) | (p[2] & p[1] & g[0]) | (p[2] & p[1] & p[0] & c[0])
    c[4] = g[3] | (p[3] & g[2]) | (p[3] & p[2] & g[1]) | (p[3] & p[2] & p[1] & g[0]) | (p[3] & p[2] & p[1] & p[0] & c[0])

    s = [p[i] ^ c[i] for i in range(4)]

    sum_val = s[0] + (s[1] << 1) + (s[2] << 2) + (s[3] << 3)
    cout = c[4]
    return sum_val, cout, c, p, g

def verify_lab09():
    print("=" * 75)
    print("KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 09 - 4-BIT CARRY LOOKAHEAD ADDER (CLA)")
    print("=" * 75)

    # 1. Kiem chung cac to hop so hoc mau
    test_cases = [
        (0, 0, 0, "Cộng 0 + 0 + 0"),
        (5, 3, 0, "Cộng thông thường: 5 + 3 = 8 (Không tràn)"),
        (9, 6, 0, "Cộng cận tràn: 9 + 6 = 15"),
        (12, 7, 0, "Cộng có tràn số nhớ: 12 + 7 = 19 (16 + 3)"),
        (15, 0, 1, "Đường lan truyền xấu nhất (Worst-Case Carry Propagate)"),
        (15, 15, 1, "Cộng cực đại mọi bit = 1: 15 + 15 + 1 = 31 (16 + 15)"),
        (10, 5, 1, "Cộng có số nhớ ngõ vào: 10 + 5 + 1 = 16 (Tràn C4)"),
    ]

    print("\n1. Kiểm chứng Bảng chân trị và Phương trình Logic CLA 4-bit:")
    print("   A (hex/dec)   B (hex/dec)   Cin | Sum (dec)   Cout | Trạng thái kiểm chứng")
    print("   -------------------------------------------------------------------------")

    for a, b, cin, desc in test_cases:
        a_bits = [(a >> i) & 1 for i in range(4)]
        b_bits = [(b >> i) & 1 for i in range(4)]
        sum_val, cout, c_list, p_list, g_list = cla_4bit_compute(a_bits, b_bits, cin)

        expected_total = a + b + cin
        expected_sum = expected_total & 0x0F
        expected_cout = (expected_total >> 4) & 1

        assert sum_val == expected_sum and cout == expected_cout, f"Lỗi tính toán CLA tại {a} + {b} + {cin}!"
        print(f"   A={a:2d} (0b{a:04b}) B={b:2d} (0b{b:04b})  {cin}  | Sum={sum_val:2d} (0b{sum_val:04b})  {cout}  | PASS - {desc}")

    # 2. Phan tich Duong tre toi han (Critical Path Analysis): RCA vs CLA
    print("\n2. Phân tích So sánh Thời gian trễ: 4-bit CLA vs 4-bit RCA:")
    # Thong so tre tu mo phong SPICE MOSIS C5N
    t_pg = 65.0      # ps (Trễ tạo cờ Pi, Gi từ ngõ vào)
    t_clg_c4 = 110.0 # ps (Trễ tạo số nhớ C4 qua khối CLG)
    t_xor_sum = 65.0 # ps (Trễ cổng XOR tạo Sum từ Pi và Ci)

    t_carry_rca_step = 70.0 # ps (Trễ lan truyền 1 tầng Carry của Mirror Adder)
    t_rca_c4 = 72.0 + 3 * t_carry_rca_step # ps (Trễ Carry 4 tầng RCA)
    t_rca_sum3 = 355.0 # ps (Tổng trễ tới Sum bit cuối của RCA)

    t_cla_c4 = t_pg + t_clg_c4 # ps (Trễ Cout của CLA)
    t_cla_sum3 = t_pg + 100.0 + t_xor_sum # ps (Trễ Sum bit 3 của CLA)

    speedup_c4 = t_rca_c4 / t_cla_c4
    speedup_sum = t_rca_sum3 / t_cla_sum3

    print(f"   - Trễ lan truyền số nhớ tràn (Carry Out C4):")
    print(f"     + 4-bit RCA (Ripple Carry, 4 tầng nối tiếp):  t_carry = {t_rca_c4:.1f} ps")
    print(f"     + 4-bit CLA (Carry Lookahead, song song):    t_carry = {t_cla_c4:.1f} ps")
    print(f"     => Tốc độ tạo số nhớ CLA nhanh hơn RCA:      {speedup_c4:.2f}x (Tăng 61%!)")
    print(f"   - Trễ đường tới hạn dài nhất (A/B -> Sum[3]):")
    print(f"     + 4-bit RCA: t_max = {t_rca_sum3:.1f} ps")
    print(f"     + 4-bit CLA: t_max = {t_cla_sum3:.1f} ps")
    print(f"     => Tốc độ tổng thể CLA nhanh hơn RCA:        {speedup_sum:.2f}x (Nhanh hơn 54%!)")

    # 3. So sanh Dien tich va So luong Transistor (Hardware Complexity)
    trans_pg = 4 * 12 # 4 x (AND2 6T + XOR2 6T) = 48T
    trans_clg = 8 + 12 + 18 + 24 # C1(8T) + C2(12T) + C3(18T) + C4(24T) = 62T
    trans_sum = 4 * 6 # 4 x XOR2 = 24T
    trans_cla_total = trans_pg + trans_clg + trans_sum # 134T

    trans_rca_total = 4 * 28 # 4 x Mirror Adder 28T = 112T
    area_overhead = ((trans_cla_total - trans_rca_total) / trans_rca_total) * 100.0

    print("\n3. So sánh Độ phức tạp Phần cứng (Transistor Count & Silicon Area):")
    print(f"   - 4-bit RCA (4 tế bào Mirror Adder 28T):  {trans_rca_total} Transistors")
    print(f"   - 4-bit CLA (4 PG + 1 CLG + 4 Sum XOR):   {trans_cla_total} Transistors")
    print(f"     + Khối PG Generator:  {trans_pg} Transistors (35.8%)")
    print(f"     + Khối CLG Generator: {trans_clg} Transistors (46.3%)")
    print(f"     + Khối Sum Unit:      {trans_sum} Transistors (17.9%)")
    print(f"   => Đánh đổi phần cứng: Tăng {area_overhead:.1f}% diện tích để đổi lấy tốc độ nhanh hơn gần 2 lần!")
    print("=" * 75)

if __name__ == "__main__":
    verify_lab09()
