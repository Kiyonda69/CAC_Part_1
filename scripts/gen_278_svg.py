#!/usr/bin/env python3
"""航大思考278用 等角投影SVG生成
ポリキューブ（小立方体の集合体）を等角投影でSVG描画する。
- 描画順: x+y+z 昇順（画家のアルゴリズム）
- 可視面: 上面(+z)・右面(+x)・左面(+y)
- グレースケール: 上面=白, 右面=中間, 左面=濃灰
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from verify_278 import (A1, Q1_OPTIONS, A2, B2, Q2_OPTIONS, ROTS, normalize)

# 等角投影パラメータ（1単位立方体）
S = 15.0          # 立方体一辺の基準
W = S * 0.866     # x/y方向の水平成分
H = S * 0.5       # x/y方向の垂直成分
CZ = S            # z方向（鉛直）成分

FILL_TOP = "#ffffff"
FILL_RIGHT = "#cccccc"   # +x面
FILL_LEFT = "#8c8c8c"    # +y面
STROKE = "#222222"


def iso(x, y, z):
    """格子点(x,y,z) → スクリーン座標(u,v)（vは下向き正）"""
    return ((x - y) * W, (x + y) * H - z * CZ)


def cube_faces(x, y, z):
    """1立方体の可視3面のポリゴン頂点列を返す"""
    p = {}
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                p[(dx, dy, dz)] = iso(x + dx, y + dy, z + dz)
    top = [p[(0, 0, 1)], p[(1, 0, 1)], p[(1, 1, 1)], p[(0, 1, 1)]]
    right = [p[(1, 0, 0)], p[(1, 1, 0)], p[(1, 1, 1)], p[(1, 0, 1)]]
    left = [p[(0, 1, 0)], p[(1, 1, 0)], p[(1, 1, 1)], p[(0, 1, 1)]]
    return [(top, FILL_TOP), (right, FILL_RIGHT), (left, FILL_LEFT)]


def hidden_count(cells):
    """3方向すべて隣接立方体に覆われて見えない立方体の数"""
    s = set(cells)
    return sum(1 for (x, y, z) in s
               if (x + 1, y, z) in s and (x, y + 1, z) in s and (x, y, z + 1) in s)


def best_orientation(cells):
    """隠れ立方体が最少（原則0）の表示向きを決定的に選ぶ"""
    cands = []
    for i, r in enumerate(ROTS):
        o = sorted(normalize([r(c) for c in cells]))
        h = hidden_count(o)
        zmax = max(c[2] for c in o)
        cands.append((h, zmax, o, i))
    cands.sort(key=lambda t: (t[0], t[1], t[2]))
    return cands[0][2], cands[0][0]


def polycube_svg_group(cells, ox, oy):
    """ポリキューブを描く<g>要素（原点(ox,oy)へ平行移動）"""
    parts = [f'<g transform="translate({ox:.1f}, {oy:.1f})">']
    for (x, y, z) in sorted(cells, key=lambda c: c[0] + c[1] + c[2]):
        for pts, fill in cube_faces(x, y, z):
            pstr = " ".join(f"{u:.1f},{v:.1f}" for u, v in pts)
            parts.append(
                f'<polygon points="{pstr}" fill="{fill}" '
                f'stroke="{STROKE}" stroke-width="1"/>')
    parts.append('</g>')
    return "\n".join(parts)


def bounds(cells):
    """投影後のバウンディングボックス (umin,umax,vmin,vmax)"""
    us, vs = [], []
    for (x, y, z) in cells:
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    u, v = iso(x + dx, y + dy, z + dz)
                    us.append(u)
                    vs.append(v)
    return min(us), max(us), min(vs), max(vs)


def centered_group(cells, cx, cy):
    """バウンディング中心が(cx,cy)に来るように配置した<g>を返す"""
    u0, u1, v0, v1 = bounds(cells)
    ox = cx - (u0 + u1) / 2
    oy = cy - (v0 + v1) / 2
    return polycube_svg_group(cells, ox, oy)


def label(x, y, text, size=14, anchor="middle"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" class="svg-text" '
            f'font-size="{size}" text-anchor="{anchor}">{text}</text>')


def box_with_dims(dims, cx, cy):
    """寸法ラベル付きの完成形直方体を描く"""
    bx, by, bz = dims
    cells = [(x, y, z) for x in range(bx) for y in range(by) for z in range(bz)]
    u0, u1, v0, v1 = bounds(cells)
    ox = cx - (u0 + u1) / 2
    oy = cy - (v0 + v1) / 2
    g = polycube_svg_group(cells, ox, oy)
    labs = []
    # 前面下端の辺（y=by側: (0,by,0)-(bx,by,0)）に x方向の個数
    mx = [(a + b) / 2 for a, b in zip(iso(0, by, 0), iso(bx, by, 0))]
    labs.append(label(ox + mx[0] - 8, oy + mx[1] + 16, str(bx)))
    # 右下端の辺（x=bx側: (bx,0,0)-(bx,by,0)）に y方向の個数
    my = [(a + b) / 2 for a, b in zip(iso(bx, 0, 0), iso(bx, by, 0))]
    labs.append(label(ox + my[0] + 10, oy + my[1] + 14, str(by)))
    # 右側の鉛直辺（(bx,0,0)-(bx,0,bz)）に z方向の個数
    mz = [(a + b) / 2 for a, b in zip(iso(bx, 0, 0), iso(bx, 0, bz))]
    labs.append(label(ox + mz[0] + 10, oy + mz[1] + 4, str(bz)))
    return g + "\n" + "\n".join(labs)


def piece_svg(cells, w, h, num=None):
    """単体ピースのSVG（選択肢ボタン用・番号ラベル付き）"""
    body = centered_group(cells, w / 2, h / 2 + (8 if num else 0))
    head = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    lab = label(w / 2, 16, f"({num})", size=14) if num else ""
    return f"{head}\n{lab}\n{body}\n</svg>"


def layer_grid(rows_labels, ox, oy, cell=34, title=""):
    """層ごとの平面図（各マスに部品記号）rows_labels[y][x]、yは奥→手前"""
    parts = []
    if title:
        parts.append(label(ox + len(rows_labels[0]) * cell / 2, oy - 8, title, 13))
    for gy, row in enumerate(rows_labels):
        for gx, lab_txt in enumerate(row):
            x = ox + gx * cell
            y = oy + gy * cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                         f'fill="white" stroke="#222" stroke-width="1.5"/>')
            parts.append(label(x + cell / 2, y + cell / 2 + 5, lab_txt, 13))
    return "\n".join(parts)


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    files = {}

    # ---- 問1 メイン図: 完成形(2x2x3) + 立体A ----
    a1_disp, h1 = best_orientation(A1)
    assert h1 == 0, "立体Aの表示向きに隠れ立方体がある"
    main1 = ['<svg width="480" height="190" viewBox="0 0 480 190">',
             box_with_dims((3, 2, 2), 130, 95),
             label(130, 180, "【完成させる直方体】", 13),
             centered_group(a1_disp, 360, 90),
             label(360, 180, "【立体A】", 13),
             '</svg>']
    files["q1_main.svg"] = "\n".join(main1)

    # ---- 問1 選択肢 ----
    for n, cells in Q1_OPTIONS.items():
        disp, h = best_orientation(cells)
        assert h == 0, f"問1選択肢{n}に隠れ立方体"
        files[f"q1_opt{n}.svg"] = piece_svg(disp, 110, 120, n)

    # ---- 問2 メイン図: 完成形(3x3x3) + 立体A + 立体B ----
    a2_disp, ha = best_orientation(A2)
    b2_disp, hb = best_orientation(B2)
    print("問2 A隠れ:", ha, " B隠れ:", hb)
    main2 = ['<svg width="620" height="220" viewBox="0 0 620 220">',
             box_with_dims((3, 3, 3), 110, 100),
             label(110, 205, "【完成させる立方体】", 13),
             centered_group(a2_disp, 330, 100),
             label(330, 205, "【立体A】", 13),
             centered_group(b2_disp, 520, 100),
             label(520, 205, "【立体B】", 13),
             '</svg>']
    files["q2_main.svg"] = "\n".join(main2)

    # ---- 問2 選択肢 ----
    for n, cells in Q2_OPTIONS.items():
        disp, h = best_orientation(cells)
        assert h == 0, f"問2選択肢{n}に隠れ立方体"
        files[f"q2_opt{n}.svg"] = piece_svg(disp, 118, 132, n)

    for name, content in files.items():
        with open(os.path.join(outdir, name), "w") as f:
            f.write(content)
        print("wrote", name)


if __name__ == "__main__":
    main()
