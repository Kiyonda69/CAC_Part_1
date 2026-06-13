# -*- coding: utf-8 -*-
"""航大思考224 ビルダー: 紙折り穴あけ問題のHTML(印刷用/動的)を生成。

座標系: 正方形の航空図を 0〜8 の格子で表す。左下が原点、y軸は上向き。
SVGピクセルは y を反転して描画する。
"""
import os

# verify_224 と同じ正解データ
P1_HOLES = [(3, 1), (5, 1), (3, 7), (5, 7)]
P2_HOLES = [(3, 1), (5, 1), (3, 7), (5, 7), (1, 3), (7, 3), (1, 5), (7, 5)]

P1_OPTIONS = {
    1: [(3, 2), (5, 2), (3, 6), (5, 6)],
    2: [(1, 3), (7, 3), (1, 5), (7, 5)],
    3: [(3, 1), (5, 1), (3, 3), (5, 3)],
    4: [(1, 1), (7, 1), (1, 7), (7, 7)],
    5: [(3, 1), (5, 1), (3, 7), (5, 7)],   # 正解
}
P1_ANSWER = 5

P2_OPTIONS = {
    1: [(3, 1), (5, 1), (3, 7), (5, 7)],
    2: [(1, 3), (7, 3), (1, 5), (7, 5)],
    3: [(3, 1), (5, 1), (3, 7), (5, 7), (2, 3), (6, 3), (2, 5), (6, 5)],
    4: [(3, 1), (5, 1), (3, 7), (5, 7), (1, 3), (7, 3), (1, 5), (7, 5)],  # 正解
    5: [(3, 1), (5, 1), (3, 7), (5, 7), (1, 2), (7, 2), (1, 6), (7, 6)],
}
P2_ANSWER = 4


def grid_region(ax, ay, bx, by, px, py, c):
    """単位格子領域[ax,bx]x[ay,by]を、左上角(=単位(ax,by))がピクセル(px,py)
    に来るよう、セル幅cで描く。SVG文字列リストと、単位->ピクセル変換関数を返す。"""
    parts = []
    w = (bx - ax) * c
    h = (by - ay) * c

    def to_px(x, y):
        return (px + (x - ax) * c, py + (by - y) * c)

    # 内側のうすい格子線
    for gx in range(ax, bx + 1):
        x1, y1 = to_px(gx, ay)
        x2, y2 = to_px(gx, by)
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                     f'stroke="#ccc" stroke-width="1"/>')
    for gy in range(ay, by + 1):
        x1, y1 = to_px(ax, gy)
        x2, y2 = to_px(bx, gy)
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                     f'stroke="#ccc" stroke-width="1"/>')
    # 外枠
    parts.append(f'<rect x="{px}" y="{py}" width="{w}" height="{h}" '
                 f'fill="none" stroke="#000" stroke-width="2"/>')
    return parts, to_px


def option_svg(holes, label, c=12, m=9, top=20):
    """8x8格子に穴(holes)を描いた選択肢用SVG。"""
    side = 8 * c
    vbw = side + 2 * m
    vbh = top + side + m
    parts, to_px = grid_region(0, 0, 8, 8, m, top, c)
    body = [f'<text x="{vbw/2:.0f}" y="14" class="svg-text" '
            f'text-anchor="middle">{label}</text>']
    body += parts
    for (gx, gy) in holes:
        cx, cy = to_px(gx, gy)
        body.append(f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="#000"/>')
    inner = "\n        ".join(body)
    return (f'<svg width="{vbw}" height="{vbh}" viewBox="0 0 {vbw} {vbh}">\n'
            f'        {inner}\n      </svg>')


def harrow(x1, y, x2):
    """右向きの遷移矢印。"""
    return (f'<line x1="{x1}" y1="{y}" x2="{x2-6}" y2="{y}" stroke="#000" '
            f'stroke-width="2"/>'
            f'<polygon points="{x2},{y} {x2-7},{y-4} {x2-7},{y+4}" fill="#000"/>')


def dash_v(px, py, length, color="#000"):
    return (f'<line x1="{px}" y1="{py}" x2="{px}" y2="{py+length}" '
            f'stroke="{color}" stroke-width="2" stroke-dasharray="5,3"/>')


def dash_h(px1, py, px2, color="#000"):
    return (f'<line x1="{px1}" y1="{py}" x2="{px2}" y2="{py}" '
            f'stroke="{color}" stroke-width="2" stroke-dasharray="5,3"/>')


def circled(px, py, txt):
    return (f'<circle cx="{px}" cy="{py}" r="9" fill="none" stroke="#000" '
            f'stroke-width="1.5"/>'
            f'<text x="{px}" y="{py+4}" class="svg-text" text-anchor="middle" '
            f'font-size="12">{txt}</text>')


def filmstrip1():
    """問1: 直交2折り + 穴あけ の3パネル。"""
    c = 11
    top = 16
    P = []
    # パネルA: 8x8, x=4 で右→左
    ax = 10
    a, toA = grid_region(0, 0, 8, 8, ax, top, c)
    P += a
    fx, _ = toA(4, 8)
    _, fyt = toA(4, 8)
    _, fyb = toA(4, 0)
    P.append(dash_v(fx, fyt, fyb - fyt))
    # 折り方向矢印(右→左)を上部に
    rx, ry = toA(6, 8)
    lx, _ = toA(2, 8)
    P.append(f'<line x1="{rx}" y1="{top-8}" x2="{lx+6}" y2="{top-8}" '
             f'stroke="#000" stroke-width="1.5"/>'
             f'<polygon points="{lx},{top-8} {lx+6},{top-12} {lx+6},{top-4}" '
             f'fill="#000"/>')
    P.append(circled(ax + 4 * c, top + 8 * c + 14, "1"))
    # 軸目盛 0,8
    for t in (0, 8):
        tx, ty = toA(t, 0)
        P.append(f'<text x="{tx}" y="{ty+13}" class="svg-text" '
                 f'text-anchor="middle" font-size="10">{t}</text>')
    # 遷移矢印1
    P.append(harrow(ax + 8 * c + 4, top + 4 * c, ax + 8 * c + 22))
    # パネルB: 4x8, y=4 で上→下
    bx = ax + 8 * c + 26
    b, toB = grid_region(0, 0, 4, 8, bx, top, c)
    P += b
    bx1, byf = toB(0, 4)
    bx2, _ = toB(4, 4)
    P.append(dash_h(bx1, byf, bx2))
    P.append(circled(bx + 2 * c, top + 8 * c + 14, "2"))
    # 遷移矢印2
    P.append(harrow(bx + 4 * c + 4, top + 4 * c, bx + 4 * c + 22))
    # パネルC: 4x4, 穴(3,1)
    cx = bx + 4 * c + 26
    cc, toC = grid_region(0, 0, 4, 4, cx, top, c)
    P += cc
    hx, hy = toC(3, 1)
    P.append(f'<circle cx="{hx}" cy="{hy}" r="5" fill="#000"/>')
    P.append(f'<text x="{hx+13}" y="{hy+4}" class="svg-text" '
             f'font-size="10">(3,1)</text>')
    P.append(circled(cx + 2 * c, top + 8 * c + 14, "3"))
    vbw = cx + 4 * c + 40
    vbh = top + 8 * c + 30
    inner = "\n        ".join(P)
    return (f'<svg width="{vbw}" height="{vbh}" viewBox="0 0 {vbw} {vbh}">\n'
            f'        {inner}\n      </svg>')


def filmstrip2():
    """問2: 直交2折り + 対角折り + 穴あけ の4パネル。
    半分の高さのパネルB/C/DはパネルAの上下中央にそろえる。"""
    c = 10
    top = 16
    half = top + 2 * c   # 半高パネルの上端(Aの中央にそろえる)
    midy = top + 4 * c    # パネルの中央y(遷移矢印の高さ)
    P = []
    cap_y = top + 8 * c + 16   # ステップ番号の行
    # パネルA: 8x8, y=4 で上→下
    ax = 10
    a, toA = grid_region(0, 0, 8, 8, ax, top, c)
    P += a
    lx, ly = toA(0, 4)
    rx, _ = toA(8, 4)
    P.append(dash_h(lx, ly, rx))
    # 下向き矢印(上→下)
    ux, uy = toA(1, 6)
    _, dy = toA(1, 2)
    P.append(f'<line x1="{ux}" y1="{uy}" x2="{ux}" y2="{dy-6}" stroke="#000" '
             f'stroke-width="1.5"/>'
             f'<polygon points="{ux},{dy} {ux-4},{dy-6} {ux+4},{dy-6}" '
             f'fill="#000"/>')
    P.append(circled(ax + 4 * c, cap_y, "1"))
    P.append(harrow(ax + 8 * c + 4, midy, ax + 8 * c + 22))
    # パネルB: 8x4, x=4 で右→左 (中央そろえ)
    bx = ax + 8 * c + 26
    b, toB = grid_region(0, 0, 8, 4, bx, half, c)
    P += b
    fx, fyt = toB(4, 4)
    _, fyb = toB(4, 0)
    P.append(dash_v(fx, fyt, fyb - fyt))
    # 左向き矢印(右→左)
    r2x, r2y = toB(6, 3)
    l2x, _ = toB(2, 3)
    P.append(f'<line x1="{r2x}" y1="{r2y}" x2="{l2x+6}" y2="{r2y}" '
             f'stroke="#000" stroke-width="1.5"/>'
             f'<polygon points="{l2x},{r2y} {l2x+6},{r2y-4} {l2x+6},{r2y+4}" '
             f'fill="#000"/>')
    P.append(circled(bx + 4 * c, cap_y, "2"))
    P.append(harrow(bx + 8 * c + 4, midy, bx + 8 * c + 22))
    # パネルC: 4x4, 対角 y=x で折る (中央そろえ)
    cx = bx + 8 * c + 26
    cc, toC = grid_region(0, 0, 4, 4, cx, half, c)
    P += cc
    d0 = toC(0, 0)
    d1 = toC(4, 4)
    P.append(f'<line x1="{d0[0]}" y1="{d0[1]}" x2="{d1[0]}" y2="{d1[1]}" '
             f'stroke="#000" stroke-width="2" stroke-dasharray="5,3"/>')
    # 折り矢印(上左→下右)
    s0 = toC(1, 3)
    s1 = toC(3, 1)
    P.append(f'<line x1="{s0[0]}" y1="{s0[1]}" x2="{s1[0]}" y2="{s1[1]}" '
             f'stroke="#000" stroke-width="1.5"/>'
             f'<polygon points="{s1[0]},{s1[1]} {s1[0]-7},{s1[1]-1} '
             f'{s1[0]-1},{s1[1]+6}" fill="#000"/>')
    P.append(circled(cx + 2 * c, cap_y, "3"))
    P.append(harrow(cx + 4 * c + 4, midy, cx + 4 * c + 22))
    # パネルD: 下三角形 + 穴(3,1) (中央そろえ)
    dx = cx + 4 * c + 26
    dd, toD = grid_region(0, 0, 4, 4, dx, half, c)
    P += dd
    t0 = toD(0, 0)
    t1 = toD(4, 0)
    t2 = toD(4, 4)
    P.append(f'<polygon points="{t0[0]},{t0[1]} {t1[0]},{t1[1]} '
             f'{t2[0]},{t2[1]}" fill="#eee" stroke="#000" stroke-width="2"/>')
    hx, hy = toD(3, 1)
    P.append(f'<circle cx="{hx}" cy="{hy}" r="5" fill="#000"/>')
    # 穴の座標ラベルはパネル下に置き、三角形の対角線と重ならないようにする
    P.append(f'<text x="{dx+2*c}" y="{half+4*c+14}" class="svg-text" '
             f'text-anchor="middle" font-size="10">(3,1)</text>')
    P.append(circled(dx + 2 * c, cap_y, "4"))
    vbw = dx + 4 * c + 30
    vbh = cap_y + 14
    inner = "\n        ".join(P)
    return (f'<svg width="{vbw}" height="{vbh}" viewBox="0 0 {vbw} {vbh}">\n'
            f'        {inner}\n      </svg>')


Q1_TEXT = (
    "正方形の航空図を机の上に置き、2回折りたたむ。図の格子は紙の位置を表し、"
    "左下を原点として横方向をx・縦方向をyとする（いずれも0〜8）。次の手順で折る。"
    "<br>① 右半分を左半分にぴったり重ねるように、折り線 x=4 で折る。"
    "<br>② 続けて、上半分を下半分に重ねるように、折り線 y=4 で折る。"
    "<br>折りたたんでできた小さな正方形の、点(3,1)の位置にきりで穴を1つあける"
    "（穴は重なった紙の全ての層を貫く）。再び元の正方形に広げたとき、"
    "穴の位置を表す図として正しいものを(1)〜(5)から1つ選べ。"
)

Q2_TEXT = (
    "同じ正方形の航空図（格子は0〜8、左下が原点）を、今度は3回折りたたむ。"
    "<br>① 上半分を下半分にぴったり重ねるように、折り線 y=4 で折る。"
    "<br>② 続けて、右半分を左半分に重ねるように、折り線 x=4 で折る。"
    "<br>③ 続けて、対角線 y=x に沿って折り、対角線より上側を下側にぴったり重ねる。"
    "<br>こうしてできた直角三角形の、点(3,1)の位置にきりで穴を1つあける"
    "（穴は全ての層を貫く）。再び元の正方形に広げたとき、"
    "穴の位置を表す図として正しいものを(1)〜(5)から1つ選べ。"
)

Q1_EXP = """<p>穴は、折り線をまたいで戻すたびに、その折り線に関して鏡像対称な位置に増えていく。</p>
<p><strong>【手順をさかのぼる】</strong></p>
<p>・折り②（y=4）を戻す：穴 y=1 は y=4 を軸に折ったので、広げると y=7（=8−1）にも対称に現れる。</p>
<p>・折り①（x=4）を戻す：穴 x=3 は x=4 を軸に折ったので、広げると x=5（=8−3）にも対称に現れる。</p>
<p>よって穴は <strong>(3,1)・(5,1)・(3,7)・(5,7)</strong> の4個。直線 x=4 と y=4 の両方について対称な配置になる。</p>
<p><strong>【選択肢の検討】</strong></p>
<p>・(1) 中心からの距離が誤り（y=2,6）→ 不正解</p>
<p>・(2) 折る向きを取り違え、x と y が入れ替わっている → 不正解</p>
<p>・(3) 折り②を戻し忘れ、下半分(y=1,3)だけ → 不正解</p>
<p>・(4) 穴の位置を隅(1,1)と誤認 → 不正解</p>
<p>・(5) 正しい4個の配置 → <strong>正解</strong></p>
<p>したがって、正解は<strong>(5)</strong>である。</p>"""

Q2_EXP = """<p>3回折ったので、3本の折り線 y=4・x=4・y=x のそれぞれについて鏡像が生じる。手順を逆順に戻して穴を増やす。</p>
<p><strong>【手順をさかのぼる】</strong></p>
<p>・折り③（対角線 y=x）を戻す：穴(3,1)は y=x に関して(1,3)にも対称に現れる。三角形内の穴は (3,1)・(1,3) の2個。</p>
<p>・折り②（x=4）を戻す：各穴に x→8−x の像が加わり (5,1)・(7,3) が増える。</p>
<p>・折り①（y=4）を戻す：各穴に y→8−y の像が加わり (3,7)・(1,5)・(5,7)・(7,5) が増える。</p>
<p>よって穴は <strong>(3,1)・(5,1)・(3,7)・(5,7)・(1,3)・(7,3)・(1,5)・(7,5)</strong> の8個。中心と両対角線について対称な配置になる。</p>
<p><strong>【選択肢の検討】</strong></p>
<p>・(1) 対角折り③を無視した4個 → 不正解</p>
<p>・(2) 直交2折りを無視した4個 → 不正解</p>
<p>・(3) 対角折りで生じる像の位置が誤り（x=2,6）→ 不正解</p>
<p>・(4) 正しい8個の配置 → <strong>正解</strong></p>
<p>・(5) 対角を別の向きで反映し位置が誤り（y=2,6）→ 不正解</p>
<p>したがって、正解は<strong>(4)</strong>である。</p>"""


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dyn_buttons(qnum, options, ans):
    out = []
    for n in range(1, 6):
        out.append(
            f'<button class="option-figure-button" data-option="{n}" '
            f'onclick="selectAnswer({qnum}, {n}, {ans})">\n        '
            f'{option_svg(options[n], f"({n})")}\n      </button>')
    return "\n      ".join(out)


def dyn_screen(qnum, active, text, title, film, options, ans, exp, meta, nav):
    cls = "screen active" if active else "screen"
    return f"""<div class="{cls}" id="q{qnum}-question">
      <div class="question-header">
        <span class="question-number">問{qnum}</span>
        <span class="question-meta">{meta}</span>
      </div>
      <div class="question-text">{text}</div>
      <div class="figure-container">
        <div class="figure-title">{title}</div>
        <div class="figure-content">{film}</div>
      </div>
      <div class="options-figure" id="q{qnum}-options">
      {dyn_buttons(qnum, options, ans)}
      </div>
      <div class="explanation-section" id="q{qnum}-explanation">
        <div class="explanation-header">問{qnum}（正解: ({ans})）</div>
        <div class="explanation-content">
{exp}
        </div>
      </div>
      <div class="nav-buttons" id="q{qnum}-nav" style="display: none;">
        {nav}
      </div>
    </div>"""


def build_dynamic():
    tpl = open(os.path.join(ROOT, 'template_dynamic.html'), encoding='utf-8').read()
    pre = tpl.split('<main class="main-content">')[0] + '<main class="main-content">\n'
    suf = '\n    </main>' + tpl.split('</main>', 1)[1]
    suf = suf.replace('2026_01/航大思考X/問', '2026_06/航大思考224/問')
    s1 = dyn_screen(1, True, Q1_TEXT, "【図1】折りの手順（格子は0〜8、左下が原点）",
                    filmstrip1(), P1_OPTIONS, P1_ANSWER, Q1_EXP,
                    "配点: 6点 / 目安時間: 3分",
                    '<button class="btn btn-secondary hidden">前の問題</button>\n'
                    '        <button class="btn btn-primary" onclick="goToQuestion(2)">問2へ</button>')
    s2 = dyn_screen(2, False, Q2_TEXT, "【図2】折りの手順（格子は0〜8、左下が原点）",
                    filmstrip2(), P2_OPTIONS, P2_ANSWER, Q2_EXP,
                    "配点: 6点 / 目安時間: 5分",
                    '<button class="btn btn-secondary" onclick="goToQuestion(1)">問1へ</button>\n'
                    '        <button class="btn btn-secondary hidden">（空欄）</button>')
    body = ('        <div class="progress-bar">\n'
            '            <div class="progress-dot" id="progress-1" onclick="goToQuestion(1)">1</div>\n'
            '            <div class="progress-dot" id="progress-2" onclick="goToQuestion(2)">2</div>\n'
            '        </div>\n\n        ' + s1 + '\n\n        ' + s2 + '\n')
    out = pre + body + suf
    path = os.path.join(ROOT, '航大思考問題', '航大思考224.html')
    open(path, 'w', encoding='utf-8').write(out)
    return path, len(out)


def stat_options(options):
    svgs = "\n          ".join(option_svg(options[n], f"({n})") for n in range(1, 6))
    return (f'<div class="figure-container" style="border: none; box-shadow: none;">\n'
            f'        <div class="figure-content">\n          {svgs}\n        </div>\n      </div>')


def stat_pages():
    q1 = f"""<div class="question-section question-page">
    <div class="page-content">
      <div class="question">
        <div class="question-number">問1．{Q1_TEXT}（6点）</div>
        <div class="figure-container">
          <div class="figure-title">【図1】折りの手順（格子は0〜8、左下が原点）</div>
          <div class="figure-content">{filmstrip1()}</div>
        </div>
        {stat_options(P1_OPTIONS)}
      </div>
    </div>
  </div>"""
    e1 = f"""<div class="question-section question-page">
    <div class="page-content">
      <div class="explanation">
        <strong>問1(正解:({P1_ANSWER}))</strong><br>
        {Q1_EXP.replace('<p>', '').replace('</p>', '<br>')}
      </div>
    </div>
  </div>"""
    q2 = f"""<div class="question-section question-page">
    <div class="page-content">
      <div class="question">
        <div class="question-number">問2．{Q2_TEXT}（6点）</div>
        <div class="figure-container">
          <div class="figure-title">【図2】折りの手順（格子は0〜8、左下が原点）</div>
          <div class="figure-content">{filmstrip2()}</div>
        </div>
        {stat_options(P2_OPTIONS)}
      </div>
    </div>
  </div>"""
    e2 = f"""<div class="question-section question-page">
    <div class="page-content">
      <div class="explanation">
        <strong>問2(正解:({P2_ANSWER}))</strong><br>
        {Q2_EXP.replace('<p>', '').replace('</p>', '<br>')}
      </div>
    </div>
  </div>"""
    return "\n\n  ".join([q1, e1, q2, e2])


def build_static():
    tpl = open(os.path.join(ROOT, 'template_static.html'), encoding='utf-8').read()
    pre = tpl.split('<body>')[0] + '<body>\n  '
    suf = '\n\n    ' + tpl[tpl.index('    <script>'):]
    out = pre + stat_pages() + suf
    path = os.path.join(ROOT, '印刷用', '印刷224.html')
    open(path, 'w', encoding='utf-8').write(out)
    return path, len(out)


if __name__ == '__main__':
    print("dynamic:", build_dynamic())
    print("static:", build_static())
