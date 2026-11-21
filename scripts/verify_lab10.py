"""
Script kiểm chứng tính toán giải tích và số liệu mô phỏng Lab 10:
Capstone Project - Tích hợp Vi mạch 4-bit Registered ALU & Xác thực Vật lý Toàn diện
Công nghệ MOSIS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

def alu_4bit_execute(op, a, b, cin=0):
    """Mô phỏng chức năng của Registered ALU 4-bit"""
    if op == 0:   # ADD
        res_full = a + b + cin
        y = res_full & 0x0F
        cout = 1 if res_full >= 16 else 0
    elif op == 1: # AND
        y = (a & b) & 0x0F
        cout = 0
    elif op == 2: # OR
        y = (a | b) & 0x0F
        cout = 0
    elif op == 3: # XOR
        y = (a ^ b) & 0x0F
        cout = 0
    else:
        raise ValueError("Invalid OP code")

    z_flag = 1 if y == 0 else 0
    return y, cout, z_flag

def verify_lab10():
    print("=" * 75)
    print("KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 10 - CAPSTONE 4-BIT REGISTERED ALU")
    print("=" * 75)

    # 1. Kiem chung chuoi chi thi da chu ky (Multi-cycle Instruction Test Program)
    program = [
        ("Chu kỳ 1: ADD thường",      0, 5, 3, 0, 8, 0, 0),
        ("Chu kỳ 2: ADD tràn (Cout=1, Z=1)", 0, 12, 4, 0, 0, 1, 1),
        ("Chu kỳ 3: AND thông thường", 1, 10, 12, 0, 8, 0, 0),
        ("Chu kỳ 4: OR thông thường",  2, 10, 5, 0, 15, 0, 0),
        ("Chu kỳ 5: XOR bằng nhau (Z=1)", 3, 9, 9, 0, 0, 0, 1),
        ("Chu kỳ 6: ADD có Cin=1",    0, 7, 8, 1, 0, 1, 1),
        ("Chu kỳ 7: XOR khác biệt",   3, 15, 0, 0, 15, 0, 0),
    ]

    print("\n1. Kiểm chứng Tập lệnh ALU 4-bit & Cờ Trạng thái (Z, Cout):")
    print("   Lệnh (OP)      A      B   Cin |  OUT[3:0]   Cout   Z  | Kết quả kiểm chứng")
    print("   -------------------------------------------------------------------------")

    op_names = ["ADD", "AND", "OR ", "XOR"]
    for desc, op, a, b, cin, exp_y, exp_cout, exp_z in program:
        y, cout, z = alu_4bit_execute(op, a, b, cin)
        assert y == exp_y and cout == exp_cout and z == exp_z, f"Lỗi thực thi ALU tại {desc}!"
        print(f"   {op_names[op]} (0b{op:02b})   {a:2d} ({a:04b}) {b:2d} ({b:04b})  {cin}  |   {y:2d} ({y:04b})    {cout}    {z}  | PASS - {desc}")

    # 2. Phan tich Duong tre toi han & Ngan sach Thoi gian (Timing Closure & f_max)
    print("\n2. Phân tích Ngân sách Thời gian (Timing Budget) & Tần số Tối đa f_max:")
    t_cq_dff = 110.0   # ps (Trễ Clock-to-Q của D-FF Master-Slave)
    t_cla4_max = 230.0 # ps (Trễ đường tới hạn khối số học CLA4)
    t_mux4 = 65.0      # ps (Trễ khối dồn kênh TG MUX4:1)
    t_setup_dff = 75.0 # ps (Thời gian thiết lập của D-FF)
    t_skew = 40.0      # ps (Biên độ dự phòng lệch pha xung nhịp Clock Skew)

    t_comb_max = t_cla4_max + t_mux4 # 295 ps
    t_clk_min_pre = t_cq_dff + t_comb_max + t_setup_dff + t_skew # ps
    f_max_pre = (1.0 / (t_clk_min_pre * 1e-12)) / 1e9 # GHz

    # Post-layout PEX trễ tăng xấp xỉ 35% do điện trở và điện dung ký sinh dây dẫn
    t_clk_min_pex = t_clk_min_pre * 1.35
    f_max_pex = (1.0 / (t_clk_min_pex * 1e-12)) / 1e9

    print(f"   - Trễ Clock-to-Q thanh ghi nguồn (t_c-q):    {t_cq_dff:.1f} ps")
    print(f"   - Trễ mạch tổ hợp tới hạn (t_comb = CLA4 + MUX4): {t_comb_max:.1f} ps ({t_cla4_max:.1f} ps + {t_mux4:.1f} ps)")
    print(f"   - Thời gian thiết lập thanh ghi đích (t_setup): {t_setup_dff:.1f} ps")
    print(f"   - Dung sai lệch pha xung nhịp (t_skew):      {t_skew:.1f} ps")
    print(f"   => Chu kỳ xung nhịp tối thiểu (Pre-layout):   T_clk_min = {t_clk_min_pre:.1f} ps")
    print(f"   => Tần số xung nhịp tối đa lý thuyết:        f_max = {f_max_pre:.2f} GHz (Vượt mốc 1.0 GHz)")
    print(f"   => Chu kỳ xung nhịp tối thiểu sau PEX:       T_clk_pex ≈ {t_clk_min_pex:.1f} ps")
    print(f"   => Tần số xung nhịp tối đa thực tế sau PEX:  f_max_pex ≈ {f_max_pex:.2f} GHz (An toàn ở 1.0 GHz!)")

    # 3. Thong ke Phan ra Phan cung Chip (Transistor Count Breakdown)
    t_cla = 134
    t_and = 4 * 6  # 24T
    t_or  = 4 * 6  # 24T
    t_xor = 4 * 6  # 24T
    t_log_total = t_and + t_or + t_xor # 72T
    t_mux = 4 * 16 # 64T
    t_dff = 4 * 18 # 72T
    t_flags = 8 + 8 # 16T (NOR4 cho Zero + Cout buffer/latch)
    t_chip_total = t_cla + t_log_total + t_mux + t_dff + t_flags

    print("\n3. Thống kê Phân bổ Phần cứng Vi mạch (Transistor Count Breakdown):")
    print(f"   - Khối Số học CLA 4-bit:     {t_cla:3d} Transistors ({t_cla/t_chip_total*100:.1f}%)")
    print(f"   - Khối Logic 4-bit (AND,OR,XOR): {t_log_total:3d} Transistors ({t_log_total/t_chip_total*100:.1f}%)")
    print(f"   - Khối Bộ chọn MUX 4:1 4-bit:   {t_mux:3d} Transistors ({t_mux/t_chip_total*100:.1f}%)")
    print(f"   - Khối Thanh ghi ngõ ra DFF:     {t_dff:3d} Transistors ({t_dff/t_chip_total*100:.1f}%)")
    print(f"   - Khối Cờ trạng thái (Z, Cout):  {t_flags:3d} Transistors ({t_flags/t_chip_total*100:.1f}%)")
    print(f"   => TỔNG SỐ TRANSISTOR TOÀN VI MẠCH: {t_chip_total} Transistors (Quy mô chuẩn cho Capstone)")
    print("=" * 75)

if __name__ == "__main__":
    verify_lab10()
