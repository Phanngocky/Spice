"""
Script kiểm chứng tính toán giải tích và mô phỏng SPICE:
Mô phỏng Phân cực DC và Đặc tuyến Vào - Ra của Transistor Lưỡng cực BJT NPN (2N3904)
Học phần: Thực hành Thiết kế VLSI (5505382)
"""

def verify_bjt():
    print("=" * 75)
    print("KIỂM CHỨNG TÍNH TOÁN GIẢI TÍCH BJT NPN - PHÂN CỰC & ĐẶC TUYẾN VÀO/RA")
    print("=" * 75)

    # Thông số linh kiện mạch phân cực phân áp (Voltage Divider Bias)
    VCC = 12.0      # V
    R1 = 33.0e3     # 33 kOhm
    R2 = 10.0e3     # 10 kOhm
    RC = 2.2e3      # 2.2 kOhm
    RE = 1.0e3      # 1.0 kOhm

    # Thông số transistor 2N3904 tiêu chuẩn
    VBE_on = 0.68   # V
    beta = 160.0    # hFE tiêu chuẩn ở dòng mA
    VA = 74.0       # Early Voltage (V)

    # 1. Phân tích Phân cực DC (Điểm làm việc tĩnh Q)
    print("\n1. Phân tích Điểm làm việc tĩnh DC (Q-Point) Mạch Phân áp:")
    V_TH = VCC * (R2 / (R1 + R2))
    R_TH = (R1 * R2) / (R1 + R2)

    print(f"   - Nguồn tương đương Thevenin: V_TH = VCC * R2/(R1+R2) = {V_TH:.3f} V")
    print(f"   - Trở tương đương Thevenin:   R_TH = R1 // R2          = {R_TH/1e3:.3f} kOhm")

    # Dòng cực Base IB:
    # V_TH - IB * R_TH - VBE - IE * RE = 0, với IE = (beta + 1) * IB
    IB = (V_TH - VBE_on) / (R_TH + (beta + 1) * RE)
    IC = beta * IB
    IE = (beta + 1) * IB

    VE = IE * RE
    VB = VE + VBE_on
    VC = VCC - IC * RC
    VCE = VC - VE

    print(f"   - Dòng điện cực gốc:          I_B  = {IB*1e6:.2f} uA")
    print(f"   - Dòng điện cực thu:          I_C  = {IC*1e3:.3f} mA")
    print(f"   - Dòng điện cực phát:         I_E  = {IE*1e3:.3f} mA")
    print(f"   - Điện áp cực phát:           V_E  = {VE:.3f} V")
    print(f"   - Điện áp cực gốc:            V_B  = {VB:.3f} V")
    print(f"   - Điện áp cực thu:            V_C  = {VC:.3f} V")
    print(f"   - Điện áp Collector - Emitter: V_CE = {VCE:.3f} V")

    # Kiểm tra điều kiện vùng tích cực (Forward-Active Mode):
    VCE_sat = 0.20
    if VCE > VCE_sat and VB > VE:
        print(f"   => KẾT LUẬN CHẾ ĐỘ: V_CE ({VCE:.2f}V) > V_CE,sat ({VCE_sat}V) và V_BE ({VBE_on}V) > 0:")
        print(f"      Transistor hoạt động ở CHẾ ĐỘ TÍCH CỰC THUẬN (Forward-Active) lý tưởng.")
        print(f"      Điểm tĩnh Q (V_CEQ = {VCE:.2f}V, I_CQ = {IC*1e3:.2f}mA) nằm ở vị trí trung tâm đường tải tĩnh!")
    else:
        print("   => CẢNH BÁO: Transistor rơi vào vùng bão hòa hoặc ngưng dẫn!")

    # 2. Đặc tuyến Ngõ vào (Input Characteristic: IB vs VBE)
    print("\n2. Phân tích Đặc tuyến Ngõ vào (Input Characteristic: I_B vs V_BE):")
    print("   - Phương trình Ebers-Moll: I_B = (I_S / beta) * [exp(V_BE / V_T) - 1]")
    print(f"   - Điện áp nhiệt ở 300K:    V_T = k*T/q ≈ 25.85 mV")
    print("   - Vùng ngưng dẫn:          V_BE < 0.60V -> I_B ≈ 0")
    print(f"   - Ngưỡng mở (Knee Voltage): V_BE,on ≈ 0.65V - 0.70V")
    print("   - Khi V_BE >= 0.70V:       Dòng I_B tăng theo hàm mũ dốc đứng.")

    # 3. Họ Đặc tuyến Ngõ ra (Output Family: IC vs VCE theo tham số IB)
    print("\n3. Phân tích Họ Đặc tuyến Ngõ ra (Output Characteristics: I_C vs V_CE):")
    print("   - Quét tham số: I_B = 10 uA, 20 uA, 30 uA, 40 uA, 50 uA")
    print("   - Vùng bão hòa (Saturation): 0 <= V_CE < 0.2V (I_C tăng tuyến tính dốc theo V_CE)")
    print("   - Vùng khuếch đại (Active):  V_CE >= 0.2V:")
    for ib_val in [10e-6, 20e-6, 30e-6, 40e-6, 50e-6]:
        # Xét hiệu ứng Early: IC = beta * IB * (1 + VCE / VA) tại VCE = 5V
        ic_active = beta * ib_val * (1.0 + 5.0 / VA)
        print(f"     + Tại I_B = {ib_val*1e6:2.0f} uA, V_CE = 5.0V: I_C ≈ {ic_active*1e3:.3f} mA (beta_eff = {ic_active/ib_val:.1f})")
    print(f"   - Hiệu ứng Early: Độ dốc đường đặc tuyến dI_C/dV_CE = (beta * I_B) / V_A")
    print(f"     Ngoại suy giao trục hoành tại V_CE = -V_A = -{VA:.1f} V")
    print("=" * 75)

if __name__ == "__main__":
    verify_bjt()
