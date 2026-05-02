"""航大思考146 解の一意性検証"""


def verify_q1():
    """問1: 月別売上表の空欄セル値"""
    A = [120, 135, 148, 162, 175, 180]
    B = [95, 108, 115, 122, 130, 138]
    # C[3]が空欄(7月)
    C = [110, 125, 132, None, 150, 158]
    D = [85, 92, 98, 105, 112, 118]
    E = [145, 158, 165, 172, 180, 188]

    # 各店舗の合計
    sum_A = sum(A)
    sum_B = sum(B)
    sum_D = sum(D)
    sum_E = sum(E)
    sum_C_known = sum(c for c in C if c is not None)

    # 各月の合計
    months_total = []
    for m in range(6):
        if m == 3:
            t = A[m] + B[m] + D[m] + E[m]
        else:
            t = A[m] + B[m] + C[m] + D[m] + E[m]
        months_total.append(t)

    # 全体合計を提示する場合
    total = 4060
    answer = total - sum_A - sum_B - sum_C_known - sum_D - sum_E

    # 検算: 7月合計700と仮定
    july_total = 700
    answer_via_july = july_total - A[3] - B[3] - D[3] - E[3]

    # C店舗合計814と仮定
    c_total = 814
    answer_via_c = c_total - sum_C_known

    print(f"問1: 全体逆算={answer}, 7月逆算={answer_via_july}, C店舗逆算={answer_via_c}")
    assert answer == 139
    assert answer_via_july == 139
    assert answer_via_c == 139

    # 各月合計表示
    print(f"4月={months_total[0]}, 5月={months_total[1]}, 6月={months_total[2]}, 7月(?除く)={months_total[3]}, 8月={months_total[4]}, 9月={months_total[5]}")
    print(f"店舗合計: A={sum_A}, B={sum_B}, D={sum_D}, E={sum_E}, C(?除く)={sum_C_known}")

    return 139


def verify_q2():
    """問2: 複数資料を組み合わせた購入個数"""
    # 会員ランク割引
    rank_discount = {"silver": 0.05, "gold": 0.10, "platinum": 0.15, "black": 0.20}
    birthday_bonus = {"silver": 0.03, "gold": 0.05, "platinum": 0.07, "black": 0.10}
    # 月キャンペーン (3月: 春の感謝祭5%)
    month_campaign = {1: 0.08, 2: 0.04, 3: 0.05, 4: 0.06, 5: 0.07, 6: 0.03}
    # カテゴリ単価
    prices = {"X": 1500, "Y": 2800, "Z": 2200, "W": 3500, "V": 4200}

    # 田中氏: ゴールド、誕生月3月、3月購入
    discount = rank_discount["gold"] + birthday_bonus["gold"] + month_campaign[3]
    assert abs(discount - 0.20) < 1e-9

    # 購入: X×3, Y×?, Z×1, W×2
    target_paid = 24400
    candidates = []
    for n in range(0, 20):
        before = prices["X"] * 3 + prices["Y"] * n + prices["Z"] * 1 + prices["W"] * 2
        after = before * (1 - discount)
        if abs(after - target_paid) < 0.5:
            candidates.append(n)

    print(f"問2: 候補={candidates}")
    assert candidates == [6], f"解が一意でない: {candidates}"

    # 検算
    n = 6
    before = prices["X"] * 3 + prices["Y"] * n + prices["Z"] * 1 + prices["W"] * 2
    after = before * 0.80
    print(f"問2検算: 割引前={before}円, 割引後={after}円")
    assert before == 30500
    assert after == 24400

    return 6


if __name__ == "__main__":
    a1 = verify_q1()
    a2 = verify_q2()
    print(f"\n問1正解: {a1} (選択肢(1))")
    print(f"問2正解: {a2} (選択肢(3))")
