"""
Generates clean, publication-quality schematic diagrams for Lab 02:
- nor2_schematic.png: NOR2 gate in Electric VLSI (nor2_x1{sch})
- nand2_schematic.png: NAND2 gate in Electric VLSI (nand2_x1{sch})
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_nor2_schematic():
    fig, ax = plt.subplots(figsize=(9, 8), dpi=300)
    ax.set_xlim(-1, 9)
    ax.set_ylim(-1, 9)
    ax.axis('off')
    
    # Title & Cell Info
    ax.text(4, 8.6, "Electric VLSI: nor2_x1{sch} (Cổng NOR2 CMOS)", 
            fontsize=15, fontweight='bold', ha='center', color='#1a365d')
    ax.text(4, 8.2, "Bố trí: 2 PMOS nối tiếp (W=24λ, L=2λ) + 2 NMOS song song (W=4λ, L=2λ)", 
            fontsize=11, ha='center', color='#4a5568', style='italic')

    # Styles
    wire_color = '#2d3748'
    pmos_color = '#c53030'
    nmos_color = '#2b6cb0'
    port_color = '#22543d'
    port_box = dict(boxstyle="round,pad=0.3", fc="#e6fffa", ec="#319795", lw=1.5)
    size_box = dict(boxstyle="square,pad=0.2", fc="#edf2f7", ec="#cbd5e0", lw=1)

    # VDD Rail & Port
    ax.plot([2, 6], [7.5, 7.5], color=wire_color, lw=2.5)
    ax.text(4, 7.5, "●", color=wire_color, ha='center', va='center', fontsize=12)
    ax.plot([4, 4], [7.5, 7.8], color=wire_color, lw=2)
    ax.text(4, 8.0, "vdd [Power]", fontsize=11, fontweight='bold', ha='center', 
            va='center', bbox=port_box, color=port_color)

    # MP1 (Top PMOS - Input A)
    # Source connected to VDD at (4, 7.5)
    ax.plot([4, 4], [7.5, 6.7], color=wire_color, lw=2)
    # Transistor box / symbol at center (4, 6.3)
    rect_mp1 = patches.Rectangle((3.5, 5.9), 1.0, 0.8, fill=True, fc="#fff5f5", ec=pmos_color, lw=2)
    ax.add_patch(rect_mp1)
    ax.text(4.0, 6.3, "MP1 (PMOS)\nW=24λ (7.2µm)\nL=2λ (0.6µm)", fontsize=9, ha='center', va='center', color=pmos_color, fontweight='bold')
    # Gate connection on left
    ax.plot([2.5, 3.5], [6.3, 6.3], color=wire_color, lw=2)
    ax.plot([2.5, 2.5], [6.3, 6.3], color=wire_color, lw=2)
    # Circle for PMOS inversion bubble at gate
    bubble_mp1 = patches.Circle((3.35, 6.3), 0.1, fill=False, ec=pmos_color, lw=1.5)
    ax.add_patch(bubble_mp1)

    # MP2 (Bottom PMOS - Input B)
    # Wire between MP1 and MP2 (Internal node xp)
    ax.plot([4, 4], [5.9, 5.1], color=wire_color, lw=2)
    ax.text(4.15, 5.5, "Node xp\n(nút nội)", fontsize=8, color='#718096', va='center')
    
    rect_mp2 = patches.Rectangle((3.5, 4.3), 1.0, 0.8, fill=True, fc="#fff5f5", ec=pmos_color, lw=2)
    ax.add_patch(rect_mp2)
    ax.text(4.0, 4.7, "MP2 (PMOS)\nW=24λ (7.2µm)\nL=2λ (0.6µm)", fontsize=9, ha='center', va='center', color=pmos_color, fontweight='bold')
    ax.plot([2.5, 3.5], [4.7, 4.7], color=wire_color, lw=2)
    bubble_mp2 = patches.Circle((3.35, 4.7), 0.1, fill=False, ec=pmos_color, lw=1.5)
    ax.add_patch(bubble_mp2)

    # Connection from MP2 drain to Out node
    ax.plot([4, 4], [4.3, 3.5], color=wire_color, lw=2)
    ax.text(4, 3.5, "●", color=wire_color, ha='center', va='center', fontsize=12)

    # Output Wire and Port out
    ax.plot([4, 7.2], [3.5, 3.5], color=wire_color, lw=2.5)
    ax.text(7.6, 3.5, "out [Output]", fontsize=11, fontweight='bold', ha='left', 
            va='center', bbox=port_box, color=port_color)

    # Parallel NMOS: MN1 (left) and MN2 (right)
    # Split wire from Out node (4, 3.5) to (2.5, 3.5) and (5.5, 3.5)
    ax.plot([2.5, 5.5], [3.5, 3.5], color=wire_color, lw=2)
    ax.plot([2.5, 2.5], [3.5, 2.7], color=wire_color, lw=2)
    ax.plot([5.5, 5.5], [3.5, 2.7], color=wire_color, lw=2)

    # MN1 (Input A, Left)
    rect_mn1 = patches.Rectangle((2.0, 1.9), 1.0, 0.8, fill=True, fc="#ebf8ff", ec=nmos_color, lw=2)
    ax.add_patch(rect_mn1)
    ax.text(2.5, 2.3, "MN1 (NMOS)\nW=4λ (1.2µm)\nL=2λ (0.6µm)", fontsize=8.5, ha='center', va='center', color=nmos_color, fontweight='bold')
    
    # MN2 (Input B, Right)
    rect_mn2 = patches.Rectangle((5.0, 1.9), 1.0, 0.8, fill=True, fc="#ebf8ff", ec=nmos_color, lw=2)
    ax.add_patch(rect_mn2)
    ax.text(5.5, 2.3, "MN2 (NMOS)\nW=4λ (1.2µm)\nL=2λ (0.6µm)", fontsize=8.5, ha='center', va='center', color=nmos_color, fontweight='bold')

    # Source connections to GND rail
    ax.plot([2.5, 2.5], [1.9, 1.1], color=wire_color, lw=2)
    ax.plot([5.5, 5.5], [1.9, 1.1], color=wire_color, lw=2)
    ax.plot([2.0, 6.0], [1.1, 1.1], color=wire_color, lw=2.5)
    ax.text(4, 1.1, "●", color=wire_color, ha='center', va='center', fontsize=12)
    ax.plot([4, 4], [1.1, 0.6], color=wire_color, lw=2)
    ax.text(4, 0.3, "gnd [Ground]", fontsize=11, fontweight='bold', ha='center', 
            va='center', bbox=port_box, color=port_color)

    # Gate input wires & Ports A, B
    # Port A connects to MP1 gate (3.5, 6.3) and MN1 gate (2.0, 2.3)
    ax.plot([1.0, 2.5], [6.3, 6.3], color=wire_color, lw=2)
    ax.plot([1.0, 1.0], [6.3, 2.3], color=wire_color, lw=2)
    ax.plot([1.0, 2.0], [2.3, 2.3], color=wire_color, lw=2)
    ax.text(0.8, 4.3, "A [Input]", fontsize=11, fontweight='bold', ha='right', 
            va='center', bbox=port_box, color=port_color)

    # Port B connects to MP2 gate (3.5, 4.7) and MN2 gate (6.0, 2.3)
    ax.plot([1.8, 3.5], [4.7, 4.7], color=wire_color, lw=2)
    ax.plot([1.8, 1.8], [4.7, 1.5], color=wire_color, lw=1.5, ls='--')
    ax.plot([1.8, 6.5], [1.5, 1.5], color=wire_color, lw=1.5, ls='--')
    ax.plot([6.5, 6.5], [1.5, 2.3], color=wire_color, lw=1.5, ls='--')
    ax.plot([6.0, 6.5], [2.3, 2.3], color=wire_color, lw=1.5, ls='--')
    ax.text(1.6, 4.7, "B [Input]", fontsize=11, fontweight='bold', ha='right', 
            va='center', bbox=port_box, color=port_color)

    # Annotation for Export Ports checklist
    checklist = (
        "DANH MỤC EXPORT PORTS BẮT BUỘC:\n"
        "1. Port 'A'   : Type = Input\n"
        "2. Port 'B'   : Type = Input\n"
        "3. Port 'out' : Type = Output\n"
        "4. Port 'vdd' : Type = Power\n"
        "5. Port 'gnd' : Type = Ground\n\n"
        "QUY TẮC SIZING (W/L):\n"
        "• PMOS (MP1, MP2 nối tiếp): W=24λ, L=2λ\n"
        "• NMOS (MN1, MN2 song song): W=4λ, L=2λ"
    )
    ax.text(7.2, 6.0, checklist, fontsize=9.5, va='top', ha='left',
            bbox=dict(boxstyle="round,pad=0.5", fc="#fffaf0", ec="#dd6b20", lw=1.5),
            color='#7b341e', family='monospace')

    plt.tight_layout()
    fig.savefig("02 - Student Workbook/images/nor2_schematic.png")
    plt.close(fig)
    print("Created nor2_schematic.png successfully.")

def draw_nand2_schematic():
    fig, ax = plt.subplots(figsize=(9, 8), dpi=300)
    ax.set_xlim(-1, 9)
    ax.set_ylim(-1, 9)
    ax.axis('off')
    
    # Title & Cell Info
    ax.text(4, 8.6, "Electric VLSI: nand2_x1{sch} (Cổng NAND2 CMOS)", 
            fontsize=15, fontweight='bold', ha='center', color='#1a365d')
    ax.text(4, 8.2, "Bố trí: 2 PMOS song song (W=12λ, L=2λ) + 2 NMOS nối tiếp (W=8λ, L=2λ)", 
            fontsize=11, ha='center', color='#4a5568', style='italic')

    wire_color = '#2d3748'
    pmos_color = '#c53030'
    nmos_color = '#2b6cb0'
    port_color = '#22543d'
    port_box = dict(boxstyle="round,pad=0.3", fc="#e6fffa", ec="#319795", lw=1.5)

    # VDD Rail & Port
    ax.plot([2, 6], [7.5, 7.5], color=wire_color, lw=2.5)
    ax.text(4, 7.5, "●", color=wire_color, ha='center', va='center', fontsize=12)
    ax.plot([4, 4], [7.5, 7.8], color=wire_color, lw=2)
    ax.text(4, 8.0, "vdd [Power]", fontsize=11, fontweight='bold', ha='center', 
            va='center', bbox=port_box, color=port_color)

    # PMOS Parallel: MP1 (left) and MP2 (right)
    # Wires from VDD to MP1 and MP2
    ax.plot([2.5, 5.5], [7.5, 7.5], color=wire_color, lw=2)
    ax.plot([2.5, 2.5], [7.5, 6.7], color=wire_color, lw=2)
    ax.plot([5.5, 5.5], [7.5, 6.7], color=wire_color, lw=2)

    # MP1 (Input A, Left)
    rect_mp1 = patches.Rectangle((2.0, 5.9), 1.0, 0.8, fill=True, fc="#fff5f5", ec=pmos_color, lw=2)
    ax.add_patch(rect_mp1)
    ax.text(2.5, 6.3, "MP1 (PMOS)\nW=12λ (3.6µm)\nL=2λ (0.6µm)", fontsize=8.5, ha='center', va='center', color=pmos_color, fontweight='bold')
    bubble_mp1 = patches.Circle((1.85, 6.3), 0.1, fill=False, ec=pmos_color, lw=1.5)
    ax.add_patch(bubble_mp1)

    # MP2 (Input B, Right)
    rect_mp2 = patches.Rectangle((5.0, 5.9), 1.0, 0.8, fill=True, fc="#fff5f5", ec=pmos_color, lw=2)
    ax.add_patch(rect_mp2)
    ax.text(5.5, 6.3, "MP2 (PMOS)\nW=12λ (3.6µm)\nL=2λ (0.6µm)", fontsize=8.5, ha='center', va='center', color=pmos_color, fontweight='bold')
    bubble_mp2 = patches.Circle((4.85, 6.3), 0.1, fill=False, ec=pmos_color, lw=1.5)
    ax.add_patch(bubble_mp2)

    # PMOS drains to common Out wire
    ax.plot([2.5, 2.5], [5.9, 5.1], color=wire_color, lw=2)
    ax.plot([5.5, 5.5], [5.9, 5.1], color=wire_color, lw=2)
    ax.plot([2.5, 5.5], [5.1, 5.1], color=wire_color, lw=2)
    ax.text(4, 5.1, "●", color=wire_color, ha='center', va='center', fontsize=12)

    # Output Wire and Port out
    ax.plot([4, 7.2], [5.1, 5.1], color=wire_color, lw=2.5)
    ax.text(7.6, 5.1, "out [Output]", fontsize=11, fontweight='bold', ha='left', 
            va='center', bbox=port_box, color=port_color)

    # Series NMOS: MN1 and MN2
    # Wire from Out (4, 5.1) to MN1 drain
    ax.plot([4, 4], [5.1, 4.3], color=wire_color, lw=2)

    # MN1 (Top NMOS - Input A)
    rect_mn1 = patches.Rectangle((3.5, 3.5), 1.0, 0.8, fill=True, fc="#ebf8ff", ec=nmos_color, lw=2)
    ax.add_patch(rect_mn1)
    ax.text(4.0, 3.9, "MN1 (NMOS)\nW=8λ (2.4µm)\nL=2λ (0.6µm)", fontsize=9, ha='center', va='center', color=nmos_color, fontweight='bold')
    ax.plot([2.5, 3.5], [3.9, 3.9], color=wire_color, lw=2)

    # Wire between MN1 and MN2 (Internal node xn)
    ax.plot([4, 4], [3.5, 2.7], color=wire_color, lw=2)
    ax.text(4.15, 3.1, "Node xn\n(nút nội)", fontsize=8, color='#718096', va='center')

    # MN2 (Bottom NMOS - Input B)
    rect_mn2 = patches.Rectangle((3.5, 1.9), 1.0, 0.8, fill=True, fc="#ebf8ff", ec=nmos_color, lw=2)
    ax.add_patch(rect_mn2)
    ax.text(4.0, 2.3, "MN2 (NMOS)\nW=8λ (2.4µm)\nL=2λ (0.6µm)", fontsize=9, ha='center', va='center', color=nmos_color, fontweight='bold')
    ax.plot([2.5, 3.5], [2.3, 2.3], color=wire_color, lw=2)

    # Source of MN2 to GND rail
    ax.plot([4, 4], [1.9, 1.1], color=wire_color, lw=2)
    ax.plot([2.0, 6.0], [1.1, 1.1], color=wire_color, lw=2.5)
    ax.text(4, 1.1, "●", color=wire_color, ha='center', va='center', fontsize=12)
    ax.plot([4, 4], [1.1, 0.6], color=wire_color, lw=2)
    ax.text(4, 0.3, "gnd [Ground]", fontsize=11, fontweight='bold', ha='center', 
            va='center', bbox=port_box, color=port_color)

    # Gate input wires & Ports A, B
    # Port A connects to MP1 (1.85, 6.3) and MN1 (2.5, 3.9)
    ax.plot([0.8, 1.75], [6.3, 6.3], color=wire_color, lw=2)
    ax.plot([0.8, 0.8], [6.3, 3.9], color=wire_color, lw=2)
    ax.plot([0.8, 3.5], [3.9, 3.9], color=wire_color, lw=2)
    ax.text(0.6, 5.1, "A [Input]", fontsize=11, fontweight='bold', ha='right', 
            va='center', bbox=port_box, color=port_color)

    # Port B connects to MP2 (4.85, 6.3) and MN2 (3.5, 2.3)
    ax.plot([1.6, 2.5], [2.3, 2.3], color=wire_color, lw=2)
    ax.plot([1.6, 1.6], [2.3, 1.5], color=wire_color, lw=1.5, ls='--')
    ax.plot([1.6, 6.5], [1.5, 1.5], color=wire_color, lw=1.5, ls='--')
    ax.plot([6.5, 6.5], [1.5, 6.3], color=wire_color, lw=1.5, ls='--')
    ax.plot([5.0, 6.5], [6.3, 6.3], color=wire_color, lw=1.5, ls='--')
    ax.text(1.4, 2.3, "B [Input]", fontsize=11, fontweight='bold', ha='right', 
            va='center', bbox=port_box, color=port_color)

    checklist = (
        "DANH MỤC EXPORT PORTS BẮT BUỘC:\n"
        "1. Port 'A'   : Type = Input\n"
        "2. Port 'B'   : Type = Input\n"
        "3. Port 'out' : Type = Output\n"
        "4. Port 'vdd' : Type = Power\n"
        "5. Port 'gnd' : Type = Ground\n\n"
        "QUY TẮC SIZING (W/L):\n"
        "• PMOS (MP1, MP2 song song): W=12λ, L=2λ\n"
        "• NMOS (MN1, MN2 nối tiếp): W=8λ, L=2λ"
    )
    ax.text(7.2, 7.0, checklist, fontsize=9.5, va='top', ha='left',
            bbox=dict(boxstyle="round,pad=0.5", fc="#fffaf0", ec="#dd6b20", lw=1.5),
            color='#7b341e', family='monospace')

    plt.tight_layout()
    fig.savefig("02 - Student Workbook/images/nand2_schematic.png")
    plt.close(fig)
    print("Created nand2_schematic.png successfully.")

if __name__ == "__main__":
    draw_nor2_schematic()
    draw_nand2_schematic()
