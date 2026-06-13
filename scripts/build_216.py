#!/usr/bin/env python3
"""航大思考216 HTMLビルド: 立体ピース嵌め合わせ問題。

既存の印刷216/航大思考216のヘッダ・スクリプト部を流用し、
本文（問題・解説）を立体パズル問題に差し替えて両ファイルを再生成する。
"""
import os
from gen_svg_216 import figure, cubes_svg, _raw_extent
from verify_216 import mirror, normalize, CAVITY

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(cells):
    return sorted(normalize(frozenset(cells)))


# ===== Q1 形状（0-indexed, x右 y奥 z上）=====
FULL = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]
CAV = set((x, y, z) for (x, y, z) in CAVITY)  # 1-indexed? -> verify uses 1..3
# verify_216 の CAVITY は 1..3 表記。0..2 へ変換。
CAV0 = set((x - 1, y - 1, z - 1) for (x, y, z) in CAVITY)
SOLID_A = [c for c in FULL if c not in CAV0]            # 立体A（22マス）

Q1_CORRECT = norm(CAV0)                                  # 正解ピース
Q1_MIRROR = norm(mirror(frozenset(CAV0)))                # 鏡像（罠）
Q1_U = [(0, 0, 1), (1, 0, 1), (2, 0, 1), (0, 0, 0), (2, 0, 0)]
Q1_P = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0)]
Q1_SAME = [(0, 0, 1), (1, 0, 1), (2, 0, 1), (2, 0, 0), (2, 1, 1)]

# ===== Q2 形状 =====
BOX = [(x, y, z) for x in range(2) for y in range(2) for z in range(3)]
P_PIECE = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]   # 三脚型
Q_PIECE = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]   # ねじれ型(左)
Q2_S = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)]
Q2_SQ = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)]
Q2_T = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0)]       # 正解
Q2_SKEWR = norm(mirror(frozenset(Q_PIECE)))              # ねじれ型(右)
Q2_L = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0)]

def slot_inner(cells, slot_w, slot_h, n=None, label_margin=24, **kw):
    """cellsをslot(slot_w×slot_h)内に中央寄せした立方体群＋番号ラベルを返す。"""
    mnx, mxx, mny, mxy = _raw_extent(cells)
    cw, ch = mxx - mnx, mxy - mny
    target_left = (slot_w - cw) / 2
    target_top = label_margin + (slot_h - label_margin - ch) / 2
    ox = target_left - mnx
    oy = target_top - mny
    body = cubes_svg(cells, ox, oy, **kw)
    if n is not None:
        body = (f'<text x="{slot_w/2:.1f}" y="16" text-anchor="middle" '
                f'font-size="15" font-weight="bold">({n})</text>') + body
    return body


def standalone(cells, slot_w, slot_h, n=None, **kw):
    inner = slot_inner(cells, slot_w, slot_h, n, **kw)
    return (f'<svg width="{slot_w}" height="{slot_h}" '
            f'viewBox="0 0 {slot_w} {slot_h}">{inner}</svg>')


def print_options_row(options, slot_w=125, slot_h=150):
    """印刷用: 5択を横一列に並べた1枚のSVGを返す。"""
    total_w = slot_w * len(options)
    gs = ""
    for i, cells in enumerate(options):
        gs += (f'<g transform="translate({i*slot_w},0)">'
               f'{slot_inner(cells, slot_w, slot_h, n=i+1)}</g>')
    return (f'<svg width="{total_w}" height="{slot_h}" '
            f'viewBox="0 0 {total_w} {slot_h}">{gs}</svg>')


def dyn_options(q, options, correct, slot_w=120, slot_h=150):
    """航大思考用: figureボタン5択のHTMLを返す。"""
    out = f'<div class="options-figure" id="q{q}-options">\n'
    for i, cells in enumerate(options):
        n = i + 1
        out += (f'                <button class="option-figure-button" '
                f'data-option="{n}" onclick="selectAnswer({q}, {n}, {correct})">'
                f'{standalone(cells, slot_w, slot_h, n=n)}</button>\n')
    out += '            </div>'
    return out


Q1_OPTS = [Q1_U, Q1_MIRROR, Q1_P, Q1_CORRECT, Q1_SAME]   # 正解=4
Q2_OPTS = [Q2_S, Q2_SQ, Q2_T, Q2_SKEWR, Q2_L]            # 正解=3


from build_216_text import Q1_TEXT, Q1_EXPL, Q2_TEXT, Q2_EXPL


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.readlines()


def fc(title, svg):
    return (f'<div class="figure-container"><div class="figure-title">{title}</div>'
            f'<div class="figure-content">{svg}</div></div>')


def build_print():
    path = os.path.join(ROOT, "印刷用", "印刷216.html")
    L = read_lines(path)
    head = "".join(L[:284])      # ～<body>
    tail = "".join(L[479:])      # JavaScript～
    a_fig = standalone(SOLID_A, 250, 240)
    box_fig = standalone(BOX, 170, 220)
    p_fig = standalone(P_PIECE, 150, 170)
    q_fig = standalone(Q_PIECE, 150, 170)
    q1opts = print_options_row(Q1_OPTS)
    q2opts = print_options_row(Q2_OPTS)
    body = f"""
    <!-- ========== 問1 問題ページ ========== -->
    <div class="question-section question-page">
        <div class="page-content">
            <div class="question">
                <div class="question-number">問1．{Q1_TEXT}（6点）</div>
                {fc('【図1】立体A（3×3×3から一部を取り除いた立体）', a_fig)}
                {fc('【図2】はめ込むピースの候補', q1opts)}
            </div>
        </div>
    </div>

    <!-- ========== 問1 解説ページ ========== -->
    <div class="question-section question-page">
        <div class="page-content">
            <div class="explanation">
                <strong>問1(正解:(4))</strong><br>
{Q1_EXPL}
            </div>
        </div>
    </div>

    <!-- ========== 問2 問題ページ ========== -->
    <div class="question-section question-page">
        <div class="page-content">
            <div class="question">
                <div class="question-number">問2．{Q2_TEXT}（6点）</div>
                {fc('【図3】組み立てる直方体（2×2×3）', box_fig)}
                <div class="figure-container"><div class="figure-title">【図4】すでに形が決まっている2つのピース</div>
                <div class="figure-content" style="display:flex;justify-content:center;gap:30px;align-items:flex-end;">
                <div><div style="font-weight:bold;">ピースP</div>{p_fig}</div>
                <div><div style="font-weight:bold;">ピースQ</div>{q_fig}</div>
                </div></div>
                {fc('【図5】残り1つのピースの候補', q2opts)}
            </div>
        </div>
    </div>

    <!-- ========== 問2 解説ページ ========== -->
    <div class="question-section question-page">
        <div class="page-content">
            <div class="explanation">
                <strong>問2(正解:(3))</strong><br>
{Q2_EXPL}
            </div>
        </div>
    </div>

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + body + tail)
    print("wrote", path)


def build_dynamic():
    path = os.path.join(ROOT, "航大思考問題", "航大思考216.html")
    L = read_lines(path)
    head = "".join(L[:428])      # ～プログレスバー閉じ
    tail = "".join(L[657:])      # JavaScript～
    a_fig = standalone(SOLID_A, 280, 250)
    box_fig = standalone(BOX, 180, 230)
    p_fig = standalone(P_PIECE, 160, 180)
    q_fig = standalone(Q_PIECE, 160, 180)
    q1opts = dyn_options(1, Q1_OPTS, 4)
    q2opts = dyn_options(2, Q2_OPTS, 3)
    body = f"""        <!-- ========== 問1 問題画面 ========== -->
        <div class="screen active" id="q1-question">
            <div class="question-header">
                <span class="question-number">問1</span>
                <span class="question-meta">配点: 6点 / 目安時間: 3分</span>
            </div>
            <div class="question-text">{Q1_TEXT}</div>
            {fc('【図1】立体A（3×3×3から一部を取り除いた立体）', a_fig)}
            <div class="figure-container"><div class="figure-title">【図2】はめ込むピースの候補（クリックで解答）</div></div>
            {q1opts}
            <div class="explanation-section" id="q1-explanation">
                <div class="explanation-header">問1（正解: (4)）</div>
                <div class="explanation-content">
{Q1_EXPL}
                </div>
            </div>
            <div class="nav-buttons" id="q1-nav" style="display: none;">
                <button class="btn btn-secondary hidden">前の問題</button>
                <button class="btn btn-primary" onclick="goToQuestion(2)">問2へ</button>
            </div>
        </div>

        <!-- ========== 問2 問題画面 ========== -->
        <div class="screen" id="q2-question">
            <div class="question-header">
                <span class="question-number">問2</span>
                <span class="question-meta">配点: 6点 / 目安時間: 5分</span>
            </div>
            <div class="question-text">{Q2_TEXT}</div>
            {fc('【図3】組み立てる直方体（2×2×3）', box_fig)}
            <div class="figure-container"><div class="figure-title">【図4】すでに形が決まっている2つのピース</div>
            <div class="figure-content" style="display:flex;justify-content:center;gap:30px;align-items:flex-end;">
            <div><div style="font-weight:bold;">ピースP</div>{p_fig}</div>
            <div><div style="font-weight:bold;">ピースQ</div>{q_fig}</div>
            </div></div>
            <div class="figure-container"><div class="figure-title">【図5】残り1つのピースの候補（クリックで解答）</div></div>
            {q2opts}
            <div class="explanation-section" id="q2-explanation">
                <div class="explanation-header">問2（正解: (3)）</div>
                <div class="explanation-content">
{Q2_EXPL}
                </div>
            </div>
            <div class="nav-buttons" id="q2-nav" style="display: none;">
                <button class="btn btn-secondary" onclick="goToQuestion(1)">問1へ</button>
                <button class="btn btn-secondary hidden">（空欄）</button>
            </div>
        </div>
    </main>

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + body + tail)
    print("wrote", path)


if __name__ == "__main__":
    print("立体A マス数:", len(SOLID_A))
    print("Q1 正解index:", Q1_OPTS.index(Q1_CORRECT) + 1,
          " Q2 正解index:", Q2_OPTS.index(Q2_T) + 1)
    build_print()
    build_dynamic()
