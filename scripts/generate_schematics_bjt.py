"""
SCRIPT TAO SO DO VA DO THI KHAO SAT DAC TUYEN VAO / RA BJT 2N3904
Hoc phan: Thuc hanh Thiet ke VLSI (5505382) - DH Su pham Ky thuat Da Nang
Tac gia: Phan Ngoc Ky (2026)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_bjt_testbench_schematic(out_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6.2), dpi=300)
    
    for ax in (ax1, ax2):
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')

    # -------------------------------------------------------------
    # SƠ ĐỒ 1 (TRÁI): MẠCH ĐO ĐẶC TUYẾN NGÕ VÀO Ib(Vbe)
    # -------------------------------------------------------------
    ax1.text(50, 95, "MẠCH ĐO ĐẶC TUYẾN NGÕ VÀO BJT NPN", fontsize=11, fontweight='bold', ha='center', color='#1A365D')
    ax1.text(50, 90, "Khảo sát dòng cực Base $I_B$ theo điện áp $V_{BE}$ (Cố định $V_{CE} = 5.0\\text{V}$)", fontsize=8.5, ha='center', color='#4A5568')

    # Khung bao quanh
    rect1 = patches.FancyBboxPatch((4, 6), 92, 80, boxstyle="round,pad=0.5", facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.5)
    ax1.add_patch(rect1)

    # BJT Q1 Symbol
    ax1.plot([50, 50], [42, 58], color='#1A202C', lw=2.5) # Base bar
    ax1.plot([42, 50], [50, 50], color='#1A202C', lw=2.0) # Base lead
    ax1.plot([50, 58], [54, 66], color='#1A202C', lw=2.0) # Collector lead
    ax1.plot([50, 58], [46, 34], color='#1A202C', lw=2.0) # Emitter lead
    ax1.annotate("", xy=(56, 37), xytext=(53, 41.5), arrowprops=dict(arrowstyle="->", lw=2, color='#1A202C'))
    ax1.text(56, 50, "Q1\n2N3904", fontsize=8.5, fontweight='bold', color='#C53030')

    # Emitter xuống đất
    ax1.plot([58, 58], [34, 22], color='#2D3748', lw=1.8)
    ax1.plot([52, 64], [22, 22], color='#2B6CB0', lw=2.2)
    ax1.plot([54, 62], [19, 19], color='#2B6CB0', lw=1.8)
    ax1.plot([56, 60], [16, 16], color='#2B6CB0', lw=1.5)
    ax1.text(58, 12, "GND (0)", fontsize=8, ha='center', color='#2B6CB0', fontweight='bold')

    # Nguồn quét VBE
    ax1.plot([42, 25], [50, 50], color='#2D3748', lw=1.8)
    c_vbe = patches.Circle((25, 40), 6, facecolor='white', edgecolor='#3182CE', lw=1.8)
    ax1.add_patch(c_vbe)
    ax1.text(25, 40, "$V_{BE}$\n$0 \\to 1\\text{V}$", fontsize=7.5, ha='center', va='center', fontweight='bold', color='#3182CE')
    ax1.plot([25, 25], [50, 46], color='#2D3748', lw=1.8)
    ax1.plot([25, 25], [34, 22], color='#2D3748', lw=1.8)
    ax1.plot([25, 58], [22, 22], color='#2D3748', lw=1.8) # Nối đất chung

    # Ampe kế ảo đo dòng IB
    ax1.annotate("", xy=(46, 50), xytext=(36, 50), arrowprops=dict(arrowstyle="->", lw=1.8, color='#E53E3E'))
    ax1.text(41, 54, "Đo $I_B$", fontsize=8, fontweight='bold', color='#E53E3E', ha='center')

    # Nguồn cố định VCE = 5V
    ax1.plot([58, 75], [66, 66], color='#2D3748', lw=1.8)
    c_vce1 = patches.Circle((75, 50), 6, facecolor='white', edgecolor='#DD6B20', lw=1.8)
    ax1.add_patch(c_vce1)
    ax1.text(75, 50, "$V_{CE}$\n$5.0\\text{V}$", fontsize=7.5, ha='center', va='center', fontweight='bold', color='#DD6B20')
    ax1.plot([75, 75], [66, 56], color='#2D3748', lw=1.8)
    ax1.plot([75, 75], [44, 22], color='#2D3748', lw=1.8)
    ax1.plot([58, 75], [22, 22], color='#2D3748', lw=1.8)

    # Lệnh SPICE Directive
    ax1.text(50, 72, "LỆNH SPICE DIRECTIVE:\n.dc Vbe 0 1.0 0.005\n.meas dc Vbe_10u WHEN I(B)=10u",
             fontsize=7.8, family='monospace', ha='center',
             bbox=dict(boxstyle='square,pad=0.4', facecolor='#EBF8FF', edgecolor='#3182CE', lw=1.2))

    # -------------------------------------------------------------
    # SƠ ĐỒ 2 (PHẢI): MẠCH ĐO HỌ ĐẶC TUYẾN NGÕ RA Ic(Vce, Ib)
    # -------------------------------------------------------------
    ax2.text(50, 95, "MẠCH ĐO HỌ ĐẶC TUYẾN NGÕ RA BJT NPN", fontsize=11, fontweight='bold', ha='center', color='#1A365D')
    ax2.text(50, 90, "Khảo sát dòng cực thu $I_C$ theo $V_{CE}$ quét tham số theo $I_B$", fontsize=8.5, ha='center', color='#4A5568')

    rect2 = patches.FancyBboxPatch((4, 6), 92, 80, boxstyle="round,pad=0.5", facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.5)
    ax2.add_patch(rect2)

    # BJT Q2 Symbol
    ax2.plot([50, 50], [42, 58], color='#1A202C', lw=2.5)
    ax2.plot([42, 50], [50, 50], color='#1A202C', lw=2.0)
    ax2.plot([50, 58], [54, 66], color='#1A202C', lw=2.0)
    ax2.plot([50, 58], [46, 34], color='#1A202C', lw=2.0)
    ax2.annotate("", xy=(56, 37), xytext=(53, 41.5), arrowprops=dict(arrowstyle="->", lw=2, color='#1A202C'))
    ax2.text(56, 50, "Q2\n2N3904", fontsize=8.5, fontweight='bold', color='#C53030')

    # Emitter xuống đất
    ax2.plot([58, 58], [34, 22], color='#2D3748', lw=1.8)
    ax2.plot([52, 64], [22, 22], color='#2B6CB0', lw=2.2)
    ax2.plot([54, 62], [19, 19], color='#2B6CB0', lw=1.8)
    ax2.plot([56, 60], [16, 16], color='#2B6CB0', lw=1.5)
    ax2.text(58, 12, "GND (0)", fontsize=8, ha='center', color='#2B6CB0', fontweight='bold')

    # Nguồn dòng bơm vào Base: Ib
    ax2.plot([42, 25], [50, 50], color='#2D3748', lw=1.8)
    c_ib = patches.Circle((25, 40), 6, facecolor='white', edgecolor='#3182CE', lw=1.8)
    ax2.add_patch(c_ib)
    ax2.text(25, 40, "$I_B$\n$10-50\\mu\\text{A}$", fontsize=7.2, ha='center', va='center', fontweight='bold', color='#3182CE')
    # Mũi tên nguồn dòng hướng vào transistor
    ax2.annotate("", xy=(38, 50), xytext=(28, 50), arrowprops=dict(arrowstyle="->", lw=1.8, color='#3182CE'))
    ax2.plot([25, 25], [50, 46], color='#2D3748', lw=1.8)
    ax2.plot([25, 25], [34, 22], color='#2D3748', lw=1.8)
    ax2.plot([25, 58], [22, 22], color='#2D3748', lw=1.8)

    # Nguồn áp quét VCE ở Collector
    ax2.plot([58, 75], [66, 66], color='#2D3748', lw=1.8)
    c_vce2 = patches.Circle((75, 50), 6, facecolor='white', edgecolor='#C53030', lw=1.8)
    ax2.add_patch(c_vce2)
    ax2.text(75, 50, "$V_{CE}$\n$0 \\to 10\\text{V}$", fontsize=7.2, ha='center', va='center', fontweight='bold', color='#C53030')
    ax2.plot([75, 75], [66, 56], color='#2D3748', lw=1.8)
    ax2.plot([75, 75], [44, 22], color='#2D3748', lw=1.8)
    ax2.plot([58, 75], [22, 22], color='#2D3748', lw=1.8)

    # Ampe kế đo dòng IC
    ax2.annotate("", xy=(66, 66), xytext=(60, 66), arrowprops=dict(arrowstyle="->", lw=1.8, color='#C53030'))
    ax2.text(63, 71, "Đo $I_C$", fontsize=8, fontweight='bold', color='#C53030', ha='center')

    # Lệnh SPICE Directive Nested Sweep
    ax2.text(50, 72, "LỆNH SPICE DIRECTIVE (2 THAM SỐ):\n.dc Vce 0 10 0.05 Ib 10u 50u 10u\n.meas dc Ic_5V WHEN V(C)=5.0",
             fontsize=7.8, family='monospace', ha='center',
             bbox=dict(boxstyle='square,pad=0.4', facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.2))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")


def draw_bjt_iv_characteristic(out_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)

    # 1. Left Plot: Input Characteristic (IB vs VBE)
    vbe = np.linspace(0, 0.85, 200)
    Is = 1e-14
    beta = 160
    Vt = 0.02585
    ib = (Is / beta) * (np.exp(vbe / Vt) - 1)
    ib_ua = ib * 1e6

    ax1.plot(vbe, ib_ua, color='#2B6CB0', lw=2.5, label=r'Đặc tuyến vào $I_B(V_{BE})$')
    ax1.axvline(x=0.70, color='#E53E3E', ls='--', lw=1.5, label=r'Ngưỡng mở $V_{BE,on} \approx 0.70\text{ V}$')
    ax1.set_xlim(0, 0.85)
    ax1.set_ylim(-1, 60)
    ax1.set_xlabel('Điện áp Base-Emitter $V_{BE}$ (V)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Dòng cực gốc $I_B$ (µA)', fontsize=10, fontweight='bold')
    ax1.set_title('ĐẶC TUYẾN NGÕ VÀO BJT NPN\n($I_B$ theo $V_{BE}$ khi cố định $V_{CE} = 5.0\\text{V}$)', fontsize=11, fontweight='bold', color='#1A365D')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left', fontsize=8.5)
    ax1.annotate(r'Vùng ngưng dẫn' + '\n' + r'($I_B \approx 0$)', xy=(0.4, 2), xytext=(0.2, 20),
                 arrowprops=dict(arrowstyle="->", color='#4A5568', lw=1.2), fontsize=8.5, color='#4A5568')
    ax1.annotate(r'Dẫn hàm mũ' + '\n' + r'($V_{BE} \geq 0.7\text{ V}$)', xy=(0.73, 25), xytext=(0.55, 42),
                 arrowprops=dict(arrowstyle="->", color='#C53030', lw=1.2), fontsize=8.5, color='#C53030')

    # 2. Right Plot: Output Characteristics Family (IC vs VCE for Ib steps)
    vce = np.linspace(0, 10, 300)
    VA = 74.0 # Early voltage
    ib_steps = [10e-6, 20e-6, 30e-6, 40e-6, 50e-6]
    colors = ['#3182CE', '#2B6CB0', '#2C5282', '#1A365D', '#0F2440']

    for i, ib_val in enumerate(ib_steps):
        # Model saturation: tanh(vce / 0.18) transition into active mode with Early slope (1 + vce / VA)
        ic_ma = (beta * ib_val * (1.0 + vce / VA) * np.tanh(vce / 0.18)) * 1e3
        ax2.plot(vce, ic_ma, color=colors[i], lw=2.0, label=f'$I_B = {ib_val*1e6:.0f}\\mu\\text{{A}}$')
        ax2.text(10.1, ic_ma[-1], f'{ib_val*1e6:.0f}µA', fontsize=8, color=colors[i], va='center')

    # Shaded saturation zone
    ax2.axvspan(0, 0.25, color='#FED7D7', alpha=0.4, label='Vùng bão hòa ($V_{CE} < 0.25\\text{V}$)')
    ax2.axvline(x=0.20, color='#C53030', ls=':', lw=1.5)
    ax2.text(0.12, 5.0, "BÃO HÒA", fontsize=8.5, fontweight='bold', color='#9B2C2C', rotation=90, va='center')

    # Annotate Active region & Beta amplification
    ax2.annotate(r'Vùng khuếch đại tích cực' + '\n' + r'$\Delta I_C / \Delta I_B = \beta \approx 160$',
                 xy=(5.0, 5.1), xytext=(3.0, 7.8),
                 arrowprops=dict(arrowstyle="->", color='#1A365D', lw=1.4), fontsize=9, fontweight='bold', color='#1A365D')

    # Annotate Early effect slope
    ax2.annotate(r'Độ dốc do hiệu ứng Early' + '\n' + r'($V_A = 74\text{ V}, r_o \approx 40\text{ k}\Omega$)',
                 xy=(8.5, 3.8), xytext=(5.5, 1.8),
                 arrowprops=dict(arrowstyle="->", color='#4A5568', lw=1.2), fontsize=8.5, color='#4A5568')

    ax2.set_xlim(-0.5, 11)
    ax2.set_ylim(-0.5, 10)
    ax2.set_xlabel('Điện áp Collector-Emitter $V_{CE}$ (V)', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Dòng cực thu $I_C$ (mA)', fontsize=10, fontweight='bold')
    ax2.set_title('HỌ ĐẶC TUYẾN NGÕ RA BJT NPN\n($I_C$ theo $V_{CE}$ quét tham số $I_B$ từ $10\\mu\\text{A} \\to 50\\mu\\text{A}$)', fontsize=11, fontweight='bold', color='#1A365D')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='lower right', fontsize=8)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_bjt_testbench_schematic("02 - Giao_Trinh_Lab_Handouts/images/bjt_bias_schematic.png")
    draw_bjt_iv_characteristic("02 - Giao_Trinh_Lab_Handouts/images/bjt_iv_characteristic.png")
