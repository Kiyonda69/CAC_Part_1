#!/usr/bin/env python3
"""セット57 検証コード"""

# ===================== 問1 検証 =====================
print("=" * 60)
print("問1: 電子部品の出荷額推移（散布図読み取り）")
print("=" * 60)

data = [
    (2010, 3200, 1800),
    (2012, 3800, 2400),
    (2014, 4500, 3100),
    (2016, 4200, 2900),
    (2018, 5000, 3500),
    (2020, 4600, 4200),
]

decreased_years = []
for i in range(1, len(data)):
    curr = data[i][1] + data[i][2]
    prev = data[i-1][1] + data[i-1][2]
    if curr < prev:
        decreased_years.append(data[i][0])

assert len(decreased_years) == 1 and decreased_years[0] == 2016
print("→ 問1正解: 2016年（唯一解確認済み）")

# ===================== 問2 検証 =====================
print("\n" + "=" * 60)
print("問2: 従業員の地域別・職種別割合から実数を求める")
print("=" * 60)

total = 3600
# 営業:技術 = 2:1 で設計
sales_pct = {"東京": 36.0, "大阪": 24.0, "名古屋": 18.0, "福岡": 15.0, "その他": 7.0}
tech_pct  = {"東京": 42.0, "大阪": 18.0, "名古屋": 24.0, "福岡": 9.0,  "その他": 7.0}
all_pct   = {"東京": 38.0, "大阪": 22.0, "名古屋": 20.0, "福岡": 13.0, "その他": 7.0}

assert sum(sales_pct.values()) == 100.0
assert sum(tech_pct.values()) == 100.0
assert sum(all_pct.values()) == 100.0

# 連立方程式: x+y=3600, 0.36x+0.42y=0.38*3600
y = round((all_pct["東京"]/100*total - sales_pct["東京"]/100*total) / (tech_pct["東京"]/100 - sales_pct["東京"]/100))
x = total - y
print(f"営業部: {x}人, 技術部: {y}人")
assert y == 1200 and x == 2400

# 全地域で検算
for region in all_pct:
    sc = sales_pct[region]/100 * x
    tc = tech_pct[region]/100 * y
    exp = all_pct[region]/100 * total
    assert abs(sc + tc - exp) < 0.01, f"{region}不整合"

# 他の地域列でも同じ解
for region in ["大阪", "名古屋", "福岡"]:
    y2 = round((all_pct[region]/100*total - sales_pct[region]/100*total) / (tech_pct[region]/100 - sales_pct[region]/100))
    assert y2 == 1200, f"{region}不整合: {y2}"

print("→ 問2正解: 1200人（唯一解確認済み、全地域整合性OK）")
print("\n検証完了")
