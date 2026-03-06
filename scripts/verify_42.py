"""
セット42 検証コード
テーマ: 産業別の製造品出荷額等と輸出割合

データ:
  産業        出荷額(兆円)  輸出比率(%)
  輸送機械      68           45
  化学          47           22
  食料品        35            3
  電子部品      28           58
  鉄鋼          19           31
  その他       103           12
  合計         300

問1（標準）: 全業種の輸出額の合計はおよそいくらか
問2（高難度）: 輸出比率が20%以上の業種について、国内出荷額の合計はおよそいくらか
"""

# データ定義
sectors = {
    "輸送機械": {"output": 68, "export_ratio": 0.45},
    "化学":     {"output": 47, "export_ratio": 0.22},
    "食料品":   {"output": 35, "export_ratio": 0.03},
    "電子部品": {"output": 28, "export_ratio": 0.58},
    "鉄鋼":     {"output": 19, "export_ratio": 0.31},
    "その他":   {"output": 103, "export_ratio": 0.12},
}

# 合計出荷額の確認
total_output = sum(s["output"] for s in sectors.values())
print(f"合計出荷額: {total_output}兆円")

# 各業種のシェア
print("\n各業種のシェア:")
for name, data in sectors.items():
    share = data["output"] / total_output * 100
    print(f"  {name}: {data['output']}兆円 ({share:.1f}%)")

# ====== 問1: 全業種の輸出額の合計 ======
print("\n===== 問1: 全業種の輸出額の合計 =====")
total_export = 0
for name, data in sectors.items():
    export = data["output"] * data["export_ratio"]
    print(f"  {name}: {data['output']} * {data['export_ratio']} = {export:.2f}兆円")
    total_export += export
print(f"  合計輸出額: {total_export:.2f}兆円")

# 選択肢候補
q1_choices = [68, 72, 76, 80, 84]
print(f"  選択肢: {q1_choices}")
# 最も近い選択肢を確認
closest = min(q1_choices, key=lambda x: abs(x - total_export))
print(f"  最も近い選択肢: {closest}兆円 (差: {abs(closest - total_export):.2f})")

# ====== 問2: 輸出比率20%以上の業種の国内出荷額合計 ======
print("\n===== 問2: 輸出比率20%以上の業種の国内出荷額合計 =====")
threshold = 0.20
total_domestic = 0
qualifying = []
for name, data in sectors.items():
    if data["export_ratio"] >= threshold:
        domestic = data["output"] * (1 - data["export_ratio"])
        print(f"  {name}: 輸出比率{data['export_ratio']*100:.0f}% >= 20% → 該当")
        print(f"    国内出荷額 = {data['output']} * {1-data['export_ratio']:.2f} = {domestic:.2f}兆円")
        total_domestic += domestic
        qualifying.append(name)
    else:
        print(f"  {name}: 輸出比率{data['export_ratio']*100:.0f}% < 20% → 該当しない")

print(f"  該当業種: {qualifying}")
print(f"  国内出荷額合計: {total_domestic:.2f}兆円")

# 選択肢候補
q2_choices = [89, 94, 99, 104, 109]
print(f"  選択肢: 約{q2_choices}兆円")
closest2 = min(q2_choices, key=lambda x: abs(x - total_domestic))
print(f"  最も近い選択肢: 約{closest2}兆円 (差: {abs(closest2 - total_domestic):.2f})")

# ====== 解の一意性確認 ======
print("\n===== 解の一意性確認 =====")
# 問1: 76.48に最も近いのは76で、次に近い80との差は3.52
diffs1 = sorted([(abs(c - total_export), c) for c in q1_choices])
print(f"  問1 正解候補からの距離: {diffs1}")
assert diffs1[0][1] == 76, f"問1: 期待される正解は76だが{diffs1[0][1]}になった"
assert diffs1[0][0] < diffs1[1][0], "問1: 解が一意でない"

# 問2: 98.93に最も近いのは99で、次に近い94との差は4.93
diffs2 = sorted([(abs(c - total_domestic), c) for c in q2_choices])
print(f"  問2 正解候補からの距離: {diffs2}")
assert diffs2[0][1] == 99, f"問2: 期待される正解は99だが{diffs2[0][1]}になった"
assert diffs2[0][0] < diffs2[1][0], "問2: 解が一意でない"

print("\n検証完了: 問1正解=76兆円, 問2正解=約99兆円")
print("解の一意性: OK")
