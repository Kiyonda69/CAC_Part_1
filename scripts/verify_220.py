"""航大思考220 検証スクリプト

テーマ: 航空機の機首方位（メンタルローテーション / 空間認識）
- 北を上、東を右とする地図上で、機影（上から見た飛行機）の向きを追跡する。
- 機首方位は北(0°)から時計回りに測る。右旋回=+、左旋回=-。
- 各選択肢は8方位のいずれかを向いた機影。最終方位と一致するものが唯一の正解。
"""

# 8方位（時計回り、北=0）
DIRS = {
    0: "北", 45: "北東", 90: "東", 135: "南東",
    180: "南", 225: "南西", 270: "西", 315: "北西",
}


def final_heading(start, turns):
    """start から turns（右旋回=正, 左旋回=負）を順に適用した最終方位"""
    h = start
    for t in turns:
        h = (h + t) % 360
    return h


def verify(start, turns, options, correct_slot):
    final = final_heading(start, turns)
    # 各選択肢のうち最終方位と一致するものを数える
    matches = [i + 1 for i, d in enumerate(options) if d % 360 == final]
    assert len(matches) == 1, f"一致する選択肢が{len(matches)}個（唯一解でない）: {matches}"
    assert matches[0] == correct_slot, f"正解スロット不一致: 実際={matches[0]}, 想定={correct_slot}"
    # 選択肢の方位に重複がないこと（紛らわしさの担保）
    assert len(set(d % 360 for d in options)) == 5, "選択肢の方位に重複がある"
    return final


# ===== 問1（標準）: 北を向いて離陸 → 右135° → 右90° =====
q1_start = 0
q1_turns = [135, 90]
q1_options = [135, 180, 45, 225, 270]  # slot1..5
q1_correct = 4
q1_final = verify(q1_start, q1_turns, q1_options, q1_correct)
print(f"問1: 最終方位 = {q1_final}° ({DIRS[q1_final]}) / 正解 = ({q1_correct})")

# ===== 問2（高難度）: 北東を向いて飛行 → 右90° → 右180° → 左45° → 左135° =====
q2_start = 45
q2_turns = [90, 180, -45, -135]
q2_options = [135, 45, 225, 315, 90]  # slot1..5
q2_correct = 1
q2_final = verify(q2_start, q2_turns, q2_options, q2_correct)
print(f"問2: 最終方位 = {q2_final}° ({DIRS[q2_final]}) / 正解 = ({q2_correct})")

# 途中経過の表示（解説の検算用）
def trace(start, turns):
    h = start
    seq = [f"{h}°({DIRS[h]})"]
    for t in turns:
        h = (h + t) % 360
        seq.append(f"{h}°({DIRS[h]})")
    return " → ".join(seq)

print("問1 経過:", trace(q1_start, q1_turns))
print("問2 経過:", trace(q2_start, q2_turns))
print("検証OK: 両問とも唯一解")
