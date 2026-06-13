# -*- coding: utf-8 -*-
"""航大思考217 / 印刷217 HTMLジェネレータ（立体の鏡像：左右反転）"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===== データ（verify_217.py と一致） =====
G1 = [[3, 1, 0], [2, 0, 1], [1, 2, 2]]
Q1_OPTS = [
    [[3, 1, 0], [2, 0, 1], [1, 2, 2]],   # (1) 元のまま
    [[2, 2, 1], [1, 0, 2], [0, 1, 3]],   # (2) 180度回転
    [[3, 2, 1], [1, 0, 2], [0, 1, 2]],   # (3) 転置
    [[0, 1, 3], [1, 0, 2], [2, 2, 1]],   # (4) 鏡像 ★正解
    [[1, 2, 2], [2, 0, 1], [3, 1, 0]],   # (5) 上下反転
]
Q1_ANS = 4

G2 = [[2, 0, 3, 1], [1, 3, 0, 2], [0, 2, 1, 3], [3, 1, 2, 0]]
G2_STAR = (1, 0)
# (grid, star)
Q2_OPTS = [
    ([[1, 3, 0, 2], [2, 0, 3, 1], [3, 1, 2, 0], [0, 2, 1, 3]], (1, 3)),  # (1) 鏡像 ★正解
    ([[2, 0, 3, 1], [1, 3, 0, 2], [0, 2, 1, 3], [3, 1, 2, 0]], (1, 0)),  # (2) 元のまま
    ([[0, 2, 1, 3], [3, 1, 2, 0], [2, 0, 3, 1], [1, 3, 0, 2]], (2, 3)),  # (3) 180度回転
    ([[2, 1, 0, 3], [0, 3, 2, 1], [3, 0, 1, 2], [1, 2, 3, 0]], (0, 1)),  # (4) 転置
    ([[3, 1, 2, 0], [0, 2, 1, 3], [1, 3, 0, 2], [2, 0, 3, 1]], (2, 0)),  # (5) 上下反転
]
Q2_ANS = 1


# ===== グリッド描画 =====
def cell_rect(x, y, cell, val, marked):
    fill = "#000" if marked else "#fff"
    tcol = "#fff" if marked else ("#bbb" if val == 0 else "#000")
    fs = int(cell * 0.5)
    return (
        f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
        f'fill="{fill}" stroke="#333" stroke-width="1.5"/>'
        f'<text x="{x + cell / 2:.0f}" y="{y + cell / 2 + fs * 0.36:.0f}" '
        f'text-anchor="middle" font-size="{fs}" '
        f'font-family="sans-serif" fill="{tcol}">{val}</text>'
    )


def grid_svg(g, ox, oy, cell, star=None):
    out = ""
    for r, row in enumerate(g):
        for c, val in enumerate(row):
            marked = star is not None and (r, c) == star
            out += cell_rect(ox + c * cell, oy + r * cell, cell, val, marked)
    return out


def label(x, y, text):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-size="15" '
            f'font-family="sans-serif" font-weight="bold">{text}</text>')


# ===== 与えられた立体の図 =====
def given1_svg():
    s = '<svg width="200" height="180" viewBox="0 0 200 180">'
    s += label(80, 22, "真上から見た図")
    s += grid_svg(G1, 25, 35, 40)
    s += label(80, 175, "↑ 正面")
    s += '<line x1="170" y1="35" x2="170" y2="155" stroke="#000" stroke-width="3"/>'
    s += label(185, 100, "鏡")
    s += "</svg>"
    return s


def given2_svg():
    s = '<svg width="220" height="210" viewBox="0 0 220 210">'
    s += label(85, 22, "真上から見た図")
    s += grid_svg(G2, 20, 35, 38, star=G2_STAR)
    s += label(85, 200, "↑ 正面")
    s += '<line x1="185" y1="35" x2="185" y2="187" stroke="#000" stroke-width="3"/>'
    s += label(200, 110, "鏡")
    s += "</svg>"
    return s


# ===== 静的版（印刷用）選択肢パネル =====
def static_opts1():
    s = '<svg width="620" height="155" viewBox="0 0 620 155">'
    for i, g in enumerate(Q1_OPTS):
        ox = 14 + i * 120
        s += label(ox + 51, 20, f"({i + 1})")
        s += grid_svg(g, ox, 30, 34)
    s += "</svg>"
    return s


def static_opts2():
    s = '<svg width="480" height="340" viewBox="0 0 480 340">'
    pos = [(15, 40), (165, 40), (315, 40), (90, 200), (240, 200)]
    for i, (g, star) in enumerate(Q2_OPTS):
        ox, oy = pos[i]
        s += label(ox + 60, oy - 10, f"({i + 1})")
        s += grid_svg(g, ox, oy, 30, star=star)
    s += "</svg>"
    return s


# ===== 動的版 選択肢ボタンSVG =====
def dyn_opt1(i, g):
    s = '<svg width="120" height="135" viewBox="0 0 120 135">'
    s += label(60, 18, f"({i + 1})")
    s += grid_svg(g, 12, 28, 32)
    s += "</svg>"
    return s


def dyn_opt2(i, g, star):
    s = '<svg width="150" height="162" viewBox="0 0 150 162">'
    s += label(75, 18, f"({i + 1})")
    s += grid_svg(g, 11, 28, 32, star=star)
    s += "</svg>"
    return s


# ===== 問題文・解説 =====
Q1_TEXT = ("積み木を組んでできた立体を真上から見て、各マスに積み上げた立方体の段数を記した"
           "ものが【図1】である。0は積み木が無いことを表す。この立体の右側に鏡を垂直に立てて"
           "映すとき、鏡に映った立体を同じように真上から見た図として正しいものを、"
           "(1)〜(5)から一つ選べ。")
Q2_TEXT = ("【図2】は、積み木を組んでできた立体を真上から見て各マスの段数を記したものである。"
           "黒く塗ったマスには、目印のついた立方体が1段だけ置かれている。この立体の右側に鏡を"
           "垂直に立てて映すとき、鏡に映った立体を真上から見た図として正しいものを、"
           "(1)〜(5)から一つ選べ。")

EXP1 = (
    "鏡を立体の<strong>右側</strong>に立てて映すと、<strong>左右が反転</strong>する。"
    "真上から見た図では、各行の数字を<strong>そのまま左右逆順</strong>に並べ替えればよい。<br><br>"
    "元の図（各行）：<br>3 1 0 ／ 2 0 1 ／ 1 2 2<br>"
    "左右反転（鏡像）：<br>0 1 3 ／ 1 0 2 ／ 2 2 1<br>"
    "これは選択肢<strong>(4)</strong>と一致する。<br><br>"
    "<strong>【選択肢の検討】</strong><br>"
    "・(1) 元の図のまま。反転していないので誤り。<br>"
    "・(2) 上下も左右も入れ替えた180度回転。鏡像ではない。<br>"
    "・(3) 行と列を入れ替えた転置（対角線対称）。左右の鏡像とは異なる。<br>"
    "・(4) 各行を左右逆にした図。これが鏡像であり正解。<br>"
    "・(5) 行の並びだけを逆にした上下反転（前後方向の鏡像）。右側の鏡では起こらない。<br><br>"
    "したがって、正解は<strong>(4)</strong>である。"
)

EXP2 = (
    "問1と同じく、右側の鏡では<strong>左右が反転</strong>する。"
    "数字の配置を各行で左右逆順にすると同時に、黒い目印のマスも左右反転で列が移動する。<br><br>"
    "元の図：2 0 3 1 ／ 1 3 0 2 ／ 0 2 1 3 ／ 3 1 2 0<br>"
    "目印は<strong>上から2行目・左端</strong>（左から1列目）にある。<br>"
    "左右反転後：1 3 0 2 ／ 2 0 3 1 ／ 3 1 2 0 ／ 0 2 1 3<br>"
    "目印は<strong>上から2行目・右端</strong>（右から1列目）へ移る。<br>"
    "これは選択肢<strong>(1)</strong>と一致する。<br><br>"
    "<strong>【選択肢の検討】</strong><br>"
    "・(1) 数字配置・目印の位置がともに左右反転と一致。正解。<br>"
    "・(2) 元の図のまま。反転していない。<br>"
    "・(3) 180度回転。目印が反対側の行・列へ移っており誤り。<br>"
    "・(4) 行と列を入れ替えた転置。配置が一致しない。<br>"
    "・(5) 上下反転。目印が下方の行へ移っており、右側の鏡では起こらない。<br><br>"
    "数字配置と目印の位置の<strong>両方</strong>が一致するのは(1)のみ。よって正解は<strong>(1)</strong>である。"
)


def build_static():
    t = open(os.path.join(ROOT, "template_static.html"), encoding="utf-8").read()
    head = t.split("<body>")[0] + "<body>"
    tail = t[t.index("    <!-- ==================== JavaScript"):]
    opt1 = static_opts1()
    opt2 = static_opts2()
    body = f"""
    <div class="question-section question-page"><div class="page-content"><div class="question">
        <div class="question-number">問1．{Q1_TEXT}（6点）</div>
        <div class="figure-container"><div class="figure-title">【図1】立体を真上から見た図と鏡の位置</div><div class="figure-content">{given1_svg()}</div></div>
        <div class="figure-container" style="border:none; box-shadow:none;"><div class="figure-title">【選択肢】鏡に映った立体を真上から見た図</div><div class="figure-content">{opt1}</div></div>
    </div></div></div>
    <div class="question-section question-page"><div class="page-content"><div class="explanation">
        <strong>問1(正解:(4))</strong><br>{EXP1}
    </div></div></div>
    <div class="question-section question-page"><div class="page-content"><div class="question">
        <div class="question-number">問2．{Q2_TEXT}（6点）</div>
        <div class="figure-container"><div class="figure-title">【図2】立体を真上から見た図（黒マス＝目印）と鏡の位置</div><div class="figure-content">{given2_svg()}</div></div>
        <div class="figure-container" style="border:none; box-shadow:none;"><div class="figure-title">【選択肢】鏡に映った立体を真上から見た図</div><div class="figure-content">{opt2}</div></div>
    </div></div></div>
    <div class="question-section question-page"><div class="page-content"><div class="explanation">
        <strong>問2(正解:(1))</strong><br>{EXP2}
    </div></div></div>
"""
    out = head + "\n" + body + "\n" + tail
    path = os.path.join(ROOT, "印刷用", "印刷217.html")
    open(path, "w", encoding="utf-8").write(out)
    print("wrote", path)


def build_dynamic():
    t = open(os.path.join(ROOT, "template_dynamic.html"), encoding="utf-8").read()
    head = t.split("<body>")[0] + "<body>"
    tail = t[t.index("    <!-- ==================== JavaScript"):]
    tail = tail.replace("2026_01/航大思考X", "2026_06/航大思考217")

    btn1 = ""
    for i, g in enumerate(Q1_OPTS):
        btn1 += (f'<button class="option-figure-button" data-option="{i+1}" '
                 f'onclick="selectAnswer(1, {i+1}, {Q1_ANS})">{dyn_opt1(i, g)}</button>')
    btn2 = ""
    for i, (g, star) in enumerate(Q2_OPTS):
        btn2 += (f'<button class="option-figure-button" data-option="{i+1}" '
                 f'onclick="selectAnswer(2, {i+1}, {Q2_ANS})">{dyn_opt2(i, g, star)}</button>')

    body = f"""    <main class="main-content">
        <div class="progress-bar">
            <div class="progress-dot" id="progress-1" onclick="goToQuestion(1)">1</div>
            <div class="progress-dot" id="progress-2" onclick="goToQuestion(2)">2</div>
        </div>
        <div class="screen active" id="q1-question">
            <div class="question-header"><span class="question-number">問1</span><span class="question-meta">配点: 6点 / 目安時間: 3分</span></div>
            <div class="question-text">{Q1_TEXT}</div>
            <div class="figure-container"><div class="figure-title">【図1】立体を真上から見た図と鏡の位置</div><div class="figure-content">{given1_svg()}</div></div>
            <div class="figure-title">鏡に映った立体を真上から見た図（クリックで解答）</div>
            <div class="options-figure" id="q1-options">{btn1}</div>
            <div class="explanation-section" id="q1-explanation"><div class="explanation-header">問1（正解: (4)）</div><div class="explanation-content">{EXP1}</div></div>
            <div class="nav-buttons" id="q1-nav" style="display: none;"><button class="btn btn-secondary hidden">前の問題</button><button class="btn btn-primary" onclick="goToQuestion(2)">問2へ</button></div>
        </div>
        <div class="screen" id="q2-question">
            <div class="question-header"><span class="question-number">問2</span><span class="question-meta">配点: 6点 / 目安時間: 5分</span></div>
            <div class="question-text">{Q2_TEXT}</div>
            <div class="figure-container"><div class="figure-title">【図2】立体を真上から見た図（黒マス＝目印）と鏡の位置</div><div class="figure-content">{given2_svg()}</div></div>
            <div class="figure-title">鏡に映った立体を真上から見た図（クリックで解答）</div>
            <div class="options-figure" id="q2-options">{btn2}</div>
            <div class="explanation-section" id="q2-explanation"><div class="explanation-header">問2（正解: (1)）</div><div class="explanation-content">{EXP2}</div></div>
            <div class="nav-buttons" id="q2-nav" style="display: none;"><button class="btn btn-secondary" onclick="goToQuestion(1)">問1へ</button><button class="btn btn-secondary hidden">（空欄）</button></div>
        </div>
    </main>
"""
    out = head + "\n" + body + "\n" + tail
    path = os.path.join(ROOT, "航大思考問題", "航大思考217.html")
    open(path, "w", encoding="utf-8").write(out)
    print("wrote", path)


if __name__ == "__main__":
    build_static()
    build_dynamic()
