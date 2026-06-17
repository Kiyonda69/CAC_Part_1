# -*- coding: utf-8 -*-
"""航大思考232 箱ひげ図問題の検証
問1: 5組の箱ひげ図の読み取り（唯一の正文）
問2: 2クラス比較＋箱ひげ図から判断可能か（唯一の正しい組合せ）
"""
import random

# ===== 問1: 5組の5数要約 (最小, Q1, 中央値, Q3, 最大) =====
boxes = {
    "A": (30, 45, 60, 75, 90),
    "B": (40, 55, 65, 72, 85),
    "C": (25, 48, 55, 82, 95),
    "D": (35, 58, 70, 80, 100),
    "E": (45, 50, 58, 62, 75),
}

def rng(b):  return b[4] - b[0]      # 範囲
def iqr(b):  return b[3] - b[1]      # 四分位範囲
def med(b):  return b[2]
def mx(b):   return b[4]
def mn(b):   return b[1]  # Q1 (使わない)

ranges = {k: rng(v) for k, v in boxes.items()}
iqrs   = {k: iqr(v) for k, v in boxes.items()}
meds   = {k: v[2]   for k, v in boxes.items()}
maxs   = {k: v[4]   for k, v in boxes.items()}
mins   = {k: v[0]   for k, v in boxes.items()}

print("範囲:", ranges, "→最大", max(ranges, key=ranges.get))
print("IQR :", iqrs, "→最大", max(iqrs, key=iqrs.get), "最小", min(iqrs, key=iqrs.get))
print("中央値:", meds, "→最大", max(meds, key=meds.get))
print("最大値:", maxs, "→最大", max(maxs, key=maxs.get))
print("最小値:", mins, "→最小", min(mins, key=mins.get))

# 候補となる5つの記述（True/Falseを評価）
statements_q1 = {
    "範囲が最も大きいのはD組である":        max(ranges, key=ranges.get) == "D",
    "四分位範囲が最も大きいのはB組である":  max(iqrs, key=iqrs.get) == "B",
    "中央値が最も高いのはD組である":        max(meds, key=meds.get) == "D",
    "最大値が最も高いのはA組である":        max(maxs, key=maxs.get) == "A",
    "四分位範囲が最も小さいのはC組である":  min(iqrs, key=iqrs.get) == "C",
}
true_q1 = [s for s, v in statements_q1.items() if v]
print("\n[問1] 正しい記述:", true_q1)
assert len(true_q1) == 1, f"正文が{len(true_q1)}個"

# ===== 問2: 2クラスの5数要約 (n=40) =====
X = (30, 50, 65, 80, 95)
Y = (40, 52, 60, 88, 100)
print("\nX:", X, "range", X[4]-X[0], "IQR", X[3]-X[1])
print("Y:", Y, "range", Y[4]-Y[0], "IQR", Y[3]-Y[1])

# ア〜エ: 箱ひげ図から「確実に正しい」と言えるか
A = X[2] > Y[2]                       # ア 中央値はX組の方が高い
I = (Y[3]-Y[1]) > (X[3]-X[1])         # イ 四分位範囲はY組の方が大きい
U = None  # ウ 80点以上の人数はY組の方が多い → 判断できない（確実でない=False扱い）
E = None  # エ 平均点はX組の方が高い       → 箱ひげ図では判断できない=False扱い
truth = {"ア": A, "イ": I, "ウ": False, "エ": False}
print("\n[問2] 各記述の正誤:", truth)
correct_set = {k for k, v in truth.items() if v}
print("確実に正しい記述の集合:", correct_set)

# 選択肢（組合せ）
options_q2 = {
    1: {"ア", "イ"},
    2: {"ア", "ウ"},
    3: {"イ", "エ"},
    4: {"ア", "イ", "ウ"},
    5: {"イ", "ウ", "エ"},
}
matches = [k for k, s in options_q2.items() if s == correct_set]
print("一致する選択肢:", matches)
assert len(matches) == 1, f"一致が{len(matches)}個"

print("\n--- ランダム正解番号 ---")
print("問1用:", random.randint(1, 5))
print("問2用:", random.randint(1, 5))
