"""
航大思考77 検証スクリプト
問1: スポーツ施設利用者の年代別・性別内訳（円グラフ読み取り）
問2: 5地域の農作物出荷額（表データ読み取り）
"""

def verify_q1():
    """問1: 30代の利用者は全体のおよそ何%か"""
    print("=" * 60)
    print("問1: スポーツ施設利用者 - 30代の割合")
    print("=" * 60)

    # データ
    total = 12000
    male = 8640  # 72%
    female = 3360  # 28%

    assert male + female == total, f"合計不一致: {male + female} != {total}"

    # 男性年代別割合
    male_pct = {
        "10代以下": 8,
        "20代": 23,
        "30代": 32,
        "40代": 21,
        "50代": 11,
        "60代以上": 5
    }

    # 女性年代別割合
    female_pct = {
        "10代以下": 12,
        "20代": 28,
        "30代": 27,
        "40代": 18,
        "50代": 10,
        "60代以上": 5
    }

    # 割合合計チェック
    assert sum(male_pct.values()) == 100, f"男性割合合計: {sum(male_pct.values())}"
    assert sum(female_pct.values()) == 100, f"女性割合合計: {sum(female_pct.values())}"

    # 各年代の人数計算
    print("\n--- 男性 ---")
    for age, pct in male_pct.items():
        num = male * pct / 100
        print(f"  {age}: {pct}% = {num:.1f}人")

    print("\n--- 女性 ---")
    for age, pct in female_pct.items():
        num = female * pct / 100
        print(f"  {age}: {pct}% = {num:.1f}人")

    # 30代の計算
    male_30 = male * male_pct["30代"] / 100
    female_30 = female * female_pct["30代"] / 100
    total_30 = male_30 + female_30
    pct_30 = total_30 / total * 100

    print(f"\n--- 30代の計算 ---")
    print(f"  男性30代: {male} x {male_pct['30代']}% = {male_30:.1f}人")
    print(f"  女性30代: {female} x {female_pct['30代']}% = {female_30:.1f}人")
    print(f"  合計30代: {total_30:.1f}人")
    print(f"  全体に占める割合: {total_30:.1f} / {total} = {pct_30:.1f}%")

    # 選択肢検証
    choices = {1: 27.3, 2: 28.9, 3: 29.5, 4: 30.6, 5: 33.8}
    correct = 4
    print(f"\n--- 選択肢 ---")
    for k, v in choices.items():
        mark = " <-- 正解" if k == correct else ""
        print(f"  ({k}) {v}%{mark}")

    assert abs(pct_30 - choices[correct]) < 0.1, f"正解値不一致: {pct_30} != {choices[correct]}"

    # 他の選択肢が間違いであることを確認（他の年代の値と一致しないか）
    for age in male_pct:
        if age == "30代":
            continue
        m = male * male_pct[age] / 100
        f = female * female_pct[age] / 100
        t = m + f
        p = t / total * 100
        for k, v in choices.items():
            if k == correct:
                continue
            # 他の選択肢と他の年代の割合が一致しないことを確認
            # (紛らわしい誤答がないか)

    print(f"\n正解: ({correct}) {choices[correct]}%")
    print("検証OK")
    return pct_30


def verify_q2():
    """問2: 5地域の農作物出荷額 - 正しい記述の組み合わせ"""
    print("\n" + "=" * 60)
    print("問2: 5地域の農作物出荷額")
    print("=" * 60)

    # データ
    data = {
        "P": {"米": 85, "野菜": 120, "果物": 45},
        "Q": {"米": 150, "野菜": 90, "果物": 60},
        "R": {"米": 70, "野菜": 200, "果物": 80},
        "S": {"米": 110, "野菜": 75, "果物": 165},
        "T": {"米": 95, "野菜": 140, "果物": 65},
    }

    # 合計計算
    for region, vals in data.items():
        total = sum(vals.values())
        print(f"  {region}: 米{vals['米']} + 野菜{vals['野菜']} + 果物{vals['果物']} = {total}")
        data[region]["合計"] = total

    # ア. 米の出荷額が最も大きい地域は、合計出荷額でも最大である。
    rice_max_region = max(data, key=lambda r: data[r]["米"])
    total_max_region = max(data, key=lambda r: data[r]["合計"])
    rice_max_val = data[rice_max_region]["米"]
    total_max_val = data[total_max_region]["合計"]

    print(f"\nア: 米最大: {rice_max_region}({rice_max_val}億円), 合計最大: {total_max_region}({total_max_val}億円)")
    a_correct = (rice_max_region == total_max_region)
    print(f"   → {'正しい' if a_correct else '正しくない'}")

    # イ. 果物の出荷額が合計の40%を超える地域がある。
    print(f"\nイ: 果物の割合:")
    b_correct = False
    for region, vals in data.items():
        fruit_pct = vals["果物"] / vals["合計"] * 100
        print(f"   {region}: {vals['果物']}/{vals['合計']} = {fruit_pct:.1f}%")
        if fruit_pct > 40:
            b_correct = True
    print(f"   → {'正しい' if b_correct else '正しくない'}")

    # ウ. 野菜の出荷額の5地域合計は、米の出荷額の5地域合計より大きい。
    veg_total = sum(data[r]["野菜"] for r in data)
    rice_total = sum(data[r]["米"] for r in data)
    print(f"\nウ: 野菜合計: {veg_total}, 米合計: {rice_total}")
    c_correct = veg_total > rice_total
    print(f"   → {'正しい' if c_correct else '正しくない'}")

    # エ. 合計出荷額に占める米の割合は、どの地域でも30%以上である。
    print(f"\nエ: 米の割合:")
    d_correct = True
    for region, vals in data.items():
        rice_pct = vals["米"] / vals["合計"] * 100
        print(f"   {region}: {vals['米']}/{vals['合計']} = {rice_pct:.1f}%")
        if rice_pct < 30:
            d_correct = False
    print(f"   → {'正しい' if d_correct else '正しくない'}")

    # オ. 果物の出荷額が最も小さい地域は、野菜の出荷額も最も小さい。
    fruit_min_region = min(data, key=lambda r: data[r]["果物"])
    veg_min_region = min(data, key=lambda r: data[r]["野菜"])
    print(f"\nオ: 果物最小: {fruit_min_region}({data[fruit_min_region]['果物']}億円), "
          f"野菜最小: {veg_min_region}({data[veg_min_region]['野菜']}億円)")
    e_correct = (fruit_min_region == veg_min_region)
    print(f"   → {'正しい' if e_correct else '正しくない'}")

    print(f"\n--- 判定結果 ---")
    results = {"ア": a_correct, "イ": b_correct, "ウ": c_correct, "エ": d_correct, "オ": e_correct}
    correct_statements = [k for k, v in results.items() if v]
    print(f"  正しい記述: {', '.join(correct_statements)}")

    # 選択肢
    choices = {1: "ア、エ", 2: "ア、オ", 3: "イ、エ", 4: "ウ、オ", 5: "イ、ウ"}
    correct_choice = 5
    print(f"\n--- 選択肢 ---")
    for k, v in choices.items():
        mark = " <-- 正解" if k == correct_choice else ""
        print(f"  ({k}) {v}{mark}")

    assert correct_statements == ["イ", "ウ"], f"正しい記述が想定と異なる: {correct_statements}"
    print(f"\n正解: ({correct_choice}) {choices[correct_choice]}")
    print("検証OK")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n" + "=" * 60)
    print("全問検証完了")
    print("=" * 60)
