"""
セット79 検証スクリプト
問1: 品目別消費支出額と国産品購入割合
問2: 部門別四半期売上高と経費率から年間利益額を分析
"""

# ============================================================
# 問1: 品目別消費支出額と国産品購入割合
# ============================================================
print("=" * 60)
print("問1: 品目別消費支出額と国産品購入割合")
print("=" * 60)

# データ
categories = [
    ("食料", 480, 0.75),
    ("衣類", 210, 0.20),
    ("家具・家電", 300, 0.35),
    ("交通・通信", 240, 0.60),
    ("その他", 270, 0.40),
]

total_spending = sum(c[1] for c in categories)
print(f"総支出額: {total_spending}千円")

domestic_total = 0
for name, amount, ratio in categories:
    domestic = amount * ratio
    print(f"  {name}: {amount} x {ratio:.0%} = {domestic:.1f}千円")
    domestic_total += domestic

print(f"\n国産品支出額合計: {domestic_total:.1f}千円")

# 選択肢: 正解は(1)
choices_q1 = [759, 774, 801, 825, 843]
correct_q1 = 1  # (1)が正解
print(f"正解: ({correct_q1}) {choices_q1[correct_q1-1]}千円")
assert domestic_total == choices_q1[correct_q1-1], f"不一致: {domestic_total} != {choices_q1[correct_q1-1]}"
print("検証OK: 解は一意")

# 支出割合の確認
print(f"\n支出構成割合:")
for name, amount, ratio in categories:
    pct = amount / total_spending * 100
    print(f"  {name}: {pct:.1f}%")

# ============================================================
# 問2: 部門別四半期売上高と経費率
# ============================================================
print("\n" + "=" * 60)
print("問2: 部門別四半期売上高と経費率")
print("=" * 60)

# データ
departments = {
    "営業": {"quarterly": [150, 180, 160, 210], "cost_rate": 0.70},
    "開発": {"quarterly": [80, 100, 110, 110], "cost_rate": 0.85},
    "製造": {"quarterly": [200, 220, 180, 200], "cost_rate": 0.65},
    "サービス": {"quarterly": [120, 140, 150, 190], "cost_rate": 0.60},
}

results = []
for dept, data in departments.items():
    annual = sum(data["quarterly"])
    profit_rate = 1 - data["cost_rate"]
    profit = annual * profit_rate
    results.append((dept, annual, profit_rate, profit))
    print(f"  {dept}: 年間売上 {annual}百万円, 利益率 {profit_rate:.0%}, 利益 {profit:.1f}百万円")

# ランキング
results_sorted = sorted(results, key=lambda x: x[3], reverse=True)
print(f"\n利益額ランキング:")
for i, (dept, annual, pr, profit) in enumerate(results_sorted, 1):
    print(f"  {i}位: {dept} = {profit:.1f}百万円")

second_largest = results_sorted[1][3]
print(f"\n2番目に大きい部門の利益額: {second_largest:.1f}百万円")

# 選択肢: 正解は(4)
choices_q2 = [200, 210, 224, 240, 280]
correct_q2 = 4  # (4)が正解
print(f"正解: ({correct_q2}) {choices_q2[correct_q2-1]}百万円")
assert second_largest == choices_q2[correct_q2-1], f"不一致: {second_largest} != {choices_q2[correct_q2-1]}"
print("検証OK: 解は一意")

print("\n" + "=" * 60)
print("全検証完了: 両問とも解が一意であることを確認")
print("=" * 60)
