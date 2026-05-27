# -*- coding: utf-8 -*-
"""航大思考191 HTML組み立て(印刷用/航大思考用)。gen_191.py から呼ばれる。"""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Q1_TEXT = ("次の(1)〜(5)は立体の見取り図で、実線・点線はすべてその立体の辺を表し、"
           "黒点は頂点を表す。これらの立体について、すべての辺を一筆書きで"
           "（同じ辺を二度なぞらず、ペンを紙から離さずに）たどれるものはどれか。"
           "正しいものを1つ選べ。")
Q2_TEXT = ("下の図は、直方体の上に三角の屋根をのせた家のような立体の見取り図で、"
           "実線・点線はすべて辺を表し、黒点は頂点を表す。この立体のすべての辺を、"
           "同じ辺を二度なぞらずに書きたい。途中でペンを紙から離してもよいとき、"
           "すべての辺を書き終えるのに必要な筆数は最小で何筆か。点線も辺として数える。"
           "正しいものを1つ選べ。")

Q1_EXP = """<strong>問1(正解:(4))</strong><br>
一筆書きの定理: 連結な図形は、奇数本の辺が集まる頂点（奇点）の数が
<strong>0個または2個</strong>のときに限り一筆書きできる。<br>
各立体で、頂点に集まる辺の数（次数）を数えて奇点の個数を調べる。<br><br>

<strong>【各立体の検討】</strong><br>
・(1) 正四面体: 4頂点すべてが次数3 → 奇点4個 → 一筆書き不可<br>
・(2) 立方体: 8頂点すべてが次数3 → 奇点8個 → 一筆書き不可<br>
・(3) 三角柱: 6頂点すべてが次数3 → 奇点6個 → 一筆書き不可<br>
・(4) 三角双錐: 上下の頂点が次数3（奇点）、赤道の3頂点が次数4（偶点） → 奇点2個 → 一筆書き可<br>
・(5) 四角錐: 頂点が次数4、底面の4頂点が次数3 → 奇点4個 → 一筆書き不可<br><br>

奇点が0個か2個なのは(4)だけである。したがって、正解は<strong>(4)</strong>である。"""

Q2_EXP = """<strong>問2(正解:(3))</strong><br>
最小筆数の定理: 連結な図形の全ての辺を書くのに必要な最小の筆数は、
奇数本の辺が集まる頂点（奇点）の数を2で割った値に等しい
（奇点が0個のときは1筆）。各頂点の次数を数えて奇点の個数を調べる。<br><br>

<strong>【各頂点の次数】</strong><br>
・底面の4頂点: 底面の辺2本＋柱1本 ＝ 次数3（奇点）<br>
・天井（壁の上）の4頂点: 天井の辺2本＋柱1本＋屋根の辺1本 ＝ 次数4（偶点）<br>
・屋根の棟の2頂点: 妻面の辺2本＋棟1本 ＝ 次数3（奇点）<br><br>

奇点は底面の4頂点と棟の2頂点の合計<strong>6個</strong>。よって最小筆数 ＝ 6÷2 ＝ <strong>3筆</strong>。<br><br>

<strong>【選択肢の検討】</strong><br>
・(1) 1筆: 奇点が0個か2個のときのみ可能。本図は奇点6個なので誤り<br>
・(2) 2筆: 奇点4個に相当。屋根の棟（次数3の奇点）を見落とした誤り<br>
・(3) 3筆: 奇点6個÷2＝3筆。正しい<br>
・(4) 4筆: 屋根を無視して直方体（奇点8個）とみなした誤り<br>
・(5) 5筆: 数えすぎ<br><br>

したがって、正解は<strong>(3)</strong>である。"""


def static_choice_svg(order, solid_lines):
    """印刷用: 5立体を横並びにしたSVG文字列(各立体をセルいっぱいに拡大)。"""
    cw = 132            # 1セル幅
    groups = []
    for i, name in enumerate(order):
        base = i * cw
        rect = (base + 12, 36, base + cw - 12, 208)
        body = solid_lines(name, rect)
        groups.append(
            f'    <g>\n'
            f'        <text x="{base + cw // 2}" y="22" class="svg-text" '
            f'style="font-size:18px" text-anchor="middle">({i+1})</text>\n'
            f'        {body}\n'
            f'    </g>')
    inner = "\n".join(groups)
    total = cw * len(order)
    return (f'<svg width="100%" height="auto" viewBox="0 0 {total} 220">\n{inner}\n</svg>')


def static_question_section(num, text, points_time, choice_svg):
    return f"""    <div class="question-section question-page">
        <div class="page-content">
            <div class="question">
                <div class="question-number">問{num}．{text}（{points_time}）</div>
                <div class="figure-container" style="border: none; box-shadow: none;">
                    <div class="figure-content">
                        {choice_svg}
                    </div>
                </div>
            </div>
        </div>
    </div>
"""


def static_explanation_section(exp_html):
    return f"""    <div class="question-section question-page">
        <div class="page-content">
            <div class="explanation">
                {exp_html}
            </div>
        </div>
    </div>
"""


STROKE_OPTS = ["1筆", "2筆", "3筆", "4筆", "5筆"]


def house_figure_svg(solid_lines):
    """家型立体を1つだけ大きく描いたSVG。"""
    body = solid_lines("切妻屋根の家", (30, 20, 350, 300))
    return f'<svg width="380" height="320" viewBox="0 0 380 320">\n{body}\n</svg>'


def static_minstroke_section(num, text, points_time, figure_svg, opts):
    """印刷用: 1つの図＋テキスト選択肢の問題ページ。"""
    lines = "<br>\n                    ".join(
        f"({i+1}) {o}" for i, o in enumerate(opts))
    return f"""    <div class="question-section question-page">
        <div class="page-content">
            <div class="question">
                <div class="question-number">問{num}．{text}（{points_time}）</div>
                <div class="figure-container">
                    <div class="figure-content">
                        {figure_svg}
                    </div>
                </div>
                <div class="options">
                    {lines}
                </div>
            </div>
        </div>
    </div>
"""


def build_static(g):
    solid_lines = g["solid_lines"]
    q1c = static_choice_svg(g["Q1_ORDER"], solid_lines)
    house = house_figure_svg(solid_lines)
    with open(os.path.join(BASE, "template_static.html"), encoding="utf-8") as f:
        t = f.read()
    head = t[: t.index("<body>") + len("<body>")]
    footer = t[t.index("    <!-- ==================== JavaScript"):]
    body = "\n".join([
        static_question_section(1, Q1_TEXT, "6点", q1c),
        static_explanation_section(Q1_EXP),
        static_minstroke_section(2, Q2_TEXT, "6点", house, STROKE_OPTS),
        static_explanation_section(Q2_EXP),
    ])
    out = head + "\n" + body + "\n" + footer
    path = os.path.join(BASE, "印刷用", "印刷191.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", path)


def dyn_options(qnum, order, correct, solid_lines):
    btns = []
    for i, name in enumerate(order):
        opt = i + 1
        rect = (10, 30, 130, 192)
        body = solid_lines(name, rect)
        btns.append(
            f'                <button class="option-figure-button" data-option="{opt}" '
            f'style="max-width:170px" '
            f'onclick="selectAnswer({qnum}, {opt}, {correct})">\n'
            f'                    <svg width="100%" height="auto" viewBox="0 0 140 200">\n'
            f'                        <text x="70" y="20" class="svg-text" '
            f'style="font-size:18px" text-anchor="middle">({opt})</text>\n'
            f'                        {body}\n'
            f'                    </svg>\n'
            f'                </button>')
    return "\n".join(btns)


def dyn_text_options(qnum, opts, correct):
    btns = []
    for i, o in enumerate(opts):
        n = i + 1
        btns.append(
            f'                <button class="option-button" data-option="{n}" '
            f'onclick="selectAnswer({qnum}, {n}, {correct})">'
            f'<span class="option-label">({n})</span>{o}</button>')
    return "\n".join(btns)


def dyn_house_content(qnum, house_svg, opts, correct):
    return f"""            <div class="figure-container">
                <div class="figure-title">【図】立体の見取り図</div>
                <div class="figure-content">
                    {house_svg}
                </div>
            </div>
            <div class="options-container" id="q{qnum}-options">
{dyn_text_options(qnum, opts, correct)}
            </div>"""


def dyn_screen(qnum, active, meta, text, content_html, exp_header, exp_content, nav_html):
    cls = "screen active" if active else "screen"
    return f"""        <div class="{cls}" id="q{qnum}-question">
            <div class="question-header">
                <span class="question-number">問{qnum}</span>
                <span class="question-meta">{meta}</span>
            </div>
            <div class="question-text">{text}</div>
{content_html}
            <div class="explanation-section" id="q{qnum}-explanation">
                <div class="explanation-header">{exp_header}</div>
                <div class="explanation-content">
                    {exp_content}
                </div>
            </div>
            <div class="nav-buttons" id="q{qnum}-nav" style="display: none;">
{nav_html}
            </div>
        </div>"""


def build_dynamic(g):
    solid_lines = g["solid_lines"]
    o1 = dyn_options(1, g["Q1_ORDER"], 4, solid_lines)
    c1 = ('            <div class="options-figure" id="q1-options">\n'
          + o1 + '\n            </div>')
    house = house_figure_svg(solid_lines)
    c2 = dyn_house_content(2, house, STROKE_OPTS, 3)
    exp1 = Q1_EXP.split("<br>\n", 1)[1]
    exp2 = Q2_EXP.split("<br>\n", 1)[1]
    nav1 = ('                <button class="btn btn-secondary hidden">前の問題</button>\n'
            '                <button class="btn btn-primary" onclick="goToQuestion(2)">問2へ</button>')
    nav2 = ('                <button class="btn btn-secondary" onclick="goToQuestion(1)">問1へ</button>\n'
            '                <button class="btn btn-secondary hidden">（空欄）</button>')
    s1 = dyn_screen(1, True, "配点: 6点 / 目安時間: 3分", Q1_TEXT, c1,
                    "解説（正解: (4)）", exp1, nav1)
    s2 = dyn_screen(2, False, "配点: 6点 / 目安時間: 5分", Q2_TEXT, c2,
                    "解説（正解: (3)）", exp2, nav2)
    with open(os.path.join(BASE, "template_dynamic.html"), encoding="utf-8") as f:
        t = f.read()
    head = t[: t.index("<body>") + len("<body>")]
    footer = t[t.index("    <!-- ==================== JavaScript"):]
    footer = footer.replace("2026_01/航大思考X/問", "2026_05/航大思考191/問")
    progress = ('        <div class="progress-bar">\n'
                '            <div class="progress-dot" id="progress-1" onclick="goToQuestion(1)">1</div>\n'
                '            <div class="progress-dot" id="progress-2" onclick="goToQuestion(2)">2</div>\n'
                '        </div>')
    main = ('    <main class="main-content">\n' + progress + "\n\n"
            + s1 + "\n\n" + s2 + "\n    </main>\n")
    out = head + "\n" + main + "\n" + footer
    path = os.path.join(BASE, "航大思考問題", "航大思考191.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", path)


def main(g):
    build_static(g)
    build_dynamic(g)
