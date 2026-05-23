"""
航大思考183: 箱ひげ図SVG生成
"""

# 問1の表示位置 → (min, Q1, med, Q3, max)
Q1_BOXES = {
    1: (25, 45, 60, 75, 85),   # E
    2: (5, 15, 30, 50, 70),    # A
    3: (15, 35, 50, 70, 85),   # C ← 正解
    4: (10, 20, 45, 65, 90),   # B
    5: (20, 40, 55, 60, 80),   # D
}

# 問2の表示位置 → (min, Q1, med, Q3, max)
Q2_BOXES = {
    1: (20, 35, 50, 65, 90),   # C ← 正解
    2: (10, 20, 35, 55, 70),   # A
    3: (25, 40, 55, 75, 95),   # E
    4: (15, 25, 40, 60, 80),   # B
    5: (5, 30, 45, 70, 85),    # D
}


def gen_boxplot_svg(boxes):
    """5つの箱ひげ図を縦に並べたSVGを生成

    SVG: 600x340, viewBox 0 0 600 340
    X軸: 値 0..100 を SVG x 80..560 にマッピング (4.8px/unit)
    5つの箱ひげ図を y = 30, 80, 130, 180, 230 に配置
    X軸は y=280
    """
    W, H = 600, 340
    LEFT, RIGHT = 80, 560
    AXIS_Y = 280

    def x_of(v):
        return LEFT + v * (RIGHT - LEFT) / 100.0

    parts = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']

    # 縦グリッド線（薄い）
    for v in range(0, 101, 10):
        x = x_of(v)
        parts.append(f'<line x1="{x:.1f}" y1="10" x2="{x:.1f}" y2="{AXIS_Y}" stroke="#e0e0e0" stroke-width="1"/>')

    # 各箱ひげ図
    y_positions = [30, 80, 130, 180, 230]
    for i, pos in enumerate([1, 2, 3, 4, 5]):
        y_center = y_positions[i]
        y_top = y_center - 18
        y_bot = y_center + 18
        cap_top = y_center - 10
        cap_bot = y_center + 10

        mn, q1, med, q3, mx = boxes[pos]
        x_min = x_of(mn)
        x_q1 = x_of(q1)
        x_med = x_of(med)
        x_q3 = x_of(q3)
        x_max = x_of(mx)

        # ラベル「(N)」
        parts.append(f'<text x="40" y="{y_center+5}" class="svg-text" text-anchor="middle" font-weight="bold">({pos})</text>')

        # 左ひげ（min から Q1）
        parts.append(f'<line x1="{x_min:.1f}" y1="{y_center}" x2="{x_q1:.1f}" y2="{y_center}" stroke="black" stroke-width="2"/>')
        # 右ひげ（Q3 から max）
        parts.append(f'<line x1="{x_q3:.1f}" y1="{y_center}" x2="{x_max:.1f}" y2="{y_center}" stroke="black" stroke-width="2"/>')
        # 左端キャップ
        parts.append(f'<line x1="{x_min:.1f}" y1="{cap_top}" x2="{x_min:.1f}" y2="{cap_bot}" stroke="black" stroke-width="2"/>')
        # 右端キャップ
        parts.append(f'<line x1="{x_max:.1f}" y1="{cap_top}" x2="{x_max:.1f}" y2="{cap_bot}" stroke="black" stroke-width="2"/>')
        # 箱（Q1 〜 Q3）
        box_w = x_q3 - x_q1
        parts.append(f'<rect x="{x_q1:.1f}" y="{y_top}" width="{box_w:.1f}" height="{y_bot-y_top}" fill="white" stroke="black" stroke-width="2"/>')
        # 中央値線
        parts.append(f'<line x1="{x_med:.1f}" y1="{y_top}" x2="{x_med:.1f}" y2="{y_bot}" stroke="black" stroke-width="3"/>')

    # X軸（メイン横線）
    parts.append(f'<line x1="{LEFT}" y1="{AXIS_Y}" x2="{RIGHT}" y2="{AXIS_Y}" stroke="black" stroke-width="2"/>')

    # X軸目盛りとラベル
    for v in range(0, 101, 10):
        x = x_of(v)
        parts.append(f'<line x1="{x:.1f}" y1="{AXIS_Y}" x2="{x:.1f}" y2="{AXIS_Y+6}" stroke="black" stroke-width="1.5"/>')
        parts.append(f'<text x="{x:.1f}" y="{AXIS_Y+22}" class="svg-text" text-anchor="middle">{v}</text>')

    # 軸ラベル「点数」
    parts.append(f'<text x="{(LEFT+RIGHT)/2}" y="{AXIS_Y+45}" class="svg-text" text-anchor="middle">点数</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


if __name__ == "__main__":
    print("===== 問1 SVG =====")
    print(gen_boxplot_svg(Q1_BOXES))
    print()
    print("===== 問2 SVG =====")
    print(gen_boxplot_svg(Q2_BOXES))
