import glob
import re
import os

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = text.splitlines()
    errors = []

    # 1. Check for table pipe issues
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            # Check if there is raw | inside math
            math_matches = re.finditer(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', line)
            for mm in math_matches:
                m_str = mm.group(1)
                if '|' in m_str:
                    errors.append((idx, 'TABLE_PIPE', f"Raw '|' in table math: '${m_str}$'"))

    # 2. Check for whitespace bordering math delimiter: '$ foo' or 'foo $'
    for idx, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            continue
        clean = re.sub(r'`[^`]*`', '', line)
        matches = re.finditer(r'(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)', clean)
        for mm in matches:
            m_str = mm.group(1)
            if m_str.startswith(' ') or m_str.endswith(' '):
                errors.append((idx, 'MATH_WHITESPACE', f"Whitespace inside delimiter: '${m_str}$'"))

    # 3. Check for Vietnamese characters inside math expressions
    vn_regex = re.compile(r'[àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđĐ]')
    # In block math
    for mm in re.finditer(r'\$\$([^\$]+)\$\$', text, flags=re.DOTALL):
        m_str = mm.group(1)
        if vn_regex.search(m_str):
            line_no = text[:mm.start()].count('\n') + 1
            errors.append((line_no, 'VN_IN_BLOCK_MATH', f"Vietnamese inside $$: '{m_str.strip()[:80]}'"))

    # In inline math
    no_block = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    for idx, line in enumerate(no_block.splitlines(), 1):
        if line.strip().startswith('```'):
            continue
        clean = re.sub(r'`[^`]*`', '', line)
        for mm in re.finditer(r'(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)', clean):
            m_str = mm.group(1)
            if vn_regex.search(m_str):
                errors.append((idx, 'VN_IN_INLINE_MATH', f"Vietnamese inside $: '{m_str.strip()}'"))

    # 4. Check for unclosed $ on lines
    for idx, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            continue
        clean = re.sub(r'`[^`]*`', '', line)
        clean = re.sub(r'\$\$.*?\$\$', '', clean)
        clean = clean.replace(r'\$', '')
        if clean.count('$') % 2 != 0:
            errors.append((idx, 'UNPAIRED_DOLLAR', f"Unpaired single $ on line: '{clean.strip()[:80]}'"))

    # 5. Check for $$ embedded with text on same line (e.g. '> $$...$$' or 'text $$...$$')
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('> $$') or (stripped.startswith('>') and '$$' in stripped):
            errors.append((idx, 'BLOCKQUOTE_MATH', f"$$ inside blockquote (>): '{stripped[:80]}'"))
        elif '$$' in stripped and not stripped.startswith('$$'):
            errors.append((idx, 'EMBEDDED_DOUBLE_DOLLAR', f"$$ embedded with text on same line: '{stripped[:80]}'"))

    return errors

def main():
    md_files = glob.glob('**/*.md', recursive=True)
    total = 0
    file_count = 0
    for fpath in sorted(md_files):
        errs = audit_file(fpath)
        if errs:
            file_count += 1
            print(f"\n[FILE] {fpath} ({len(errs)} issues):")
            for line_no, err_type, msg in errs:
                print(f"  L{line_no:4d} [{err_type}]: {msg}")
            total += len(errs)

    print(f"\n==========================================")
    print(f"Summary: {total} issues found across {file_count} files (out of {len(md_files)} files).")

if __name__ == '__main__':
    main()
