"""
セット132 検証スクリプト - 折れ線グラフ読み取り（電気料金指数）

問1: 2015年の電気料金から2024年の電気料金を求める（指数換算）
問2: 2020年の価格から2022〜2024年の3年分合計を求める

電気料金指数データ（2020年=100）:
  2015: 93.0, 2016: 94.5, 2017: 96.2, 2018: 97.8, 2019: 99.0
  2020: 100.0, 2021: 102.3, 2022: 109.6, 2023: 117.5, 2024: 124.0
"""

# 指数データ（2020年=100）
index_data = {
    2015: 93.0,  2016: 94.5,  2017: 96.2,  2018: 97.8,  2019: 99.0,
    2020: 100.0, 2021: 102.3, 2022: 109.6, 2023: 117.5, 2024: 124.0,
}

print("=== セット132 データ検証 ===")
print("\n電気料金指数 (2020年=100):")
for year, val in index_data.items():
    print(f"  {year}年: {val}")

print("\n=== 問1: 2015年6,000円 → 2024年の電気料金 ===")
base_price = 6000
base_year = 2015
target_year = 2024

price_2024 = base_price * index_data[target_year] / index_data[base_year]
print(f"計算: {base_price}円 × {index_data[target_year]} / {index_data[base_year]}")
print(f"    = {base_price}円 × {index_data[target_year]/index_data[base_year]:.6f}")
print(f"    = {price_2024:.2f}円")

# 厳密な計算確認
# 6000 × 124.0 / 93.0 = 6000 × (4/3) = 8000 （93×4=372, 372/3=124 → 124/93=4/3）
assert index_data[2024] == 124.0
assert index_data[2015] == 93.0
exact = 6000 * 124 / 93
assert abs(exact - 8000) < 0.01, f"8000でない: {exact}"
print(f"→ 正確に 8,000円 ✓  （93×4/3=124より）")

# 選択肢との比較
choices_q1 = [7600, 7800, 7900, 8000, 8200]
diffs_q1 = [abs(price_2024 - c) for c in choices_q1]
closest_q1 = choices_q1[diffs_q1.index(min(diffs_q1))]
print(f"最も近い選択肢: {closest_q1}円  （選択肢4が正解）")

print("\n=== 問2: 2020年10,000円 → 2022〜2024年の3年合計 ===")
base_price_2 = 10000

p2022 = base_price_2 * index_data[2022] / index_data[2020]
p2023 = base_price_2 * index_data[2023] / index_data[2020]
p2024 = base_price_2 * index_data[2024] / index_data[2020]
total = p2022 + p2023 + p2024

print(f"2022年: {base_price_2}円 × {index_data[2022]}/100 = {p2022:.0f}円")
print(f"2023年: {base_price_2}円 × {index_data[2023]}/100 = {p2023:.0f}円")
print(f"2024年: {base_price_2}円 × {index_data[2024]}/100 = {p2024:.0f}円")
print(f"3年合計: {p2022:.0f} + {p2023:.0f} + {p2024:.0f} = {total:.0f}円")

choices_q2 = [34100, 34600, 35100, 35600, 36100]
diffs_q2 = [abs(total - c) for c in choices_q2]
closest_q2 = choices_q2[diffs_q2.index(min(diffs_q2))]
print(f"\n各選択肢との差:")
for c, d in zip(choices_q2, diffs_q2):
    marker = " ← 最小" if c == closest_q2 else ""
    print(f"  {c}円: 差={d:.0f}円{marker}")
print(f"→ 最も近い選択肢: {closest_q2}円  （選択肢3が正解）")

assert closest_q2 == 35100, f"最近似選択肢が35100でない: {closest_q2}"

print("\n=== 検証完了 ===")
