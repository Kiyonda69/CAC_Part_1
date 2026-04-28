"""
セット131 検証スクリプト - 帯グラフ（メコグラフ）読み取り問題

問1: B国の機械輸出額とC国の食品輸出額の比
問2: 4か国輸出額データに関する正誤判定（正しい記述を選ぶ）

データ:
  横軸シェア: A国20%, B国40%, C国30%, D国10%
  内訳（上から順: その他, 化学品, 機械, 食品）:
    A国: その他10%, 化学品20%, 機械40%, 食品30%
    B国: その他10%, 化学品20%, 機械50%, 食品20%
    C国: その他10%, 化学品20%, 機械20%, 食品50%
    D国: その他10%, 化学品30%, 機械20%, 食品40%
"""
from math import gcd

# 国別データ
countries = {
    'A': {'share': 20, 'food': 30, 'machinery': 40, 'chemical': 20, 'other': 10},
    'B': {'share': 40, 'food': 20, 'machinery': 50, 'chemical': 20, 'other': 10},
    'C': {'share': 30, 'food': 50, 'machinery': 20, 'chemical': 20, 'other': 10},
    'D': {'share': 10, 'food': 40, 'machinery': 20, 'chemical': 30, 'other': 10},
}

# 検証: 内訳の合計が100%か
for name, d in countries.items():
    total = d['food'] + d['machinery'] + d['chemical'] + d['other']
    assert total == 100, f"{name}国の内訳合計が{total}%"

# 検証: 横軸シェアの合計が100%か
total_share = sum(d['share'] for d in countries.values())
assert total_share == 100, f"横軸シェア合計が{total_share}%"

print("=== セット131 データ検証 ===")
print("\n各国の実質生産額（全体に占める割合）:")
vals = {}
for name, d in countries.items():
    vals[name] = {}
    for item in ['food', 'machinery', 'chemical', 'other']:
        vals[name][item] = d['share'] * d[item] / 100
    print(f"  {name}国: 食品={vals[name]['food']:.1f}, "
          f"機械={vals[name]['machinery']:.1f}, "
          f"化学品={vals[name]['chemical']:.1f}, "
          f"その他={vals[name]['other']:.1f}")

totals = {item: sum(vals[n][item] for n in countries) for item in ['food', 'machinery', 'chemical', 'other']}
print(f"\n4か国合計: 食品={totals['food']:.1f}, 機械={totals['machinery']:.1f}, "
      f"化学品={totals['chemical']:.1f}, その他={totals['other']:.1f}")
assert abs(sum(totals.values()) - 100) < 0.01, "合計が100%でない"

print("\n=== 問1: B国機械 vs C国食品 の比 ===")
B_mach = vals['B']['machinery']
C_food = vals['C']['food']
print(f"B国機械 = {countries['B']['share']}% × {countries['B']['machinery']}% = {B_mach:.1f}")
print(f"C国食品 = {countries['C']['share']}% × {countries['C']['food']}% = {C_food:.1f}")
n1, n2 = int(B_mach * 10), int(C_food * 10)
g = gcd(n1, n2)
print(f"比 = {B_mach}:{C_food} = {n1//g}:{n2//g}")
assert n1 // g == 4 and n2 // g == 3, "比が4:3でない"
print("→ 正解: 4:3 ✓  （選択肢5が正解）")

print("\n=== 問2: 記述の正誤判定 ===")
checks = [
    ("(1) A国食品はD国食品の2倍以上",
     vals['A']['food'] >= 2 * vals['D']['food'],
     f"A食品={vals['A']['food']:.1f}, D食品={vals['D']['food']:.1f}, "
     f"A/D={vals['A']['food']/vals['D']['food']:.2f}"),
    ("(2) C国食品は食品合計の50%超",
     vals['C']['food'] > totals['food'] * 0.5,
     f"C食品={vals['C']['food']:.1f}, 食品合計={totals['food']:.1f}, "
     f"割合={vals['C']['food']/totals['food']*100:.1f}%"),
    ("(3) 化学品合計>機械合計",
     totals['chemical'] > totals['machinery'],
     f"化学品合計={totals['chemical']:.1f}, 機械合計={totals['machinery']:.1f}"),
    ("(4) B国機械は機械合計の50%超 ← 正解",
     vals['B']['machinery'] > totals['machinery'] * 0.5,
     f"B機械={vals['B']['machinery']:.1f}, 機械合計={totals['machinery']:.1f}, "
     f"割合={vals['B']['machinery']/totals['machinery']*100:.1f}%"),
    ("(5) D国化学品>A国化学品",
     vals['D']['chemical'] > vals['A']['chemical'],
     f"D化学品={vals['D']['chemical']:.1f}, A化学品={vals['A']['chemical']:.1f}"),
]

correct_count = 0
for label, result, detail in checks:
    print(f"  {label}: {'TRUE ✓' if result else 'FALSE'} ({detail})")
    if result:
        correct_count += 1

assert correct_count == 1, f"正解が{correct_count}個（唯一解でない）"
print("\n→ 唯一の正解: (4) ✓  （選択肢4が正解）")

print("\n=== 検証完了 ===")
