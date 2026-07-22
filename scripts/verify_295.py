#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""航大思考295 検証: 資料解釈の空欄穴埋め（大量計算型）"""

def verify_q1():
    """問1: 図書館貸出冊数の空欄ア・イ・ウ"""
    # 表データ: 館: (2023年度, 2024年度, 増減率%)
    # B館2023=ア, C館2024=イ, 合計2023=ウ
    a2023, a2024 = 12400, 13020
    b2024, b_rate = 16940, 10.0
    c2023, c_rate = 18600, -5.0
    d2023, d2024 = 9800, 10290
    e2023, e2024 = 15500, 14880

    # 表記載の増減率が整合するか確認
    assert abs(a2024 / a2023 - 1.05) < 1e-9, "A館増減率不整合"
    assert abs(d2024 / d2023 - 1.05) < 1e-9, "D館増減率不整合"
    assert abs(e2024 / e2023 - 0.96) < 1e-9, "E館増減率不整合"

    # ア: B館2023 = 16940 / 1.10（唯一に決まる）
    ans_a = round(b2024 / (1 + b_rate / 100))
    assert ans_a * 11 == b2024 * 10, "ア: 割り切れない"
    assert ans_a == 15400, f"ア={ans_a}"
    # イ: C館2024 = 18600 * 0.95
    ans_i = c2023 * (1 + c_rate / 100)
    assert ans_i == 17670, f"イ={ans_i}"
    # ウ: 合計2023
    ans_u = a2023 + ans_a + c2023 + d2023 + e2023
    assert ans_u == 71700, f"ウ={ans_u}"
    # 整合性: 2024合計（表に記載）
    total2024 = a2024 + b2024 + ans_i + d2024 + e2024
    assert total2024 == 72800, f"2024合計={total2024}"

    # 一意性: ア候補を総当たりし +10.0% になるのは 15400 のみ
    cands = [x for x in range(10000, 20001)
             if abs(b2024 / x - 1.10) < 5e-4]  # 表示は小数1桁 → ±0.05%
    # 10.0%表示（9.95〜10.05%）に入る整数は複数あるが、割り切れる値は一意
    exact = [x for x in cands if b2024 * 10 == x * 11]
    assert exact == [15400], f"ア一意性NG: {exact}"

    # 罠の値
    trap_a = round(b2024 * 0.90)        # 15246: 2024年から10%引く誤り
    trap_i = round(c2023 * 1.05)        # 19530: 5%増と取り違え
    trap_u_1 = a2023 + trap_a + c2023 + d2023 + e2023  # 71546
    assert (trap_a, trap_i, trap_u_1) == (15246, 19530, 71546)
    print("問1 OK: ア=15,400 イ=17,670 ウ=71,700")

def verify_q2():
    """問2: 農産物産出額の空欄ア〜エ"""
    # 表(億円): 品目: [2022, 2023, 2024]
    rice = [480, None, 462]     # 2023=ア
    veg = [650, 702, None]      # 2024=イ
    fruit = [None, 380, 399]    # 2022=ウ
    livestock = [570, 590, 630]
    total = [2100, 2128, None]  # 2024=エ

    # ア: 2023年合計からの引き算
    ans_a = total[1] - veg[1] - fruit[1] - livestock[1]
    assert ans_a == 456, f"ア={ans_a}"
    # 参考: 米2023は2022年比5%減とも整合
    assert rice[0] * 0.95 == ans_a

    # イ: 野菜2024は2022年比20%増（順算）
    ans_i = veg[0] * 1.20
    assert ans_i == 780, f"イ={ans_i}"

    # ウ: 果実2023(380)は2022年比5%減 → 逆算
    ans_u = fruit[1] / 0.95
    assert ans_u == 400, f"ウ={ans_u}"
    # 2022年合計との整合
    assert rice[0] + veg[0] + ans_u + livestock[0] == total[0]
    # 果実2024の増加率も確認(380→399は+5%)
    assert abs(fruit[2] / fruit[1] - 1.05) < 1e-9

    # エ: 2024年合計
    ans_e = rice[2] + ans_i + fruit[2] + livestock[3 - 3 + 2]
    assert ans_e == 2271, f"エ={ans_e}"

    # 一意性: ウ候補総当たり（×0.95がちょうど380になる整数は400のみ）
    exact = [x for x in range(100, 1001) if x * 95 == 380 * 100]
    assert exact == [400], f"ウ一意性NG: {exact}"

    # 罠の値
    trap_u = round(fruit[1] * 0.95)          # 361: 逆算せず掛けてしまう
    trap_a = total[1] - (650 + 380 + 570)    # 528: 2022年の野菜で引く
    trap_i = round(veg[1] * 1.20)            # 842: 2023年基準で20%増
    trap_e_i = rice[2] + trap_i + fruit[2] + livestock[2]  # 2333
    trap_e = ans_e - 100                      # 2171: 単純な集計ミス
    assert (trap_u, trap_a, trap_i, trap_e_i, trap_e) == (361, 528, 842, 2333, 2171)
    print("問2 OK: ア=456 イ=780 ウ=400 エ=2,271")

if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証パス: 解は一意")
