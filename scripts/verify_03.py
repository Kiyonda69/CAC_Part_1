"""
verify_03.py - 航大思考3 解の一意性検証

問1: 商品発注表の空欄穴埋め（標準難度）
問2: 輸送コスト表の空欄穴埋め（高難度）
"""


def verify_q1():
    """
    問1: 商品発注データ表

    計算式:
    - 注文金額 = 単価 × 注文数
    - 請求額 = 注文金額 × (1 - 割引率)

    既知データ:
      商品A: 単価120, 注文数5, 割引率10%, 請求額540
      商品B: 単価200, 注文数3, 割引率15%, 請求額510
      商品C: 単価150, 注文数4, 割引率20%, 請求額480
      商品D: 単価（ア）, 注文数6, 割引率25%, 請求額450

    求め方:
    1. 請求額 = 注文金額 × (1 - 割引率) → 注文金額 = 請求額 / (1 - 割引率)
    2. 単価 = 注文金額 / 注文数
    """
    print("=== 問1: 商品発注表の検証 ===")

    # 既知データの検証
    data = [
        {"name": "A", "unit_price": 120, "quantity": 5, "discount": 0.10, "charge": 540},
        {"name": "B", "unit_price": 200, "quantity": 3, "discount": 0.15, "charge": 510},
        {"name": "C", "unit_price": 150, "quantity": 4, "discount": 0.20, "charge": 480},
    ]

    for d in data:
        order_amount = d["unit_price"] * d["quantity"]
        calc_charge = order_amount * (1 - d["discount"])
        assert abs(calc_charge - d["charge"]) < 0.01, (
            f"商品{d['name']}: 計算結果{calc_charge} != 期待値{d['charge']}"
        )
        print(f"  商品{d['name']}: 注文金額={order_amount}, 請求額={calc_charge} ✓")

    # 商品Dの単価（ア）を求める
    d_discount = 0.25
    d_quantity = 6
    d_charge = 450

    d_order_amount = d_charge / (1 - d_discount)  # = 600
    d_unit_price = d_order_amount / d_quantity     # = 100

    print(f"\n  商品D: 注文金額 = {d_charge} / {1 - d_discount} = {d_order_amount}")
    print(f"  商品D: 単価（ア）= {d_order_amount} / {d_quantity} = {d_unit_price}")

    # 唯一解の確認（総当たりで整数解を検索）
    valid = []
    for candidate in range(1, 1000):
        order_amt = candidate * d_quantity
        charge = order_amt * (1 - d_discount)
        if abs(charge - d_charge) < 0.01:
            valid.append(candidate)

    print(f"\n  整数の候補解: {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個存在: {valid}"
    assert valid[0] == int(d_unit_price), f"計算値と候補が一致しない"

    print(f"\n  正解: （ア）= {valid[0]} 円（唯一解）")
    return valid[0]


def verify_q2():
    """
    問2: 輸送コスト表

    計算式:
    - 運賃 = 基本料金 + 重量料金 × 重量
    - 利益 = 運賃 - 実費
    - 利益率 = 利益 / 運賃

    既知データ:
      ルートP: 基本料金1500, 重量30, 重量料金100, 実費3150
      ルートQ: 基本料金1500, 重量60, 重量料金100, 実費5250
      ルートR: 基本料金2000, 重量80, 重量料金100, 実費7000
      ルートS: 基本料金2000, 重量（ア）, 重量料金100, 実費9800

    求め方:
    1. P,Q,Rの利益率を計算し、共通のパターンを発見（全て30%）
    2. Sの利益率=30%を前提に、連立方程式を解く
       利益 = 運賃 × 0.30 かつ 利益 = 運賃 - 9800
       → 0.30×運賃 = 運賃 - 9800
       → 0.70×運賃 = 9800
       → 運賃 = 14000
    3. 運賃 = 基本料金 + 重量料金×重量
       14000 = 2000 + 100×（ア）
       → （ア）= 120
    """
    print("\n=== 問2: 輸送コスト表の検証 ===")

    weight_rate = 100  # 重量料金(円/kg)

    # 既知データの検証
    routes = [
        {"name": "P", "base": 1500, "weight": 30,  "actual_cost": 3150},
        {"name": "Q", "base": 1500, "weight": 60,  "actual_cost": 5250},
        {"name": "R", "base": 2000, "weight": 80,  "actual_cost": 7000},
    ]

    profit_rates = []
    for r in routes:
        fare = r["base"] + weight_rate * r["weight"]
        profit = fare - r["actual_cost"]
        profit_rate = profit / fare
        profit_rates.append(profit_rate)
        print(f"  ルート{r['name']}: 運賃={fare}, 利益={profit}, 利益率={profit_rate:.4f}")

    # 全ルートの利益率が等しいことを確認
    assert all(abs(pr - profit_rates[0]) < 0.0001 for pr in profit_rates), \
        f"利益率が一致しない: {profit_rates}"
    common_rate = profit_rates[0]
    print(f"\n  共通利益率: {common_rate:.4f} = {common_rate*100:.1f}%")

    # ルートSの重量（ア）を求める
    s_base = 2000
    s_actual = 9800

    # 利益率 = (運賃 - 実費) / 運賃 = common_rate
    # (1 - common_rate) × 運賃 = 実費
    s_fare = s_actual / (1 - common_rate)
    s_weight = (s_fare - s_base) / weight_rate

    print(f"\n  ルートS: 実費={s_actual}")
    print(f"  ルートS: 運賃 = {s_actual} / {1 - common_rate} = {s_fare}")
    print(f"  ルートS: 重量（ア）= ({s_fare} - {s_base}) / {weight_rate} = {s_weight}")

    # 唯一解の確認（整数の重量で検索）
    valid = []
    for candidate in range(1, 1000):
        fare = s_base + weight_rate * candidate
        profit = fare - s_actual
        if fare > 0:
            rate = profit / fare
            if abs(rate - common_rate) < 0.0001:
                valid.append(candidate)

    print(f"\n  整数の候補解: {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個存在: {valid}"
    assert valid[0] == int(s_weight), f"計算値と候補が一致しない"

    print(f"\n  正解: （ア）= {valid[0]} kg（唯一解）")
    return valid[0]


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()

    print("\n" + "=" * 40)
    print(f"問1の正解: {q1_answer} 円")
    print(f"問2の正解: {q2_answer} kg")
    print("両問とも唯一解が確認されました。")
