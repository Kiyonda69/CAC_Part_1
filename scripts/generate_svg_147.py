"""
航大思考147 問2 用 SVG 生成スクリプト

8セクター円の SVG を生成する。
- 各円は8等分されたパイ
- 数値 = 塗りつぶされたセクターの値の合計（バイナリ）
- セクター i は 2^i の値、12時方向から時計回りに配置
"""

import math


def sector_path(cx, cy, r, sector_idx):
    """8セクターのうち、sector_idx 番目のパイ片の SVG path d 属性を返す。"""
    # 12時方向から始めて時計回り
    start_deg = -90 + sector_idx * 45
    end_deg = -90 + (sector_idx + 1) * 45
    sa = math.radians(start_deg)
    ea = math.radians(end_deg)
    x1 = cx + r * math.cos(sa)
    y1 = cy + r * math.sin(sa)
    x2 = cx + r * math.cos(ea)
    y2 = cy + r * math.sin(ea)
    # 45° なので large_arc_flag=0, sweep_flag=1（時計回り）
    return (
        f"M {cx:.2f} {cy:.2f} "
        f"L {x1:.2f} {y1:.2f} "
        f"A {r:.2f} {r:.2f} 0 0 1 {x2:.2f} {y2:.2f} Z"
    )


def render_circle(cx, cy, r, filled_sectors, label=None, label_dy=-10):
    """円1つ分の SVG 要素文字列を返す。"""
    parts = []
    if label is not None:
        parts.append(
            f'<text x="{cx}" y="{cy - r + label_dy}" '
            f'text-anchor="middle" font-size="13" font-family="sans-serif">'
            f"{label}</text>"
        )
    # 全セクター描画
    for i in range(8):
        fill = "#888" if i in filled_sectors else "white"
        parts.append(
            f'<path d="{sector_path(cx, cy, r, i)}" '
            f'fill="{fill}" stroke="black" stroke-width="1"/>'
        )
    # 外円（境界線強調）
    parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" '
        f'fill="none" stroke="black" stroke-width="1.5"/>'
    )
    return "\n        ".join(parts)


def filled_sectors_for(n):
    """数値 n のバイナリ表現から塗るセクターを返す。"""
    return [i for i in range(8) if (n >> i) & 1]


def generate_reference_svg(width=600, height=210, r=24):
    """1〜12 の参照円 SVG（2行 × 6列）を生成。"""
    parts = [f'<svg width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}" '
             f'xmlns="http://www.w3.org/2000/svg">']
    # 6列のx座標
    spacing = 90
    start_x = 60
    row1_y = 60
    row2_y = 150

    for n in range(1, 13):
        if n <= 6:
            cx = start_x + (n - 1) * spacing
            cy = row1_y
        else:
            cx = start_x + (n - 7) * spacing
            cy = row2_y
        parts.append("    " + render_circle(cx, cy, r, filled_sectors_for(n), label=str(n)))

    parts.append("</svg>")
    return "\n".join(parts)


def generate_options_svg(options, width=600, height=110, r=24):
    """選択肢の円 SVG を生成。options は [(label, filled_sectors), ...] のリスト。"""
    parts = [f'<svg width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}" '
             f'xmlns="http://www.w3.org/2000/svg">']
    spacing = 110
    start_x = 70
    cy = 65
    for i, (label, sectors) in enumerate(options):
        cx = start_x + i * spacing
        parts.append("    " + render_circle(cx, cy, r, sectors, label=f"({label})"))
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    # 参照円 (1-12)
    ref_svg = generate_reference_svg()
    # 選択肢
    # 正解: 53 = 0011 0101 → sectors [0, 2, 4, 5]
    options = [
        ("1", filled_sectors_for(53)),  # 53 (正解)
        ("2", filled_sectors_for(51)),  # 51 = 0011 0011 → [0,1,4,5]
        ("3", filled_sectors_for(45)),  # 45 = 0010 1101 → [0,2,3,5]
        ("4", filled_sectors_for(85)),  # 85 = 0101 0101 → [0,2,4,6]
        ("5", filled_sectors_for(54)),  # 54 = 0011 0110 → [1,2,4,5]
    ]
    opt_svg = generate_options_svg(options)

    # 各選択肢の値を確認
    print("選択肢の値検証:")
    for label, sectors in options:
        val = sum(2**i for i in sectors)
        print(f"  ({label}) sectors {sectors} = {val}")

    # 出力
    with open("/tmp/ref_147.svg", "w") as f:
        f.write(ref_svg)
    with open("/tmp/opt_147.svg", "w") as f:
        f.write(opt_svg)
    print("\nSVG生成完了: /tmp/ref_147.svg, /tmp/opt_147.svg")
    print(f"参照SVGサイズ: 600x210")
    print(f"選択肢SVGサイズ: 600x110")
