"""
SCRIPT TAO SO DO VA DO THI KHAO SAT NAP - XA TU DIEN (RC CHARGE & DISCHARGE)
Hoc phan: Thuc hanh Thiet ke VLSI (5505382) - DH Su pham Ky thuat Da Nang
Tac gia: Phan Ngoc Ky (2026)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_rc_schematic(out_path):
    fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, "SƠ ĐỒ NGUYÊN LÝ MẠCH NẠP VÀ XẢ TỤ ĐIỆN RC CƠ BẢN", fontsize=12, fontweight='bold', ha='center', color='#1A365D')
    ax.text(50, 89, "Khảo sát quá trình quá độ (Transient) nạp và phóng điện tích với nguồn xung vuông PULSE", fontsize=8.8, ha='center', color='#4A5568')

    # Outer border frame
    rect = patches.FancyBboxPatch((5, 8), 90, 76, boxstyle="round,pad=0.5", facecolor='#F8FAFC', edgecolor='#CBD5E0', lw=1.5)
    ax.add_patch(rect)

    # 1. Pulse Source Vin
    ax.plot([18, 18], [60, 48], color='#2D3748', lw=2.0)
    ax.plot([18, 18], [32, 22], color='#2D3748', lw=2.0)
    c_vin = patches.Circle((18, 40), 8, facecolor='white', edgecolor='#3182CE', lw=2.0)
    ax.add_patch(c_vin)
    ax.text(18, 41, "Vin\nPULSE", fontsize=8.5, fontweight='bold', color='#3182CE', ha='center', va='center')
    ax.text(18, 28, "0V -> 5V", fontsize=7.5, color='#2B6CB0', ha='center')

    # Source parameters note
    src_info = "PULSE(0 5 0 10n 10n 500u 1000u)\nChu kỳ T = 1.0ms (Ton = 500us = 5*tau)"
    ax.text(18, 14, src_info, fontsize=7.2, family='monospace', ha='center', color='#4A5568')

    # 2. Resistor R
    ax.plot([18, 38], [60, 60], color='#2D3748', lw=2.0)
    res = patches.Rectangle((38, 55), 14, 10, facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.5)
    ax.add_patch(res)
    ax.text(45, 60, "R = 10kΩ", fontsize=8.5, fontweight='bold', color='#B7791F', ha='center', va='center')
    ax.plot([52, 70], [60, 60], color='#2D3748', lw=2.0)

    # Current flow arrows
    # Charge current (positive)
    ax.annotate("", xy=(34, 63), xytext=(24, 63), arrowprops=dict(arrowstyle="->", lw=1.8, color='#38A169'))
    ax.text(29, 66, "Dòng nạp i_charge > 0", fontsize=7.5, fontweight='bold', color='#2F855A', ha='center')

    # Discharge current (negative)
    ax.annotate("", xy=(24, 57), xytext=(34, 57), arrowprops=dict(arrowstyle="->", lw=1.8, color='#E53E3E'))
    ax.text(29, 52, "Dòng xả i_discharge < 0", fontsize=7.5, fontweight='bold', color='#C53030', ha='center')

    # 3. Output Node Vout / Vc
    ax.plot([70], [60], marker='o', markersize=6, color='#E53E3E')
    ax.text(70, 64, "Vout = V_C(t)", fontsize=9.0, fontweight='bold', color='#E53E3E', ha='center')

    # Lead to capacitor
    ax.plot([70, 70], [60, 48], color='#2D3748', lw=2.0)

    # Capacitor Plates
    ax.plot([62, 78], [48, 48], color='#2D3748', lw=2.5) # Top plate
    ax.plot([62, 78], [42, 42], color='#2D3748', lw=2.5) # Bottom plate
    ax.text(82, 45, "C = 10nF\nτ = RC = 100µs", fontsize=8.2, fontweight='bold', color='#2B6CB0', va='center')

    # Bottom lead to ground
    ax.plot([70, 70], [42, 22], color='#2D3748', lw=2.0)
    ax.plot([18, 70], [22, 22], color='#2D3748', lw=2.0)

    # Ground Symbol
    ax.plot([44, 44], [22, 16], color='#2D3748', lw=2.0)
    ax.plot([38, 50], [16, 16], color='#2B6CB0', lw=2.2)
    ax.plot([40, 48], [13, 13], color='#2B6CB0', lw=1.8)
    ax.plot([42, 46], [10, 10], color='#2B6CB0', lw=1.5)
    ax.text(44, 6, "GND (Node 0)", fontsize=8.0, fontweight='bold', ha='center', color='#2B6CB0')

    # Right info box: Mathematical formulas
    info_text = (
        "QUY TẮC NẠP VÀ XẢ:\n"
        "1. Quá trình Nạp (0 <= t < Ton):\n"
        "   Vc(t) = Vo * [1 - exp(-t/τ)]\n"
        "   i(t)  = (Vo/R) * exp(-t/τ) > 0\n"
        "   - Tại t = τ:   Vc = 63.2% Vo = 3.16V\n"
        "   - Tại t = 5τ:  Vc = 99.3% Vo = 4.97V (Đầy)\n"
        "\n"
        "2. Quá trình Xả (Ton <= t < T):\n"
        "   Vc(t') = Vo * exp(-t'/τ)\n"
        "   i(t')  = -(Vo/R) * exp(-t'/τ) < 0\n"
        "   - Tại t' = τ:  Vc = 36.8% Vo = 1.84V\n"
        "   - Tại t' = 5τ: Vc = 0.7% Vo = 0.03V (Hết)"
    )
    ax.text(93, 47, info_text, fontsize=7.2, family='monospace', va='center', ha='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.2))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")


def draw_rc_waveforms(out_path):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 7.5), dpi=300, sharex=True)

    # Time array: 0 to 1000 us (1.0 ms)
    t = np.linspace(0, 1000, 2000) # time in us
    tau = 100.0 # us
    V0 = 5.0 # V
    R = 10.0 # kOhm

    # Input square pulse Vin(t)
    vin = np.where(t < 500, V0, 0.0)

    # Output capacitor voltage Vc(t)
    vc = np.zeros_like(t)
    for i, ti in enumerate(t):
        if ti < 500:
            vc[i] = V0 * (1.0 - np.exp(-ti / tau))
        else:
            t_discharge = ti - 500
            vc[i] = V0 * np.exp(-t_discharge / tau)

    # Current i(t) in mA: i = (Vin - Vc)/R
    i_ma = (vin - vc) / R

    # -------------------------------------------------------------
    # PANEL 1: ĐIỆN ÁP Vin(t) VÀ Vc(t)
    # -------------------------------------------------------------
    ax1.plot(t, vin, color='#718096', lw=1.8, ls='--', label='Điện áp ngõ vào $V_{in}(t)$ (Xung vuông 0-5V)')
    ax1.plot(t, vc, color='#2B6CB0', lw=2.5, label='Điện áp trên tụ $V_C(t)$ (Nạp và Xả)')

    # Shaded phases
    ax1.axvspan(0, 500, color='#EBF8FF', alpha=0.5, label='Giai đoạn NẠP điện ($0 \\to 500\\mu\\text{s} = 5\\tau$)')
    ax1.axvspan(500, 1000, color='#FFF5F5', alpha=0.5, label='Giai đoạn XẢ điện ($500 \\to 1000\\mu\\text{s} = 5\\tau$)')

    # Annotations for Charging
    ax1.plot([100], [V0 * (1 - np.exp(-1))], marker='o', markersize=6, color='#E53E3E')
    ax1.annotate(r'$t = \tau = 100\mu\text{s}$' + '\n' + r'$V_C = 63.2\% V_0 = 3.16\text{V}$',
                 xy=(100, 3.16), xytext=(120, 2.2),
                 arrowprops=dict(arrowstyle="->", color='#E53E3E', lw=1.2), fontsize=8.2, fontweight='bold', color='#C53030')

    ax1.plot([500], [V0 * (1 - np.exp(-5))], marker='o', markersize=6, color='#2F855A')
    ax1.annotate(r'$t = 5\tau = 500\mu\text{s}$' + '\n' + r'Nạp đầy $99.3\% \approx 5.0\text{V}$',
                 xy=(500, 4.97), xytext=(350, 4.0),
                 arrowprops=dict(arrowstyle="->", color='#2F855A', lw=1.2), fontsize=8.2, fontweight='bold', color='#2F855A')

    # Annotations for Discharging
    ax1.plot([600], [V0 * np.exp(-1)], marker='o', markersize=6, color='#D69E2E')
    ax1.annotate(r"$t' = \tau = 100\mu\text{s}$ ($t=600\mu\text{s}$)" + '\n' + r'$V_C = 36.8\% V_0 = 1.84\text{V}$',
                 xy=(600, 1.84), xytext=(630, 2.8),
                 arrowprops=dict(arrowstyle="->", color='#D69E2E', lw=1.2), fontsize=8.2, fontweight='bold', color='#B7791F')

    ax1.plot([1000], [V0 * np.exp(-5)], marker='o', markersize=6, color='#805AD5')
    ax1.annotate(r"$t' = 5\tau = 500\mu\text{s}$ ($t=1000\mu\text{s}$)" + '\n' + r'Xả cạn $0.7\% \approx 0\text{V}$',
                 xy=(1000, 0.05), xytext=(780, 0.8),
                 arrowprops=dict(arrowstyle="->", color='#805AD5', lw=1.2), fontsize=8.2, fontweight='bold', color='#6B46C1')

    ax1.set_ylabel('Điện áp (V)', fontsize=10, fontweight='bold')
    ax1.set_title('ĐÁP ỨNG QUÁ ĐỘ ĐIỆN ÁP TRONG QUÁ TRÌNH NẠP VÀ XẢ TỤ ĐIỆN RC (R=10kΩ, C=10nF, τ=100µs)', fontsize=11, fontweight='bold', color='#1A365D')
    ax1.set_ylim(-0.5, 5.8)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='center right', fontsize=8.5)

    # -------------------------------------------------------------
    # PANEL 2: DÒNG ĐIỆN NẠP VÀ XẢ i(t)
    # -------------------------------------------------------------
    ax2.plot(t, i_ma, color='#D69E2E', lw=2.2, label='Dòng điện nạp/xả qua mạch $i(t)$ (mA)')
    ax2.axhline(0, color='#A0AEC0', lw=1.0, ls='-')

    # Peak current annotations
    ax2.annotate(r'Dòng nạp cực đại: $I_{peak} = +V_0/R = +0.50\text{mA}$',
                 xy=(0, 0.50), xytext=(80, 0.38),
                 arrowprops=dict(arrowstyle="->", color='#2F855A', lw=1.2), fontsize=8.5, fontweight='bold', color='#2F855A')

    ax2.annotate(r'Dòng xả cực đại (đổi chiều): $I_{peak} = -V_0/R = -0.50\text{mA}$',
                 xy=(500, -0.50), xytext=(550, -0.35),
                 arrowprops=dict(arrowstyle="->", color='#C53030', lw=1.2), fontsize=8.5, fontweight='bold', color='#C53030')

    ax2.set_xlabel('Thời gian t (µs)', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Dòng điện (mA)', fontsize=10, fontweight='bold')
    ax2.set_title('DÒNG ĐIỆN QUÁ ĐỘ: DÒNG NẠP DƯƠNG VÀ DÒNG PHÓNG ĐIỆN TÍCH ÂM', fontsize=10.5, fontweight='bold', color='#1A365D')
    ax2.set_xlim(0, 1000)
    ax2.set_ylim(-0.65, 0.65)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='lower right', fontsize=8.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created {out_path} successfully.")

if __name__ == "__main__":
    draw_rc_schematic("02 - Student Workbook/images/rc_charge_discharge_schematic.png")
    draw_rc_waveforms("02 - Student Workbook/images/rc_charge_discharge_waveform.png")
