import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_bjt_bias_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10.5, 6.8), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(52.5, 96, "MẠCH PHÂN CỰC PHÂN ÁP & ĐO ĐẶC TUYẾN BJT NPN (2N3904)", fontsize=13, fontweight='bold', ha='center', color='#1A365D')
    ax.text(52.5, 92, "Khảo sát Điểm làm việc tĩnh DC (Q-Point) và Cấu hình đo Đặc tuyến Vào - Ra trong SPICE", fontsize=9.2, ha='center', color='#4A5568')

    # Left Side: Voltage Divider Bias Circuit (x: 10 to 50)
    # Power Rail VCC
    ax.plot([15, 48], [85, 85], color='#E53E3E', lw=2.5)
    ax.text(12, 85, "VCC = 12V", fontsize=9.5, fontweight='bold', color='#E53E3E', va='center', ha='right')
    ax.plot([15, 48], [12, 12], color='#2B6CB0', lw=2.5)
    ax.text(12, 12, "GND (0)", fontsize=9.5, fontweight='bold', color='#2B6CB0', va='center', ha='right')

    # Resistor R1 (top left)
    r1 = patches.Rectangle((18, 62), 6, 14, facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.2)
    ax.add_patch(r1)
    ax.text(21, 69, "R1\n33k", fontsize=8.0, fontweight='bold', ha='center', va='center')
    ax.plot([21, 21], [85, 76], color='#2D3748', lw=1.5)
    ax.plot([21, 21], [62, 48], color='#2D3748', lw=1.5)

    # Resistor R2 (bottom left)
    r2 = patches.Rectangle((18, 22), 6, 14, facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.2)
    ax.add_patch(r2)
    ax.text(21, 29, "R2\n10k", fontsize=8.0, fontweight='bold', ha='center', va='center')
    ax.plot([21, 21], [48, 36], color='#2D3748', lw=1.5)
    ax.plot([21, 21], [22, 12], color='#2D3748', lw=1.5)

    # Base Node VB
    ax.plot([21, 32], [48, 48], color='#2D3748', lw=1.5)
    ax.plot([21], [48], marker='o', markersize=5, color='#2B6CB0')
    ax.text(23, 51, "VB ≈ 2.70V", fontsize=7.8, fontweight='bold', color='#2B6CB0')

    # BJT Symbol (NPN)
    ax.plot([32, 32], [42, 54], color='#1A202C', lw=2.5) # Base bar
    ax.plot([26, 32], [48, 48], color='#1A202C', lw=2.0) # Base lead
    ax.plot([32, 40], [51, 62], color='#1A202C', lw=2.0) # Collector lead
    ax.plot([32, 40], [45, 34], color='#1A202C', lw=2.0) # Emitter lead
    # Emitter Arrow
    ax.annotate("", xy=(38, 37), xytext=(35, 41), arrowprops=dict(arrowstyle="->", lw=2, color='#1A202C'))
    ax.text(37, 48, "Q1\n2N3904", fontsize=7.8, fontweight='bold', color='#C53030')

    # Collector Resistor RC (top right of circuit)
    rc = patches.Rectangle((37, 68), 6, 12, facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.2)
    ax.add_patch(rc)
    ax.text(40, 74, "RC\n2.2k", fontsize=8.0, fontweight='bold', ha='center', va='center')
    ax.plot([40, 40], [85, 80], color='#2D3748', lw=1.5)
    ax.plot([40, 40], [68, 62], color='#2D3748', lw=1.5)
    ax.plot([40], [62], marker='o', markersize=5, color='#C53030')
    ax.text(42, 63, "VC ≈ 7.60V", fontsize=7.8, fontweight='bold', color='#C53030')

    # Emitter Resistor RE (bottom right of circuit)
    re = patches.Rectangle((37, 18), 6, 12, facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.2)
    ax.add_patch(re)
    ax.text(40, 24, "RE\n1.0k", fontsize=8.0, fontweight='bold', ha='center', va='center')
    ax.plot([40, 40], [34, 30], color='#2D3748', lw=1.5)
    ax.plot([40, 40], [18, 12], color='#2D3748', lw=1.5)
    ax.plot([40], [34], marker='o', markersize=5, color='#2B6CB0')
    ax.text(42, 35, "VE ≈ 2.01V", fontsize=7.8, fontweight='bold', color='#2B6CB0')

    # Circuit Frame & Note
    ax.text(30, 6, "Hình (a): Mạch Phân cực Phân áp (Voltage Divider Bias) - Điểm Q (5.58V, 2.00mA)",
            fontsize=8.5, fontweight='bold', ha='center', color='#2D3748')

    # Right Side: Test Setup for I-V Curves (x: 58 to 98)
    rect_test = patches.FancyBboxPatch((55, 14), 46, 72, boxstyle="round,pad=0.5", facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.5)
    ax.add_patch(rect_test)
    ax.text(78, 81, "CẤU HÌNH ĐO ĐẶC TUYẾN SPICE", fontsize=10, fontweight='bold', color='#1A365D', ha='center')

    # Test BJT
    ax.plot([75, 75], [44, 56], color='#1A202C', lw=2.5) # Base bar
    ax.plot([68, 75], [50, 50], color='#1A202C', lw=2.0)
    ax.plot([75, 83], [53, 64], color='#1A202C', lw=2.0) # Collector
    ax.plot([75, 83], [47, 36], color='#1A202C', lw=2.0) # Emitter
    ax.annotate("", xy=(81, 39), xytext=(78, 43), arrowprops=dict(arrowstyle="->", lw=2, color='#1A202C'))
    ax.text(80, 50, "Q_dut\n2N3904", fontsize=7.5, fontweight='bold', color='#C53030')

    # Emitter to ground
    ax.plot([83, 83], [36, 26], color='#2D3748', lw=1.5)
    ax.plot([78, 88], [26, 26], color='#2B6CB0', lw=2)
    ax.text(83, 22, "0 (GND)", fontsize=8, ha='center', color='#2B6CB0')

    # Collector to VCE source
    ax.plot([83, 94], [64, 64], color='#C53030', lw=1.5)
    c_vce = patches.Circle((94, 52), 4, facecolor='white', edgecolor='#C53030', lw=1.5)
    ax.add_patch(c_vce)
    ax.text(94, 52, "VCE\n(0-10V)", fontsize=7.0, ha='center', va='center', color='#C53030')
    ax.plot([94, 94], [64, 56], color='#C53030', lw=1.5)
    ax.plot([94, 94], [48, 26], color='#2D3748', lw=1.5)
    ax.plot([94, 83], [26, 26], color='#2D3748', lw=1.5)

    # Base to IB source (or VBE source)
    c_ib = patches.Circle((64, 50), 4, facecolor='white', edgecolor='#3182CE', lw=1.5)
    ax.add_patch(c_ib)
    ax.text(64, 50, "IB\n(Step)", fontsize=7.0, ha='center', va='center', color='#3182CE')
    ax.plot([60, 57, 57, 83], [50, 50, 26, 26], color='#2D3748', lw=1.5)

    # Command hints
    cmd_info = (
        "LỆNH MÔ PHỎNG SPICE:\n"
        "1. Đặc tuyến vào (I_B vs V_BE):\n"
        "   .dc Vbe 0 1.0 0.005\n"
        "2. Họ đặc tuyến ra (I_C vs V_CE):\n"
        "   .dc Vce 0 10 0.05 Ib 10u 50u 10u"
    )
    ax.text(78, 30, cmd_info, fontsize=7.5, family='monospace', ha='center',
            bbox=dict(boxstyle='square,pad=0.4', facecolor='#EBF8FF', edgecolor='#3182CE'))

    ax.text(78, 6, "Hình (b): Testbench đo Đặc tuyến Vào (Vbe Sweep) và Ra (Vce/Ib Sweep)",
            fontsize=8.5, fontweight='bold', ha='center', color='#2D3748')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")


def draw_bjt_iv_characteristic(out_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.5), dpi=300)

    # 1. Left Plot: Input Characteristic (IB vs VBE)
    vbe = np.linspace(0, 0.85, 200)
    Is = 1e-14
    beta = 160
    Vt = 0.02585
    ib = (Is / beta) * (np.exp(vbe / Vt) - 1)
    ib_ua = ib * 1e6

    ax1.plot(vbe, ib_ua, color='#2B6CB0', lw=2.5, label='Đặc tuyến vào $I_B(V_{BE})$')
    ax1.axvline(x=0.70, color='#E53E3E', ls='--', lw=1.5, label='Điện áp ngưỡng $V_{BE,on} \\approx 0.70V$')
    ax1.set_xlim(0, 0.85)
    ax1.set_ylim(-1, 60)
    ax1.set_xlabel('Điện áp Base-Emitter $V_{BE}$ (V)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Dòng cực gốc $I_B$ (µA)', fontsize=10, fontweight='bold')
    ax1.set_title('ĐẶC TUYẾN NGÕ VÀO BJT NPN\n($I_B$ theo $V_{BE}$)', fontsize=11, fontweight='bold', color='#1A365D')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left', fontsize=8.5)
    ax1.annotate('Vùng ngưng dẫn\n($I_B \\approx 0$)', xy=(0.4, 2), xytext=(0.2, 20),
                 arrowprops=dict(arrowstyle="->", color='#4A5568', lw=1.2), fontsize=8.5, color='#4A5568')
    ax1.annotate('Dẫn hàm mũ\n($V_{BE} \\geq 0.7V$)', xy=(0.73, 25), xytext=(0.55, 42),
                 arrowprops=dict(arrowstyle="->", color='#C53030', lw=1.2), fontsize=8.5, color='#C53030')

    # 2. Right Plot: Output Characteristics Family (IC vs VCE for Ib steps)
    vce = np.linspace(0, 10, 300)
    VA = 74.0 # Early voltage
    ib_steps = [10e-6, 20e-6, 30e-6, 40e-6, 50e-6]
    colors = ['#3182CE', '#2B6CB0', '#2C5282', '#1A365D', '#0F2440']

    for i, ib_val in enumerate(ib_steps):
        # Model saturation: tanh(vce / 0.15) transition into active mode with Early slope (1 + vce / VA)
        ic_ma = (beta * ib_val * (1.0 + vce / VA) * np.tanh(vce / 0.18)) * 1e3
        ax2.plot(vce, ic_ma, color=colors[i], lw=2.0, label=f'$I_B = {ib_val*1e6:.0f}\\mu A$')
        ax2.text(10.1, ic_ma[-1], f'{ib_val*1e6:.0f}µA', fontsize=8, color=colors[i], va='center')

    # Shaded saturation zone
    ax2.axvspan(0, 0.25, color='#FED7D7', alpha=0.35, label='Vùng bão hòa ($V_{CE} < 0.2V$)')
    ax2.axvline(x=0.20, color='#C53030', ls=':', lw=1.5)
    ax2.text(0.12, 5.0, "BÃO HÒA", fontsize=8.5, fontweight='bold', color='#9B2C2C', rotation=90, va='center')

    # Q-point marker
    ax2.plot([5.58], [2.00], marker='o', markersize=8, color='#E53E3E')
    ax2.text(5.7, 1.85, "Điểm tĩnh Q\n(5.58V, 2.00mA)", fontsize=8.5, fontweight='bold', color='#E53E3E')

    # Early voltage extrapolation dashed lines
    ax2.set_xlim(-1, 11)
    ax2.set_ylim(-0.5, 10)
    ax2.set_xlabel('Điện áp Collector-Emitter $V_{CE}$ (V)', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Dòng cực thu $I_C$ (mA)', fontsize=10, fontweight='bold')
    ax2.set_title('HỌ ĐẶC TUYẾN NGÕ RA BJT NPN\n($I_C$ theo $V_{CE}$ với tham số $I_B$)', fontsize=11, fontweight='bold', color='#1A365D')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='lower right', fontsize=8)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_bjt_bias_schematic("02 - Giao_Trinh_Lab_Handouts/images/bjt_bias_schematic.png")
    draw_bjt_iv_characteristic("02 - Giao_Trinh_Lab_Handouts/images/bjt_iv_characteristic.png")
