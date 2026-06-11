"""
航大思考210 解の一意性検証

問1: レストランデータ表からの条件絞り込み（標準）
問2: 旅行プラン選択（複数表組み合わせ・高難度）
"""

# ==========================================
# 問1: レストランデータ表
# ==========================================
# 10店舗の表から下記すべてを満たす店舗を選ぶ
# A. 平均単価が5000円以下
# B. 評価が4.3以上
# C. 駅徒歩6分以内
# D. 個室あり
# E. ランチ営業あり(開店11時)

restaurants = [
    # (店舗番号, 種類, 単価, 評価, 開店, 閉店, 徒歩, 個室)
    (1, "中華", 5200, 4.4, 11, 23, 4, True),   # 単価NG
    (2, "和食", 4500, 4.2, 11, 22, 5, True),   # 評価NG
    (3, "洋食", 4800, 4.5, 17, 23, 3, True),   # ランチNG
    (4, "和食", 4200, 4.6, 11, 22, 8, True),   # 徒歩NG
    (5, "中華", 3800, 4.3, 11, 23, 6, False),  # 個室NG
    (6, "和食", 6500, 4.7, 17, 23, 2, True),   # 単価NG, ランチNG
    (7, "洋食", 4900, 4.5, 11, 23, 5, True),   # ★全条件満たす（正解）
    (8, "中華", 3500, 4.1, 11, 22, 9, False),  # 評価NG, 徒歩NG, 個室NG
    (9, "和食", 5500, 4.4, 11, 22, 4, True),   # 単価NG
    (10, "洋食", 4400, 4.0, 11, 23, 6, True),  # 評価NG
]

# 選択肢: 店舗3, 店舗4, 店舗9, 店舗1, 店舗7
options_q1 = [3, 4, 9, 1, 7]  # 正解は(5) = 店舗7

def check_restaurant(r):
    """5条件すべて満たすか判定"""
    num, kind, price, rating, open_h, close_h, walk, room = r
    A = price <= 5000
    B = rating >= 4.3
    C = walk <= 6
    D = room
    E = open_h == 11
    return A and B and C and D and E

print("=" * 60)
print("問1: レストラン絞り込み検証")
print("=" * 60)
print(f"{'店舗':<6}{'単価':<6}{'評価':<6}{'徒歩':<6}{'個室':<6}{'ランチ':<6}{'判定'}")
valid = []
for r in restaurants:
    num, kind, price, rating, open_h, close_h, walk, room = r
    ok = check_restaurant(r)
    if ok:
        valid.append(num)
    print(f"{num:<6}{price:<6}{rating:<6}{walk:<6}{'有' if room else '無':<6}{'◯' if open_h == 11 else '✗':<6}{'★正解' if ok else ''}")

print(f"\n条件を満たす店舗: {valid}")
assert len(valid) == 1, f"解が{len(valid)}個存在: {valid}"
correct_store_q1 = valid[0]
correct_idx_q1 = options_q1.index(correct_store_q1) + 1
print(f"正解番号: ({correct_idx_q1}) = 店舗{correct_store_q1}")
assert correct_idx_q1 == 5, f"正解番号がランダム化値(5)と一致しません: {correct_idx_q1}"

# 各選択肢が異なる条件で落ちることも確認（教育的価値）
print("\n各選択肢の不満たし条件:")
for idx, store_num in enumerate(options_q1, 1):
    r = restaurants[store_num - 1]
    num, kind, price, rating, open_h, close_h, walk, room = r
    fails = []
    if price > 5000: fails.append("A:単価")
    if rating < 4.3: fails.append("B:評価")
    if walk > 6: fails.append("C:徒歩")
    if not room: fails.append("D:個室")
    if open_h != 11: fails.append("E:ランチ")
    print(f"  ({idx}) 店舗{store_num}: " + ("全条件OK★" if not fails else ", ".join(fails) + " NG"))


# ==========================================
# 問2: 旅行プラン選択
# ==========================================
# 5つのツアープランから条件すべて満たすプランを選ぶ
# プラン基本情報 + 追加オプション料金 + 割引条件 から計算

# プラン基本情報
# (プラン名, 行先, 日数, 基本料金, 出発曜日(0=月), 食事回数, ホテル等級)
plans = [
    ("P", "北海道", 3, 38000, 5, 4, 4),   # 金発, 4食, 4★ ← 正解
    ("Q", "京都",   2, 32000, 6, 3, 3),   # 土発NG
    ("R", "沖縄",   4, 60000, 4, 5, 5),   # 木発, 5食, 5★ → 予算NG(60100)
    ("S", "九州",   3, 41000, 5, 1, 4),   # 食事NG(1+1=2食)
    ("T", "東北",   2, 28000, 1, 3, 3),   # 火曜NG
]

# 追加オプション料金（円/人）
# (オプション名, 料金)
options_table = {
    "送迎": 3500,
    "保険": 2800,
    "夕食追加": 4200,
    "個室": 5500,
    "現地ガイド": 6800,
}

# 割引条件
# - 木曜出発: 基本料金から8%引
# - 5★ホテル: オプション「個室」が無料
# - 食事5回以上含むプラン: 「夕食追加」不要
# - 4日以上: 「保険」が半額

# 顧客の条件:
# - 予算: 1人あたり総額 55,000円以下
# - 必須オプション: 送迎、保険、個室
# - 食事は4回以上必要（プラン食事数＋夕食追加で4回以上）
# - 金曜または木曜出発

required_options = ["送迎", "保険", "個室"]

def calculate_total(plan):
    name, dest, days, base, weekday, meals, hotel = plan

    # 基本料金（木曜出発は8%引）
    if weekday == 4:  # 木曜
        actual_base = base * 0.92
    else:
        actual_base = base

    # オプション料金合計
    opt_total = 0
    for opt in required_options:
        if opt == "個室" and hotel == 5:
            # 5★ホテルは個室無料
            opt_total += 0
        elif opt == "保険" and days >= 4:
            # 4日以上は保険半額
            opt_total += options_table[opt] // 2
        else:
            opt_total += options_table[opt]

    # 食事追加が必要か
    meal_addition = 0
    if meals < 4:
        # 夕食追加（5回以上の食事数がプランに含まれていれば不要だが、ここでは食事不足の場合追加が必要）
        # ルール: 食事5回以上含むプランは「夕食追加」不要 = 但し食事数不足の場合は追加要
        meal_addition = options_table["夕食追加"]

    total = actual_base + opt_total + meal_addition
    return total, opt_total, meal_addition, actual_base

def check_plan(plan):
    name, dest, days, base, weekday, meals, hotel = plan
    total, opt_t, meal_t, actual_base = calculate_total(plan)
    # 予算条件
    budget_ok = total <= 55000
    # 食事条件: 食事数 + 追加分(あれば1回として加算は実装上不要、ルール上は「夕食追加」で1回プラス想定)
    # 単純化: プランの食事数（or 食事追加後）が4回以上必要
    effective_meals = meals + (1 if meal_t > 0 else 0)
    meal_ok = effective_meals >= 4
    # 出発曜日条件
    day_ok = weekday in (4, 5)  # 木曜=4, 金曜=5
    return budget_ok and meal_ok and day_ok, total, opt_t, meal_t, actual_base


print("\n" + "=" * 60)
print("問2: 旅行プラン選択検証")
print("=" * 60)
print(f"{'プラン':<8}{'実質基本':<10}{'OP合計':<10}{'食事追加':<10}{'総額':<10}{'判定'}")

valid_q2 = []
for plan in plans:
    name = plan[0]
    ok, total, opt_t, meal_t, actual_base = check_plan(plan)
    if ok:
        valid_q2.append(name)
    print(f"{name:<8}{int(actual_base):<10}{opt_t:<10}{meal_t:<10}{int(total):<10}{'★正解' if ok else ''}")

print(f"\n条件を満たすプラン: {valid_q2}")
assert len(valid_q2) == 1, f"解が{len(valid_q2)}個存在: {valid_q2}"

# 選択肢は (1)P (2)Q (3)R (4)S (5)T
options_q2 = ["P", "Q", "R", "S", "T"]
correct_plan = valid_q2[0]
correct_idx_q2 = options_q2.index(correct_plan) + 1
print(f"正解番号: ({correct_idx_q2}) = プラン{correct_plan}")
assert correct_idx_q2 == 1, f"正解番号がランダム化値(1)と一致しません: {correct_idx_q2}"

# 各プランの落とし所
print("\n各プランの不満たし条件:")
for idx, plan in enumerate(plans, 1):
    name, dest, days, base, weekday, meals, hotel = plan
    ok, total, opt_t, meal_t, actual_base = check_plan(plan)
    fails = []
    if total > 55000: fails.append(f"予算{int(total)}>55000")
    eff_meals = meals + (1 if meal_t > 0 else 0)
    if eff_meals < 4: fails.append(f"食事{eff_meals}回<4")
    if weekday not in (4, 5): fails.append("曜日NG")
    print(f"  ({idx}) {name}: " + ("全条件OK★" if not fails else " / ".join(fails)))

print("\n" + "=" * 60)
print("両問の解の一意性検証完了")
print("=" * 60)
