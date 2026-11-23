#!/usr/bin/env python3
"""Kiểm nhanh số liệu VLSI bằng công thức giải tích và mô hình MOSFET bậc hai.

CẢNH BÁO: mô hình bậc hai (square-law) không có bão hòa vận tốc, suy giảm độ linh động
hay hiệu ứng thân; KHÔNG phải mô hình Level 3 của MOSIS C5. Dùng để phát hiện mâu thuẫn
và đặt cận cho số đo, không dùng làm số đo.

Ví dụ:
  python quick_checks.py rc --R 20k --C 5n --V0 5
  python quick_checks.py vm --wn 4 --wp 12
  python quick_checks.py vm --wn 4 --target 2.5
  python quick_checks.py ron --wl 2 --type n
  python quick_checks.py tp --CL 50f --wn 2 --wp 6
  python quick_checks.py buffer --H 50 --p 1
  python quick_checks.py cell --wn-d 4 --wp-l 1 --wn-ax 2
"""
import argparse, math, re

DEFAULTS = dict(VDD=5.0, Vtn=0.7, Vtp=0.8, Kn=120e-6, Kp=40e-6)
SI = {'t': 1e12, 'g': 1e9, 'meg': 1e6, 'k': 1e3, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15}


def val(s):
    """Đọc số kiểu SPICE: 20k, 5n, 2.2Meg, 1e-9."""
    m = re.match(r'^\s*([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\s*([a-zA-Z]*)\s*$', str(s))
    if not m:
        raise argparse.ArgumentTypeError(f'không đọc được số: {s}')
    x, suf = float(m.group(1)), m.group(2).lower()
    if suf.startswith('meg'):
        return x * 1e6
    if suf and suf[0] in SI:
        return x * SI[suf[0]]
    return x


def add_model(p):
    p.add_argument('--VDD', type=val, default=DEFAULTS['VDD'])
    p.add_argument('--Vtn', type=val, default=DEFAULTS['Vtn'])
    p.add_argument('--Vtp', type=val, default=DEFAULTS['Vtp'])
    p.add_argument('--Kn', type=val, default=DEFAULTS['Kn'], help='K\' NMOS (A/V^2)')
    p.add_argument('--Kp', type=val, default=DEFAULTS['Kp'], help='K\' PMOS (A/V^2)')


class M:
    def __init__(s, a):
        s.VDD, s.Vtn, s.Vtp, s.Kn, s.Kp = a.VDD, a.Vtn, a.Vtp, a.Kn, a.Kp

    def In(s, vgs, vds, wl):
        if vgs <= s.Vtn or vds <= 0:
            return 0.0
        vov = vgs - s.Vtn
        return s.Kn * wl * (vov * vds - vds * vds / 2) if vds < vov else s.Kn * wl / 2 * vov * vov

    def Ip(s, vsg, vsd, wl):
        if vsg <= abs(s.Vtp) or vsd <= 0:
            return 0.0
        vov = vsg - abs(s.Vtp)
        return s.Kp * wl * (vov * vsd - vsd * vsd / 2) if vsd < vov else s.Kp * wl / 2 * vov * vov


def solve(fn, lo, hi):
    for _ in range(60):
        mid = (lo + hi) / 2
        if fn(lo) * fn(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def cmd_rc(a):
    tau = a.R * a.C
    print(f'tau            = {tau:.6g} s')
    print(f'v(tau)         = {a.V0 * (1 - math.exp(-1)):.4f} V')
    print(f't_50 (ln2)     = {math.log(2) * tau:.6g} s')
    print(f't_10 / t_90    = {-math.log(0.9) * tau:.6g} s / {math.log(10) * tau:.6g} s')
    print(f't_r (ln9)      = {math.log(9) * tau:.6g} s')
    fc = 1 / (2 * math.pi * tau)
    print(f'f_-3dB         = {fc:.6g} Hz')
    print(f't_r * f_c      = {math.log(9) * tau * fc:.4f}  (kỳ vọng ~0,35)')
    print(f'I_peak (V0/R)  = {a.V0 / a.R:.6g} A')
    print(f'Energy: C*V0^2 (nguồn) = {a.C * a.V0**2:.6g} J ; 1/2*C*V0^2 (trong R) = {0.5 * a.C * a.V0**2:.6g} J')
    for k in (1, 2, 3, 4, 5):
        print(f'  t = {k} tau : {100 * (1 - math.exp(-k)):.1f} %')


def vm(m, wn, wp):
    r = (m.Kp * wp) / (m.Kn * wn)
    return (m.Vtn + math.sqrt(r) * (m.VDD - abs(m.Vtp))) / (1 + math.sqrt(r))


def cmd_vm(a):
    m = M(a)
    if a.target is not None:
        sq = (a.target - m.Vtn) / (m.VDD - a.target - abs(m.Vtp))
        r = sq * sq
        print(f'Để V_M = {a.target} V: r = {r:.4f}; (W/L)p / (W/L)n = {r * m.Kn / m.Kp:.3f}')
        if a.wn:
            print(f'Với (W/L)n = {a.wn}: (W/L)p = {r * m.Kn / m.Kp * a.wn:.3f}')
    else:
        print(f'V_M = {vm(m, a.wn, a.wp):.4f} V  (W/L n = {a.wn}, p = {a.wp})')


def cmd_ron(a):
    m = M(a)
    K, Vt = (m.Kn, m.Vtn) if a.type == 'n' else (m.Kp, abs(m.Vtp))
    r0 = 1 / (K * a.wl * (m.VDD - Vt))
    print(f'R_on tại V_DS≈0, V_GS=V_DD: {r0:.1f} ohm')
    if a.vin is not None:
        # transmission-gate style: Vgs phụ thuộc Vin (bỏ qua hiệu ứng thân)
        vov = (m.VDD - a.vin - Vt) if a.type == 'n' else (a.vin - Vt)
        print(f'R_on tại V_in = {a.vin} V (bỏ qua hiệu ứng thân): {1 / (K * a.wl * vov):.1f} ohm' if vov > 0 else 'Linh kiện tắt tại V_in này')


def cmd_tp(a):
    m = M(a)
    dt = 1e-13
    v, t = m.VDD, 0.0
    while v > m.VDD / 2:
        v -= m.In(m.VDD, v, a.wn) / a.CL * dt
        t += dt
    hl = t
    v, t = 0.0, 0.0
    while v < m.VDD / 2:
        v += m.Ip(m.VDD, m.VDD - v, a.wp) / a.CL * dt
        t += dt
    lh = t
    rn = 1 / (m.Kn * a.wn * (m.VDD - m.Vtn))
    rp = 1 / (m.Kp * a.wp * (m.VDD - abs(m.Vtp)))
    print(f'Tích phân số (ngõ vào bước lý tưởng): tpHL = {hl * 1e12:.1f} ps, tpLH = {lh * 1e12:.1f} ps')
    print(f'0,69·R_on·C_L                      : tpHL = {0.693 * rn * a.CL * 1e12:.1f} ps, tpLH = {0.693 * rp * a.CL * 1e12:.1f} ps')
    print(f'Tỉ số tích phân số / 0,69RC (HL)   : {hl / (0.693 * rn * a.CL):.2f}')


def cmd_buffer(a):
    print('N   f=H^(1/N)   D = N(f+p)')
    best = None
    for n in range(1, 8):
        f = a.H ** (1 / n)
        d = n * (f + a.p)
        best = (n, f, d) if best is None or d < best[2] else best
        print(f'{n}   {f:8.3f}   {d:8.2f}')
    fs = solve(lambda f: f + a.p - f * math.log(f), 1.5, 20) if a.p == 1 else None
    print(f'Tối ưu rời rạc: N = {best[0]} (D = {best[2]:.2f})')
    if fs:
        print(f'f* (nghiệm f(ln f - 1) = p) ≈ {fs:.3f}; N* = ln H / ln f* = {math.log(a.H) / math.log(fs):.2f}')


def vtc(m, wn_d, wp_l, wn_ax=None):
    def f(vin):
        def net(vo):
            i = m.Ip(m.VDD - vin, m.VDD - vo, wp_l)
            if wn_ax:
                i += m.In(m.VDD - vo, m.VDD - vo, wn_ax)
            return i - m.In(vin, vo, wn_d)
        return solve(net, 0, m.VDD)
    return f


def snm(m, f):
    res = []
    for sign in (1, -1):
        best = 0
        n = 226
        for i in range(n):
            c = sign * 4.5 * i / (n - 1)
            xa = solve(lambda x: f(x) - x - c, 0, m.VDD)
            xb = solve(lambda x: f(min(max(x + c, 0), m.VDD)) - x, 0, m.VDD)
            best = max(best, abs(xa - xb))
        res.append(best)
    return min(res)


def cmd_cell(a):
    m = M(a)
    hold, read = vtc(m, a.wn_d, a.wp_l), vtc(m, a.wn_d, a.wp_l, a.wn_ax)
    cr = a.wn_d / a.wn_ax
    vq = (m.VDD - m.Vtn) * (1 - math.sqrt(cr / (1 + cr)))
    print(f'Cell ratio CR = {cr:.2f}')
    print(f'V_Q (đọc, giải bậc hai, bỏ qua hiệu ứng thân) = {vq:.3f} V')
    print(f'V_M inverter (hold) = {solve(lambda x: hold(x) - x, 0, m.VDD):.3f} V')
    print(f'SNM hold = {snm(m, hold):.3f} V ; SNM read = {snm(m, read):.3f} V (mô hình bậc hai)')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('rc'); p.add_argument('--R', type=val, required=True); p.add_argument('--C', type=val, required=True)
    p.add_argument('--V0', type=val, default=5.0); p.set_defaults(fn=cmd_rc)
    p = sub.add_parser('vm'); add_model(p); p.add_argument('--wn', type=float); p.add_argument('--wp', type=float)
    p.add_argument('--target', type=float); p.set_defaults(fn=cmd_vm)
    p = sub.add_parser('ron'); add_model(p); p.add_argument('--wl', type=float, required=True)
    p.add_argument('--type', choices=['n', 'p'], default='n'); p.add_argument('--vin', type=float); p.set_defaults(fn=cmd_ron)
    p = sub.add_parser('tp'); add_model(p); p.add_argument('--CL', type=val, required=True)
    p.add_argument('--wn', type=float, default=2); p.add_argument('--wp', type=float, default=6); p.set_defaults(fn=cmd_tp)
    p = sub.add_parser('buffer'); p.add_argument('--H', type=float, required=True); p.add_argument('--p', type=float, default=1.0)
    p.set_defaults(fn=cmd_buffer)
    p = sub.add_parser('cell'); add_model(p); p.add_argument('--wn-d', type=float, default=4)
    p.add_argument('--wp-l', type=float, default=1); p.add_argument('--wn-ax', type=float, default=2); p.set_defaults(fn=cmd_cell)
    a = ap.parse_args()
    if a.cmd == 'vm' and a.target is None and (a.wn is None or a.wp is None):
        ap.error('vm cần --wn và --wp, hoặc --target')
    a.fn(a)


if __name__ == '__main__':
    main()
