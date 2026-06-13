#!/usr/bin/env python3
"""航大思考216 図形生成: 立体ピース嵌め合わせ問題のSVGを生成する。

等角風（キャビネット）投影で単位立方体の集合を描く。
- x（右）: 画面 (+W, 0)
- z（上）: 画面 (0, -H)
- y（奥）: 画面 (+Dx, -Dy)
各立方体の見える3面（上面・前面・右面）を塗り分け、
ペインターのアルゴリズム（奥から手前）で重ね描きする。
"""

W, H, DX, DY = 38, 38, 20, 20  # 立方体の画面寸法


def proj(x, y, z, ox, oy):
    return (ox + x * W + y * DX, oy - z * H - y * DY)


def cube_svg(x, y, z, ox, oy, top="#ffffff", front="#d9d9d9", side="#b3b3b3",
             stroke="#222", sw=1.4):
    """単位立方体1個分の3面ポリゴンを返す。"""
    def pt(a, b, c):
        px, py = proj(a, b, c, ox, oy)
        return f"{px:.1f},{py:.1f}"
    top_f = f'<polygon points="{pt(x,y,z+1)} {pt(x+1,y,z+1)} {pt(x+1,y+1,z+1)} {pt(x,y+1,z+1)}" fill="{top}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
    front_f = f'<polygon points="{pt(x,y,z)} {pt(x+1,y,z)} {pt(x+1,y,z+1)} {pt(x,y,z+1)}" fill="{front}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
    side_f = f'<polygon points="{pt(x+1,y,z)} {pt(x+1,y+1,z)} {pt(x+1,y+1,z+1)} {pt(x+1,y,z+1)}" fill="{side}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
    return top_f + front_f + side_f


def cubes_svg(cells, ox, oy, **kw):
    """複数立方体を奥から手前へ重ね描き。"""
    # 視点: 前(小y)・右(大x)・上(大z)。遠い順 = (-x + y - z) 降順。
    order = sorted(cells, key=lambda c: (-c[0] + c[1] - c[2]), reverse=True)
    return "".join(cube_svg(x, y, z, ox, oy, **kw) for (x, y, z) in order)


def _raw_extent(cells):
    xs, ys = [], []
    for (x, y, z) in cells:
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    px, py = proj(x + dx, y + dy, z + dz, 0, 0)
                    xs.append(px)
                    ys.append(py)
    return min(xs), max(xs), min(ys), max(ys)


def figure(cells, pad=16, label=None, **kw):
    """立方体集合を、自動サイズのviewBox付き<svg>に収めて返す。"""
    mnx, mxx, mny, mxy = _raw_extent(cells)
    lab_h = 22 if label else 0
    w = (mxx - mnx) + 2 * pad
    h = (mxy - mny) + 2 * pad + lab_h
    ox = pad - mnx
    oy = pad - mny + lab_h  # 画面yはoyから上方向に伸びる
    body = cubes_svg(cells, ox, oy, **kw)
    if label:
        body += (f'<text x="{w/2:.1f}" y="{h-6:.1f}" text-anchor="middle" '
                 f'font-size="15" font-weight="bold">{label}</text>')
    return (f'<svg width="{w:.0f}" height="{h:.0f}" '
            f'viewBox="0 0 {w:.0f} {h:.0f}">{body}</svg>')


if __name__ == "__main__":
    cells = [(x, y, z) for x in range(2) for y in range(2) for z in range(2)]
    print(figure(cells, label="test")[:160])
