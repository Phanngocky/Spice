import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_sram_6t_cell_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10.5, 7.0), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(52.5, 96, "CELL SCHEMATIC: sram_6t_cell{sch}", fontsize=13.5, fontweight='bold', ha='center', color='#1A365D')
    ax.text(52.5, 92, "Ô nhớ tĩnh 6-Transistor SRAM Cell (MOSIS C5N 0.5µm, VDD = 5.0V)", fontsize=9.5, ha='center', color='#4A5568')

    # Power Rails
    ax.plot([25, 80], [84, 84], color='#E53E3E', lw=2.5)
    ax.text(22, 84, "vdd", fontsize=10, fontweight='bold', color='#E53E3E', va='center', ha='right')
    ax.plot([25, 80], [14, 14], color='#2B6CB0', lw=2.5)
    ax.text(22, 14, "gnd", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # Bitlines (Vertical lines on left and right)
    ax.plot([12, 12], [8, 86], color='#805AD5', lw=2.5)
    ax.text(12, 88, "BL", fontsize=11, fontweight='bold', color='#805AD5', ha='center')
    ax.plot([93, 93], [8, 86], color='#805AD5', lw=2.5)
    ax.text(93, 88, "BLB (BL_b)", fontsize=11, fontweight='bold', color='#805AD5', ha='center')

    # Wordline WL (Horizontal line at mid-height)
    ax.plot([5, 100], [48, 48], color='#DD6B20', lw=2.0, ls='--')
    ax.text(3, 48, "WL", fontsize=11, fontweight='bold', color='#DD6B20', va='center', ha='right')

    # Access NMOS Left (M_AX1)
    r_ax1 = patches.FancyBboxPatch((18, 43), 12, 10, boxstyle="round,pad=0.3", facecolor='#FEEBC8', edgecolor='#DD6B20', lw=1.5)
    ax.add_patch(r_ax1)
    ax.text(24, 49, "M_AX1\nW=4λ, L=2λ", fontsize=7.5, fontweight='bold', ha='center', color='#7B341E')
    ax.plot([12, 18], [48, 48], color='#805AD5', lw=2) # BL to AX1
    ax.plot([30, 38], [48, 48], color='#2B6CB0', lw=2) # AX1 to Q

    # Access NMOS Right (M_AX2)
    r_ax2 = patches.FancyBboxPatch((75, 43), 12, 10, boxstyle="round,pad=0.3", facecolor='#FEEBC8', edgecolor='#DD6B20', lw=1.5)
    ax.add_patch(r_ax2)
    ax.text(81, 49, "M_AX2\nW=4λ, L=2λ", fontsize=7.5, fontweight='bold', ha='center', color='#7B341E')
    ax.plot([93, 87], [48, 48], color='#805AD5', lw=2) # BLB to AX2
    ax.plot([75, 67], [48, 48], color='#2B6CB0', lw=2) # AX2 to QB

    # Storage Node Q
    ax.plot([38], [48], marker='o', markersize=6, color='#2B6CB0')
    ax.text(35, 52, "Q", fontsize=11, fontweight='bold', color='#2B6CB0')

    # Storage Node QB
    ax.plot([67], [48], marker='o', markersize=6, color='#2B6CB0')
    ax.text(69, 52, "QB", fontsize=11, fontweight='bold', color='#2B6CB0')

    # Load PMOS Left (M_L1)
    r_l1 = patches.Rectangle((33, 68), 10, 10, facecolor='#FED7D7', edgecolor='#C53030', lw=1.5)
    ax.add_patch(r_l1)
    ax.text(38, 73.5, "M_L1 (PMOS)\nW=2λ, L=2λ", fontsize=7.0, fontweight='bold', ha='center', va='center', color='#9B2C2C')
    ax.plot([38, 38], [78, 84], color='#E53E3E', lw=2) # to VDD
    ax.plot([38, 38], [68, 48], color='#2B6CB0', lw=2) # to Q

    # Driver NMOS Left (M_D1)
    r_d1 = patches.Rectangle((33, 20), 10, 10, facecolor='#E2E8F0', edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(r_d1)
    ax.text(38, 25.5, "M_D1 (Driver)\nW=8λ, L=2λ", fontsize=7.0, fontweight='bold', ha='center', va='center', color='#2C5282')
    ax.plot([38, 38], [20, 14], color='#2B6CB0', lw=2) # to GND
    ax.plot([38, 38], [30, 48], color='#2B6CB0', lw=2) # to Q

    # Load PMOS Right (M_L2)
    r_l2 = patches.Rectangle((62, 68), 10, 10, facecolor='#FED7D7', edgecolor='#C53030', lw=1.5)
    ax.add_patch(r_l2)
    ax.text(67, 73.5, "M_L2 (PMOS)\nW=2λ, L=2λ", fontsize=7.0, fontweight='bold', ha='center', va='center', color='#9B2C2C')
    ax.plot([67, 67], [78, 84], color='#E53E3E', lw=2) # to VDD
    ax.plot([67, 67], [68, 48], color='#2B6CB0', lw=2) # to QB

    # Driver NMOS Right (M_D2)
    r_d2 = patches.Rectangle((62, 20), 10, 10, facecolor='#E2E8F0', edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(r_d2)
    ax.text(67, 25.5, "M_D2 (Driver)\nW=8λ, L=2λ", fontsize=7.0, fontweight='bold', ha='center', va='center', color='#2C5282')
    ax.plot([67, 67], [20, 14], color='#2B6CB0', lw=2) # to GND
    ax.plot([67, 67], [30, 48], color='#2B6CB0', lw=2) # to QB

    # Cross-coupling wires: Q to gates of L2/D2, and QB to gates of L1/D1
    # Q -> Gates of Right Inverter (L2, D2)
    ax.plot([38, 46, 46, 60], [48, 48, 55, 55], color='#3182CE', lw=1.5, ls=':')
    ax.plot([60, 60], [25, 74], color='#3182CE', lw=1.5, ls=':')
    ax.plot([60, 62], [73.5, 73.5], color='#3182CE', lw=1.5) # into L2
    ax.plot([60, 62], [25.5, 25.5], color='#3182CE', lw=1.5) # into D2

    # QB -> Gates of Left Inverter (L1, D1)
    ax.plot([67, 59, 59, 45], [48, 48, 41, 41], color='#DD6B20', lw=1.5, ls=':')
    ax.plot([45, 45], [25, 74], color='#DD6B20', lw=1.5, ls=':')
    ax.plot([45, 43], [73.5, 73.5], color='#DD6B20', lw=1.5) # into L1
    ax.plot([45, 43], [25.5, 25.5], color='#DD6B20', lw=1.5) # into D1

    # Ratio Callouts
    info_cr = (
        "READ STABILITY (Cell Ratio):\n"
        "CR = W_driver / W_access\n"
        "CR = 8λ / 4λ = 2.0 (>= 1.5)\n"
        "-> Ngăn V_Q vượt ngưỡng V_tn\n"
        "   tránh lỗi Read Disturb!"
    )
    ax.text(2, 28, info_cr, fontsize=7.8, family='monospace',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#EBF8FF', edgecolor='#3182CE'))

    info_pr = (
        "WRITABILITY (Pull-up Ratio):\n"
        "PR = W_load / W_access\n"
        "PR = 2λ / 4λ = 0.5 (<= 1.0)\n"
        "-> Access kéo tụt nút '1' xuống '0'\n"
        "   thắng PMOS Load khi Ghi!"
    )
    ax.text(103, 28, info_pr, fontsize=7.8, family='monospace', ha='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFAF0', edgecolor='#DD6B20'))

    # Footer note
    ax.text(52.5, 5, "TỔ CHỨC 6T: 2 Inverter ghép chéo (L1/D1 & L2/D2) + 2 Transistor truy xuất Access (AX1, AX2)",
            fontsize=8.5, ha='center', color='#2D3748', style='italic')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")


def draw_sense_amplifier_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10.5, 6.8), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(52.5, 96, "MẠCH KHUẾCH ĐẠI CẢM NHẬN (VOLTAGE LATCH SENSE AMPLIFIER)", fontsize=13, fontweight='bold', ha='center', color='#1A365D')
    ax.text(52.5, 92, "Cơ chế khuếch đại vi sai biên độ nhỏ (100 - 200mV) thành mức logic số toàn dải (0V - 5.0V)", fontsize=9.2, ha='center', color='#4A5568')

    # Power Rails
    ax.plot([15, 90], [86, 86], color='#E53E3E', lw=2.5)
    ax.text(12, 86, "vdd", fontsize=10, fontweight='bold', color='#E53E3E', va='center', ha='right')
    ax.plot([15, 90], [10, 10], color='#2B6CB0', lw=2.5)
    ax.text(12, 10, "gnd", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # Bitline inputs from memory array (top)
    ax.plot([30, 30], [92, 80], color='#805AD5', lw=2.0)
    ax.text(30, 94, "BL", fontsize=10, fontweight='bold', color='#805AD5', ha='center')
    ax.plot([75, 75], [92, 80], color='#805AD5', lw=2.0)
    ax.text(75, 94, "BLB", fontsize=10, fontweight='bold', color='#805AD5', ha='center')

    # Equalization & Precharge Block
    rect_pre = patches.FancyBboxPatch((25, 72), 55, 11, boxstyle="round,pad=0.3", facecolor='#FED7D7', edgecolor='#C53030', lw=1.2)
    ax.add_patch(rect_pre)
    ax.text(52.5, 78, "KHỐI NẠP TRƯỚC VÀ CÂN BẰNG BITLINE (PRECHARGE & EQ)", fontsize=8.5, fontweight='bold', ha='center', color='#9B2C2C')
    ax.text(52.5, 74, "3 PMOS: Nạp BL & BLB lên VDD và cân bằng điện áp triệt tiêu offset", fontsize=7.5, ha='center', color='#742A2A')

    # Isolation / Sense Nodes SO and SOB
    ax.plot([38, 38], [72, 60], color='#2B6CB0', lw=2.0)
    ax.plot([38], [55], marker='o', markersize=6, color='#2B6CB0')
    ax.text(33, 55, "SO", fontsize=10.5, fontweight='bold', color='#2B6CB0')

    ax.plot([67, 67], [72, 60], color='#2B6CB0', lw=2.0)
    ax.plot([67], [55], marker='o', markersize=6, color='#2B6CB0')
    ax.text(71, 55, "SOB", fontsize=10.5, fontweight='bold', color='#2B6CB0')

    # Cross-coupled Latch (Inverter Pair)
    rect_latch = patches.FancyBboxPatch((30, 32), 45, 26, boxstyle="round,pad=0.5", facecolor='#EBF8FF', edgecolor='#3182CE', lw=1.5)
    ax.add_patch(rect_latch)
    ax.text(52.5, 47, "LATCH CHỐT CHÉO VI SAI (CROSS-COUPLED PAIR)", fontsize=9, fontweight='bold', ha='center', color='#2B6CB0')
    ax.text(52.5, 41, "2 PMOS (Kéo lên) + 2 NMOS (Kéo xuống)\nHồi tiếp dương siêu nhanh (Positive Feedback)", fontsize=7.5, ha='center', color='#2C5282')

    # Tail NMOS (M_tail) activated by SAEN
    r_tail = patches.FancyBboxPatch((44, 16), 17, 10, boxstyle="round,pad=0.3", facecolor='#ED8936', edgecolor='#C05621', lw=1.5)
    ax.add_patch(r_tail)
    ax.text(52.5, 22, "M_tail (NMOS)\nW=12λ, L=2λ", fontsize=7.5, fontweight='bold', ha='center', color='white')
    ax.plot([52.5, 52.5], [32, 26], color='#2B6CB0', lw=2.0)
    ax.plot([52.5, 52.5], [16, 10], color='#2B6CB0', lw=2.0)

    # SAEN Gate
    ax.plot([44, 30], [21, 21], color='#DD6B20', lw=2.0)
    ax.plot([30], [21], marker='s', markersize=7, color='#DD6B20')
    ax.text(28, 21, "SAEN", fontsize=10, fontweight='bold', color='#DD6B20', va='center', ha='right')

    # Principle callout
    sa_info = (
        "NGUYÊN LÝ HOẠT ĐỘNG:\n"
        "1. Trước đọc: Precharge BL & BLB lên VDD (5.0V).\n"
        "2. Đọc: WL kích hoạt, ô nhớ kéo tụt nhẹ một đường (Delta_V ≈ 150mV).\n"
        "3. Kích xung SAEN = 1: M_tail mở, hồi tiếp dương khuếch đại vi sai\n"
        "   nhanh chóng chốt SO/SOB về 5.0V và 0V trong < 100ps!\n"
        "-> Giảm 95% công suất nạp/xả Bitline & tăng tốc đọc > 5 lần!"
    )
    ax.text(52.5, 2, sa_info, fontsize=7.5, family='monospace', ha='center', va='bottom',
            bbox=dict(boxstyle='square,pad=0.5', facecolor='#F7FAFC', edgecolor='#CBD5E0'))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_sram_6t_cell_schematic("02 - Giao_Trinh_Lab_Handouts/images/sram_6t_cell_schematic.png")
    draw_sense_amplifier_schematic("02 - Giao_Trinh_Lab_Handouts/images/sense_amplifier_schematic.png")
