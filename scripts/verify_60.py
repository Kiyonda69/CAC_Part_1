"""
航大思考60 検証スクリプト
問1: 研修施設の応募倍率ランキング（標準）
問2: 研修施設データから正しい記述を選ぶ（高難度）
"""

# ===== データ定義 =====
data = {
    2019: {"定員": 40, "応募者数": 248, "受講者数": 180, "修了者数": 162},
    2020: {"定員": 40, "応募者数": 312, "受講者数": 200, "修了者数": 174},
    2021: {"定員": 60, "応募者数": 342, "受講者数": 250, "修了者数": 225},
    2022: {"定員": 60, "応募者数": 420, "受講者数": 280, "修了者数": 238},
    2023: {"定員": 60, "応募者数": 354, "受講者数": 250, "修了者数": 240},
}

print("=" * 60)
print("問1: 応募倍率（応募者数÷定員）ランキング")
print("=" * 60)

ratios = {}
for year, d in data.items():
    ratio = d["応募者数"] / d["定員"]
    ratios[year] = ratio
    print(f"  {year}: {d['応募者数']}/{d['定員']} = {ratio:.2f}")

ranking = sorted(ratios.items(), key=lambda x: x[1], reverse=True)
print(f"\n  高い順: {'→'.join(str(y) for y, _ in ranking)}")
print(f"  値: {', '.join(f'{y}({r:.2f})' for y, r in ranking)}")

# 正解は(2): 2020→2022→2019→2023→2021
expected_q1 = [2020, 2022, 2019, 2023, 2021]
actual_q1 = [y for y, _ in ranking]
assert actual_q1 == expected_q1, f"問1: 期待{expected_q1} != 実際{actual_q1}"
print(f"\n  正解(2): {' → '.join(str(y) for y in expected_q1)} ✓")

# 解が一意であることを確認（全て異なる値）
values = list(ratios.values())
assert len(values) == len(set(values)), "応募倍率に同じ値が存在する"
print("  解の一意性: ✓（全ての値が異なる）")

print()
print("=" * 60)
print("問2: 記述の正誤判定")
print("=" * 60)

# 選考通過率
print("\n  【選考通過率 = 受講者数÷応募者数×100】")
pass_rates = {}
for year, d in data.items():
    rate = d["受講者数"] / d["応募者数"] * 100
    pass_rates[year] = rate
    print(f"  {year}: {d['受講者数']}/{d['応募者数']}×100 = {rate:.2f}%")

# 修了率
print("\n  【修了率 = 修了者数÷受講者数×100】")
completion_rates = {}
for year, d in data.items():
    rate = d["修了者数"] / d["受講者数"] * 100
    completion_rates[year] = rate
    print(f"  {year}: {d['修了者数']}/{d['受講者数']}×100 = {rate:.2f}%")

# ア：選考通過率が最も高い年度は2021年度である
print("\n  ア：選考通過率が最も高い年度は2021年度である")
max_pass_year = max(pass_rates, key=pass_rates.get)
a_correct = (max_pass_year == 2021)
print(f"    最高: {max_pass_year}({pass_rates[max_pass_year]:.2f}%) → {'正' if a_correct else '誤'}")

# イ：選考通過率が70%を超えている年度は3つある
print("\n  イ：選考通過率が70%を超えている年度は3つある")
over_70 = [y for y, r in pass_rates.items() if r > 70]
b_correct = (len(over_70) == 3)
print(f"    70%超: {over_70} ({len(over_70)}つ) → {'正' if b_correct else '誤'}")

# ウ：修了率が最も低い年度は、応募倍率も最も高い
print("\n  ウ：修了率が最も低い年度は、応募倍率も最も高い")
min_comp_year = min(completion_rates, key=completion_rates.get)
max_ratio_year = max(ratios, key=ratios.get)
c_correct = (min_comp_year == max_ratio_year)
print(f"    修了率最低: {min_comp_year}({completion_rates[min_comp_year]:.1f}%)")
print(f"    応募倍率最高: {max_ratio_year}({ratios[max_ratio_year]:.2f})")
print(f"    → {'正' if c_correct else '誤'}（年度が異なる）")

# エ：応募者数に対する修了者数の割合が最も高い年度は2023年度である
print("\n  エ：応募者数に対する修了者数の割合が最も高い年度は2023年度")
total_rates = {}
for year, d in data.items():
    rate = d["修了者数"] / d["応募者数"] * 100
    total_rates[year] = rate
    print(f"    {year}: {d['修了者数']}/{d['応募者数']}×100 = {rate:.2f}%")
max_total_year = max(total_rates, key=total_rates.get)
d_correct = (max_total_year == 2023)
print(f"    最高: {max_total_year}({total_rates[max_total_year]:.2f}%) → {'正' if d_correct else '誤'}")

# オ：修了率が90%以上の年度は、選考通過率も70%以上である
print("\n  オ：修了率が90%以上の年度は、選考通過率も70%以上である")
comp_over_90 = [(y, completion_rates[y]) for y in data if completion_rates[y] >= 90]
print(f"    修了率≥90%: {[(y, f'{r:.1f}%') for y, r in comp_over_90]}")
e_correct = all(pass_rates[y] > 70 for y, _ in comp_over_90)
for y, _ in comp_over_90:
    print(f"    {y}: 選考通過率={pass_rates[y]:.2f}% {'≥70✓' if pass_rates[y] > 70 else '<70✗'}")
print(f"    → {'正' if e_correct else '誤'}")

print("\n  【まとめ】")
results = {"ア": a_correct, "イ": b_correct, "ウ": c_correct, "エ": d_correct, "オ": e_correct}
for name, correct in results.items():
    print(f"    {name}: {'正' if correct else '誤'}")

correct_statements = [name for name, correct in results.items() if correct]
print(f"\n  正しい記述: {', '.join(correct_statements)}")
assert correct_statements == ["ア", "イ", "エ", "オ"], f"期待: ア,イ,エ,オ != {correct_statements}"
print("  正解(1): ア、イ、エ、オ ✓")

print()
print("=" * 60)
print("全検証パス")
print("=" * 60)
