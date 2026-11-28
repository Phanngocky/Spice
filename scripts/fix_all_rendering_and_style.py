#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix corrupted LaTeX control chars, CRLF endings, table columns, and pedagogical phrasing
across all Student Workbook, Teacher_Book, and Instructor_Solutions markdown files.
"""

import glob, re

md_files = sorted(
    glob.glob('02 - Student Workbook/*.md') +
    glob.glob('Teacher_Book/*.md') +
    glob.glob('03 - Instructor_Solutions/**/*.md', recursive=True)
)

# Pedagogical phrasing replacements (exact case-preserving / context-safe)
phrase_replacements = [
    ('đối soánh', 'đối sánh'),
    ('Đối Soánh', 'Đối sánh'),
    ('trùng khớp 100%', 'trùng khớp hoàn toàn'),
    ('chính xác 100%', 'chính xác'),
    ('đạt 100%', 'đạt đầy đủ'),
    ('siêu nhanh', 'tốc độ cao'),
    ('siêu tốc', 'tốc độ cao'),
    ('vượt trội', 'đáng kể'),
    ('hoàn hảo', 'đồng bộ'),
    ('cực mạnh', 'mạnh'),
    ('xóa sổ', 'làm mất'),
    ('bất đối xứng nghiêm trọng', 'bất đối xứng lớn'),
    # Replace 'tuyệt đối' when NOT in the confidentiality disclaimer
    ('chống nhiễu tuyệt đối', 'chống nhiễu tốt'),
    ('khống chế tuyệt đối', 'chi phối trực tiếp'),
    ('an toàn tuyệt đối', 'an toàn'),
    ('tuyệt đối không', 'không'),  # Wait - careful not to touch 'Tuyệt đối không phát cho sinh viên'!
]

fixed_count = 0
for f in md_files:
    with open(f, 'rb') as fp:
        raw = fp.read()
    text = raw.decode('utf-8')
    orig = text

    # 1. Normalize CRLF -> LF
    text = text.replace('\r\n', '\n')

    # 2. Restore corrupted LaTeX control characters
    text = text.replace('\x07pprox', r'\approx')
    text = text.replace('\x07', r'\a')
    text = text.replace('\x08ar', r'\bar')
    text = text.replace('\x08egin', r'\begin')
    text = text.replace('\x08', r'\b')
    text = text.replace('\x0crac', r'\frac')
    text = text.replace('\x0c', r'\f')
    # Tab before LaTeX commands
    text = re.sub(r'\t(ext|au|imes|o\b|o_|riangle|heta|op)', r'\\t\1', text)

    # 3. Fix Teacher_Book/README.md missing column for Lab 08 and Lab 09
    if f.endswith('Teacher_Book\\README.md') or f.endswith('Teacher_Book/README.md'):
        text = text.replace(
            '| **Lab 08** | Thiết kế Ô nhớ SRAM 6T & Sense Amplifier | Đồ án / Tự chọn |',
            '| **Lab 08** | Thiết kế Ô nhớ SRAM 6T & Sense Amplifier | Ngoài đề cương | Đồ án / Tự chọn |'
        )
        text = text.replace(
            '| **Lab 09** | Khối cộng nhanh 4-bit CLA (Carry Lookahead) | Đồ án / Tự chọn |',
            '| **Lab 09** | Khối cộng nhanh 4-bit CLA (Carry Lookahead) | Ngoài đề cương | Đồ án / Tự chọn |'
        )

    # 4. Pedagogical wording polish (preserve confidentiality banner)
    banner = 'Tuyệt đối không phát cho sinh viên'
    banner_upper = 'TUYỆT ĐỐI KHÔNG PHÁT CHO SINH VIÊN'
    text = text.replace(banner, '__CONF_BANNER__').replace(banner_upper, '__CONF_BANNER_UP__')

    for old, new in phrase_replacements:
        if old == 'tuyệt đối không':
            text = text.replace('tuyệt đối không', 'không')
            text = text.replace('Tuyệt đối không', 'Không')
        else:
            text = text.replace(old, new)
            text = text.replace(old.capitalize(), new.capitalize())

    # Replace remaining 'tuyệt đối' in prose (except 'chênh lệch tuyệt đối' / 'giá trị tuyệt đối' / 'trị tuyệt đối')
    text = re.sub(r'(?<!trị )(?<!lệch )tuyệt đối', 'hoàn toàn', text)

    text = text.replace('__CONF_BANNER__', banner).replace('__CONF_BANNER_UP__', banner_upper)

    if text != orig:
        with open(f, 'wb') as fp:
            fp.write(text.encode('utf-8'))
        fixed_count += 1
        print(f'Fixed: {f}')

print(f'Total files updated: {fixed_count}')
