# -*- coding: utf-8 -*-
"""航大思考194 / 印刷194 を template から再構築する。
資料空欄穴埋め問題（製品生産表・部門人件費表）。
正解位置: 問1=(4) 値500, 問2=(3) 値330。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def splice(template_path, middle):
    with open(template_path, encoding="utf-8") as f:
        t = f.read()
    head = t[: t.index("<body>") + len("<body>")]
    tail = t[t.rindex("<script>"):]
    return head, tail

# ===================== 表HTML =====================
def cell(v, blank=False):
    if blank:
        return f'<td style="background-color:#e0e0e0;font-weight:bold;">{v}</td>'
    return f'<td>{v}</td>'

TABLE1 = (
    '<table class="figure-table">'
    '<tr><th>製品</th><th>1月</th><th>2月</th><th>3月</th><th>4月</th><th>行合計</th></tr>'
    '<tr><th>A</th>' + cell(120)+cell(150)+cell("ア",True)+cell(180)+cell(600) + '</tr>'
    '<tr><th>B</th>' + cell("イ",True)+cell(200)+cell(170)+cell(160)+cell(700) + '</tr>'
    '<tr><th>C</th>' + cell(140)+cell("ウ",True)+cell(190)+cell(210)+cell(720) + '</tr>'
    '<tr><th>月別合計</th>' + cell(430)+cell(530)+cell(510)+cell(550)+cell(2020) + '</tr>'
    '</table>'
)

TABLE2 = (
    '<table class="figure-table">'
    '<tr><th>部門</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th><th>行合計</th></tr>'
    '<tr><th>営業部</th>' + cell("ア",True)+cell("イ",True)+cell(350)+cell(400)+cell(1400) + '</tr>'
    '<tr><th>製造部</th>' + cell(300)+cell("ウ",True)+cell("エ",True)+cell(510)+cell(1770) + '</tr>'
    '<tr><th>開発部</th>' + cell(280)+cell(260)+cell("オ",True)+cell("カ",True)+cell(1190) + '</tr>'
    '<tr><th>管理部</th>' + cell(180)+cell(190)+cell(210)+cell("キ",True)+cell(780) + '</tr>'
    '<tr><th>四半期合計</th>' + cell(1090)+cell(1240)+cell(1350)+cell(1460)+cell(5140) + '</tr>'
    '</table>'
)

Q1_TEXT = ("ある工場の製品別・月別生産台数を下の【表1】に示す。各行（製品）には行合計、"
           "各列（月）には月別合計、右下に総合計が与えられている。表中の空欄ア・イ・ウに入る数値を求め、"
           "<strong>ア＋イ＋ウ</strong>の値を答えよ。")
Q2_TEXT = ("ある企業の部門別・四半期別の人件費（単位：万円）を下の【表2】に示す。各行（部門）には行合計、"
           "各列（四半期）には四半期合計、右下に総合計が与えられている。表中の空欄ア〜キに入る数値を順に求め、"
           "<strong>営業部の第1四半期（空欄ア）</strong>の人件費を答えよ。")

Q1_EXP = ("各製品の行合計から、その行で1つだけ空いているマスを引き算で求める。<br>"
          "ア（製品A・3月）＝600−(120＋150＋180)＝<strong>150</strong><br>"
          "イ（製品B・1月）＝700−(200＋170＋160)＝<strong>170</strong><br>"
          "ウ（製品C・2月）＝720−(140＋190＋210)＝<strong>180</strong><br>"
          "よって ア＋イ＋ウ＝150＋170＋180＝<strong>500</strong>。<br>"
          "月別合計（430・530・510・550）および総合計2020とも矛盾しない。")
Q2_EXP = ("「行または列で空欄が1つだけのところ」から順に確定していくと、次の一通りの順序でしか解けない。<br>"
          "キ（管理部Q4）＝780−(180＋190＋210)＝<strong>200</strong><br>"
          "カ（開発部Q4）：Q4列より 1460−(400＋510＋200)＝<strong>350</strong><br>"
          "オ（開発部Q3）：開発部行より 1190−(280＋260＋350)＝<strong>300</strong><br>"
          "エ（製造部Q3）：Q3列より 1350−(350＋300＋210)＝<strong>490</strong><br>"
          "ウ（製造部Q2）：製造部行より 1770−(300＋490＋510)＝<strong>470</strong><br>"
          "イ（営業部Q2）：Q2列より 1240−(470＋260＋190)＝<strong>320</strong><br>"
          "ア（営業部Q1）：営業部行より 1400−(320＋350＋400)＝<strong>330</strong><br>"
          "よって営業部の第1四半期の人件費は<strong>330万円</strong>。")

# 正解位置: Q1=(4)=500, Q2=(3)=330
Q1_OPTS = [("1","480"),("2","490"),("3","510"),("4","500"),("5","520")]
Q1_CORRECT = 4
Q2_OPTS = [("1","310"),("2","320"),("3","330"),("4","340"),("5","350")]
Q2_CORRECT = 3

# ===================== 静的（印刷用） =====================
def static_options(opts):
    rows = "<br>\n        ".join(f"({n}) {v}" for n, v in opts)
    return f'<div class="options">\n        {rows}\n      </div>'

def static_qpage(qnum, text, table, opts):
    return (
f'''    <div class="question-section question-page">
      <div class="page-content">
        <div class="question">
          <div class="question-number">問{qnum}．{text}（6点）</div>
          <div class="figure-container">
            <div class="figure-title">【表{qnum}】{"製品別・月別生産台数（単位：台）" if qnum==1 else "部門別・四半期別人件費（単位：万円）"}</div>
            <div class="figure-content">{table}</div>
          </div>
          {static_options(opts)}
        </div>
      </div>
    </div>''')

def static_exp(qnum, correct, exp):
    return (
f'''    <div class="question-section question-page">
      <div class="page-content">
        <div class="explanation">
          <strong>問{qnum}(正解:({correct}))</strong><br>
          {exp}
        </div>
      </div>
    </div>''')

STATIC_MIDDLE = "\n".join([
    static_qpage(1, Q1_TEXT, TABLE1, Q1_OPTS),
    static_exp(1, Q1_CORRECT, Q1_EXP),
    static_qpage(2, Q2_TEXT, TABLE2, Q2_OPTS),
    static_exp(2, Q2_CORRECT, Q2_EXP),
])

# ===================== 動的（航大思考） =====================
def dyn_buttons(qnum, opts, correct):
    btns = []
    for n, v in opts:
        btns.append(
            f'        <button class="option-button" data-option="{n}" '
            f'onclick="selectAnswer({qnum}, {n}, {correct})">'
            f'<span class="option-label">({n})</span>{v}</button>')
    return "\n".join(btns)

def dyn_screen(qnum, active, text, table, opts, correct, exp, meta, nav):
    cls = "screen active" if active else "screen"
    tnum = qnum
    title = "製品別・月別生産台数（単位：台）" if qnum == 1 else "部門別・四半期別人件費（単位：万円）"
    return (
f'''    <div class="{cls}" id="q{qnum}-question">
      <div class="question-header">
        <span class="question-number">問{qnum}</span>
        <span class="question-meta">{meta}</span>
      </div>
      <div class="question-text">{text}</div>
      <div class="figure-container">
        <div class="figure-title">【表{tnum}】{title}</div>
        <div class="figure-content">{table}</div>
      </div>
      <div class="options-container" id="q{qnum}-options">
{dyn_buttons(qnum, opts, correct)}
      </div>
      <div class="explanation-section" id="q{qnum}-explanation">
        <div class="explanation-header">解説（正解: ({correct})）</div>
        <div class="explanation-content"><p>{exp}</p></div>
      </div>
      <div class="nav-buttons" id="q{qnum}-nav" style="display: none;">
{nav}
      </div>
    </div>''')

NAV1 = ('        <button class="btn btn-secondary hidden">前の問題</button>\n'
        '        <button class="btn btn-primary" onclick="goToQuestion(2)">問2へ</button>')
NAV2 = ('        <button class="btn btn-secondary" onclick="goToQuestion(1)">問1へ</button>\n'
        '        <button class="btn btn-secondary hidden">次へ</button>')

DYN_MIDDLE = (
'''    <main class="main-content">
      <div class="progress-bar">
        <div class="progress-dot" id="progress-1" onclick="goToQuestion(1)">1</div>
        <div class="progress-dot" id="progress-2" onclick="goToQuestion(2)">2</div>
      </div>
'''
+ dyn_screen(1, True, Q1_TEXT, TABLE1, Q1_OPTS, Q1_CORRECT, Q1_EXP, "配点: 6点 / 目安時間: 3分", NAV1) + "\n"
+ dyn_screen(2, False, Q2_TEXT, TABLE2, Q2_OPTS, Q2_CORRECT, Q2_EXP, "配点: 6点 / 目安時間: 5分", NAV2) + "\n"
+ "    </main>")

# ===================== 出力 =====================
sh, st = splice(os.path.join(ROOT, "template_static.html"), STATIC_MIDDLE)
static_out = sh + "\n" + STATIC_MIDDLE + "\n" + st
with open(os.path.join(ROOT, "印刷用/印刷194.html"), "w", encoding="utf-8") as f:
    f.write(static_out)

dh, dt = splice(os.path.join(ROOT, "template_dynamic.html"), DYN_MIDDLE)
dt = dt.replace("2026_01/航大思考X", "2026_05/航大思考194")
dyn_out = dh + "\n" + DYN_MIDDLE + "\n" + dt
with open(os.path.join(ROOT, "航大思考問題/航大思考194.html"), "w", encoding="utf-8") as f:
    f.write(dyn_out)

print("WROTE static=%d dynamic=%d" % (len(static_out), len(dyn_out)))
print("recordAnswer_fixed=%s" % ("2026_05/航大思考194" in dyn_out))

