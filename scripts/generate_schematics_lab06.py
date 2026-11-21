import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_mirror_adder_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10.5, 7), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(52.5, 96, "CELL SCHEMATIC: mirror_adder_1b{sch}", fontsize=14, fontweight='bold', ha='center', color='#1A365D')
    ax.text(52.5, 92, "Mạch cộng toàn phần 1-bit kiểu Gương (28-Transistor Mirror Adder)", fontsize=10, ha='center', color='#4A5568')

    # Rails
    ax.plot([5, 100], [87, 87], color='#E53E3E', lw=2.5)
    ax.text(3, 87, "vdd", fontsize=10, fontweight='bold', color='#E53E3E', va='center', ha='right')
    ax.plot([5, 100], [13, 13], color='#2B6CB0', lw=2.5)
    ax.text(3, 13, "gnd", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # Block 1: Carry Generation Block (Cout_b) - Left
    rect_c = patches.FancyBboxPatch((8, 18), 38, 64, boxstyle="round,pad=1.0", facecolor='#F7FAFC', edgecolor='#2B6CB0', lw=1.8)
    ax.add_patch(rect_c)
    ax.text(27, 83, "KHỐI TẠO CARRY (Cout_b)", fontsize=10.5, fontweight='bold', ha='center', color='#2B6CB0')
    ax.text(27, 79, r"$\overline{C_{out}} = \overline{AB + C_{in}(A+B)}$ (8 MOSFETs)", fontsize=8.5, ha='center', color='#4A5568')

    # Draw Carry PUN (Top of Block 1)
    # Series Cin with (A // B), and parallel with (A series B)
    r_cp1 = patches.Rectangle((12, 63), 12, 10, facecolor='#FED7D7', edgecolor='#C53030', lw=1.2)
    ax.add_patch(r_cp1)
    ax.text(18, 68, "Cin\n(P1)", fontsize=8, fontweight='bold', ha='center', va='center', color='#9B2C2C')

    r_cp2 = patches.Rectangle((28, 63), 14, 10, facecolor='#FED7D7', edgecolor='#C53030', lw=1.2)
    ax.add_patch(r_cp2)
    ax.text(35, 68, "A // B\n(P2, P3)", fontsize=8, fontweight='bold', ha='center', va='center', color='#9B2C2C')

    # Carry PDN (Bottom of Block 1)
    r_cn1 = patches.Rectangle((12, 27), 12, 10, facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.2)
    ax.add_patch(r_cn1)
    ax.text(18, 32, "Cin\n(N1)", fontsize=8, fontweight='bold', ha='center', va='center', color='#2B6CB0')

    r_cn2 = patches.Rectangle((28, 27), 14, 10, facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.2)
    ax.add_patch(r_cn2)
    ax.text(35, 32, "A // B\n(N2, N3)", fontsize=8, fontweight='bold', ha='center', va='center', color='#2B6CB0')

    # Cout_b line
    ax.plot([40, 46], [50, 50], color='#2B6CB0', lw=2)
    ax.plot([46], [50], marker='o', markersize=4, color='#2B6CB0')
    ax.text(46, 53, "cout_b", fontsize=8.5, fontweight='bold', color='#4A5568', ha='center')

    # Cout Inverter
    tri_c = patches.Polygon([[46, 45], [46, 55], [51, 50]], facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.2)
    ax.add_patch(tri_c)
    bub_c = patches.Circle((52, 50), 1.0, facecolor='white', edgecolor='#4A5568', lw=1.2)
    ax.add_patch(bub_c)
    ax.plot([53, 58], [50, 50], color='#2B6CB0', lw=2)
    ax.plot([58], [50], marker='s', markersize=8, color='#2B6CB0')
    ax.text(60, 50, "cout", fontsize=10.5, fontweight='bold', color='#2B6CB0', va='center')

    # Block 2: Sum Generation Block - Right
    rect_s = patches.FancyBboxPatch((55, 18), 44, 64, boxstyle="round,pad=1.0", facecolor='#F7FAFC', edgecolor='#C53030', lw=1.8)
    ax.add_patch(rect_s)
    ax.text(77, 83, "KHỐI TẠO TỔNG (Sum_b)", fontsize=10.5, fontweight='bold', ha='center', color='#C53030')
    ax.text(77, 79, r"$\overline{Sum} = ABC_{in} + \overline{C_{out}}(A+B+C_{in})$ (12 MOSFETs)", fontsize=8, ha='center', color='#4A5568')

    # Sum PUN (Top of Block 2)
    r_sp1 = patches.Rectangle((60, 63), 16, 10, facecolor='#FED7D7', edgecolor='#C53030', lw=1.2)
    ax.add_patch(r_sp1)
    ax.text(68, 68, "A // B // Cin\n(P4, P5, P6)", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#9B2C2C')

    r_sp2 = patches.Rectangle((80, 63), 15, 10, facecolor='#FED7D7', edgecolor='#C53030', lw=1.2)
    ax.add_patch(r_sp2)
    ax.text(87.5, 68, "cout_b\n(P7)", fontsize=8, fontweight='bold', ha='center', va='center', color='#9B2C2C')

    # Sum PDN (Bottom of Block 2)
    r_sn1 = patches.Rectangle((60, 27), 16, 10, facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.2)
    ax.add_patch(r_sn1)
    ax.text(68, 32, "A // B // Cin\n(N4, N5, N6)", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#2B6CB0')

    r_sn2 = patches.Rectangle((80, 27), 15, 10, facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.2)
    ax.add_patch(r_sn2)
    ax.text(87.5, 32, "cout_b\n(N7)", fontsize=8, fontweight='bold', ha='center', va='center', color='#2B6CB0')

    # Sum_b line
    ax.plot([87.5, 87.5], [58, 50], color='#C53030', lw=1.5)
    ax.plot([87.5, 91], [50, 50], color='#C53030', lw=2)
    ax.text(89, 53, "sum_b", fontsize=7.5, fontweight='bold', color='#4A5568', ha='center')

    # Sum Inverter
    tri_s = patches.Polygon([[91, 45], [91, 55], [96, 50]], facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.2)
    ax.add_patch(tri_s)
    bub_s = patches.Circle((97, 50), 1.0, facecolor='white', edgecolor='#4A5568', lw=1.2)
    ax.add_patch(bub_s)
    ax.plot([98, 102], [50, 50], color='#2B6CB0', lw=2)
    ax.plot([102], [50], marker='s', markersize=8, color='#2B6CB0')
    ax.text(103.5, 50, "sum", fontsize=10.5, fontweight='bold', color='#2B6CB0', va='center')

    # Connect Cout_b to Sum block
    ax.plot([46, 46], [50, 40], color='#4A5568', lw=1.2, ls=':')
    ax.plot([46, 80], [40, 40], color='#4A5568', lw=1.2, ls=':')
    ax.plot([80, 80], [40, 37], color='#4A5568', lw=1.2, ls=':')
    ax.plot([80, 80], [40, 63], color='#4A5568', lw=1.2, ls=':')
    ax.text(63, 42, "cout_b phản hồi vào khối Sum", fontsize=7.5, color='#4A5568', style='italic')

    # Summary Info Box
    summary_box = (
        "ĐẶC ĐIỂM KỸ THUẬT MIRROR ADDER (24 - 28 TRANSISTORS):\n"
        "• Khối Carry: 8T (4 PMOS + 4 NMOS) + 2T Inverter = 10 Transistors.\n"
        "• Khối Sum: 12T (6 PMOS + 6 NMOS) + 2T Inverter = 14 Transistors (Tổng 24T lõi, có đệm 28T).\n"
        "• ĐƯỜNG TRỄ TỚI HẠN (CRITICAL PATH): Cin -> Cout chỉ qua 1 tầng logic + 1 Inverter đệm (tpd ≈ 60ps).\n"
        "• Cực Cổng Cin được bố trí sát nút ngõ ra Cout_b nhất để cực tiểu hóa điện trở/điện dung ký sinh."
    )
    ax.text(52.5, 6, summary_box, fontsize=8.2, family='monospace',
            bbox=dict(boxstyle='square,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'),
            ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

def draw_tg_adder_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, "CELL SCHEMATIC: tg_adder_1b{sch}", fontsize=13.5, fontweight='bold', ha='center', color='#1A365D')
    ax.text(50, 90, "Mạch cộng toàn phần dùng Cổng truyền (16-Transistor Transmission Gate Adder)", fontsize=9.5, ha='center', color='#4A5568')

    # Inputs A, B, Cin
    ax.plot([5, 15], [75, 75], color='#2B6CB0', lw=2)
    ax.plot([5], [75], marker='s', markersize=7, color='#2B6CB0')
    ax.text(3, 75, "a", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    ax.plot([5, 15], [60, 60], color='#2B6CB0', lw=2)
    ax.plot([5], [60], marker='s', markersize=7, color='#2B6CB0')
    ax.text(3, 60, "b", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    ax.plot([5, 50], [25, 25], color='#2B6CB0', lw=2)
    ax.plot([5], [25], marker='s', markersize=7, color='#2B6CB0')
    ax.text(3, 25, "cin", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # XOR1 Block (A xor B -> P)
    rect_xor1 = patches.FancyBboxPatch((15, 52), 22, 32, boxstyle="round,pad=0.5", facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(rect_xor1)
    ax.text(26, 73, "TG XOR1", fontsize=9.5, fontweight='bold', ha='center', color='#2B6CB0')
    ax.text(26, 62, "P = A ⊕ B\n(4 - 6 Transistors)", fontsize=8, ha='center', color='#2C5282')

    # Line P out
    ax.plot([37, 50], [68, 68], color='#2B6CB0', lw=2)
    ax.plot([44], [68], marker='o', markersize=4, color='#2B6CB0')
    ax.text(44, 72, "P", fontsize=9, fontweight='bold', color='#2B6CB0', ha='center')

    # XOR2 Block (P xor Cin -> Sum)
    rect_xor2 = patches.FancyBboxPatch((50, 52), 24, 32, boxstyle="round,pad=0.5", facecolor='#FED7D7', edgecolor='#C53030', lw=1.5)
    ax.add_patch(rect_xor2)
    ax.text(62, 73, "TG XOR2", fontsize=9.5, fontweight='bold', ha='center', color='#C53030')
    ax.text(62, 62, "Sum = P ⊕ Cin\n(4 Transistors)", fontsize=8, ha='center', color='#9B2C2C')

    # Line Cin up to XOR2
    ax.plot([30, 30], [25, 38], color='#2B6CB0', lw=1.5)
    ax.plot([30, 50], [38, 38], color='#2B6CB0', lw=1.5)
    ax.plot([50, 50], [38, 58], color='#2B6CB0', lw=1.5)

    # Line Sum out
    ax.plot([74, 90], [68, 68], color='#2B6CB0', lw=2)
    ax.plot([90], [68], marker='s', markersize=8, color='#2B6CB0')
    ax.text(93, 68, "sum", fontsize=10.5, fontweight='bold', color='#2B6CB0', va='center')

    # Carry MUX Block: Cout = MUX(Cin, A, sel=P)
    # When P=1 -> Cout = Cin; When P=0 -> Cout = A
    rect_mux = patches.FancyBboxPatch((50, 15), 24, 25, boxstyle="round,pad=0.5", facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.5)
    ax.add_patch(rect_mux)
    ax.text(62, 32, "TG MUX (Cout)", fontsize=9.5, fontweight='bold', ha='center', color='#B7791F')
    ax.text(62, 22, "P=1: Cout = Cin\nP=0: Cout = A\n(4 Transistors)", fontsize=7.5, ha='center', color='#744210')

    # Connect A to MUX
    ax.plot([10, 10], [75, 18], color='#2B6CB0', lw=1.2)
    ax.plot([10, 50], [18, 18], color='#2B6CB0', lw=1.2)

    # Connect P to MUX Select
    ax.plot([44, 44], [68, 48], color='#2B6CB0', lw=1.2)
    ax.plot([44, 62], [48, 48], color='#2B6CB0', lw=1.2)
    ax.plot([62, 62], [48, 40], color='#2B6CB0', lw=1.2)

    # Line Cout out
    ax.plot([74, 90], [27, 27], color='#2B6CB0', lw=2)
    ax.plot([90], [27], marker='s', markersize=8, color='#2B6CB0')
    ax.text(93, 27, "cout", fontsize=10.5, fontweight='bold', color='#2B6CB0', va='center')

    # Footnote
    ax.text(50, 4, "ƯU THẾ: Tổng cộng chỉ dùng 16 Transistors (Tiết kiệm 43% diện tích so với Mirror Adder 28T)",
            fontsize=8.5, family='monospace', ha='center', color='#2D3748')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_mirror_adder_schematic("02 - Giao_Trinh_Lab_Handouts/images/mirror_adder_schematic.png")
    draw_tg_adder_schematic("02 - Giao_Trinh_Lab_Handouts/images/tg_adder_schematic.png")
