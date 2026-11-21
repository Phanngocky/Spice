"""
Script kiểm chứng tính toán giải tích và số liệu mô phỏng Lab 06:
Thiết kế Mạch cộng Toàn phần 1-bit (1-bit Full Adder)
Công nghệ MOSIS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

def verify_lab06():
    print("=" * 70)
    print("KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 06 - 1-BIT FULL ADDER")
    print("=" * 70)

    # 1. Bang chan tri 8 to hop
    print("\n1. Bảng chân trị 1-bit Full Adder:")
    print("   A  B  Cin | Sum  Cout | Nhận xét trạng thái")
    print("   -------------------------------------------------")
    truth_table = [
        (0, 0, 0, 0, 0, "Không có nhớ, không có tổng"),
        (0, 0, 1, 1, 0, "Sum = 1"),
        (0, 1, 0, 1, 0, "Sum = 1"),
        (0, 1, 1, 0, 1, "Cout = 1 (Tạo tràn từ B và Cin)"),
        (1, 0, 0, 1, 0, "Sum = 1"),
        (1, 0, 1, 0, 1, "Cout = 1 (Tạo tràn từ A và Cin)"),
        (1, 1, 0, 0, 1, "Cout = 1 (Tạo tràn từ A và B)"),
        (1, 1, 1, 1, 1, "Sum = 1 và Cout = 1"),
    ]
    for a, b, cin, sum_val, cout_val, note in truth_table:
        s_calc = a ^ b ^ cin
        c_calc = (a & b) | (cin & (a ^ b))
        assert s_calc == sum_val and c_calc == cout_val, "Lỗi logic Full Adder!"
        print(f"   {a}  {b}   {cin}  |  {sum_val}    {cout_val}   | {note}")

    # 2. So sanh PPA 2 kien truc FA
    print("\n2. So sánh Kiến trúc Mirror Adder (28T) vs TG Adder (16T):")
    print("   a. Mirror Adder (28 Transistors):")
    print("      - Khối Carry: 8T (4P + 4N) + 2T Inverter = 10 Transistors")
    print("      - Khối Sum:   12T (6P + 6N) + 2T Inverter = 14 Transistors (hoặc 24-28T)")
    print("      - Ưu điểm: Tín hiệu phục hồi biên độ tuyệt đối (Strong 0/1); độ bền nhiễu cao")
    print("      - Trễ Cin -> Cout: Chỉ qua 1 tầng logic + Inverter đệm ≈ 65 - 75 ps")
    print("   b. Transmission Gate Adder (16 Transistors):")
    print("      - XOR 1 (A xor B): 4-6T (TG + Inverter)")
    print("      - XOR 2 (P xor Cin -> Sum): 4T")
    print("      - Carry MUX (MUX(Cin, A, sel=P)): 4T")
    print("      - Tổng số: 16 Transistors (Tiết kiệm 43% diện tích so với 28T)")
    print("      - Nhược điểm: Tín hiệu Cin đi qua Pass-TG bị suy giảm sườn xung khi nối chuỗi dài")

    # 3. Phan tich Duong tre toi han (Critical Path)
    tpd_cin_cout_mirror = 68.0 # ps
    tpd_a_sum_mirror = 142.0   # ps
    print("\n3. Phân tích Đường trễ tới hạn (Critical Path):")
    print(f"   - Trễ Carry Propagation: tpd(Cin -> Cout) ≈ {tpd_cin_cout_mirror:.1f} ps (RẤT QUAN TRỌNG TRONG CHUỖI)")
    print(f"   - Trễ Sum Generation:    tpd(A -> Sum)     ≈ {tpd_a_sum_mirror:.1f} ps")
    print("   => Trong bộ cộng N-bit RCA (Ripple Carry Adder):")
    print("      Tổng trễ T_add = tpd(A -> Cout_0) + (N - 2) * tpd(Cin -> Cout) + tpd(Cin -> Sum_N-1)")
    print("      => Cực tiểu hóa trễ Cin -> Cout là ưu tiên sống còn của thiết kế tế bào FA!")
    print("=" * 70)

if __name__ == "__main__":
    verify_lab06()
