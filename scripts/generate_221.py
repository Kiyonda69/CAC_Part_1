# -*- coding: utf-8 -*-
"""
航大思考221 生成スクリプト
verify_221.py で一意性を確認済みの立体から、
- 三面図（正面/側面/平面）の図
- 各選択肢の等角投影（アイソメ）図
を生成し、印刷用/航大思考用の2つのHTMLを 220 をテンプレートに組み立てる。
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_221 import (front_view, side_view, top_view,
                        correct1, options1, W1, D1, H1,
                        correct2, options2, W2, D2, H2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===== 等角投影パラメータ =====
U, V, Hh, PAD = 18, 9, 20, 12

def proj(x, y, z, W, D, H):
    sx = (x - y) * U
    sy = (x + y) * V - z * Hh
    # 全体グリッド(0..W,0..D,0..H)の最小値が PAD になるよう平行移動
    return (sx + D * U + PAD, sy + H * Hh + PAD)

def iso_viewbox(W, D, H):
    w = (W + D) * U + 2 * PAD
    h = (W + D) * V + H * Hh + 2 * PAD
    return w, h

def cube_faces(cx, cy, cz, W, D, H):
    """1つの立方体の可視3面(上/左+y/右+x)のpolygon points文字列を返す"""
    def pt(x, y, z):
        a, b = proj(x, y, z, W, D, H)
        return f"{a:.1f},{b:.1f}"
    top = " ".join([pt(cx,cy,cz+1), pt(cx+1,cy,cz+1), pt(cx+1,cy+1,cz+1), pt(cx,cy+1,cz+1)])
    right = " ".join([pt(cx+1,cy,cz), pt(cx+1,cy+1,cz), pt(cx+1,cy+1,cz+1), pt(cx+1,cy,cz+1)])
    left = " ".join([pt(cx,cy+1,cz), pt(cx+1,cy+1,cz), pt(cx+1,cy+1,cz+1), pt(cx,cy+1,cz+1)])
    return top, left, right

def iso_svg_inner(cubes, W, D, H, indent="    "):
    """立体のアイソメ図(svgの中身)を生成。奥→手前(x+y+z昇順)に描画"""
    lines = []
    for (cx, cy, cz) in sorted(cubes, key=lambda c: (c[0]+c[1]+c[2], c[1], c[0])):
        top, left, right = cube_faces(cx, cy, cz, W, D, H)
        lines.append(f'{indent}<polygon points="{right}" fill="#808080" stroke="#222" stroke-width="1"/>')
        lines.append(f'{indent}<polygon points="{left}" fill="#b8b8b8" stroke="#222" stroke-width="1"/>')
        lines.append(f'{indent}<polygon points="{top}" fill="#ffffff" stroke="#222" stroke-width="1"/>')
    return "\n".join(lines)

# ===== 三面図グリッド =====
CELL = 24

def grid_svg_inner(cells, cols, rows, ox, oy):
    """cells: {(c,r)} 埋まるマス。r=0が下。ox,oyは左上原点。"""
    out = []
    for r in range(rows):
        for c in range(cols):
            x = ox + c * CELL
            y = oy + (rows - 1 - r) * CELL  # r=0 を下に
            fill = "#444" if (c, r) in cells else "#ffffff"
            out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                       f'fill="{fill}" stroke="#222" stroke-width="1"/>')
    return "\n".join("                        " + s for s in out)


# ===== 凡例（アイソメ図の軸方向）=====
def axis_legend_inner(x0, y0):
    """原点(x0,y0)から 幅(右下)/奥行(左下)/高さ(上) の矢印"""
    def arrow(dx, dy, label, lx, ly):
        return (f'<line x1="{x0}" y1="{y0}" x2="{x0+dx}" y2="{y0+dy}" '
                f'stroke="#222" stroke-width="1.5" marker-end="url(#ar)"/>'
                f'<text x="{x0+lx}" y="{y0+ly}" class="svg-text" '
                f'font-size="12" text-anchor="middle">{label}</text>')
    parts = ['<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" '
             'orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#222"/></marker></defs>']
    parts.append(arrow(36, 18, '幅', 48, 24))
    parts.append(arrow(-36, 18, '奥行', -46, 24))
    parts.append(arrow(0, -40, '高さ', 0, -48))
    return "\n                        " + "\n                        ".join(parts)


def views_figure_inner(specs, legend_xy):
    """specs: [(cells, cols, rows, title, xcap, ox), ...] を1つのsvgに配置"""
    out = []
    oy = 56
    for cells, cols, rows, title, xcap, ox in specs:
        cx = ox + cols * CELL / 2
        out.append(f'                        <text x="{cx:.0f}" y="40" class="svg-text" '
                   f'font-weight="bold" text-anchor="middle">{title}</text>')
        out.append(grid_svg_inner(cells, cols, rows, ox, oy))
        cy = oy + rows * CELL + 18
        out.append(f'                        <text x="{cx:.0f}" y="{cy:.0f}" class="svg-text" '
                   f'font-size="12" text-anchor="middle">{xcap}</text>')
    out.append(axis_legend_inner(*legend_xy))
    return "\n".join(out)


def options_dynamic(qnum, options, W, D, H, correct):
    """航大思考用の図形選択肢ブロック"""
    vw, vh = iso_viewbox(W, D, H)
    blocks = []
    for i, sol in enumerate(options, 1):
        inner = iso_svg_inner(sol, W, D, H, indent="                        ")
        blocks.append(
            f'                <button class="option-figure-button" data-option="{i}" '
            f'onclick="selectAnswer({qnum}, {i}, {correct})">\n'
            f'                    <svg width="{vw}" height="{vh+22}" viewBox="0 0 {vw} {vh+22}">\n'
            f'                        <text x="{vw/2:.0f}" y="16" class="svg-text" '
            f'text-anchor="middle">({i})</text>\n'
            f'                        <g transform="translate(0,22)">\n{inner}\n'
            f'                        </g>\n'
            f'                    </svg>\n'
            f'                </button>')
    return ('            <div class="options-figure" id="q%d-options">\n' % qnum
            + "\n\n".join(blocks) + '\n            </div>')


def options_static(options, W, D, H):
    """印刷用の選択肢(1つのsvgに5個横並び)"""
    vw, vh = iso_viewbox(W, D, H)
    step = vw + 12
    total_w = step * 5
    parts = []
    for i, sol in enumerate(options, 1):
        inner = iso_svg_inner(sol, W, D, H, indent="                                ")
        tx = (i - 1) * step
        parts.append(
            f'                            <g transform="translate({tx:.0f},22)">\n'
            f'                                <text x="{vw/2:.0f}" y="-6" class="svg-text" '
            f'text-anchor="middle">({i})</text>\n{inner}\n'
            f'                            </g>')
    return (f'                        <svg width="{total_w:.0f}" height="{vh+30}" '
            f'viewBox="0 0 {total_w:.0f} {vh+30}">\n' + "\n".join(parts)
            + '\n                        </svg>')


# ===== 本文・解説 =====
Q1_TEXT = ('ある立体は、同じ大きさの立方体のブロックをすき間なく積み重ねて作られている。'
           '下の【図1】は、この立体を<strong>正面・側面・真上</strong>の3方向から見たときの形'
           '（正投影図）である。塗りつぶしたマスがブロックのある位置を表す。'
           '右の凡例のとおり、<strong>幅は右方向・奥行きは左奥方向・高さは上方向</strong>とする。'
           'この三面図のすべてに一致する立体を、下の(1)〜(5)から1つ選べ。')

Q2_TEXT = ('問1と同じ要領で、立方体のブロックを積み重ねて作られた立体を考える。'
           '下の【図2】は、この立体を<strong>正面・側面・真上</strong>の3方向から見た正投影図である。'
           '軸の向きは問1の凡例と同じとする。'
           'この三面図のすべてに一致する立体を、下の(1)〜(5)から1つ選べ。')

Q1_EXP = [
    '三面図は次のように読む。<strong>平面図</strong>は真上から見た形で、ブロックが置かれている「幅×奥行き」の位置を表す。<strong>正面図</strong>は各「幅」位置での最も高い積み上げ（高さの輪郭）を、<strong>側面図</strong>は各「奥行き」位置での最も高い積み上げを表す。',
    '与えられた三面図を満たすには、(a)平面図どおりの位置にだけブロックがあり、(b)左端(幅0)が2段・他は1段という正面図、(c)手前(奥行0)が2段・奥は1段という側面図、をすべて満たす必要がある。これらをすべて満たすのは<strong>(3)</strong>だけである。',
    '<strong>【各選択肢の検討】</strong>',
    '・(1) 2段の柱が右端にある。正面図が「右が高い」形になり、左端が高い与図と一致しない。',
    '・(2) 2段の柱が奥にある。側面図が「奥が高い」形になり、手前が高い与図と一致しない。',
    '・(3) 平面図・正面図・側面図のすべてに一致する。正解。',
    '・(4) 底面の欠け（ブロックの無い位置）が奥の左側にある。平面図が与図と一致しない。',
    '・(5) 手前側の2本が2段になっている。正面図の左2列が高くなり、与図と一致しない。',
    'したがって、正解は<strong>(3)</strong>である。',
]

Q2_EXP = [
    '問1と同様に、平面図でブロックの位置（幅×奥行き）を、正面図・側面図でそれぞれの方向から見た高さの輪郭を読み取る。',
    'この立体は、奥の列に幅3のブロック列があり、中央の列だけが手前へ2マス伸びるT字の土台をもつ。中央奥が最も高い3段の塔で、その手前が2段、最も手前が1段に下がっていく。これらの条件をすべて満たすのは<strong>(1)</strong>だけである。',
    '<strong>【各選択肢の検討】</strong>',
    '・(1) 平面図・正面図・側面図のすべてに一致する。正解。',
    '・(2) 土台に余分なブロックが1つ加わっており、平面図の形が与図と一致しない。',
    '・(3) 右奥の積みが3段になっており、正面図の右端が高くなって与図と一致しない。',
    '・(4) 中央手前の積みが1段不足し、側面図の中央の高さが足りず与図と一致しない。',
    '・(5) 最も手前の左側に余分なブロックがあり、平面図の形が与図と一致しない。',
    'したがって、正解は<strong>(1)</strong>である。',
]


def build_figure(fig_no, title, vbw, vbh, inner):
    return (f'            <div class="figure-container">\n'
            f'                <div class="figure-title">【図{fig_no}】この立体の三面図（正投影図）と軸の凡例</div>\n'
            f'                <div class="figure-content">\n'
            f'                    <svg width="{vbw}" height="{vbh}" viewBox="0 0 {vbw} {vbh}">\n'
            f'{inner}\n'
            f'                    </svg>\n'
            f'                </div>\n'
            f'            </div>')

def q1_specs():
    f = front_view(correct1, W1, H1); s = side_view(correct1, D1, H1); t = top_view(correct1, W1, D1)
    return [(f,3,2,'正面図','横=幅 / 縦=高さ',40),
            (s,2,2,'側面図','横=奥行き(左が手前)',190),
            (t,3,2,'平面図','上が奥',300)], (515,118)

def q2_specs():
    f = front_view(correct2, W2, H2); s = side_view(correct2, D2, H2); t = top_view(correct2, W2, D2)
    return [(f,3,3,'正面図','横=幅 / 縦=高さ',40),
            (s,3,3,'側面図','横=奥行き(左が手前)',210),
            (t,3,3,'平面図','上が奥',380)], (565,128)

def exp_to_dynamic(lines):
    return "\n".join(f'                    <p>{ln}</p>' if not ln.startswith('<strong>【')
                     else f'                    <br>\n                    <p>{ln}</p>' for ln in lines)

def exp_to_static(lines):
    out = []
    for ln in lines:
        out.append(ln + '<br>')
    return "\n                ".join(out)

# ---- 動的(航大思考)画面 ----
def dynamic_screen(qnum, meta, text, fig, options_block, exp_lines, correct, nav):
    return (f'        <div class="screen{" active" if qnum==1 else ""}" id="q{qnum}-question">\n'
            f'            <div class="question-header">\n'
            f'                <span class="question-number">問{qnum}</span>\n'
            f'                <span class="question-meta">{meta}</span>\n'
            f'            </div>\n\n'
            f'            <div class="question-text">\n                {text}\n            </div>\n\n'
            f'{fig}\n\n'
            f'{options_block}\n\n'
            f'            <div class="explanation-section" id="q{qnum}-explanation">\n'
            f'                <div class="explanation-header">問{qnum}（正解: ({correct})）</div>\n'
            f'                <div class="explanation-content">\n'
            f'{exp_to_dynamic(exp_lines)}\n'
            f'                </div>\n            </div>\n\n'
            f'            <div class="nav-buttons" id="q{qnum}-nav" style="display: none;">\n{nav}\n'
            f'            </div>\n        </div>')

# ---- 静的(印刷)ページ ----
def static_q_page(qnum, text, fig, options_block):
    return (f'    <div class="question-section question-page">\n        <div class="page-content">\n'
            f'            <div class="question">\n'
            f'                <div class="question-number">問{qnum}．{text}（6点）</div>\n\n'
            f'{fig}\n\n'
            f'                <div class="figure-container" style="border: none; box-shadow: none;">\n'
            f'                    <div class="figure-content">\n'
            f'{options_block}\n'
            f'                    </div>\n                </div>\n'
            f'            </div>\n        </div>\n    </div>')

def static_exp_page(qnum, correct, exp_lines):
    return (f'    <div class="question-section question-page">\n        <div class="page-content">\n'
            f'            <div class="explanation">\n'
            f'                <strong>問{qnum}(正解:({correct}))</strong><br>\n'
            f'                {exp_to_static(exp_lines)}\n'
            f'            </div>\n        </div>\n    </div>')


def main():
    # 図(三面図)生成
    s1, lx1 = q1_specs(); s2, lx2 = q2_specs()
    fig1 = build_figure(1, '', 600, 165, views_figure_inner(s1, lx1))
    fig2 = build_figure(2, '', 640, 180, views_figure_inner(s2, lx2))

    # ===== 航大思考(動的) =====
    opt1d = options_dynamic(1, options1, W1, D1, H1, 3)
    opt2d = options_dynamic(2, options2, W2, D2, H2, 1)
    nav1 = ('                <button class="btn btn-secondary hidden">前の問題</button>\n'
            '                <button class="btn btn-primary" onclick="goToQuestion(2)">問2へ</button>')
    nav2 = ('                <button class="btn btn-secondary" onclick="goToQuestion(1)">問1へ</button>\n'
            '                <button class="btn btn-secondary hidden">（空欄）</button>')
    scr1 = dynamic_screen(1, '配点: 6点 / 目安時間: 3分', Q1_TEXT, fig1, opt1d, Q1_EXP, 3, nav1)
    scr2 = dynamic_screen(2, '配点: 6点 / 目安時間: 5分', Q2_TEXT, fig2, opt2d, Q2_EXP, 1, nav2)
    screens = scr1 + '\n\n' + scr2 + '\n    </main>'

    src = open(os.path.join(ROOT, '航大思考問題/航大思考220.html'), encoding='utf-8').read()
    mk = '        <!-- ========== 問1 問題画面 ========== -->'
    head = src[:src.index(mk)]
    footer = src[src.index('    </main>'):]
    footer = footer.replace('航大思考220', '航大思考221')
    out_dyn = head + screens.split('\n    </main>')[0] + '\n' + footer
    open(os.path.join(ROOT, '航大思考問題/航大思考221.html'), 'w', encoding='utf-8').write(out_dyn)

    # ===== 印刷(静的) =====
    opt1s = options_static(options1, W1, D1, H1)
    opt2s = options_static(options2, W2, D2, H2)
    sfig1 = build_figure(1, '', 600, 165, views_figure_inner(s1, lx1))
    sfig2 = build_figure(2, '', 640, 180, views_figure_inner(s2, lx2))
    pages = "\n\n".join([
        static_q_page(1, Q1_TEXT, sfig1, opt1s),
        static_exp_page(1, 3, Q1_EXP),
        static_q_page(2, Q2_TEXT, sfig2, opt2s),
        static_exp_page(2, 1, Q2_EXP),
    ])
    ssrc = open(os.path.join(ROOT, '印刷用/印刷220.html'), encoding='utf-8').read()
    smk = '    <div class="question-section question-page">'
    shead = ssrc[:ssrc.index(smk)]
    sfoot = ssrc[ssrc.index('    <!-- ==================== JavaScript ==================== -->'):]
    out_sta = shead + pages + '\n\n' + sfoot
    open(os.path.join(ROOT, '印刷用/印刷221.html'), 'w', encoding='utf-8').write(out_sta)
    print('生成完了: 航大思考221.html / 印刷221.html')

if __name__ == '__main__':
    main()
