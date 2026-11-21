import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_tg_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, "CELL SCHEMATIC: tg_gate{sch}", fontsize=14, fontweight='bold', ha='center', color='#1A365D')
    ax.text(50, 91, "Cổng truyền CMOS Transmission Gate (TG) | MOSIS SCMOS C5N 0.5µm", fontsize=10, ha='center', color='#4A5568')

    # Input / Output lines
    ax.plot([15, 35], [50, 50], color='#2B6CB0', lw=2.5)
    ax.plot([15], [50], marker='s', markersize=9, color='#2B6CB0')
    ax.text(12, 50, "in", fontsize=11, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    ax.plot([65, 85], [50, 50], color='#2B6CB0', lw=2.5)
    ax.plot([85], [50], marker='s', markersize=9, color='#2B6CB0')
    ax.text(88, 50, "out", fontsize=11, fontweight='bold', color='#2B6CB0', va='center', ha='left')

    # Branches to PMOS (top) and NMOS (bottom)
    ax.plot([35, 35], [28, 72], color='#2B6CB0', lw=2)
    ax.plot([65, 65], [28, 72], color='#2B6CB0', lw=2)
    ax.plot([35, 42], [72, 72], color='#C53030', lw=2)
    ax.plot([58, 65], [72, 72], color='#C53030', lw=2)
    ax.plot([35, 42], [28, 28], color='#2B6CB0', lw=2)
    ax.plot([58, 65], [28, 28], color='#2B6CB0', lw=2)

    # PMOS box (top)
    rect_p = patches.FancyBboxPatch((42, 65), 16, 14, boxstyle="round,pad=0.5", facecolor='#FED7D7', edgecolor='#C53030', lw=1.5)
    ax.add_patch(rect_p)
    ax.text(50, 74, "MP (PMOS)", fontsize=10, fontweight='bold', ha='center', color='#C53030')
    ax.text(50, 68, r"W=12$\lambda$ (3.6$\mu$m), L=2$\lambda$", fontsize=8, ha='center', color='#2D3748')

    # PMOS Gate (EN_n)
    ax.plot([50, 50], [79, 87], color='#C53030', lw=1.5)
    ax.plot([50], [87], marker='s', markersize=8, color='#C53030')
    ax.text(50, 90, "en_n (ENB)", fontsize=9.5, fontweight='bold', color='#C53030', ha='center')

    # PMOS Bulk (VDD)
    ax.plot([58, 68], [75, 75], color='#E53E3E', lw=1.2, ls='--')
    ax.text(70, 75, "Bulk -> vdd", fontsize=8, color='#E53E3E', va='center')

    # NMOS box (bottom)
    rect_n = patches.FancyBboxPatch((42, 21), 16, 14, boxstyle="round,pad=0.5", facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(rect_n)
    ax.text(50, 30, "MN (NMOS)", fontsize=10, fontweight='bold', ha='center', color='#2B6CB0')
    ax.text(50, 24, r"W=4$\lambda$ (1.2$\mu$m), L=2$\lambda$", fontsize=8, ha='center', color='#2D3748')

    # NMOS Gate (EN)
    ax.plot([50, 50], [21, 13], color='#2B6CB0', lw=1.5)
    ax.plot([50], [13], marker='s', markersize=8, color='#2B6CB0')
    ax.text(50, 10, "en (EN)", fontsize=9.5, fontweight='bold', color='#2B6CB0', ha='center')

    # NMOS Bulk (GND)
    ax.plot([58, 68], [25, 25], color='#2B6CB0', lw=1.2, ls='--')
    ax.text(70, 25, "Bulk -> gnd", fontsize=8, color='#2B6CB0', va='center')

    # Function box
    func_text = (
        "NGUYÊN LÝ HOẠT ĐỘNG CỔNG TRUYỀN (TG):\n"
        "• EN = 1 (en=5V, en_n=0V): Cổng DẪN (ON)\n"
        "  - NMOS truyền Strong '0' (0V -> VDD - Vthn)\n"
        "  - PMOS truyền Strong '1' (|Vthp| -> VDD)\n"
        "  => Toàn dải Rail-to-Rail: 0V đến 5.0V\n"
        "• EN = 0 (en=0V, en_n=5V): Cổng NGẮT (OFF)\n"
        "  => Ngõ ra out ở trạng thái trở kháng cao (Hi-Z)"
    )
    ax.text(50, 48, func_text, fontsize=8.5, family='monospace',
            bbox=dict(boxstyle='square,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'),
            ha='center', va='top')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

def draw_mux2_tg_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, "CELL SCHEMATIC: mux2_tg{sch}", fontsize=14, fontweight='bold', ha='center', color='#1A365D')
    ax.text(50, 91, "Bộ dồn kênh 2:1 dùng Cổng truyền (TG-based MUX 2:1) | 6 Transistors", fontsize=10, ha='center', color='#4A5568')

    # Input D0
    ax.plot([10, 30], [70, 70], color='#2B6CB0', lw=2)
    ax.plot([10], [70], marker='s', markersize=8, color='#2B6CB0')
    ax.text(8, 70, "d0", fontsize=10.5, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # Input D1
    ax.plot([10, 30], [30, 30], color='#2B6CB0', lw=2)
    ax.plot([10], [30], marker='s', markersize=8, color='#2B6CB0')
    ax.text(8, 30, "d1", fontsize=10.5, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # TG0 Box (top)
    rect_tg0 = patches.FancyBboxPatch((30, 60), 22, 20, boxstyle="round,pad=0.5", facecolor='#EDF2F7', edgecolor='#4A5568', lw=1.5)
    ax.add_patch(rect_tg0)
    ax.text(41, 73, "TG0 (D0 Gate)", fontsize=9.5, fontweight='bold', ha='center', color='#2D3748')
    ax.text(41, 65, "ON khi S = 0", fontsize=8.5, ha='center', color='#718096')

    # TG1 Box (bottom)
    rect_tg1 = patches.FancyBboxPatch((30, 20), 22, 20, boxstyle="round,pad=0.5", facecolor='#EDF2F7', edgecolor='#4A5568', lw=1.5)
    ax.add_patch(rect_tg1)
    ax.text(41, 33, "TG1 (D1 Gate)", fontsize=9.5, fontweight='bold', ha='center', color='#2D3748')
    ax.text(41, 25, "ON khi S = 1", fontsize=8.5, ha='center', color='#718096')

    # Output merge
    ax.plot([52, 68], [70, 70], color='#2B6CB0', lw=2)
    ax.plot([52, 68], [30, 30], color='#2B6CB0', lw=2)
    ax.plot([68, 68], [30, 70], color='#2B6CB0', lw=2)
    ax.plot([68, 85], [50, 50], color='#2B6CB0', lw=2.5)
    ax.plot([85], [50], marker='s', markersize=9, color='#2B6CB0')
    ax.text(88, 50, "y (out)", fontsize=11, fontweight='bold', color='#2B6CB0', va='center')

    # Select input S and Inverter for S_n
    ax.plot([15, 15], [10, 50], color='#DD6B20', lw=2)
    ax.plot([15], [10], marker='s', markersize=8, color='#DD6B20')
    ax.text(12, 10, "s (Select)", fontsize=10, fontweight='bold', color='#DD6B20', va='center', ha='right')

    # Inverter symbol at x=20, y=48
    tri = patches.Polygon([[18, 43], [18, 57], [25, 50]], facecolor='#FEEBC8', edgecolor='#DD6B20', lw=1.2)
    ax.add_patch(tri)
    bub = patches.Circle((26, 50), 1.0, facecolor='white', edgecolor='#DD6B20', lw=1.2)
    ax.add_patch(bub)
    ax.text(21, 59, "INV", fontsize=7.5, color='#DD6B20', ha='center')

    # Line from S to inverter input
    ax.plot([15, 18], [50, 50], color='#DD6B20', lw=1.5)
    # Output of inverter: S_n
    ax.plot([27, 29], [50, 50], color='#DD6B20', lw=1.5)
    ax.text(28, 46, "s_n", fontsize=8, color='#C05621')

    # Wiring S and S_n to TG0 and TG1
    # For TG0: NMOS gate gets S_n, PMOS gate gets S
    # For TG1: NMOS gate gets S, PMOS gate gets S_n
    ax.plot([15, 33], [10, 10], color='#DD6B20', lw=1.2)
    ax.plot([33, 33], [10, 20], color='#DD6B20', lw=1.2) # S to TG1 NMOS
    ax.text(33, 18, "S (NMOS)", fontsize=7.5, color='#DD6B20', ha='center')

    ax.plot([29, 33], [50, 50], color='#C05621', lw=1.2)
    ax.plot([33, 33], [50, 60], color='#C05621', lw=1.2) # S_n to TG0 NMOS
    ax.text(33, 58, "S_n (NMOS)", fontsize=7.5, color='#C05621', ha='center')

    # Summary Table Box
    info_table = (
        "BẢNG CHÂN TRỊ MUX 2:1:\n"
        "┌───┬────────┬────────┬───────┐\n"
        "│ S │  TG0   │  TG1   │   Y   │\n"
        "├───┼────────┼────────┼───────┤\n"
        "│ 0 │   ON   │  OFF   │  D0   │\n"
        "│ 1 │  OFF   │   ON   │  D1   │\n"
        "└───┴────────┴────────┴───────┘\n"
        "ƯU THẾ VƯỢT TRỘI:\n"
        "• Dùng 6 MOSFETs (thay vì 12T)\n"
        "• Trễ qua cổng: duy nhất 1 TG"
    )
    ax.text(70, 20, info_table, fontsize=8.5, family='monospace',
            bbox=dict(boxstyle='square,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'),
            ha='left', va='bottom')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_tg_schematic("02 - Giao_Trinh_Lab_Handouts/images/tg_schematic.png")
    draw_mux2_tg_schematic("02 - Giao_Trinh_Lab_Handouts/images/mux2_tg_schematic.png")
