#!/usr/bin/env python3
"""
航大思考59 検証スクリプト
問題タイプ: 資料読み取り（前年比推移グラフ）
"""

# ============================================================
# 問1（標準難度）: 前年比推移から特定店舗の売上高を求める
# ============================================================
# 3店舗 P, Q, R の売上高の前年比推移（%）
# 年:      2021  2022  2023  2024
# 店舗P:   +10   +20    -5   +15
# 店舗Q:   +25   -10    +5   +30
# 店舗R:    +5   +15   +25    -5

# 問題: 2020年の店舗Qの売上高が4000万円のとき、
#       2024年の店舗Qの売上高はおよそいくらか。

print("=" * 60)
print("問1: 店舗Qの2024年売上高")
print("=" * 60)

Q_2020 = 4000
Q_rates = [25, -10, 5, 30]  # 2021, 2022, 2023, 2024

Q_current = Q_2020
for i, rate in enumerate(Q_rates):
    Q_prev = Q_current
    Q_current = Q_current * (1 + rate / 100)
    print(f"  {2020+i} -> {2021+i}: {Q_prev:.1f} x {1+rate/100:.2f} = {Q_current:.1f}")

print(f"\n  店舗Q 2024年売上高: {Q_current:.1f}万円")
print(f"  概算値: 約{round(Q_current / 10) * 10}万円")

# 検算: 4000 * 1.25 * 0.90 * 1.05 * 1.30
check = 4000 * 1.25 * 0.90 * 1.05 * 1.30
print(f"  検算: {check:.1f}万円")

# 選択肢の検討
options_q1 = {
    1: 4960,
    2: 5380,
    3: 5820,
    4: 6140,
    5: 6500
}
print(f"\n  正解: {Q_current:.1f} ≈ 6140万円")
for k, v in options_q1.items():
    mark = " ★正解" if abs(v - Q_current) < 50 else ""
    print(f"    ({k}) {v}万円{mark}")

# ============================================================
# 問2（高難度）: 比率条件から個別売上を求め、2店舗の差を算出
# ============================================================
# 追加条件:
# - 2020年の3店舗の売上高合計 = 12000万円
# - 2020年の P:Q:R = 3:2:1
# 問題: 2024年における店舗Pと店舗Rの売上高の差はおよそいくらか。

print("\n" + "=" * 60)
print("問2: PとRの2024年売上高の差")
print("=" * 60)

total_2020 = 12000
# P:Q:R = 3:2:1 → total ratio = 6
P_2020 = total_2020 * 3 / 6
Q_2020_check = total_2020 * 2 / 6
R_2020 = total_2020 * 1 / 6
print(f"  2020年: P={P_2020:.0f}, Q={Q_2020_check:.0f}, R={R_2020:.0f}")
print(f"  合計確認: {P_2020 + Q_2020_check + R_2020:.0f}")

# 店舗Pの計算
P_rates = [10, 20, -5, 15]
P_current = P_2020
print(f"\n  店舗P:")
for i, rate in enumerate(P_rates):
    P_prev = P_current
    P_current = P_current * (1 + rate / 100)
    print(f"    {2020+i} -> {2021+i}: {P_prev:.1f} x {1+rate/100:.2f} = {P_current:.1f}")

# 店舗Rの計算
R_rates = [5, 15, 25, -5]
R_current = R_2020
print(f"\n  店舗R:")
for i, rate in enumerate(R_rates):
    R_prev = R_current
    R_current = R_current * (1 + rate / 100)
    print(f"    {2020+i} -> {2021+i}: {R_prev:.1f} x {1+rate/100:.2f} = {R_current:.1f}")

diff = P_current - R_current
print(f"\n  P 2024: {P_current:.1f}万円")
print(f"  R 2024: {R_current:.1f}万円")
print(f"  差: {diff:.1f}万円")
print(f"  概算値: 約{round(diff / 10) * 10}万円")

# 選択肢の検討
options_q2 = {
    1: 4560,
    2: 5130,
    3: 5780,
    4: 6320,
    5: 6900
}
print(f"\n  正解: {diff:.1f} ≈ 5780万円")
for k, v in options_q2.items():
    mark = " ★正解" if abs(v - diff) < 50 else ""
    print(f"    ({k}) {v}万円{mark}")

# 唯一解の確認
print("\n" + "=" * 60)
print("解の一意性確認")
print("=" * 60)
print("問1: 計算過程が一意（前年比を順に掛けるのみ）→ 唯一解")
print("問2: 比率から個別値が一意に決まり、計算過程も一意 → 唯一解")

# 誤答パターンの分析
print("\n" + "=" * 60)
print("誤答パターン分析")
print("=" * 60)

# 問1の誤答パターン
print("\n問1:")
# パターン1: 単純加算する間違い
wrong1 = 4000 + 4000 * (25 - 10 + 5 + 30) / 100
print(f"  誤パターン1 (比率を単純加算): 4000 + 4000×50% = {wrong1:.0f}万円")
# パターン2: 最終年の比率だけ適用
wrong2 = 4000 * 1.30
print(f"  誤パターン2 (最終年のみ): 4000×1.30 = {wrong2:.0f}万円")
# パターン3: 2023年まで計算して停止
wrong3 = 4000 * 1.25 * 0.90 * 1.05
print(f"  誤パターン3 (2023年まで): {wrong3:.1f}万円")

