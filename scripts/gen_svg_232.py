# -*- coding: utf-8 -*-
"""航大思考232 箱ひげ図SVGを生成"""

def xmap(score, x0, x1, s0, s1):
    return x0 + (score - s0) * (x1 - x0) / (s1 - s0)

def box_svg(label, b, y, x0, x1, s0, s1, h=26):
    """1本の水平箱ひげ図 (b=(min,Q1,med,Q3,max))。yは箱の上端基準の中心線"""
    mn, q1, med, q3, mx = [xmap(v, x0, x1, s0, s1) for v in b]
    cy = y
    top = y - h/2
    bot = y + h/2
    p = []
    p.append(f'    <text x="38" y="{cy+5:.0f}" class="svg-text" text-anchor="end" font-weight="bold">{label}</text>')
    # ひげ（左）
    p.append(f'    <line x1="{mn:.1f}" y1="{cy}" x2="{q1:.1f}" y2="{cy}" stroke="black" stroke-width="1.5"/>')
    p.append(f'    <line x1="{mn:.1f}" y1="{top:.0f}" x2="{mn:.1f}" y2="{bot:.0f}" stroke="black" stroke-width="1.5"/>')
    # ひげ（右）
    p.append(f'    <line x1="{q3:.1f}" y1="{cy}" x2="{mx:.1f}" y2="{cy}" stroke="black" stroke-width="1.5"/>')
    p.append(f'    <line x1="{mx:.1f}" y1="{top:.0f}" x2="{mx:.1f}" y2="{bot:.0f}" stroke="black" stroke-width="1.5"/>')
    # 箱
    p.append(f'    <rect x="{q1:.1f}" y="{top:.0f}" width="{q3-q1:.1f}" height="{h}" fill="white" stroke="black" stroke-width="1.5"/>')
    # 中央値
    p.append(f'    <line x1="{med:.1f}" y1="{top:.0f}" x2="{med:.1f}" y2="{bot:.0f}" stroke="black" stroke-width="2.5"/>')
    return "\n".join(p)

def axis_svg(yaxis, x0, x1, s0, s1, step=10):
    p = []
    p.append(f'    <line x1="{x0}" y1="{yaxis}" x2="{x1}" y2="{yaxis}" stroke="#333" stroke-width="1"/>')
    s = s0
    while s <= s1:
        x = xmap(s, x0, x1, s0, s1)
        p.append(f'    <line x1="{x:.1f}" y1="{yaxis}" x2="{x:.1f}" y2="{yaxis+5}" stroke="#333" stroke-width="1"/>')
        p.append(f'    <text x="{x:.1f}" y="{yaxis+20}" class="svg-text" text-anchor="middle">{s}</text>')
        s += step
    p.append(f'    <text x="{(x0+x1)/2:.0f}" y="{yaxis+40}" class="svg-text" text-anchor="middle">（点）</text>')
    return "\n".join(p)

# ===== 問1: 5組 =====
boxes1 = [
    ("A組", (30, 45, 60, 75, 90)),
    ("B組", (40, 55, 65, 72, 85)),
    ("C組", (25, 48, 55, 82, 95)),
    ("D組", (35, 58, 70, 80, 100)),
    ("E組", (45, 50, 58, 62, 75)),
]
x0, x1, s0, s1 = 70, 590, 20, 100
print("===== 問1 SVG =====")
print('<svg width="620" height="320" viewBox="0 0 620 320">')
y = 30
for label, b in boxes1:
    print(box_svg(label, b, y, x0, x1, s0, s1))
    y += 48
print(axis_svg(y - 8, x0, x1, s0, s1))
print('</svg>')

# ===== 問2: 2クラス =====
boxes2 = [
    ("X組", (30, 50, 65, 80, 95)),
    ("Y組", (40, 52, 60, 88, 100)),
]
print("\n===== 問2 SVG =====")
print('<svg width="620" height="200" viewBox="0 0 620 200">')
y = 40
for label, b in boxes2:
    print(box_svg(label, b, y, x0, x1, s0, s1, h=34))
    y += 70
print(axis_svg(y - 18, x0, x1, s0, s1))
print('</svg>')
