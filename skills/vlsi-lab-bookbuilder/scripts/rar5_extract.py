#!/usr/bin/env python3
"""Giải nén tệp RAR5 đơn giản không cần unrar (khi môi trường không có công cụ giải nén).

Hỗ trợ: RAR5, không nén liền khối (non-solid), phương pháp nén LZ chuẩn (không bộ lọc E8/delta),
không mã hóa. Kiểm CRC32 từng tệp. Phù hợp với tệp văn bản (.md) nhỏ.
Nếu thất bại, nhờ người dùng gửi lại dạng .zip hoặc thư mục.

Dùng:  python rar5_extract.py <tệp.rar> <thư mục đích>
"""
import os, struct, sys, zlib


def vint(b, p):
    r = s = 0
    while True:
        x = b[p]; p += 1
        r |= (x & 0x7F) << s; s += 7
        if not x & 0x80:
            return r, p


def parse(d):
    if d[:8] != b'Rar!\x1a\x07\x01\x00':
        raise SystemExit('Không phải RAR5')
    files, p, solid = [], 8, False
    while p < len(d):
        p += 4
        hs, p = vint(d, p); st = p
        t, p = vint(d, p); fl, p = vint(d, p)
        if fl & 1: _, p = vint(d, p)
        data = 0
        if fl & 2: data, p = vint(d, p)
        if t == 1:
            af, p = vint(d, p); solid = bool(af & 4)
        if t == 2:
            ff, p = vint(d, p); us, p = vint(d, p); _, p = vint(d, p)
            if ff & 2: p += 4
            c = None
            if ff & 4: c = struct.unpack('<I', d[p:p + 4])[0]; p += 4
            ci, p = vint(d, p); _, p = vint(d, p); nl, p = vint(d, p)
            files.append((d[p:p + nl].decode('utf8', 'replace'), us, c, ci, ff, d[st + hs:st + hs + data]))
        p = st + hs + data
        if t == 5: break
    return files, solid


class BR:
    def __init__(s, b): s.b, s.pos = b, 0
    def bits(s, n):
        v = 0
        for _ in range(n):
            i = s.pos >> 3
            byte = s.b[i] if i < len(s.b) else 0
            v = (v << 1) | ((byte >> (7 - (s.pos & 7))) & 1); s.pos += 1
        return v


class Huff:
    def __init__(s, lens):
        s.maxl = max(lens) if lens else 0
        s.cnt = [0] * (s.maxl + 2)
        for l in lens:
            if l: s.cnt[l] += 1
        s.first = [0] * (s.maxl + 2); s.idx = [0] * (s.maxl + 2); s.syms = []
        code = 0
        for l in range(1, s.maxl + 1):
            code = (code + s.cnt[l - 1]) << 1 if l > 1 else 0
            s.first[l] = code; s.idx[l] = len(s.syms)
            s.syms += [x for x, ll in enumerate(lens) if ll == l]
    def dec(s, br):
        code = 0
        for l in range(1, s.maxl + 1):
            code = (code << 1) | br.bits(1)
            c = s.cnt[l]
            if c and 0 <= code - s.first[l] < c:
                return s.syms[s.idx[l] + code - s.first[l]]
        raise ValueError('mã Huffman sai')


def slot2len(br, slot):
    L = 2
    if slot < 8: lb = 0; L += slot
    else: lb = slot // 4 - 1; L += (4 | (slot & 3)) << lb
    if lb: L += br.bits(lb)
    return L


def unpack(comp, size, out, st):
    br = BR(comp); target = len(out) + size; old = st['old']; last = st['last']
    while len(out) < target:
        br.pos = (br.pos + 7) & ~7
        bf = br.bits(8); br.bits(8)
        bsz = 0
        for i in range(((bf >> 3) & 3) + 1): bsz |= br.bits(8) << (8 * i)
        bbs = (bf & 7) + 1; start = br.pos; endbit = start + (bsz - 1) * 8 + bbs
        if bf & 0x80:
            bl, i = [], 0
            while i < 20:
                n = br.bits(4)
                if n == 15:
                    z = br.bits(4)
                    if z == 0: bl.append(15); i += 1
                    else:
                        for _ in range(z + 2):
                            if i < 20: bl.append(0); i += 1
                else: bl.append(n); i += 1
            bd = Huff(bl); tab = []
            while len(tab) < 430:
                n = bd.dec(br)
                if n < 16: tab.append(n)
                elif n < 18: tab += [tab[-1]] * ((br.bits(3) + 3) if n == 16 else (br.bits(7) + 11))
                else: tab += [0] * ((br.bits(3) + 3) if n == 18 else (br.bits(7) + 11))
            tab = tab[:430]
            st['t'] = (Huff(tab[:306]), Huff(tab[306:370]), Huff(tab[370:386]), Huff(tab[386:430]))
        LD, DD, LDD, RD = st['t']
        def copy(L, D):
            for _ in range(L): out.append(out[-D])
        while br.pos < endbit and len(out) < target:
            m = LD.dec(br)
            if m < 256: out.append(m); continue
            if m == 256: raise ValueError('tệp dùng bộ lọc (filter), không hỗ trợ')
            if m == 257:
                if last: copy(last, old[0])
                continue
            if m >= 262:
                L = slot2len(br, m - 262); ds = DD.dec(br)
                if ds < 4: db = 0; D = 1 + ds
                else: db = ds // 2 - 1; D = 1 + ((2 | (ds & 1)) << db)
                if db > 0:
                    if db >= 4:
                        if db > 4: D += br.bits(db - 4) << 4
                        D += LDD.dec(br)
                    else: D += br.bits(db)
                if D > 0x100:
                    L += 1
                    if D > 0x2000:
                        L += 1
                        if D > 0x40000: L += 1
                old[:] = [D] + old[:3]; last = L; copy(L, D)
            else:
                n = m - 258; D = old[n]; del old[n]; old.insert(0, D)
                L = slot2len(br, RD.dec(br)); last = L; copy(L, D)
        br.pos = start + bsz * 8
        if bf & 0x40: break
    st['last'] = last
    return out


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    d = open(src, 'rb').read()
    files, solid = parse(d)
    os.makedirs(dst, exist_ok=True)
    out = bytearray(); st = {'old': [0, 0, 0, 0], 'last': 0}
    bad = 0
    for nm, us, c, ci, ff, comp in files:
        if not solid:
            out = bytearray(); st = {'old': [0, 0, 0, 0], 'last': 0}
        s = len(out)
        method = (ci >> 7) & 7
        try:
            if method == 0:
                out += comp[:us]
            else:
                unpack(comp, us, out, st)
        except Exception as e:
            print(f'LỖI {nm}: {e}'); bad += 1; continue
        data = bytes(out[s:s + us])
        ok = c is None or (zlib.crc32(data) & 0xFFFFFFFF) == c
        print(f'{nm}\t{len(data)} byte\t{"CRC OK" if ok else "CRC SAI"}')
        bad += 0 if ok else 1
        path = os.path.join(dst, nm)
        os.makedirs(os.path.dirname(path) or dst, exist_ok=True)
        open(path, 'wb').write(data)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
