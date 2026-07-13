#!/usr/bin/env python3
"""航大思考278 解説用の層別配置図SVGを生成"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from verify_278 import A1, A2, B2
from gen_278_svg import layer_grid, label


def build_layers(box, pieces):
    """pieces: {記号: cells} → z層ごとの2次元ラベル配列（y=0が上の行）"""
    bx, by, bz = box
    layers = []
    for z in range(bz):
        rows = []
        for y in range(by):
            row = []
            for x in range(bx):
                mark = "?"
                for sym, cells in pieces.items():
                    if (x, y, z) in cells:
                        mark = sym
                for_cell = mark
                row.append(for_cell)
            rows.append(row)
        layers.append(rows)
    return layers


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."

    # ---- 問1: 2x2x3 の組み立て（A + 正解(4)） ----
    box1 = (3, 2, 2)
    k1 = [(x, y, z) for x in range(3) for y in range(2) for z in range(2)
          if (x, y, z) not in A1]
    layers1 = build_layers(box1, {"A": set(A1), "(4)": set(k1)})
    parts = ['<svg width="360" height="140" viewBox="0 0 360 140">']
    titles = ["下段（1段目）", "上段（2段目）"]
    for i, rows in enumerate(layers1):
        parts.append(layer_grid(rows, 40 + i * 170, 40, cell=36, title=titles[i]))
    parts.append(label(180, 132, "※組み立て方の一例（各段を上から見た配置）", 12))
    parts.append('</svg>')
    with open(os.path.join(outdir, "q1_layers.svg"), "w") as f:
        f.write("\n".join(parts))

    # ---- 問2: 3x3x3 の組み立て（A + B + 正解(4)） ----
    box2 = (3, 3, 3)
    c2 = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)
          if (x, y, z) not in set(A2) | set(B2)]
    layers2 = build_layers(box2, {"A": set(A2), "B": set(B2), "C": set(c2)})
    parts = ['<svg width="500" height="180" viewBox="0 0 500 180">']
    titles = ["下段（1段目）", "中段（2段目）", "上段（3段目）"]
    for i, rows in enumerate(layers2):
        parts.append(layer_grid(rows, 30 + i * 160, 40, cell=36, title=titles[i]))
    parts.append(label(250, 172, "※組み立て方の一例（各段を上から見た配置）。C は (4) の立体を表す", 12))
    parts.append('</svg>')
    with open(os.path.join(outdir, "q2_layers.svg"), "w") as f:
        f.write("\n".join(parts))
    print("wrote q1_layers.svg, q2_layers.svg")


if __name__ == "__main__":
    main()
