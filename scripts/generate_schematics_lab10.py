import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_alu_4bit_top_architecture(out_path):
    fig, ax = plt.subplots(figsize=(11.5, 7.5), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(57.5, 96.5, "KIẾN TRÚC VI MẠCH REGISTERED ALU 4-BIT (CAPSTONE PROJECT)", fontsize=13.5, fontweight='bold', ha='center', color='#1A365D')
    ax.text(57.5, 92.5, "Hệ thống Tích hợp Toàn diện: CLA 4-bit + Khối Logic + MUX 4:1 + D-FF Register + Cờ Trạng thái", fontsize=9.2, ha='center', color='#4A5568')

    # Primary Inputs on Left
    ax.plot([5, 18], [78, 78], color='#2B6CB0', lw=2.5)
    ax.plot([5], [78], marker='s', markersize=7, color='#2B6CB0')
    ax.text(3, 78, "A[3:0]", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    ax.plot([5, 18], [62, 62], color='#2B6CB0', lw=2.5)
    ax.plot([5], [62], marker='s', markersize=7, color='#2B6CB0')
    ax.text(3, 62, "B[3:0]", fontsize=10, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    ax.plot([5, 18], [48, 48], color='#C53030', lw=2)
    ax.plot([5], [48], marker='s', markersize=6, color='#C53030')
    ax.text(3, 48, "Cin", fontsize=9.5, fontweight='bold', color='#C53030', va='center', ha='right')

    # ALU Execution Units (Column 1: x = 18 to 44)
    # 1. CLA Adder 4-bit
    r_cla = patches.FancyBboxPatch((18, 68), 26, 18, boxstyle="round,pad=0.4", facecolor='#FED7D7', edgecolor='#C53030', lw=1.5)
    ax.add_patch(r_cla)
    ax.text(31, 79, "KHỐI SỐ HỌC", fontsize=8.5, fontweight='bold', color='#9B2C2C', ha='center')
    ax.text(31, 74, "4-bit CLA Adder\n(A + B + Cin)", fontsize=7.8, ha='center', color='#742A2A')
    ax.text(31, 69.5, "OP = 00", fontsize=7.5, fontweight='bold', ha='center', color='#C53030')

    # 2. Logic Unit (AND, OR, XOR)
    r_log = patches.FancyBboxPatch((18, 16), 26, 46, boxstyle="round,pad=0.4", facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(r_log)
    ax.text(31, 56, "KHỐI LOGIC 4-BIT", fontsize=8.5, fontweight='bold', color='#1A365D', ha='center')
    ax.text(31, 48, "• 4-bit AND (OP = 01)\n  Y = A · B\n\n• 4-bit OR (OP = 10)\n  Y = A + B\n\n• 4-bit XOR (OP = 11)\n  Y = A ⊕ B",
            fontsize=7.5, color='#2C5282', ha='center')

    # Input bus routing into execution units
    ax.plot([12, 12], [48, 78], color='#2B6CB0', lw=1.5)
    ax.plot([12, 18], [74, 74], color='#2B6CB0', lw=1.5) # into CLA
    ax.plot([12, 18], [38, 38], color='#2B6CB0', lw=1.5) # into Logic

    # Data lines from Units to MUX 4:1
    # CLA out
    ax.plot([44, 56], [77, 77], color='#C53030', lw=1.8)
    ax.text(50, 79, "Sum[3:0]", fontsize=7.5, color='#C53030', ha='center')
    # AND out
    ax.plot([44, 56], [50, 50], color='#2B6CB0', lw=1.5)
    ax.text(50, 52, "AND[3:0]", fontsize=7.5, color='#2B6CB0', ha='center')
    # OR out
    ax.plot([44, 56], [38, 38], color='#2B6CB0', lw=1.5)
    ax.text(50, 40, "OR[3:0]", fontsize=7.5, color='#2B6CB0', ha='center')
    # XOR out
    ax.plot([44, 56], [26, 26], color='#2B6CB0', lw=1.5)
    ax.text(50, 28, "XOR[3:0]", fontsize=7.5, color='#2B6CB0', ha='center')

    # Cout from CLA
    ax.plot([44, 98], [71, 71], color='#C53030', lw=1.5, ls='--')
    ax.plot([98, 98], [71, 78], color='#C53030', lw=1.5, ls='--')
    ax.plot([98, 108], [78, 78], color='#C53030', lw=2)
    ax.plot([108], [78], marker='s', markersize=7, color='#C53030')
    ax.text(110, 78, "Cout", fontsize=10, fontweight='bold', color='#C53030', va='center')

    # Column 2: 4-bit 4:1 MUX (x = 56 to 72)
    r_mux = patches.Polygon([[56, 18], [56, 84], [72, 72], [72, 30]], facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.8)
    ax.add_patch(r_mux)
    ax.text(64, 51, "MUX 4:1\n4-BIT\n(TG MUX)", fontsize=8.5, fontweight='bold', ha='center', color='#744210')

    # OP[1:0] Control inputs into MUX
    ax.plot([64, 64], [88, 78], color='#D69E2E', lw=2)
    ax.plot([64], [88], marker='s', markersize=7, color='#D69E2E')
    ax.text(64, 90, "OP[1:0]", fontsize=9.5, fontweight='bold', color='#B7791F', ha='center')

    # MUX output to Register (ALU_Result[3:0])
    ax.plot([72, 80], [51, 51], color='#805AD5', lw=2.2)
    ax.text(76, 53.5, "res[3:0]", fontsize=7.5, color='#805AD5', ha='center')

    # Column 3: 4-bit Output Register DFF_REG4 (x = 80 to 98)
    r_dff = patches.FancyBboxPatch((80, 28), 18, 46, boxstyle="round,pad=0.4", facecolor='#E9D8FD', edgecolor='#6B46C1', lw=1.8)
    ax.add_patch(r_dff)
    ax.text(89, 58, "THANH GHI\nNGÕ RA 4-BIT", fontsize=8.2, fontweight='bold', color='#44337A', ha='center')
    ax.text(89, 47, "4x DFF_MS_X1\n(Master-Slave\nChốt theo CLK)", fontsize=7.2, color='#553C9A', ha='center')

    # Clock input into Register
    ax.plot([89, 89], [14, 28], color='#4A5568', lw=2)
    ax.plot([89], [14], marker='s', markersize=7, color='#4A5568')
    ax.text(89, 11, "CLK", fontsize=10, fontweight='bold', color='#2D3748', ha='center')

    # Registered Outputs on Right (OUT[3:0])
    ax.plot([98, 108], [51, 51], color='#6B46C1', lw=2.5)
    ax.plot([108], [51], marker='s', markersize=8, color='#6B46C1')
    ax.text(110, 51, "OUT[3:0]", fontsize=11, fontweight='bold', color='#6B46C1', va='center')

    # Zero Flag Generator (NOR4)
    ax.plot([102, 102], [51, 32], color='#6B46C1', lw=1.5)
    ax.plot([102, 105], [32, 32], color='#319795', lw=1.5)
    r_z = patches.FancyBboxPatch((104, 24), 6, 16, boxstyle="round,pad=0.2", facecolor='#E6FFFA', edgecolor='#319795', lw=1.2)
    ax.add_patch(r_z)
    ax.text(107, 32, "NOR4", fontsize=7.0, fontweight='bold', color='#234E52', ha='center', va='center', rotation=-90)
    ax.plot([110, 113], [32, 32], color='#319795', lw=2)
    ax.text(114, 32, "Z (Zero)", fontsize=9.5, fontweight='bold', color='#234E52', va='center')

    # Footer note
    ax.text(57.5, 4, "CHIP SPECIFICATION: 358 Transistors | f_max > 1.0 GHz | MOSIS C5N 0.5µm | Hoàn thiện cấp Hệ thống",
            fontsize=8.5, ha='center', color='#2D3748', style='italic')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")


def draw_alu_chip_layout_floorplan(out_path):
    fig, ax = plt.subplots(figsize=(10.5, 7.0), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(52.5, 96.5, "MẶT BẰNG CHIP & VÒNG CẤP NGUỒN (CHIP FLOORPLAN & POWER RING)", fontsize=13, fontweight='bold', ha='center', color='#1A365D')
    ax.text(52.5, 92.5, "Phân bố mặt bằng vật lý hoàn chỉnh với Power Ring VDD/GND kép và I/O Pad Frame", fontsize=9.0, ha='center', color='#4A5568')

    # Outer Chip Boundary (Substrate)
    r_chip = patches.Rectangle((6, 6), 93, 83, facecolor='#F7FAFC', edgecolor='#4A5568', lw=2)
    ax.add_patch(r_chip)

    # Power Ring Outer: VDD (Red line)
    r_vdd = patches.Rectangle((10, 10), 85, 75, fill=False, edgecolor='#E53E3E', lw=3.0)
    ax.add_patch(r_vdd)
    ax.text(52.5, 86, "POWER RING VDD (Metal 2/Metal 1) - 5.0V", fontsize=8.0, fontweight='bold', color='#C53030', ha='center')

    # Power Ring Inner: GND (Blue line)
    r_gnd = patches.Rectangle((13, 13), 79, 69, fill=False, edgecolor='#2B6CB0', lw=3.0)
    ax.add_patch(r_gnd)
    ax.text(52.5, 80, "GROUND RING GND (Metal 2/Metal 1) - 0.0V", fontsize=8.0, fontweight='bold', color='#2B6CB0', ha='center')

    # Core Area
    r_core = patches.Rectangle((16, 16), 73, 61, facecolor='#EDF2F7', edgecolor='#718096', lw=1.2, ls='--')
    ax.add_patch(r_core)
    ax.text(52.5, 75, "VÙNG LÕI TÍNH TOÁN (CORE AREA)", fontsize=8.5, fontweight='bold', color='#4A5568', ha='center')

    # Internal Macro Blocks
    # Block 1: CLA4 Core (Top Left)
    r_b1 = patches.Rectangle((20, 48), 30, 24, facecolor='#FED7D7', edgecolor='#C53030', lw=1.5)
    ax.add_patch(r_b1)
    ax.text(35, 62, "KHỐI CLA 4-BIT\n(134 Transistors)", fontsize=8, fontweight='bold', color='#9B2C2C', ha='center')
    ax.text(35, 53, "PG + CLG + Sum", fontsize=7.2, color='#742A2A', ha='center')

    # Block 2: Logic Units (Bottom Left)
    r_b2 = patches.Rectangle((20, 20), 30, 24, facecolor='#BEE3F8', edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(r_b2)
    ax.text(35, 34, "KHỐI LOGIC 4-BIT\n(72 Transistors)", fontsize=8, fontweight='bold', color='#1A365D', ha='center')
    ax.text(35, 25, "AND4 + OR4 + XOR4", fontsize=7.2, color='#2C5282', ha='center')

    # Block 3: MUX4 4-bit (Center Right)
    r_b3 = patches.Rectangle((54, 28), 16, 40, facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.5)
    ax.add_patch(r_b3)
    ax.text(62, 50, "MUX 4:1\n4-BIT\n(64T)", fontsize=8, fontweight='bold', color='#744210', ha='center')

    # Block 4: DFF Output Register & Flag (Far Right)
    r_b4 = patches.Rectangle((73, 22), 14, 50, facecolor='#E9D8FD', edgecolor='#6B46C1', lw=1.5)
    ax.add_patch(r_b4)
    ax.text(80, 52, "THANH GHI\nDFF 4-BIT\n(72T)\n+\nCỜ Z, COUT\n(16T)", fontsize=7.2, fontweight='bold', color='#44337A', ha='center')

    # I/O Pins annotations on Perimeter
    ax.text(2, 50, "A[3:0]\nB[3:0]\nCin", fontsize=8, fontweight='bold', color='#2B6CB0', va='center')
    ax.text(52.5, 98, "OP[1:0] / CONTROL BUS", fontsize=8.5, fontweight='bold', color='#B7791F', ha='center')
    ax.text(52.5, 2, "CLK / RESET / TEST PINS", fontsize=8.5, fontweight='bold', color='#2D3748', ha='center')
    ax.text(100, 50, "OUT[3:0]\nCout\nZ_flag", fontsize=8.5, fontweight='bold', color='#6B46C1', va='center')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_alu_4bit_top_architecture("02 - Student Workbook/images/alu_4bit_top_architecture.png")
    draw_alu_chip_layout_floorplan("02 - Student Workbook/images/alu_chip_layout_floorplan.png")
