#!/usr/bin/env python3
"""Rà soát nhanh tệp Markdown của bài lab (Student Book hoặc Teacher Book).

Kiểm: ký tự CJK lạc, bảng bị vỡ (số cột không khớp), ảnh tham chiếu không tồn tại,
từ tuyệt đối, rò đáp án trong Student Book, ngữ cảnh đơn vị SPICE dễ nhầm.

Dùng:  python lint_lab.py <tệp hoặc thư mục> [--role student|teacher]
Thoát mã 1 nếu có mức ERROR.
"""
import argparse, pathlib, re, sys

CJK = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]')
ABS = re.compile(r'(hoàn toàn|tuyệt đối|hoàn hảo|luôn luôn|không bao giờ|100\s?%)', re.I)
LEAK = re.compile(r'(Instructor_Solutions|đáp án|đáp số|lời giải|solutions?)', re.I)
IMG = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
SPICE_M = re.compile(r'(?<![\w.])\d+(?:\.\d+)?M(?![a-zA-Z\d])')
SPICE_F = re.compile(r'(?<![\w.])\d+(?:\.\d+)?F(?![a-zA-Z\d])')


def split_row(line):
    """Tách ô của hàng bảng, bỏ qua gạch đứng trong code span."""
    out, cur, in_code = [], '', False
    for ch in line.strip():
        if ch == '`':
            in_code = not in_code
        if ch == '|' and not in_code:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    if out and out[0].strip() == '':
        out = out[1:]
    if out and out[-1].strip() == '':
        out = out[:-1]
    return out


def lint(path, role):
    text = path.read_text(encoding='utf-8', errors='replace').replace('\r', '')
    lines = text.split('\n')
    res = []  # (level, line, msg)
    in_code = False
    table = []
    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith('```'):
            in_code = not in_code
            continue
        for m in CJK.finditer(ln):
            res.append(('ERROR', i, f'ký tự CJK lạc: "{m.group()}" trong: {ln.strip()[:60]}'))
            break
        if in_code:
            for m in SPICE_M.finditer(ln):
                res.append(('WARN', i, f'"{m.group()}" trong mã SPICE là milli, không phải mega (dùng Meg)'))
            for m in SPICE_F.finditer(ln):
                res.append(('WARN', i, f'"{m.group()}" trong mã SPICE là femto, không phải farad'))
            continue
        for m in ABS.finditer(ln):
            res.append(('WARN', i, f'từ tuyệt đối "{m.group()}": viết điều kiện áp dụng'))
        for m in IMG.finditer(ln):
            p = m.group(1).split()[0]
            if not p.startswith(('http://', 'https://', 'data:')) and not (path.parent / p).exists():
                res.append(('WARN', i, f'ảnh không có trong gói: {p}'))
        if role == 'student' and LEAK.search(ln):
            res.append(('ERROR', i, f'có thể rò đáp án / trỏ tới thư mục đáp án: {ln.strip()[:70]}'))
        if ln.strip().startswith('|'):
            table.append((i, ln))
        else:
            if len(table) >= 2:
                res += check_table(table)
            table = []
    if len(table) >= 2:
        res += check_table(table)
    blanks = text.count('____')
    return res, blanks


def check_table(rows):
    out = []
    n = len(split_row(rows[0][1]))
    for i, ln in rows[1:]:
        k = len(split_row(ln))
        if k != n:
            out.append(('ERROR', i, f'bảng lệch cột: {k} ô thay vì {n} (có gạch đứng trong ô?)'))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('path')
    ap.add_argument('--role', choices=['student', 'teacher'], default='student')
    a = ap.parse_args()
    root = pathlib.Path(a.path)
    files = sorted(root.rglob('*.md')) if root.is_dir() else [root]
    err = 0
    for f in files:
        res, blanks = lint(f, a.role)
        e = sum(1 for r in res if r[0] == 'ERROR')
        w = len(res) - e
        err += e
        print(f'== {f.name}: {e} ERROR, {w} WARN, {blanks} chỗ trống ____')
        for lvl, ln, msg in res[:40]:
            print(f'  [{lvl}] dòng {ln}: {msg}')
        if len(res) > 40:
            print(f'  ... còn {len(res) - 40} mục nữa')
    sys.exit(1 if err else 0)


if __name__ == '__main__':
    main()
