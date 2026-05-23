"""
セット182: 資料空欄穴埋め問題の解の一意性検証

問1: スポーツクラブの会員数報告書
問2: 商品別月次生産量の連鎖推論
"""


def verify_q1():
    """
    問1: スポーツクラブ「アクシス」会員数
    総会員数360名
    ヨガ = 全体の25%
    スイミング = 130名（与えられている）
    テニス = スイミングの半分
    ダンス = ヨガより15名少ない
    """
    total = 360
    swimming_given = 130

    yoga = total * 0.25
    tennis = swimming_given / 2
    dance = yoga - 15

    # 検算: 合計が360になることを確認
    sum_check = yoga + swimming_given + tennis + dance
    assert sum_check == total, f"合計が一致しない: {sum_check}"
    assert yoga == int(yoga), "ヨガが整数でない"
    assert tennis == int(tennis), "テニスが整数でない"
    assert dance == int(dance), "ダンスが整数でない"

    print(f"問1の解:")
    print(f"  ア (ヨガ)    = {int(yoga)}")
    print(f"  イ (テニス)  = {int(tennis)}")
    print(f"  ウ (ダンス)  = {int(dance)}")
    print(f"  検算: 合計 = {int(sum_check)} = 360 ✓")
    return int(yoga), int(tennis), int(dance)


def verify_q2():
    """
    問2: 商品別月次生産量（A, B, C）

    7月: A:B:C = 5:4:3, 合計 12,000個
    8月: A = 7月Aの10%増, B = 7月B - 500, C = 7月Cと同じ
    9月: 合計 = 8月合計 + 500
         A = 8月Aの80%
         B = 9月合計の30%

    求めるもの:
      ア = 8月A
      イ = 9月B
      ウ = 9月C
    """
    jul_total = 12000
    jul_a = jul_total * 5 / 12
    jul_b = jul_total * 4 / 12
    jul_c = jul_total * 3 / 12
    assert jul_a == 5000 and jul_b == 4000 and jul_c == 3000

    # 8月
    aug_a = jul_a * 1.10  # 10%増
    aug_b = jul_b - 500
    aug_c = jul_c
    aug_total = aug_a + aug_b + aug_c

    # 9月
    sep_total = aug_total + 500
    sep_a = aug_a * 0.80
    sep_b = sep_total * 0.30
    sep_c = sep_total - sep_a - sep_b

    # すべて整数か確認
    for name, val in [("8月A", aug_a), ("9月A", sep_a),
                      ("9月B", sep_b), ("9月C", sep_c),
                      ("9月合計", sep_total), ("8月合計", aug_total)]:
        assert val == int(val), f"{name}が整数でない: {val}"

    print(f"\n問2の解:")
    print(f"  7月: A={int(jul_a)}, B={int(jul_b)}, C={int(jul_c)}, 合計={jul_total}")
    print(f"  8月: A=（ア）={int(aug_a)}, B={int(aug_b)}, C={int(aug_c)}, 合計={int(aug_total)}")
    print(f"  9月: A={int(sep_a)}, B=（イ）={int(sep_b)}, C=（ウ）={int(sep_c)}, 合計={int(sep_total)}")
    print(f"  検算: 9月合計 = {int(sep_a)}+{int(sep_b)}+{int(sep_c)} = {int(sep_a+sep_b+sep_c)} = {int(sep_total)} ✓")
    return int(aug_a), int(sep_b), int(sep_c)


def verify_options():
    """選択肢の妥当性検証"""
    q1_ans = verify_q1()
    q2_ans = verify_q2()

    # 問1選択肢
    q1_options = [
        (72, 65, 57),    # (1) 20%と誤算
        (90, 260, 75),   # (2) テニス×2と誤読
        (90, 65, 75),    # (3) 正解
        (90, 65, 105),   # (4) 符号誤り: 90+15
        (120, 65, 105),  # (5) 33.3%と誤算
    ]
    correct_q1 = 3
    assert q1_options[correct_q1 - 1] == q1_ans, "問1の正解が一致しない"

    # 問2選択肢
    q2_options = [
        (5500, 3750, 3000),  # (1) 9月Cを8月Cと同じと誤解
        (5500, 3600, 4000),  # (2) 9月合計を12,000のままで計算
        (5500, 3750, 4350),  # (3) 正解
        (5050, 3750, 4350),  # (4) 10%増加を50増加と誤算
        (5500, 4400, 3700),  # (5) 9月Bを9月Aと同じと誤読
    ]
    correct_q2 = 3
    assert q2_options[correct_q2 - 1] == q2_ans, "問2の正解が一致しない"

    print(f"\n問1正解: ({correct_q1}) {q1_options[correct_q1 - 1]}")
    print(f"問2正解: ({correct_q2}) {q2_options[correct_q2 - 1]}")
    print("\n✓ すべての検証が成功しました")


if __name__ == "__main__":
    verify_options()
