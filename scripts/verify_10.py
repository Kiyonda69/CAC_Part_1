"""
問題9 解の一意性検証

問1: 航空会社の路線別運賃データ（複合割引率の発見と逆算）
  - 正解: 路線Dの正規価格 = 50,000円 → 選択肢(5)

問2: 航空貨物輸送料金データ（重量×距離の複合単価 + 附加料逆算）
  - 正解: 品物Wの輸送距離 = 2,000km → 選択肢(3)
"""

def verify_q1():
    """
    問1検証: 路線別運賃データ
    規則:
      往復割引価格 = 正規価格 × 往復割引率
      会員割引価格 = 往復割引価格 × 会員割引率
      燃油サーチャージ = 飛行距離 × 燃油単価
    """
    print("=" * 50)
    print("問1検証: 路線別運賃データ")
    print("=" * 50)

    data = [
        # (路線, 飛行距離, 正規価格, 往復割引価格, 会員割引価格, 燃油サーチャージ)
        ('A', 1000, 20000, 16000, 12800, 3000),
        ('B', 1500, 30000, 24000, 19200, 4500),
        ('C', 2000, 40000, 32000, 25600, 6000),
    ]
    D = {'距離': 2500, '往復': 40000, '会員': 32000, '燃油': 7500}

    # Step 1: 往復割引率を発見
    early_ratios = [row[3] / row[2] for row in data]  # 往復/正規
    print("【往復割引率の発見】")
    for i, (row, ratio) in enumerate(zip(data, early_ratios)):
        print(f"  路線{row[0]}: {row[3]:,} ÷ {row[2]:,} = {ratio:.4f}")
    assert all(abs(r - early_ratios[0]) < 1e-9 for r in early_ratios), "往復割引率が一定でない"
    early_rate = early_ratios[0]
    print(f"  → 往復割引率 = {early_rate} (= {int(early_rate*100)}%割引)")

    # Step 2: 会員割引率を発見
    member_ratios = [row[4] / row[3] for row in data]  # 会員/往復
    print("\n【会員割引率の発見】")
    for i, (row, ratio) in enumerate(zip(data, member_ratios)):
        print(f"  路線{row[0]}: {row[4]:,} ÷ {row[3]:,} = {ratio:.4f}")
    assert all(abs(r - member_ratios[0]) < 1e-9 for r in member_ratios), "会員割引率が一定でない"
    member_rate = member_ratios[0]
    print(f"  → 会員割引率 = {member_rate} (= {int(member_rate*100)}%割引)")

    # Step 3: 燃油単価を発見
    fuel_rates = [row[5] / row[1] for row in data]  # 燃油/距離
    print("\n【燃油単価の発見】")
    for i, (row, rate) in enumerate(zip(data, fuel_rates)):
        print(f"  路線{row[0]}: {row[5]:,} ÷ {row[1]:,} = {rate:.2f}円/km")
    assert all(abs(r - fuel_rates[0]) < 1e-9 for r in fuel_rates), "燃油単価が一定でない"
    fuel_rate = fuel_rates[0]
    print(f"  → 燃油単価 = {fuel_rate:.1f}円/km")

    # Step 4: 路線Dの正規価格を逆算
    D_reg = D['往復'] / early_rate
    print(f"\n【路線Dの正規価格（ア）を逆算】")
    print(f"  往復割引価格 = 正規価格 × {early_rate}")
    print(f"  正規価格 = {D['往復']:,} ÷ {early_rate} = {D_reg:,.0f}円")

    # 検証（会員割引価格 = 往復割引価格 × 会員割引率 = 正規 × early_rate × member_rate）
    D_round = D_reg * early_rate
    D_member_calc = D_round * member_rate
    assert abs(D_member_calc - D['会員']) < 1e-6, f"会員価格不一致: {D_member_calc} ≠ {D['会員']}"
    assert abs(D['距離'] * fuel_rate - D['燃油']) < 1e-6, "燃油サーチャージ不一致"
    print(f"\n【検証】")
    print(f"  会員割引価格 = 往復({D_round:,.0f}) × {member_rate} = {D_member_calc:,.0f}円 ✓")
    print(f"  燃油サーチャージ = {D['距離']:,} × {fuel_rate:.1f} = {D['距離']*fuel_rate:,.0f}円 ✓")

    # 唯一解確認
    valid = []
    for reg in range(30000, 80001, 1000):
        if abs(reg * early_rate - D['往復']) < 1e-6:
            if abs(reg * early_rate * member_rate - D['会員']) < 1e-6:
                valid.append(reg)
    assert len(valid) == 1, f"解が{len(valid)}個存在: {valid}"
    print(f"\n唯一解確認: {valid[0]:,}円 (唯一解 ✓)")
    print(f"\n正解: (ア) = {int(D_reg):,}円 → 選択肢(5)")
    return int(D_reg)


def verify_q2():
    """
    問2検証: 航空貨物輸送料金データ
    規則:
      基本運賃(円) = 重量(kg) × 距離(km) × 基本単価
      燃料附加料(円) = 基本運賃 × 燃料附加率
      保険料(円) = 基本運賃 × 保険料率
    """
    print("\n" + "=" * 50)
    print("問2検証: 航空貨物輸送料金データ")
    print("=" * 50)

    data = [
        # (品物, 重量, 距離, 基本運賃, 燃料附加料, 保険料, 合計)
        ('X', 100,  1000, 20000,  8000, 2000,  30000),
        ('Y', 200,  1500, 60000, 24000, 6000,  90000),
        ('Z', 150,  2000, 60000, 24000, 6000,  90000),
    ]
    W = {'重量': 250, '燃料附加料': 40000, '保険料': 10000}

    # Step 1: 燃料附加率を発見
    fuel_ratios = [row[4] / row[3] for row in data]
    print("【燃料附加率の発見】")
    for row, ratio in zip(data, fuel_ratios):
        print(f"  品物{row[0]}: {row[4]:,} ÷ {row[3]:,} = {ratio:.4f} (= {int(ratio*10)}/10)")
    assert all(abs(r - fuel_ratios[0]) < 1e-9 for r in fuel_ratios), "燃料附加率が一定でない"
    fuel_rate = fuel_ratios[0]
    print(f"  → 燃料附加率 = {fuel_rate} (基本運賃の{int(fuel_rate*100)}%)")

    # Step 2: 保険料率を発見
    ins_ratios = [row[5] / row[3] for row in data]
    print("\n【保険料率の発見】")
    for row, ratio in zip(data, ins_ratios):
        print(f"  品物{row[0]}: {row[5]:,} ÷ {row[3]:,} = {ratio:.4f} (= 1/10)")
    assert all(abs(r - ins_ratios[0]) < 1e-9 for r in ins_ratios), "保険料率が一定でない"
    ins_rate = ins_ratios[0]
    print(f"  → 保険料率 = {ins_rate} (基本運賃の{int(ins_rate*100)}%)")

    # Step 3: 基本単価を発見（基本運賃 = 重量×距離×単価）
    unit_rates = [row[3] / (row[1] * row[2]) for row in data]
    print("\n【基本単価の発見】")
    for row, rate in zip(data, unit_rates):
        print(f"  品物{row[0]}: {row[3]:,} ÷ ({row[1]} × {row[2]:,}) = {rate:.4f}円/(kg·km)")
    assert all(abs(r - unit_rates[0]) < 1e-9 for r in unit_rates), "基本単価が一定でない"
    unit_rate = unit_rates[0]
    print(f"  → 基本単価 = {unit_rate:.1f}円/(kg·km)")
    print(f"  ※ 品物YとZは重量×距離が同じ(300,000)なので基本運賃も同値")

    # Step 4: 品物Wの基本運賃を逆算
    W_base = W['燃料附加料'] / fuel_rate
    print(f"\n【品物Wの基本運賃を逆算】")
    print(f"  燃料附加料 = 基本運賃 × {fuel_rate}")
    print(f"  基本運賃 = {W['燃料附加料']:,} ÷ {fuel_rate} = {W_base:,.0f}円")

    # 保険料で確認
    assert abs(W_base * ins_rate - W['保険料']) < 1e-6, "保険料不一致"
    print(f"  保険料確認: {W_base:,.0f} × {ins_rate} = {W_base*ins_rate:,.0f}円 ✓")

    # Step 5: 輸送距離を逆算
    W_dist = W_base / (W['重量'] * unit_rate)
    print(f"\n【品物Wの輸送距離（ア）を逆算】")
    print(f"  基本運賃 = 重量 × 距離 × {unit_rate}")
    print(f"  距離 = {W_base:,.0f} ÷ ({W['重量']} × {unit_rate}) = {W_dist:,.0f}km")

    # 唯一解確認
    valid = []
    for dist in range(500, 5001, 50):
        base = W['重量'] * dist * unit_rate
        if abs(base * fuel_rate - W['燃料附加料']) < 1e-6:
            if abs(base * ins_rate - W['保険料']) < 1e-6:
                valid.append(dist)
    assert len(valid) == 1, f"解が{len(valid)}個存在: {valid}"
    print(f"\n唯一解確認: {valid[0]:,}km (唯一解 ✓)")
    print(f"\n正解: (ア) = {int(W_dist):,}km → 選択肢(3)")
    return int(W_dist)


if __name__ == "__main__":
    ans1 = verify_q1()
    ans2 = verify_q2()
    print("\n" + "=" * 50)
    print("【最終確認】")
    print(f"  問1 正解: (ア) = {ans1:,}円 → 選択肢(5)")
    print(f"  問2 正解: (ア) = {ans2:,}km → 選択肢(3)")
