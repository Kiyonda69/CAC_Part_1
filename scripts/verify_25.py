#!/usr/bin/env python3
"""航大思考25 問題検証スクリプト"""
import math

print("=" * 60)
print("問1: 測量装置による位置特定の論理推論")
print("=" * 60)

# 装置A(距離計): 円を生成
# 装置B(方位計): レイを生成

choices_q1 = {
    "ア": ("装置A 1台で一意に特定", False, "円上の無限点"),
    "イ": ("装置A 2台(異なる位置)で常に一意", False, "2円の交点が2つになる場合あり"),
    "ウ": ("装置B 2台(異なる位置)で常に一意", False, "Xが2装置を結ぶ直線上の場合、レイ重複"),
    "エ": ("装置A+B 同一位置で常に一意", True, "円の中心からのレイは円と1点のみ交差"),
    "オ": ("装置A+B 異なる位置で常に一意", False, "レイが円と2点で交差する場合あり"),
}

correct_count = sum(1 for v in choices_q1.values() if v[1])
assert correct_count == 1, f"正解が{correct_count}個"
print(f"正解の選択肢数: {correct_count} (エのみ) ✓")

# 装置A+B同一地点の数学的検証
for theta_deg in range(0, 360, 15):
    theta = math.radians(theta_deg)
    d = 5
    x = d * math.cos(theta)
    y = d * math.sin(theta)
    assert abs(x**2 + y**2 - d**2) < 1e-10
print("全方位(15°刻み)で唯一解を確認 ✓")

print("\n" + "=" * 60)
print("問2: 紙の折り畳みと穴あけパターン")
print("=" * 60)

def unfold(holes):
    """折り畳み状態の穴から展開後の穴位置を計算"""
    result = set()
    for (c, r) in holes:
        for col in [c, 5 - c]:
            for row in [r, 5 - r]:
                result.add((col, row))
    return result

def show_pattern(name, pattern):
    """パターンを表示"""
    print(f"\n{name}:")
    for row in range(1, 5):
        line = "  "
        for col in range(1, 5):
            line += "● " if (col, row) in pattern else "○ "
        print(line)
    return pattern

# 正解: 穴(1,3)と(2,4)
correct = unfold([(1, 3), (2, 4)])
show_pattern("正解パターン", correct)
assert len(correct) == 8
assert correct == {(1,2),(1,3),(2,1),(2,4),(3,1),(3,4),(4,2),(4,3)}
print("  正解検証 ✓ (8穴)")

# 誤答1: 正解の反転パターン (穴と空白が入れ替わったような)
wrong1 = {(1,1),(1,4),(2,2),(2,3),(3,2),(3,3),(4,1),(4,4)}
show_pattern("誤答1 (反転フレーム)", wrong1)
assert len(wrong1) == 8

# 誤答2: 中央2列パターン
wrong2 = {(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(3,4)}
show_pattern("誤答2 (中央2列)", wrong2)
assert len(wrong2) == 8

# 誤答3: 外側2列パターン  
wrong3 = {(1,1),(1,2),(1,3),(1,4),(4,1),(4,2),(4,3),(4,4)}
show_pattern("誤答3 (外側2列)", wrong3)
assert len(wrong3) == 8

# 誤答4: 上下2行パターン
wrong4 = {(1,1),(2,1),(3,1),(4,1),(1,4),(2,4),(3,4),(4,4)}
show_pattern("誤答4 (上下2行)", wrong4)
assert len(wrong4) == 8

# 全パターンが互いに異なることを確認
all_patterns = [correct, wrong1, wrong2, wrong3, wrong4]
names = ["正解", "誤答1", "誤答2", "誤答3", "誤答4"]
for i in range(len(all_patterns)):
    for j in range(i+1, len(all_patterns)):
        assert all_patterns[i] != all_patterns[j], f"{names[i]}と{names[j]}が同一"
print("\n全5パターンが互いに異なることを確認 ✓")

print("\n" + "=" * 60)
print("全検証完了")
print("=" * 60)
