"""
generate_81.py - 航大思考81のSVGコンテンツを生成するヘルパー
"""

CELL = 36  # セルサイズ

def shape_svg(symbol, cx, cy):
    """記号のSVGを生成"""
    if symbol is None:
        return ""
    r = 10
    s = 12
    t = 13
    d = 15
    shapes = {
        '●': f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="black"/>',
        '○': f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="black" stroke-width="2"/>',
        '□': f'<rect x="{cx-s}" y="{cy-s}" width="{2*s}" height="{2*s}" fill="none" stroke="black" stroke-width="2"/>',
        '■': f'<rect x="{cx-s}" y="{cy-s}" width="{2*s}" height="{2*s}" fill="black"/>',
        '△': f'<polygon points="{cx},{cy-t} {cx-t},{cy+t} {cx+t},{cy+t}" fill="none" stroke="black" stroke-width="2"/>',
        '▲': f'<polygon points="{cx},{cy-t} {cx-t},{cy+t} {cx+t},{cy+t}" fill="black"/>',
        '▼': f'<polygon points="{cx},{cy+t} {cx-t},{cy-t} {cx+t},{cy-t}" fill="black"/>',
        '◇': f'<polygon points="{cx},{cy-d} {cx+d},{cy} {cx},{cy+d} {cx-d},{cy}" fill="none" stroke="black" stroke-width="2"/>',
    }
    return shapes.get(symbol, "")

def grid_svg(grid, ox, oy, label=None):
    """3x3グリッドのSVGを生成"""
    lines = []
    gw = CELL * 3

    # ラベル
    if label:
        lines.append(f'<text x="{ox + gw//2}" y="{oy - 5}" text-anchor="middle" class="svg-text" font-size="14">{label}</text>')

    # グリッド枠
    lines.append(f'<rect x="{ox}" y="{oy}" width="{gw}" height="{gw}" fill="none" stroke="black" stroke-width="2"/>')

    # 内部線
    for i in range(1, 3):
        lines.append(f'<line x1="{ox + i*CELL}" y1="{oy}" x2="{ox + i*CELL}" y2="{oy + gw}" stroke="black" stroke-width="1"/>')
        lines.append(f'<line x1="{ox}" y1="{oy + i*CELL}" x2="{ox + gw}" y2="{oy + i*CELL}" stroke="black" stroke-width="1"/>')

    # 記号
    for r in range(3):
        for c in range(3):
            if grid[r][c]:
                cx = ox + c * CELL + CELL // 2
                cy = oy + r * CELL + CELL // 2
                lines.append(shape_svg(grid[r][c], cx, cy))

    return '\n'.join(lines)


# 問1のデータ
# 例示用シート
ex_sheet1 = [
    ['○', None, None],
    [None, '□', None],
    [None, None, None],
]
ex_sheet2 = [
    [None, None, '▲'],
    [None, None, None],
    [None, '●', None],
]
ex_overlay = [
    ['○', None, '▲'],
    [None, '□', None],
    [None, '●', None],
]

# 問1シート
sheets_q1 = {
    'ア': [['●', None, None], [None, '○', None], [None, None, '●']],
    'イ': [[None, '□', None], ['◇', None, None], ['△', None, None]],
    'ウ': [[None, None, '▲'], [None, None, '■'], [None, '▼', None]],
    'エ': [[None, None, '▲'], [None, '○', None], ['△', None, None]],
    'オ': [['●', '□', None], [None, None, '■'], [None, '▼', None]],
}
target_q1 = [['●', '□', '▲'], ['◇', '○', '■'], ['△', '▼', '●']]

# 問2のデータ
# 例示用（回転の説明）
ex2_sheet1 = [
    ['○', None, None],
    [None, '□', None],
    [None, None, None],
]
# Sheet2 original
ex2_sheet2_orig = [
    [None, None, '▲'],
    [None, None, None],
    [None, '●', None],
]
# Sheet2 rotated 90° CW
ex2_sheet2_rot = [
    [None, None, None],
    ['●', None, None],
    [None, None, '▲'],
]
# Overlay with original
ex2_overlay_orig = [
    ['○', None, '▲'],
    [None, '□', None],
    [None, '●', None],
]
# Overlay with rotated
ex2_overlay_rot = [
    ['○', None, None],
    ['●', '□', None],
    [None, None, '▲'],
]

sheets_q2 = {
    'ア': [['■', None, None], [None, None, '○'], [None, None, None]],
    'イ': [[None, None, None], ['▲', None, None], [None, None, '●']],
    'ウ': [[None, None, '◇'], ['△', None, None], [None, '□', None]],
    'エ': [[None, '▲', None], [None, None, None], ['●', None, '◇']],
    'オ': [['■', None, '◇'], [None, None, None], [None, '□', None]],
}
target_q2 = [['■', '▲', '◇'], ['△', None, '○'], ['●', '□', None]]


def gen_example_svg_q1():
    """問1の例示SVG（シート1 + シート2 → 重ね合わせ結果）"""
    w = 500
    h = 140
    svg = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
    svg += grid_svg(ex_sheet1, 10, 25, "シート1") + '\n'
    svg += f'<text x="140" y="75" class="svg-text" font-size="20" text-anchor="middle">+</text>\n'
    svg += grid_svg(ex_sheet2, 160, 25, "シート2") + '\n'
    svg += f'<text x="295" y="75" class="svg-text" font-size="20" text-anchor="middle">=</text>\n'
    svg += grid_svg(ex_overlay, 320, 25, "重ね合わせ") + '\n'
    svg += '</svg>'
    return svg


def gen_sheets_svg(sheets, label_list=None):
    """5枚のシートを横並びで表示するSVG"""
    if label_list is None:
        label_list = list(sheets.keys())
    w = 620
    h = 140
    svg = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
    for i, name in enumerate(label_list):
        ox = i * 124 + 5
        svg += grid_svg(sheets[name], ox, 25, name) + '\n'
    svg += '</svg>'
    return svg


def gen_target_svg(target, label="目標パターン"):
    """目標パターンのSVG"""
    w = 200
    h = 150
    svg = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
    svg += grid_svg(target, 45, 25, label) + '\n'
    svg += '</svg>'
    return svg


def gen_example_svg_q2():
    """問2の例示SVG（回転の説明）"""
    # Part 1: シート1 + シート2(回転なし) = 結果1
    w = 600
    h = 320
    svg = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'

    # Row 1: 回転なしの重ね合わせ
    svg += grid_svg(ex2_sheet1, 10, 25, "シート1") + '\n'
    svg += f'<text x="140" y="75" class="svg-text" font-size="20" text-anchor="middle">+</text>\n'
    svg += grid_svg(ex2_sheet2_orig, 160, 25, "シート2") + '\n'
    svg += f'<text x="295" y="75" class="svg-text" font-size="20" text-anchor="middle">=</text>\n'
    svg += grid_svg(ex2_overlay_orig, 320, 25, "図1") + '\n'

    # Row 2: 回転ありの重ね合わせ
    svg += grid_svg(ex2_sheet1, 10, 185, "シート1") + '\n'
    svg += f'<text x="140" y="235" class="svg-text" font-size="20" text-anchor="middle">+</text>\n'
    svg += grid_svg(ex2_sheet2_rot, 160, 185, "シート2(90°回転)") + '\n'
    svg += f'<text x="295" y="235" class="svg-text" font-size="20" text-anchor="middle">=</text>\n'
    svg += grid_svg(ex2_overlay_rot, 320, 185, "図2") + '\n'

    svg += '</svg>'
    return svg


if __name__ == '__main__':
    print("=== 問1 例示SVG ===")
    print(gen_example_svg_q1())
    print()
    print("=== 問1 シートSVG ===")
    print(gen_sheets_svg(sheets_q1))
    print()
    print("=== 問1 目標SVG ===")
    print(gen_target_svg(target_q1))
    print()
    print("=== 問2 例示SVG ===")
    print(gen_example_svg_q2())
    print()
    print("=== 問2 シートSVG ===")
    print(gen_sheets_svg(sheets_q2))
    print()
    print("=== 問2 目標SVG ===")
    print(gen_target_svg(target_q2))
