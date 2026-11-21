import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_dlatch_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, "CELL SCHEMATIC: dlatch_x1{sch}", fontsize=14, fontweight='bold', ha='center', color='#1A365D')
    ax.text(50, 91, "Mạch chốt D dùng Cổng truyền (TG-based D-Latch) | Tích cực mức cao (CLK = 1)", fontsize=10, ha='center', color='#4A5568')

    # Input D
    ax.plot([8, 22], [60, 60], color='#2B6CB0', lw=2)
    ax.plot([8], [60], marker='s', markersize=8, color='#2B6CB0')
    ax.text(6, 60, "d", fontsize=11, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # TG1: Input Transmission Gate (Passes D when CLK=1)
    rect_tg1 = patches.FancyBboxPatch((22, 50), 16, 20, boxstyle="round,pad=0.5", facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(rect_tg1)
    ax.text(30, 62, "TG1 (Input)", fontsize=9.5, fontweight='bold', ha='center', color='#2B6CB0')
    ax.text(30, 54, "ON: CLK=1", fontsize=8.5, ha='center', color='#2C5282')

    # Node X (storage node)
    ax.plot([38, 50], [60, 60], color='#2B6CB0', lw=2)
    ax.plot([46], [60], marker='o', markersize=5, color='#2B6CB0')
    ax.text(46, 64, "Node X", fontsize=8.5, ha='center', color='#2B6CB0', style='italic')

    # INV1 (Forward Inverter: creates Q_n)
    tri1 = patches.Polygon([[50, 52], [50, 68], [60, 60]], facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.5)
    ax.add_patch(tri1)
    bub1 = patches.Circle((61.5, 60), 1.5, facecolor='white', edgecolor='#4A5568', lw=1.5)
    ax.add_patch(bub1)
    ax.text(54, 60, "I1", fontsize=9, fontweight='bold', ha='center', va='center', color='#2D3748')

    # Line from INV1 out to Node Q_n
    ax.plot([63, 76], [60, 60], color='#2B6CB0', lw=2)
    ax.plot([70], [60], marker='o', markersize=5, color='#2B6CB0')
    ax.text(70, 64, "q_n", fontsize=9, fontweight='bold', ha='center', color='#4A5568')

    # INV2 (Output Inverter: creates Q)
    tri2 = patches.Polygon([[76, 52], [76, 68], [86, 60]], facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.5)
    ax.add_patch(tri2)
    bub2 = patches.Circle((87.5, 60), 1.5, facecolor='white', edgecolor='#4A5568', lw=1.5)
    ax.add_patch(bub2)
    ax.text(80, 60, "I2", fontsize=9, fontweight='bold', ha='center', va='center', color='#2D3748')

    # Output Q
    ax.plot([89, 96], [60, 60], color='#2B6CB0', lw=2)
    ax.plot([96], [60], marker='s', markersize=8, color='#2B6CB0')
    ax.text(98, 60, "q", fontsize=11, fontweight='bold', color='#2B6CB0', va='center')

    # Feedback Path: from Node Q_n down through INV3 and TG2 back to Node X
    # Down from Q_n (x=70)
    ax.plot([70, 70], [60, 28], color='#C53030', lw=1.5)
    ax.plot([70, 62], [28, 28], color='#C53030', lw=1.5)

    # INV3 (Feedback Inverter - pointing left)
    tri3 = patches.Polygon([[62, 34], [62, 22], [52, 28]], facecolor='#FED7D7', edgecolor='#C53030', lw=1.5)
    ax.add_patch(tri3)
    bub3 = patches.Circle((50.5, 28), 1.5, facecolor='white', edgecolor='#C53030', lw=1.5)
    ax.add_patch(bub3)
    ax.text(58, 28, "I3 (Weak)", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#9B2C2C')

    # Connect INV3 out to TG2
    ax.plot([49, 38], [28, 28], color='#C53030', lw=1.5)

    # TG2: Feedback Transmission Gate (Closes loop when CLK=0)
    rect_tg2 = patches.FancyBboxPatch((22, 18), 16, 20, boxstyle="round,pad=0.5", facecolor='#FED7D7', edgecolor='#C53030', lw=1.5)
    ax.add_patch(rect_tg2)
    ax.text(30, 30, "TG2 (Feedback)", fontsize=8.5, fontweight='bold', ha='center', color='#9B2C2C')
    ax.text(30, 22, "ON: CLK=0", fontsize=8, ha='center', color='#742A2A')

    # Line from TG2 left up back to Node X (x=46)
    ax.plot([22, 14], [28, 28], color='#C53030', lw=1.5)
    ax.plot([14, 14], [42, 42], color='#C53030', lw=1.5)
    ax.plot([14, 46], [42, 42], color='#C53030', lw=1.5)
    ax.plot([46, 46], [42, 60], color='#C53030', lw=1.5)

    # Clock inputs box
    clk_box = (
        "ĐIỀU KHIỂN XUNG NHỊP (CLOCK):\n"
        "• CLK = 1 (clk=5V, clk_n=0V):\n"
        "  - TG1 DẪN (ON), TG2 NGẮT (OFF)\n"
        "  => Trạng thái TRONG SUỐT (Transparent): Q bám theo D\n"
        "• CLK = 0 (clk=0V, clk_n=5V):\n"
        "  - TG1 NGẮT (OFF), TG2 DẪN (ON)\n"
        "  => Trạng thái CHỐT GIỮ (Opaque / Hold): Khóa vòng I1-I3"
    )
    ax.text(50, 8, clk_box, fontsize=8.5, family='monospace',
            bbox=dict(boxstyle='square,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'),
            ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

def draw_dff_ms_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, "CELL SCHEMATIC: dff_ms_x1{sch}", fontsize=14, fontweight='bold', ha='center', color='#1A365D')
    ax.text(50, 91, "D-Flip-Flop Master-Slave kích hoạt sườn dương (Positive Edge-Triggered DFF)", fontsize=10, ha='center', color='#4A5568')

    # Master Stage Box (Left)
    rect_m = patches.FancyBboxPatch((8, 30), 38, 48, boxstyle="round,pad=1.0", facecolor='#F7FAFC', edgecolor='#2B6CB0', lw=1.8, ls='--')
    ax.add_patch(rect_m)
    ax.text(27, 74, "MASTER LATCH", fontsize=11, fontweight='bold', ha='center', color='#2B6CB0')
    ax.text(27, 70, "(Tích cực mức thấp: CLK = 0)", fontsize=8.5, ha='center', color='#4A5568')

    # Slave Stage Box (Right)
    rect_s = patches.FancyBboxPatch((54, 30), 38, 48, boxstyle="round,pad=1.0", facecolor='#F7FAFC', edgecolor='#C53030', lw=1.8, ls='--')
    ax.add_patch(rect_s)
    ax.text(73, 74, "SLAVE LATCH", fontsize=11, fontweight='bold', ha='center', color='#C53030')
    ax.text(73, 70, "(Tích cực mức cao: CLK = 1)", fontsize=8.5, ha='center', color='#4A5568')

    # Master elements
    # D input
    ax.plot([2, 13], [52, 52], color='#2B6CB0', lw=2)
    ax.plot([2], [52], marker='s', markersize=8, color='#2B6CB0')
    ax.text(1, 52, "d", fontsize=11, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # TG_M1
    r_tg_m1 = patches.Rectangle((13, 44), 9, 16, facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.2)
    ax.add_patch(r_tg_m1)
    ax.text(17.5, 52, "TG1\n(CLK=0)", fontsize=7, fontweight='bold', ha='center', va='center')

    # Inv M1
    ax.plot([22, 27], [52, 52], color='#2B6CB0', lw=1.5)
    tri_m1 = patches.Polygon([[27, 46], [27, 58], [33, 52]], facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.2)
    ax.add_patch(tri_m1)
    bub_m1 = patches.Circle((34, 52), 1.0, facecolor='white', edgecolor='#4A5568', lw=1.2)
    ax.add_patch(bub_m1)

    # Master node QM
    ax.plot([35, 41], [52, 52], color='#2B6CB0', lw=1.5)
    ax.plot([38], [52], marker='o', markersize=4, color='#2B6CB0')
    ax.text(38, 56, "qm", fontsize=8, fontweight='bold', ha='center', color='#2B6CB0')

    # Master Feedback (TG_M2 + Inv M2)
    ax.plot([38, 38], [52, 38], color='#2B6CB0', lw=1.2)
    ax.plot([38, 33], [38, 38], color='#2B6CB0', lw=1.2)
    tri_m2 = patches.Polygon([[33, 42], [33, 34], [27, 38]], facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.0)
    ax.add_patch(tri_m2)
    bub_m2 = patches.Circle((26, 38), 1.0, facecolor='white', edgecolor='#4A5568', lw=1.0)
    ax.add_patch(bub_m2)
    ax.plot([25, 22], [38, 38], color='#2B6CB0', lw=1.2)
    r_tg_m2 = patches.Rectangle((13, 33), 9, 10, facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.0)
    ax.add_patch(r_tg_m2)
    ax.text(17.5, 38, "TG2\n(CLK=1)", fontsize=6.5, fontweight='bold', ha='center', va='center')
    ax.plot([13, 10], [38, 38], color='#2B6CB0', lw=1.2)
    ax.plot([10, 10], [38, 48], color='#2B6CB0', lw=1.2)
    ax.plot([10, 24], [48, 48], color='#2B6CB0', lw=1.2)
    ax.plot([24, 24], [48, 52], color='#2B6CB0', lw=1.2)

    # Connect Master to Slave
    ax.plot([41, 59], [52, 52], color='#4A5568', lw=2)

    # Slave elements
    # TG_S1
    r_tg_s1 = patches.Rectangle((59, 44), 9, 16, facecolor='#FED7D7', edgecolor='#C53030', lw=1.2)
    ax.add_patch(r_tg_s1)
    ax.text(63.5, 52, "TG3\n(CLK=1)", fontsize=7, fontweight='bold', ha='center', va='center')

    # Inv S1
    ax.plot([68, 73], [52, 52], color='#C53030', lw=1.5)
    tri_s1 = patches.Polygon([[73, 46], [73, 58], [79, 52]], facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.2)
    ax.add_patch(tri_s1)
    bub_s1 = patches.Circle((80, 52), 1.0, facecolor='white', edgecolor='#4A5568', lw=1.2)
    ax.add_patch(bub_s1)

    # Output Q
    ax.plot([81, 96], [52, 52], color='#C53030', lw=2)
    ax.plot([96], [52], marker='s', markersize=8, color='#C53030')
    ax.text(98, 52, "q", fontsize=11, fontweight='bold', color='#C53030', va='center')

    # Slave Feedback
    ax.plot([84], [52], marker='o', markersize=4, color='#C53030')
    ax.plot([84, 84], [52, 38], color='#C53030', lw=1.2)
    ax.plot([84, 79], [38, 38], color='#C53030', lw=1.2)
    tri_s2 = patches.Polygon([[79, 42], [79, 34], [73, 38]], facecolor='#E2E8F0', edgecolor='#4A5568', lw=1.0)
    ax.add_patch(tri_s2)
    bub_s2 = patches.Circle((72, 38), 1.0, facecolor='white', edgecolor='#4A5568', lw=1.0)
    ax.add_patch(bub_s2)
    ax.plot([71, 68], [38, 38], color='#C53030', lw=1.2)
    r_tg_s2 = patches.Rectangle((59, 33), 9, 10, facecolor='#FED7D7', edgecolor='#C53030', lw=1.0)
    ax.add_patch(r_tg_s2)
    ax.text(63.5, 38, "TG4\n(CLK=0)", fontsize=6.5, fontweight='bold', ha='center', va='center')
    ax.plot([59, 56], [38, 38], color='#C53030', lw=1.2)
    ax.plot([56, 56], [38, 48], color='#C53030', lw=1.2)
    ax.plot([56, 70], [48, 48], color='#C53030', lw=1.2)
    ax.plot([70, 70], [48, 52], color='#C53030', lw=1.2)

    # Timing explanation box at bottom
    timing_box = (
        "QUY TẮC HOẠT ĐỘNG KÍCH HOẠT SƯỜN DƯƠNG (POSITIVE EDGE):\n"
        "• Khi CLK = 0: Master mở (TG1 ON, TG2 OFF: QM bắt D), Slave đóng (TG3 OFF, TG4 ON: Q giữ nguyên).\n"
        "• Khi CLK nhảy 0 -> 1 (Sườn lên): Master đóng (TG1 OFF, TG2 ON: chốt D), Slave mở (TG3 ON, TG4 OFF: truyền QM ra Q).\n"
        "  => Dữ liệu chỉ được cập nhật ra ngõ Q duy nhất tại thời điểm sườn xung nhịp tăng!\n"
        "• CÁC THÔNG SỐ ĐỊNH THỜI TỚI HẠN: t_setup (thời gian lập), t_hold (thời gian giữ), t_c-q (trễ xung-ngõ ra)."
    )
    ax.text(50, 6, timing_box, fontsize=8.2, family='monospace',
            bbox=dict(boxstyle='square,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'),
            ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_dlatch_schematic("02 - Giao_Trinh_Lab_Handouts/images/dlatch_schematic.png")
    draw_dff_ms_schematic("02 - Giao_Trinh_Lab_Handouts/images/dff_ms_schematic.png")
