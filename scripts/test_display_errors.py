import glob
import re

open_files = [
    '01 - De_Cuong_Hoc_Phan/De_Cuong_Chi_Tiet_TH_Thiet_Ke_VLSI.md',
    '02 - Giao_Trinh_Lab_Handouts/lab-01-dac-tinh-mosfet-va-cmos-inverter.md',
    '03 - Instructor_Solutions/lab00/dap_an_chi_tiet_lab00.md',
    '03 - Instructor_Solutions/lab01/dap_an_chi_tiet_lab01.md',
    '03 - Instructor_Solutions/lab02/dap_an_chi_tiet_lab02.md',
    '03 - Instructor_Solutions/lab03/dap_an_chi_tiet_lab03.md'
]

print("=== CHECKING ALL OPEN FILES FOR DISPLAY / RENDERING ISSUES ===")

for filepath in open_files:
    print(f"\n--- Checking: {filepath} ---")
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()

    # 1. Check display math blocks $$...$$
    # Must have blank line before and after
    in_block = False
    for i, line in enumerate(lines):
        if line.strip() == '$$':
            if not in_block:
                # Opening $$
                in_block = True
                if i > 0 and lines[i-1].strip() != '':
                    print(f"  Line {i+1}: Missing blank line BEFORE opening $$: previous line is '{lines[i-1].strip()}'")
            else:
                # Closing $$
                in_block = False
                if i < len(lines) - 1 and lines[i+1].strip() != '':
                    print(f"  Line {i+1}: Missing blank line AFTER closing $$: next line is '{lines[i+1].strip()}'")

    # 2. Check for pipes inside inline math in tables
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and line.strip().endswith('|'):
            # It's a table row
            # Find all inline math $...$ in this line
            maths = re.findall(r'(?<!\\)\$(.*?)(?<!\\)\$', line)
            for m in maths:
                if '|' in m:
                    print(f"  Line {i+1}: Pipe '|' inside math expression in table row: ${m}$")

    # 3. Check for unescaped code blocks or weird characters
    for i, line in enumerate(lines):
        if line.strip() == '```':
            print(f"  Line {i+1}: Fenced code block without language tag: '```'")
