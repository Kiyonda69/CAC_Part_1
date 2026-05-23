"""
航大思考183.html に問題コンテンツを追加する
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_boxplot_svg_183 import gen_boxplot_svg, Q1_BOXES, Q2_BOXES

Q1_ANSWER = 3
Q2_ANSWER = 1

# ============================================================
# 解説（HTMLフラグメント）
# ============================================================
Q1_EXPLANATION = f"""
<p>各箱ひげ図の統計値を整理し、条件を満たすクラスを順に特定する。</p><br>

<p><strong>【各箱ひげ図の統計値】</strong></p>
<p>・(1): 最小値25, Q1=45, 中央値60, Q3=75, 最大値85 → 範囲60, 四分位範囲30</p>
<p>・(2): 最小値5, Q1=15, 中央値30, Q3=50, 最大値70 → 範囲65, 四分位範囲35</p>
<p>・(3): 最小値15, Q1=35, 中央値50, Q3=70, 最大値85 → 範囲70, 四分位範囲35</p>
<p>・(4): 最小値10, Q1=20, 中央値45, Q3=65, 最大値90 → 範囲80, 四分位範囲45</p>
<p>・(5): 最小値20, Q1=40, 中央値55, Q3=60, 最大値80 → 範囲60, 四分位範囲20</p><br>

<p><strong>【条件による特定】</strong></p>
<p>・条件ア（Aの中央値が最小）→ 中央値: 60, 30, 50, 45, 55 のうち最小は(2)の30。<strong>A=(2)</strong>。</p>
<p>・条件イ（Bの範囲が最大）→ 範囲: 60, 65, 70, 80, 60 のうち最大は(4)の80。<strong>B=(4)</strong>。</p>
<p>・条件ウ（Dの四分位範囲が最小）→ 四分位範囲: 30, 35, 35, 45, 20 のうち最小は(5)の20。<strong>D=(5)</strong>。</p>
<p>・条件エ（Eの最小値が最大）→ 最小値: 25, 5, 15, 10, 20 のうち最大は(1)の25。<strong>E=(1)</strong>。</p><br>

<p>A=(2), B=(4), D=(5), E=(1) が特定できたので、残る (3) がクラスCである。</p><br>

<p>したがって、正解は <strong>({Q1_ANSWER})</strong> である。</p>
"""

Q2_EXPLANATION = f"""
<p>各箱ひげ図の統計値を整理し、条件を段階的に適用する。</p><br>

<p><strong>【各箱ひげ図の統計値】</strong></p>
<p>・(1): 最小値20, Q1=35, 中央値50, Q3=65, 最大値90 → 範囲70</p>
<p>・(2): 最小値10, Q1=20, 中央値35, Q3=55, 最大値70 → 範囲60</p>
<p>・(3): 最小値25, Q1=40, 中央値55, Q3=75, 最大値95 → 範囲70</p>
<p>・(4): 最小値15, Q1=25, 中央値40, Q3=60, 最大値80 → 範囲65</p>
<p>・(5): 最小値5, Q1=30, 中央値45, Q3=70, 最大値85 → 範囲80</p><br>

<p><strong>【条件による段階的推論】</strong></p>

<p><strong>手順1: 条件エから D を特定</strong></p>
<p>範囲: 70, 60, 70, 65, 80 のうち最大は(5)の80のみ。よって <strong>D = (5)</strong>（DのQ1=30）。</p><br>

<p><strong>手順2: 条件イから B を特定</strong></p>
<p>BのQ1 = DのQ1 − 5 = 30 − 5 = 25。Q1=25 の箱ひげ図は(4)のみ。よって <strong>B = (4)</strong>。</p><br>

<p><strong>手順3: 条件アから A と E を特定</strong></p>
<p>残るのは (1), (2), (3)。最小値はそれぞれ 20, 10, 25。</p>
<p>Eの最小値 − Aの最小値 = 15 となる組は (A=10, E=25) のみ。すなわち <strong>A = (2), E = (3)</strong>。</p><br>

<p><strong>手順4: 条件オで検証</strong></p>
<p>EのQ3 − AのQ3 = 75 − 55 = 20 ✓（条件オに一致）</p><br>

<p><strong>手順5: 残った (1) が C</strong></p>
<p>条件ウで検証: Eの中央値 − Cの中央値 = 55 − 50 = 5 ✓（条件ウに一致）</p><br>

<p>したがって、正解は <strong>({Q2_ANSWER})</strong> である。</p>
"""


def build_q_screen(qnum, q_meta_time, q_text, conditions, svg, figure_title, answer):
    """1問分のscreen divを生成"""
    options_html = "\n".join(
        f'<button class="option-button" data-option="{i}" '
        f'onclick="selectAnswer({qnum}, {i}, {answer})">'
        f'<span class="option-label">({i})</span>図の({i})の箱ひげ図'
        f'</button>'
        for i in range(1, 6)
    )
    conditions_html = "<br>".join(conditions)
    explanation = Q1_EXPLANATION if qnum == 1 else Q2_EXPLANATION
    active_class = " active" if qnum == 1 else ""

    # ナビゲーション
    if qnum == 1:
        nav = (
            '<button class="btn btn-secondary hidden">前の問題</button>\n'
            '<button class="btn btn-primary" onclick="goToQuestion(2)">問2へ</button>'
        )
    else:
        nav = (
            '<button class="btn btn-secondary" onclick="goToQuestion(1)">問1へ</button>\n'
            '<button class="btn btn-secondary hidden">（空欄）</button>'
        )

    return f"""
<!-- ========== 問{qnum} 問題画面 ========== -->
<div class="screen{active_class}" id="q{qnum}-question">
<div class="question-header">
<span class="question-number">問{qnum}</span>
<span class="question-meta">配点: 6点 / 目安時間: {q_meta_time}</span>
</div>

<div class="question-text">{q_text}</div>

<div class="figure-container">
<div class="figure-title">{figure_title}</div>
<div class="figure-content">
{svg}
</div>
</div>

<div class="condition-box">
<div class="condition-title">【条件】</div>
{conditions_html}
</div>

<div class="question-text" style="margin-top:18px;">
クラスCを表す箱ひげ図はどれか、(1)〜(5)の中から1つ選べ。
</div>

<div class="options-container" id="q{qnum}-options">
{options_html}
</div>

<div class="explanation-section" id="q{qnum}-explanation">
<div class="explanation-header">問{qnum}（正解: ({answer})）の解説</div>
<div class="explanation-content">
{explanation}
</div>
</div>

<div class="nav-buttons" id="q{qnum}-nav" style="display: none;">
{nav}
</div>
</div>
"""


JS = """
<script>
const state = { currentQuestion: 1, answers: {} };

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
    window.scrollTo(0, 0);
}

function goToQuestion(questionNum) {
    state.currentQuestion = questionNum;
    showScreen(`q${questionNum}-question`);
    if (state.answers[questionNum] === undefined) {
        document.querySelectorAll('.progress-dot').forEach(dot => {
            const dotNum = parseInt(dot.textContent);
            if (state.answers[dotNum] === undefined) {
                dot.classList.remove('active');
            }
        });
        document.getElementById(`progress-${questionNum}`).classList.add('active');
    }
}

function startQuestion(questionNum) { goToQuestion(questionNum); }

function selectAnswer(questionNum, selectedOption, correctOption) {
    const optionsContainer = document.getElementById(`q${questionNum}-options`);
    const buttons = optionsContainer.querySelectorAll('.option-figure-button, .option-button');

    if (state.answers[questionNum] !== undefined) {
        state.answers[questionNum] = undefined;
        buttons.forEach(btn => btn.classList.remove('selected', 'correct', 'incorrect'));
        document.getElementById(`q${questionNum}-explanation`).classList.remove('show');
        document.getElementById(`q${questionNum}-nav`).style.display = 'none';
        const progressDot = document.getElementById(`progress-${questionNum}`);
        progressDot.classList.remove('completed', 'incorrect-dot');
        progressDot.classList.add('active');
        return;
    }

    state.answers[questionNum] = selectedOption;
    const isCorrect = selectedOption === correctOption;

    try {
        if (window.parent && window.parent.recordAnswer) {
            window.parent.recordAnswer(
                `2026_05/航大思考183/問${questionNum}`,
                selectedOption, correctOption, isCorrect
            );
        }
    } catch (e) {}

    buttons.forEach(btn => {
        btn.classList.remove('selected', 'correct', 'incorrect');
        const option = parseInt(btn.dataset.option);
        if (option === selectedOption) {
            btn.classList.add('selected');
            if (!isCorrect) btn.classList.add('incorrect');
        }
        if (option === correctOption) btn.classList.add('correct');
    });

    const progressDot = document.getElementById(`progress-${questionNum}`);
    progressDot.classList.remove('active');
    progressDot.classList.add(isCorrect ? 'completed' : 'incorrect-dot');

    const explanationSection = document.getElementById(`q${questionNum}-explanation`);
    explanationSection.classList.add('show');
    document.getElementById(`q${questionNum}-nav`).style.display = 'flex';

    setTimeout(() => {
        explanationSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('progress-1').classList.add('active');
});
</script>
</main>
</body>
</html>
"""


HEAD_HTML = """<!--
================================================================================
航大思考183.html - セット183: 箱ひげ図問題（インタラクティブ版）
================================================================================
問1（標準）: 5クラスA-Eの箱ひげ図、4条件でクラスCを特定
問2（高難度）: 5クラスA-Eの箱ひげ図、5条件（連鎖推論）でクラスCを特定
================================================================================
-->
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>航空大学校入学試験 総合Part I 思考パズル問題</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: "ヒラギノ明朝 ProN", "Hiragino Mincho ProN", "游明朝", "Yu Mincho", serif;
    font-size: 16px; line-height: 1.8;
    background-color: #f5f5f5; min-height: 100vh;
}
.main-content { max-width: 800px; margin: 0 auto; padding: 20px 20px 40px; }
.screen { display: none; background-color: white; padding: 30px; border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.screen.active { display: block; }
.question-header { display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #333; }
.question-number { font-weight: bold; font-size: 18px; }
.question-meta { font-size: 14px; color: #666; }
.question-text { margin-bottom: 18px; text-align: justify; }
.condition-box {
    margin: 16px 0; padding: 16px 20px;
    background-color: #fafafa; border: 1px solid #ddd; border-radius: 4px;
    line-height: 2;
}
.condition-title { font-weight: bold; margin-bottom: 6px; }
.figure-container {
    margin: 18px 0; padding: 20px; background-color: #fafafa;
    border: 1px solid #ddd; border-radius: 4px; text-align: center;
}
.figure-title { font-weight: bold; margin-bottom: 15px; font-size: 15px; }
.figure-content { display: inline-block; margin: 10px auto; }
svg { max-width: 100%; height: auto; }
.svg-text {
    font-family: "ヒラギノ明朝 ProN", "Hiragino Mincho ProN", "游明朝", "Yu Mincho", serif;
    font-size: 14px;
}
.options-container { margin: 18px 0; }
.option-button {
    display: block; width: 100%; padding: 14px 20px; margin: 8px 0;
    background-color: white; border: 2px solid #ddd; border-radius: 8px;
    text-align: left; cursor: pointer; transition: all 0.2s ease;
    font-family: inherit; font-size: 16px;
}
.option-button:hover:not(.disabled) { border-color: #666; background-color: #f9f9f9; }
.option-button.selected { border-color: #2196F3; background-color: #e3f2fd; }
.option-button.correct { border-color: #4CAF50; background-color: #e8f5e9; }
.option-button.incorrect { border-color: #f44336; background-color: #ffebee; }
.option-button.disabled { cursor: default; opacity: 0.8; }
.option-button .option-label { font-weight: bold; margin-right: 10px; }
.btn { padding: 12px 30px; font-size: 16px; font-family: inherit; border: none;
    border-radius: 8px; cursor: pointer; transition: all 0.2s ease; }
.btn-primary { background-color: #2196F3; color: white; }
.btn-primary:hover { background-color: #1976D2; }
.btn-secondary { background-color: #666; color: white; }
.btn-secondary:hover { background-color: #555; }
.explanation-section { display: none; margin-top: 30px; padding: 25px;
    background-color: #f8f9fa; border: 1px solid #ddd; border-radius: 8px; }
.explanation-section.show { display: block; }
.explanation-header { font-weight: bold; font-size: 16px; margin-bottom: 15px;
    padding-bottom: 10px; border-bottom: 2px solid #333; }
.explanation-content { line-height: 2; }
.explanation-content strong { color: #333; }
.progress-bar { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }
.progress-dot { width: 32px; height: 32px; border-radius: 50%; background-color: #ddd;
    cursor: pointer; display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: bold; color: #666; transition: all 0.2s ease; }
.progress-dot:hover { transform: scale(1.1); }
.progress-dot.active { background-color: #2196F3; color: white; }
.progress-dot.completed { background-color: #4CAF50; color: white; }
.progress-dot.incorrect-dot { background-color: #f44336; color: white; }
.nav-buttons { display: flex; justify-content: space-between; margin-top: 20px;
    padding-top: 20px; border-top: 1px solid #eee; }
.nav-buttons .btn { min-width: 120px; }
.nav-buttons .btn.hidden { visibility: hidden; }
</style>
</head>
<body>
<main class="main-content">
<div class="progress-bar">
<div class="progress-dot" id="progress-1" onclick="goToQuestion(1)">1</div>
<div class="progress-dot" id="progress-2" onclick="goToQuestion(2)">2</div>
</div>
"""


def main():
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, '..', '航大思考問題', '航大思考183.html')

    head_content = HEAD_HTML

    # 問1, 問2 を組み立て
    q1_text = (
        "ある中学校の5つのクラスA, B, C, D, Eで同じ100点満点のテストを実施し、"
        "下図のように各クラスの結果を箱ひげ図で表した。ただし、図の(1)〜(5)は"
        "A〜Eのいずれかに対応するが、その順序は不明である。次のア〜エの条件が"
        "すべて成り立つとき、クラスCを表す箱ひげ図を求めよ。"
    )
    q1_conditions = [
        "ア. クラスAの中央値は、5クラスの中で最も小さい。",
        "イ. クラスBの範囲（最大値 − 最小値）は、5クラスの中で最も大きい。",
        "ウ. クラスDの四分位範囲（第3四分位数 − 第1四分位数）は、5クラスの中で最も小さい。",
        "エ. クラスEの最小値は、5クラスの中で最も大きい。",
    ]

    q2_text = (
        "ある高校の5つのクラスA, B, C, D, Eで同じ100点満点のテストを実施し、"
        "下図のように各クラスの結果を箱ひげ図で表した。ただし、図の(1)〜(5)は"
        "A〜Eのいずれかに対応するが、その順序は不明である。次のア〜オの条件が"
        "すべて成り立つとき、クラスCを表す箱ひげ図を求めよ。"
    )
    q2_conditions = [
        "ア. クラスEの最小値は、クラスAの最小値より15点大きい。",
        "イ. クラスBの第1四分位数は、クラスDの第1四分位数より5点小さい。",
        "ウ. クラスCの中央値は、クラスEの中央値より5点小さい。",
        "エ. クラスDの範囲（最大値 − 最小値）は、5クラスの中で最も大きい。",
        "オ. クラスEの第3四分位数は、クラスAの第3四分位数より20点大きい。",
    ]

    svg_q1 = gen_boxplot_svg(Q1_BOXES)
    svg_q2 = gen_boxplot_svg(Q2_BOXES)

    q1_screen = build_q_screen(1, "3分", q1_text, q1_conditions, svg_q1,
                                "【図1】各クラスの箱ひげ図", Q1_ANSWER)
    q2_screen = build_q_screen(2, "5分", q2_text, q2_conditions, svg_q2,
                                "【図2】各クラスの箱ひげ図", Q2_ANSWER)

    full = head_content + q1_screen + q2_screen + JS
    with open(path, 'w') as f:
        f.write(full)
    print(f"航大思考183.html を作成: {len(full)} 文字")


if __name__ == "__main__":
    main()
