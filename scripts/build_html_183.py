"""
航大思考183: 印刷用・動的HTMLを組み立てる
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_boxplot_svg_183 import gen_boxplot_svg, Q1_BOXES, Q2_BOXES


# 問1の正解番号（クラスCの表示位置）
Q1_ANSWER = 3
# 問2の正解番号（クラスCの表示位置）
Q2_ANSWER = 1


# ============================================================
# 共通: 問題説明文
# ============================================================
Q1_TEXT = (
    "ある中学校の5つのクラスA, B, C, D, Eで同じ100点満点のテストを実施し、"
    "下図のように各クラスの結果を箱ひげ図で表した。ただし、図の(1)〜(5)は"
    "A〜Eのいずれかに対応するが、その順序は不明である。次のア〜エの条件が"
    "すべて成り立つとき、クラスCを表す箱ひげ図として正しいものを(1)〜(5)の"
    "中から1つ選べ。"
)

Q1_CONDITIONS = [
    "ア. クラスAの中央値は、5クラスの中で最も小さい。",
    "イ. クラスBの範囲（最大値 − 最小値）は、5クラスの中で最も大きい。",
    "ウ. クラスDの四分位範囲（第3四分位数 − 第1四分位数）は、5クラスの中で最も小さい。",
    "エ. クラスEの最小値は、5クラスの中で最も大きい。",
]

Q2_TEXT = (
    "ある高校の5つのクラスA, B, C, D, Eで同じ100点満点のテストを実施し、"
    "下図のように各クラスの結果を箱ひげ図で表した。ただし、図の(1)〜(5)は"
    "A〜Eのいずれかに対応するが、その順序は不明である。次のア〜オの条件が"
    "すべて成り立つとき、クラスCを表す箱ひげ図として正しいものを(1)〜(5)の"
    "中から1つ選べ。"
)

Q2_CONDITIONS = [
    "ア. クラスEの最小値は、クラスAの最小値より15点大きい。",
    "イ. クラスBの第1四分位数は、クラスDの第1四分位数より5点小さい。",
    "ウ. クラスCの中央値は、クラスEの中央値より5点小さい。",
    "エ. クラスDの範囲（最大値 − 最小値）は、5クラスの中で最も大きい。",
    "オ. クラスEの第3四分位数は、クラスAの第3四分位数より20点大きい。",
]


# ============================================================
# 解説文
# ============================================================
Q1_EXPLANATION_HTML = f"""
<strong>問1（正解: ({Q1_ANSWER})）</strong><br><br>
各箱ひげ図の統計値を読み取って整理する。<br><br>

<strong>【各箱ひげ図の統計値】</strong><br>
・(1): 最小値25, Q1=45, 中央値60, Q3=75, 最大値85 → 範囲60, 四分位範囲30<br>
・(2): 最小値5, Q1=15, 中央値30, Q3=50, 最大値70 → 範囲65, 四分位範囲35<br>
・(3): 最小値15, Q1=35, 中央値50, Q3=70, 最大値85 → 範囲70, 四分位範囲35<br>
・(4): 最小値10, Q1=20, 中央値45, Q3=65, 最大値90 → 範囲80, 四分位範囲45<br>
・(5): 最小値20, Q1=40, 中央値55, Q3=60, 最大値80 → 範囲60, 四分位範囲20<br><br>

<strong>【条件による特定】</strong><br>
・条件ア（Aの中央値が最小）→ 中央値: 60, 30, 50, 45, 55 のうち最小は(2)の30。よってA=(2)。<br>
・条件イ（Bの範囲が最大）→ 範囲: 60, 65, 70, 80, 60 のうち最大は(4)の80。よってB=(4)。<br>
・条件ウ（Dの四分位範囲が最小）→ 四分位範囲: 30, 35, 35, 45, 20 のうち最小は(5)の20。よってD=(5)。<br>
・条件エ（Eの最小値が最大）→ 最小値: 25, 5, 15, 10, 20 のうち最大は(1)の25。よってE=(1)。<br><br>

A=(2), B=(4), D=(5), E=(1) と特定できたので、残る(3)がクラスCである。<br><br>

したがって、正解は<strong>({Q1_ANSWER})</strong>である。
"""

Q2_EXPLANATION_HTML = f"""
<strong>問2（正解: ({Q2_ANSWER})）</strong><br><br>
各箱ひげ図の統計値を整理し、条件を順に適用してA〜Eを特定する。<br><br>

<strong>【各箱ひげ図の統計値】</strong><br>
・(1): 最小値20, Q1=35, 中央値50, Q3=65, 最大値90 → 範囲70<br>
・(2): 最小値10, Q1=20, 中央値35, Q3=55, 最大値70 → 範囲60<br>
・(3): 最小値25, Q1=40, 中央値55, Q3=75, 最大値95 → 範囲70<br>
・(4): 最小値15, Q1=25, 中央値40, Q3=60, 最大値80 → 範囲65<br>
・(5): 最小値5, Q1=30, 中央値45, Q3=70, 最大値85 → 範囲80<br><br>

<strong>【条件による特定（段階的推論）】</strong><br>

<strong>手順1: 条件エから D を特定</strong><br>
範囲: (1)=70, (2)=60, (3)=70, (4)=65, (5)=80。最大は(5)の80のみ。<br>
→ <strong>D = (5)</strong>（Dの第1四分位数 = 30）<br><br>

<strong>手順2: 条件イから B を特定</strong><br>
BのQ1 = DのQ1 − 5 = 30 − 5 = 25。Q1=25である箱ひげ図は(4)のみ。<br>
→ <strong>B = (4)</strong><br><br>

<strong>手順3: 条件アから (A, E) のペアを絞り込む</strong><br>
残るのは (1), (2), (3)。これらの最小値はそれぞれ 20, 10, 25。<br>
Eの最小値 − Aの最小値 = 15 となる組み合わせは、(A=10, E=25) のみ、<br>
すなわち <strong>A = (2), E = (3)</strong>。<br><br>

<strong>手順4: 条件オで検証</strong><br>
EのQ3 − AのQ3 = 75 − 55 = 20。条件オに一致 ✓<br><br>

<strong>手順5: 残った (1) が C</strong><br>
条件ウで検証: CのEからの中央値差 = Eの中央値 − Cの中央値 = 55 − 50 = 5 ✓<br><br>

したがって、クラスC = <strong>({Q2_ANSWER})</strong> である。
"""


# ============================================================
# 印刷用HTML生成
# ============================================================
def build_static_html():
    svg_q1 = gen_boxplot_svg(Q1_BOXES)
    svg_q2 = gen_boxplot_svg(Q2_BOXES)

    q1_conditions_html = "<br>".join(Q1_CONDITIONS)
    q2_conditions_html = "<br>".join(Q2_CONDITIONS)

    head = open(os.path.join(os.path.dirname(__file__), '..', '印刷用', '印刷183.html')).read()
    # We already created the head portion. We need to overwrite the file completely.

    style_part = head.split('<body>')[0] + '<body>\n'

    body = f"""
<!-- ========== 問1 問題ページ ========== -->
<div class="question-section question-page">
<div class="page-content">
<div class="question">
<div class="question-number">問1．{Q1_TEXT}（6点）</div>

<div class="figure-container">
<div class="figure-title">【図1】各クラスの箱ひげ図</div>
<div class="figure-content">
{svg_q1}
</div>
</div>

<div style="margin: 12px 0 5px 0;"><strong>【条件】</strong></div>
<div class="options">
{q1_conditions_html}
</div>

<div style="margin-top: 15px;">クラスCを表す箱ひげ図はどれか。</div>
<div class="options">
(1) 図の(1)　(2) 図の(2)　(3) 図の(3)　(4) 図の(4)　(5) 図の(5)
</div>
</div>
</div>
</div>

<!-- ========== 問1 解説ページ ========== -->
<div class="question-section question-page">
<div class="page-content">
<div class="explanation">
{Q1_EXPLANATION_HTML}
</div>
</div>
</div>

<!-- ========== 問2 問題ページ ========== -->
<div class="question-section question-page">
<div class="page-content">
<div class="question">
<div class="question-number">問2．{Q2_TEXT}（6点）</div>

<div class="figure-container">
<div class="figure-title">【図2】各クラスの箱ひげ図</div>
<div class="figure-content">
{svg_q2}
</div>
</div>

<div style="margin: 12px 0 5px 0;"><strong>【条件】</strong></div>
<div class="options">
{q2_conditions_html}
</div>

<div style="margin-top: 15px;">クラスCを表す箱ひげ図はどれか。</div>
<div class="options">
(1) 図の(1)　(2) 図の(2)　(3) 図の(3)　(4) 図の(4)　(5) 図の(5)
</div>
</div>
</div>
</div>

<!-- ========== 問2 解説ページ ========== -->
<div class="question-section question-page">
<div class="page-content">
<div class="explanation">
{Q2_EXPLANATION_HTML}
</div>
</div>
</div>

<script>
function scalePages() {{
    const pages = document.querySelectorAll('.question-section');
    const baseWidth = 800;
    const viewportWidth = window.innerWidth;
    const padding = 40;
    const scale = Math.min(1, (viewportWidth - padding) / baseWidth);
    pages.forEach(page => {{
        page.style.transform = `scale(${{scale}})`;
        const originalHeight = page.offsetHeight / scale;
        const scaledHeight = originalHeight * scale;
        page.style.marginBottom = `${{20 - (originalHeight - scaledHeight)}}px`;
    }});
}}
window.addEventListener('load', scalePages);
window.addEventListener('resize', scalePages);
</script>
</body>
</html>
"""

    full = style_part + body
    out_path = os.path.join(os.path.dirname(__file__), '..', '印刷用', '印刷183.html')
    with open(out_path, 'w') as f:
        f.write(full)
    print(f"印刷183.html を作成: {len(full)} 文字")


if __name__ == "__main__":
    build_static_html()
