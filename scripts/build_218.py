# -*- coding: utf-8 -*-
"""航大思考218 HTMLビルド: 印刷用と航大思考用を生成する。

template_static.html / template_dynamic.html の CSS・JS をそのまま使い、
本文（main / body内）だけを差し替える。SVGは gen_svg_218.render で生成。
"""
import os
import gen_svg_218 as g
from verify_218 import (Q1_solid, Q1_options, Q1_correct,
                        Q2_solid, Q2_options, Q2_correct)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main_svg(solid, s, title):
    """主図: 立体 + 右側の鏡（縦線）を描く。"""
    inner, w, h = g.render(solid, s=s, label=title, label_fs=15)
    # 右側に鏡（縦線）を追加。図の右端から少し離して立てる。
    mx = w + 26
    line = ('<line x1="%.1f" y1="18" x2="%.1f" y2="%.1f" stroke="#000" '
            'stroke-width="3"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="14" '
            'font-family="sans-serif" font-weight="bold">鏡</text>'
            % (mx, mx, h - 6, mx + 14, h / 2))
    W = w + 56
    return ('<svg width="%d" height="%d" viewBox="0 0 %d %d">%s%s</svg>'
            % (round(W), round(h), round(W), round(h), inner, line))


def options_grid(options, s, cols=5):
    """印刷用: 5択を1枚のSVGに横並びで配置する。"""
    rendered = [g.render(o, s=s, label="(%d)" % (i + 1))
                for i, o in enumerate(options)]
    colw = max(r[1] for r in rendered) + 8
    rowh = max(r[2] for r in rendered) + 8
    rows = (len(options) + cols - 1) // cols
    W = colw * min(cols, len(options))
    H = rowh * rows
    parts = []
    for i, (inner, w, h) in enumerate(rendered):
        cx = (i % cols) * colw + (colw - w) / 2
        cy = (i // cols) * rowh + (rowh - h) / 2
        parts.append('<g transform="translate(%.1f,%.1f)">%s</g>'
                     % (cx, cy, inner))
    return ('<svg width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>'
            % (round(W), round(H), round(W), round(H), "".join(parts)))


def option_buttons(qnum, options, correct, s):
    """航大思考用: クリック可能な5つのボタンを生成する。"""
    btns = []
    for i, o in enumerate(options, 1):
        inner, w, h = g.render(o, s=s, label="(%d)" % i)
        svg = ('<svg width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>'
               % (round(w), round(h), round(w), round(h), inner))
        btns.append('<button class="option-figure-button" data-option="%d" '
                    'onclick="selectAnswer(%d, %d, %d)">%s</button>'
                    % (i, qnum, i, correct, svg))
    return '<div class="options-figure" id="q%d-options">%s</div>' % (
        qnum, "".join(btns))


# ==================== 本文テキスト ====================
Q1_TEXT = ("【図1】は、いくつかの立方体をすき間なく積み重ねてできた立体を、"
           "右ななめ上の方向から見た見取図である（手前の面・上面・右側面が見えている）。"
           "黒い丸（●）は手前の面につけた目印である。この立体の右側に大きな鏡を"
           "床に対して垂直に立てて映すとき、鏡の中に見える立体の図として最も適切な"
           "ものを、(1)〜(5)から一つ選べ。")

Q2_TEXT = ("【図2】は、立方体を積み重ねてできた立体を右ななめ上から見た見取図である"
           "（上面と右側面が見えている）。手前の面には黒い丸（●）と黒い四角（■）の"
           "2つの目印がつけてある。この立体の右側に鏡を垂直に立てて映すとき、"
           "鏡の中に見える立体の図として正しいものを、(1)〜(5)から一つ選べ。")

Q1_EXP = (
    "鏡を立体の<strong>右側</strong>に垂直に立てると、鏡の中の像は<strong>左右が"
    "反転</strong>する。立体の問題で見落としやすいのは、左右反転と同時に"
    "<strong>見える側面の向き（奥行きの向き）も反転する</strong>点である。"
    "もとの図は奥行きが右上に伸びて<strong>右側面</strong>が見えているが、"
    "鏡の中では奥行きが左上に伸びて<strong>左側面</strong>が見える形になる。<br><br>"
    "もとの立体は「左に高さ3の柱＋下段が右へ伸びるL字」で、目印●は下段の右端にある。"
    "左右反転すると「右に高さ3の柱＋下段が左へ伸びるL字」となり、●は下段の左端へ移る。"
    "さらに側面は左に見えるようになる。これが選択肢<strong>(4)</strong>である。<br><br>"
    "<strong>【選択肢の検討】</strong><br>"
    "・(1) もとの立体のまま。左右が反転していないので誤り。<br>"
    "・(2) 形は左右反転しているが、側面が<strong>右</strong>に見えたまま。"
    "奥行きの反転を忘れた図で、鏡像ではない。<br>"
    "・(3) 上下が反転した図。床（真下）に置いた鏡の像であり、"
    "右側に立てた鏡では起こらない。<br>"
    "・(4) 左右反転し、側面も<strong>左</strong>に見える正しい鏡像。これが正解。<br>"
    "・(5) 180度回転した図。鏡像とは異なる。<br><br>"
    "したがって、正解は<strong>(4)</strong>である。")

Q2_EXP = (
    "問1と同じく、右側の鏡では<strong>左右が反転</strong>し、同時に"
    "<strong>見える側面が右から左へ</strong>変わる。さらにこの問題では、"
    "●と■の<strong>2つの目印の対応</strong>を正しく追う必要がある。<br><br>"
    "もとの立体は「左に高さ3の柱（●は左上）」「右に高さ2の部分（■）」"
    "「下段4マス」である。左右反転すると「右に高さ3の柱（●は右上）」"
    "「左に高さ2の部分（■）」となり、側面は左に見える。これが"
    "選択肢<strong>(3)</strong>と一致する。<br><br>"
    "<strong>【選択肢の検討】</strong><br>"
    "・(1) もとの立体のまま。反転していない。<br>"
    "・(2) 左右反転しているが側面が<strong>右</strong>のまま。奥行きの反転忘れで誤り。<br>"
    "・(3) 左右反転・側面の向き・目印の位置がすべて正しい鏡像。これが正解。<br>"
    "・(4) 形と側面の向きは正しいが、<strong>●と■の位置が入れ替わっている</strong>。"
    "目印の取り違えで誤り。<br>"
    "・(5) 上下が反転した図。右側の鏡では起こらない。<br><br>"
    "目印●・■の位置と側面の向きがすべて一致するのは(3)のみ。"
    "よって正解は<strong>(3)</strong>である。")


# ==================== 動的版（航大思考）組み立て ====================
def build_dynamic():
    fig1 = main_svg(Q1_solid, s=44, title="【図1】立体の見取図と鏡の位置")
    fig2 = main_svg(Q2_solid, s=40, title="【図2】立体の見取図と鏡の位置")
    opt1 = option_buttons(1, Q1_options, Q1_correct, s=30)
    opt2 = option_buttons(2, Q2_options, Q2_correct, s=27)

    def screen(qnum, active, meta, qtext, figtitle, figsvg, opts, exp,
               nav, correct):
        cls = "screen active" if active else "screen"
        return (
            '<div class="%s" id="q%d-question">\n'
            '            <div class="question-header"><span class="question-number">問%d</span>'
            '<span class="question-meta">%s</span></div>\n'
            '            <div class="question-text">%s</div>\n'
            '            <div class="figure-container"><div class="figure-title">%s</div>'
            '<div class="figure-content">%s</div></div>\n'
            '            <div class="figure-title">鏡の中に見える立体の図（クリックで解答）</div>\n'
            '            %s\n'
            '            <div class="explanation-section" id="q%d-explanation">'
            '<div class="explanation-header">問%d（正解: (%d)）</div>'
            '<div class="explanation-content">%s</div></div>\n'
            '            %s\n'
            '        </div>'
            % (cls, qnum, qnum, meta, qtext, figtitle, figsvg, opts,
               qnum, qnum, correct, exp, nav))

    nav1 = ('<div class="nav-buttons" id="q1-nav" style="display: none;">'
            '<button class="btn btn-secondary hidden">前の問題</button>'
            '<button class="btn btn-primary" onclick="goToQuestion(2)">問2へ</button></div>')
    nav2 = ('<div class="nav-buttons" id="q2-nav" style="display: none;">'
            '<button class="btn btn-secondary" onclick="goToQuestion(1)">問1へ</button>'
            '<button class="btn btn-secondary hidden">（空欄）</button></div>')

    s1 = screen(1, True, "配点: 6点 / 目安時間: 3分", Q1_TEXT,
                "【図1】立体の見取図と鏡の位置", fig1, opt1, Q1_EXP, nav1, Q1_correct)
    s2 = screen(2, False, "配点: 6点 / 目安時間: 5分", Q2_TEXT,
                "【図2】立体の見取図と鏡の位置", fig2, opt2, Q2_EXP, nav2, Q2_correct)

    progress = ('<div class="progress-bar">\n'
                '            <div class="progress-dot" id="progress-1" onclick="goToQuestion(1)">1</div>\n'
                '            <div class="progress-dot" id="progress-2" onclick="goToQuestion(2)">2</div>\n'
                '        </div>')
    body = '\n        '.join([progress, s1, s2])

    tpl = open(os.path.join(ROOT, "template_dynamic.html"), encoding="utf-8").read()
    head = tpl.split('<main class="main-content">')[0]
    tail = tpl.split('</main>')[1]
    tail = tail.replace('`2026_01/航大思考X/問${questionNum}`',
                        '`2026_06/航大思考218/問${questionNum}`')
    html = (head + '<main class="main-content">\n        ' + body
            + '\n    </main>' + tail)
    out = os.path.join(ROOT, "航大思考問題", "航大思考218.html")
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, len(html), "bytes")


# ==================== 静的版（印刷用）組み立て ====================
def build_static():
    fig1 = main_svg(Q1_solid, s=44, title="【図1】立体の見取図と鏡の位置")
    fig2 = main_svg(Q2_solid, s=40, title="【図2】立体の見取図と鏡の位置")
    optg1 = options_grid(Q1_options, s=26)
    optg2 = options_grid(Q2_options, s=20)

    def qsec(qnum, qtext, pts, figtitle, figsvg, optsvg):
        return (
            '    <div class="question-section question-page">\n'
            '        <div class="page-content">\n'
            '            <div class="question">\n'
            '                <div class="question-number">問%d．%s（%d点）</div>\n'
            '                <div class="figure-container"><div class="figure-title">%s</div>'
            '<div class="figure-content">%s</div></div>\n'
            '                <div class="figure-container" style="border:none;box-shadow:none;">'
            '<div class="figure-title">【選択肢】鏡の中に見える立体の図</div>'
            '<div class="figure-content">%s</div></div>\n'
            '            </div>\n'
            '        </div>\n'
            '    </div>'
            % (qnum, qtext, pts, figtitle, figsvg, optsvg))

    def expsec(qnum, correct, exp):
        return (
            '    <div class="question-section question-page">\n'
            '        <div class="page-content">\n'
            '            <div class="explanation">\n'
            '                <strong>問%d(正解:(%d))</strong><br>\n'
            '                %s\n'
            '            </div>\n'
            '        </div>\n'
            '    </div>'
            % (qnum, correct, exp))

    body = "\n".join([
        qsec(1, Q1_TEXT, 6, "【図1】立体の見取図と鏡の位置", fig1, optg1),
        expsec(1, Q1_correct, Q1_EXP),
        qsec(2, Q2_TEXT, 6, "【図2】立体の見取図と鏡の位置", fig2, optg2),
        expsec(2, Q2_correct, Q2_EXP),
    ])

    tpl = open(os.path.join(ROOT, "template_static.html"), encoding="utf-8").read()
    lines = tpl.split("\n")
    head = "\n".join(lines[:284])   # ～<body>
    tail = "\n".join(lines[454:])   # JavaScriptコメント以降
    html = head + "\n" + body + "\n\n" + tail
    out = os.path.join(ROOT, "印刷用", "印刷218.html")
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, len(html), "bytes")


if __name__ == "__main__":
    build_dynamic()
    build_static()
