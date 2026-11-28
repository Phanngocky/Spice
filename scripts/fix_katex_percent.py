#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Safely eliminates % and \% inside $...$ and $$...$$ across all .md files
so Markdown backslash-unescaping never turns \% into a LaTeX % comment in KaTeX.
"""

import glob, re

def clean_math_span(full_match):
    is_display = full_match.startswith('$$')
    delim = '$$' if is_display else '$'
    inner = full_match[2:-2] if is_display else full_match[1:-1]

    if '%' not in inner:
        return full_match

    # Case 1: Subscripts like _{50\%} or _{CLK,50\%} or _{D,50\%}
    inner = re.sub(r'50\\?%', '50', inner)

    # Case 2: Simple standalone percentage like "$40\%$" or "$\approx 40\%$" or "$\le 2,0\%$"
    stripped = inner.strip()
    if stripped.endswith(r'\%') or stripped.endswith('%'):
        # If the entire math span is just a number + % (e.g. "$40\%$", "$+40,0\%$"), drop $...$ completely
        no_pct = re.sub(r'\\?%$', '', stripped).strip()
        if re.fullmatch(r'[+\-]?\s*[0-9.,\s\-–~]+', no_pct):
            return no_pct + '%'
        # If it's a comparison/approx followed by number + % (e.g. "$\le 2,0\%$", "$\approx 69\%$"),
        # move % outside the closing $: "$\le 2,0$%"
        if not is_display:
            return f'${no_pct}$%'

    # Case 3: Expressions like "$26,1\% V_{DD}$" or "$< 1\% V_{DD}$"
    inner = re.sub(r'([0-9.,]+)\s*\\?%\s*V_\{DD\}', r'\1\\text{ pct } V_{DD}', inner)
    # Wait: better in prose: "$26,1$% $V_{DD}$" if inline!
    if not is_display and re.search(r'^\s*[<>≤≥≈~\\a-zA-Z0-9.,+\-\s]*\\?%\s+V_\{DD\}\s*$', full_match[1:-1]):
        m = re.match(r'^\s*(.*?)([0-9.,]+)\s*\\?%\s+(V_\{DD\})\s*$', full_match[1:-1])
        if m:
            prefix, num, vdd = m.groups()
            prefix_part = f'${prefix.strip()}$ ' if prefix.strip() else ''
            return f'{prefix_part}{num}% ${vdd}$'

    # Case 4: Remaining cases like "(\%)" or "\Delta t_{pd} (\%)"
    inner = re.sub(r'\(\s*\\?%\s*\)', r'(\\text{pct})', inner)
    inner = re.sub(r'\\?%', r'\\text{ pct}', inner)

    return f'{delim}{inner}{delim}'

files = sorted(glob.glob('**/*.md', recursive=True))
changed = 0
for f in files:
    if '.git' in f:
        continue
    with open(f, 'rb') as fp:
        raw = fp.read()
    text = raw.decode('utf-8')
    lines = text.splitlines(keepends=True)
    in_code = False
    new_lines = []
    for line in lines:
        if line.strip().startswith('```'):
            in_code = not in_code
            new_lines.append(line)
            continue
        if in_code or '%' not in line:
            new_lines.append(line)
            continue
        new_line = re.sub(r'\$\$(.+?)\$\$|\$([^$\n]+?)\$', lambda m: clean_math_span(m.group(0)), line)
        new_lines.append(new_line)
    new_text = ''.join(new_lines)
    if new_text != text:
        new_text = new_text.replace('\r\n', '\n')
        with open(f, 'wb') as fp:
            fp.write(new_text.encode('utf-8'))
        changed += 1
        print(f'Updated: {f}')

print(f'Total files updated: {changed}')
