"""
航大思考145 解の一意性検証
- 問1: 5社の人事データ表から複数条件を満たす会社を選ぶ
- 問2: 飲食チェーン5店舗のグラフ+表から複数条件を満たす店舗を選ぶ
"""


def verify_q1():
    """問1: 6項目×5社の表データ"""
    # (社員数, 女性比率%, 平均年齢, 平均年収万円, 平均勤続年数, 月平均残業時間)
    companies = {
        "A": (180, 40, 35, 510, 5.5, 25),
        "B": (320, 28, 37, 540, 7.0, 28),
        "C": (250, 35, 36, 520, 6.5, 22),
        "D": (280, 32, 39, 530, 6.0, 26),
        "E": (220, 36, 38, 480, 5.8, 35),
    }
    valid = []
    for name, (n, fr, age, salary, tenure, ot) in companies.items():
        if n >= 200 and fr >= 30 and age <= 38 and salary >= 500 and tenure >= 5 and ot <= 30:
            valid.append(name)
    print(f"問1: 条件を満たす会社 = {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    assert valid[0] == "C", f"想定はC社、実際は{valid[0]}"
    return valid[0]


def verify_q2():
    """問2: 来客数グラフ+項目表"""
    # (Q1, Q2, Q3, Q4 人/月), (客単価, リピート率, 食品比率, 飲料比率, 新規顧客比率)
    stores = {
        "A": ((800, 850, 900, 950), (1400, 65, 55, 20, 25)),
        "B": ((1000, 1100, 1050, 1200), (1600, 70, 60, 25, 20)),
        "C": ((900, 950, 1100, 1150), (1550, 55, 50, 35, 22)),
        "D": ((750, 850, 950, 1100), (1700, 72, 55, 28, 18)),
        "E": ((800, 880, 980, 1050), (1850, 62, 45, 30, 15)),
    }
    valid = []
    for name, (q, t) in stores.items():
        price, repeat, food, drink, new = t
        cond_a = q[0] < q[1] < q[2] < q[3]
        cond_b = price >= 1500
        cond_c = repeat >= 60
        cond_d = q[3] * price >= 1_800_000
        cond_e = food + drink >= 80
        if cond_a and cond_b and cond_c and cond_d and cond_e:
            valid.append(name)
    print(f"問2: 条件を満たす店舗 = {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    assert valid[0] == "D", f"想定はD店、実際は{valid[0]}"
    return valid[0]


if __name__ == "__main__":
    a1 = verify_q1()
    a2 = verify_q2()
    print(f"\n問1正解: {a1}社 (選択肢(3))")
    print(f"問2正解: {a2}店 (選択肢(4))")
