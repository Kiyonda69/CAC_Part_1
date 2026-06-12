#!/usr/bin/env python3
"""航大思考213 のSVG図版スニペットを生成して /tmp/svg213/ に出力する"""
import os

OUT = "/tmp/svg213"
os.makedirs(OUT, exist_ok=True)

# 問1: 高さグリッド（d=0手前, x=0左）。表示は上が奥。
GRID = [
    [1, 2, 0, 1],  # d=0 手前
    [2, 0, 3, 1],
    [0, 3, 1, 4],
    [2, 1, 2, 0],  # d=3 奥
]
Q1_OPTS = {1: [4, 3, 3, 2], 2: [2, 4, 3, 2], 3: [1, 2, 0, 1],
           4: [2, 3, 4, 4], 5: [2, 3, 3, 4]}
F = [3, 1, 4, 2]            # 問2 正面図
R_DISP = [1, 3, 4, 2]       # 問2 右側面図（左→右=奥→手前）


def rects(heights, x0, base_y, u):
    """柱状シルエットの単位正方形rect群を返す"""
    out = []
    for i, h in enumerate(heights):
        for k in range(h):
            x = x0 + u * i
            y = base_y - u * (k + 1)
            out.append(f'<rect x="{x}" y="{y}" width="{u}" height="{u}" '
                       f'fill="#d9d9d9" stroke="black" stroke-width="1"/>')
    return out


def q1_main():
    """真上から見た4x4グリッド＋方向矢印（SVG 460x350）"""
    gx, gy, c = 110, 40, 50
    p = ['<svg width="460" height="350" viewBox="0 0 460 350">']
    p.append(f'<text x="{gx + 2 * c}" y="30" class="svg-text" '
             'text-anchor="middle" font-size="14">奥</text>')
    # グリッド線
    for i in range(5):
        p.append(f'<line x1="{gx + c * i}" y1="{gy}" x2="{gx + c * i}" '
                 f'y2="{gy + 4 * c}" stroke="black" stroke-width="2"/>')
        p.append(f'<line x1="{gx}" y1="{gy + c * i}" x2="{gx + 4 * c}" '
                 f'y2="{gy + c * i}" stroke="black" stroke-width="2"/>')
    # 数字（表示行: 上=奥d3 → 下=手前d0）
    for row_disp in range(4):
        d = 3 - row_disp
        for x in range(4):
            v = GRID[d][x]
            if v > 0:
                cx = gx + c * x + c // 2
                cy = gy + c * row_disp + c // 2 + 7
                p.append(f'<text x="{cx}" y="{cy}" class="svg-text" '
                         f'text-anchor="middle" font-size="20" '
                         f'font-weight="bold">{v}</text>')
    # 矢印A（手前→グリッド: 下から上へ）
    ax = gx + 2 * c
    p.append(f'<line x1="{ax}" y1="310" x2="{ax}" y2="255" '
             'stroke="black" stroke-width="2"/>')
    p.append(f'<polygon points="{ax},248 {ax - 6},260 {ax + 6},260" fill="black"/>')
    p.append(f'<text x="{ax}" y="332" class="svg-text" text-anchor="middle" '
             'font-size="14">A（正面）</text>')
    # 矢印B（右→グリッド: 右から左へ）
    by = gy + 2 * c
    p.append(f'<line x1="430" y1="{by}" x2="335" y2="{by}" '
             'stroke="black" stroke-width="2"/>')
    p.append(f'<polygon points="328,{by} 340,{by - 6} 340,{by + 6}" fill="black"/>')
    p.append(f'<text x="385" y="{by - 14}" class="svg-text" text-anchor="middle" '
             'font-size="14">B（右側面）</text>')
    p.append('</svg>')
    return "\n".join(p)


def q1_opt_dyn(n):
    """インタラクティブ版の選択肢SVG（90x110）"""
    h = Q1_OPTS[n]
    p = [f'<svg width="90" height="110" viewBox="0 0 90 110">',
         f'<text x="45" y="15" class="svg-text" text-anchor="middle">({n})</text>',
         '<line x1="10" y1="100" x2="80" y2="100" stroke="black" stroke-width="2"/>']
    p += rects(h, 13, 100, 16)
    p.append('</svg>')
    return "\n".join(p)


def q1_opts_print():
    """印刷用の選択肢SVG（600x180, 5択横並び）"""
    p = ['<svg width="600" height="180" viewBox="0 0 600 180">']
    for n in range(1, 6):
        gx0 = 10 + 100 * (n - 1)
        p.append(f'<g transform="translate({gx0}, 30)">')
        p.append(f'<text x="40" y="12" class="svg-text" text-anchor="middle">({n})</text>')
        p.append('<line x1="5" y1="95" x2="75" y2="95" stroke="black" stroke-width="2"/>')
        p += rects(Q1_OPTS[n], 8, 95, 16)
        p.append('</g>')
    p.append('</svg>')
    return "\n".join(p)


def q2_views():
    """問2: 正面図と右側面図（SVG 520x240）"""
    u = 30
    p = ['<svg width="520" height="240" viewBox="0 0 520 240">']
    # 正面図（A方向）
    p.append('<text x="120" y="30" class="svg-text" text-anchor="middle" '
             'font-size="14">正面（Aの方向）から見た図</text>')
    p.append('<line x1="45" y1="180" x2="195" y2="180" stroke="black" stroke-width="2"/>')
    p += rects(F, 60, 180, u)
    p.append('<text x="75" y="202" class="svg-text" text-anchor="middle" '
             'font-size="13">左</text>')
    p.append('<text x="165" y="202" class="svg-text" text-anchor="middle" '
             'font-size="13">右</text>')
    # 右側面図（B方向）
    p.append('<text x="380" y="30" class="svg-text" text-anchor="middle" '
             'font-size="14">右側面（Bの方向）から見た図</text>')
    p.append('<line x1="305" y1="180" x2="455" y2="180" stroke="black" stroke-width="2"/>')
    p += rects(R_DISP, 320, 180, u)
    p.append('<text x="335" y="202" class="svg-text" text-anchor="middle" '
             'font-size="13">奥</text>')
    p.append('<text x="425" y="202" class="svg-text" text-anchor="middle" '
             'font-size="13">手前</text>')
    p.append('</svg>')
    return "\n".join(p)


def main():
    snippets = {"q1_main": q1_main(), "q1_opts_print": q1_opts_print(),
                "q2_views": q2_views()}
    for n in range(1, 6):
        snippets[f"q1_opt_dyn_{n}"] = q1_opt_dyn(n)
    for name, svg in snippets.items():
        with open(f"{OUT}/{name}.svg", "w") as fp:
            fp.write(svg)
        print(f"{name}: {len(svg)} bytes")


if __name__ == "__main__":
    main()
