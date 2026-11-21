import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_cla_4bit_architecture(out_path):
    fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(55, 96, "KIẾN TRÚC ĐƯỜNG DỮ LIỆU BỘ CỘNG NHANH 4-BIT (4-BIT CLA ADDER)", fontsize=13, fontweight='bold', ha='center', color='#1A365D')
    ax.text(55, 92, "Cấu trúc 3 tầng: Khối sinh cờ PG -> Khối tạo số nhớ sớm CLG -> Khối tạo Tổng Sum", fontsize=9.2, ha='center', color='#4A5568')

    # Top Inputs A[3:0] and B[3:0]
    for i in range(4):
        x = 18 + i * 22
        ax.plot([x - 3, x - 3], [88, 76], color='#2B6CB0', lw=2)
        ax.plot([x + 3, x + 3], [88, 76], color='#2B6CB0', lw=2)
        ax.text(x - 3, 89, f"A[{i}]", fontsize=8.5, fontweight='bold', color='#2B6CB0', ha='center')
        ax.text(x + 3, 89, f"B[{i}]", fontsize=8.5, fontweight='bold', color='#2B6CB0', ha='center')

    # Stage 1: 4 PG Units
    for i in range(4):
        x = 18 + i * 22
        r_pg = patches.FancyBboxPatch((x - 8, 64), 16, 12, boxstyle="round,pad=0.3", facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.5)
        ax.add_patch(r_pg)
        ax.text(x, 71, f"PG CELL {i}", fontsize=8.5, fontweight='bold', color='#1A365D', ha='center')
        ax.text(x, 66.5, f"Pi = Ai ⊕ Bi\nGi = Ai · Bi", fontsize=6.8, ha='center', color='#2C5282')

    # Lines from PG to CLG and Sum
    for i in range(4):
        x = 18 + i * 22
        # Gi to CLG
        ax.plot([x - 3, x - 3], [64, 52], color='#C53030', lw=1.5)
        ax.text(x - 4, 58, f"G{i}", fontsize=7.5, color='#C53030', ha='right')
        # Pi to CLG
        ax.plot([x + 3, x + 3], [64, 52], color='#DD6B20', lw=1.5)
        ax.text(x + 4, 58, f"P{i}", fontsize=7.5, color='#DD6B20', ha='left')
        # Pi bypass to Sum Stage (dashed line)
        ax.plot([x + 5, x + 5, x + 7, x + 7], [64, 60, 60, 26], color='#805AD5', lw=1.2, ls=':')

    # Stage 2: Carry Lookahead Generator (CLG) Block
    r_clg = patches.FancyBboxPatch((8, 38), 92, 14, boxstyle="round,pad=0.5", facecolor='#FED7D7', edgecolor='#C53030', lw=2)
    ax.add_patch(r_clg)
    ax.text(55, 47, "KHỐI TẠO SỐ NHỚ NHANH (CARRY LOOKAHEAD GENERATOR - CLG)", fontsize=10, fontweight='bold', color='#9B2C2C', ha='center')
    ax.text(55, 41.5, "Tính toán song song C1, C2, C3, C4 qua các cổng logic phức hợp AOI (Trễ chỉ qua 1 tầng cổng)", fontsize=7.8, ha='center', color='#742A2A')

    # Cin (C0) Input on right
    ax.plot([106, 100], [45, 45], color='#C53030', lw=2)
    ax.plot([106], [45], marker='s', markersize=6, color='#C53030')
    ax.text(108, 45, "Cin (C0)", fontsize=9, fontweight='bold', color='#C53030', va='center')
    # Cin also branches to Sum0
    ax.plot([102, 102, 23, 23], [45, 30, 30, 26], color='#C53030', lw=1.2, ls='--')

    # Carry outputs C1, C2, C3 from CLG to Sum Units
    for i in range(1, 4):
        x_sum = 18 + i * 22
        ax.plot([x_sum - 2, x_sum - 2], [38, 26], color='#C53030', lw=1.8)
        ax.text(x_sum - 3, 32, f"C{i}", fontsize=7.5, fontweight='bold', color='#C53030', ha='right')

    # Carry Output C4 on left
    ax.plot([8, 2], [45, 45], color='#C53030', lw=2.5)
    ax.plot([2], [45], marker='s', markersize=7, color='#C53030')
    ax.text(1, 48, "Cout (C4)", fontsize=10, fontweight='bold', color='#C53030', ha='left')

    # Stage 3: 4 Sum XOR Units
    for i in range(4):
        x = 18 + i * 22
        r_sum = patches.FancyBboxPatch((x - 8, 14), 16, 12, boxstyle="round,pad=0.3", facecolor='#E9D8FD', edgecolor='#6B46C1', lw=1.5)
        ax.add_patch(r_sum)
        ax.text(x, 21.5, f"SUM CELL {i}", fontsize=8.5, fontweight='bold', color='#44337A', ha='center')
        ax.text(x, 16.5, f"Si = Pi ⊕ Ci", fontsize=7.5, ha='center', color='#553C9A')

        # Output Sum lines
        ax.plot([x, x], [14, 4], color='#6B46C1', lw=2)
        ax.plot([x], [4], marker='s', markersize=7, color='#6B46C1')
        ax.text(x, 1.5, f"S[{i}]", fontsize=9.5, fontweight='bold', color='#6B46C1', ha='center')

    # Side callout: Delay advantage
    info_box = (
        "ƯU THẾ TỐC ĐỘ:\n"
        "• RCA: Trễ Carry = 4 * t_carry ≈ 340 ps (Nối tiếp O(N))\n"
        "• CLA: Trễ Carry = t_PG + t_CLG ≈ 175 ps (Song song O(1))\n"
        "-> Tốc độ tăng gần gấp đôi so với Bộ cộng gợn sóng!"
    )
    ax.text(55, 7, info_box, fontsize=7.5, family='monospace', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F7FAFC', edgecolor='#CBD5E0'))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")


def draw_clg_carry_logic_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10.5, 6.8), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(52.5, 96, "SƠ ĐỒ LOGIC KHỐI TẠO SỐ NHỚ (CARRY LOOKAHEAD LOGIC)", fontsize=13, fontweight='bold', ha='center', color='#1A365D')
    ax.text(52.5, 92, "Hiện thực hệ phương trình số nhớ song song bằng cổng phức hợp AOI", fontsize=9.2, ha='center', color='#4A5568')

    # 4 Carry Equation Boxes
    eqs = [
        ("C1 = G0 + P0·C0",
         "Cổng AOI21 + Inverter\n(1 nhánh 2T nối tiếp + 1 nhánh 1T)",
         80, '#FED7D7', '#C53030'),
        ("C2 = G1 + P1·G0 + P1·P0·C0",
         "Cổng AOI321 + Inverter\n(3 nhánh song song: 1T, 2T, 3T)",
         58, '#FEEBC8', '#DD6B20'),
        ("C3 = G2 + P2·G1 + P2·P1·G0 + P2·P1·P0·C0",
         "Cổng AOI4321 + Inverter\n(4 nhánh song song: 1T, 2T, 3T, 4T)",
         36, '#EBF8FF', '#3182CE'),
        ("C4 = G3 + P3·G2 + P3·P2·G1 + P3·P2·P1·G0 + P3·P2·P1·P0·C0",
         "Cổng AOI54321 + Inverter\n(5 nhánh song song: 1T, 2T, 3T, 4T, 5T)",
         14, '#E9D8FD', '#6B46C1')
    ]

    for title, desc, y, bg, border in eqs:
        r = patches.FancyBboxPatch((8, y - 8), 88, 16, boxstyle="round,pad=0.4", facecolor=bg, edgecolor=border, lw=1.5)
        ax.add_patch(r)
        ax.text(12, y + 3, title, fontsize=10, fontweight='bold', color=border)
        ax.text(12, y - 4, desc, fontsize=8, color='#2D3748')

        # Output pin on right
        ax.plot([96, 102], [y, y], color=border, lw=2)
        ax.plot([102], [y], marker='s', markersize=6, color=border)
        carry_name = title.split(" = ")[0]
        ax.text(103, y, carry_name, fontsize=10, fontweight='bold', color=border, va='center')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_cla_4bit_architecture("02 - Giao_Trinh_Lab_Handouts/images/cla_4bit_architecture.png")
    draw_clg_carry_logic_schematic("02 - Giao_Trinh_Lab_Handouts/images/clg_carry_logic_schematic.png")
