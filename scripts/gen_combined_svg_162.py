"""航大思考162の統合SVG生成（自己完結）"""

def dice_face(x, y, val, size=60, dot_r=None):
    if dot_r is None:
        dot_r = max(2, round(size * 0.08))
    s = size
    pos = {
        1: [(s/2, s/2)],
        2: [(s/4, s/4), (3*s/4, 3*s/4)],
        3: [(s/4, s/4), (s/2, s/2), (3*s/4, 3*s/4)],
        4: [(s/4, s/4), (3*s/4, s/4), (s/4, 3*s/4), (3*s/4, 3*s/4)],
        5: [(s/4, s/4), (3*s/4, s/4), (s/2, s/2), (s/4, 3*s/4), (3*s/4, 3*s/4)],
        6: [(s/4, s/4), (s/4, s/2), (s/4, 3*s/4), (3*s/4, s/4), (3*s/4, s/2), (3*s/4, 3*s/4)],
    }
    out = f'<rect x="{x:g}" y="{y:g}" width="{s}" height="{s}" fill="white" stroke="black" stroke-width="2"/>'
    for px, py in pos[val]:
        out += f'<circle cx="{x+px:g}" cy="{y+py:g}" r="{dot_r}" fill="black"/>'
    return out


def cross_layout(arr, ox=20, oy=20, size=60):
    a, b, c, d, e, f = arr
    parts = [
        dice_face(ox + size, oy, a, size),
        dice_face(ox, oy + size, b, size),
        dice_face(ox + size, oy + size, c, size),
        dice_face(ox + 2*size, oy + size, d, size),
        dice_face(ox + 3*size, oy + size, e, size),
        dice_face(ox + size, oy + 2*size, f, size),
    ]
    return "".join(parts)


options_q1 = [
    [1, 2, 3, 4, 5, 6],
    [2, 3, 1, 4, 6, 5],   # ★正解
    [1, 3, 2, 5, 4, 6],
    [1, 4, 3, 2, 5, 6],
    [3, 1, 2, 5, 4, 6],
]


def build_combined(size, gap, label_y, layout_oy):
    cell_w = size * 4 + 8
    cell_h = size * 3 + (layout_oy + 8)
    total_w = cell_w * 5 + gap * 4
    parts = []
    for i, opt in enumerate(options_q1):
        ox = i * (cell_w + gap)
        label_x = ox + cell_w / 2
        parts.append(f'<text x="{label_x:g}" y="{label_y}" text-anchor="middle" class="svg-text">({i+1})</text>')
        layout_ox = ox + (cell_w - size * 4) / 2
        parts.append(cross_layout(opt, ox=layout_ox, oy=layout_oy, size=size))
    return total_w, cell_h, "".join(parts)


# 印刷用 (size=28)
total_w, cell_h, body = build_combined(size=28, gap=8, label_y=14, layout_oy=22)
print("===== 印刷用 統合SVG =====")
print(f'<svg width="{total_w}" height="{cell_h}" viewBox="0 0 {total_w} {cell_h}">')
print(body)
print('</svg>')

# 動的版 (size=34)
total_w, cell_h, body = build_combined(size=34, gap=6, label_y=16, layout_oy=24)
print("\n===== 動的版 統合SVG =====")
print(f'<svg width="{total_w}" height="{cell_h}" viewBox="0 0 {total_w} {cell_h}">')
print(body)
print('</svg>')

# 動的版 各選択肢ボタン (size=20)
size = 20
btn_w = size * 4 + 16
btn_h = size * 3 + 16
print("\n===== 動的版 ボタン用 =====")
for i, opt in enumerate(options_q1):
    inner = cross_layout(opt, ox=8, oy=8, size=size)
    print(f"\n--- ({i+1}) ---")
    print(f'<svg width="{btn_w}" height="{btn_h}" viewBox="0 0 {btn_w} {btn_h}">')
    print(inner)
    print('</svg>')

# 問2の展開図 (印刷用 size=60、動的版 size=55)
print("\n===== 問2 展開図 印刷用 (size=60) =====")
inner = cross_layout([3, 2, 1, 5, 6, 4], ox=20, oy=20, size=60)
print(f'<svg width="280" height="220" viewBox="0 0 280 220">')
print(inner)
print('</svg>')

print("\n===== 問2 展開図 動的版 (size=55) =====")
inner = cross_layout([3, 2, 1, 5, 6, 4], ox=20, oy=20, size=55)
print(f'<svg width="260" height="205" viewBox="0 0 260 205">')
print(inner)
print('</svg>')
