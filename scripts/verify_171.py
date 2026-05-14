"""
航大思考171 解の一意性検証
問1: 5店舗の月間売上の箱ひげ図 → 1つだけ正しい記述を選ぶ
問2: 6部署の月間残業時間の箱ひげ図 → 正しい記述の組合せを選ぶ
"""


def stats(name, data):
    mn, q1, med, q3, mx = data
    return {
        "name": name, "min": mn, "q1": q1, "med": med, "q3": q3, "max": mx,
        "iqr": q3 - q1, "range": mx - mn,
    }


def verify_q1():
    shops = {
        "A": stats("A", (18, 24, 30, 38, 46)),
        "B": stats("B", (22, 28, 34, 40, 48)),
        "C": stats("C", (14, 22, 32, 42, 50)),
        "D": stats("D", (20, 26, 28, 36, 44)),
        "E": stats("E", (24, 30, 36, 42, 46)),
    }

    statements = {
        1: min(shops, key=lambda k: shops[k]["iqr"]) == "D",
        2: max(shops, key=lambda k: shops[k]["med"]) == "B",
        3: shops["C"]["min"] >= 30,
        4: shops["A"]["q1"] > shops["E"]["q1"],
        5: max(shops, key=lambda k: shops[k]["range"]) == "B",
    }

    correct = [k for k, v in statements.items() if v]
    print("問1 各記述の真偽:", statements)
    print("問1 IQR:", {k: v["iqr"] for k, v in shops.items()})
    print("問1 中央値:", {k: v["med"] for k, v in shops.items()})
    print("問1 範囲:", {k: v["range"] for k, v in shops.items()})
    print("問1 正解:", correct)
    assert correct == [1], f"問1の正解が一意でない: {correct}"
    return correct[0]


def verify_q2():
    depts = {
        "営業": stats("営業", (10, 16, 24, 30, 42)),
        "開発": stats("開発", (12, 22, 26, 36, 50)),
        "総務": stats("総務", (4, 10, 14, 20, 28)),
        "人事": stats("人事", (14, 18, 22, 26, 34)),
        "経理": stats("経理", (8, 14, 18, 24, 36)),
        "製造": stats("製造", (16, 22, 30, 38, 46)),
    }

    truth = {
        "ア": max(depts, key=lambda k: depts[k]["med"]) == "製造",
        "イ": depts["開発"]["iqr"] >= depts["人事"]["iqr"] * 2,
        "ウ": max(depts, key=lambda k: depts[k]["max"]) == "開発",
        "エ": depts["総務"]["q3"] > depts["人事"]["q1"],
        "オ": depts["人事"]["range"] > depts["経理"]["range"],
    }

    options = {
        1: {"ア", "イ", "ウ"},
        2: {"ア", "イ", "エ"},
        3: {"ア", "ウ", "エ"},
        4: {"イ", "ウ", "オ"},
        5: {"イ", "エ", "オ"},
    }
    correct_set = {k for k, v in truth.items() if v}
    matched = [opt for opt, s in options.items() if s == correct_set]

    print("問2 各記述の真偽:", truth)
    print("問2 中央値:", {k: v["med"] for k, v in depts.items()})
    print("問2 IQR:", {k: v["iqr"] for k, v in depts.items()})
    print("問2 最大値:", {k: v["max"] for k, v in depts.items()})
    print("問2 範囲:", {k: v["range"] for k, v in depts.items()})
    print("問2 正しい記述:", correct_set)
    print("問2 マッチする選択肢:", matched)
    assert matched == [3], f"問2の正解が一意でない: {matched}"
    return matched[0]


if __name__ == "__main__":
    a1 = verify_q1()
    print()
    a2 = verify_q2()
    print()
    print(f"=> 問1の正解: ({a1})")
    print(f"=> 問2の正解: ({a2})")
