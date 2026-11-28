#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob, re

files = sorted(glob.glob('**/*.md', recursive=True))
total_issues = 0
for f in files:
    if '.git' in f:
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        text = fp.read()
    lines = text.splitlines()
    in_code = False
    issues = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in re.finditer(r'\$\$(.+?)\$\$|\$([^$\n]+?)\$', line):
            math = m.group(1) if m.group(1) is not None else m.group(2)
            if '%' in math:
                issues.append((i, 'has % in math', math[:65]))
            opens = len(re.findall(r'(?<!\\)\{', math))
            closes = len(re.findall(r'(?<!\\)\}', math))
            if opens != closes:
                issues.append((i, f'brace mismatch {opens}!={closes}', math[:65]))
    if issues:
        total_issues += len(issues)
        print(f'KATEX ISSUE in {f}: {len(issues)} hits')
        for item in issues[:5]:
            print('  ', item)
print(f'Total KaTeX % / brace issues found: {total_issues}')
