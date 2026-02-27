"""
問題セット9 解の一意性検証スクリプト

問1: プロジェクト工数管理データ（直接費の逆算）
問2: フランチャイズ店舗収益データ（客単価の逆算）
"""

def verify_q1():
    """
    問1: Dδの直接費（ア）を求める
    
    規則:
    - 工数（人日）= チーム人数 × 作業日数
    - 直接費（万円）= 工数 × 日当単価（全PJで一定）
    - 間接費（万円）= 直接費 × 間接費率 / 100
    - 総費用（万円）= 直接費 + 間接費
    """
    # 既知データ
    projects = [
        {"name": "Aα", "team": 5,  "days": 20, "work": 100, "direct": 300, "indirect": 60,  "total": 360},
        {"name": "Bβ", "team": 8,  "days": 25, "work": 200, "direct": 600, "indirect": 120, "total": 720},
        {"name": "Cγ", "team": 6,  "days": 30, "work": 180, "direct": 540, "indirect": 108, "total": 648},
    ]
    
    # 工数の検証
    for p in projects:
        assert p["work"] == p["team"] * p["days"], f"{p['name']}: 工数={p['team']*p['days']}, 期待={p['work']}"
    print("  工数検証 ✓（工数 = チーム人数 × 作業日数）")
    
    # 日当単価の逆算（全PJで一致を確認）
    unit_prices = [p["direct"] / p["work"] for p in projects]
    assert all(abs(u - unit_prices[0]) < 0.001 for u in unit_prices), \
        f"日当単価が一致しない: {unit_prices}"
    unit_price = unit_prices[0]
    print(f"  日当単価 = {unit_price}万円/人日（全PJ一定）✓")
    
    # 間接費率の確認（全PJで一致を確認）
    indirect_rates = [p["indirect"] / p["direct"] * 100 for p in projects]
    assert all(abs(r - indirect_rates[0]) < 0.001 for r in indirect_rates), \
        f"間接費率が一致しない: {indirect_rates}"
    indirect_rate = indirect_rates[0]
    print(f"  間接費率 = {indirect_rate}%（全PJ一定）✓")
    
    # Dδの計算
    d_team = 10
    d_days = 15
    d_work = d_team * d_days  # = 150人日
    d_direct = unit_price * d_work  # = 3 × 150 = 450万円
    d_indirect = 90  # 与えられた値
    
    # 解の検証
    assert d_work == 150, f"Dδ工数={d_work}, 期待=150"
    print(f"  Dδ工数 = {d_team} × {d_days} = {d_work}人日 ✓")
    
    assert d_direct == 450.0, f"Dδ直接費={d_direct}, 期待=450"
    print(f"  Dδ直接費 = {unit_price} × {d_work} = {d_direct}万円 ✓")
    
    # 間接費整合性確認
    expected_indirect = d_direct * indirect_rate / 100
    assert abs(expected_indirect - d_indirect) < 0.001, \
        f"間接費不一致: 計算={expected_indirect}, 表={d_indirect}"
    print(f"  Dδ間接費率 = {d_indirect}/{d_direct} = {d_indirect/d_direct*100:.0f}%（表と一致）✓")
    
    # 解の一意性確認（選択肢の中で唯一）
    choices = [390, 450, 480, 510, 540]
    valid = [c for c in choices if c * indirect_rate / 100 == d_indirect]
    assert len(valid) == 1, f"有効解が{len(valid)}個: {valid}"
    print(f"  選択肢の中で条件を満たすのは{valid[0]}万円のみ ✓")
    
    print(f"\n  【問1の答え】（ア）= {int(d_direct)}万円")
    return int(d_direct)


def verify_q2():
    """
    問2: S4の客単価（ア）を求める
    
    規則:
    - 月間売上（万円）= 月間客数（人）× 客単価（円）÷ 10,000
    - ロイヤリティ（万円）= 月間売上 × ロイヤリティ率（%）÷ 100
    - 費用（万円）= 月間売上 × 費用率（%）÷ 100
    - 営業利益（万円）= 月間売上 - ロイヤリティ - 費用
    """
    # 既知データ（月間客数は500〜1000人規模の専門店）
    stores = [
        {"name": "S1", "customers": 500,  "unit_price": 4000, "sales": 200, "royalty": 10, "cost": 140, "profit": 50},
        {"name": "S2", "customers": 800,  "unit_price": 5000, "sales": 400, "royalty": 20, "cost": 280, "profit": 100},
        {"name": "S3", "customers": 600,  "unit_price": 5000, "sales": 300, "royalty": 15, "cost": 210, "profit": 75},
    ]
    
    # 月間売上の公式確認
    for s in stores:
        calc_sales = s["customers"] * s["unit_price"] / 10000
        assert abs(calc_sales - s["sales"]) < 0.001, \
            f"{s['name']}: 売上={calc_sales}, 期待={s['sales']}"
    print("  月間売上 = 客数 × 客単価 ÷ 10,000 ✓")
    
    # ロイヤリティ率の確認（全店舗で一致）
    royalty_rates = [s["royalty"] / s["sales"] * 100 for s in stores]
    assert all(abs(r - royalty_rates[0]) < 0.001 for r in royalty_rates), \
        f"ロイヤリティ率が一致しない: {royalty_rates}"
    royalty_rate = royalty_rates[0]
    print(f"  ロイヤリティ率 = {royalty_rate}%（全店舗一定）✓")
    
    # 費用率の確認（全店舗で一致）
    cost_rates = [s["cost"] / s["sales"] * 100 for s in stores]
    assert all(abs(r - cost_rates[0]) < 0.001 for r in cost_rates), \
        f"費用率が一致しない: {cost_rates}"
    cost_rate = cost_rates[0]
    print(f"  費用率 = {cost_rate}%（全店舗一定）✓")
    
    # 利益率の確認
    profit_rates = [s["profit"] / s["sales"] * 100 for s in stores]
    assert all(abs(r - profit_rates[0]) < 0.001 for r in profit_rates), \
        f"利益率が一致しない: {profit_rates}"
    profit_rate = profit_rates[0]
    print(f"  利益率 = {profit_rate}%（全店舗一定）✓")
    print(f"  確認: {royalty_rate}% + {cost_rate}% + {profit_rate}% = {royalty_rate+cost_rate+profit_rate}% ✓")
    
    # S4の計算
    s4_customers = 1000
    s4_royalty = 30  # 与えられた値
    s4_cost = 420    # 与えられた値
    
    # 方法1: ロイヤリティ率から月間売上を逆算
    s4_sales_from_royalty = s4_royalty / (royalty_rate / 100)
    # 方法2: 費用率から月間売上を逆算
    s4_sales_from_cost = s4_cost / (cost_rate / 100)
    
    assert abs(s4_sales_from_royalty - s4_sales_from_cost) < 0.001, \
        f"売上の二通りの計算が一致しない: {s4_sales_from_royalty} vs {s4_sales_from_cost}"
    s4_sales = s4_sales_from_royalty
    print(f"\n  S4月間売上（ロイヤリティから逆算）= {s4_royalty} ÷ {royalty_rate}% = {s4_sales}万円 ✓")
    print(f"  S4月間売上（費用から逆算）= {s4_cost} ÷ {cost_rate}% = {s4_sales_from_cost}万円 ✓")
    
    # 客単価を逆算
    s4_unit_price = s4_sales * 10000 / s4_customers
    print(f"  S4客単価 = {s4_sales} × 10,000 ÷ {s4_customers} = {s4_unit_price}円")
    
    # 解の検証
    assert s4_unit_price == 6000.0, f"客単価={s4_unit_price}, 期待=6000"
    s4_profit = s4_sales - s4_royalty - s4_cost
    assert abs(s4_profit / s4_sales * 100 - profit_rate) < 0.001, \
        f"利益率不一致: {s4_profit/s4_sales*100}% vs {profit_rate}%"
    print(f"  S4利益率 = {s4_profit}/{s4_sales} = {s4_profit/s4_sales*100:.1f}%（全店舗と一致）✓")
    
    # 解の一意性確認（選択肢の中で唯一）
    choices = [4000, 5000, 6000, 7000, 8000]
    valid = []
    for c in choices:
        test_sales = s4_customers * c / 10000
        test_royalty = test_sales * royalty_rate / 100
        test_cost = test_sales * cost_rate / 100
        if abs(test_royalty - s4_royalty) < 0.001 and abs(test_cost - s4_cost) < 0.001:
            valid.append(c)
    assert len(valid) == 1, f"有効解が{len(valid)}個: {valid}"
    print(f"  選択肢の中で条件を満たすのは{valid[0]}円のみ ✓")
    
    print(f"\n  【問2の答え】（ア）= {int(s4_unit_price)}円")
    return int(s4_unit_price)


if __name__ == "__main__":
    print("=" * 50)
    print("問題セット9 検証")
    print("=" * 50)
    
    print("\n【問1: プロジェクト工数管理データ】")
    ans1 = verify_q1()
    
    print("\n【問2: フランチャイズ店舗収益データ】")
    ans2 = verify_q2()
    
    print("\n" + "=" * 50)
    print(f"問1正解: {ans1}万円（選択肢(2)）")
    print(f"問2正解: {ans2}円（選択肢(3)）")
    print("両問題とも解が一意であることを確認 ✓")
