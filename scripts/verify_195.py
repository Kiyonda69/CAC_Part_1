# -*- coding: utf-8 -*-
"""
航大思考195 検証スクリプト
資料の空欄穴埋め問題（売上集計・損益計算）
"""


def verify_q1():
    """
    問1: 4店舗売上集計表の穴埋め
    商品A=750円, 商品B=1,200円, 商品C=900円
    """
    A, B, C = 750, 1200, 900

    # 与えられた値
    east_A, east_C = 124, 88
    east_total = 286_200

    west_A, west_C = 108, 112
    west_total = 273_000

    south_A, south_B, south_C = 96, 134, 67

    north_A, north_B = 142, 88
    north_total = 306_600

    # 空欄1: 東店の合計売上
    east_B = 95
    calc_east_total = A * east_A + B * east_B + C * east_C
    assert calc_east_total == east_total, f"East mismatch: {calc_east_total}"

    # 空欄2: 西店のB個数（売上から逆算）
    calc_west_B = (west_total - A * west_A - C * west_C) // B
    assert (west_total - A * west_A - C * west_C) % B == 0
    assert calc_west_B == 76, f"West B = {calc_west_B}"

    # 空欄3: 南店の合計売上
    south_total = A * south_A + B * south_B + C * south_C
    assert south_total == 293_100, f"South total = {south_total}"

    # 空欄4: 北店のC個数（売上から逆算）
    calc_north_C = (north_total - A * north_A - B * north_B) // C
    assert (north_total - A * north_A - B * north_B) % C == 0
    assert calc_north_C == 105, f"North C = {calc_north_C}"

    # 4店舗合計売上
    total = east_total + west_total + south_total + north_total
    print(f"問1 4店舗合計売上 = {total:,} 円")
    assert total == 1_158_900, f"Total = {total}"

    # 選択肢
    options = [1_142_300, 1_151_500, 1_154_700, 1_158_900, 1_167_200]
    correct_idx = options.index(1_158_900) + 1
    print(f"問1 正解は選択肢({correct_idx})")
    assert correct_idx == 4
    return total


def verify_q2():
    """
    問2: 4製品の損益計算表
    売上 × 原価率 = 原価
    売上 - 原価 = 粗利
    粗利 - 販売費 = 営業利益
    """
    # 製品Aの値
    A_sales = 1200
    A_cost_rate = 0.60
    A_cost = A_sales * A_cost_rate
    A_gross = A_sales - A_cost
    A_sg = 200
    A_op = A_gross - A_sg
    assert A_cost == 720
    assert A_gross == 480
    assert A_op == 280

    # 製品B
    B_cost = 440
    B_cost_rate = 0.55
    B_sales = round(B_cost / B_cost_rate)
    B_gross = B_sales - B_cost
    B_op = 210
    B_sg = B_gross - B_op
    assert B_sales == 800, B_sales
    assert B_gross == 360
    assert B_sg == 150

    # 製品C
    C_sales = 1500
    C_cost = 1020
    C_cost_rate = C_cost / C_sales
    C_gross = C_sales - C_cost
    C_sg = 240
    C_op = C_gross - C_sg
    assert C_cost_rate == 0.68
    assert C_gross == 480
    assert C_op == 240

    # 製品D
    D_cost_rate = 0.72
    D_gross = 280
    D_sales = round(D_gross / (1 - D_cost_rate))
    D_cost = D_sales - D_gross
    D_sg = 140
    D_op = D_gross - D_sg
    assert D_sales == 1000, D_sales
    assert D_cost == 720
    assert D_op == 140

    total_op = A_op + B_op + C_op + D_op
    print(f"問2 営業利益合計 = {total_op} 万円")
    assert total_op == 870

    # 選択肢
    options = [850, 870, 880, 890, 920]
    correct_idx = options.index(870) + 1
    print(f"問2 正解は選択肢({correct_idx})")
    assert correct_idx == 2
    return total_op


if __name__ == "__main__":
    print("=" * 50)
    print("航大思考195 検証")
    print("=" * 50)
    verify_q1()
    verify_q2()
    print("=" * 50)
    print("全テスト合格")
