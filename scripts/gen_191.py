# -*- coding: utf-8 -*-
"""航大思考191 生成スクリプト: 立体図形の一筆書き問題のSVG/HTMLを生成。
検証済み(verify_191.py)の辺グラフと完全一致する作図を出力する。"""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 各立体の2D投影座標(頂点番号 -> (x,y))。verify_191.py の頂点番号に対応
COORDS = {
    "正四面体": {0: (50, 30), 1: (22, 98), 2: (78, 98), 3: (50, 74)},
    "立方体": {0: (38, 30), 1: (88, 30), 2: (72, 46), 3: (22, 46),
              4: (38, 76), 5: (88, 76), 6: (72, 92), 7: (22, 92)},
    "三角柱": {0: (35, 28), 1: (20, 80), 2: (62, 80),
             3: (57, 14), 4: (42, 66), 5: (84, 66)},
    "四角錐": {0: (52, 22), 1: (24, 92), 2: (70, 92), 3: (84, 74), 4: (38, 74)},
    "三角双錐": {0: (50, 16), 1: (50, 104), 2: (26, 60), 3: (74, 60), 4: (50, 48)},
    "正八面体": {0: (52, 14), 1: (52, 106), 2: (20, 58),
              3: (52, 70), 4: (84, 58), 5: (52, 46)},
}

# 実線(見える辺)と破線(隠れた辺)。verify_191.py の辺集合と一致することは別途検証済み
SOLID = {
    "正四面体": [(0, 1), (0, 2), (1, 2)],
    "立方体": [(0, 1), (1, 2), (2, 3), (3, 0), (5, 6), (6, 7), (1, 5), (2, 6), (3, 7)],
    "三角柱": [(0, 1), (1, 2), (2, 0), (5, 3), (0, 3), (2, 5)],
    "四角錐": [(1, 2), (2, 3), (0, 1), (0, 2), (0, 3)],
    "三角双錐": [(2, 3), (0, 2), (0, 3), (1, 2), (1, 3)],
    "正八面体": [(2, 3), (3, 4), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)],
}
DASH = {
    "正四面体": [(0, 3), (1, 3), (2, 3)],
    "立方体": [(0, 4), (4, 5), (7, 4)],
    "三角柱": [(3, 4), (4, 5), (1, 4)],
    "四角錐": [(3, 4), (4, 1), (0, 4)],
    "三角双錐": [(3, 4), (4, 2), (0, 4), (1, 4)],
    "正八面体": [(4, 5), (5, 2), (0, 5), (1, 5)],
}

# 問ごとの選択肢配置(位置1..5の立体名)
Q1_ORDER = ["正四面体", "立方体", "三角双錐", "三角柱", "四角錐"]   # 正解=位置3
Q2_ORDER = ["三角双錐", "四角錐", "立方体", "正八面体", "三角柱"]   # 正解=位置4


def _bbox(name):
    xs = [p[0] for p in COORDS[name].values()]
    ys = [p[1] for p in COORDS[name].values()]
    return min(xs), min(ys), max(xs), max(ys)


def fit_coords(name, rx0, ry0, rx1, ry1):
    """立体の頂点を矩形[rx0,ry0]-[rx1,ry1]に縦横比保持で最大化配置。"""
    x0, y0, x1, y1 = _bbox(name)
    w, h = x1 - x0, y1 - y0
    s = min((rx1 - rx0) / w, (ry1 - ry0) / h)
    ox = rx0 + ((rx1 - rx0) - w * s) / 2 - x0 * s
    oy = ry0 + ((ry1 - ry0) - h * s) / 2 - y0 * s
    co = {v: (round(p[0] * s + ox, 1), round(p[1] * s + oy, 1))
          for v, p in COORDS[name].items()}
    return co, s


def solid_lines(name, rect):
    """立体を矩形rect=(x0,y0,x1,y1)いっぱいに描く線分と頂点ドットを返す。"""
    co, s = fit_coords(name, *rect)
    sw = round(2.2 * s, 2)        # 実線の太さ
    dw = round(1.7 * s, 2)        # 破線の太さ
    r = round(3.4 * s, 2)         # 頂点ドット半径
    dash = f"{round(5*s,1)},{round(3.5*s,1)}"
    out = []
    for a, b in SOLID[name]:
        x1, y1 = co[a]
        x2, y2 = co[b]
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                   f'stroke="black" stroke-width="{sw}" stroke-linecap="round"/>')
    for a, b in DASH[name]:
        x1, y1 = co[a]
        x2, y2 = co[b]
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                   f'stroke="black" stroke-width="{dw}" stroke-dasharray="{dash}"/>')
    for (x, y) in co.values():
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="black"/>')
    return "\n            ".join(out)


if __name__ == "__main__":
    import gen_191_build  # 組み立て処理を分割
    gen_191_build.main(globals())
