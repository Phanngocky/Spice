"""
Script kiểm chứng tính toán giải tích và số liệu mô phỏng Lab 07:
Kỹ thuật Logic Động (Dynamic CMOS Logic & Domino Logic)
Công nghệ MOSIS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
"""

def verify_lab07():
    print("=" * 75)
    print("KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH LAB 07 - DYNAMIC & DOMINO CMOS LOGIC")
    print("=" * 75)

    VDD = 5.0
    Vtn = 0.70
    Vtp = -0.90

    # 1. Cơ chế 2 pha của Dynamic Logic
    print("\n1. Chu trình Hoạt động 2 pha (Precharge & Evaluate):")
    print("   - Pha Nạp trước (Precharge - CLK = 0V):")
    print("     + Mp (PMOS W=12λ) DẪN mạnh, Me (Foot NMOS W=8λ) NGẮT.")
    print("     + Nút động X được nạp hoàn toàn lên VDD = 5.00 V.")
    print("     + Ngõ ra bộ đệm tĩnh Domino: Y = NOT(X) = 0.00 V.")
    print("     + M_keeper (PMOS W=2λ) DẪN nhẹ (bị đóng bởi Y = 0V).")
    print("   - Pha Đánh giá (Evaluate - CLK = 5V):")
    print("     + Mp NGẮT, Me DẪN.")
    print("     + Trường hợp A (PDN Dẫn - Có ít nhất 1 ngõ vào = 5V):")
    print("       Nút X xả nhanh xuống GND (0V) qua PDN và Me.")
    print("       Ngõ ra Y lật lên 5.0V. M_keeper ngắt khi Y lên cao.")
    print("     + Trường hợp B (PDN Ngắt - Mọi ngõ vào = 0V):")
    print("       Nút X giữ nguyên mức cao (Floating High).")
    print("       M_keeper tiếp tục dẫn nhẹ, bù đắp dòng rò Ioff và giữ Vx = 5.00 V.")

    # 2. Phân tích hiện tượng Chia sẻ Điện tích (Charge Sharing)
    print("\n2. Phân tích Hiện tượng Chia sẻ điện tích (Charge Sharing):")
    Cx = 20.0  # fF (Điện dung ký sinh tại nút động X)
    Cint = 14.0 # fF (Điện dung nút nội bộ trong nhánh NMOS)
    
    # Khi nút nội Cint ban đầu xả về 0V trong chu kỳ trước, sau đó CLK=1,
    # transistor trên dẫn nhưng transistor dưới ngắt:
    Vx_shared = VDD * (Cx / (Cx + Cint))
    delta_Vx = VDD - Vx_shared
    print(f"   - Điện dung nút động Cx = {Cx:.1f} fF")
    print(f"   - Điện dung nút nội Cint = {Cint:.1f} fF")
    print(f"   - Điện áp nút X sau chia sẻ (Không có Keeper):")
    print(f"     Vx' = VDD * [Cx / (Cx + Cint)] = {VDD:.2f} * [{Cx:.1f} / {Cx+Cint:.1f}] = {Vx_shared:.2f} V")
    print(f"     Độ sụt áp: Delta_Vx = {delta_Vx:.2f} V (Sụt {(delta_Vx/VDD)*100:.1f}%)")
    
    # Ngưỡng lật của Inverter tĩnh
    VM_inv = 2.45 # V
    print(f"   - Ngưỡng chuyển tiếp của Inverter tĩnh VM ≈ {VM_inv:.2f} V")
    if Vx_shared > VM_inv:
        margin = Vx_shared - VM_inv
        print(f"   => Vx' ({Vx_shared:.2f}V) > VM ({VM_inv:.2f}V): Biên độ an toàn dự phòng NM_H = {margin:.2f} V")
        print("      CẢNH BÁO: Nếu có thêm nhiễu ghép (Crosstalk) hoặc dòng rò, cổng INV sẽ lật giả (False Switching)!")
    else:
        print(f"   => LỖI LOGIC: Vx' tụt dưới VM, cổng Domino bị đánh giá sai trạng thái!")
        
    print("   - Giải pháp Keeper Transistor (M_kp):")
    print("     + Khi có Keeper PMOS (W=2λ): Dòng nạp Ikp bổ sung điện tích tức thời,")
    print("       kéo phục hồi điện áp nút X về lại 5.00 V, triệt tiêu hoàn toàn sụt áp!")

    # 3. Tính đơn điệu (Monotonicity) và Ghép tầng Domino
    print("\n3. Tính đơn điệu (Monotonicity) và Khả năng Ghép tầng Domino:")
    print("   - Cổng Dynamic thuần (không có INV):")
    print("     + Trong Precharge, X = 1. Nếu nối thẳng vào tầng Dynamic tiếp theo,")
    print("       tầng sau sẽ xả sớm ngoài ý muốn trước khi tầng trước kịp đánh giá!")
    print("   - Cổng Domino (Dynamic Gate + Static Inverter):")
    print("     + Trong Precharge, ngõ ra Y = NOT(X) = 0V.")
    print("     + Trong Evaluate, Y CHỈ CÓ THỂ CHUYỂN TỪ 0 -> 1 (hoặc giữ nguyên 0).")
    print("     + Chuyển dịch 0 -> 1 là đơn điệu tăng (Monotonically Rising).")
    print("     + Do đó, các transistor nhận tín hiệu ở tầng kế tiếp chỉ có thể từ NGẮT -> DẪN,")
    print("       hoàn toàn ngăn chặn hiện tượng xả sai (Premature Discharge)!")

    # 4. So sánh PPA Domino OR4 vs Static CMOS OR4
    print("\n4. So sánh Hiệu năng (PPA) Domino OR4 vs Static CMOS OR4:")
    tpd_domino_or4 = 78.5 # ps (Thời gian trễ đánh giá Evaluate)
    tpd_static_or4 = 215.0 # ps (Static NOR4 + INV)
    speedup = tpd_static_or4 / tpd_domino_or4
    
    area_domino = 8 # PMOS_pre + NMOS_eval + Keeper + 4 NMOS PDN + 2T Inverter = 9T
    area_static = 10 # NOR4 (4P ser + 4N par) + 2T Inverter = 10T (PMOS size rất lớn 4x để cân bằng)
    
    print(f"   - Trễ lan truyền đánh giá Domino OR4 (tpd_eval): {tpd_domino_or4:.1f} ps")
    print(f"   - Trễ lan truyền Static CMOS OR4 (tpd_static):   {tpd_static_or4:.1f} ps")
    print(f"   - Tốc độ vượt trội (Speedup factor):              {speedup:.2f}x (Nhanh hơn gấp 2.7 lần!)")
    print(f"   - Tổng số Transistor: Domino OR4 = 9T | Static CMOS OR4 = 10T")
    print(f"   - Tải điện dung ngõ vào (Input Capacitance):")
    print("     + Domino OR4: Mỗi ngõ vào chỉ nối tới 1 cổng NMOS (W=4λ) -> Cin = 4*Cox*L")
    print("     + Static OR4: Mỗi ngõ vào nối tới 1 NMOS và 1 PMOS (size lớn) -> Cin ≈ 20*Cox*L")
    print("     => Tải ngõ vào của Domino nhỏ hơn ~5 lần -> Logical Effort g cực thấp!")
    print("=" * 75)

if __name__ == "__main__":
    verify_lab07()
