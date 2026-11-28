#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, glob

wb_files = sorted(glob.glob('02 - Student Workbook/*.md'))
tb_files = sorted(glob.glob('Teacher_Book/*.md'))
img_dir = '02 - Student Workbook/images'
existing_imgs = set(os.listdir(img_dir)) if os.path.exists(img_dir) else set()
print('Existing images in 02 - Student Workbook/images:', sorted(existing_imgs))
print('-' * 75)

all_files = wb_files + tb_files
bad_words = [
    'cực mạnh', 'hoàn hảo', 'tuyệt đối', 'siêu nhanh', 'siêu tốc',
    'đối soánh', 'khổng lồ', 'vĩnh viễn', 'xóa sổ', 'điện荷',
    'xung nhịp xung nhịp', 'chính xác 100%', 'trùng khớp 100%',
    'hoàn toàn xứng đáng', 'phá hủy hoàn toàn', 'vượt trội'
]

for f in all_files:
    with open(f, 'rb') as fp:
        raw = fp.read()
    crlf = b'\r\n' in raw
    text = raw.decode('utf-8')
    lines = text.splitlines()

    # 1. Check code fences
    fences = sum(1 for l in lines if l.strip().startswith('```'))

    # 2. Check images
    imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)
    missing_imgs = []
    for im in imgs:
        bname = os.path.basename(im)
        if bname not in existing_imgs:
            missing_imgs.append(im)

    # 3. Check CJK
    cjk = re.findall(r'[\u4e00-\u9fff]', text)

    # 4. Check unmatched $$
    dd_count = text.count('$$')

    # 5. Check bad words
    found_bad = []
    low = text.lower()
    for bw in bad_words:
        if bw in low:
            found_bad.append(bw)

    # 6. Check table column consistency
    table_errs = 0
    in_table = False
    expected_cols = 0
    for idx, l in enumerate(lines, 1):
        s = l.strip()
        if s.startswith('|') and s.endswith('|') and ('---' not in s):
            cols = len([c for c in s.split('|')[1:-1]])
            if not in_table:
                in_table = True
                expected_cols = cols
            elif cols != expected_cols:
                table_errs += 1
        elif s.startswith('|') and ('---' in s):
            pass
        else:
            in_table = False

    # 7. Check unclosed inline $ per paragraph (outside code blocks)
    in_code = False
    odd_dollar_lines = []
    for idx, l in enumerate(lines, 1):
        if l.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Remove $$ pairs first
        l_no_dd = l.replace('$$', '')
        # Count unescaped $
        dollars = len(re.findall(r'(?<!\\)\$', l_no_dd))
        if dollars % 2 != 0:
            odd_dollar_lines.append(idx)

    if crlf or fences % 2 != 0 or missing_imgs or cjk or dd_count % 2 != 0 or found_bad or table_errs or odd_dollar_lines:
        print(f'ISSUE in {f}:')
        if crlf: print(f'  - CRLF line endings')
        if fences % 2 != 0: print(f'  - Odd code fences: {fences}')
        if missing_imgs: print(f'  - Missing images: {missing_imgs}')
        if cjk: print(f'  - CJK chars: {cjk}')
        if dd_count % 2 != 0: print(f'  - Odd $$ count: {dd_count}')
        if found_bad: print(f'  - Non-pedagogical / typo words: {found_bad}')
        if table_errs: print(f'  - Table column mismatches: {table_errs}')
        if odd_dollar_lines: print(f'  - Odd inline $ on lines: {odd_dollar_lines}')
    else:
        print(f'CLEAN: {f}')
