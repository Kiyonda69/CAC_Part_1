# -*- coding: utf-8 -*-
"""航大思考218 SVG生成: 立体（積み木の壁）を斜投影で描画する。

verify_218 の Solid を受け取り、SVG文字列を返す。
- 前面: 白
- 上面: 薄いグレー(#e6e6e6)
- 側面: 中間グレー(#bdbdbd)
- 目印 dot=●(黒円), sq=■(黒四角)
グレースケールのみ。
"""
from verify_218 import (Q1_solid, Q1_options, Q1_mirror, Q1_correct,
                        Q2_solid, Q2_options, Q2_mirror, Q2_correct)


def render(solid, s=34, depth_ratio=0.42, pad=14, label=None,
           label_fs=15, mark_scale=1.0):
    """Solid を斜投影SVGに描画して (svg_inner, width, height) を返す。"""
    d = s * depth_ratio
    ddx = d if solid.depth == 'R' else -d
    ddy = -d
    cells = solid.cells
    # 前面グリッドの基準。bounding box を計算するため一旦 x0=y0=0 で配置。
    def fx(c): return c * s
    def fy(r): return r * s
    xs, ys = [], []
    for (c, r) in cells:
        xs += [fx(c), fx(c) + s, fx(c) + ddx, fx(c) + s + ddx]
        ys += [fy(r), fy(r) + s, fy(r) + ddy, fy(r) + s + ddy]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    topgap = label_fs + 8 if label else 0
    offx = pad - minx
    offy = pad - miny + topgap
    width = (maxx - minx) + pad * 2
    height = (maxy - miny) + pad * 2 + topgap

    def FX(c): return fx(c) + offx
    def FY(r): return fy(r) + offy

    parts = []
    if label:
        parts.append('<text x="%.1f" y="%.1f" text-anchor="middle" '
                     'font-size="%d" font-family="sans-serif" '
                     'font-weight="bold">%s</text>'
                     % (width / 2, label_fs + 2, label_fs, label))

    # 奥行き面（上面・側面）を先に描く
    for (c, r) in sorted(cells, key=lambda t: (t[1], t[0])):
        x, y = FX(c), FY(r)
        # 上面: 真上にキューブが無いとき見える
        if (c, r - 1) not in cells:
            pts = "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
                x, y, x + s, y, x + s + ddx, y + ddy, x + ddx, y + ddy)
            parts.append('<polygon points="%s" fill="#e6e6e6" '
                         'stroke="#333" stroke-width="1.5"/>' % pts)
        # 側面
        if solid.depth == 'R':
            if (c + 1, r) not in cells:
                pts = "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
                    x + s, y, x + s + ddx, y + ddy,
                    x + s + ddx, y + s + ddy, x + s, y + s)
                parts.append('<polygon points="%s" fill="#bdbdbd" '
                             'stroke="#333" stroke-width="1.5"/>' % pts)
        else:
            if (c - 1, r) not in cells:
                pts = "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
                    x, y, x + ddx, y + ddy,
                    x + ddx, y + s + ddy, x, y + s)
                parts.append('<polygon points="%s" fill="#bdbdbd" '
                             'stroke="#333" stroke-width="1.5"/>' % pts)

    # 前面（白）
    for (c, r) in sorted(cells, key=lambda t: (t[1], t[0])):
        x, y = FX(c), FY(r)
        parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                     'fill="#fff" stroke="#333" stroke-width="1.5"/>'
                     % (x, y, s, s))

    # 目印
    for name, (c, r) in solid.markers.items():
        cx, cy = FX(c) + s / 2, FY(r) + s / 2
        if name == 'dot':
            parts.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#000"/>'
                         % (cx, cy, s * 0.17 * mark_scale))
        else:  # sq
            half = s * 0.16 * mark_scale
            parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                         'fill="#000"/>'
                         % (cx - half, cy - half, half * 2, half * 2))

    inner = "".join(parts)
    return inner, width, height


def svg_tag(inner, w, h):
    return ('<svg width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>'
            % (round(w), round(h), round(w), round(h), inner))
