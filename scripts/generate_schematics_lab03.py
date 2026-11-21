import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_aoi21_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 96, "CELL SCHEMATIC: aoi21_x1{sch}", fontsize=14, fontweight='bold', ha='center', color='#1A365D')
    ax.text(50, 92, r"$Y = \overline{(A \cdot B) + C}$ | MOSIS SCMOS C5N 0.5$\mu$m", fontsize=11, ha='center', color='#4A5568')

    # Rails
    # VDD
    ax.plot([15, 85], [86, 86], color='#E53E3E', lw=3)
    ax.text(12, 86, "vdd", fontsize=11, fontweight='bold', color='#E53E3E', va='center', ha='right')
    ax.plot([15], [86], marker='s', markersize=8, color='#E53E3E') # Port export

    # GND
    ax.plot([15, 85], [10, 10], color='#2B6CB0', lw=3)
    ax.text(12, 10, "gnd", fontsize=11, fontweight='bold', color='#2B6CB0', va='center', ha='right')
    ax.plot([15], [10], marker='s', markersize=8, color='#2B6CB0') # Port export

    # Draw Boxes for Transistors
    def draw_mos(x, y, w, h, name, size, m_type, gate_text, gate_side='left'):
        box_color = '#FED7D7' if m_type == 'P' else '#BEE3F8'
        edge_color = '#C53030' if m_type == 'P' else '#2B6CB0'
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.5",
                                      facecolor=box_color, edgecolor=edge_color, lw=1.5)
        ax.add_patch(rect)
        ax.text(x, y + 1.2, name, fontsize=9.5, fontweight='bold', ha='center', color=edge_color)
        ax.text(x, y - 2.2, size, fontsize=8, ha='center', color='#2D3748')
        
        # Gate line
        if gate_side == 'left':
            ax.plot([x - w/2, x - w/2 - 6], [y, y], color='#4A5568', lw=1.5)
            if gate_text:
                ax.text(x - w/2 - 7, y, gate_text, fontsize=9.5, fontweight='bold', ha='right', va='center', color='#2B6CB0')
        elif gate_side == 'right':
            ax.plot([x + w/2, x + w/2 + 6], [y, y], color='#4A5568', lw=1.5)
            if gate_text:
                ax.text(x + w/2 + 7, y, gate_text, fontsize=9.5, fontweight='bold', ha='left', va='center', color='#2B6CB0')

    # PMOS PUN Network: (A // B) series with C
    # MP_A and MP_B in parallel
    draw_mos(36, 75, 16, 7, "MP_A (PMOS)", r"W=24$\lambda$ (7.2$\mu$m)", 'P', "A", 'left')
    draw_mos(64, 75, 16, 7, "MP_B (PMOS)", r"W=24$\lambda$ (7.2$\mu$m)", 'P', "B", 'right')

    # Connections to VDD
    ax.plot([36, 36], [78.5, 86], color='#C53030', lw=1.5)
    ax.plot([64, 64], [78.5, 86], color='#C53030', lw=1.5)
    ax.plot([36, 64], [86, 86], marker='o', markersize=4, color='#C53030')

    # Merge below MP_A and MP_B -> Node Xp
    ax.plot([36, 36], [71.5, 66], color='#C53030', lw=1.5)
    ax.plot([64, 64], [71.5, 66], color='#C53030', lw=1.5)
    ax.plot([36, 64], [66, 66], color='#C53030', lw=1.5)
    ax.plot([50, 50], [66, 61.5], color='#C53030', lw=1.5)
    ax.plot([50], [66], marker='o', markersize=4, color='#C53030')
    ax.text(53, 66, "Node Xp", fontsize=8, color='#742A2A', style='italic')

    # MP_C in series below (A // B)
    draw_mos(50, 58, 18, 7, "MP_C (PMOS)", r"W=24$\lambda$ (7.2$\mu$m)", 'P', "C", 'left')
    
    # Line from MP_C to Output Out
    ax.plot([50, 50], [54.5, 48], color='#C53030', lw=1.5)
    ax.plot([50], [48], marker='o', markersize=5, color='#2D3748')
    ax.plot([50, 80], [48, 48], color='#2D3748', lw=2)
    ax.plot([80], [48], marker='s', markersize=9, color='#2B6CB0')
    ax.text(83, 48, "out", fontsize=11, fontweight='bold', color='#2B6CB0', va='center')

    # NMOS PDN Network: (MN_A series MN_B) parallel with MN_C
    # Branch 1: MN_A series MN_B
    draw_mos(36, 35, 16, 7, "MN_A (NMOS)", r"W=8$\lambda$ (2.4$\mu$m)", 'N', "A", 'left')
    draw_mos(36, 21, 16, 7, "MN_B (NMOS)", r"W=8$\lambda$ (2.4$\mu$m)", 'N', "B", 'left')

    # Connection from out to MN_A
    ax.plot([50, 36], [48, 48], color='#2B6CB0', lw=1.5)
    ax.plot([36, 36], [48, 38.5], color='#2B6CB0', lw=1.5)

    # Series connection MN_A to MN_B (Node Xn)
    ax.plot([36, 36], [31.5, 24.5], color='#2B6CB0', lw=1.5)
    ax.plot([36], [28], marker='o', markersize=4, color='#2B6CB0')
    ax.text(39, 28, "Node Xn", fontsize=8, color='#2A4365', style='italic')

    # Bottom of MN_B to GND
    ax.plot([36, 36], [17.5, 10], color='#2B6CB0', lw=1.5)
    ax.plot([36], [10], marker='o', markersize=4, color='#2B6CB0')

    # Branch 2: MN_C in parallel
    draw_mos(64, 28, 16, 7, "MN_C (NMOS)", r"W=4$\lambda$ (1.2$\mu$m)", 'N', "C", 'right')

    # Top of MN_C to out
    ax.plot([50, 64], [48, 48], color='#2B6CB0', lw=1.5)
    ax.plot([64, 64], [48, 31.5], color='#2B6CB0', lw=1.5)

    # Bottom of MN_C to GND
    ax.plot([64, 64], [24.5, 10], color='#2B6CB0', lw=1.5)
    ax.plot([64], [10], marker='o', markersize=4, color='#2B6CB0')

    # Highlight Export Pins
    ax.plot([21], [75], marker='s', markersize=8, color='#2B6CB0') # A
    ax.plot([79], [75], marker='s', markersize=8, color='#2B6CB0') # B
    ax.plot([33], [58], marker='s', markersize=8, color='#2B6CB0') # C

    # Summary box
    info_text = (
        "CẤU HÌNH EXPORT PORTS (6 CHÂN):\n"
        "• A, B, C: Ngõ vào logic (Input)\n"
        "• out: Ngõ ra hàm Y = !((A*B) + C) (Output)\n"
        "• vdd: Nguồn cấp 5.0V (Power)\n"
        "• gnd: Đất chuẩn 0V (Ground)\n"
        "QUY TẮC ĐỊNH CỠ TƯƠNG ĐƯƠNG INV_X1:\n"
        "• Nhánh nối tiếp 2 PMOS: Wp = 24λ = 7.2µm\n"
        "• Nhánh nối tiếp 2 NMOS: Wn = 8λ = 2.4µm\n"
        "• Nhánh 1 NMOS đơn (C): Wn = 4λ = 1.2µm"
    )
    ax.text(88, 25, info_text, fontsize=8, family='monospace', bbox=dict(boxstyle='square,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'), va='center', ha='left')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

def draw_buffer_chain_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    ax.text(50, 46, "TỐI ƯU HÓA CHUỖI ĐỆM INVERTER THEO LOGICAL EFFORT", fontsize=13, fontweight='bold', ha='center', color='#1A365D')
    ax.text(50, 42, r"Lái tải nặng $C_L = 1\,\mathrm{pF} = 50 \times C_{in}$ ($H=50$, $N=3$ tầng, $\hat{f} = \sqrt[3]{50} \approx 3.68$)", fontsize=10, ha='center', color='#4A5568')

    # Draw Inverters as triangles
    def draw_inv(x, y, scale, label, size_text, cin_text):
        # Triangle
        h_tri = 12 * scale
        w_tri = 10 * scale
        triangle = patches.Polygon([[x - w_tri/2, y - h_tri/2], [x - w_tri/2, y + h_tri/2], [x + w_tri/2, y]],
                                   facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=1.5)
        ax.add_patch(triangle)
        # Bubble
        r_bub = 1.2 * scale
        bubble = patches.Circle((x + w_tri/2 + r_bub, y), r_bub, facecolor='white', edgecolor='#2B6CB0', lw=1.5)
        ax.add_patch(bubble)
        # Text
        ax.text(x - 1, y - h_tri/2 - 3, label, fontsize=9, fontweight='bold', ha='center', color='#2B6CB0')
        ax.text(x - 1, y - h_tri/2 - 6, size_text, fontsize=8, ha='center', color='#2D3748')
        ax.text(x - 1, y + h_tri/2 + 2, cin_text, fontsize=8, ha='center', color='#718096')
        return x + w_tri/2 + 2 * r_bub

    # Input line
    ax.plot([5, 15], [25, 25], color='#2B6CB0', lw=2)
    ax.plot([5], [25], marker='s', markersize=8, color='#2B6CB0')
    ax.text(3, 25, "in", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # Stage 1: 1X
    p1 = draw_inv(22, 25, 1.0, "Tầng 1 (1X)", "Wn=4λ, Wp=12λ", "Cin = 20fF")

    # Connect stage 1 to 2
    ax.plot([p1, 40], [25, 25], color='#2B6CB0', lw=2)

    # Stage 2: 3.7X
    p2 = draw_inv(48, 25, 1.25, "Tầng 2 (3.7X)", "Wn=15λ, Wp=44λ", "Cin ≈ 74fF")

    # Connect stage 2 to 3
    ax.plot([p2, 68], [25, 25], color='#2B6CB0', lw=2)

    # Stage 3: 13.6X
    p3 = draw_inv(78, 25, 1.55, "Tầng 3 (13.6X)", "Wn=54λ, Wp=163λ", "Cin ≈ 272fF")

    # Output line and Load Capacitor
    ax.plot([p3, 93], [25, 25], color='#2B6CB0', lw=2)
    ax.plot([93], [25], marker='s', markersize=8, color='#2B6CB0')
    ax.text(95, 25, "out", fontsize=10, fontweight='bold', color='#2B6CB0', va='center')

    # Capacitor CL
    ax.plot([90, 90], [25, 18], color='#4A5568', lw=1.5)
    ax.plot([87, 93], [18, 18], color='#4A5568', lw=2)
    ax.plot([87, 93], [16, 16], color='#4A5568', lw=2)
    ax.plot([90, 90], [16, 12], color='#4A5568', lw=1.5)
    ax.plot([88, 92], [12, 12], color='#4A5568', lw=1.5) # GND
    ax.text(93, 17, r" $C_L = 1\,\mathrm{pF}$", fontsize=9, fontweight='bold', color='#E53E3E', va='center')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_aoi21_schematic("02 - Giao_Trinh_Lab_Handouts/images/aoi21_schematic.png")
    draw_buffer_chain_schematic("02 - Giao_Trinh_Lab_Handouts/images/buffer_chain_schematic.png")
