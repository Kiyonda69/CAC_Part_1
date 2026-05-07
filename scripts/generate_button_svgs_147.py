"""航大思考147 用、ボタン内に入れる単一円 SVG を5つ生成する。"""
import math


def sector_path(cx, cy, r, idx):
    sa = math.radians(-90 + idx * 45)
    ea = math.radians(-90 + (idx + 1) * 45)
    x1, y1 = cx + r * math.cos(sa), cy + r * math.sin(sa)
    x2, y2 = cx + r * math.cos(ea), cy + r * math.sin(ea)
    return f"M {cx:.2f} {cy:.2f} L {x1:.2f} {y1:.2f} A {r:.2f} {r:.2f} 0 0 1 {x2:.2f} {y2:.2f} Z"


def render(filled):
    cx, cy, r = 40, 40, 24
    parts = [f'<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">']
    for i in range(8):
        fill = "#888" if i in filled else "white"
        parts.append(f'    <path d="{sector_path(cx, cy, r, i)}" fill="{fill}" stroke="black" stroke-width="1"/>')
    parts.append(f'    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="black" stroke-width="1.5"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def filled_for(n):
    return [i for i in range(8) if (n >> i) & 1]


if __name__ == "__main__":
    options = [
        (1, filled_for(53)),  # 53 (正解)
        (2, filled_for(51)),  # 51
        (3, filled_for(45)),  # 45
        (4, filled_for(85)),  # 85
        (5, filled_for(54)),  # 54
    ]
    for label, sectors in options:
        val = sum(2**i for i in sectors)
        print(f"\n=== Option ({label}) value={val} sectors={sectors} ===")
        print(render(sectors))
