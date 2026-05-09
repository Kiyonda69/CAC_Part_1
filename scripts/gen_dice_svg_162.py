"""航大思考162のSVG生成ヘルパー"""

def dice_face(x, y, val, size=60, dot_r=None):
    """サイコロの1面分（マス＋目）のSVG文字列を返す"""
    if dot_r is None:
        dot_r = max(2, round(size * 0.075))
    s = size
    pos = {
        1: [(s/2, s/2)],
        2: [(s/4, s/4), (3*s/4, 3*s/4)],
        3: [(s/4, s/4), (s/2, s/2), (3*s/4, 3*s/4)],
        4: [(s/4, s/4), (3*s/4, s/4), (s/4, 3*s/4), (3*s/4, 3*s/4)],
        5: [(s/4, s/4), (3*s/4, s/4), (s/2, s/2), (s/4, 3*s/4), (3*s/4, 3*s/4)],
        6: [(s/4, s/4), (s/4, s/2), (s/4, 3*s/4), (3*s/4, s/4), (3*s/4, s/2), (3*s/4, 3*s/4)],
    }
    out = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="white" stroke="black" stroke-width="2"/>'
    for px, py in pos[val]:
        out += f'<circle cx="{x+px:g}" cy="{y+py:g}" r="{dot_r}" fill="black"/>'
    return out


def cross_layout(arrangement, ox=20, oy=20, size=60):
    """十字型展開図 [a, b, c, d, e, f] のSVG（中身のみ）を返す
    配置:
         [a]
      [b][c][d][e]
         [f]
    """
    a, b, c, d, e, f = arrangement
    parts = []
    # a: 列2, 行1 (中央上)
    parts.append(dice_face(ox + size, oy, a, size))
    # b, c, d, e: 行2
    parts.append(dice_face(ox, oy + size, b, size))
    parts.append(dice_face(ox + size, oy + size, c, size))
    parts.append(dice_face(ox + 2*size, oy + size, d, size))
    parts.append(dice_face(ox + 3*size, oy + size, e, size))
    # f: 列2, 行3 (中央下)
    parts.append(dice_face(ox + size, oy + 2*size, f, size))
    return "".join(parts)


# 問1の選択肢
print("=" * 30, "問1の選択肢SVG", "=" * 30)
options_q1 = [
    [1, 2, 3, 4, 5, 6],
    [2, 3, 1, 4, 6, 5],   # ★正解
    [1, 3, 2, 5, 4, 6],
    [1, 4, 3, 2, 5, 6],
    [3, 1, 2, 5, 4, 6],
]
# 印刷用：選択肢サイズ size=28、SVG幅= 4*28 + 20 = 132、高= 3*28 + 30 = 114
print("\n--- 印刷用 (size=28) ---")
for i, opt in enumerate(options_q1):
    svg_inner = cross_layout(opt, ox=10, oy=20, size=28)
    print(f"\n選択肢 ({i+1}): {opt}")
    print(f'<svg width="132" height="114" viewBox="0 0 132 114">')
    print(f'  <text x="66" y="14" text-anchor="middle" class="svg-text">({i+1})</text>')
    print(f'  {svg_inner}')
    print('</svg>')

# 動的版用 (大きめ size=40)
print("\n--- 動的版 (size=40) ---")
for i, opt in enumerate(options_q1):
    svg_inner = cross_layout(opt, ox=12, oy=22, size=40)
    print(f"\n選択肢 ({i+1}):")
    print(f'<svg width="184" height="154" viewBox="0 0 184 154">')
    print(f'  <text x="92" y="16" text-anchor="middle" class="svg-text">({i+1})</text>')
    print(f'  {svg_inner}')
    print('</svg>')


# 問2の展開図
print("\n" + "=" * 30, "問2の展開図SVG", "=" * 30)
q2_arr = [3, 2, 1, 5, 6, 4]
print("\n--- 印刷用/動的兼用 (size=60) ---")
svg_inner = cross_layout(q2_arr, ox=20, oy=20, size=60)
print(f'<svg width="280" height="220" viewBox="0 0 280 220">')
print(f'  {svg_inner}')
print('</svg>')
