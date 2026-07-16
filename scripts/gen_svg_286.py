#!/usr/bin/env python3
"""航大思考286用のSVG図（骨組みワイヤーフレーム）を生成する"""
import os

OUT = os.environ.get("OUT_DIR", "/tmp/svg286")


def project(x, y, z, a, d, ox, oy):
    """斜投影: x右, y奥(右上へ), z上"""
    return ox + x * a + y * d, oy - z * a - y * d


def lattice_svg(nx, ny, nz, a, d, ox, oy):
    """格子骨組みの棒(line)と玉(circle)のSVG要素を返す"""
    pts = [(x, y, z) for x in range(nx + 1)
           for y in range(ny + 1) for z in range(nz + 1)]
    pset = set(pts)
    lines, balls = [], []
    for (x, y, z) in pts:
        for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            if (x + dx, y + dy, z + dz) in pset:
                x1, y1 = project(x, y, z, a, d, ox, oy)
                x2, y2 = project(x + dx, y + dy, z + dz, a, d, ox, oy)
                lines.append(
                    f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                    f'stroke="#333" stroke-width="1.5"/>')
    for (x, y, z) in pts:
        px, py = project(x, y, z, a, d, ox, oy)
        balls.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3" '
                     f'fill="#fff" stroke="#000" stroke-width="1.2"/>')
    return lines + balls


def fig_q1():
    """問1: 横一列 1個・2個・3個の骨組み"""
    a, d = 42, 17
    parts = ['<svg width="620" height="180" viewBox="0 0 620 180">']
    labels = []
    for k, ox in ((1, 40), (2, 190), (3, 400)):
        oy = 130
        parts += lattice_svg(k, 1, 1, a, d, ox, oy)
        cx = ox + (k * a + d) / 2
        labels.append(f'<text x="{cx:.0f}" y="168" font-size="14" '
                      f'text-anchor="middle">第{k}番目</text>')
    parts += labels
    parts.append('</svg>')
    return "\n".join(parts)


def fig_q2():
    """問2: n×n×n 格子 n=1,2,3"""
    parts = ['<svg width="620" height="220" viewBox="0 0 620 220">']
    labels = []
    for n, ox, a, d in ((1, 45, 40, 16), (2, 175, 34, 13), (3, 390, 30, 12)):
        oy = 165
        parts += lattice_svg(n, n, n, a, d, ox, oy)
        cx = ox + (n * a + n * d) / 2
        labels.append(f'<text x="{cx:.0f}" y="205" font-size="14" '
                      f'text-anchor="middle">第{n}番目</text>')
    parts += labels
    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, svg in (("q1.svg", fig_q1()), ("q2.svg", fig_q2())):
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)
        print(name, "OK,", svg.count("<line"), "本 /", svg.count("<circle"), "玉")
