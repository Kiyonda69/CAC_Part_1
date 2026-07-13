#!/usr/bin/env python3
"""航大思考278 / 印刷278 のHTMLをテンプレートから組み立てる"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVGDIR = sys.argv[1] if len(sys.argv) > 1 else "."


def svg(name):
    with open(os.path.join(SVGDIR, name)) as f:
        return f.read()


Q1_TEXT = ("下の図のような、同じ大きさの小立方体を面と面をぴったり合わせて"
           "作った立体Aがある。立体Aと、(1)〜(5)のうちのいずれか1つの立体とを"
           "すきまなく組み合わせて、図に示すたて2個・よこ3個・高さ2個"
           "（小立方体12個分）の直方体を作りたい。立体Aと組み合わせることが"
           "できる立体はどれか。ただし、どの立体も自由に回転させて置いてよい。"
           "また、選択肢の立体はいずれも小立方体6個からなる。")

Q2_TEXT = ("下の図のような、同じ大きさの小立方体9個ずつを面と面をぴったり"
           "合わせて作った立体Aと立体Bがある。立体A・立体Bと、(1)〜(5)の"
           "うちのいずれか1つの立体との3つをすきまなく組み合わせて、1辺に"
           "小立方体が3個並ぶ立方体（小立方体27個分）を作りたい。組み合わせる"
           "立体として正しいものはどれか。ただし、どの立体も自由に回転させて"
           "置いてよい。また、選択肢の立体はいずれも小立方体9個からなる。")

Q1_EXPL = [
    "完成させる直方体は小立方体12個分であり、立体Aは6個からなるので、残りの空間はちょうど小立方体6個分である。ただし選択肢はすべて6個からなるため、個数では絞り込めず、<strong>残りの空間の「形」と一致するか</strong>を考える必要がある。",
    "<strong>【残りの空間の形を求める】</strong>",
    "立体Aは、L字形に並べた4個の小立方体の上に、端の2個分を重ねた形である。これを直方体の中に置くと、残る空間は「2×2×1の板の一方の端に、小立方体2個を付け足した形」になる。これは(4)の立体を回転させた形とちょうど一致する。次の層別図は組み立て方の一例であり、すきまも重なりもなく直方体が完成する。",
    "<strong>【選択肢の検討】</strong>",
    "・(1) 2×2×2の立方体から、上面の対角線上にある2個を除いた形。Aのくぼみとかみ合わず、どの向きに置いてもすきまができる。",
    "・(2) 立体Aと同じ形。Aを2つ組み合わせても、どの向きの組でも2×3×2の直方体にはならない。",
    "・(3) 3×2の平板。Aの段差部分（高さの異なる部分）を埋めることができない。",
    "・(4) 残りの空間と同じ形であり、直方体が完成する。（正解）",
    "・(5) 2×2×2の立方体から、対角線上で反対側にある2個を除いた形。Aと組むと必ず1個分のすきまと1個分のはみ出しが生じる。",
    "したがって、正解は<strong>(4)</strong>である。",
]

Q2_EXPL = [
    "完成させる立方体は小立方体27個分であり、立体Aと立体Bはそれぞれ9個からなるので、残りの空間はちょうど9個分である。選択肢もすべて9個からなるため、ここでも<strong>残りの空間の形</strong>を特定する必要がある。",
    "<strong>【組み立て方を考える】</strong>",
    "立体Aは、階段状のL字形の底面から一つの角に向かって高くなる形であり、立方体の一つの段の大部分と角の柱を受け持つ。立体Bは、一つの面の壁ぎわを底から上まで囲む形である。この2つを向かい合わせにかみ合わせると、残る空間は、2つの段にまたがってかぎ形に折れ曲がった9個分の立体になる。これは(4)の立体を回転させた形とちょうど一致する。次の層別図は組み立て方の一例であり（Cが(4)の立体）、すきまも重なりもなく立方体が完成する。",
    "<strong>【選択肢の検討】</strong>",
    "・(1) (4)と似ているが、小立方体1個の位置が異なる（張り出しの位置が1つずれている）。この1個分がどうしても収まらない。",
    "・(2) 立体Aと同じ形。A・Bとどの向きで組み合わせても、必ず重なりかすきまが生じる。",
    "・(3) (4)と似ているが、下段側の1個の位置が異なるため、Bの壁ぎわの空間を埋められない。",
    "・(4) 残りの空間と同じ形であり、立方体が完成する。（正解）",
    "・(5) (4)と似ているが、奥側の1個の位置が異なるため、中段にすきまが残る。",
    "したがって、正解は<strong>(4)</strong>である。",
]


def para(lines):
    return "\n".join(f"<p>{s}</p>" for s in lines)


def br_join(lines):
    return "<br>\n".join(lines)


def figure(title, body):
    return (f'<div class="figure-container">\n'
            f'<div class="figure-title">{title}</div>\n'
            f'<div class="figure-content">\n{body}\n</div>\n</div>')


def build_static():
    with open(os.path.join(ROOT, "template_static.html")) as f:
        tpl = f.read()
    head = tpl[:tpl.index("<body>") + len("<body>")]
    js_marker = "    <!-- ==================== JavaScript ===================="
    tail = tpl[tpl.index(js_marker):]

    def qpage(num, text, fig_title, fig_svg, opts):
        opts_html = "\n".join(svg(o) for o in opts)
        return f'''
    <!-- ========== 問{num} 問題ページ ========== -->
    <div class="question-section question-page">
        <div class="page-content">
            <div class="question">
                <div class="question-number">問{num}．{text}（6点）</div>
                {figure(fig_title, fig_svg)}
                <div class="figure-container" style="border: none;">
                    <div class="figure-content">
{opts_html}
                    </div>
                </div>
            </div>
        </div>
    </div>
'''

    def epage(num, ans, lines, layer_svg):
        return f'''
    <!-- ========== 問{num} 解説ページ ========== -->
    <div class="question-section question-page">
        <div class="page-content">
            <div class="explanation">
                <strong>問{num}(正解:({ans}))</strong><br>
                {br_join(lines)}<br>
                <div class="figure-container" style="border: none;">
                    <div class="figure-content">
{layer_svg}
                    </div>
                </div>
            </div>
        </div>
    </div>
'''

    body = (qpage(1, Q1_TEXT, "【図1】完成させる直方体と立体A", svg("q1_main.svg"),
                  [f"q1_opt{i}.svg" for i in range(1, 6)])
            + epage(1, 4, Q1_EXPL, svg("q1_layers.svg"))
            + qpage(2, Q2_TEXT, "【図2】完成させる立方体と立体A・立体B", svg("q2_main.svg"),
                    [f"q2_opt{i}.svg" for i in range(1, 6)])
            + epage(2, 4, Q2_EXPL, svg("q2_layers.svg")))

    out = head + "\n" + body + "\n" + tail
    path = os.path.join(ROOT, "印刷用", "印刷278.html")
    with open(path, "w") as f:
        f.write(out)
    print("wrote", path)


def build_dynamic():
    with open(os.path.join(ROOT, "template_dynamic.html")) as f:
        tpl = f.read()
    q1_marker = "        <!-- ========== 問1 問題画面 =========="
    js_marker = "    <!-- ==================== JavaScript ==================== -->"
    head = tpl[:tpl.index(q1_marker)]
    tail = tpl[tpl.index(js_marker):].replace(
        "2026_01/航大思考X", "2026_07/航大思考278")

    def screen(num, active, meta, text, fig_title, fig_svg, opts, ans,
               expl_lines, layer_svg, nav):
        buttons = "\n".join(
            f'''                <button class="option-figure-button" data-option="{i}" onclick="selectAnswer({num}, {i}, {ans})">
{svg(o)}
                </button>''' for i, o in enumerate(opts, 1))
        return f'''        <!-- ========== 問{num} 問題画面 ========== -->
        <div class="screen{' active' if active else ''}" id="q{num}-question">
            <div class="question-header">
                <span class="question-number">問{num}</span>
                <span class="question-meta">{meta}</span>
            </div>
            <div class="question-text">
                {text}
            </div>
            {figure(fig_title, fig_svg)}
            <div class="options-figure" id="q{num}-options">
{buttons}
            </div>
            <div class="explanation-section" id="q{num}-explanation">
                <div class="explanation-header">問{num}（正解: ({ans})）</div>
                <div class="explanation-content">
{para(expl_lines)}
<div style="text-align: center; margin-top: 10px;">
{layer_svg}
</div>
                </div>
            </div>
            <div class="nav-buttons" id="q{num}-nav" style="display: none;">
{nav}
            </div>
        </div>
'''

    nav1 = ('                <button class="btn btn-secondary hidden">前の問題</button>\n'
            '                <button class="btn btn-primary" onclick="goToQuestion(2)">問2へ</button>')
    nav2 = ('                <button class="btn btn-secondary" onclick="goToQuestion(1)">問1へ</button>\n'
            '                <button class="btn btn-secondary hidden">（空欄）</button>')

    body = (screen(1, True, "配点: 6点 / 目安時間: 3分", Q1_TEXT,
                   "【図1】完成させる直方体と立体A", svg("q1_main.svg"),
                   [f"q1_opt{i}.svg" for i in range(1, 6)], 4,
                   Q1_EXPL, svg("q1_layers.svg"), nav1)
            + "\n"
            + screen(2, False, "配点: 6点 / 目安時間: 5分", Q2_TEXT,
                     "【図2】完成させる立方体と立体A・立体B", svg("q2_main.svg"),
                     [f"q2_opt{i}.svg" for i in range(1, 6)], 4,
                     Q2_EXPL, svg("q2_layers.svg"), nav2)
            + "    </main>\n\n")

    out = head + body + tail
    path = os.path.join(ROOT, "航大思考問題", "航大思考278.html")
    with open(path, "w") as f:
        f.write(out)
    print("wrote", path)


if __name__ == "__main__":
    build_static()
    build_dynamic()
