# -*- coding: utf-8 -*-
"""航大思考227 SVG生成補助：検証済みセル集合をSVG矩形に変換して出力"""
import sys
sys.path.insert(0, "scripts")
from verify_227 import (normalize, dims, rot90cw, rot180, rot270cw, mirror)


def rects(cells, ox, oy, cs, fill="#cccccc"):
    """セル集合を、原点(ox,oy)・セル一辺csのSVG矩形文字列にする"""
    cells = normalize(cells)
    R, C = dims(cells)
    out = []
    for r, c in sorted(cells):
        x = ox + c * cs
        y = oy + r * cs
        out.append(f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" '
                   f'fill="{fill}" stroke="black" stroke-width="1.5"/>')
    return "\n".join(out), R, C


def option_svg(cells, cs=18):
    """選択肢用：90x110 viewBox内に中央寄せで描く矩形群を返す"""
    cells = normalize(cells)
    R, C = dims(cells)
    w, h = C * cs, R * cs
    ox = (90 - w) / 2
    oy = 22 + (78 - h) / 2  # ラベル(1)分を空ける
    s, _, _ = rects(cells, ox, oy, cs)
    return s


def figs(base):
    return {
        "cw90": rot90cw(base),
        "ccw90": rot270cw(base),
        "rot180": rot180(base),
        "mirror": mirror(base),
        "mir_cw90": rot90cw(mirror(base)),
    }


if __name__ == "__main__":
    base1 = {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1)}
    base2 = {(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3)}

    print("########## 問1 元図 (cs=26, 原点20,20) ##########")
    s, R, C = rects(base1, 20, 20, 26)
    print(s)
    print(f"# grid {R}x{C}")

    f1 = figs(base1)
    # pos1=rot180, pos2=mirror, pos3=cw90(正解), pos4=ccw90, pos5=mir_cw90
    order1 = ["rot180", "mirror", "cw90", "ccw90", "mir_cw90"]
    for i, k in enumerate(order1, 1):
        print(f"\n########## 問1 選択肢({i}) = {k} ##########")
        print(option_svg(f1[k]))

    print("\n\n########## 問2 元図 (cs=26, 原点20,20) ##########")
    s, R, C = rects(base2, 20, 20, 26)
    print(s)
    print(f"# grid {R}x{C}")

    f2 = figs(base2)
    # pos1=ccw90, pos2=cw90(正解), pos3=mirror, pos4=rot180, pos5=mir_cw90
    order2 = ["ccw90", "cw90", "mirror", "rot180", "mir_cw90"]
    for i, k in enumerate(order2, 1):
        print(f"\n########## 問2 選択肢({i}) = {k} ##########")
        print(option_svg(f2[k]))
