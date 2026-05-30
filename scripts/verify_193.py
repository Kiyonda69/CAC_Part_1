# -*- coding: utf-8 -*-
"""
航大思考193 解の一意性検証
問1（標準）: 5物流センターの2表クロス参照（売上→営業利益→利益率→1日あたりの多段計算）
問2（高難度）: 6ホテルの2表クロス参照（売上→変動費→営業利益→利益率→1室あたりの多段計算）
"""

def check_unique(options, truth):
    """trueとなる記述集合に一致する選択肢が唯一かを確認"""
    matches = [i for i, s in options.items() if s == truth]
    return matches

# =========================================================
# 問1: 5物流センター（A〜E）
#   表1: 取扱個数(千個/月), 1個あたり配送料(円), 稼働日数(日)
#   表2: 変動費率(%), 人件費(万円/月), その他固定費(万円/月)
#   売上(万円) = 取扱個数(千個)*1000*配送料 / 10000 = 取扱個数 * 配送料 / 10
# =========================================================
print("=" * 55)
print("問1: 5物流センター")
print("=" * 55)

q1 = {
    "A": (300, 500, 25, 55, 3000, 1500),
    "B": (250, 600, 25, 50, 3500, 1800),
    "C": (400, 400, 25, 60, 2800, 1600),
    "D": (200, 700, 25, 45, 3200, 2000),
    "E": (360, 500, 30, 58, 3400, 2000),
}

q1res = {}
for k, (qty, price, days, vc, labor, fixed) in q1.items():
    sales = qty * price / 10
    vcost = sales * vc / 100
    profit = sales - vcost - labor - fixed
    rate = profit / sales * 100
    per_day = qty * 1000 / days
    q1res[k] = dict(sales=sales, profit=profit, rate=rate, per_day=per_day)
    print(f"{k}: 売上={sales:.0f}万 変動費={vcost:.0f} 利益={profit:.0f}万 利益率={rate:.2f}% 1日={per_day:.1f}個")

# 記述（問1）
a1 = (max(q1res, key=lambda x: q1res[x]['sales']) == "E")              # ア 売上最大E
b1 = (max(q1res, key=lambda x: q1res[x]['profit']) == "D")            # イ 利益最大D
c1 = (len([k for k in q1res if q1res[k]['rate'] >= 15]) == 2)         # ウ 利益率15%以上が2つ
d1 = (max(q1res, key=lambda x: q1res[x]['per_day']) == "E")          # エ 1日最多E(実際はC=罠)
truth1 = {"ア": a1, "イ": b1, "ウ": c1, "エ": d1}
print("\n問1 真の記述:", {k: v for k, v in truth1.items()})

# 選択肢: 各「正しい記述の組合せ」。真集合={ア,イ,ウ}
def s(*keys):
    return {k: (k in keys) for k in ["ア", "イ", "ウ", "エ"]}
opt1 = {
    1: s("ア", "イ"),
    2: s("ア", "ウ"),
    3: s("ア", "イ", "ウ"),
    4: s("イ", "ウ", "エ"),
    5: s("ア", "イ", "エ"),
}
m1 = check_unique(opt1, truth1)
print("問1 一致選択肢:", m1)
assert len(m1) == 1, f"問1 解が一意でない: {m1}"
print(f"問1 正解: ({m1[0]})")

# =========================================================
# 問2: 6ホテル（A〜F）高難度
#   表1: 延べ宿泊室数(室/月), 平均客室単価(円/室), 営業日数(日)
#   表2: 変動費率(%), 人件費(万円/月), その他固定費(万円/月)
#   売上(万円) = 室数 * 単価 / 10000
# =========================================================
print("\n" + "=" * 55)
print("問2: 6ホテル")
print("=" * 55)

q2 = {
    "A": (9000, 12000, 30, 30, 2000, 1500),
    "B": (12000, 9000, 30, 35, 1800, 1300),
    "C": (9600, 12500, 30, 25, 2500, 2000),
    "D": (15000, 8000, 30, 40, 2200, 1400),
    "E": (6000, 20000, 30, 20, 3000, 2500),
    "F": (10500, 10000, 30, 30, 2000, 1500),
}

q2res = {}
for k, (rooms, adr, days, vc, labor, fixed) in q2.items():
    sales = rooms * adr / 10000
    vcost = sales * vc / 100
    profit = sales - vcost - labor - fixed
    rate = profit / sales * 100
    per_day = rooms / days
    q2res[k] = dict(sales=sales, profit=profit, rate=rate, per_day=per_day)
    print(f"{k}: 売上={sales:.0f}万 変動費={vcost:.0f} 利益={profit:.0f}万 利益率={rate:.2f}% 1日={per_day:.1f}室")

# 記述（問2）
a2 = (max(q2res, key=lambda x: q2res[x]['profit']) == "C")               # ア 利益最大C
b2 = (max(q2res, key=lambda x: q2res[x]['rate']) == "C")                 # イ 利益率最大C(実際A=罠)
c2 = (len([k for k in q2res if q2res[k]['rate'] >= 35]) == 4)            # ウ 利益率35%以上が4つ
d2 = (max(q2res, key=lambda x: q2res[x]['per_day']) == "D")             # エ 1日最多D
# オ 売上最大はAとB(実際は12000のC/D/E=罠)
e2 = (q2res["A"]['sales'] == max(r['sales'] for r in q2res.values()) and
      q2res["B"]['sales'] == max(r['sales'] for r in q2res.values()))
truth2 = {"ア": a2, "イ": b2, "ウ": c2, "エ": d2, "オ": e2}
print("\n問2 真の記述:", truth2)
print("  利益率35%以上:", [k for k in q2res if q2res[k]['rate'] >= 35])

def s2(*keys):
    return {k: (k in keys) for k in ["ア", "イ", "ウ", "エ", "オ"]}
opt2 = {
    1: s2("ア", "ウ"),
    2: s2("イ", "ウ", "エ"),
    3: s2("ア", "エ", "オ"),
    4: s2("ア", "ウ", "エ"),
    5: s2("ア", "イ", "ウ", "エ"),
}
m2 = check_unique(opt2, truth2)
print("問2 一致選択肢:", m2)
assert len(m2) == 1, f"問2 解が一意でない: {m2}"
print(f"問2 正解: ({m2[0]})")

print("\n" + "=" * 55)
print("検証完了: 問1・問2ともに解が一意")
print("=" * 55)
