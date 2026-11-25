import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_dynamic_cmos_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, "NGUYÊN LÝ CỔNG LOGIC ĐỘNG (DYNAMIC CMOS LOGIC)", fontsize=13.5, fontweight='bold', ha='center', color='#1A365D')
    ax.text(50, 91, "Cơ chế 2 pha: Precharge (CLK=0) và Evaluate (CLK=1) & Hiện tượng Charge Sharing", fontsize=9.5, ha='center', color='#4A5568')

    # Rails
    ax.plot([15, 85], [85, 85], color='#E53E3E', lw=2.5)
    ax.text(12, 85, "vdd", fontsize=10, fontweight='bold', color='#E53E3E', va='center', ha='right')
    ax.plot([15, 85], [12, 12], color='#2B6CB0', lw=2.5)
    ax.text(12, 12, "gnd", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # Precharge PMOS (top)
    rect_p = patches.FancyBboxPatch((40, 70), 20, 10, boxstyle="round,pad=0.5", facecolor='#FED7D7', edgecolor='#C53030', lw=1.5)
    ax.add_patch(rect_p)
    ax.text(50, 76, "Mp (Precharge)", fontsize=9, fontweight='bold', ha='center', color='#C53030')
    ax.text(50, 72, "W=12λ, L=2λ", fontsize=7.5, ha='center', color='#2D3748')
    # PMOS Gate (CLK)
    ax.plot([40, 30], [75, 75], color='#4A5568', lw=1.5)
    ax.plot([30], [75], marker='s', markersize=7, color='#4A5568')
    ax.text(28, 75, "clk", fontsize=9, fontweight='bold', color='#4A5568', va='center', ha='right')
    # Line to VDD
    ax.plot([50, 50], [80, 85], color='#C53030', lw=2)

    # Dynamic Node X
    ax.plot([50, 50], [70, 55], color='#2B6CB0', lw=2)
    ax.plot([50], [55], marker='o', markersize=5, color='#2B6CB0')
    ax.text(53, 56, "Nút động X (C_X)", fontsize=9.5, fontweight='bold', color='#2B6CB0', va='bottom')

    # Line out from Node X
    ax.plot([50, 80], [55, 55], color='#2B6CB0', lw=2)
    ax.plot([80], [55], marker='s', markersize=8, color='#2B6CB0')
    ax.text(82, 55, "out_dyn", fontsize=10, fontweight='bold', color='#2B6CB0', va='center')

    # Capacitor Cx (Parasitic at Node X)
    ax.plot([70, 70], [55, 48], color='#718096', lw=1.2)
    ax.plot([67, 73], [48, 48], color='#718096', lw=1.5)
    ax.plot([67, 73], [46, 46], color='#718096', lw=1.5)
    ax.plot([70, 70], [46, 42], color='#718096', lw=1.2)
    ax.text(75, 47, r"$C_X$", fontsize=8.5, color='#718096')

    # PDN Network (Logic Block)
    rect_pdn = patches.FancyBboxPatch((38, 32), 24, 18, boxstyle="round,pad=0.5", facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(rect_pdn)
    ax.text(50, 43, "MẠNG PDN (NMOS)", fontsize=9.5, fontweight='bold', ha='center', color='#2B6CB0')
    ax.text(50, 37, "Thực hiện hàm logic\n(Nút nội Cint)", fontsize=7.5, ha='center', color='#2C5282')
    # Line from Node X to PDN
    ax.plot([50, 50], [55, 50], color='#2B6CB0', lw=1.5)

    # Evaluate Foot NMOS (bottom)
    rect_foot = patches.FancyBboxPatch((40, 16), 20, 10, boxstyle="round,pad=0.5", facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.5)
    ax.add_patch(rect_foot)
    ax.text(50, 22, "Me (Evaluate Foot)", fontsize=8.5, fontweight='bold', ha='center', color='#2D3748')
    ax.text(50, 18, "W=8λ, L=2λ", fontsize=7.5, ha='center', color='#4A5568')
    # Foot Gate (CLK)
    ax.plot([40, 30], [21, 21], color='#4A5568', lw=1.5)
    ax.plot([30], [21], marker='s', markersize=7, color='#4A5568')
    ax.text(28, 21, "clk", fontsize=9, fontweight='bold', color='#4A5568', va='center', ha='right')
    # Line from PDN to Foot, Foot to GND
    ax.plot([50, 50], [32, 26], color='#2B6CB0', lw=1.5)
    ax.plot([50, 50], [16, 12], color='#2B6CB0', lw=2)

    # Info Box: 2 Phases
    info_box = (
        "CHU TRÌNH 2 PHA:\n"
        "1. Pha Nạp trước (Precharge - CLK = 0):\n"
        "   - Mp DẪN nạp nút X lên VDD (5.0V)\n"
        "   - Me NGẮT ngăn dòng xả xuống đất\n"
        "2. Pha Đánh giá (Evaluate - CLK = 1):\n"
        "   - Mp NGẮT, Me DẪN cho phép xả\n"
        "   - Nếu PDN dẫn -> X xả xuống 0V\n"
        "   - Nếu PDN ngắt -> X giữ điện tích (Floating High)\n"
        "HIỆN TƯỢNG CHARGE SHARING:\n"
        "   Khi PDN ngắt nhưng nút nội Cint nối với X:\n"
        "   Vx' = VDD * Cx / (Cx + Cint) -> Sụt áp!"
    )
    ax.text(5, 50, info_box, fontsize=7.8, family='monospace',
            bbox=dict(boxstyle='square,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'),
            ha='left', va='center')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

def draw_domino_logic_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10.5, 6.5), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(52.5, 96, "CELL SCHEMATIC: domino_or4_x1{sch}", fontsize=13.5, fontweight='bold', ha='center', color='#1A365D')
    ax.text(52.5, 92, "Cổng Domino OR 4-ngõ vào kèm Keeper Transistor & Inverter tĩnh", fontsize=9.5, ha='center', color='#4A5568')

    # Rails
    ax.plot([5, 100], [86, 86], color='#E53E3E', lw=2.5)
    ax.text(3, 86, "vdd", fontsize=10, fontweight='bold', color='#E53E3E', va='center', ha='right')
    ax.plot([5, 100], [12, 12], color='#2B6CB0', lw=2.5)
    ax.text(3, 12, "gnd", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # Precharge PMOS
    r_pre = patches.Rectangle((30, 72), 16, 9, facecolor='#FED7D7', edgecolor='#C53030', lw=1.2)
    ax.add_patch(r_pre)
    ax.text(38, 77.5, "M_pre (PMOS)\nW=12λ, L=2λ", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#9B2C2C')
    ax.plot([38, 38], [81, 86], color='#C53030', lw=1.5)
    ax.plot([30, 24], [76.5, 76.5], color='#4A5568', lw=1.2)
    ax.plot([24], [76.5], marker='s', markersize=6, color='#4A5568')
    ax.text(22, 76.5, "clk", fontsize=8.5, fontweight='bold', color='#4A5568', va='center', ha='right')

    # Weak Keeper PMOS (Parallel with M_pre)
    r_kp = patches.Rectangle((54, 72), 16, 9, facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.2)
    ax.add_patch(r_kp)
    ax.text(62, 77.5, "M_kp (Weak)\nW=2λ, L=2λ", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#B7791F')
    ax.plot([62, 62], [81, 86], color='#C53030', lw=1.5)

    # Dynamic Node X
    ax.plot([38, 38], [72, 58], color='#2B6CB0', lw=2)
    ax.plot([62, 62], [72, 58], color='#2B6CB0', lw=2)
    ax.plot([38, 62], [58, 58], color='#2B6CB0', lw=2)
    ax.plot([50], [58], marker='o', markersize=5, color='#2B6CB0')
    ax.text(50, 61, "Nút động X", fontsize=9, fontweight='bold', color='#2B6CB0', ha='center')

    # Static Inverter (Transforms Dynamic to Monotonic Domino Signal)
    ax.plot([50, 75], [58, 58], color='#2B6CB0', lw=2)
    tri_inv = patches.Polygon([[75, 51], [75, 65], [83, 58]], facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.5)
    ax.add_patch(tri_inv)
    bub_inv = patches.Circle((84.5, 58), 1.5, facecolor='white', edgecolor='#4A5568', lw=1.5)
    ax.add_patch(bub_inv)
    ax.text(78, 58, "INV", fontsize=8, fontweight='bold', ha='center', va='center', color='#2D3748')

    # Output Y
    ax.plot([86, 98], [58, 58], color='#2B6CB0', lw=2)
    ax.plot([98], [58], marker='s', markersize=8, color='#2B6CB0')
    ax.text(100, 58, "y", fontsize=11, fontweight='bold', color='#2B6CB0', va='center')

    # Keeper Feedback: from Out (Y) back to Keeper Gate
    ax.plot([90, 90], [58, 76.5], color='#D69E2E', lw=1.2, ls='--')
    ax.plot([90, 70], [76.5, 76.5], color='#D69E2E', lw=1.2, ls='--')
    ax.text(82, 79, "Phản hồi Keeper", fontsize=7.5, color='#B7791F', style='italic')

    # PDN: 4 NMOS in Parallel (OR4)
    # A, B, C, D
    r_pdn = patches.FancyBboxPatch((28, 30), 44, 22, boxstyle="round,pad=0.5", facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(r_pdn)
    ax.text(50, 44, "MẠNG PDN: 4 NMOS SONG SONG (OR4)", fontsize=9, fontweight='bold', ha='center', color='#2B6CB0')
    ax.text(50, 36, "A // B // C // D (Mỗi NMOS: W=4λ, L=2λ)", fontsize=8, ha='center', color='#2C5282')
    ax.plot([50, 50], [58, 52], color='#2B6CB0', lw=2)

    # Evaluate Foot NMOS
    r_foot = patches.Rectangle((42, 16), 16, 9, facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.2)
    ax.add_patch(r_foot)
    ax.text(50, 20.5, "M_eval (Foot)\nW=8λ, L=2λ", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#4A5568')
    ax.plot([50, 50], [30, 25], color='#2B6CB0', lw=1.5)
    ax.plot([50, 50], [16, 12], color='#2B6CB0', lw=2)
    ax.plot([42, 36], [20.5, 20.5], color='#4A5568', lw=1.2)
    ax.plot([36], [20.5], marker='s', markersize=6, color='#4A5568')
    ax.text(34, 20.5, "clk", fontsize=8.5, fontweight='bold', color='#4A5568', va='center', ha='right')

    # Footnote
    ax.text(52.5, 4, "VAI TRÒ KEEPER: Bù dòng rò dưới ngưỡng & ngăn tụt áp do chia sẻ điện tích mà không làm chậm sườn xả",
            fontsize=8, family='monospace', ha='center', color='#2D3748')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_dynamic_cmos_schematic("02 - Student Workbook/images/dynamic_cmos_schematic.png")
    draw_domino_logic_schematic("02 - Student Workbook/images/domino_logic_schematic.png")
